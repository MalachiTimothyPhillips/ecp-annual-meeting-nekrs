import meshio
import numpy as np
import matplotlib.pyplot as plt
import mpl_toolkits.mplot3d as a3

xyz = np.array([
    [-1,-1,-1], # 0
    [ 1,-1,-1], # 1
    [ 1, 1,-1], # 2
    [-1, 1,-1], # 3
    [-1,-1, 1], # 4
    [ 1,-1, 1], # 5
    [ 1, 1, 1], # 6
    [-1, 1, 1]  # 7
    ], dtype=np.float64) 

def distance(point1, point2):
    return np.linalg.norm(point1 - point2)
def triangles_from_point(point_index):
    # gather connected points
    connectedPoints = [point_index]
    for point in range(0,8):
        if np.isclose(distance(xyz[point], xyz[point_index]), 2.0):
            connectedPoints.append(point)
    print(connectedPoints)
    assert len(connectedPoints) == 4
    return np.array([
        [connectedPoints[0], connectedPoints[1], connectedPoints[2]],
        [connectedPoints[0], connectedPoints[2], connectedPoints[3]],
        [connectedPoints[1], connectedPoints[2], connectedPoints[3]],
    ], dtype=np.int64)

#tri = np.array([
# [0,1,4],
# [0,3,4],
# [1,3,4],
# ],dtype=np.int64)
tri = triangles_from_point(0)


fig = plt.figure(figsize=plt.figaspect(0.5)) # 2 times wider than it is tall

def draw_tet(fig, tetNum):
  tri = triangles_from_point(tetNum)
  axes = fig.add_subplot(2, 4, tetNum + 1, projection='3d')
  vts = xyz[tri, :]
  tri = a3.art3d.Poly3DCollection(vts)
  tri.set_alpha(0.2)
  tri.set_color('blue')
  axes.add_collection3d(tri)
  axes.plot(xyz[:,0], xyz[:,1], xyz[:,2], 'ko')
  
  # bottom faceedges
  axes.plot([-1,1],[-1,-1],[-1,-1], color="black")
  axes.plot([1,1],[-1,1],[-1,-1], color="black")
  axes.plot([1,-1],[1,1],[-1,-1], color="black")
  axes.plot([-1,-1],[1,-1],[-1,-1], color="black")
  
  # top face edges
  axes.plot([-1,1],[-1,-1],[1,1], color="black")
  axes.plot([1,1],[-1,1],[1,1], color="black")
  axes.plot([1,-1],[1,1],[1,1], color="black")
  axes.plot([-1,-1],[1,-1],[1,1], color="black")
  
  axes.plot([1,1],[-1,-1],[-1,1], color="black")
  axes.plot([-1,-1],[-1,-1],[-1,1], color="black")
  axes.plot([1,1],[1,1],[-1,1], color="black")
  axes.plot([-1,-1],[1,1],[-1,1], color="black")
  
  axes.set_axis_off()
  axes.set_aspect('auto')

for i in range(0,8):
  draw_tet(fig, i)

#plt.savefig("../figs/one-tet-per-vertex.png", dpi=300)
plt.tight_layout()
plt.savefig("../figs/one-tet-per-vertex.png", dpi=300)
#plt.show()