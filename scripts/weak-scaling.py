import numpy as np
import os
import common
import numpy.linalg as la
import scipy.sparse as sp
import uuid
from typing import Union, Tuple
import scipy.linalg as scla
import re
import glob
import matplotlib.pyplot as plt

ranksPerNode = 6
myMethodToName = dict()
for method, name in common.methodToName.items():
  myMethodToName[method] = name
myMethodToName["asm"] = "ASM,(7,3,1)"
myMethodToName["ras"] = "RAS,(7,3,1)"

def grep_max_neighbors(fileName : str) -> Union[int, None]:
  regex = "nMessages   max\/min\/avg:(.+?)\s"
  with open(fileName, "r") as fileObj:
    for line in fileObj.readlines():
      m = re.search(regex, line)
      if m:
        return float(m.groups()[0])
  return None # something went wrong
def grep_aspect_ratio(fileName : str) -> Union[int, None]:
  regex = "aspect ratio     min\/max\/avg:(.+?)(\s+)(.+?)(\s)"
  with open(fileName, "r") as fileObj:
    for line in fileObj.readlines():
      m = re.search(regex, line)
      if m:
        return float(m.groups()[2])
  return None # something went wrong
def grep_problem_size(fileName : str) -> Union[int, None]:
  regex = "gridpoints unique\/tot:(\s+)(.+?)(\s+)"
  with open(fileName, "r") as fileObj:
    for line in fileObj.readlines():
      m = re.search(regex, line)
      if m:
        return float(m.groups()[1])
  return None # something went wrong
def grep_solve_time(fileName : str) -> Union[int, None]:
  regex = "avg solve time:(\s+)(.+?)\s"
  with open(fileName, "r") as fileObj:
    for line in fileObj.readlines():
      m = re.search(regex, line)
      if m:
        return float(m.groups()[1])
  return None # something went wrong
def grep_iteration_count(fileName : str) -> Union[int, None]:
  regex = "iterations:(\s+)(.+)"
  with open(fileName, "r") as fileObj:
    for line in fileObj.readlines():
      m = re.search(regex, line)
      if m:
        return float(m.groups()[1])
      elif "iterations" in line:
        print(line)

def process_files(baseDir, method, nodes, outputFile):
  rows=[]
  for node in nodes:
      logfile = common.grab_latest_logfile(f"{baseDir}/{method}-{node}")
      if os.path.isfile(logfile):
        iterations = grep_iteration_count(logfile)
        timeToSol = grep_solve_time(logfile)
        ndofs = grep_problem_size(logfile)
        maxNeighbors = grep_max_neighbors(logfile)
        aspectRatio = grep_aspect_ratio(logfile)
        if timeToSol and iterations:
            rows.append([node,ndofs,iterations,timeToSol, maxNeighbors, aspectRatio])
  matrix = np.asarray(rows)
  np.savetxt(outputFile, matrix, delimiter=",")

def process(eps):
  nodes=[2,4,8,16,32,64]
  methods = myMethodToName.keys()
  for method in methods:
    baseDir = f"../data/summit/weak-scaling/kershaw/eps-{eps}"
    outputFile = f"../data/summit/weak-scaling/kershaw/eps-{eps}/{method}.csv"
    process_files(baseDir, method, nodes, outputFile)

def weak_scaling_plot(path, mapMethodToName, funcX, funcY, plotter=plt.semilogx):
  # Scaling plot
  for method in mapMethodToName.keys():
    fileName = f"{path}/{method}.csv"
    data = np.genfromtxt(fileName, delimiter=',')
    if len(data.shape) > 1:
        x = funcX(data)
        y = funcY(data)
        label = mapMethodToName[method]
        if "jac" in method:
          label = mapMethodToName["cheby-jac-boomeramg-1"]
        plotter(x, 
          y,
          color = common.grab_color(method),
          marker = common.parse_order(method),
          #label = mapMethodToName[method],
          label = label,
          linestyle = common.archToLineStyle["GPU"])
  #plt.grid(which="both")
  #plt.legend(prop={'size':6})

def ranks(data):
  nodes = data[:,0]
  return ranksPerNode * nodes
def dofsPerRank(data):
  nodes = data[:,0]
  dofs = data[:,1]
  return dofs / (ranksPerNode * nodes)

def baseDir(eps):
  return f"../data/summit/weak-scaling/kershaw/eps-{eps}"

