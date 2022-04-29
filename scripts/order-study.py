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
myMethodToName={
  "cheby-jac" : "Cheby-Jac(2)",
  "cheby-jac-boomeramg-1" : "Cheby-Jac(2)",
  "cheby-asm" : "Cheby-ASM(2)",
  "cheby-ras" : "Cheby-RAS(2)",
  "cheby-asm-1" : "Cheby-ASM(1)",
  "cheby-ras-1" : "Cheby-RAS(1)",
  "cheby-asm-3" : "Cheby-ASM(3)",
  "cheby-ras-3" : "Cheby-RAS(3)",
  "semfem"    : "SEMFEM",
  "asm"    : "ASM",
  "ras"    : "RAS",
}

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

def process_files(baseDir, method, orders, outputFile):
  rows=[]
  for order in orders:
      logfile = common.grab_latest_logfile(f"{baseDir}/{method}-p-{order}")
      if os.path.isfile(logfile):
        iterations = grep_iteration_count(logfile)
        timeToSol = grep_solve_time(logfile)
        ndofs = grep_problem_size(logfile)
        if timeToSol and iterations:
            rows.append([order,ndofs,iterations,timeToSol])
  matrix = np.asarray(rows)
  np.savetxt(outputFile, matrix, delimiter=",")

def process(eps):
  orders=np.arange(2,11)
  methods = myMethodToName.keys()
  for method in methods:
    baseDir = f"../data/summit/order-dependence/kershaw/eps-{eps}"
    outputFile = f"../data/summit/order-dependence/kershaw/eps-{eps}/{method}.csv"
    process_files(baseDir, method, orders, outputFile)

if 0:
  process(0.05)
  exit()
#process("0.3")
#process("1.0")

def order_scaling_plot(path, mapMethodToName, funcX, funcY, plotter=plt.plot):
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
  plt.grid(which="both")
  #plt.legend(prop={'size':6})

def orders(data):
  return data[:,0]
def dofs(data):
  return data[:,1]
def iterations(data):
  return data[:,2]
def times(data):
  return data[:,3]
def baseDir(eps):
  return f"../data/summit/order-dependence/kershaw/eps-{eps}"
if 0:
  for eps in ["0.3","1.0"]:
    order_scaling_plot(baseDir(eps), myMethodToName, orders, iterations, plotter=plt.plot)
    plt.title(f"$\\varepsilon={eps}$")
    plt.xlabel("$p$")
    plt.ylabel("Iterations")
    plt.legend(prop={'size':6})
    plt.savefig(f"../figs/kershaw-order-scaling-iters-eps-{eps}.png",dpi=300,figsize=(6,6))
    plt.clf()
  
    order_scaling_plot(baseDir(eps), myMethodToName, orders, times, plotter=plt.plot)
    plt.title(f"$\\varepsilon={eps}$")
    plt.xlabel("$p$")
    plt.ylabel("Time / Pressure solve (s)")
    plt.legend(prop={'size':6})
    #plt.tight_layout()
    plt.savefig(f"../figs/kershaw-order-scaling-time-eps-{eps}.png",dpi=300, figsize=(6,6))
    plt.clf()

fig, axs = plt.subplots(2,3, sharex=True, constrained_layout=True)
eps = 1.0
def custom_plotter(*args, **kwargs):
  axs[0,0].plot(*args, **kwargs)
  return
order_scaling_plot(baseDir(eps), myMethodToName, orders, iterations, plotter=custom_plotter)
axs[0,0].set(ylabel = "Iterations")
axs[0,0].set(title = f"$\\varepsilon={eps}$")
def custom_plotter(*args, **kwargs):
  axs[1,0].plot(*args, **kwargs)
  return
order_scaling_plot(baseDir(eps), myMethodToName, orders, times, plotter=custom_plotter)
axs[1,0].set(ylabel = "Time / Pressure solve (s)")
axs[1,0].set(title = f"$\\varepsilon={eps}$")
axs[1,0].set(xlabel = "$p$")
eps = 0.3
def custom_plotter(*args, **kwargs):
  axs[0,1].plot(*args, **kwargs)
  return
order_scaling_plot(baseDir(eps), myMethodToName, orders, iterations, plotter=custom_plotter)
#axs[0,1].set(ylabel = "Iterations")
axs[0,1].set(title = f"$\\varepsilon={eps}$")
def custom_plotter(*args, **kwargs):
  axs[1,1].plot(*args, **kwargs)
  return
order_scaling_plot(baseDir(eps), myMethodToName, orders, times, plotter=custom_plotter)
#axs[1,1].set(ylabel = "Time / Pressure solve (s)")
axs[1,1].set(title = f"$\\varepsilon={eps}$")
axs[1,1].set(xlabel = "$p$")

eps = 0.05
def custom_plotter(*args, **kwargs):
  axs[0,2].plot(*args, **kwargs)
  return
order_scaling_plot(baseDir(eps), myMethodToName, orders, iterations, plotter=custom_plotter)
#axs[0,1].set(ylabel = "Iterations")
axs[0,2].set(title = f"$\\varepsilon={eps}$")
def custom_plotter(*args, **kwargs):
  axs[1,2].plot(*args, **kwargs)
  return
order_scaling_plot(baseDir(eps), myMethodToName, orders, times, plotter=custom_plotter)
#axs[1,1].set(ylabel = "Time / Pressure solve (s)")
axs[1,2].set(title = f"$\\varepsilon={eps}$")
axs[1,2].set(xlabel = "$p$")

for ax in axs.flat:
  ax.grid(which="both")
#for ax in axs.flat:
#  ax.label_outer()

handles, labels = ax.get_legend_handles_labels()
#fig.legend(handles, labels, loc='center right')
fig.legend(handles, labels, bbox_to_anchor=(0.9, 0.325), loc='center left', borderaxespad=0., fontsize="small")

fig.set_size_inches(13.5,7)
#fig.tight_layout()

myFont = {'fontname': 'serif'}
#myFont = {'fontname': 'Times New Roman'}
#myFont = {'fontname': 'Helvetica'}

axs[0,0].annotate("(a)", xy=(-0.1,-0.075), xycoords="axes fraction", fontsize=16, **myFont)
axs[0,1].annotate("(b)", xy=(-0.1,-0.075), xycoords="axes fraction", fontsize=16, **myFont)
axs[0,2].annotate("(c)", xy=(-0.1,-0.075), xycoords="axes fraction", fontsize=16, **myFont)

axs[1,0].annotate("(d)", xy=(-0.1,-0.075), xycoords="axes fraction", fontsize=16, **myFont)
axs[1,1].annotate("(e)", xy=(-0.1,-0.075), xycoords="axes fraction", fontsize=16, **myFont)
axs[1,2].annotate("(f)", xy=(-0.1,-0.075), xycoords="axes fraction", fontsize=16, **myFont)

#plt.show()
plt.savefig(f"../figs/kershaw-order-scaling.png",dpi=300)
