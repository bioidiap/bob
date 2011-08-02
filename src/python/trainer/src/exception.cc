/**
 * @author Francois Moulin <francois.moulin@idiap.ch>
 * @author Andre Anjos <andre.anjos@idiap.ch>
 * @date Thu 16 Jun 14:12:23 2011 CEST
 *
 * Binds some trainer exceptions to Python
 */

#include "core/python/exception.h"
#include "trainer/Exception.h"

using namespace Torch::core::python;

void bind_trainer_exception() {
  register_exception_translator<Torch::trainer::IncompatibleMachine>(PyExc_TypeError);
}
