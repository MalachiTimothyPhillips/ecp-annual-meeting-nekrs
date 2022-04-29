import argparse
import numpy as np
import util
import matplotlib.pyplot as plt

def rolling_average(a, n=3) :
    ret = np.cumsum(a, dtype=float)
    ret[n:] = ret[n:] - ret[:-n]
    return ret[n - 1:] / n

def parse_history(filename : str):
  toleranceRegex = "P  :(.+?)tol (.+)"
  iterationRegex = "P  : iter (.+?) "
  divErrRegex = "divErrNorms (.+?) (.+)"

  tolerances = util.field_by_regex(toleranceRegex, filename, 1)
  iterations = util.field_by_regex(iterationRegex, filename, 0)
  errors = util.field_by_regex(divErrRegex, filename, 1)
  weightedErrors = util.field_by_regex(divErrRegex, filename, 0)
  tolerances = np.asarray(tolerances)
  iterations = np.asarray(iterations)
  errors = np.asarray(errors)
  weightedErrors = np.asarray(weightedErrors)

  return tolerances, iterations, errors, weightedErrors

def add_cumulative_qoi_line(qoi, labelName):
  cumQoi = np.cumsum(qoi)
  solveCounts = np.arange(1,cumQoi.shape[0]+1)
  plt.plot(solveCounts, cumQoi, label=f"${labelName}$")

def add_qoi_line(qoi, labelName, plotter = plt.plot):
  solveCounts = np.arange(1,qoi.shape[0]+1)
  plotter(solveCounts, qoi, label=f"${labelName}$")

def add_qoi_rolling_avg_line(qoi, labelName, plotter = plt.plot, N = 3):
  rollingAvgQoi = rolling_average(qoi, N)
  solveCounts = np.arange(1,rollingAvgQoi.shape[0]+1)
  plotter(solveCounts, rollingAvgQoi, label=f"${labelName}$")

def plot_cumulative_qoi(qois, labels, pngFile, xlabel = "", ylabel = "", title = ""):
  for qoi, label in zip(qois, labels):
    add_cumulative_qoi_line(qoi, label)
  
  plt.legend()
  plt.xlabel(xlabel)
  plt.ylabel(ylabel)
  plt.title(title)
  #plt.show()
  print(f"Writing pngFile = {pngFile}")
  plt.savefig(pngFile, dpi=300)
  plt.clf()

def plot_qoi(qois, labels, pngFile, xlabel = "", ylabel = "", title = "", plotter = plt.plot):
  for qoi, label in zip(qois, labels):
    add_qoi_line(qoi, label, plotter)
  
  plt.legend()
  plt.xlabel(xlabel)
  plt.ylabel(ylabel)
  plt.title(title)
  #plt.show()
  plt.savefig(pngFile, dpi=300)
  plt.clf()

def plot_rolling_avg_qoi(qois, labels, pngFile, xlabel = "", ylabel = "", title = "", plotter = plt.plot, N=3):
  for qoi, label in zip(qois, labels):
    add_qoi_rolling_avg_line(qoi, label, plotter, N)
  
  plt.legend()
  plt.xlabel(xlabel)
  plt.ylabel(ylabel)
  plt.title(title)
  #plt.show()
  plt.savefig(pngFile, dpi=300)
  plt.clf()



if __name__ == "__main__":

  def gen_ethier_auto_tol_plot():
    fileNames = [
      "../data/auto-tol/ethier/results-1e-4-div-err",
      "../data/auto-tol/ethier/results-1e-6-tol"
    ]
    names = [
      "\\vert\\vert Q_T - \\nabla \\cdot u\\vert\\vert < 10^{-4}",
      "Tol_{Pr} = 10^{-6}"
    ]
    allIterations = []
    allTolerances = []
    allErrors = []
    allWeightedErrors = []
    for fileName in fileNames:
      tolerances, iterations, errors, weightedErrors = parse_history(fileName)
      allIterations.append(iterations)
      allTolerances.append(tolerances)
      allErrors.append(errors)
      allWeightedErrors.append(weightedErrors)
    plot_cumulative_qoi(allIterations,
      names,
      "../figs/ethier-auto-tol-pr-iterations.png",
      "Solve Count",
      "Pressure Iterations",
      "ethier, Jacobi preconditioner")
    plot_qoi([allTolerances[0]],
      [names[0]],
      "../figs/ethier-auto-tol-pr-tol.png",
      "Solve Count",
      "Pressure Tolerance",
      "ethier, Jacobi preconditioner",
      plt.semilogy)

    plt.semilogy(np.arange(1,allErrors[0].shape[0]+1), [1e-4]*allErrors[0].shape[0])
    plot_qoi(allErrors,
      names,
      "../figs/ethier-auto-tol-pr-div-err.png",
      "Solve Count",
      "$\\vert\\vert Q_T - \\nabla \\cdot u\\vert\\vert$",
      "ethier, Jacobi preconditioner",
      plt.semilogy)
    return
  
  def gen_turbpipe_auto_tol_plot():
    fileNames = [
      #"../data/auto-tol/turbPipe/turbPipe-tol-div-1e-2",
      #"../data/auto-tol/turbPipe/turbPipe-tol-div-1e-1",
      "../data/auto-tol/turbPipe/turbPipe-tol-div-5e-1",
      "../data/auto-tol/turbPipe/turbPipe-tol-1e-4"
    ]
    names = [
      #"\\vert\\vert Q_T - \\nabla \\cdot u\\vert\\vert < 10^{-2}",
      #"\\vert\\vert Q_T - \\nabla \\cdot u\\vert\\vert < 10^{-1}",
      "\\vert\\vert Q_T - \\nabla \\cdot u\\vert\\vert < 5\\times 10^{-1}",
      "Tol_{Pr} = 10^{-4}"
    ]
    allIterations = []
    allTolerances = []
    allErrors = []
    allWeightedErrors = []
    for fileName in fileNames:
      tolerances, iterations, errors, weightedErrors = parse_history(fileName)
      allIterations.append(iterations)
      allTolerances.append(tolerances)
      allErrors.append(errors)
      allWeightedErrors.append(weightedErrors)
    plot_cumulative_qoi(allIterations,
      names,
      "../figs/turbPipe-auto-tol-pr-iterations.png",
      "Solve Count",
      "Pressure Iterations",
      "turbPipe")
    #plot_qoi(allTolerances,
    #  names,
    #  "../figs/turbPipe-auto-tol-pr-tol.png",
    #  "Solve Count",
    #  "Pressure Tolerance",
    #  "turbPipe",
    #  plt.semilogy)

    plot_qoi(allErrors,
      names,
      "../figs/turbPipe-auto-tol-pr-div-err.png",
      "Solve Count",
      "$\\vert\\vert Q_T - \\nabla \\cdot u\\vert\\vert$",
      "turbPipe",
      plt.semilogy)
    plot_qoi(allWeightedErrors,
      names,
      "../figs/turbPipe-auto-tol-pr-wt-avg-div-err.png",
      "Solve Count",
      "$avg(Q_T - \\nabla \\cdot u)$",
      "turbPipe",
      plt.semilogy)
    plot_rolling_avg_qoi(allWeightedErrors,
      names,
      "../figs/turbPipe-auto-tol-pr-wt-rolling-avg-div-err.png",
      "Solve Count",
      "$\\operatorname{rollingAvg}(Q_T - \\nabla \\cdot u)$",
      "turbPipe",
      plt.semilogy,
      N = 100)
    return
  
  gen_ethier_auto_tol_plot()
  plt.clf()
  gen_turbpipe_auto_tol_plot()
  plt.clf()