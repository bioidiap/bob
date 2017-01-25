.. vim: set fileencoding=utf-8 :
.. Andre Anjos <andre.anjos@idiap.ch>
.. Mon 17 Feb 2014 17:40:07 CET
.. Copyright (C) 2011-2014 Idiap Research Institute, Martigny, Switzerland

=======================
 Bob
=======================

Bob is a free signal-processing and machine learning toolbox originally
developed by the Biometrics group at `Idiap`_ Research Institute, Switzerland.

The toolbox is written in a mix of `Python`_ and `C++`_ and is designed to be
both efficient and reduce development time. It is composed of a reasonably
large number of `packages`_ that implement tools for image, audio & video
processing, machine learning and pattern recognition.

.. todolist::

.. toctree::
   :maxdepth: 2

   install


Bob is organized in several independent python packages. Below you can find the
list of all packages organized by category with their respectives documentation
and building status.


Basic Functionality
-------------------

.. toctree::
   :maxdepth: 2

   temp/bob.core/doc/index
   temp/bob.math/doc/index
   temp/bob.measure/doc/index

Data Input and Output
---------------------

.. toctree::
   :maxdepth: 2

   temp/bob.io.base/doc/index
   temp/bob.io.image/doc/index
   temp/bob.io.video/doc/index
   temp/bob.io.audio/doc/index
   temp/bob.io.matlab/doc/index

Signal, Audio, Image and Video Processing
-----------------------------------------

.. toctree::
   :maxdepth: 2

   temp/bob.sp/doc/index
   temp/bob.ap/doc/index
   temp/bob.ip.base/doc/index
   temp/bob.ip.color/doc/index
   temp/bob.ip.draw/doc/index
   temp/bob.ip.gabor/doc/index
   temp/bob.ip.facedetect/doc/index
   temp/bob.ip.optflow.liu/doc/index
   temp/bob.ip.optflow.hornschunck/doc/index
   temp/bob.ip.flandmark/doc/index

Machine Learning
----------------

.. toctree::
   :maxdepth: 2

   temp/bob.learn.activation/doc/index
   temp/bob.learn.linear/doc/index
   temp/bob.learn.mlp/doc/index
   temp/bob.learn.libsvm/doc/index
   temp/bob.learn.em/doc/index
   temp/bob.learn.boosting/doc/index
   

Database Modules
----------------

.. toctree::
   :maxdepth: 2

   temp/bob.db.base/doc/index
   temp/bob.db.mnist/doc/index
   temp/bob.db.wine/doc/index
   temp/bob.db.atnt/doc/index
   temp/bob.db.iris/doc/index
   


Modules for Developers
----------------------

.. toctree::
   :maxdepth: 2

   temp/bob.extension/doc/index
   temp/bob.blitz/doc/index
   
.. include:: links.rst
