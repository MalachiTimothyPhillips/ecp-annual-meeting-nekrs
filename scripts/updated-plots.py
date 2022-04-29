import glob
import os
import re
import numpy as np
import matplotlib.pyplot as plt
import common

def gather_constant_rank_data(path, mapMethodToName, precisions, E, p, nodeCount, plotter=plt.semilogx):
  points = []
  for method in mapMethodToName.keys():
      for precision in precisions:
        fileName = f"{path}/{method}-{precision}.csv"
        data = np.genfromtxt(fileName, delimiter=',')
        if len(data.shape) > 1:
            nodes = data[:,0]
            if nodeCount in nodes:
              for i, node in enumerate(nodes):
                if node == nodeCount:
                  points.append(data[i,1])
  time_to_solutions = np.array(points)
  time_to_solutions = np.sort(time_to_solutions)

  #Nsteps = data[:,2]
  Nsteps = 2000
  gridpoints = E * p ** 3.0
  time_per_timesteps = time_to_solutions / Nsteps
  work_units_per_node = gridpoints / (time_per_timesteps * nodeCount)
  plotter(time_per_timesteps, 
    work_units_per_node)
  return
def machine_scaling_study(path, mapMethodToName, precisions, E, p, plotter=plt.semilogx):
  # Scaling plot
  for method in mapMethodToName.keys():
      for precision in precisions:
        fileName = f"{path}/{method}-{precision}.csv"
        data = np.genfromtxt(fileName, delimiter=',')
        if len(data.shape) > 1:
            nodes = data[:,0]
            time_to_solutions = data[:,1]
            Nsteps = data[:,2]
            gridpoints = E * p ** 3.0
            time_per_timesteps = time_to_solutions / Nsteps
            work_units_per_node = gridpoints / (time_per_timesteps * nodes)
            plotter(time_per_timesteps, 
              work_units_per_node,
              color = common.grab_color(method),
              marker = common.parse_order(method),
              label = mapMethodToName[method],
              linestyle = common.archToLineStyle["GPU"])
  return

def add_processor_counts(path, mapMethodToName, precisions, E, p, texter=plt.text):
  # Scaling plot
  for method in mapMethodToName.keys():
      for precision in precisions:
        fileName = f"{path}/{method}-{precision}.csv"
        data = np.genfromtxt(fileName, delimiter=',')
        if len(data.shape) > 1:
            nodes = data[:,0]
            time_to_solutions = data[:,1]
            Nsteps = data[:,2]
            gridpoints = E * p ** 3.0
            time_per_timesteps = time_to_solutions / Nsteps
            work_units_per_node = gridpoints / (time_per_timesteps * nodes)
            strings=[]
            for node in nodes:
              strings.append("$P = {}$".format(int(6*node)))
            
            for time_per_step, work_unit_per_node, string in zip(time_per_timesteps, work_units_per_node, strings):
              texter(time_per_step, 
                work_unit_per_node,
                string
                #color = common.grab_color(method),
                #marker = common.parse_order(method),
                #label = mapMethodToName[method],
                #linestyle = common.archToLineStyle["GPU"]
                )
  return

