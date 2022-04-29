import glob
import os
import re
import numpy as np
import matplotlib.pyplot as plt
from util import field_by_regex
import common

def parse_pressure_solver_time(baseDir, precision, method, nodes, ranksPerNode, outputFile):
  pressureIterationRegex = "P:(\s+)(\d+)\s"
  timeSolveRegex = "total solve(\s+)(.+?)s"
  pressureSolveRegex = "pressureSolve(\s+)(.+?)s"
  alternateStepRegex = "step=  (.+?) runtime statistics"
  stepRegex = "runtime statistics \(step = (.+?)\)"
  tunerRegex = "tuner(.+?)s"

  rows=[]
  for node in nodes:
      logfile = common.grab_latest_logfile(f"{baseDir}/{precision}/{method}-{node}")
      if os.path.isfile(logfile):
        time_to_solution = field_by_regex(pressureSolveRegex, logfile, 1)
        time_ns = field_by_regex(timeSolveRegex, logfile, 1)
        steps = field_by_regex(stepRegex, logfile, 0)
        pressureIters = field_by_regex(pressureIterationRegex, logfile, 1)
        pressureIters = np.asarray(pressureIters)
        iters = np.mean(pressureIters)
        #tuner = field_by_regex(tunerRegex, logfile, 0)
        print(f"Steps = {steps}")
        print(f"Time to solution = {time_to_solution}")
        print(f"NS time = {time_ns}")
        #print(f"Tuner = {tuner}")
        if time_to_solution:
            if len(steps) != len(time_to_solution):
              steps = field_by_regex(alternateStepRegex, logfile, 0)
              assert(len(steps) == len(time_to_solution))
            time_to_solution = np.array(time_to_solution)
            time_ns = np.array(time_ns)
            #if tuner:
            #  assert(len(tuner) == len(time_to_solution))
            #  tuner = np.array(tuner)
            #  time_to_solution -= tuner
            rows.append([node,time_to_solution[-1],steps[-1],time_ns[-1],iters])
  matrix = np.asarray(rows)
  #np.savetxt(f"../data/summit/scaling/pb146/{method}-{precision}.csv", matrix, delimiter=",")
  np.savetxt(outputFile, matrix, delimiter=",")

if __name__ == "__main__":
  #methods=["semfem", "cheby-jac", "cheby-asm", "cheby-ras", "auto"]
  #precisions=["fp32", "fp64"]
  precisions=["fp32"]
  ranksPerNode=6
  def pb146():
    methods = common.methodToName.keys()
    #methods = ["combo"]
    #methods = ["combo", "combo-v2", "combo-v3"]
    nodes=[0.5,1,2,3]
    for method in methods:
        for precision in precisions:
          outputFile = f"../data/summit/scaling/pb146/ns-{method}-{precision}.csv"
          parse_pressure_solver_time(f"../data/summit/scaling/pb146/",
            precision,
            method,
            nodes,
            ranksPerNode,
            outputFile)
  def pb1568():
    #nodes=[8,11,12,16,22,24]
    #nodes=[8,12,16,24]
    nodes=[4,8,12,16]
    methods = common.methodToName.keys()
    #methods = ["combo"]
    #methods = ["combo-v2", "combo-v3"]
    #methods = ["combo", "combo-v2", "combo-v3"]
    for method in methods:
        for precision in ["fp32"]:
          outputFile = f"../data/summit/scaling/pb1568/ns-{method}-{precision}.csv"
          parse_pressure_solver_time(f"../data/summit/scaling/pb1568/",
            precision,
            method,
            nodes,
            ranksPerNode,
            outputFile)
  def BoeingSpeedBump():
    #nodes=[8,11,12,16,22,24]
    nodes=[16,24,36,48,60,72]
    methods = common.methodToNameBSB.keys()
    #methods = ["combo"]
    #methods = ["combo-v2", "combo-v3", "combo-v4"]
    #methods = ["combo", "combo-v2", "combo-v3", "combo-v4"]
    for method in methods:
        for precision in ["fp32"]:
          outputFile = f"../data/summit/scaling/BoeingSpeedBump/ns-{method}-{precision}.csv"
          parse_pressure_solver_time(f"../data/summit/scaling/BoeingSpeedBump/",
            precision,
            method,
            nodes,
            ranksPerNode,
            outputFile)
  def pb67():
    #nodes=[1,2,3,4]
    nodes=[2,3,4]
    methods = common.methodToName.keys()
    #methods = ["combo-v2", "combo-v3"]
    #methods = ["combo", "combo-v2", "combo-v3"]
    for method in methods:
        for precision in ["fp32"]:
          outputFile = f"../data/summit/scaling/67peb/ns-{method}-{precision}.csv"
          parse_pressure_solver_time(f"../data/summit/scaling/67peb/",
            precision,
            method,
            nodes,
            ranksPerNode,
            outputFile)
  pb146()
  pb1568()
  BoeingSpeedBump()
  pb67()
