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

.. _section-installation:

======================
 Installing |project|
======================

We offer pre-compiled binary installations of Bob using `conda`_ for Linux
64-bit operating systems.  To install this version of Bob_, first install
miniconda_, then use the following command to create an environment for Bob_::

  $ conda create -n bobv1 -c https://www.idiap.ch/software/bob/conda bob=1


On the other hand, if the supported binary installation methods are not
appropriate or you would like to become a developer of |project|, you may try
to compile |project| yourself as explained at :doc:`Compilation`.

.. include:: links.rst
