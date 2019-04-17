#include <pybind11/pybind11.h>
#include <pybind11/eigen.h>
#include <pybind11/operators.h>
#include <Eigen/Dense>
#include <iostream>
#include <sstream>

namespace py=pybind11;

class MatrixS
{ // Matrix Superior >:$
public:
  typedef Eigen::MatrixXd Matrix;
  MatrixS(int m_in, int n_in) : m(m_in), n(n_in)
  {
    mat = Matrix::Zero(m, n);
  }
  int m, n;
  std::string to_string()
  {
    std::stringstream ss;
    ss << mat;
    return ss.str();
  }
  void randomize()
  {
    mat = Matrix::Random(m, n);
  }
  double getitem(int i, int j)
  const {
    return mat(i, j);
  }
  MatrixS operator+(const MatrixS &m) const {
    MatrixS sum(m.m, m.n);
    sum.mat = m.mat+mat;
    return sum;
  }
  MatrixS operator*(double v) const {
    MatrixS matv(m, n);
    matv.mat = mat*v;
    return matv;
  }
  friend MatrixS operator*(double v, const MatrixS &m)
  {
    return m*v;
  }
  Matrix mat;
};

PYBIND11_MODULE(example, m)
{
  py::class_<MatrixS>(m, "MatrixS")
    .def(py::init<int, int>())
    .def_readwrite("m", &MatrixS::m)
    .def_readonly("n", &MatrixS::n)
    .def_readonly("mat", &MatrixS::mat)
    .def("randomize", &MatrixS::randomize)
    .def("getitem", &MatrixS::getitem)
    //.def("__getitem__", &MatrixS::getitem)//, py::is_operator())
    .def("__repr__", &MatrixS::to_string)
    .def(py::self + py::self)
    .def(double() * py::self)
    .def(py::self * double())
  ;
}
