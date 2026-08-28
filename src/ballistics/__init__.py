"""Exterior ballistics library, built module by module across the course.

This package starts nearly empty on purpose. Each course module in ``modules/``
adds one or more files here, and the module's lesson explains why the code is
shaped the way it is. See ``CURRICULUM.md`` for the library build map: which
module owns which file, and what public API it introduces.

Conventions that hold everywhere in this package (see ``docs/units-and-conventions.md``):

* All internals are strict SI: metres, kilograms, seconds, kelvin, pascals, radians.
* Every variable name carries a unit suffix: ``range_m``, ``velocity_mps``,
  ``mass_kg``, ``angle_rad``. Imperial units appear only at the I/O boundary and
  are suffixed too: ``twist_in``, ``drop_moa``, ``mv_fps``.
* The one deliberate exception is ballistic coefficient, kept in lb/in^2,
  because that is its definition. It is named ``bc_lbin2``.
* Coordinate frame: right-handed, origin at the muzzle. +x downrange along the
  line of sight, +y up, +z to the shooter's right.
"""

__version__ = "0.1.0"

__all__ = ["__version__"]
