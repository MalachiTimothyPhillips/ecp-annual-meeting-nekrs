import matplotlib.pyplot as plt
import matplotlib._color_data as mcd
import re
import glob
import numpy as np

def grab_latest_logfile(directory):
    latest = 0
    latestFile = ""
    for logfile in glob.glob(f"{directory}/*nekRS_*"): # capture "auto_preco_nekRS, too
        fileNum = int(re.search("nekRS_(.+?)\.(.+)", logfile).groups()[1])
        if fileNum > latest:
            latest = fileNum
            latestFile = logfile
    return latestFile
def grab_all_logfiles(directory):
    logFiles=[]
    fileNums=[]
    for logfile in glob.glob(f"{directory}/*nekRS_*"): # capture "auto_preco_nekRS, too
        fileNum = int(re.search("nekRS_(.+?)\.(.+)", logfile).groups()[1])
        logFiles.append(logfile)
        fileNums.append(fileNum)
    fileNums = np.asarray(fileNums)
    logFiles = np.asarray(logFiles)
    index = np.argsort(fileNums)[::-1]
    return logFiles[index]


methodToName={
  "cheby-jac" : "Cheby-Jac(2)+2crs,(7,5,3,1)",
  "cheby-jac-boomeramg-1" : "Cheby-Jac(2),(7,5,3,1)",
  "cheby-asm" : "Cheby-ASM(2),(7,3,1)",
  "cheby-ras" : "Cheby-RAS(2),(7,3,1)",
  "cheby-asm-1" : "Cheby-ASM(1),(7,3,1)",
  "cheby-ras-1" : "Cheby-RAS(1),(7,3,1)",
  "cheby-asm-3" : "Cheby-ASM(3),(7,3,1)",
  "cheby-ras-3" : "Cheby-RAS(3),(7,3,1)",
  "cheby-asm-pmg-7531" : "Cheby-ASM(2),(7,5,3,1)",
  "cheby-ras-pmg-7531" : "Cheby-RAS(2),(7,5,3,1)",
  "semfem"    : "SEMFEM",
  "combo"     : "Cheby-ASM(2),(7,6)+SEMFEM",
  "combo-v2"     : "Cheby-ASM(2),(7,5)+SEMFEM",
  "combo-v3"     : "Cheby-ASM(2),(7,3)+SEMFEM",
  #"auto"    : "Auto-tuned",
}
methodToNameBSB={
  "cheby-jac" : "Cheby-Jac(2)+2crs,(9,7,5,1)",
  "cheby-jac-boomeramg-1" : "Cheby-Jac(2),(9,7,5,1)",
  "cheby-asm" : "Cheby-ASM(2),(9,5,1)",
  "cheby-ras" : "Cheby-RAS(2),(9,5,1)",
  "cheby-asm-1" : "Cheby-ASM(1),(9,5,1)",
  "cheby-ras-1" : "Cheby-RAS(1),(9,5,1)",
  "cheby-asm-3" : "Cheby-ASM(3),(9,5,1)",
  "cheby-ras-3" : "Cheby-RAS(3),(9,5,1)",
  "cheby-asm-pmg-9751" : "Cheby-ASM(2),(9,7,5,1)",
  "cheby-ras-pmg-9751" : "Cheby-RAS(2),(9,7,5,1)",
  "semfem"    : "SEMFEM",
  "combo"     : "Cheby-ASM(2),(9,8)+SEMFEM",
  "combo-v2"     : "Cheby-ASM(2),(9,7)+SEMFEM",
  "combo-v3"     : "Cheby-ASM(2),(9,5)+SEMFEM",
  "combo-v4"     : "Cheby-ASM(2),(9,3)+SEMFEM",
  #"auto"    : "Auto-tuned",
}


# Order is ugly
#color_cycle=[]
#for xkcdName, colorHash in mcd.XKCD_COLORS.items():
#  color_cycle.append(colorHash)

#https://xkcd.com/color/rgb/
color_cycle = [
  "#7e1e9c", # pruple
  "#15b01a", # green
  "#0343df", # blue
  "#ff81c0", # pink
  "#653700", # brown
  # skip red (RG colorblind-ness)
  # skip light blue (too
  # skip teal
  "#f97306", # orange (UIUC!)
  # skip light green
  "#c20078", # magenta
  # skip yellow
  # skip sky blue
  "#929591", # grey
  # skip lime green
  "#bf77f6", # light purple
  # skip a few more...
  "#00035b", # dark blue
]

markerStyles=["o","v"]
lineStyles=["dotted", "dashed"]

precisionToMarker = {
  "FP32" : "o",
  "FP64" : "v"
}

archToLineStyle = {
  "GPU" : "dotted",
  "CPU" : "dashed"
}

orderMarker = {
  1 : "v",
  2 : "o",
  3 : "x",
}

methodToColor = {
  "SEMFEM" : color_cycle[0],
  "ASM" : color_cycle[4],
  "RAS" : color_cycle[5],
  "CHEBY-JAC" : color_cycle[3],
  "CHEBY-ASM" : "black", # our default solver
  "CHEBY-RAS" : color_cycle[1],
  "IDEAL SEMFEM" : color_cycle[6],
  "JACOBI" : color_cycle[7],
  "AUTO" : color_cycle[2],
  "COMBO" : color_cycle[8],
}

def grab_color(methodName):
  longestSubStr = ""
  lengthLongestSubStr = 0
  for method in methodToColor.keys():
    if method.upper() in methodName.upper():
      if len(method) > lengthLongestSubStr:
        lengthLongestSubStr = len(method)
        longestSubStr = method
  return methodToColor[longestSubStr]

def parse_order(methodName):
  regex = "cheby-(.+?)-(\d)"
  m = re.search(regex, methodName)
  if m and "pmg" not in methodName:
    return orderMarker[int(m.groups()[1])]
  elif "boomeramg" in methodName:
    return "v"
  elif "pmg" in methodName:
    return "s"
  elif "combo" in methodName:
    if "v2" in methodName:
      return "^"
    if "v3" in methodName:
      return "x"
    if "v4" in methodName:
      return "s"
    return "o"
  else:
    return "o"

def add_marker_attributes(plotter = plt.loglog):
    for precision, markerStyle in precisionToMarker.items():
        plotter([],[],marker=markerStyle,lineStyle='None',label=precision, color='k')