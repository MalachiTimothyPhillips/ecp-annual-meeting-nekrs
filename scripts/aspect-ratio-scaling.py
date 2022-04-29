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
        return int(m.groups()[1])
      elif "iterations" in line:
        print(line)
  return None # something went wrong
def grep_throughput(fileName : str) -> Union[int, None]:
  regex = "avg throughput: (.+) \("
  with open(fileName, "r") as fileObj:
    for line in fileObj.readlines():
      m = re.search(regex, line)
      if m:
        return float(m.groups()[0])
  return None # something went wrong
def grep_aspect_ratio_stats(fileName : str) -> Union[Tuple[float,float,float], None]:
  regex = "aspect ratio(.+?):\s(.+?)\s(.+?)\s(.+?)"
  with open(fileName, "r") as fileObj:
    for line in fileObj.readlines():
      m = re.search(regex, line)
      if m:
        # only care about max aspect ratio
        return float(m.groups()[2])
  return None # something went wrong

def process_qoi(baseFileName : str, func) -> Tuple[np.ndarray, np.ndarray]:
  epsilons = []
  qois = []
  maxAspects=[]
  epsRegex = "eps-(.+)\."
  for dataFile in glob.glob(baseFileName):
    eps = float(re.search(epsRegex, dataFile).groups()[0])
    qoi = func(dataFile)
    maxAspect = grep_aspect_ratio_stats(dataFile)
    qois.append(qoi)
    epsilons.append(eps)
    maxAspects.append(maxAspect)
  assert len(epsilons) == len(qois)
  epsilons = np.asarray(epsilons)
  maxAspects = np.asarray(maxAspects)
  qois = np.asarray(qois)
  idx = np.argsort(epsilons)
  epsilons = epsilons[idx]
  qois = qois[idx]
  maxAspects = maxAspects[idx]
  return  epsilons, qois, maxAspects


class KershawData:
  def __init__(self):
    self.files = [
      #"../data/logs/aspect-ratio-scaling/kershaw-e-36x36x36/kershaw-gmres-20-p-7-jacobi-eps-*",
      "../data/logs/aspect-ratio-scaling/kershaw-e-36x36x36/kershaw-gmres-20-p-7-asm-eps-*",
      "../data/logs/aspect-ratio-scaling/kershaw-e-36x36x36/kershaw-gmres-20-p-7-ras-eps-*",
      "../data/logs/aspect-ratio-scaling/kershaw-e-36x36x36/kershaw-gmres-20-p-7-cheby-jac-eps-*",
      "../data/logs/aspect-ratio-scaling/kershaw-e-36x36x36/kershaw-gmres-20-p-7-cheby-asm-eps-*",
      "../data/logs/aspect-ratio-scaling/kershaw-e-36x36x36/kershaw-gmres-20-p-7-cheby-ras-eps-*",
      "../data/logs/aspect-ratio-scaling/kershaw-e-36x36x36/kershaw-gmres-20-p-7-semfem-eps-*",
      "../data/logs/aspect-ratio-scaling/kershaw-e-36x36x36/kershaw-gmres-20-p-7-semfem-oversolve-eps-*",
    ]
    self.names = [
      #"Jacobi",
      "ASM",
      "RAS",
      "Cheby-Jac",
      "Cheby-ASM",
      "Cheby-RAS",
      "SEMFEM",
      "Ideal SEMFEM",
    ]
class KershawDataPCG:
  def __init__(self):
    self.files = [
      "../data/logs/aspect-ratio-scaling/kershaw-e-36x36x36/kershaw-pcg-p-7-jacobi-eps-*",
      "../data/logs/aspect-ratio-scaling/kershaw-e-36x36x36/kershaw-pcg-p-7-asm-eps-*",
      "../data/logs/aspect-ratio-scaling/kershaw-e-36x36x36/kershaw-pcg-p-7-ras-eps-*",
      "../data/logs/aspect-ratio-scaling/kershaw-e-36x36x36/kershaw-pcg-p-7-cheby-jac-eps-*",
      "../data/logs/aspect-ratio-scaling/kershaw-e-36x36x36/kershaw-pcg-p-7-cheby-asm-eps-*",
      "../data/logs/aspect-ratio-scaling/kershaw-e-36x36x36/kershaw-pcg-p-7-cheby-ras-eps-*",
      "../data/logs/aspect-ratio-scaling/kershaw-e-36x36x36/kershaw-pcg-p-7-semfem-eps-*",
      "../data/logs/aspect-ratio-scaling/kershaw-e-36x36x36/kershaw-pcg-p-7-semfem-oversolve-eps-*",
    ]
    self.names = [
      "Jacobi",
      "ASM",
      "RAS",
      "Cheby-Jac",
      "Cheby-ASM",
      "Cheby-RAS",
      "SEMFEM",
      "Ideal SEMFEM",
    ]
