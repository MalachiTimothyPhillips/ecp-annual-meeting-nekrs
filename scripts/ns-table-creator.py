import glob
import os
import re
import numpy as np
import matplotlib.pyplot as plt
import common

def timePerSolve(data):
  Nsteps = data[:,2]
  time_to_solutions = data[:,3] # ns solve
  return time_to_solutions / Nsteps

def percentPressureSolve(data):
  time_to_p_solve = data[:,1] # ns solve
  time_to_solutions = data[:,3] # ns solve
  return time_to_p_solve / time_to_solutions

def pressureIters(data):
  return data[:,4] # average number of pressure iterations, 2000 steps

def collocateData(path, mapMethodToName, qoiFunc):
  ranks = set()
  results = {}
  for method in mapMethodToName.keys():
      rankToQOI = {}
      for precision in ["fp32"]:
        fileName = f"{path}/ns-{method}-{precision}.csv"
        data = np.genfromtxt(fileName, delimiter=',')
        if len(data.shape) > 1:
            nodes = data[:,0]
            for node in nodes:
              ranks.add(int(6*node))
            qois = qoiFunc(data)
            for node, qoi in zip(nodes, qois):
              rankToQOI[int(6*node)] = qoi
      results[method] = rankToQOI
  ranks = np.asarray(list(ranks))
  ranks = np.sort(ranks)
  return ranks, results

def tableStart(ranks, results):
  table = "\\begin{table*}\n\centering\n"
  table += "\\begin{tabular}{||c||"
  table += "c" * len(ranks)
  table += "||}\n"
  table += "\t\\hline\n"
  table += "\t$P$ "
  for rank in ranks:
    table += f"& {rank} "
  table += "\\\\\n"
  table += "\t\\hline\\hline\n"
  return table
def tableEnd():
    table = "\\hline\n"
    table += "\\end{tabular}\n"
    table += "\\caption{\label{table:foobar}}\n"
    table += "\\end{table*}\n"
    return table
def generateTable(ranks, results, mapMethodToName, formatStr = None):
  table = ""
  for method in results.keys():
    table += f"\t{mapMethodToName[method]}"
    for rank in ranks:
      if rank in results[method]:
        if formatStr:
          table += f"\t&\t{formatStr.format(results[method][rank])}"
        else:
          table += f"\t&\t{round(results[method][rank],3)}"

      else:
        table += "\t&\t --"
    table += "\\\\\n"
  return table

def finalizeTable(ranks, results, mapMethodToName, formatStr = None):
  table = ""
  table += tableStart(ranks, results)
  table += generateTable(ranks, results, mapMethodToName, formatStr)
  table += tableEnd()
  return table

def dumpCSV(ranks, results, mapMethodToName):
  table = "Method "
  for rank in ranks:
    table += f", P = {rank}"
  table += "\n"
  for method in results.keys():
    table += f"\"{mapMethodToName[method]}\""
    for rank in ranks:
      if rank in results[method]:
        table += f", {results[method][rank]}"
      else:
        table += ", --"
    table += "\n"
  return table

if __name__ == "__main__":

  # pb146
  ranks, results = collocateData(f"../data/summit/scaling/pb146", common.methodToName, timePerSolve)
  table = finalizeTable(ranks, results, common.methodToName)
  print(table)
  with open("pb146-ns-time-per-solve.tex", "w") as f:
    f.write(table)
  myCSV = dumpCSV(ranks, results, common.methodToName)
  print(myCSV)
  with open("pb146-ns-time-per-solve.csv", "w") as f:
    f.write(myCSV)

  ranks, results = collocateData(f"../data/summit/scaling/pb146", common.methodToName, percentPressureSolve)
  table = finalizeTable(ranks, results, common.methodToName)
  print(table)
  with open("pb146-fraction-pressure-solve.tex", "w") as f:
    f.write(table)
  myCSV = dumpCSV(ranks, results, common.methodToName)
  print(myCSV)
  with open("pb146-fraction-pressure-solve.csv", "w") as f:
    f.write(myCSV)

  ranks, results = collocateData(f"../data/summit/scaling/pb146", common.methodToName, pressureIters)
  table = finalizeTable(ranks, results, common.methodToName)
  print(table)
  with open("pb146-iterations-pressure-solve.tex", "w") as f:
    f.write(table)
  myCSV = dumpCSV(ranks, results, common.methodToName)
  print(myCSV)
  with open("pb146-iterations-pressure-solve.csv", "w") as f:
    f.write(myCSV)
  

  E = 62132
  p = 7
  def workPerNode(data):
    nodes = data[:,0]
    time_to_solutions = data[:,1]
    Nsteps = data[:,2]
    gridpoints = E * p ** 3.0
    time_per_timesteps = time_to_solutions / Nsteps
    work_units_per_node = gridpoints / (time_per_timesteps * nodes)
    return work_units_per_node

  ranks, results = collocateData(f"../data/summit/scaling/pb146", common.methodToName, workPerNode)
  table = finalizeTable(ranks, results, common.methodToName, "{:.2e}")
  print(table)
  with open("pb146-ns-work-rate.tex", "w") as f:
    f.write(table)
  myCSV = dumpCSV(ranks, results, common.methodToName)
  print(myCSV)
  with open("pb146-ns-work-rate.csv", "w") as f:
    f.write(myCSV)

  
  # pb1568
  ranks, results = collocateData(f"../data/summit/scaling/pb1568", common.methodToName, timePerSolve)
  table = finalizeTable(ranks, results, common.methodToName)
  print(table)
  with open("pb1568-ns-time-per-solve.tex", "w") as f:
    f.write(table)
  myCSV = dumpCSV(ranks, results, common.methodToName)
  print(myCSV)
  with open("pb1568-ns-time-per-solve.csv", "w") as f:
    f.write(myCSV)

  ranks, results = collocateData(f"../data/summit/scaling/pb1568", common.methodToName, percentPressureSolve)
  table = finalizeTable(ranks, results, common.methodToName)
  print(table)
  with open("pb1568-fraction-pressure-solve.tex", "w") as f:
    f.write(table)
  myCSV = dumpCSV(ranks, results, common.methodToName)
  print(myCSV)
  with open("pb1568-fraction-pressure-solve.csv", "w") as f:
    f.write(myCSV)

  ranks, results = collocateData(f"../data/summit/scaling/pb1568", common.methodToName, pressureIters)
  table = finalizeTable(ranks, results, common.methodToName)
  print(table)
  with open("pb1568-iterations-pressure-solve.tex", "w") as f:
    f.write(table)
  myCSV = dumpCSV(ranks, results, common.methodToName)
  print(myCSV)
  with open("pb1568-iterations-pressure-solve.csv", "w") as f:
    f.write(myCSV)
  
  E = 524386
  p = 7
  def workPerNode(data):
    nodes = data[:,0]
    time_to_solutions = data[:,1]
    Nsteps = data[:,2]
    gridpoints = E * p ** 3.0
    time_per_timesteps = time_to_solutions / Nsteps
    work_units_per_node = gridpoints / (time_per_timesteps * nodes)
    return work_units_per_node

  ranks, results = collocateData(f"../data/summit/scaling/pb1568", common.methodToName, workPerNode)
  table = finalizeTable(ranks, results, common.methodToName, "{:.2e}")
  print(table)
  with open("pb1568-ns-work-rate.tex", "w") as f:
    f.write(table)
  myCSV = dumpCSV(ranks, results, common.methodToName)
  print(myCSV)
  with open("pb1568-ns-work-rate.csv", "w") as f:
    f.write(myCSV)
