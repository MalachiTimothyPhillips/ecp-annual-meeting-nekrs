import glob
import os
import re
import numpy as np
import matplotlib.pyplot as plt
import common
import util
def sanitize_method(method):
  sanitized = "".join(method.split())
  sanitized = sanitized.replace("Chebyshev", "Cheby")
  sanitized = sanitized.replace("Jacobi", "Jac")
  sanitized = sanitized.replace("+Degree=", "(")
  sanitized = sanitized.replace(",(", "),(")
  sanitized = sanitized.replace("+", "-")
  return sanitized
def parse_method(method):
  print(method)
  regex = "Cheby-(.+?)\((\d)\),(.+)"
  m = re.search(regex, method)
  return m.groups()

def parse_real_solver_time(baseDir, nodes, methods):
  methodToData=dict()
  pressureSolveRegex = "pressureSolve(\s+)(.+?)s"
  fastestSolverRegex = "Fastest solver : (.+)"
  for node in nodes:
      autoLogFile = common.grab_latest_logfile(f"{baseDir}/fp32/auto-{node}")
      #autoLogFile = common.grab_all_logfiles(f"{baseDir}/fp32/auto-{node}")[1] # 2nd most recent
      defaultLogFile = common.grab_latest_logfile(f"{baseDir}/fp32/cheby-asm-{node}")

      worstSolverTime = -np.inf
      worstSolver = ""

      bestSolverTime = np.inf
      bestSolver = ""

      def solveTimes(logfile):
        print(logfile)
        if os.path.isfile(logfile):
          solverTimes = util.field_by_regex(pressureSolveRegex, logfile, 1)
          fastestSolver = util.field_by_regex(fastestSolverRegex, logfile, 0, str)
          if fastestSolver:
            fastestSolver = fastestSolver[0]
          if solverTimes:
            solverTimes = np.asarray(solverTimes)
            return solverTimes[-1] - solverTimes[-3], fastestSolver
          return None, None
        return None, None
      
      for method in methods:
        methodLogFile = common.grab_latest_logfile(f"{baseDir}/fp32/{method}-{node}")
        solverTime, _ = solveTimes(methodLogFile)
        if solverTime:
          if solverTime > worstSolverTime:
            worstSolverTime = solverTime
            worstSolver = method
          if solverTime < bestSolverTime:
            bestSolverTime = solverTime
            bestSolver = method

      autoSolverTime, fastestSolver = solveTimes(autoLogFile)
      if not fastestSolver: continue
      solver = sanitize_method(fastestSolver)
      bestSmootherType, bestOrder, bestSchedule = parse_method(solver)
      realMethodName = ""
      if bestOrder != "2":
        realMethodName = f"cheby-{bestSmootherType.lower()}-{bestOrder}"
      else:
        realMethodName = f"cheby-{bestSmootherType.lower()}"
      print(realMethodName)
      actualLogFile = common.grab_latest_logfile(f"{baseDir}/fp32/{realMethodName}-{node}")
      print(actualLogFile)
      actualAutoSolverTime, _ = solveTimes(actualLogFile)
      if actualAutoSolverTime:
        # noisy, take min
        autoSolverTime = min(autoSolverTime, actualAutoSolverTime)


      defaultSolverTime, _          = solveTimes(defaultLogFile)
      methodToData[node] = dict()
      methodToData[node]["default"] = ("default", defaultSolverTime)
      methodToData[node]["auto"] = (fastestSolver, autoSolverTime)
      methodToData[node]["worst"] = (worstSolver, worstSolverTime)
      methodToData[node]["best"] = (bestSolver, bestSolverTime)

  return methodToData

def table_start():
  table = "\\begin{table*}\n\centering\n"
  table += "\\begin{tabular}{||c|| c| c| c| c| c| c| c| c||}\n"
  table += "\t\\hline\n"
  table += "\tCase & $P$ ($n/P$) & Auto & Best & Worst & $T_p$ & $S_D$ & $S_B$ & $S_W$\\\\\n"
  table += "\t\\hline\\hline\n"
  return table
def table_end():
    table = "\\hline\n"
    table += "\\end{tabular}\n"
    table += "\\caption{\label{table:foobar}}\n"
    table += "\\end{table*}\n"
    return table
def make_table(casename, n, methodToData):
  table = ""
  for node in methodToData.keys():
    autoMethod, autoTime = methodToData[node]["auto"]
    defaultMethod, defaultTime = methodToData[node]["default"]
    worstMethod, worstTime = methodToData[node]["worst"]
    bestMethod, bestTime = methodToData[node]["best"]
    speedupDefault = defaultTime / autoTime
    speedupWorst = worstTime / autoTime
    speedupBest = bestTime / autoTime

    table += f"\t{casename}\t&\t{int(node*6)}\t({round((n/(6*node))*1e-6,2)}M)\t&"
    table += f"\t{autoMethod}\t&\t{bestMethod}\t&{worstMethod}\t&"
    table += f"\t{round(autoTime,3)}\t&\t{round(speedupDefault,2)}\t&{round(speedupBest,2)}\t&\t{round(speedupWorst,2)}\\\\\n"
  return table

if __name__ == "__main__":
  ranksPerNode=6
  def gen():
    table = ""
    table += table_start()
    E = 62132
    p = 7
    n = E * p ** 3.0
    nodes=[1,2,3]
    data = parse_real_solver_time(f"../data/summit/scaling/pb146",
      nodes,
      common.methodToName)
    #print(data)

    table += make_table("146 pebble", n, data)

    E = 524386
    p = 7
    n = E * p ** 3.0
    nodes=[8,12,16]
    data = parse_real_solver_time(f"../data/summit/scaling/pb1568",
      nodes,
      common.methodToName)
    #print(data)

    table += make_table("1568 pebble", n, data)

    #E = 884736
    #p = 9
    #n = E * p ** 3.0
    #nodes=[24,36,48,60,72]
    #data = parse_real_solver_time(f"../data/summit/scaling/BoeingSpeedBump",
    #  nodes,
    #  common.methodToNameBSB)
    ##print(data)

    #table += make_table("speed bump", n, data)

    table += table_end()
    print(table)
  gen()