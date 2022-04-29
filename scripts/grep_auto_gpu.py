import glob
import os
import re
import numpy as np
import matplotlib.pyplot as plt
import common

def parse_marker(methodName):
  orderRegex = "\+\((.+?)\),"
  m = re.search(orderRegex, methodName)
  assert m
  order = int(m.groups()[0])
  if order == 1:
    return "v"
  if order == 2:
    return "o"
  if order == 3:
    return "x"
  else:
    return "fail"

def parse_linestyle(methodName):
  scheduleRegex = ",\((.+?)\)"
  m = re.search(scheduleRegex, methodName)
  assert m
  schedule = m.groups()[0]
  nLevels = schedule.count(",") + 1
  if nLevels == 3:
    return "solid"
  if nLevels == 4:
    return "dotted"
  else:
    return "fail"
  

def parse_log(regex,log_file_name, skipStr = "someDummyString", fieldnum = 0, returnType = float):
    with open(log_file_name) as log_file:
        content =log_file.readlines()
    content = [x.strip() for x in content]
    field=[]
    for line in content:
        if skipStr in line:
          continue
        m = re.search(regex,line)
        if m:
          try:
            field.append(returnType(m.groups()[fieldnum]))
          except:
            pass
    return field

def parse_auto_solver_time(baseDir, nodes):
  methodToData=dict()
  autoSolveRegex = "\|(.+?)\|(.+?)\|(.+?)\/(.+?)\|"

  for node in nodes:
      logfile = common.grab_latest_logfile(f"{baseDir}/fp32/auto-{node}")
      #print(logfile)
      if os.path.isfile(logfile):
        methods = parse_log(autoSolveRegex, logfile, "Preconditioner", 0, str)
        iterations = parse_log(autoSolveRegex, logfile, "Preconditioner", 1, int)
        minSolverTimes = parse_log(autoSolveRegex, logfile, "Preconditioner", 2, float)
        maxSolverTimes = parse_log(autoSolveRegex, logfile, "Preconditioner", 3, float)
        if methods:
          methods = np.asarray(methods)
          iterations = np.asarray(iterations)
          minSolverTimes = np.asarray(minSolverTimes)
          maxSolverTimes = np.asarray(maxSolverTimes)
          for method, iteration, minSolve, maxSolve in zip(methods, iterations, minSolverTimes, maxSolverTimes):
            if not method in methodToData:
              methodToData[method] = []
            methodToData[method].append((node, iteration, minSolve, maxSolve))
  return methodToData

def make_plot(methodToData):
  for method in methodToData.keys():
    shortMethodName = "".join(method.split())
    shortMethodName = shortMethodName.replace("Chebyshev", "Cheby")
    shortMethodName = shortMethodName.replace("Jacobi", "Jac")
    shortMethodName = shortMethodName.replace("+Degree=", "(")
    shortMethodName = shortMethodName.replace(",(", "),(")
    shortMethodName = shortMethodName.replace("+", "-")
    nodes = []
    minSolveTimes = []
    maxSolveTimes = []
    for (node, iteration, minSolve, maxSolve) in methodToData[method]:
      minSolveTimes.append(minSolve)
      maxSolveTimes.append(maxSolve)
      nodes.append(node)
    nodes = np.asarray(nodes)
    minSolveTimes = np.asarray(minSolveTimes)
    maxSolveTimes = np.asarray(maxSolveTimes)
    errors = (maxSolveTimes-minSolveTimes)*0.5
    plt.errorbar(6*nodes, minSolveTimes, yerr = errors, label=shortMethodName,
      color = common.grab_color(shortMethodName),
      marker=parse_marker(shortMethodName),
      lineStyle=parse_linestyle(shortMethodName))
  plt.xscale("log")
  plt.xlabel("Ranks")
  plt.ylabel("Time per solve (s)")
  plt.grid(which="both")
  plt.legend(prop={'size':6})
  plt.show()

