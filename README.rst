.. vim: set fileencoding=utf-8 :

.. image:: http://img.shields.io/badge/docs-stable-yellow.svg
   :target: https://www.idiap.ch/software/bob/docs/bob/bob/v4.0.1/index.html
.. image:: http://img.shields.io/badge/docs-latest-orange.svg
   :target: https://www.idiap.ch/software/bob/docs/bob/bob/master/index.html
.. image:: https://gitlab.idiap.ch/bob/bob/badges/v4.0.1/build.svg
   :target: https://gitlab.idiap.ch/bob/bob/commits/v4.0.1
.. image:: https://gitlab.idiap.ch/bob/bob/badges/v4.0.1/coverage.svg
   :target: https://gitlab.idiap.ch/bob/bob/commits/v4.0.1
.. image:: https://img.shields.io/badge/gitlab-project-0000c0.svg
   :target: https://gitlab.idiap.ch/bob/bob
.. image:: http://img.shields.io/pypi/v/bob.svg
   :target: https://pypi.python.org/pypi/bob

====================
 Bob
====================

Bob is a free signal-processing and machine learning toolbox originally
developed by the Biometrics group at the `Idiap`_ Research Institute,
Switzerland.

The toolbox is written in a mix of `Python`_ and `C++`_ and is designed to be
both efficient and reduce development time. It is composed of a reasonably
large number of `packages`_ that implement tools for image, audio & video
processing, machine learning & pattern recognition, and a lot more task
specific packages.

**Please visit our** `website`_ **for more information.**


For the maintainers
===================

Below are some instructions for the maintainers of the package.


Adding/Removing a dependency package
------------------------------------

To remove or add a package from bob, search for its name (or the name of a
similar package in case you are adding a new package) in this repository and
add/remove its name in appropriate places.


Releasing a new version of Bob
------------------------------

Use the release script from bob.admin to do this.

.. External References

.. _c++: http://www2.research.att.com/~bs/C++.html
.. _python: http://www.python.org
.. _idiap: http://www.idiap.ch
.. _packages: https://www.idiap.ch/software/bob/packages
.. _wiki: https://www.idiap.ch/software/bob/wiki
.. _bug tracker: https://www.idiap.ch/software/bob/issues
.. _installation: https://www.idiap.ch/software/bob/install
.. _website: https://www.idiap.ch/software/bob
