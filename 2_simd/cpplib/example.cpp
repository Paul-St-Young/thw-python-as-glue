#include <pybind11/pybind11.h>
#include <pybind11/numpy.h>

namespace py=pybind11;

double add(double i, double j)
{
  return i+j;
}

PYBIND11_MODULE(example, m)
{
  m.def("add", py::vectorize(add), "add two integers");
}
