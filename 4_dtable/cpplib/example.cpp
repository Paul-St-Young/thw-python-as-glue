#include <pybind11/pybind11.h>
#include <pybind11/eigen.h>
#include <Eigen/Dense>

namespace py=pybind11;
typedef Eigen::MatrixXd Matrix;
typedef Eigen::VectorXd Vector;

Eigen::Ref<Matrix> distance_table(
  Eigen::Ref<const Matrix>& pos, double lbox)
{
  const int natom = pos.rows();
  const int ndim = pos.cols();
  Matrix dtable = Matrix::Zero(natom, natom);
  Vector drij(ndim);
  for (int i=0;i<natom;i++)
  {
    for (int j=i; j<natom; j++)
    {
      drij = pos.row(i) - pos.row(j);
      for (int idim=0;idim<ndim;idim++)
      {
        drij(idim) -= lbox*std::round(drij(idim)/lbox);
      }
      dtable(i, j) = drij.norm();
    }
  }
  return dtable;
}

PYBIND11_MODULE(example, m)
{
  //m.def("distance_table", &distance_table, "PBC distances");
  m.def("distance_table", &distance_table, "PBC distances",
        py::return_value_policy::reference_internal);
}
