#!/usr/bin/env python
import os
import numpy as np
import matplotlib.pyplot as plt

from ase import Atoms
from ase.build import make_supercell

def init_pos(natom):
  rho = 2.2e22*1e6/1e30 # atoms/A^3
  lbox = (natom/rho)**(1./3)
  nxf = (natom/4.)**(1./3)
  nx = int(round(nxf))
  if not np.isclose(nx, nxf):
    raise RuntimeError('natom=%d nxf=%3.2f!=%d' % (natom, nxf, nx))
  # create FCC crystal
  alat = lbox/nx
  axes0 = alat/2*(np.ones(3)-np.eye(3))
  tmat = nx*( np.ones(3)-2*np.eye(3) )
  s0 = Atoms('H', cell=axes0, positions=[[0,0,0]], pbc=[1,1,1])
  s1 = make_supercell(s0, tmat)
  pos = s1.get_positions()
  axes = s1.get_cell()
  # check density
  rho1 = natom/s1.get_volume()
  if not np.isclose(rho, rho1):
    raise RuntimeError('supercell density is wrong')
  return axes, pos

def disp_in_box(pos, lbox):
  nint = np.round(pos/lbox)
  return pos-nint*lbox

def get_dtable_vec(pos, lbox):
  dptable = disp_in_box(pos[:, np.newaxis] - pos[np.newaxis, :], lbox)
  dtable = np.linalg.norm(dptable, axis=-1)
  return dtable

def get_dtable(pos, lbox):
  natom = len(pos)
  dtable = np.zeros([natom, natom])
  for i in range(natom):
    for j in range(natom):
      dtable[i, j] = np.linalg.norm(disp_in_box(pos[i]-pos[j], lbox))
  return dtable

def check_correct(methods, func_map, pos, lbox):
  # get ase distance table (reference distance table)
  natom = len(pos)
  axes = lbox*np.eye(3)
  s1 = Atoms('H%d' % natom, cell=axes, positions=pos, pbc=[1,1,1])
  #print [cmd for cmd in dir(s1) if 'dist' in cmd]
  #assert 0

  # check only unique pair distances
  idx = np.triu_indices(natom, k=1)

  adt = s1.get_all_distances(mic=True)
  for method in methods:
    func = func_map[method]
    mydt = func(pos, lbox)
    print('%s correct:' % method, np.allclose(mydt[idx], adt[idx]))

  ## check PBC distance limit
  #print 3**0.5/2*lbox
  #print ase_dtable[idx].max()
  #print fdt[idx].max()
  #fig, axl = plt.subplots(1, 2)
  #axl[0].matshow(dtable)
  #axl[1].matshow(fdt)
  #plt.show()

if __name__ == '__main__':
  natom = 32
  natom = 108
  natom = 8**3*4
  axes, pos = init_pos(natom)
  ## view crystal
  #from qharv.inspect import crystal, volumetric
  #fig, ax = volumetric.figax3d()
  #crystal.draw_cell(ax, axes)
  #crystal.draw_atoms(ax, pos)
  #plt.show()

  import forlib.example as fex
  import forlib.example as cex
  func_map = {
    'python': get_dtable_vec,
    'fortran': fex.distance_table,
    'cpp': cex.distance_table
  }
  lbox = axes[0, 0]
  #methods = ['fortran', 'cpp', 'python']
  methods = ['cpp', 'fortran', 'python']
  check_correct(methods, func_map, pos, lbox)

  nrun = 3  # number of times to repeat timing measurement
  import sys
  sys.path.insert(0, '../2_simd')
  from pyadd import time_func
  times = {}
  for method in methods:
    func = func_map[method]
    time = time_func(nrun)(func)(pos, lbox)
    times[method] = time
  pyt = times['python']
  for method, time in times.items():
    print('python/%s' % method, pyt/time)
# end __main__
