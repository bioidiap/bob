.. _bob.install:

***************************
 Installation Instructions
***************************

We offer pre-compiled binary installations of Bob using `conda`_ for Linux and
MacOS 64-bit operating systems. Currently, we do not support Windows.

Please install and get familiar with `conda`_ first by referring to their
website before getting started. Then, make sure you have an up-to-date `conda`_
installation with the **correct configuration** by running the commands below:

.. code:: sh

    $ conda update -n root conda
    $ conda config --set show_channel_urls True
    $ conda config --add channels defaults
    $ conda config --add channels https://www.idiap.ch/software/bob/conda

Now you can create an envrionment and install |project| in that environment:

.. code:: sh

    $ conda create -n bob_py3 --override-channels \
      -c https://www.idiap.ch/software/bob/conda \
      -c defaults \
      python=3 bob
    $ source activate bob_py3
    $ python -c 'import bob.io.base'

.. warning::

    Be aware that if you use packages from our channel and other user/community
    channels (especially ``conda-forge``) in one environment, you may end up
    with a broken envrionment. We can only guarantee that the packages in our
    channel is compatible with the ``defaults`` channel.

You can install other |project| `packages`_ by reading the instructions on
their webpage. In most cases, the installation should be as simple as:

.. code:: sh

   $ conda install <package-name>

or if there are no conda packages available for that package:

.. code:: sh

   $ pip install <package-name>


For a comprehensive list of packages that are either part of |project| or use
|project|, please visit `packages`_.


.. include:: links.rst
