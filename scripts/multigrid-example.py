import numpy as np
import matplotlib.pyplot as plt

# generate plot of fine grid, unsmoothed
Nfine = 12
Ncoarse = 5
def unsmooth(N, axis):
  x = np.linspace(-1,1,N)
  def f(x):
    sumr = 0.0 * x
    for i in range(1,5):
      sumr += np.sin(i*np.pi*x)
    scale = np.max(np.abs(sumr))
    return sumr / scale
  y = f(x)
  axis.plot(x,y, "o-")
  axis.plot(x,0*x, "o-", color="black")
  axis.axis("off")

def smoothed(N, axis):
  x = np.linspace(-1,1,N)
  def f(x):
    sumr = 0.0 * x
    for i in range(1,2):
      sumr += np.sin(i*np.pi*x)
    scale = np.max(np.abs(sumr))
    return sumr / scale
  y = f(x)
  axis.plot(x,y, "o-")
  axis.plot(x,0*x, "o-", color="black")
  axis.axis("off")

fig = plt.figure(figsize=plt.figaspect(3.0))
axis = fig.add_subplot(3,1,1)
unsmooth(Nfine, axis)
axis = fig.add_subplot(3,1,2)
smoothed(Nfine, axis)
axis = fig.add_subplot(3,1,3)
smoothed(Ncoarse, axis)
#plt.tight_layout(pad=5)
plt.subplots_adjust(left=0.0, bottom=0.0, right=1.0, top=1.0, hspace=0.0)
plt.savefig("../figs/multigrid.png", dpi=300)
#plt.show()