if 0:
  weak_scaling_plot(baseDir("0.3"), {"cheby-asm":1}, ranks, dofsPerRank)
  #plt.title("Degree of Freedom, Kershaw")
  plt.ylabel("$\\dfrac {n}{P}$")
  plt.xlabel("$P$")
  plt.ylim((0,3e6))
  #plt.tight_layout()
  plt.savefig("../figs/kershaw-weak-scaling-ndofs.png",dpi=300)
  plt.clf()

def iterations(data):
  iters = data[:,2]
  return iters
def times(data):
  time = data[:,3]
  return time
def timePerIteration(data):
  iters = data[:,2]
  time = data[:,3]
  return time / iters
def neighbors(data):
  return data[:,4]
def aspectRatios(data):
  return data[:,5]
def efficiency(data):
  return data[0,3]/data[:,3]

if 0:
  process("0.05")
  exit()
  #process("0.3")
  #process("1.0")

if 0:
  epsilons = ["0.3", "1.0"]
  for eps in epsilons:
    weak_scaling_plot(baseDir(eps), myMethodToName, ranks, iterations, plotter=plt.semilogx)
    plt.title(f"$\\varepsilon={eps}$")
    plt.ylabel("Iterations")
    plt.xlabel("$P$")
    plt.legend(prop={'size':6})
    plt.savefig(f"../figs/kershaw-weak-scaling-iters-eps-{eps}.png",dpi=300)
    plt.clf()
    
    weak_scaling_plot(baseDir(eps), myMethodToName, ranks, times, plotter=plt.semilogx)
    plt.title(f"$\\varepsilon={eps}$")
    plt.ylabel("Time / Pressure solve (s)")
    plt.xlabel("$P$")
    plt.legend(prop={'size':6})
    plt.savefig(f"../figs/kershaw-weak-scaling-time-eps-{eps}.png",dpi=300)
    plt.clf()
    
    weak_scaling_plot(baseDir(eps), myMethodToName, ranks, timePerIteration, plotter=plt.semilogx)
    plt.title(f"$\\varepsilon={eps}$")
    plt.ylabel("Time / Pressure iteration (s)")
    plt.xlabel("$P$")
    plt.legend(prop={'size':6})
    plt.savefig(f"../figs/kershaw-weak-scaling-time-per-iter-eps-{eps}.png",dpi=300)
    plt.clf()
  
    weak_scaling_plot(baseDir(eps), myMethodToName, ranks, efficiency, plotter=plt.semilogx)
    plt.title(f"$\\varepsilon={eps}$")
    plt.ylabel("Parallel Efficiency")
    plt.xlabel("$P$")
    plt.legend(prop={'size':6})
    plt.savefig(f"../figs/kershaw-weak-scaling-eff-eps-{eps}.png",dpi=300)
    plt.clf()
  
  if 0:
    eps = 1.0
    fileName = f"{baseDir(eps)}/cheby-asm.csv"
    data = np.genfromtxt(fileName, delimiter=',')
    x = ranks(data)
    y = neighbors(data)
    plt.semilogx(x, 
      y,
      color = "black",
      marker = "o")
    plt.grid(which="both")
    
    plt.ylabel("Max Neighbors")
    plt.xlabel("$P$")
    plt.savefig(f"../figs/kershaw-weak-scaling-neighbors.png",dpi=300)
    plt.clf()

#fig, axs = plt.subplots(2,3, sharex=True, constrained_layout=True)
fig, axs = plt.subplots(3,3, sharex=True)
eps = 1.0
def custom_plotter(*args, **kwargs):
  axs[0,0].semilogx(*args, **kwargs)
  return
weak_scaling_plot(baseDir(eps), myMethodToName, ranks, iterations, plotter=custom_plotter)
axs[0,0].set(ylabel = "Iterations")
axs[0,0].set(title = f"$\\varepsilon={eps}$")

def custom_plotter(*args, **kwargs):
  axs[0,1].semilogx(*args, **kwargs)
  return
weak_scaling_plot(baseDir(eps), myMethodToName, ranks, times, plotter=custom_plotter)
axs[0,1].set(ylabel = "Time / Pressure solve (s)")
axs[0,1].set(title = f"$\\varepsilon={eps}$")

def custom_plotter(*args, **kwargs):
  axs[0,2].semilogx(*args, **kwargs)
  return
weak_scaling_plot(baseDir(eps), myMethodToName, ranks, efficiency, plotter=custom_plotter)
axs[0,2].set(ylabel = "Parallel Efficiency")
axs[0,2].set(title = f"$\\varepsilon={eps}$")

