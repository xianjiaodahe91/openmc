.. _notes_0.6.2:

==============================
Release Notes for OpenMC 0.6.2
==============================

-------------------
System Requirements
-------------------

There are no special requirements for running the OpenMC code. As of this
release, OpenMC has been tested on a variety of Linux distributions, Mac OS X,
and Microsoft Windows 7. Memory requirements will vary depending on the size of
the problem at hand (mostly on the number of nuclides in the problem).

------------
New Features
------------

- Meshline plotting capability
- Support for plotting cells/materials on middle universe levels
- Ability to model cells with no surfaces
- Compatibility with PETSc 3.5
- Compatability with OpenMPI 1.7/1.8
- Improved overall performance via logarithmic-mapped energy grid search
- Improved multi-threaded performance with atomic operations
- Support for fixed source problems with fissionable materials

---------
Bug Fixes
---------

- 26fb93_: Fix problem with -t, --track command-line flag
- 2f07c0_: Improved evaporation spectrum algorithm
- e6abb9_: Fix segfault when tallying in a void material
- 291b45_: Handle metastable nuclides in NNDC data and multiplicities in MT=5 data

.. _26fb93: https://github.com/mit-crpg/openmc/commit/26fb93
.. _2f07c0: https://github.com/mit-crpg/openmc/commit/2f07c0
.. _e6abb9: https://github.com/mit-crpg/openmc/commit/e6abb9
.. _291b45: https://github.com/mit-crpg/openmc/commit/291b45

------------
Contributors
------------

This release contains new contributions from the following people:

- `Will Boyd <wbinventor@gmail.com>`_
- `Matt Ellis <mellis13@mit.edu>`_
- `Sterling Harper <smharper@mit.edu>`_
- `Bryan Herman <bherman@mit.edu>`_
- `Nicholas Horelik <nicholas.horelik@gmail.com>`_
- `Anton Leontiev <bunder@t-25.ru>`_
- `Adam Nelson <nelsonag@umich.edu>`_
- `Paul Romano <paul.k.romano@gmail.com>`_
- `Jon Walsh <walshjon@mit.edu>`_
- `John Xia <john.danger.xia@gmail.com>`_
