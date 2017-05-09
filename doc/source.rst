.. _bob.source:

=======================
 Compiling from Source
=======================

Following, you will find the software dependencies required for Bob's
compilation and instructions on how to compile |project|.


Dependencies
------------

This section describes software dependencies required for Bob's compilation
**and** runtime dependencies.

.. note::

   We keep here a comprehensive list of **all** packages you may need to
   compile most of the available Bob packages. You may not need all this
   software for special deployments. You should choose whatever suits you best.
   If you have problems or would like to report a success story, please use our
   `mailing list`_ for discussions.

+----------------+--------+-----------------------------+-------------------------+
| Library        | Min.   | License                     | Notes                   |
|                | Versio |                             |                         |
|                | n      |                             |                         |
+================+========+=============================+=========================+
| Std. C/C++     | any    | Depends on the compiler     | Required by all         |
| Libraries      |        |                             | packages with C/C++     |
|                |        |                             | bindings                |
+----------------+--------+-----------------------------+-------------------------+
| `Blitz++`_     | 0.10   | `Artistic-2.0`_ or LGPLv3+  | Required by all         |
|                |        | or GPLv3+                   | packages with C/C++     |
|                |        |                             | bindings                |
+----------------+--------+-----------------------------+-------------------------+
| `Lapack`_      | any    | BSD-style                   | Required by             |
|                |        |                             | ``bob.math``            |
+----------------+--------+-----------------------------+-------------------------+
| `Python`_      | 2.5    | `Python-2.0`_               | Required by all         |
|                |        |                             | packages                |
+----------------+--------+-----------------------------+-------------------------+
| `Boost`_       | 1.34   | `BSL-1.0`_                  | Required by all         |
|                |        |                             | packages with C/C++     |
|                |        |                             | bindings                |
+----------------+--------+-----------------------------+-------------------------+
| `HDF5`_        | 1.8.4  | `HDF5 License`_ (BSD-like,  | Required by all I/O     |
|                |        | 5 clauses)                  | operations (direct or   |
|                |        |                             | indirect dependencies   |
|                |        |                             | to ``bob.io.base``)     |
+----------------+--------+-----------------------------+-------------------------+
| `libpng`_      | 1.2.42 | `libpng license`_           | Required by all         |
|                | ?      |                             | packages that do image  |
|                |        |                             | I/O and manipulation    |
|                |        |                             | (depend directly or     |
|                |        |                             | indirectly on           |
|                |        |                             | ``bob.io.image``)       |
+----------------+--------+-----------------------------+-------------------------+
| `libtiff`_     | 3.9.2  | BSD-style                   | Required by all         |
|                |        |                             | packages that do image  |
|                |        |                             | I/O and manipulation    |
|                |        |                             | (depend directly or     |
|                |        |                             | indirectly on           |
|                |        |                             | ``bob.io.image``)       |
+----------------+--------+-----------------------------+-------------------------+
| `giflib`_      | 4.1.6- | `MIT`_                      | Required by all         |
|                | 9      |                             | packages that do image  |
|                |        |                             | I/O and manipulation    |
|                |        |                             | (depend directly or     |
|                |        |                             | indirectly on           |
|                |        |                             | ``bob.io.image``)       |
+----------------+--------+-----------------------------+-------------------------+
| `libjpeg`_     | 6.2?   | `GPL-2.0`_ or later (also   | Required by all         |
|                |        | commercial)                 | packages that do image  |
|                |        |                             | I/O and manipulation    |
|                |        |                             | (depend directly or     |
|                |        |                             | indirectly on           |
|                |        |                             | ``bob.io.image``)       |
+----------------+--------+-----------------------------+-------------------------+
| `FFMpeg`_ or   | 0.5    | `LGPL-2.1`_ or later, or    | Required by all         |
| `libAV`_       | (ffmpe | `GPL-2.0`_ or later         | packages that do video  |
|                | g)     |                             | I/O and manipulation    |
|                | or 0.8 |                             | (depend directly or     |
|                | (libav |                             | indirectly on           |
|                | )      |                             | ``bob.io.video``)       |
+----------------+--------+-----------------------------+-------------------------+
| `MatIO`_       | 1.3.3? | `BSD-2-Clause`_             | Required by all         |
|                |        |                             | packages that do Matlab |
|                |        |                             | I/O and manipulation    |
|                |        |                             | (depend directly or     |
|                |        |                             | indirectly on           |
|                |        |                             | ``bob.io.matlab``)      |
+----------------+--------+-----------------------------+-------------------------+
| `VLFeat`_      | 0.9.14 | `BSD-2-Clause`_             | Required by             |
|                |        |                             | ``bob.ip.base`` and all |
|                |        |                             | dependents              |
+----------------+--------+-----------------------------+-------------------------+
| `LIBSVM`_      | 2.89+  | `BSD-3-Clause`_             | Required by             |
|                |        |                             | ``bob.learn.libsvm``    |
|                |        |                             | and all dependents      |
+----------------+--------+-----------------------------+-------------------------+
| `CMake`_       | 2.8    | `BSD-3-Clause`_             | Required by all         |
|                |        |                             | packages with C/C++     |
|                |        |                             | bindings. **Use at      |
|                |        |                             | least CMake 2.8.12 on   |
|                |        |                             | Mac OS X**.             |
+----------------+--------+-----------------------------+-------------------------+
| `Dvipng`_      | 1.12?  | `GPL-3.0`_                  | Required by all         |
|                |        |                             | packages (documentation |
|                |        |                             | generation)             |
+----------------+--------+-----------------------------+-------------------------+
| `LaTeX`_       | any    | ?                           | Required by all         |
|                |        |                             | packages (documentation |
|                |        |                             | generation). You will   |
|                |        |                             | also need to install    |
|                |        |                             | the Extra-Latex fonts   |
|                |        |                             | package.                |
+----------------+--------+-----------------------------+-------------------------+
| `pkg-config`_  | any    | `GPL-2.0`_                  | Required to find        |
|                |        |                             | dependencies while      |
|                |        |                             | building bob packages.  |
+----------------+--------+-----------------------------+-------------------------+