if __name__ == "__main__":

  def bsb():
    fig, axs = plt.subplots(1, 1, figsize=(13.5/2.0,5))

    E = 884736
    p = 9
    ranksPerNode = 6
    precisions = ["fp32"]
    path = "../data/summit/scaling/BoeingSpeedBump"

    def custom_plotter(*args, **kwargs):
      axs.semilogx(*args, **kwargs)
      return
    machine_scaling_study(path,
      common.methodToNameBSB,
      precisions,
      E,
      p,
      plotter=custom_plotter)
    axs.set_title("$P=96:432$, Cheby-RAS wins", fontsize="x-large")

    # Add processor counts
    def custom_texter(*args, **kwargs):
      x, y, string = args
      if "96" in string:
        axs.text(x + 0.025, y, string, **kwargs, fontsize="large")
      if "432" in string:
        axs.text(x - 0.05, y - 5e6, string, **kwargs, fontsize="large")
      return

    add_processor_counts(path,
      {"cheby-ras" : "Cheby-RAS(2),(9,5,1)"},
      precisions,
      E,
      p,
      texter=custom_texter)

    axs.grid(which="both")
    axs.set_ylabel("Gridpoints / (time per solve * node)")
    axs.set_xlabel("Time per solve (s)")
  
    tickMarks = [0.3,0.4,0.5,0.6,0.7,1.0,2.0]
    tickMarkLabels = [str(np.round(x,1)) for x in tickMarks]
    axs.set_xticks(tickMarks)
    axs.set_xticklabels(tickMarkLabels, rotation=30)

    def my_plotter(xdat,ydat):
      axs.semilogx(xdat,ydat,color="black",linestyle="--")
      return
    gather_constant_rank_data(path,
      common.methodToNameBSB,
      precisions,
      E,
      p,
      48,
      plotter=my_plotter)
    
    # add annotation
    axs.annotate("$P=288$", xy=(0.3, 0.25), xytext=(0.2,0.1), xycoords='axes fraction', fontsize="medium",
      arrowprops=dict(facecolor='black', width=1, headwidth=5))


    plt.tight_layout()
    #plt.subplots_adjust(right=0.78)
    handles, labels = axs.get_legend_handles_labels()
    fig.legend(handles, labels, bbox_to_anchor=(0.65, 0.62), loc='center left', borderaxespad=0., fontsize="small")
    #fig.legend(handles, labels)

    #plt.show()
    plt.savefig("../figs/bsb-scaling.png",dpi=300)
    return

  def pb146():
    fig, axs = plt.subplots(1, 1, figsize=(13.5/2.0,5))

    E = 62132
    p = 7
    ranksPerNode = 6
    precisions = ["fp32"]
    path = "../data/summit/scaling/pb146"

    def custom_plotter(*args, **kwargs):
      axs.semilogx(*args, **kwargs)
      return
    machine_scaling_study(path,
      common.methodToName,
      precisions,
      E,
      p,
      plotter=custom_plotter)
    axs.set_title("$P=3:18$, Cheby-RAS wins", fontsize="x-large")

    # Add processor counts
    def custom_texter(*args, **kwargs):
      x, y, string = args
      if "3" in string:
        axs.text(x + 0.025, y, string, **kwargs, fontsize="large")
      if "18" in string:
        axs.text(x - 0.025, y - 1e7, string, **kwargs, fontsize="large")
      return

    add_processor_counts(path,
      {"cheby-ras" : "Cheby-RAS(2),(7,3,1)"},
      precisions,
      E,
      p,
      texter=custom_texter)

    axs.grid(which="both")
    axs.set_ylabel("Gridpoints / (time per solve * node)")
    axs.set_xlabel("Time per solve (s)")
  
    tickMarks = [0.1,0.2,0.3,0.4,0.5,0.6,0.8]
    tickMarkLabels = [str(np.round(x,1)) for x in tickMarks]
    axs.set_xticks(tickMarks)
    axs.set_xticklabels(tickMarkLabels, rotation=30)

    plt.tight_layout()
    handles, labels = axs.get_legend_handles_labels()
    fig.legend(handles, labels, bbox_to_anchor=(0.65, 0.65), loc='center left', borderaxespad=0., fontsize="small")

    #plt.show()
    plt.savefig("../figs/pb146-scaling.png",dpi=300)
    return
  def pb67():
    fig, axs = plt.subplots(1, 1, figsize=(13.5/2.0,5))

    E = 122284
    p = 7
    ranksPerNode = 6
    precisions = ["fp32"]
    path = "../data/summit/scaling/67peb"

    def custom_plotter(*args, **kwargs):
      axs.semilogx(*args, **kwargs)
      return
    machine_scaling_study(path,
      common.methodToName,
      precisions,
      E,
      p,
      plotter=custom_plotter)
    axs.set_title("$P=12:24$, SEMFEM is the only choice!", fontsize="x-large")

    # Add processor counts
    def custom_texter(*args, **kwargs):
      x, y, string = args
      if "12" in string:
        axs.text(x + 0.005, y, string, **kwargs, fontsize="large")
      if "24" in string:
        axs.text(x - 0.005, y - 1e7, string, **kwargs, fontsize="large")
      return

    add_processor_counts(path,
      {"semfem" : "SEMFEM"},
      precisions,
      E,
      p,
      texter=custom_texter)

    axs.grid(which="both")
    axs.set_ylabel("Gridpoints / (time per solve * node)")
    axs.set_xlabel("Time per solve (s)")
  
    tickMarks = [0.1,0.2,0.3,0.4,0.5,0.6,0.8]
    tickMarkLabels = [str(np.round(x,1)) for x in tickMarks]
    axs.set_xticks(tickMarks)
    axs.set_xticklabels(tickMarkLabels, rotation=30)

    plt.tight_layout()
    handles, labels = axs.get_legend_handles_labels()
    fig.legend(handles, labels, bbox_to_anchor=(0.225, 0.5), loc='center left', borderaxespad=0., fontsize="medium")

    #plt.show()
    plt.savefig("../figs/pb67-scaling.png",dpi=300)
    return
  def pb1568():
    fig, axs = plt.subplots(1, 1, figsize=(13.5/2.0,5))

    E = 524386
    p = 7
    ranksPerNode = 6
    precisions = ["fp32"]
    path = "../data/summit/scaling/pb1568"

    def custom_plotter(*args, **kwargs):
      axs.semilogx(*args, **kwargs)
      return
    machine_scaling_study(path,
      common.methodToName,
      precisions,
      E,
      p,
      plotter=custom_plotter)
    axs.set_title("$P=24:96$, SEMFEM wins", fontsize="x-large")
    # Add processor counts
    def custom_texter(*args, **kwargs):
      x, y, string = args
      if "24" in string:
        axs.text(x - 0.075, y - 1e7, string, **kwargs, fontsize="large")
      if "96" in string:
        axs.text(x - 0.025, y - 1e7, string, **kwargs, fontsize="large")
      return

    add_processor_counts(path,
      {"cheby-jac-boomeramg-1" : "Cheby-Jac(2),(9,7,5,1)"},
      precisions,
      E,
      p,
      texter=custom_texter)

    axs.grid(which="both")
    axs.set_ylabel("Gridpoints / (time per solve * node)")
    axs.set_xlabel("Time per solve (s)")
  
    tickMarks = np.linspace(0.2,0.8,num=7)
    tickMarkLabels = [str(np.round(x,1)) for x in tickMarks]
    axs.set_xticks(tickMarks)
    axs.set_xticklabels(tickMarkLabels, rotation=30)

    plt.tight_layout()
    handles, labels = axs.get_legend_handles_labels()
    fig.legend(handles, labels, bbox_to_anchor=(0.65, 0.65), loc='center left', borderaxespad=0., fontsize="medium")

    #plt.show()
    plt.savefig("../figs/pb1568-scaling.png",dpi=300)
    return
  
  #bsb()
  #pb146()
  #pb1568()
  pb67()