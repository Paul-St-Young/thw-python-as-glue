#!/usr/bin/env python
import numpy as np
from forlib import example as fex
from cpplib import example as cex

def add(i, j):
  return i+j

def check_correct(vec1, vec2):
  pyvec = add(vec1, vec2)
  cvec = cex.add(vec1, vec2)
  fvec = fex.add(vec1, vec2)
  print('cpp=python', np.allclose(cvec, pyvec))
  print('fortran=python', np.allclose(fvec, pyvec))

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
  methods = ['fortran', 'cpp']
  check_correct(vec1, vec2)
  # compare C and Fortran time against Python
  pyfunc = func_map['python']
  nrun = 10000  # number of times to repeat timing measurement
  pytime = time_func(nrun)(pyfunc)(vec1, vec2)
  for method in methods+['python']:
    func = func_map[method]
    time = time_func(nrun)(func)(vec1, vec2)
    print('python/'+method, pytime/time)
  # cpp can handle matrices with no modification
  # fortran must be modified
# end __main__
