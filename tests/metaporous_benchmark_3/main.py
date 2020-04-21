import sys
import numpy as np
import matplotlib.pyplot as plt


from pyPLANES.model.model import Model
from pyPLANES.classes.model_classes import ModelParameter
from pyPLANES.utils.utils_PW import Solver_PW
from pyPLANES.gmsh.write_geo_file import Gmsh as Gmsh

from pymls import from_yaml, Solver, Layer, backing

param = ModelParameter()
theta_d = 0
param.frequency = (10., 5010., 201)
param.name_project = "metaporous_benchmark_3"

param.theta_d = theta_d
L = 0.02
d = 0.02
a = 0.008
lcar = 0.01

param.order = 2
# param.plot = [True, True, True, False, False, False]
param.plot = [False]*6

p = param
G = Gmsh(p.name_project)

p_0 = G.new_point(0, 0, lcar)
p_1 = G.new_point(L, 0,lcar)
p_2 = G.new_point(L, d, lcar)
p_3 = G.new_point(0, d, lcar)
l_0 = G.new_line(p_0, p_1)
l_1 = G.new_line(p_1, p_2)
l_2 = G.new_line(p_2, p_3)
l_3 = G.new_line(p_3, p_0)
ll_0 = G.new_line_loop([l_0, l_1, l_2, l_3])
c_0 = G.new_circle(L/2, d/2, a, lcar)

matrice = G.new_surface([ll_0.tag, -c_0.tag])
inclusion = G.new_surface([c_0.tag])

G.new_physical(l_2, "condition=Rigid Wall")
G.new_physical([l_1, l_3], "condition=Periodicity")
G.new_physical(l_0, "condition=Incident_PW")
G.new_physical(matrice, "mat=pem_benchmark_1")
G.new_physical(inclusion, "mat=pem_benchmark_2")
G.new_physical([l_0, l_1, l_3, l_2], "model=FEM1D")
G.new_physical([matrice, inclusion], "model=FEM2D")
G.new_periodicity(l_1, l_3, (L, 0, 0))

option = "-2 "
G.run_gmsh(option)

model = Model(param)

model.resolution(param)


output = np.loadtxt(model.outfile_name)
plt.plot(output[:, 0], output[:, 1])
plt.savefig(param.name_project+".pdf")
