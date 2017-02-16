********************************
 Getting started with |project|
********************************

The following tutorial constitutes a suitable starting point to get to
know how to use Bob's packages and to learn its fundamental concepts.

They all rely on the lab-like environment which is `Python`_. Using Bob
within a Python environment is convenient because:

-  you can easily glue together all of the components of an experiment
   within a single Python script (which does not require to be
   compiled),

-  scripts may easily rely on other Python tools like `SciPy`_ as well
   as Bob, and

-  Python bindings are used to transparently run the underlying
   efficient C++ compiled code for the key features of the library.


Installation
============

These tutorials rely on several package of Bob. Please make sure that you have
read the :doc:`install` section to be able to follow the examples.


Multi-dimensional Arrays
========================

The fundamental data structure of Bob is a multi-dimensional array. In signal-
processing and machine learning, arrays are a suitable representation for many
different types of digital signals such as images, audio data and extracted
features. Python is the working environment selected for this library and so
when using Python we have relied on the existing `NumPy`_ multi-dimensional
arrays :any:`numpy.ndarray`. This provides with greater flexibility within the
Python environment.

At the C++ level, the `Blitz++`_ library is used to handle arrays. Although we
initially bound Blitz++ Arrays in Python, we quickly realized that it might be
more clever to use the existing NumPy ndarrays from Python, as they can
directly be processed by numerous existing Python libraries such as `NumPy`_
and `SciPy`_.

This means that Bob's multi-dimensional arrays are represented in Python by
NumPy ndarrays. This also implies that there are internal conversion routines
to convert NumPy ndarrays from/to Blitz++. As they are done implicitly, the
user has no need to care about this aspect and should just use NumPy ndarrays
everywhere.

For an introduction and tutorials about NumPy ndarrays, just visit the `NumPy
Reference`_ website. For a short tutorial on the bindings from NumPy ndarrays
to Blitz++, you can read the :doc:`temp/bob.blitz/doc/py_api` of our
:ref:`bob.blitz` package.

..note::

   Many functions in Bob will return multi-dimensional arrays type
   ``bob.blitz.array``, which are **wrapped** by as a ``numpy.ndarray``. While
   you can use these arrays in all contexts inside Bob, NumPy and Scipy, some
   functionality of the ``numpy.ndarray`` are **not available**. In
   particular, resizing the arrays with ``numpy.ndarray.resize`` will raise an
   exception. In such cases, please make a **copy** of the array using
   ``numpy.ndarray.copy()``.

Digital signals as multi-dimensional arrays
===========================================

For Bob, we have decided to represent digital signals directly as
``numpy.ndarray`` rather than having dedicated classes for each type of
signals. This implies that some convention has been defined.

Vectors and matrices
--------------------

A vector is represented as a 1D NumPy array, whereas a matrix is
represented by a 2D array whose first dimension corresponds to the rows,
and second dimension to the columns.

.. code:: python

    >>> import numpy
    >>> A = numpy.array([[1, 2, 3], [4, 5, 6]], dtype='uint8') # A is a matrix 2x3
    >>> print(A)
    [[1 2 3]
     [4 5 6]]
    >>> b = numpy.array([1, 2, 3], dtype='uint8') # b is a vector of length 3
    >>> print(b)
    [1 2 3]

Images
------

**Grayscale** images are represented as 2D arrays, the first dimension
being the height (number of rows) and the second dimension being the
width (number of columns). For instance:

.. code:: python

    >>> img = numpy.ndarray((480,640), dtype='uint8')

``img`` which is a 2D array can be seen as a gray-scale image of
dimension 640 (width) by 480 (height). In addition, ``img`` can be seen
as a matrix with 480 rows and 640 columns. This is the reason why we
have decided that for images, the first dimension is the height and the
second one the width, such that it matches the matrix convention as
well.

**Color** images are represented as 3D arrays, the first dimension being
the number of color planes, the second dimension the height and the
third the width. As an image is an array, this is the responsibility of
the user to know in which color space the content is stored.
:ref:`bob.ip.color` provides functions to perform color-space conversion:

.. code:: python

    >>> import bob.ip.color
    >>> colored = numpy.ndarray((3,480,640), dtype='uint8')
    >>> gray = bob.ip.color.rgb_to_gray(colored)
    >>> print (gray.shape)
    [480 640]

Videos
------

A video can be seen as a sequence of images over time. By convention,
the first dimension is for the frame indices (time index), whereas the
remaining ones are related to the corresponding image frame. More
information about loading and handling video sources can be found in the
:doc:`temp/bob.io.video/doc/guide` of :ref:`bob.io.video`.

Audio signals
-------------

Audio signals in Bob are represented as 2D arrays: the first dimension being
the number of channels and the second dimension corresponding to the time
index. For instance:

.. code:: python
   
   >>> import bob.io.audio
   >>> audio = bob.io.audio.reader("test.wav")
   >>> audio.rate
   16000.0
   >>> signal = audio.load()
   >>> signal.shape
   (1, 268197)

:ref:`bob.io.audio` supports loading a variety of audio files. Please refer to
its documentation for more information.

.. warning::

   You can also use ``scipy.io.wavfile`` to load wav files in Python but the
   returned data is slightly different compared to ``bob.io.audio``. In Scipy
   the first dimension corresponds to the time index rather than the audio
   channel. Also in Scipy, the loaded signal maybe an ``int8`` or ``int16`` or
   something else depending on the audio but ``bob.io.audio`` always returns
   the data as ``float`` arrays. We recommend using ``bob.io.audio`` since it
   supports more audio formats and it is more consistent with the rest of Bob
   packages.


