.. _bob.install:

***************************
 Installation Instructions
***************************

We offer pre-compiled binary installations of Bob using `conda`_ for Linux and
MacOS 64-bit operating systems.

#.  Please install `conda`_ (miniconda is preferred) and get familiar with it.
#.  Make sure you have an up-to-date `conda`_ installation (conda 4.4 and above
    is needed) with the **correct configuration** by running the commands
    below:

    .. code:: sh

       $ conda update -n base conda
       $ conda config --set show_channel_urls True

#.  Create an environment for Bob:

    .. code:: sh

       $ conda create --name bob_py3 --override-channels \
         -c https://www.idiap.ch/software/bob/conda -c defaults \
         python=3 bob
       $ conda activate bob_py3
       $ conda config --env --add channels defaults
       $ conda config --env --add channels https://www.idiap.ch/software/bob/conda

#.  Install the Bob packages that you need in that environment:

    .. code:: sh

       $ conda install bob.io.image bob.bio.base ...

**Repeat the last two steps for every conda environment that you create for
Bob.**

For a comprehensive list of packages that are either part of |project| or use
|project|, please visit `packages`_.

.. warning::

    Be aware that if you use packages from our channel and other user/community
    channels (especially ``conda-forge``) in one environment, you may end up
    with a broken envrionment. We can only guarantee that the packages in our
    channel are compatible with the ``defaults`` channel.

.. note::

    Bob does not work on Windows and hence no conda packages are available for
    it. It will not work even if you install it from source. If you are an
    experienced user and manage to make Bob work on Windows, please let us know
    through our `mailing list`_.

.. note::

    Bob has been reported to run on arm processors (e.g. Raspberry Pi) but is
    not installable with conda. Please see :ref:`bob.source` for installations
    on how to install Bob from source.


Installing older versions of Bob
================================

Since Bob 4, you can easily select the Bob version that you want to install
using conda. For example:

.. code:: sh

    $ conda install bob=4.0.0 bob.io.base

will install the version of ``bob.io.base`` that was associated with the Bob
4.0.0 release.

Bob packages that were released before Bob 4 are not easily installable. Here,
we provide conda environment files (**Linux 64-bit only**) that will install
all Bob packages associated with an older release of Bob:

===========  ==============================================================
Bob Version  Environment Files
===========  ==============================================================
2.6.2        :download:`envs/v262py27.yaml`, :download:`envs/v262py35.yaml`
2.7.0        :download:`envs/v270py27.yaml`, :download:`envs/v270py35.yaml`
3.0.0        :download:`envs/v300py27.yaml`, :download:`envs/v300py36.yaml`
===========  ==============================================================

To install them, download one of the files above and run:

.. code:: sh

    $ conda env create --file v300py36.yaml


Details (Advanced Users)
========================

Since Bob 4, the ``bob`` conda package is just a meta package that pins all
packages to a specific version. Installing ``bob`` will not install anything;
it will just impose pinnings in your environment. Normally, installations of
Bob packages should work without installing ``bob`` itself. For example,
running:

.. code:: sh

    $ conda create --name env_name --override-channels \
      -c https://www.idiap.ch/software/bob/conda -c defaults \
      bob.<package-name>

should always create a working environment. If it doesn't, please let us know.


.. include:: links.rst
