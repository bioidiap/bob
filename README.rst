.. vim: set fileencoding=utf-8 :
.. Tiago de Freitas Pereira <tiago.pereira@idiap.ch>
.. Mon 20 Jul 2015 16:57:00 CEST


.. image:: http://img.shields.io/badge/docs-stable-yellow.svg
   :target: http://pythonhosted.org/bob/index.html
.. image:: http://img.shields.io/badge/docs-latest-orange.svg
   :target: https://www.idiap.ch/software/bob/docs/latest/bob/bob/master/index.html
.. image:: https://gitlab.idiap.ch/bob/bob/badges/v2.6.1/build.svg
   :target: https://gitlab.idiap.ch/bob/bob/commits/v2.6.1
.. image:: https://img.shields.io/badge/gitlab-project-0000c0.svg
   :target: https://gitlab.idiap.ch/bob/bob/commits/v2.6.1
.. image:: http://img.shields.io/pypi/v/bob.svg
   :target: https://pypi.python.org/pypi/bob
.. image:: http://img.shields.io/pypi/dm/bob.svg
   :target: https://pypi.python.org/pypi/bob

====================
 Bob
====================

Bob is a free signal-processing and machine learning toolbox originally
developed by the Biometrics group at `Idiap`_ Research Institute, Switzerland.

The toolbox is written in a mix of `Python`_ and `C++`_ and is designed to be
both efficient and reduce development time. It is composed of a reasonably
large number of `packages`_ that implement tools for image, audio & video
processing, machine learning and pattern recognition.


Installation
------------

Follow our `installation`_ instructions. Then, using the Python interpreter
provided by the distribution, bootstrap and buildout this package::

  $ python bootstrap-buildout.py
  $ ./bin/buildout
  

For the maintainers
-------------------

In the next subsections we have instructions for the maintainers of the package.

Adding a dependency package
===========================

   
   To add a package on bob, just append the package name in the file ('requirements.txt').

.. warning::
   Before adding a package to this prototype, please ensure that the package:

   * contains a README clearly indicating how to install the package (including
     external dependencies required). Also, please add package badges for the
     build status and coverage as shown in other packages.

   * Has unit tests.

   * Is integrated with Gitlab-CI and correctly tests on that platform (i.e.
     it builds, it tests fine and a documentation can be constructed and tested
     w/o errors)

   If you don't know how to do this, ask for information on the bob-devel
   mailing list.


Updating the dependencies
=========================

 If you want to update the version of the dependency packages, run the following commands::
 
 $ ./bin/python ./bob/script/get_versions.py > requirements.txt
 $ git commit requirements.txt -m "Update requeriments" && git push
 

Removing a dependency package
=============================

   To remove a package on bob, just remove the package name in the file ('requirements.txt').


.. External References

.. _c++: http://www2.research.att.com/~bs/C++.html
.. _python: http://www.python.org
.. _idiap: http://www.idiap.ch
.. _packages: https://www.idiap.ch/software/bob/packages
.. _wiki: https://www.idiap.ch/software/bob/wiki
.. _bug tracker: https://www.idiap.ch/software/bob/issues
.. _dependencies: https://gitlab.idiap.ch/bob/bob/wikis/Dependencies
.. _installation: https://www.idiap.ch/software/bob/install