class KershawDataBoth:
  def __init__(self):
    self.pcgFiles = [
      "../data/logs/aspect-ratio-scaling/kershaw-e-36x36x36/kershaw-pcg-p-7-cheby-jac-eps-*",
      "../data/logs/aspect-ratio-scaling/kershaw-e-36x36x36/kershaw-pcg-p-7-cheby-ras-eps-*",
      "../data/logs/aspect-ratio-scaling/kershaw-e-36x36x36/kershaw-pcg-p-7-semfem-eps-*",
      "../data/logs/aspect-ratio-scaling/kershaw-e-36x36x36/kershaw-pcg-p-7-semfem-oversolve-eps-*",
    ]
    self.gmresFiles = [
      "../data/logs/aspect-ratio-scaling/kershaw-e-36x36x36/kershaw-gmres-20-p-7-cheby-jac-eps-*",
      "../data/logs/aspect-ratio-scaling/kershaw-e-36x36x36/kershaw-gmres-20-p-7-cheby-ras-eps-*",
      "../data/logs/aspect-ratio-scaling/kershaw-e-36x36x36/kershaw-gmres-20-p-7-semfem-eps-*",
      "../data/logs/aspect-ratio-scaling/kershaw-e-36x36x36/kershaw-gmres-20-p-7-semfem-oversolve-eps-*",
    ]
    self.pcgNames = [
      "Cheby-Jac", #PCG
      "Cheby-RAS",
      "SEMFEM",
      "Ideal SEMFEM",
    ]
    self.gmresNames = [
      "Cheby-Jac", # GMRES
      "Cheby-RAS",
      "SEMFEM",
      "Ideal SEMFEM",
    ]


