# Notation

One symbol table for the whole course. A module may not introduce a competing
symbol for a quantity that already appears here. If a module genuinely needs a
new symbol, it adds a row to this file in the same session.

Where the literature disagrees with itself -- and in ballistics it often does --
this table states which convention we follow and names the alternative, so that
reading McCoy or Litz alongside the course does not cause confusion.

## Dimensions

Module 01 checks equations for dimensional homogeneity, which needs symbols for
the *dimensions* themselves rather than for quantities. Those are written in
square brackets, always:

| Notation | Meaning |
|---|---|
| $[x]$ | the dimensions of the quantity $x$ |
| $[\mathrm{M}]$, $[\mathrm{L}]$, $[\mathrm{T}]$ | the mass, length, and time dimensions |
| $[\Theta]$ | the thermodynamic temperature dimension (needed from M09 on) |
| $[1]$ | dimensionless |

The brackets are not decoration. Bare $M$, $L$, and $T$ are already taken in
this file -- Mach number, lapse rate, and temperature respectively -- so
$[\mathrm{M}]$ and $M$ are different things and the notation has to say which
is meant. A velocity is $[\mathrm{L}][\mathrm{T}]^{-1}$; a Mach number is
$[1]$.

## Kinematics

| Symbol | Quantity | SI unit | Notes |
|---|---|---|---|
| $t$ | time | s | $t=0$ at muzzle exit |
| $\vec{r}$ | position | m | components $(x, y, z)$ |
| $x$ | downrange distance | m | along the line of sight |
| $y$ | vertical position | m | positive up |
| $z$ | lateral position | m | positive right of the shooter |
| $\vec{v}$ | velocity | m/s | |
| $v$ | speed, $\lVert\vec{v}\rVert$ | m/s | |
| $\hat{v}$ | unit velocity vector | -- | $\vec{v}/v$ |
| $v_0$ | muzzle velocity | m/s | |
| $\vec{a}$ | acceleration | m/s² | |
| $\vec{g}$ | gravitational acceleration | m/s² | $\vec{g} = (0, -g, 0)$ |
| $g$ | standard gravity | m/s² | 9.80665 |
| $\theta$ | launch angle above the line of sight | rad | |
| $\phi_{\text{inc}}$ | inclination of the line of sight | rad | positive uphill |
| $T$ | time of flight | s | |

## The projectile

| Symbol | Quantity | SI unit | Notes |
|---|---|---|---|
| $m$ | projectile mass | kg | |
| $d$ | projectile diameter (calibre) | m | |
| $l$ | projectile length | m | often expressed in calibres, $l/d$ |
| $A$ | reference area | m² | $A = \pi d^2/4$ |
| $\text{SD}$ | sectional density | lb/in² | $m/d^2$ -- see units note below |
| $i$ | form factor | -- | relative to a named reference projectile |
| $\text{BC}$ | ballistic coefficient | lb/in² | $\text{SD}/i$ -- see units note below |
| $n$ | rifling twist | m/turn | one turn in $n$; commonly quoted in inches |
| $p$ | axial spin rate | rad/s | $p = 2\pi v_0 / n$ at the muzzle |
| $I_x$ | axial moment of inertia | kg·m² | |
| $I_y$ | transverse moment of inertia | kg·m² | |
| $S_g$ | gyroscopic stability factor | -- | dimensionless; $S_g > 1$ required |

## The atmosphere

| Symbol | Quantity | SI unit | Notes |
|---|---|---|---|
| $\rho$ | air density | kg/m³ | ~1.225 at ICAO sea level |
| $p$ | pressure | Pa | **station** pressure unless stated |
| $T$ | temperature | K | |
| $\text{RH}$ | relative humidity | -- | fraction in $[0,1]$, not percent |
| $e$ | water vapour partial pressure | Pa | |
| $R_d$ | specific gas constant, dry air | J/(kg·K) | 287.0528 |
| $R_v$ | specific gas constant, water vapour | J/(kg·K) | 461.495 |
| $\gamma$ | ratio of specific heats | -- | 1.400 for dry air |
| $a$ | speed of sound | m/s | $a=\sqrt{\gamma R_d T}$ |
| $M$ | Mach number | -- | $M = v/a$ |
| $L$ | temperature lapse rate | K/m | 0.0065 in the ICAO troposphere |
| $h$ | geopotential altitude | m | |
| $h_\rho$ | density altitude | m | |
| $\mu$ | dynamic viscosity | Pa·s | Sutherland's law |
| $\text{Re}$ | Reynolds number | -- | |

