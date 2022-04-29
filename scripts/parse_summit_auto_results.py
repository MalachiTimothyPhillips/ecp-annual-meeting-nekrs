import util
import numpy as np
import glob

"""
\begin{table}[h!]
\centering
\begin{tabular}{||c c c c||} 
 \hline
 Col1 & Col2 & Col2 & Col3 \\ [0.5ex] 
 \hline\hline
 1 & 6 & 87837 & 787 \\ 
 2 & 7 & 78 & 5415 \\
 3 & 545 & 778 & 7507 \\
 4 & 545 & 18744 & 7560 \\
 5 & 88 & 788 & 6344 \\ [1ex] 
 \hline
\end{tabular}
\caption{This is the caption for the first table.}
\label{table:1}
\end{table}
"""

def table_start():
  table = "\\begin{table}\n\centering\n"
  table += "\\begin{tabular}{||c| c c c c c c c||}\n"
  table += "  \\hline\n"
  table += "  Case Name & $P$ ($n/P$) & Smoother Type & Order & Schedule & Time/solve & Speedup (Default) & Speedup (Worst)\\\\\n"
  table += "  \\hline\\hline\n"
  return table

def table_end():
    table = "\\hline\n"
    table += "\\end{tabular}\n"
    table += "\\end{table}\n"
    return table

def read_results(caseName, fileNames) -> str:

  smoothers = [
    "Chebyshev+Jacobi",
    "Chebyshev+ASM",
    "Chebyshev+RAS",
  ]
  degrees = [1,2,3]

  taskRegex = "MPI tasks: (.+)"
  ranksPerNode = 6

  table = ""

  tDefault = 0.0
  tMin = np.inf
  defaultSmoother = "Chebyshev+ASM+Degree=2"
  minSmoother = ""

  for fileName in fileNames:
    for smoother in smoothers:
      for degree in degrees:
        regex = smoother.replace("+", "\+") + "\+Degree=" + str(degree) + " took (.+) s"
        smootherString = smoother + "+Degree=" + str(degree)
        time = util.field_by_regex(regex, fileName)
        if time:
          tSmoother = time[0]
          if tSmoother < tMin:
            tMin = tSmoother
            minSmoother = smootherString
          if smootherString == defaultSmoother:
            tDefault = tSmoother
    nodes = util.field_by_regex(taskRegex, fileName)[0] / ranksPerNode
    minSmoother = minSmoother.replace("Chebyshev+", "")
    minSmoother = minSmoother.replace("Degree=", "")
    minSmoother = minSmoother.replace("+", ",")
    table += f"  {caseName} & {int(nodes)} & {minSmoother} & {np.round(tMin / 50.,3)} & {np.round(tDefault / tMin, 3)}\\\\\n"
  
  return table


if __name__ == "__main__":

  def make_table():
    table = table_start()

    nodes = [1,2,3]
    for node in nodes:
      files = glob.glob(f"../data/summit/scaling/pb146/fp32/auto-{node}/*")
      table += read_results("146 pebble", files)
    
    table += "  \\hline\n"

    nodes = [8,12,16]
    for node in nodes:
      files = glob.glob(f"../data/summit/scaling/pb1568/fp32/auto-{node}/*")
      table += read_results("1568 pebble", files)

    nodes = [24,36,48,60,72]
    for node in nodes:
      files = glob.glob(f"../data/summit/scaling/BoeingSpeedBump/fp32/auto-{node}/*")
      table += read_results("speed bump", files)

    table += table_end()
    print(table)
  
  make_table()