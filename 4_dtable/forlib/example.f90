subroutine distance_table(pos, lbox, natom, ndim, dtable)
  integer, intent(in) :: natom, ndim
  real*8, intent(in) :: pos(natom, ndim), lbox
  real*8, intent(out) :: dtable(natom, natom)
  integer i, j
  real*8 drij(ndim)
  do i=1,natom
    do j=i+1,natom
      drij = pos(i, :) - pos(j, :)
      drij = drij - lbox*nint(drij/lbox)
      dtable(i, j) = norm2(drij)
      !write (*, '(4f8.4)') drij, dtable(i, j)
    end do
    !stop
  end do
end subroutine