Note the collision on $p$: pressure in the atmosphere chapters, spin rate in the
stability chapters. They never appear in the same equation. Where a section
risks ambiguity, write $p_{\text{air}}$ and $p_{\text{spin}}$.

## Aerodynamics

| Symbol | Quantity | SI unit | Notes |
|---|---|---|---|
| $F_D$ | drag force | N | |
| $C_D$ | drag coefficient | -- | a function of $M$, not of $v$ |
| $C_{D_0}$ | zero-yaw drag coefficient | -- | what a 3DOF model uses |
| $q$ | dynamic pressure | Pa | $q = \tfrac{1}{2}\rho v^2$ |
| $\alpha$ | angle of attack | rad | |
| $\alpha_R$ | yaw of repose | rad | the source of spin drift |
| $C_{L\alpha}$ | lift curve slope | /rad | |
| $C_{M\alpha}$ | overturning moment coefficient | /rad | |

## Wind and Earth

| Symbol | Quantity | SI unit | Notes |
|---|---|---|---|
| $\vec{W}$ | wind velocity | m/s | the vector the **air** moves, not "from" |
| $W_x, W_z$ | head/tail and cross components | m/s | |
| $\vec{v}_{\text{air}}$ | air-relative velocity | m/s | $\vec{v} - \vec{W}$ |
| $D_z$ | crosswind deflection | m | |
| $\vec{\Omega}$ | Earth's angular velocity | rad/s | 7.292115e-5 |
| $\varphi$ | latitude | rad | positive north |
| $\psi$ | firing azimuth | rad | clockwise from true north |

Wind direction is a notorious ambiguity. **In this course $\vec{W}$ is the
velocity of the air**, so a "wind from the west" blowing toward the east is
$\vec{W}$ pointing east. Shooters normally name the direction wind comes *from*
(a "3 o'clock wind" comes from the shooter's right); `frames.wind_vector()` does
that conversion, and it is the only place the convention flips.

## Statistics and error

| Symbol | Quantity | Unit | Notes |
|---|---|---|---|
| $\sigma$ | standard deviation | varies | |
| $\sigma_r$ | radial (Rayleigh) dispersion parameter | m or rad | |
| $\bar{r}$ | mean radius | m or rad | |
| $\text{CEP}$ | circular error probable | m or rad | the 50% radius |
| $\text{ES}$ | extreme spread | m | largest centre-to-centre distance in a group |
| $n$ | sample size | -- | collides with twist rate; write $N_{\text{shots}}$ if unclear |
| $u(x)$ | standard uncertainty in $x$ | units of $x$ | GUM notation |
| $P_{\text{hit}}$ | hit probability | -- | |

## Angular measure

| Symbol | Quantity | Notes |
|---|---|---|
| $\text{MOA}$ | minute of angle | exactly 1/60 degree = 2.908882e-4 rad |
| $\text{SMOA}$ | "shooter's MOA" / IPHY | exactly 1 inch per 100 yards, i.e. 1/3600 as a ratio -- *not* a true MOA. $\text{MOA}/\text{SMOA} = \pi/3$ exactly (M01) |
| $\text{mil}$ | milliradian | exactly 0.001 rad; **not** any of the military 6000/6300/6400-mil circles |

"Mil" is the most abused unit in shooting. In this course it is always the true
milliradian, 1/1000 radian. Scope manufacturers agree with this; artillery
manuals often do not.

## The two units that are not SI, on purpose

Sectional density and ballistic coefficient are defined in **lb/in²**, and every
published BC you will ever encounter is in those units. Converting them to SI
would produce numbers that match no reference table and no bullet box, which is
worse than the inconsistency. So they stay imperial, and the variable names say
so: `sd_lbin2`, `bc_lbin2`. Every other quantity in the library is SI.
