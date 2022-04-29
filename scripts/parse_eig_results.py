import util
import numpy as np

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
def read_results(fileName : str) -> str:
  minEigRegex = "Min Multiplier : (.+)"
  maxEigRegex = "Max Multiplier : (.+)"
  NiterRegex  = "Niter          : (.+)"
  ConvRegex   = "Conv Rate      : (.+)"
  minEigs = np.asarray(util.field_by_regex(minEigRegex, fileName))
  maxEigs = np.asarray(util.field_by_regex(maxEigRegex, fileName))
  iters   = np.asarray(util.field_by_regex(NiterRegex , fileName))
  rates   = np.asarray(util.field_by_regex(ConvRegex  , fileName))

  iters = iters.astype(int)
  rates = np.round(rates, decimals=5)

  def gen_table(qoi, minEigs, maxEigs):
    table = "\\renewcommand{\\arraystretch}{2}\n"
    table += "\\begin{table}\n\centering\n"
    nCols = len(np.unique(maxEigs))
    nRows = len(np.unique(minEigs))
    table += "\\begin{tabular}{||c|" + " c" * nCols + "||}\n"
    table += "  \hline\n"
    table += "  $\lambda_{min}\\backslash \lambda_{max}$"
    for maxEig in np.unique(maxEigs):
      table += f" & ${maxEig} \\tilde\\lambda$"
    table += "  \\\\ \n"
    table += "\\hline\\hline\n"

    minEigs = np.unique(minEigs)
    maxEigs = np.unique(maxEigs)

    for rowId in range(0, nRows):
      table += f"${minEigs[rowId]} \\tilde\\lambda$"
      for colId in range(0, nCols):
        table += f" & {qoi[colId*nRows + rowId]}"
      table += " \\\\ \n"
  
    table += "\\hline\n"
    table += "\\end{tabular}\n"
    table += "\\end{table}\n"
    return table
  
  table1 = gen_table(iters, minEigs, maxEigs)
  table2 = gen_table(rates, minEigs, maxEigs)
  return table1 + "\n\n" + table2


if __name__ == "__main__":
  #fileName = "../data/eig-results/kershaw/results-0.1"
  #fileName = "../data/eig-results/kershaw/results-0.3"
  #fileName = "../data/eig-results/kershaw/results-1.0"
  #fileName = "../data/eig-results/kershaw/updated-results-eps-0.3"
  fileName = "../data/eig-results/kershaw/more-results-0.3"
  print(read_results(fileName))
