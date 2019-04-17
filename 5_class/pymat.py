#!/usr/bin/env python
import numpy as np

if __name__ == '__main__':
  import cpplib.example as cex
  # initialize
  mat = cex.MatrixS(2, 3)
  print('initial size', mat.m, mat.n)
  # modify
  mat.m = 5
  print('modified size', mat.m, mat.n)
  # fill data
  mat.randomize()
  print('randomized:\n', mat)
  # get data
  print('entry (0, 1):', mat.getitem(0, 1))
  #print(mat[0, 1])
  # multiply
  mat *= 5
  print('mat*5', mat)
  # does math work?
  print('math works:', np.allclose(
    (6*mat).mat,
    (mat+mat*5).mat
  ))
# end __main__
