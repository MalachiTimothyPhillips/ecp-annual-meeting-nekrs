from sem import zwgll
import numpy as np
import matplotlib.pyplot as plt

p = 12
z,w = zwgll(p)
dOmega = np.pi/6
r0 = 0.5
dr = 1.0 - r0

thetas=[np.pi/2, np.pi/2-dOmega]
Xs=[]
Ys=[]
Xapprox_s=[]
Yapprox_s=[]

def make_linear_function(x0,x1,y0,y1):
    slope = (y1-y0)/(x1-x0)
    b = y0 - slope * x0
    def f(x):
        return slope*x + b
    return f

for theta0 in thetas:
    z_rMapper = make_linear_function(z[0],z[-1],r0,r0+dr)
    z_thetaMapper = make_linear_function(z[0],z[-1],theta0,theta0+dOmega)
    r, theta = z_rMapper(z), z_thetaMapper(z)
    # Generate x,y coordinates and display domain Omega
    R, Theta = np.meshgrid(r,theta)
    X,Y = R*np.cos(Theta), R*np.sin(Theta)
    Xs.append(X)
    Ys.append(Y)

def plane_space_harmonic_mean_wt(X,Y):
    lx = 0.0
    sumr = 0.0
    ly = 0.0
    for i in range(len(X[:,0])):
        dist_x = X[i,-1]-X[i,0]
        dist_y = Y[i,-1]-Y[i,0]
        lx += w[i] / (dist_x ** 2. + dist_y ** 2.)
        sumr += w[i]
    lx /= sumr
    lx = 1./np.sqrt(lx)
    for i in range(len(X[:,0])):
        dist_x = X[-1,i]-X[0,i]
        dist_y = Y[-1,i]-Y[0,i]
        ly += w[i] / (dist_x ** 2. + dist_y ** 2.)
        sumr += w[i]
    ly /= sumr
    ly = 1./np.sqrt(ly)
    mean_l = np.mean(X.flatten())
    mean_b = np.mean(Y.flatten())
    return mean_l, mean_b, lx, ly

for X,Y in zip(Xs,Ys):
    mean_l, mean_b, lx, ly = plane_space_harmonic_mean_wt(X,Y)
    z_arithmean_x = make_linear_function(z[0],z[-1],mean_l-0.5*lx, mean_l+0.5*lx)
    z_arithmean_y = make_linear_function(z[0],z[-1],mean_b-0.5*ly, mean_b+0.5*ly)
    x_approx = z_arithmean_x(z)
    y_approx = z_arithmean_y(z)
    X_approx, Y_approx = np.meshgrid(x_approx, y_approx)
    Xapprox_s.append(X_approx)
    Yapprox_s.append(Y_approx)

def plot_element(X,Y,color,index = 1, offset = 0.0, symbol = "\\Omega_"):
    x_center = np.mean(X.flatten())
    y_center = np.mean(Y.flatten())
    for i, x in enumerate(X[:,0]):
        if i == 0 or i == len(X[:,0])-1:
            plt.plot(X[:,i], Y[:,i], color = color, linewidth=1, linestyle="solid")
    for i, x in enumerate(X[:,0]):
        if i == 0 or i == len(X[:,0])-1:
            plt.plot(X[i,:], Y[i,:], color = color, linewidth=1, linestyle="solid")
    plt.text(x_center+offset,y_center+offset,f"${symbol}" + f"{index}$", color = color, size=24)

for i, (X,Y,X_approx,Y_approx) in enumerate(zip(Xs,Ys,Xapprox_s,Yapprox_s)):
    plot_element(X,Y,"black", i+1, -0.05, "\\Omega_")
    plot_element(X_approx,Y_approx,"blue", i+1, 0.0, "\\bar \\Omega_")

plt.axis("equal")
plt.axis("off")
plt.tight_layout()
plt.savefig(f"../figs/schwarz-approximation.png", dpi=300)
plt.clf()

p=5
z,w = zwgll(p)
dz = z[2]-z[0]
dz_near = z[1]-z[0]
z_ext = np.zeros(p+3+2)
z_ext[0] = -1 - dz
z_ext[1] = -1 - dz_near
z_ext[2:-2] = z
z_ext[-2] = 1+dz_near
z_ext[-1] = 1+dz

elements = [
  np.meshgrid(z,z),
  np.meshgrid(z+2,z+2),
  np.meshgrid(z+2,z),
  np.meshgrid(z,z+2),
  np.meshgrid(z-2,z-2),
  np.meshgrid(z-2,z),
  np.meshgrid(z,z-2),
  np.meshgrid(z+2,z-2),
  np.meshgrid(z-2,z+2),
           ]

def plot_element(X,Y,color,primary=True):
    plt.scatter(X,Y,color=color, s=2)
    solidLine = "solid"
    if not primary:
        solidLine = "dashed"
    for i, x in enumerate(X[:,0]):
        if i == 0 or i == len(X[:,0])-1:
            plt.plot(X[:,i], Y[:,i], color = color, linewidth=1, linestyle=solidLine)
        else:
            #plt.plot(X[:,i], Y[:,i], color = color, linewidth=1, linestyle="dashed")
            pass
    for i, x in enumerate(X[:,0]):
        if i == 0 or i == len(X[:,0])-1:
            plt.plot(X[i,:], Y[i,:], color = color, linewidth=1, linestyle=solidLine)
        else:
            #plt.plot(X[i,:], Y[i,:], color = color, linewidth=1, linestyle="dashed")
            pass

for element in elements:
    X,Y = element
    plot_element(X, Y, "black",primary=False)
X,Y = np.meshgrid(z_ext,z_ext)
plot_element(X,Y, "blue")
index = len(X[:,0])-1
#plt.annotate("$u=0|_{\\partial\\bar{\\Omega}^e}$", (X[index,int(p/2+1)], Y[index,int(p/2+1)]+0.2), color = "black")
plt.text(X[index,int(p/2+1)]-0.6, Y[index,int(p/2+1)]+0.2,"$u=0|_{\\partial\\bar{\\Omega}_e}$", color = "blue", fontsize=24)
plt.arrow(1.2-0.6, 1.9, 0.3, -0.1, color = "blue", head_width=0.1)
color = "blue"
plt.text(-0.15,-0.15,"$\\bar{\\Omega}_e$", color = color, size=24)
plt.axis("equal")
plt.axis("off")
plt.tight_layout()
plt.savefig(f"../figs/overlapping-schwarz-diagram-p={p}.png", dpi=300)
#plt.show()