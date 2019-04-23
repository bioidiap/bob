.. vim: set fileencoding=utf-8 :
.. Andre Anjos <andre.anjos@idiap.ch>
.. Wed Jan 11 14:43:35 2012 +0100
..
.. Copyright (C) 2011-2013 Idiap Research Institute, Martigny, Switzerland
..
.. This program is free software: you can redistribute it and/or modify
.. it under the terms of the GNU General Public License as published by
.. the Free Software Foundation, version 3 of the License.
..
.. This program is distributed in the hope that it will be useful,
.. but WITHOUT ANY WARRANTY; without even the implied warranty of
.. MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
.. GNU General Public License for more details.
..
.. You should have received a copy of the GNU General Public License
.. along with this program.  If not, see <http://www.gnu.org/licenses/>.

.. _section-compilation:

==============================
 Compiling |project| Yourself
==============================

.. ****************************** BIG WARNING ********************************
.. If you update this document, please make sure to also update the INSTALL.md
.. file at the root of bob. It contains a simplified version of these
.. instructions. Thanks.
.. ****************************** BIG WARNING ********************************

Grab a release tarball and change into its directory:

.. code-block:: sh

  $ wget https://gitlab.idiap.ch/bob/bob/-/archive/v1.2.3/bob-v1.2.3.tar.bz2
  $ tar xfj bob-1.2.3.tar.bz2
  $ cd bob-v1.2.3


.. _section-checkout:

Cloning |project|
-----------------

If you decide to checkout the latest sources from our git repository, do the
following at your shell prompt:


.. code-block:: sh

   $ git clone --branch=1.2 https://gitlab.idiap.ch/bob/bob
   $ cd bob


Compiling the code
------------------

Follow build instructions at ``conda/meta.yaml``, it is our reference build
system.  You may optionally build the release using ``conda-build``, which will
also test it:

.. code-block:: sh

   $ conda-build --python=2.7 conda


Influential CMake Variables
===========================

Some variables that may be handy:

 * `CMAKE_BUILD_TYPE`: options `Release` or `Debug` are supported
 * `CMAKE_PREFIX_PATH`: places to look-up for external dependencies
 * `WITH_PYTHON`: if you would like to force a specific version of python, you
   can define it with this variable
 * `WITH_MKL`: tries to compile against the Intel MKL instead of the standard
   BLAS/LAPACK installation. You should provide the path to the MKL such as
   `-DWITH_MKL=/PATH/TO/MKL/LIB`.
 * `WITH_LIBSVM`: makes LibSVM detection obligatory.
 * `WITH_VLFEAT`: makes VLFeat detection obligatory.
 * `WITH_MATIO`: makes MatIO detection obligatory.
 * `WITH_FFMPEG`: makes FFmpeg detection obligatory.
 * `WITH_PERFTOOLS`: makes Google Perftools detection obligatory.


Troubleshooting compilation
===========================

Most of the problems concerning compilation come from not satisfying correctly
the :ref:`section-dependencies`. Start by double-checking every dependency or
base OS and check everything is as expected. If after exhausting all of these
possibilities you are still unable to compile |project|, please
`submit a new bug report`_ in our tracking system. At this time make sure to
specify your OS version and the versions of the external dependencies so we can
try to reproduce the failure.


Eager for more functionality?
=============================

|project| functionality can be augmented by the use of `Satellite Packages`_.
Please check that page for more material before start developing your own tools
based on |project|.

.. include:: links.rst