def make_speedup_plot(methodToData, defaultPreconditioner):
  defaultName = "".join(defaultPreconditioner.split())
  defaultMinTimes = []
  defaultMaxTimes = []
  for method in methodToData.keys():
    if defaultName in method:
      for (node, iteration, minSolve, maxSolve) in methodToData[method]:
        defaultMinTimes.append(minSolve)
        defaultMaxTimes.append(maxSolve)
  defaultMinTimes = np.asarray(defaultMinTimes)
  defaultMaxTimes = np.asarray(defaultMaxTimes)

  for method in methodToData.keys():
    # include the default...
    #if defaultName in method: continue
    shortMethodName = "".join(method.split())
    shortMethodName = shortMethodName.replace("Chebyshev", "Cheby")
    shortMethodName = shortMethodName.replace("Jacobi", "Jac")
    shortMethodName = shortMethodName.replace("+Degree=", "(")
    shortMethodName = shortMethodName.replace(",(", "),(")
    shortMethodName = shortMethodName.replace("+", "-")
    nodes = []
    minSolveTimes = []
    maxSolveTimes = []
    for (node, iteration, minSolve, maxSolve) in methodToData[method]:
      minSolveTimes.append(minSolve)
      maxSolveTimes.append(maxSolve)
      nodes.append(node)
    nodes = np.asarray(nodes)
    minSolveTimes = np.asarray(minSolveTimes)
    maxSolveTimes = np.asarray(maxSolveTimes)
    speedup = defaultMinTimes / minSolveTimes
    plt.plot(6*nodes, speedup, label=shortMethodName,
      color = common.grab_color(shortMethodName),
      marker=parse_marker(shortMethodName),
      lineStyle=parse_linestyle(shortMethodName))
  plt.xscale("log")
  plt.xlabel("Ranks")
  plt.ylabel("Relative Speedup to Default")
  plt.grid(which="both")
  plt.legend(prop={'size':6})
  plt.show()

def make_speedup_over_worst(methodToData):
  worstSolver = dict()
  worstSolverTimes = dict()
  # initial reduction for the worst params
  for method in methodToData.keys():
    nodes = []
    minSolveTimes = []
    for (node, iteration, minSolve, maxSolve) in methodToData[method]:
      minSolveTimes.append(minSolve)
      nodes.append(node)
    nodes = np.asarray(nodes)
    minSolveTimes = np.asarray(minSolveTimes)
    for node, solveTime in zip(nodes, minSolveTimes):
      if not node in worstSolver:
        worstSolver[node] = ""
        worstSolverTimes[node] = -np.inf
      currentWorst = worstSolverTimes[node]
      if solveTime > currentWorst:
        worstSolver[node] = method
        worstSolverTimes[node] = solveTime
  
  worstTimes = []
  for node, time in worstSolverTimes.items():
    worstTimes.append(time)
  
  worstTimes = np.asarray(worstTimes)

  for method in methodToData.keys():
    shortMethodName = "".join(method.split())
    shortMethodName = shortMethodName.replace("Chebyshev", "Cheby")
    shortMethodName = shortMethodName.replace("Jacobi", "Jac")
    shortMethodName = shortMethodName.replace("+Degree=", "(")
    shortMethodName = shortMethodName.replace(",(", "),(")
    shortMethodName = shortMethodName.replace("+", "-")
    nodes = []
    minSolveTimes = []
    maxSolveTimes = []
    for (node, iteration, minSolve, maxSolve) in methodToData[method]:
      minSolveTimes.append(minSolve)
      maxSolveTimes.append(maxSolve)
      nodes.append(node)
    nodes = np.asarray(nodes)
    minSolveTimes = np.asarray(minSolveTimes)
    maxSolveTimes = np.asarray(maxSolveTimes)
    speedup = worstTimes / minSolveTimes
    plt.plot(6*nodes, speedup, label=shortMethodName,
      color = common.grab_color(shortMethodName),
      marker=parse_marker(shortMethodName),
      lineStyle=parse_linestyle(shortMethodName))
  plt.xscale("log")
  plt.xlabel("Ranks")
  plt.ylabel("Relative Speedup to Worst")
  plt.grid(which="both")
  plt.legend(prop={'size':6})
  plt.show()

def table_start():
  table = "\\begin{table*}\n\centering\n"
  table += "\\begin{tabular}{||c|| c| c| c| c| c| c| c||}\n"
  table += "\t\\hline\n"
  table += "\tCase Name & $P$ ($n/P$) & Smoother & Order & Schedule & $T_p$ & $S_D$ & $S_W$\\\\\n"
  table += "\t\\hline\\hline\n"
  return table
def table_end():
    table = "\\hline\n"
    table += "\\end{tabular}\n"
    table += "\\caption{\label{table:foobar}}\n"
    table += "\\end{table*}\n"
    return table
