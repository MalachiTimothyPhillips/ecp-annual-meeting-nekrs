import glob
import os
import re
import numpy as np
import matplotlib.pyplot as plt
import common

def efficiency_plot(path, mapMethodToName, precisions):
  for method in mapMethodToName.keys():
      for precision in precisions:
        fileName = f"{path}/{method}-{precision}.csv"
        data = np.genfromtxt(fileName, delimiter=',')
        if len(data.shape) > 1:
            nodes = data[:,0]
            time_to_solutions = data[:,1]
            speedup = data[:,1]/data[0,1]
            rankRatio = data[0,0]/data[:,0]
            eff = speedup * rankRatio
            plt.semilogx(nodes * 6, 
              eff,
              color = common.grab_color(method),
              marker = common.parse_order(method),
              label = mapMethodToName[method],
              linestyle = common.archToLineStyle["GPU"])
  plt.grid(which="both")
  plt.legend(prop={'size':6})
  return
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
  
  #plt.grid(which="both")
  #plt.legend(prop={'size':6})

if __name__ == "__main__":
  def pb146():
    E = 62132
    p = 7
    ranksPerNode = 6
    precisions = ["fp32"]
    path = "../data/summit/scaling/pb146"
    outputFileName = "../figs/pb146-machine-study.png"

    machine_scaling_study(path,
      common.methodToName,
      precisions,
      E,
      p)

    plt.title("pb146, $P=3:18$")
    plt.xlabel("Time per solve (s)")
    plt.ylabel("Gridpoints / (time per solve * node)")
    plt.legend()
    plt.grid(which="both")
    plt.savefig(outputFileName,dpi=300)
    plt.clf()

    outputFileName = "../figs/pb146-strong-scaling-eff.png"
    efficiency_plot(path,
      common.methodToName,
      precisions)

    plt.title("pb146, $P=3:18$")
    plt.xlabel("Ranks")
    plt.ylabel("Parallel Efficiency")
    plt.savefig(outputFileName,dpi=300)
    plt.clf()

  def pb1568():
    E = 524386
    p = 7
    ranksPerNode = 6
    methods=["semfem","cheby-jac", "cheby-asm", "cheby-ras", "auto"]
    precisions = ["fp32"]
    path = "../data/summit/scaling/pb1568"
    outputFileName = "../figs/pb1568-machine-study.png"

    #common.add_marker_attributes()
    machine_scaling_study(path,
      common.methodToName,
      precisions,
      E,
      p)

    plt.title("pb1568, $P=24:96$")
    plt.xlabel("Time per solve (s)")
    plt.ylabel("Gridpoints / (time per solve * node)")
    plt.savefig(outputFileName,dpi=300)
    plt.clf()

    outputFileName = "../figs/pb1568-strong-scaling-eff.png"
    efficiency_plot(path,
      common.methodToName,
      precisions)

    plt.title("pb1568, $P=24:96$")
    plt.xlabel("Ranks")
    plt.ylabel("Parallel Efficiency")
    plt.savefig(outputFileName,dpi=300)
    plt.clf()

  def BoeingSpeedBump():
    E = 884736
    p = 9
    ranksPerNode = 6
    #methods=["semfem","cheby-jac", "cheby-asm", "cheby-ras", "auto"]
    methods=["semfem","cheby-jac", "cheby-asm", "cheby-ras"]
    precisions = ["fp32"]
    path = "../data/summit/scaling/BoeingSpeedBump"
    outputFileName = "../figs/BoeingSpeedBump-machine-study.png"
    #common.add_marker_attributes()
    machine_scaling_study(path,
      common.methodToNameBSB,
      precisions,
      E,
      p)

    plt.title("BoeingSpeedBump, $P=96:432$")
    plt.xlabel("Time per solve (s)")
    plt.ylabel("Gridpoints / (time per solve * node)")
    plt.savefig(outputFileName,dpi=300)
    plt.clf()

    outputFileName = "../figs/BoeingSpeedBump-strong-scaling-eff.png"
    #common.add_marker_attributes()
    efficiency_plot(path,
      common.methodToNameBSB,
      precisions)

    plt.title("BoeingSpeedBump, $P=96:432$")
    plt.xlabel("Ranks")
    plt.ylabel("Parallel Efficiency")
    plt.savefig(outputFileName,dpi=300)
    plt.clf()

  pb146()
  pb1568()
  BoeingSpeedBump()

  plotPebble = True
  if 0:
    fig, axs = plt.subplots(1, 1, figsize=(13.5/2.0,5))
    E = 122284
    p = 7
    ranksPerNode = 6
    precisions = ["fp32"]
    path = "../data/summit/scaling/67peb"
    machine_scaling_study(path,
      common.methodToName,
      precisions,
      E,
      p,
      plotter=plt.semilogx)
    plt.title("pb67, $P=12:24$, pMG")
    plt.xlabel("Time per solve (s)")
    plt.ylabel("Gridpoints / (time per solve * node)")
    #plt.legend()
    plt.grid(which="both")
    plt.tight_layout()
    plt.subplots_adjust(right=0.75)
    handles, labels = axs.get_legend_handles_labels()
    fig.legend(handles, labels, bbox_to_anchor=(0.6, 0.7), loc='center left', borderaxespad=0., fontsize="medium")
    #plt.show()
    plt.savefig("../figs/pb67-zoom-scaling.png",dpi=300)

    exit()

  if plotPebble:
    #fig, axs = plt.subplots(1, 3, figsize=(13.5,4))
    fig, axs = plt.subplots(1, 3, figsize=plt.figaspect(1.0/3.0))

    E = 62132
    p = 7
    ranksPerNode = 6
    precisions = ["fp32"]
    path = "../data/summit/scaling/pb146"

    def custom_plotter(*args, **kwargs):
      axs[0].semilogx(*args, **kwargs)
      return
    machine_scaling_study(path,
      common.methodToName,
      precisions,
      E,
      p,
      plotter=custom_plotter)
  
    axs[0].set_title("pb146, $P=3:18$")
    axs[0].set_ylabel("Gridpoints / (time per solve * node)")

    E = 122284
    p = 7
    ranksPerNode = 6
    precisions = ["fp32"]
    path = "../data/summit/scaling/67peb"
    def custom_plotter(*args, **kwargs):
      axs[2].semilogx(*args, **kwargs)
      return
    machine_scaling_study(path,
      common.methodToName,
      precisions,
      E,
      p,
      plotter=custom_plotter)
    axs[2].set_title("pb67, $P=12:24$")

    # add line for P=18 
    if 0:
      def my_plotter(xdat,ydat):
        axs[2].semilogx(xdat,ydat,color="black",linestyle="--")
        return
      gather_constant_rank_data(path,
        common.methodToName,
        precisions,
        E,
        p,
        3, # plot at 3 nodes
        plotter=my_plotter)
    
      # add annotation
      axs[2].annotate("$P=18$", xy=(0.34, 0.49), xytext=(0.5,0.65), xycoords='axes fraction', fontsize="medium",
        arrowprops=dict(facecolor='black', width=1, headwidth=5))

    E = 524386
    p = 7
    ranksPerNode = 6
    precisions = ["fp32"]
    path = "../data/summit/scaling/pb1568"

    def custom_plotter(*args, **kwargs):
      axs[1].semilogx(*args, **kwargs)
      return
    machine_scaling_study(path,
      common.methodToName,
      precisions,
      E,
      p,
      plotter=custom_plotter)
    axs[1].set_title("pb1568, $P=24:96$")

    tickMarks = [0.1,0.2,0.3,0.4,0.5,0.6,0.8]
    tickMarkLabels = [str(np.round(x,1)) for x in tickMarks]
    axs[0].set_xticks(tickMarks)
    axs[0].set_xticklabels(tickMarkLabels, rotation=30)
    tickMarks = np.linspace(0.2,0.8,num=7)
    tickMarkLabels = [str(np.round(x,1)) for x in tickMarks]
    axs[1].set_xticks(tickMarks)
    axs[1].set_xticklabels(tickMarkLabels, rotation=30)
    tickMarks = [0.1,0.2,0.3,0.4,0.5,0.6,0.8]
    tickMarkLabels = [str(np.round(x,1)) for x in tickMarks]
    axs[2].set_xticks(tickMarks)
    axs[2].set_xticklabels(tickMarkLabels, rotation=30)
    for ax in axs.flat:
      ax.grid(which="both")
      ax.set_xlabel("Time per solve (s)")

    plt.tight_layout()
    plt.subplots_adjust(right=0.78)
    handles, labels = ax.get_legend_handles_labels()
    fig.legend(handles, labels, bbox_to_anchor=(0.6, 0.7), loc='center left', borderaxespad=0., fontsize="medium")
    #fig.legend(handles, labels)
    myFont = {'fontname': 'serif'}
    #myFont = {'fontname': 'Times New Roman'}
    #myFont = {'fontname': 'Helvetica'}
    
    axs[0].annotate("(a)", xy=(-0.10,-0.175), xycoords="axes fraction", fontsize=16, **myFont)
    axs[1].annotate("(b)", xy=(-0.10,-0.175), xycoords="axes fraction", fontsize=16, **myFont)
    axs[2].annotate("(c)", xy=(-0.10,-0.175), xycoords="axes fraction", fontsize=16, **myFont)

    #plt.show()
    #plt.savefig("../figs/pb-scaling.png",dpi=300)
  else:

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
    axs.set_title("BoeingSpeedBump, $P=96:432$")

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