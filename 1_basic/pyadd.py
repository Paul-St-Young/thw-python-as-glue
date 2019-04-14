#!/usr/bin/env python
import os
import numpy as np

from forlib import example as fex
from cpplib import example as cex

def add(i, j):
  return i+j

if __name__ == '__main__':
  i = 1
  j = 1
  print(fex.add(i, j))
  print(cex.add(i, j))
  print(    add(i, j))
# end __main__
