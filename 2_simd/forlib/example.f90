subroutine add(vec1, vec2, vecout, n)
  integer, intent(in) :: n
  real*8, intent(in) :: vec1(n), vec2(n)
  real*8, intent(out) :: vecout(n)
  vecout = vec1+vec2
end subroutine
