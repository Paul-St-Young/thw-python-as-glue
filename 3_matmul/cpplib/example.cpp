#include <pybind11/pybind11.h>
#include <pybind11/eigen.h>
#include <Eigen/Dense>

namespace py=pybind11;
typedef Eigen::MatrixXd Matrix;
typedef Eigen::VectorXd Vector;

Vector mmul(
  Eigen::Ref<const Matrix>& mat,
  Eigen::Ref<const Vector>& vec)
{
  return mat*vec;
}

PYBIND11_MODULE(example, m)
{
  m.def("mmul", &mmul, "multiply matrix vector");
}
