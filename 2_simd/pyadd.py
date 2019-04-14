#!/usr/bin/env python
import os
import numpy as np

from forlib import example as fex
from cpplib import example as cex

def add(i, j):
  return i+j

def check_correct(methods, func_map, vec1, vec2, pyvec):
  for method in methods:
    func = func_map[method]
    vec = func(vec1, vec2)
    print('%s correct:' % method, np.allclose(vec, pyvec))

def time_func(nrun):
  def wrap(func):
    def wrap1(*args, **kwargs):
      from timeit import default_timer as timer
      start = timer()
      for irun in range(nrun):
        func(*args, **kwargs)
      end = timer()
      return (end-start)/nrun
    return wrap1
  return wrap

if __name__ == '__main__':
  n = 100
  seed = 1836137
  np.random.seed(seed)
  vec1 = np.random.rand(n)
  vec2 = np.random.randn(n)
  func_map = {
    'python': add,
    'fortran': fex.add,
    'cpp': cex.add
  }
  # check against python answer
  pyfunc = func_map['python']
  pyvec = pyfunc(vec1, vec2)
  methods = ['fortran', 'cpp']
  check_correct(methods, func_map, vec1, vec2, pyvec)
  nrun = 10000
  pytime = time_func(nrun)(pyfunc)(vec1, vec2)
  for method in methods+['python']:
    func = func_map[method]
    time = time_func(nrun)(func)(vec1, vec2)
    print('python/'+method, pytime/time)
  # cpp can handle matrices with no modification
  # fortran must be modified
# end __main__
