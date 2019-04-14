#!/usr/bin/env python
import numpy as np
from timeit import default_timer as timer

from forlib import example as fex
from cpplib import example as cex

def matmul(mat, vec):
  return np.dot(mat, vec)

def check_correct():
  n = 100
  seed = 1836137
  np.random.seed(seed)
  mat = np.random.rand(n, n)
  vec = np.random.randn(n)
  fret = fex.mmul(mat, vec)
  cret = cex.mmul(mat, vec)
  pyret = matmul(mat, vec)
  print("fortran=python", np.allclose(fret, pyret))
  print("cpp=python", np.allclose(cret, pyret))

import sys
sys.path.insert(0, '../2_simd')
from pyadd import time_func

if __name__ == '__main__':
  check_correct()
  # time implementations
  nrun = 100
  n = 1024
  seed = 1836137
  np.random.seed(seed)
  mat = np.random.rand(n, n)
  vec = np.random.randn(n)
  func_map = {
    'numpy': np.dot,
    'fortran': fex.mmul,
    'cpp': cex.mmul
  }
  # Q/ Does order matter? A/ Yes!
  methods = ['fortran', 'cpp', 'numpy']
  pyfunc = func_map['numpy']
  pytime = time_func(nrun)(pyfunc)(mat, vec)
  for method in methods:
    func = func_map[method]
    time = time_func(nrun)(func)(mat, vec)
    print('python/'+method, pytime/time)
# end __main__