Here is a list of Python packages software that is also used by Bob. It is not
required that such software be installed at the moment you compile Bob. It will
be fetched automatically from PyPI otherwise.

+---------------+-----+-----------------+------------------------------------------+
| Library       | Min | License         | Notes                                    |
|               | .   |                 |                                          |
|               | Ver |                 |                                          |
|               | sio |                 |                                          |
|               | n   |                 |                                          |
+===============+=====+=================+==========================================+
| `NumPy`_      | 1.3 | `BSD-3-Clause`_ | Required by all packages. If not         |
|               |     |                 | installed natively on your machine, may  |
|               |     |                 | not correctly use *optimized* LaPACK or  |
|               |     |                 | BLAS implementations. Consequently,      |
|               |     |                 | ``bob.math`` will *not* either.          |
+---------------+-----+-----------------+------------------------------------------+
| `SciPy`_      | 0.7 | `BSD-3-Clause`_ | Required at least by ``bob.ap``,         |
|               | ?   |                 | ``bob.learn.boosting``,                  |
|               |     |                 | ``bob.ip.optflow.hornschunk`` and        |
|               |     |                 | ``facereclib``                           |
+---------------+-----+-----------------+------------------------------------------+
| `Matplotlib`_ | 0.9 | Based on        | Required for plotting                    |
|               | 9   | `Python-2.0`_   |                                          |
+---------------+-----+-----------------+------------------------------------------+
| `SQLAlchemy`_ | 0.5 | `MIT`_          | Required by all database accessor        |
|               |     |                 | packages (i.e., any that starts with     |
|               |     |                 | ``bob.db``)                              |
+---------------+-----+-----------------+------------------------------------------+
| `nose`_       | 1.0 | `LGPL-2.1`_     | For unit testing, on all packages        |
|               | ?   |                 |                                          |
+---------------+-----+-----------------+------------------------------------------+
| `Sphinx`_     | 0.6 | `BSD-2-Clause`_ | Required by all packages (documentation  |
|               |     |                 | generation)                              |
+---------------+-----+-----------------+------------------------------------------+
| `Setuptools`_ | 8.0 | `Python-2.0`_   | Required by all packages (Buildout and   |
|               |     |                 | package compilation)                     |
+---------------+-----+-----------------+------------------------------------------+
| `Pillow`_     | 1.7 | BSD-like        | Required by at least ``bob.io.video``    |
|               | .x? |                 | and ``bob.ip.optflow.liu``               |
+---------------+-----+-----------------+------------------------------------------+
| `IPython`_    | any | `BSD-3-Clause`_ | Recommended as interactive prompt        |
+---------------+-----+-----------------+------------------------------------------+


