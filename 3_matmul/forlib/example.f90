subroutine mmul(mat, vec, vecout, m, n)
  integer, intent(in) :: m, n
  real*8, intent(in) :: mat(m, n), vec(n)
  real*8, intent(out) :: vecout(n)
  vecout = matmul(mat, vec)
end subroutine
