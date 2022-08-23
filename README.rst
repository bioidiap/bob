.. vim: set fileencoding=utf-8 :

.. image:: https://img.shields.io/badge/docs-latest-orange.svg
   :target: https://www.idiap.ch/software/bob/docs/bob/bob/master/index.html
.. image:: https://gitlab.idiap.ch/bob/bob/badges/master/pipeline.svg
   :target: https://gitlab.idiap.ch/bob/bob/commits/master
.. image:: https://gitlab.idiap.ch/bob/bob/badges/master/coverage.svg
   :target: https://gitlab.idiap.ch/bob/bob/commits/master
.. image:: https://img.shields.io/badge/gitlab-project-0000c0.svg
   :target: https://gitlab.idiap.ch/bob/bob

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

The list of bob packages here should be in sync with bob.nightlies.
You may use the `bdt gitlab update-bob` command for automatic update of the list of
packages.


Releasing a new version of Bob
------------------------------

See bob.devtools documentation.

.. External References

.. _c++: http://www2.research.att.com/~bs/C++.html
.. _python: http://www.python.org
.. _idiap: http://www.idiap.ch
.. _packages: https://www.idiap.ch/software/bob/packages
.. _wiki: https://www.idiap.ch/software/bob/wiki
.. _bug tracker: https://www.idiap.ch/software/bob/issues
.. _installation: https://www.idiap.ch/software/bob/install
.. _website: https://www.idiap.ch/software/bob