if __name__ == "__main__":

  data = KershawData()
  files = data.files
  names = data.names

  def plot_kershaw(files, names, qoi):
    ax1 = plt.subplot(1,1,1)
    eps, _, maxAspects = process_qoi(files[0], qoi)
    for fileName, name in zip(files, names):
       eps, solveTimes, maxAspects = process_qoi(fileName, qoi)
       #eps, throughput, maxAspects = process_qoi(fileName, grep_iteration_count)
       markerStyle = common.precisionToMarker["FP32"]
       #lineStyle = common.archToLineStyle["GPU"]
       lineStyle = "solid"
       color = common.methodToColor[name.upper()]
       ax1.plot(maxAspects,
         solveTimes,
         label=name,
         color=color,
         lineStyle=lineStyle,
         marker=markerStyle)
  
    ax1.set_xscale("log")
    ax1.set_yscale("log")
    ax1.set_xlabel("Max Aspect Ratio")
    #ax1.set_ylabel("Average Time per Solve (s)")
    ax2 = ax1.twiny()
    ax2.set_xscale("log")
    ax2.set_yscale("log")
    #ax1.set_xticks(maxAspects)
    #ax1.set_xticklabels(maxAspects)
    ax2.set_xticks(maxAspects)
    epsLabels=[]
    for value in eps:
      if abs(value - 0.25) < 1e-10:
        epsLabels.append("")
      else:
        epsLabels.append(f"$\\varepsilon={value}$")
    #epsLabels = [f"$\\varepsilon = {value}$" for value in eps]
    ax2.set_xticklabels(epsLabels)
    ax2.xaxis.set_ticks_position('top') # set the position of the second x-axis to bottom
    ax2.xaxis.set_label_position('top') # set the position of the second x-axis to bottom
    #ax2.spines['top'].set_position(('inward', 10))
    #ax2.set_xlabel('$\\varepsilon$')
    ax2.set_xlim(ax1.get_xlim())

    #plt.ylabel("Iterations")
    #ax1.set_title("Kershaw, $E=36^3$, GMRES(20)")
    ax1.legend()
    ax1.grid()
    return ax1

  def plot_comparison(pcgFiles, pcgNames, gmresFiles, gmresNames, qoi):
    ax1 = plt.subplot(1,1,1)
    eps, _, maxAspects = process_qoi(files[0], qoi)

    ax1.plot([],[],marker="o", lineStyle="solid",color="k",label="GMRES(20)")
    ax1.plot([],[],marker="v", lineStyle="dashed",color="k",label="PCG")

    for gmresFile, gmresName in zip(gmresFiles, gmresNames):
       eps, solveTimes, maxAspects = process_qoi(gmresFile, qoi)
       #eps, throughput, maxAspects = process_qoi(fileName, grep_iteration_count)
       #lineStyle = common.archToLineStyle["GPU"]
       lineStyle = "solid"
       markerStyle = "o"
       color = common.methodToColor[gmresName.upper()]
       ax1.plot(maxAspects,
         solveTimes,
         label=gmresName,
         color=color,
         lineStyle=lineStyle,
         marker=markerStyle)

    for pcgFile, pcgName in zip(pcgFiles, pcgNames):
       eps, solveTimes, maxAspects = process_qoi(pcgFile, qoi)
       #eps, throughput, maxAspects = process_qoi(fileName, grep_iteration_count)
       #lineStyle = common.archToLineStyle["GPU"]
       lineStyle = "dashed"
       markerStyle = "v"
       color = common.methodToColor[pcgName.upper()]
       ax1.plot(maxAspects,
         solveTimes,
         label=pcgName,
         color=color,
         lineStyle=lineStyle,
         marker=markerStyle)
  
    ax1.set_xscale("log")
    ax1.set_yscale("log")
    ax1.set_xlabel("Max Aspect Ratio")
    #ax1.set_ylabel("Average Time per Solve (s)")
    ax2 = ax1.twiny()
    ax2.set_xscale("log")
    ax2.set_yscale("log")
    #ax1.set_xticks(maxAspects)
    #ax1.set_xticklabels(maxAspects)
    ax2.set_xticks(maxAspects)
    epsLabels=[]
    for value in eps:
      if abs(value - 0.25) < 1e-10:
        epsLabels.append("")
      else:
        epsLabels.append(f"$\\varepsilon={value}$")
    #epsLabels = [f"$\\varepsilon = {value}$" for value in eps]
    ax2.set_xticklabels(epsLabels)
    ax2.xaxis.set_ticks_position('top') # set the position of the second x-axis to bottom
    ax2.xaxis.set_label_position('top') # set the position of the second x-axis to bottom
    #ax2.spines['top'].set_position(('inward', 10))
    #ax2.set_xlabel('$\\varepsilon$')
    ax2.set_xlim(ax1.get_xlim())

    #plt.ylabel("Iterations")
    #ax1.set_title("Kershaw, $E=36^3$, GMRES(20)")
    ax1.legend()
    ax1.grid()
    return ax1

  
  # solve time, GMRES(20)
  axis = plot_kershaw(files, names, grep_solve_time)
  axis.set_ylabel("Average Time per Solve (s)")
  axis.set_title("Kershaw, $E=36^3$, GMRES(20)")
  plt.savefig("../figs/kershaw-solve-times-gmres-20.png", dpi=300)
  plt.clf()

  # iteration counts, GMRES(20)
  axis = plot_kershaw(files, names, grep_iteration_count)
  axis.set_ylabel("Iterations")
  plt.title("Kershaw, $E=36^3$, GMRES(20)")
  plt.savefig("../figs/kershaw-iterations-gmres-20.png", dpi=300)
  plt.clf()


  data = KershawDataPCG()
  files = data.files
  names = data.names

  # solve time, PCG
  axis = plot_kershaw(files, names, grep_solve_time)
  axis.set_ylabel("Average Time per Solve (s)")
  plt.title("Kershaw, $E=36^3$, PCG")
  plt.savefig("../figs/kershaw-solve-times-pcg.png", dpi=300)
  plt.clf()

  # iteration counts, PCG
  axis = plot_kershaw(files, names, grep_iteration_count)
  axis.set_ylabel("Iterations")
  plt.title("Kershaw, $E=36^3$, PCG")
  plt.savefig("../figs/kershaw-iterations-pcg.png", dpi=300)
  plt.clf()


  data = KershawDataBoth()
  pcgFiles = data.pcgFiles
  pcgNames = data.pcgNames
  gmresFiles = data.gmresFiles
  gmresNames = data.gmresNames

  # solve time, both
  axis = plot_comparison(pcgFiles, pcgNames, gmresFiles, gmresNames, grep_solve_time)
  axis.set_ylabel("Average Time per Solve (s)")
  plt.title("Kershaw, $E=36^3$")
  plt.savefig("../figs/kershaw-solve-times-comparison.png", dpi=300)
  plt.clf()

  # iteration counts, PCG
  axis = plot_comparison(pcgFiles, pcgNames, gmresFiles, gmresNames, grep_iteration_count)
  axis.set_ylabel("Iterations")
  plt.title("Kershaw, $E=36^3$")
  plt.savefig("../figs/kershaw-iterations-comparison.png", dpi=300)
  plt.clf()