def make_table(casename, n, methodToData, defaultPreconditioner):
  # get default timers
  defaultName = "".join(defaultPreconditioner.split())
  defaultSolverTimes = dict()
  for method in methodToData.keys():
    if defaultName in method:
      for (node, iteration, minSolve, maxSolve) in methodToData[method]:
        defaultSolverTimes[node] = minSolve

  worstSolver = dict()
  worstSolverTimes = dict()
  bestSolver = dict()
  bestSolverTimes = dict()
  # initial reduction for the best/worst params
  for method in methodToData.keys():
    nodes = []
    minSolveTimes = []
    for (node, iteration, minSolve, maxSolve) in methodToData[method]:
      minSolveTimes.append(minSolve)
      nodes.append(node)
    nodes = np.asarray(nodes)
    minSolveTimes = np.asarray(minSolveTimes)
    for node, solveTime in zip(nodes, minSolveTimes):
      if not node in worstSolver:
        worstSolver[node] = ""
        worstSolverTimes[node] = -np.inf
      if not node in bestSolver:
        bestSolver[node] = ""
        bestSolverTimes[node] = np.inf
      currentWorst = worstSolverTimes[node]
      currentBest = bestSolverTimes[node]
      if solveTime > currentWorst:
        worstSolver[node] = method
        worstSolverTimes[node] = solveTime
      if solveTime < currentBest:
        bestSolver[node] = method
        bestSolverTimes[node] = solveTime

  table = ""
  for node in bestSolver.keys():
    bestMethod, bestTime = bestSolver[node], bestSolverTimes[node]
    worstMethod, worstTime = worstSolver[node], worstSolverTimes[node]
    defaultTime = defaultSolverTimes[node]
    def sanitize_method(method):
      sanitized = "".join(method.split())
      sanitized = sanitized.replace("Chebyshev", "Cheby")
      sanitized = sanitized.replace("Jacobi", "Jac")
      sanitized = sanitized.replace("+Degree=", "(")
      sanitized = sanitized.replace(",(", "),(")
      sanitized = sanitized.replace("+", "-")
      return sanitized
    def parse_method(method):
      regex = "Cheby-(.+?)\((\d)\),(.+)"
      m = re.search(regex, method)
      return m.groups()
    
    bestMethod = sanitize_method(bestMethod)
    bestSmootherType, bestOrder, bestSchedule = parse_method(bestMethod)
    speedupDefault = defaultTime / bestTime
    speedupWorst = worstTime / bestTime
    table += f"\t{casename}\t&\t{int(node*6)}\t({round((n/(6*node))*1e-6,2)}M)\t&"
    table += f"\t{bestSmootherType}\t&\t{bestOrder}\t&{bestSchedule}\t&"
    table += f"\t{round(bestTime,3)}\t&\t{round(speedupDefault,2)}\t&{round(speedupWorst,2)}\\\\\n"
  return table


if __name__ == "__main__":
  ranksPerNode=6
  def pb146():
    E = 62132
    p = 7
    n = E * p ** 3.0
    defaultPreconditioner = "Chebyshev+ASM+Degree=2,(7,3,1)"
    nodes=[1,2,3]
    data = parse_auto_solver_time(f"../data/summit/scaling/pb146",
      nodes)
    table = ""
    table += table_start()
    table += make_table("146 pebble", n, data, defaultPreconditioner)
    table += table_end()
    print(table)
    #make_plot(data)
    #make_speedup_plot(data, defaultPreconditioner)
    #make_speedup_over_worst(data)

  def pb1568():
    defaultPreconditioner = "Chebyshev+ASM+Degree=2,(7,3,1)"
    nodes=[6,8,12,16]
    data = parse_auto_solver_time(f"../data/summit/scaling/pb1568",
      nodes)
    #make_plot(data)
    #make_speedup_plot(data, defaultPreconditioner)
    make_speedup_over_worst(data)
  def BoeingSpeedBump():
    defaultPreconditioner = "Chebyshev+ASM+Degree=2,(9,5,1)"
    nodes=[16,24,36,48,60,72]
    data = parse_auto_solver_time(f"../data/summit/scaling/BoeingSpeedBump",
      nodes)
    #make_plot(data)
    #make_speedup_plot(data, defaultPreconditioner)
    make_speedup_over_worst(data)

  #pb146()
  #pb1568()
  #BoeingSpeedBump()

  def gen():
    table = ""
    table += table_start()
    E = 62132
    p = 7
    n = E * p ** 3.0
    defaultPreconditioner = "Chebyshev+ASM+Degree=2,(7,3,1)"
    nodes=[1,2,3]
    data = parse_auto_solver_time(f"../data/summit/scaling/pb146",
      nodes)
    table += make_table("146 pebble", n, data, defaultPreconditioner)

    E = 524386
    p = 7
    n = E * p ** 3.0
    defaultPreconditioner = "Chebyshev+ASM+Degree=2,(7,3,1)"
    nodes=[4,6,8,12,16]
    data = parse_auto_solver_time(f"../data/summit/scaling/pb1568",
      nodes)
    table += make_table("1568 pebble", n, data, defaultPreconditioner)

    E = 884736
    p = 9
    n = E * p ** 3.0
    defaultPreconditioner = "Chebyshev+ASM+Degree=2,(9,5,1)"
    nodes=[16,24,36,48,60,72]
    data = parse_auto_solver_time(f"../data/summit/scaling/BoeingSpeedBump",
      nodes)
    table += make_table("speed bump", n, data, defaultPreconditioner)

    table += table_end()
    #print(table)
  
  gen()

  baseDir = "../data/summit/scaling/pb1568"
  node=8
  logFiles = common.grab_all_logfiles(f"{baseDir}/fp32/auto-{node}")
  print(logFiles)