eps = 0.3
def custom_plotter(*args, **kwargs):
  axs[1,0].semilogx(*args, **kwargs)
  return
weak_scaling_plot(baseDir(eps), myMethodToName, ranks, iterations, plotter=custom_plotter)
axs[1,0].set(ylabel = "Iterations")
axs[1,0].set(xlabel = "$P$")
axs[1,0].set(title = f"$\\varepsilon={eps}$")

def custom_plotter(*args, **kwargs):
  axs[1,1].semilogx(*args, **kwargs)
  return
weak_scaling_plot(baseDir(eps), myMethodToName, ranks, times, plotter=custom_plotter)
axs[1,1].set(ylabel = "Time / Pressure solve (s)")
axs[1,1].set(xlabel = "$P$")
axs[1,1].set(title = f"$\\varepsilon={eps}$")

def custom_plotter(*args, **kwargs):
  axs[1,2].semilogx(*args, **kwargs)
  return
weak_scaling_plot(baseDir(eps), myMethodToName, ranks, efficiency, plotter=custom_plotter)
axs[1,2].set(ylabel = "Parallel Efficiency")
axs[1,2].set(xlabel = "$P$")
axs[1,2].set(title = f"$\\varepsilon={eps}$")

eps = 0.05
def custom_plotter(*args, **kwargs):
  axs[2,0].semilogx(*args, **kwargs)
  return
weak_scaling_plot(baseDir(eps), myMethodToName, ranks, iterations, plotter=custom_plotter)
axs[2,0].set(ylabel = "Iterations")
axs[2,0].set(xlabel = "$P$")
axs[2,0].set(title = f"$\\varepsilon={eps}$")

def custom_plotter(*args, **kwargs):
  axs[2,1].semilogx(*args, **kwargs)
  return
weak_scaling_plot(baseDir(eps), myMethodToName, ranks, times, plotter=custom_plotter)
axs[2,1].set(ylabel = "Time / Pressure solve (s)")
axs[2,1].set(xlabel = "$P$")
axs[2,1].set(title = f"$\\varepsilon={eps}$")

def custom_plotter(*args, **kwargs):
  axs[2,2].semilogx(*args, **kwargs)
  return
weak_scaling_plot(baseDir(eps), myMethodToName, ranks, efficiency, plotter=custom_plotter)
axs[2,2].set(ylabel = "Parallel Efficiency")
axs[2,2].set(xlabel = "$P$")
axs[2,2].set(title = f"$\\varepsilon={eps}$")

for ax in axs.flat:
  ax.grid(which="both")

handles, labels = axs[0,0].get_legend_handles_labels()
#fig.legend(handles, labels, loc='center right')

fig.set_size_inches(13.5, 9.5)

myFont = {'fontname': 'serif'}
#myFont = {'fontname': 'Times New Roman'}
#myFont = {'fontname': 'Helvetica'}

axs[0,0].annotate("(a)", xy=(-0.1,-0.15), xycoords="axes fraction", fontsize=16, **myFont)
axs[0,1].annotate("(b)", xy=(-0.1,-0.15), xycoords="axes fraction", fontsize=16, **myFont)
axs[0,2].annotate("(c)", xy=(-0.1,-0.15), xycoords="axes fraction", fontsize=16, **myFont)

axs[1,0].annotate("(d)", xy=(-0.1,-0.15), xycoords="axes fraction", fontsize=16, **myFont)
axs[1,1].annotate("(e)", xy=(-0.1,-0.15), xycoords="axes fraction", fontsize=16, **myFont)
axs[1,2].annotate("(f)", xy=(-0.1,-0.15), xycoords="axes fraction", fontsize=16, **myFont)

axs[2,0].annotate("(g)", xy=(-0.1,-0.15), xycoords="axes fraction", fontsize=16, **myFont)
axs[2,1].annotate("(h)", xy=(-0.1,-0.15), xycoords="axes fraction", fontsize=16, **myFont)
axs[2,2].annotate("(i)", xy=(-0.1,-0.15), xycoords="axes fraction", fontsize=16, **myFont)

plt.tight_layout()
plt.subplots_adjust(right=0.825)
fig.legend(handles, labels, bbox_to_anchor=(0.8375, 0.5), loc='center left', borderaxespad=0., fontsize="medium")

#plt.show()
plt.savefig(f"../figs/kershaw-weak-scaling.png",dpi=300)