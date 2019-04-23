/**
 * @file machine/python/main.cc
 * @date Tue Jan 18 17:07:26 2011 +0100
 * @author André Anjos <andre.anjos@idiap.ch>
 * @author Laurent El Shafey <Laurent.El-Shafey@idiap.ch>
 *
 * @brief Combines all modules to make up the complete bindings
 *
 * Copyright (C) 2011-2013 Idiap Research Institute, Martigny, Switzerland
 * 
 * This program is free software: you can redistribute it and/or modify
 * it under the terms of the GNU General Public License as published by
 * the Free Software Foundation, version 3 of the License.
 * 
 * This program is distributed in the hope that it will be useful,
 * but WITHOUT ANY WARRANTY; without even the implied warranty of
 * MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
 * GNU General Public License for more details.
 * 
 * You should have received a copy of the GNU General Public License
 * along with this program.  If not, see <http://www.gnu.org/licenses/>.
 */

#include <bob/config.h>
#include <bob/python/ndarray.h>

void bind_machine_base();
void bind_machine_bic();
void bind_machine_gabor();
void bind_machine_gaussian();
void bind_machine_gmm();
void bind_machine_kmeans();
void bind_machine_activation();
void bind_machine_linear();
void bind_machine_mlp();
void bind_machine_linear_scoring();
void bind_machine_ztnorm();
void bind_machine_jfa();
void bind_machine_ivector();
void bind_machine_plda();
void bind_machine_roll();
void bind_machine_wiener();
void bind_machine_version();

#if WITH_LIBSVM
void bind_machine_svm();
#endif

BOOST_PYTHON_MODULE(_machine) {
  boost::python::docstring_options docopt(true, true, false);
  bob::python::setup_python("bob classes and sub-classes for machine access");

  bind_machine_base();
  bind_machine_bic();
  bind_machine_gabor();
  bind_machine_gaussian();
  bind_machine_gmm();
  bind_machine_kmeans();
  bind_machine_activation();
  bind_machine_linear();
  bind_machine_mlp();
  bind_machine_linear_scoring();
  bind_machine_ztnorm();
  bind_machine_jfa();
  bind_machine_ivector();
  bind_machine_plda();
  bind_machine_roll();
  bind_machine_wiener();
  bind_machine_version();

#if WITH_LIBSVM
  bind_machine_svm();
#endif
}