Installing |project| from source
--------------------------------

Once the dependecies are installed you can use pip to install |project| from
source.

It is possible to install |project| packages using ``pip``, globally or on your
private ``virtualenv``, if that is the way you like your Python work
environments. You will need to manually install all packages you need (directly
or indirectly), as ``pip``/``setuptools`` has presently no way to coherently
install Python packages that depend on each other *for building*, such as is
the case of many |project| packages.

For example, to install ``bob.io.image`` in a newly created virtual
environment, here is the sequence of commands to execute:

.. code:: sh

   $ pip install numpy
   $ pip install bob.extension
   $ pip install bob.blitz
   $ pip install bob.core
   $ pip install bob.io.base
   $ pip install bob.io.image

.. note::

   Each ``pip`` command must be executed separately, respecting the inter-
   package dependency.

   The following will **not** work as expected:

   .. code:: sh

      $ #Do not do this:
      $ pip install numpy bob.io.image

The dependency of |project| core packages can be summarized into 8 layers and
the following script can be used to install all core |project| packages using
``pip``:

.. code:: sh

   $ bash pip_install_bob.sh
   -------------------------
   #!/bin/bash
   set -e

   get_layer() {
   case $1 in
     1)
       packages=("bob.extension")
       ;;
     2)
       packages=("bob.blitz")
       ;;
     3)
       packages=("bob.core" "bob.ip.draw")
       ;;
     4)
       packages=("bob.io.base" "bob.sp" "bob.math")
       ;;
     5)
       packages=("bob.ap" "bob.measure" "bob.db.base" "bob.io.image" "bob.io.video" "bob.io.matlab" "bob.ip.base" "bob.ip.color" "bob.ip.gabor" "bob.learn.activation" "bob.learn.libsvm" "bob.learn.boosting")
       ;;
     6)
       packages=("bob.io.audio" "bob.learn.linear" "bob.learn.mlp" "bob.db.wine" "bob.db.mnist" "bob.db.atnt" "bob.ip.flandmark" "bob.ip.facedetect" "bob.ip.optflow.hornschunck" "bob.ip.optflow.liu")
       ;;
     7)
       packages=("bob.learn.em" "bob.db.iris")
       ;;
     8)
       packages=("bob")
       ;;
   esac
   }

   for layer in `seq 1 8`;
   do
     get_layer ${layer}
     for pkg in "${packages[@]}";
     do
       pip install $pkg
     done
   done


Hooking-in privately compiled externals
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

If you have placed external libraries outside default search paths, make sure
you set the environment variable ``BOB_PREFIX_PATH`` to point to the root of
the installation paths for those, **before** you run ``pip install...``:

.. code:: sh

    $ export BOB_PREFIX_PATH="/path/to/my-install:/path/to/my-other-install"
    $ pip install numpy
    $ pip install bob.io.image
    ...


Developer's Guide
-----------------

Please refer to :ref:`bob.extension` for a complete guide on how to develop
existing and new |project| packages.


.. include:: links.rst
