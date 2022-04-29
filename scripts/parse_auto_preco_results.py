import util
import numpy as np
import glob

def read_results(baseDir : str) -> str:
  tSolveRegex = "pressureSolve(\s+)(.+?)s"
  fastestRegex = "Determined fastest solver is : (.+)"
  procRegex = "MPI tasks: (.+)"
  nGPUsPerNode = 4
  table = "\\begin{table}\n\centering\n"
  table += "\\begin{tabular}{||c| c c c c c||}\n"
  table += "  \hline\n"
  table += "  Case & Nodes & Default Time & Tuner Time & Best Time & Best Solver \\\\"
  table += "  \hline\hline\n"
  for filePath in glob.glob(f"{baseDir}/*"):
    caseName = filePath.replace(f"{baseDir}/", "")
    nnodes        = util.field_by_regex(procRegex   , f"{filePath}/best-preco",    0, int)[0]/nGPUsPerNode
    tSolveBest    = np.round(util.field_by_regex(tSolveRegex , f"{filePath}/best-preco",    1)[0], 2)
    tSolveAuto    = np.round(util.field_by_regex(tSolveRegex , f"{filePath}/auto-preco",    1)[0], 2)
    tSolveDefault = np.round(util.field_by_regex(tSolveRegex , f"{filePath}/no-auto-preco", 1)[0], 2)
    fastestMethod = util.field_by_regex(fastestRegex, f"{filePath}/auto-preco",    0, str)[0]
    table += f"  {caseName} & {int(nnodes)} & {tSolveDefault} & {tSolveAuto} & {tSolveBest} & {fastestMethod} \\\\\n"
  
  table += "\\hline\n"
  table += "\\end{tabular}\n"
  table += "\\end{table}\n"
  return table


if __name__ == "__main__":
  #fileName = "../data/eig-results/kershaw/results"
  baseDir = "../data/auto-preco"
  print(read_results(baseDir))