Input and output
================

The default way to read and write data from and to files with Bob is
using the binary `HDF5`_ format which has several tools to inspect those
files. Bob's support for HDF5 files is given through the :ref:`bob.io.base`
package, which provides a :doc:`temp/bob.io.base/doc/guide` as well.

On the other hand, loading and writing of different kinds of data is provided
in other `Packages`_ of Bob using a plug-in strategy. Many image types can be
read using :ref:`bob.io.image`, and many video codecs are supported through
the :ref:`bob.io.video` plug-in. Also, a comprehensive support for
MatLab files is given through the :ref:`bob.io.matlab` interface.

Additionally, :ref:`bob.io.base` provides two generic functions
:any:`bob.io.base.load` and :any:`bob.io.base.save` to load and save data of
various types, based on the filename extension. For example, to load a
.jpg image, simply call:

.. code:: python

    >>> import bob.io.base
    >>> import bob.io.image #under the hood: loads Bob plug-in for image files
    >>> img = bob.io.base.load("myimg.jpg")

Image processing
================

The image processing module is split into several packages, where most
functionality is contained in the :ref:`bob.ip.base` module. For an
introduction in simple affine image transformations such as scaling and
rotating images, as well as for more complex operations like Gaussian or Sobel
filtering, please refer to the :doc:`temp/bob.ip.base/doc/guide`. Also, simple
texture features like LBP's can be extracted using :any:`bob.ip.base.LBP`.

Gabor wavelet functionality has made it into its own package
:ref:`bob.ip.gabor`. A tutorial on how to perform a Gabor wavelet transform,
extract Gabor jets in grid graphs and compare Gabor jets, please read the
:doc:`temp/bob.ip.gabor/doc/guide`.

Machine learning
================

*Machines* and *Trainers* are one of the core components of Bob.
Machines represent statistical models or other functions defined by
parameters that can be trained or set by using trainers. Two examples of
machines are multi-layer perceptrons (MLPs) and Gaussian mixture models
(GMMs).

The operation you normally expect from a machine is to be able to feed a
feature vector and extract the machine response or output for that input
vector. It works, in many ways, similarly to signal processing blocks.
Different types of machines will give you a different type of output.
Here, we examine a few of the machines and trainers available in Bob.

-  For a start, you should read the :doc:`temp/bob.learn.linear/doc/guide`,
   which is able to perform subspace projections like PCA and LDA.

-  :doc:`temp/bob.learn.mlp/doc/guide` are provided within the
   :any:`bob.learn.mlp` package.

-  :doc:`temp/bob.learn.libsvm/doc/guide` are provided though a bridge to
   `LibSVM`_.

-  Generating strong classifiers by :doc:`temp/bob.learn.boosting/doc/guide`
   weak classifiers is provided by :ref:`bob.learn.boosting`.

-  K-Means clustering and Gaussian Mixture Modeling, as well as Joint
   Factor Analysis, Inter-Session Variability and Total Variability
   modeling and, finally, Probabilistic Linear Discriminant Analysis is
   implemented in :ref:`bob.learn.em`. A nice introduction into these
   techniques can be found in :doc:`temp/bob.learn.em/doc/guide`.

Database interfaces
===================

Bob provides an API to easily query and interface with well known
databases. A database contains information about the organization of the
files, functions to query information such as the data which might be
used for training a model, but it usually does **not** contain the data
itself (except for some toy examples). Most of the databases are stored
in an `SQLite`_ file, whereas the smallest ones can be stored as
filelists.

Bob includes a (growing) list of supported database interfaces. There are some
small toy databases like :doc:`temp/bob.db.iris/doc/guide` and the
:doc:`temp/bob.db.mnist/doc/guide` database can be used to train and evaluate
classification experiments. For the former, a detailed example on how to use
Bob's machine learning techniques to classify the Iris flowers is given in
:doc:`temp/bob.db.iris/doc/example`.

However, most of the databases contain face images, speech data or
videos that are used for biometric recognition and anti-spoofing. A
complete (and growing) list of database packages can be found in our
`Packages`_.

Several databases that can be used for biometric recognition share a common
interface, which is defined in the :any:`bob.bio.base.database.BioDatabase`
package. Generic functionality that is available in all verification database
packages is defined in the `Implementation Details
<https://pythonhosted.org/bob.bio.base/implementation.html>`_, while a list of
databases that implement this interface can be found in  `bob.bio.face
<https://pypi.python.org/pypi/bob.bio.face>`_, `bob.bio.video
<https://pypi.python.org/pypi/bob.bio.video>`_, `bob.bio.spear
<https://pypi.python.org/pypi/bob.bio.spear>`_, or any other biometric package
depending on the modality of the database. Finally, how to use these databases
to build an complete biometric recognition experiment is described in detail
in the **outdated** `bob.example.faceverify
<https://pythonhosted.org/bob.example.faceverify/index.html>`_ example package.

Performance evaluation
======================

Methods in the :ref:`bob.measure` module can be used evaluate error for
multi-class or binary classification problems. Several evaluation
techniques such as Root Mean Squared Error, F-score, Recognition Rates,
False Acceptance and False Rejection Rates, and Equal Error Rates can be
computed, but also functionality for plotting CMC, ROC, DET and EPC
curves are described in more detail in the :doc:`temp/bob.measure/doc/guide`.


.. include:: links.rst
