# StructureAnalysisEnvironment (SAE)

[![en](https://img.shields.io/badge/lang-en-red.svg)](https://github.com/ohara-lab-su/sae/blob/main/README.en.md)
[![ja](https://img.shields.io/badge/lang-ja-yellow.svg)](https://github.com/ohara-lab-su/sae/blob/main/README.md)

[![GitHub](https://img.shields.io/badge/GitHub-ohara--lab--su%2Fsae-181717?logo=github)](https://github.com/ohara-lab-su/sae/)
[![Ohara Lab](https://img.shields.io/badge/Ohara%20Lab-Home-4B5563?logo=homeassistant&logoColor=white)](https://ohara-lab-su.github.io/index.en.html)


## Introduction

As of 2026, projects such as ASE and pymatgen have advanced considerably, leaving almost no reason for this project to exist. This code is effectively obsolete.

Nevertheless, it supports some relatively obscure Japanese-developed codes, so it may still be useful in certain circumstances. I have made some modifications to bring it into a form that can be used today. However, it has hardly been tested.

## About the Program

This Python framework aims to unify input/output handling and analysis across first-principles and reverse Monte Carlo calculation codes, including VASP, WIEN2k, Quantum ESPRESSO, OpenMX, CP2K, HiLAPW, FDMNES, and RMC_POT. It enables structural construction, analysis, and input/output operations through a common interface, without requiring users to be concerned with differences between calculation codes. The practical tools developed using the framework also allow end users to perform calculations and analyses using essentially the same procedures.

Version 0.1.0 takes the existing class architecture one step further by organizing namespaces by calculation code and classes by the files and functions handled within each namespace. Version 0.0.x already used the pattern of loading structures and calculation results into instances and applying methods to transform, analyze, and write them. That principle remains unchanged. This update reorganizes functionality and call destinations scattered by years of incremental development, making the library easier to use while preserving the results produced by the existing formulas, algorithms, and parsers.

## Excuses from the Original Development Period

This was developed in considerable haste, and many planned features were never fully realized. Major development largely stopped around 2015; although I have made changes when necessary since then, the result remains incomplete. I also did not understand Python particularly well at the time, and much of the code looks rather careless in retrospect.

## History

- ver_0.1.0: 2026.10.15 Reorganized and extended the existing class architecture, separating namespaces by calculation code. Retained Python 3.7 syntax and consolidated package configuration in `pyproject.toml`.
- ver_0.0.18: 2020.11.18 21:11 Hasty minor adjustments; partially resolved namespace problems.
- ver_0.0.15: 2020.11.18 Hasty minor adjustments.
- ver_0.0.6: 2018.10.15 Hasty minor adjustments (minor fixes). **Python3.0**
- ver_0.0.0: 2015.02.16 Last-Release Version (development discontinued).
- ... relics from even earlier versions.

## License and Disclaimer

This software is licensed under Apache License 2.0. Users must comply with Apache License 2.0 when using it. Under that license, the author assumes no liability for the software. See the included `LICENSE.txt` for details.

## Intended Runtime Environment

Development was primarily performed on Mac OS X, and testing primarily on Linux. Version 0.0.x was also tested to some extent on Windows 7 Pro and Windows 8.1 Pro. Ideally, the software should run almost anywhere Python is installed, but version 0.1.0 has not been revalidated on every platform.

Version 0.1.0 uses **Python 3.7 or later syntax**. Syntax and instantiation of the central classes were checked under Python 3.7.9; tests involving numerical processing were performed under Python 3.12.11. This does not mean that all numerical operations, including dependencies, have been verified under Python 3.7. The principal test environments for 0.0.x were Python 3.6.10, 3.7.10, and 3.9.1.

## Installation

Extract the source and execute the following in the directory containing `pyproject.toml`:

```sh
python -m pip install .
```

Installation from a wheel is also supported:

```sh
python -m pip install structureanalysisenvironment-0.1.0-py3-none-any.whl
```

The distribution name remains `StructureAnalysisEnvironment`, while its Python import name is `sae`. Build configuration, dependencies, and tool registrations are consolidated in `pyproject.toml`. Version 0.1.0 is self-contained; earlier versions and the `OLD` directory are not required.

Previously, installation instructions used `python setup.py install` or pip installation from Git:

```sh
pip install git+http://selenium.spring8.or.jp:8081/analysis/sae.git
```

Those instructions and that distribution location applied to 0.0.x. Version 0.1.0 does not use `setup.py`. The still older 64-bit Windows installer, `StructureAnalysisEnvironment-0.0.1.win-amd64.exe`, targeted Python 2.7 and had some restrictions under Python 2.6. At that time the package was not registered on PyPI, so installation relied on that installer or `setup.py`. The Windows installer is no longer supported.

## Required Python Version and Modules

The original targets were Python 2.7 and, subsequently, Python 3.5 or later. Version 0.1.0 standardizes on Python 3.7 or later syntax. Install compatible versions of the following modules for your Python environment:

* [ASE](https://wiki.fysik.dtu.dk/) (AtomicSimulationEnvironment)
* [NumPy](http://www.numpy.org)
* [Matplotlib](http://matplotlib.org)
* pandas
* humanfriendly
* coloredlogs
* xlogger-py

Some CIF-related operations use PyCifRW, while some 3D rendering and GUI operations use [VPython](http://vpython.org) and [wxPython](http://www.wxpython.org). The GUI components assume the older `visual` and `wx` environments; they have not been rewritten for the current VPython API. Calculation programs, their result files, and configuration such as OpenMX pseudopotentials must be supplied separately.

### Modules Previously Required for Matplotlib

Older environments also listed the following modules in addition to NumPy and SciPy. Install them as appropriate for the Matplotlib version and environment:

* [SciPy](http://www.numpy.org): Used in Matplotlib-based processing.
* [pytz](https://pypi.python.org/pypi/pytz/): Used in older Matplotlib environments.
* [pyparsing](https://pypi.python.org/pypi/pyparsing): Used by Matplotlib.
* [six](https://pypi.python.org/pypi/six): Used in older Matplotlib environments.

## Basic Framework Usage

Programs can be written in ordinary object-oriented Python style. As in 0.0.x, structural information and calculation results are loaded into class instances and processed by methods. For example, the following few lines convert a VASP POSCAR structure file into FDMNES format. <b>The actual conversion requires just two lines of code.</b>

```python
#!/usr/bin/env python
from sae import VASP

cell = VASP("POSCAR")
cell.write(code="FDMNES")
```

This corresponds to the previous `import StructureAnalysisEnvironment as SAE` and `SAE.io.Read(filename='POSCAR', code='VASP')` usage. In 0.1.0, you can directly use the class for a particular calculation code. No compatibility layer for the old import name is provided; existing scripts must update their imports and call sites.

These classes and methods provide various options. For example, they can read VASP input files other than POSCAR and automatically generate inputs with nearly equivalent calculation conditions. Coordinates can also be transformed while retaining the structure, and the result written out.

```python
from sae import VASP

vasp = VASP("POSCAR")
vasp.conv_direct2car()
vasp.write(outname="converted", code="FDMNES")
```

`vasp.structure` is a `ReadVaspPoscar` instance holding the structure. To handle DOSCAR, call `vasp.read_dos("DOSCAR")`: the resulting `ReadVaspDoscar` instance is stored in `vasp.dos` and also returned. State changes, return values, and default options of individual methods follow their existing implementations. Methods have not been standardized to return a separate instance for every transformation.

You can also instantiate the class for the target file directly:

```python
from sae.vasp.poscar import ReadVaspPoscar

cell = ReadVaspPoscar("POSCAR")
cell.conv_direct2car()
cell.write(outname="converted", code="FDMNES")
```

Previously, in addition to an instance's `write` method, operations could be invoked through functions such as `SAE.write(cell, code='FDMNES')`. In 0.1.0, formerly independent operations have been grouped into classes according to their roles. The corresponding usage is available through `StructureWriter` methods:

```python
from sae.vasp.poscar import ReadVaspPoscar
from sae.structure.writer import StructureWriter

cell = ReadVaspPoscar("POSCAR")
StructureWriter().write(cell, code="FDMNES")
```

Numerous additional structural methods are available, including supercell construction and rotations based on Euler angles. Post-calculation electronic-state processing can be performed through similar procedures. Each operation offers numerous options, so users familiar with Python should be able to handle everything from structural construction to electronic-state analysis through a unified interface.

### Classes and Internal Architecture

Version 0.0.x already grouped data and operations into various Read classes and shared Method classes. As calculation codes and functionality accumulated, however, the locations of classes and standalone functions and the names used by their callers became difficult to follow. Version 0.1.0 reorganizes these components by calculation code and separates the corresponding files and functions within each code.

| Calculation code / target | Namespace | Main class |
| --- | --- | --- |
| VASP | `sae.vasp` | `VASP` |
| OpenMX | `sae.openmx` | `OpenMX` |
| FDMNES | `sae.fdmnes` | `FDMNES` |
| HiLAPW | `sae.hilapw` | `HiLAPW` |
| Quantum ESPRESSO / PWscf | `sae.pwscf` | `PWscf` |
| WIEN2k | `sae.wien2k` | `WIEN2k` |
| RMC_POT | `sae.rmcpot` | `RMC_POT` |
| LOBSTER | `sae.lobster` | `LOBSTER` |
| Bader | `sae.bader` | `Bader` |
| Athena | `sae.athena` | `Athena` |
| PF | `sae.pf` | `PF` |

For example, the `VASP` class in `sae/vasp/vasp.py` holds instances for structure, input, output, and analysis associated with a calculation. POSCAR data and coordinate operations belong to `ReadVaspPoscar` in `sae/vasp/poscar.py`; DOSCAR is handled by `ReadVaspDoscar` in `doscar.py`; POSCAR output is handled by `PoscarWriter` in `poscar_writer.py`. The same operations are accessible through file-specific classes or calculation-code-level classes.

Likewise, FDMNES separates input structures (`sae/fdmnes/inp.py`), input generation (`inp_writer.py`), and calculation results (`bav.py`). Distinctions for different generations of output formats have been retained. Existing commands for CP2K are included, but there is not yet a standalone `CP2K` class.

Shared coordinate transformations have been grouped into `CoordinateTransforms`, supercell operations into `SupercellOperations`, the periodic table into `ElementTable`, and text-file reading into `TextFiles`. Former standalone functions are used as methods of these classes. Their implementations reside in the respective modules; this is not a mechanism for calling into the old source tree. The existing approach of loading structures or calculation results and then transforming, analyzing, and generating data from them remains unchanged.

For more detail on the layout, see the [implementation map](docs/implementation-map.json), [class bindings](docs/class-bindings.json), and [design documentation](docs/design.md).

### Usage Examples and Samples

[examples/vasp_conversion.py](examples/vasp_conversion.py) demonstrates VASP structure conversion, while [examples/fdmnes_input.py](examples/fdmnes_input.py) demonstrates FDMNES input generation. Small practical scripts from earlier versions, including their comments, are retained in [examples/legacy](examples/legacy/README.md). They may be useful as starting points for scripts that users adapt to their own requirements.

Whereas `examples/` contains code usage examples, `src/sae/sample_input/` contains sample calculation data and related files. Reference values saved for testing are stored in `tests/golden/`.

The individual functions are not described exhaustively here. In practice, they can also be accessed through the tools built on this framework. End users performing ordinary calculations and analyses should begin with the tools described below.


## Tools Built on the Framework

The tools are located in `src/sae/commands` and are registered as executable scripts during installation. In version 0.1.0, the classes called internally have been connected to the new namespaces. For the 197 commands actually included, consult the [command list](docs/commands.md) and `pyproject.toml`. The descriptions below also include older development plans and historical support status, so they do not necessarily match the current inventory. Legacy scripts whose names contain `BUG` also remain.

### Basic Conventions

Ordinary users rarely need to use the framework directly. Instead, they generally use the tools distributed with it. With some exceptions, the tools follow the naming conventions below. Similarly named tools usually provide similar functions, allowing a large number of operations to be performed through nearly identical procedures.

1. Programs beginning with an <b>uppercase letter</b> are <b>general-purpose tools</b> that users need not edit. Some have grown into highly capable, relatively large programs with numerous command-line options. Most provide at least some help with `-h`. They can be regarded as sophisticated general-purpose macros.
2. Programs beginning with a <b>lowercase letter</b> must be edited directly by users as necessary. In practice, however, they are small, flexible scripts; anyone familiar with Python can readily adapt them to a particular purpose. In that sense they may be the most useful tools. They are a kind of informal, ad hoc macro.
3. The initial <b>uppercase or lowercase letter</b> identifies the calculation code. The naming convention was inspired by tools such as `LAcopy`, distributed with Professor Oguchi's HiLAPW. Numerous analogous utilities exist for other codes, including `Vcopy` and `Vmove` for VASP, but many are written in c-shell, b-shell, or Perl and are therefore not packaged as framework tools.
   1. `CP*.py` (prefix <b>CP</b>): <b>CP2K</b>.
   2. `FD*.py` (prefix <b>FD</b>): <b>FDMNES</b>.
   3. `LA*.py` (prefix <b>LA</b>): <b>HiLAPW</b>.
   4. `MX*.py` (prefix <b>MX</b>): <b>OpenMX</b>.
   5. `PW*.py` (prefix <b>PW</b>): <b>Quantum ESPRESSO (PWscf)</b>.
   6. `R*.py` (prefix <b>R</b>): <b>RMC_POT</b>.
   7. `V*.py` (prefix <b>V</b>): <b>VASP</b>.
   8. `W*.py` (prefix <b>W</b>): <b>WIEN2k</b>.
4. Tools whose names differ only in their initial uppercase letter generally perform the same task using almost the same procedure.
   1. For example, `Vplot_LDOS.py` and `Wplot_LDOS.py` both plot LDOS with nearly identical command-line options.
   2. `LAcopy` and `FDcopy` provide nearly equivalent functionality.
   3. Programs with `*plot*` in their names use matplotlib for 2D or 3D plotting.

### Overview of Included Tools

The following are selected tools developed using this framework that are considered reasonably maintained and practical. They are included in the framework package and should be available on the command line after installation, assuming the installation registered their paths correctly. The package contains many more tools than are described here; those the author seldom uses, older tools, and collections of functions intended to be invoked from other programs (including scripts used directly as functions rather than modules) are omitted from this introduction.

Plotting tools in particular have grown considerably and offer very large numbers of options. Most options are not explained here; consult the help displayed by running each tool with `-h`.

#### for CP2K
- <b>CPvasp2inp.py</b>: Converts a VASP POSCAR file into CP2K `*.inp` format. The CP2K input syntax supports sophisticated macro-like constructs, and only part of it is currently supported. The script also reads VASP calculation-control input files in addition to the POSCAR structure and supports a subset of their parameters and input formats. Although incomplete, it can generate CP2K input from VASP input files that can be used to run a calculation. Support was planned to be expanded incrementally.

#### for FDMNES
- <b>FDbav2xyz.py</b>: Exports an XYZ file from `*_bav.txt`. The structure recorded in `*_bav.txt` depends on the cluster radius used in the calculation. Conversion to XYZ makes it easy to visualize the cluster cut out at a given radius. XYZ can be visualized by VESTA and almost all other structural visualization tools.
- <b>FDcif2fdm.py</b>: Generates an FDMNES `*.inp` input file from `*.cif`. In addition to structural information, the generated input contains a sample configuration for a typical calculation. Thus, a CIF file can be turned into input suitable for basic XANES calculations with almost no modifications.
- <b>FDclean.py</b>: Deletes FDMNES output and related files, restoring the pre-calculation file layout. Its design follows the author's Vclean, LAclean, and similar utilities for other codes written in c-shell, b-shell, or Perl. It is implemented in Python specifically to retrieve the filename prefix from the `filout` tag in `*.inp` through the FDMNES class. The older scripts were intended to be migrated to Python incrementally.
- <b>FDmove.py</b>: Renames the files produced according to the `filout` tag in one operation, providing functionality similar to `Vmove`.
- <b>FDconv_e2photoe.py</b>: Converts a post-calculation `*_conv.txt` file expressed in energy above the Fermi level to photon-energy form and reruns the convolution calculation. Useful when the original calculation omitted the `Energpho` tag, or when converting back to the original Fermi-level representation.
- <b>FDfdm2vasp.py</b>: Converts structural information from an FDMNES `*.inp` input file to VASP POSCAR format. This may be useful when an FDMNES structure has been entered manually rather than converted from another structure. Some flexible FDMNES-specific structural input forms, including space-group specifications, are not yet fully supported.
- <b>FDmakeCconvAllsite.py</b>: When a calculation uses multiple absorbers, for example with `allsite` and no explicitly specified absorber, convolution is not performed for every site. This script prepares convolution for all sites after the calculation by generating the required `*.inp` files in a batch, along with `fdmfiles.txt` to execute them sequentially. **Running this script overwrites `fdmfiles.txt`.**
- <b>FDpbd2fdm.py</b>: Converts a PDB file to FDMNES `*.inp` format. FDMNES already has a native PDB import function, but some programs write lattice information in commented lines to represent periodic structures. The author suspects this is not part of the official PDB specification, although programs such as VESTA and CrystalMaker support it. FDMNES appears to recognize this convention, but its import behavior for it seems somewhat buggy, perhaps because it is not an official PDB feature. For exported periodic structures, explicitly converting to `*.inp` with this script may reproduce the intended structure more reliably than native FDMNES import. Ordinary PDB files containing XYZ-style coordinates are also supported.
- <b>FDplot_XAS.py</b>: A feature-rich plotting utility for displaying XANES calculation results from `*_conv.txt`, `*.txt`, and related files together with density-of-states data from files such as `*_sd.txt`. It also supports averaging results and numerous other options. It normally opens a matplotlib GUI, allowing zooming and saving, and automatically exports plots as PDF, PNG, and EPS by default. Run with `-h` for details.
- <b>FDplot_XASs.py</b>:
- <b>FDplot_XAS_LDOS.py</b>: Displays convolved XAS results and the LDOS of selected atoms in stacked panels for orbital analysis. Much of its basic functionality is already available in `FDplot_LDOS.py`, making this something of a shortcut script. Because development has concentrated on `FDplot_LDOS.py`, this script may eventually be retired.
- <b>FDplot_LDOS.py</b>: Displays the LDOS of selected atoms in stacked panels for orbital analysis. It can sum contributions from multiple selected atoms, plot XANES simultaneously, and display integrated DOS. It also supports raw and convolved XANES spectra, total DOS, and integrated DOS. Although it overlaps with `FDplot_XAS.py`, its main focus is LDOS and it does not include options such as averaging XAS results.
- <b>FDplot_PDOS.py</b>: Displays the PDOS of selected atoms in stacked panels: the PDOS counterpart of the LDOS plotting tool. Since FDMNES output is originally resolved by `lm`, this may be regarded as the fully featured counterpart of `LDOS.py`. Intended for orbital analysis; it also allows the user to specify which orbitals to display and how the selected orbitals are labeled.
- <b>FDvasp2fdm.py</b>: Converts a VASP POSCAR file into FDMNES `*.inp`. It writes both structural data and sample settings for a typical calculation, allowing basic XANES calculations with almost no changes.
- <b>FDxyz2fdm.py</b>: Converts an XYZ-format (MD-format) file into FDMNES `*.inp`.
- <b>fdExp_comp_XAS.py</b>: A simpler counterpart of `FDplot_XAS.py` that also uses the framework's Athena class for reading normalized experimental data (`nor` format), allowing experimental and calculated spectra to be plotted together. Its deliberately simple implementation makes it easy for users to edit for their particular plots; it also serves as an example program.
- <b>fdLDOS.py</b>: A minimal program containing the basic plotting functionality for DOS information in `*_sd*.txt`. `FDplot_XAS.py` can plot the absorber DOS, but not the local DOS of other sites. This script is a useful starting point for local DOS analysis.
- <b>fdLDOS0_specified.py</b>: Similar to `fdLDOS.py`, but includes LDOS normalization options also found in `FDplot_XAS.py`, such as normalization by site or by atom. It serves as a basic example for checking and using these features.
- <b>fdPDOS_XAS_av.py</b>: Based on `FDplot_PDOS.py`; directly accesses multiple calculation results to average and plot them. It must be adapted case by case.
- <b>fdLDOSmulti.py</b>: A minimal, manually assembled multipanel example based on `FDplot_LDOS.py`, using `subplot`. It requires editing, but is a flexible and practical template.
- <b>fdMulti.py</b>: Another minimal manually assembled multipanel example based on `FDplot_LDOS.py`, using explicit numeric placement instead of `subplot`. It is more readily adjustable than `fdLDOSmulti.py` without needing to master `subplot`.
- fdXAS.py
- fdXAS_specified.py

#### for HiLAPW
- <b>LAvasp2sets.py</b>: Converts VASP POSCAR format to HiLAPW `sets.in`. At present it only generates space group P1, preserving the VASP description. The author had planned to develop an independent symmetry finder for P1 structures such as those used by VASP. External tools such as [FINDSYM](http://stokes.byu.edu/iso/findsym.php) can identify symmetry; FINDSYM is particularly powerful and recommended.

#### for OpenMX
- MXEE.py
- MXEI.py
- <b>MXdat2vasp.py</b>: Converts structural information in an OpenMX `*.dat` file to VASP POSCAR format, with options for Cartesian and direct coordinates.
- <b>MXdat2xyz.py</b>: Converts structural information in an OpenMX `*.dat` file into XYZ format.
- MXdosall.py
- MXfindDAT.py
- MXfindPAO.py
- MXgetvalence.py
- MXjoinxyz.py
- <b>MXmd2vasprun.py</b>: Forcibly converts the `*.md` output of an OpenMX structural relaxation into VASP `vasprun.xml` format. This makes it easy to animate the `*.md` trajectory using the VASP visualization tool p4vasp. The author believes that a converter specifically producing XML for p4vasp may have been the first of its kind. It can be unexpectedly useful for VASP users.
- MXplot\_ADOS.py
- MXplot\_ADOS\_portrait.py
- MXplot\_LDOS.py
- MXplot\_MXEI.py
- MXplot\_PDOS.py
- MXplot\_TDOS+.py
- MXplot\_TDOS.py
- MXplot\_temperature.py
- MXtemp.py
- <b>MXvasp2mx.py</b>: Reads a VASP POSCAR structural file and converts it to OpenMX `*.dat` input. OpenMX `*.dat` also contains calculation controls corresponding to VASP INCAR and KPOINTS. When these other VASP input files are available, the script actively reads them and automatically generates OpenMX input with calculation conditions as close as possible to the VASP setup, enabling nearly one-to-one conversion between VASP and OpenMX. Numerous options allow conversion using Cartesian or fractional coordinates relative to primitive translation vectors. The author selects pseudopotential and pseudo-atomic-orbital (PAO) information from examples on the OpenMX website based on the POSCAR data, so the generated `*.dat` should generally run without editing. Users dissatisfied with these recommended defaults should modify the PAO and VPP files themselves.
- mxDOS1.py

#### for Quantum ESPRESSO
- <b>PWin2vasp.py</b>: Reads a Quantum ESPRESSO (PWscf) `*.in` input file and converts it to VASP POSCAR format. Since PWscf input includes calculation controls as well as structure, the program can also translate these into VASP INCAR and KPOINTS. Options include reading pseudopotential information and automatically generating POTCAR.
- PWmakePPinp.py
- <b>PWout2vasp.py</b>: Reads a Quantum ESPRESSO (PWscf) calculation output file (called `*.out` here, although its name is arbitrary) and converts its structure to VASP POSCAR format. Optional functions read calculation-control information and prepare INCAR, KPOINTS, and POTCAR to reproduce the PWscf calculation conditions as closely as possible.
- <b>PWout2vasprun.py</b>: Reads Quantum ESPRESSO (PWscf) calculation output and rewrites it in VASP `vasprun.xml` format. This can be visualized with p4vasp, making MD animations, forces, and other results easy to inspect. Conversion of DOS and LDOS output to `vasprun.xml` is not supported at present.
- PWplot\_TDOS.py
- PWplot\_XAS.py
- <b>PWvasp2in.py</b>: Generates Quantum ESPRESSO (PWscf) `*.in` input from a VASP POSCAR structure. PWscf reads standard input, so the actual filename is arbitrary; `*.in` is used here as a convention. Optional functions also read KPOINTS, POTCAR, and INCAR when present and translate their information into PWscf input.
- <b>pwPDOS.py</b>: Be aware that Quantum ESPRESSO PDOS requires an absurdly large number of k-points to obtain reasonable results (the output is not symmetrized).
- pwTDOS.py

#### for RMC\_POT
- Rcfg2vasp.py
- RchangeDensity.py
- RcollSplit.py
- RcollSplit\_nonSplit.py
- RgetDensity.py
- Rmove.py
- Rmove1.py
- Rplot\_Crystal.py
- Rplot\_Crystal0.py
- Rplot\_CrystalAnimeCFG.py
- Rplot\_fit.py
- Rplot\_ppcf.py
- Rplot\_ppcf2.py
- Rplot\_ppcf3.py
- Rvasp2cfg.py

#### for VASP
- Vacf.py
- Vados.py
- Vband.py
- <b>Vcar2direct.py</b>: Converts a Cartesian POSCAR to Direct coordinates.
- <b>Vch</b>: Checks files required for a VASP calculation. Running it before calculation helps prevent omissions of required files or parameters.
- <b>VchangeVacumm.py</b>: Readjusts vacuum regions in POSCAR and related structures.
- <b>Vdirect2car.py</b>: Converts Direct POSCAR coordinates to Cartesian. Compared with my Perl version, options such as changing the lattice-constant scale without changing internal absolute coordinates are currently disabled.
- Vextract0.py
- VfindBond.py
- VfindNN0.py
- VfindNN1\_library0.py
- VfindNN1\_library1.py
- VfindNN2FNC.py
- Vforce.py
- Vforce2md.py
- <b>VgetCOHPinfo.py</b>: Checks the orbital components and bonded atom pairs included in COHP analysis.
- <b>Vldos.py</b>: Exports LDOS in gnuplot format, compatible with my Perl plotting scripts, with nearly the same functionality as Vldos.pl. The Vplot\_LDOS*.py series now largely replaces it, but it remains useful for gnuplot users, particularly those with elaborate gnuplot scripts. Automatically sums m-resolved contributions into l components when lm decomposition was calculated. The gnuplot output uses indices to separate atomic species; see comments in the output files. Spin is supported.
- <b>Vldos_COHP.py</b>: Like Vldos.py, but reads DOSCAR.lobster instead of DOSCAR and exports the LOBSTER-reprojected LDOS in gnuplot format.
- <b>VmakeSuperCell2.py</b>: Builds a supercell from VASP POSCAR using specified multiplication factors.
- VmodifyAtomPosition.py
- <b>Vpdos.py</b>: Exports PDOS in gnuplot format, compatible with my Perl plotting programs and offering nearly the same functionality as Vpdos.pl. The Vplot\_PDOS*.py series now largely replaces it, but this tool remains useful for gnuplot users, particularly with advanced existing gnuplot scripts. The output uses gnuplot indices to separate atomic species; see the comments in the output files. Spin is supported.
- Vplot\_ADOS.py
- Vplot\_ADOS\_portrait.py
- Vplot\_Bader.py
- <b>Vplot\_COHP\_tate.py</b>: Plots LOBSTER pCOHP results, together with the LDOS reprojected for pCOHP analysis. Uses two side-by-side columns: DOS on the left and COHP on the right. With spin polarization, the default shows up-spin only and starts from the LDOS of the first atom. Displays COHP for selected numbered atomic pairs. Multiple pair numbers can be specified to display multiple LDOS and pCOHP results together, although many atoms or pairs quickly make the plot hard to interpret. Spins can be selected separately, or up and down spins plotted together, although the latter can become overcrowded. Select only the information needed. Running VgetCOHPinfo.py first makes it easier to identify analyzed orbital components and atom pairs and specify them to Vplot\_COHP\_tate.py.
- <b>Vplot\_COHP\_yoko.py</b>: Performs nearly the same analysis as Vplot\_COHP\_tate.py, but displays the LDOS used in COHP analysis in vertically stacked panels, as in Vplot\_LDOSm.py. This layout may be more suitable for publication figures focused on orbital decomposition of LDOS. Features include plotting multiple bonded pairs together, selecting a single pair, and showing its l-decomposed LDOS components.
- Vplot\_Crystal.py
- Vplot\_CrystalAnimeMD.py
- Vplot\_CrystalAnimePOSCAR.py
- <b>Vplot\_COHP_LDOSm.py</b>: Equivalent to Vplot\_LDOSm.py, except that it reads DOSCAR.lobster rather than DOSCAR.
- <b>Vplot\_COHP_PDOS.py</b>: Equivalent to Vplot\_PDOS.py, except that it reads DOSCAR.lobster rather than DOSCAR. It can also display COHP results for specified bonded pairs simultaneously.
- <b>Vplot\_LDOS.py</b>: Plots LDOS from DOSCAR and PROCAR in a single panel. Arguments select particular atomic species. Numerous options control plot ranges and other settings, making it a versatile plotting tool. It is convenient for quickly producing LDOS plots. Output files such as *.pdf acquire an atomic-species suffix when species are selected. Supports a single spin or both spins, with one inverted vertically.
- <b>Vplot\_LDOSm.py</b>: Whereas Vplot\_LDOS.py displays l-decomposed LDOS for selected atoms in a single panel, Vplot\_LDOSm.py displays orbital components in multiple stacked subplots. In most cases the multipanel view makes orbital components easier to inspect and is recommended. Supports one spin or both spins, with one inverted. If VASP was run with lm decomposition, for example LORBIT=11, it automatically sums m components into l components. Since lm-projected calculations contain the information needed for l decomposition, I recommend calculating lm-resolved rather than only l-resolved LDOS.
- <b>Vplot\_PDOS.py</b>: Uses DOSCAR and PROCAR to plot lm-decomposed LDOS in multiple panels. By identifying the point group of the material, it can by default group and plot degenerate orbital components, such as t2g and eg in cubic symmetry.
- Vplot\_TDOS.py
- Vplot\_VDEI.py
- Vplot\_VEE.py
- Vplot\_VEI.py
- <b>Vplot\_band.py</b>: Plots calculated band dispersion (E–k) using EIGENVAL. It accounts for Brillouin-zone path lengths to scale the horizontal axis correctly. Some band plotting tools join bands with lines, but VASP does not determine the irreducible representations required to identify band connectivity, so joining them can be physically misleading. This tool deliberately plots points rather than lines. The result may look less attractive but represents the VASP data without implying unverified connectivity. Options include combined or separate spin plots, plotting modes, and band indices. See the program help (-h). My Perl version also supports noncollinear magnetism and spin–orbit coupling; the Python version does not yet. Contact me if you need the Perl version.
- <b>Vplot\_com.py</b>: Plots E–k band dispersion using not only EIGENVAL but also PROCAR to visualize the wavefunction components making up each band. Point size or continuously graded color indicates the magnitude of selected projections, making it easier to identify the orbital character of bands. Brillouin-zone path lengths are adjusted correctly. As in Vplot\_band.py, bands are plotted as points rather than joined lines to avoid physically misleading connectivity. Includes options for combined or separate spins, plotting modes, and band indices; see help (-h). Compared with my Perl version, it lacks noncollinear and spin–orbit support, but its visualization is more polished.
- Vplot\_temperature.py
- <b>VrotPOSCAR.py</b>: Rotates POSCAR by Euler angles (alpha, beta, gamma), using the z–y–z convention defined on page 121 of *Applied Group Theory*. Useful when, for example, an applied electric field requires a particular orientation of crystal axes. After rotation, check kx, ky, kz in KPOINTS when a vacuum region is present.
- Vtdos.py
- Vtemp.py
- Vvasp2xyz.py
- Vxdat2MD.py
- Vxml2CONTCAR\_ALL.py
- Vxml2MD.py
- <b>Vxml2POSCAR.py</b>: Extracts the original POSCAR structure used in a calculation from VASP's XML output, vasprun.xml. Since vasprun.xml contains almost all calculation results, it is surprisingly useful when an appropriate reader class is available.
- vLDOSm\_3d.py
- vLDOSm\_4d.py
- vLDOSmulti.py
- vLDOSs.py

#### for WIEN2k
- WchkEparm.py
- Wgeteparm.py
- Wgeteph.py
- Wgetepl.py
- Wldos.py
- Wplot\_ADOS.py
- Wplot\_ADOS\_portrait.py
- Wplot\_LDOS.py
- Wplot\_LDOS\_portrait.py
- Wplot\_LDOSm.py
- Wplot\_TDOS.py
- Wplot\_XAS.py
- Wstruct2vasp.py
- Wvasp2struct.py
- wLCOS\_core.py
- wLDOS\_core.py
- wLDOSm\_3d.py
- wLDOSm\_4d.py
- wXAS.py
- wfch\_XAS.py

## Release Notes

### Reorganization and Verification in 0.1.0

This release reorganizes and extends the existing class structure, separating namespaces by calculation code. It does not rewrite structure-conversion or analysis algorithms. The criterion is that identical inputs should produce the same results and generated artifacts as before. Where incremental additions had caused mismatches in names, arguments, or return-value handling, connections were repaired to match the original implementation of the called code.

Comparing the actual 0.0.x sources stored in OLD, 890 of 904 method bodies matched after normalizing namespaces, imports, and additions of `self` to standalone functions. The remaining 14 concern bytes/str boundaries for element symbols, allocated sizes and return-value connections for supercell generation, attribute names, dynamic imports, references in type checks, and GUI connections to existing conversion routines. Actual differences are documented in [Method Differences](docs/method-differences.txt). This source comparison alone cannot establish identical results for all inputs; numerical and generated-file comparisons were also performed.

On Python 3.12.11, **1,188 tests passed**: 899 arithmetic-expression comparisons against a previously saved porting snapshot, 260 class-connection checks, 13 comparisons of numerical results and artifacts with the preserved old version, 11 existing connection repairs and related checks, and 5 checks covering preservation of documentation, comments, and data, plus GUI-related behavior. Arithmetic-expression comparisons and the full-method comparison against the current OLD source are separate checks. On Python 3.7.9, syntax was verified for 348 source, example, and test files, and empty instances of 11 central classes were successfully constructed. In an environment where the old package could not be imported, loading implementation modules from the wheel, VASP conversion, and FDMNES input generation were also verified.

Source explanations and historical notes have been retained. A comparison of 23,666 comment tokens across 342 files confirmed preservation, and no class or method docstrings were lost after ignoring indentation and surrounding whitespace. This is why some comments retain old names and historical usage instructions. The correspondence between original and ported files, and data hashes, are in the [Migration Inventory](docs/migration-inventory.json); previous settings, package initialization explanations, and historical documents are in [docs/history](docs/history/README.md). This README likewise retains historical tool descriptions and development background while integrating 0.1.0 usage instructions into the relevant sections.

Not all 197 commands, calculation codes, formats, or real-world datasets have been executed. Actual GUI display and the complete numerical workflow on Python 3.7 remain unverified. Some routines retain their historical exit behavior or unimplemented methods; these are not considered evidence of problems in their formulas or algorithms. For details of results and scope, see [Validation Records](docs/validation.md), [Migration Audit](docs/release-audit.md), and the version-by-version [CHANGELOG](CHANGELOG.md).

## Features

<p>At present, the main functionality is converting input and output among calculation codes. Structural conversion, for example, includes not only converting crystal or molecular structures to a code's required format but also translating the other input settings needed to run a calculation. The guiding aim is that once working input files have been prepared for one calculation code, they can be used with another without manual editing. One objective is to absorb differences among calculation codes as far as possible and provide unified handling of their inputs and outputs. Naturally, fundamental algorithmic differences sometimes make equivalent treatment impossible. In such cases, I simplify the process by supplying default parameters based, to some extent, on my own subjective recommendations; detailed configuration remains possible. Some specialized functions deliberately cannot be unified, but they can still be operated through largely consistent procedures. The framework offers a common operating environment not only for input structures but also for calculated results and electronic-structure analysis. Its extensive analysis capabilities are a particular feature.

### Framework

<p>Intermediate files are avoided wherever possible. Processing is unified within a Python object-oriented (OOP) framework. One could instead build an integrated environment from small programs communicating through intermediate files, but this project favors OOP to reduce development effort and unify processing. For example, conversion of structures between different calculation programs can be accomplished in just two lines of code, a considerable advantage.

Version 0.1.0 retains this unified OOP approach. While preserving the existing groupings of data and methods, the namespace layout now makes it possible to find VASP-related classes under `sae.vasp` and FDMNES-related classes under `sae.fdmnes`. For the distinction between classes handling individual files and classes holding them at the calculation-code level, see “Classes and Internal Structure” above.

In Professor Kotani's more elegant phrasing, one could call this the design of <B>“a dedicated language for computation.”</B>

For end users, the framework itself probably matters very little; what matters in practice is the collection of tools I develop using it. I do not currently recommend that third parties develop against this framework, since its design has changed direction repeatedly. Unless there is a special reason, developing with the established ASE framework is likely far more productive.

Whatever redesign the framework undergoes, I intend to preserve the interfaces of the end-user tools so their usability remains essentially unchanged.

### Support for Less-Common Codes and Analyses

<p>A practical distinguishing feature is support for some less-common Japanese calculation codes, reverse Monte Carlo codes, and less-common plane-wave analysis outputs such as pCOHP through tools including LOBSTER. I believe support for RMC\_POT may have been a first, and pCOHP support in a Python framework possibly also a first. Including FDMNES in an integrated environment, rather than a method-specific package, may likewise have been unprecedented. Since FDMNES has not been especially widespread in Japan's XANES community, I hope this framework also encourages its adoption. There seem to be very few frameworks enabling flexible conversion between VASP and other codes and FDMNES. XANES receives particular emphasis and should be useful to researchers in that field. With the exception of OpenMX and RMC\_POT, all supported first-principles codes can calculate XANES spectra; in that sense this can also be called an <b>XANES spectrum calculation framework</b>. Indeed, XANES analysis is essentially the main professional motivation for the current development. Although that objective has not yet been fully realized, the tools are already reasonably convenient.

### Analysis Support

<p>Beyond standard analyses such as charge density, LDOS, band dispersion, Bader charges, XANES spectra, and pCOHP, the package provides numerous tools for analyzing and plotting different calculations and preparing their inputs. I suspect its analysis-log parsing and plotting functions may be more extensive than ASE's. Developing analysis-support functions is now the author's primary motivation.

### Structure-Building Support

<p>Functions include supercell generation, coordination-number and bond searches, coordinate modifications such as translation and rotation of selected local structures, surface generation, and creation of vacuum regions. There are quite a few supporting classes and functions, but they are not yet especially sophisticated and remain incomplete. Unlike ASE, this framework cannot automatically generate nanoparticles or nanotubes.

### 2D Plotting

<p>2D plotting mainly uses matplotlib and supports PDF/EPS output. Many templates implement routine analyses such as LDOS and band calculations, making it straightforward to automate production of publication-ready figures. Script-driven execution and routine automation are assumed; little effort has gone into GUI development. Band plots can visualize wavefunction components directly on E–k plots through continuously varying colors or point sizes. An unusual feature is conversion of results from multiple calculation codes to the XML format used by p4vasp, a common VASP visualization program. I believe both the idea and implementation of such forced p4vasp conversion may have been firsts. For example, OpenMX MD results in XYZ format can readily be animated in p4vasp. Many tools support XCrySDen, but this project prioritized p4vasp and does not yet support XCrySDen. Support for Professor Oguchi's PSP format is quietly progressing, although direct PDF output through matplotlib is currently a sounder and more convenient approach.

### 3D Plotting

Version 0.1.0 groups the previous `CrystalMaker` and unit-cell drawing routines under `sae.gui`. The rendering mechanism itself has not changed; see “Required Python and Modules” for the necessary `visual` and `wx` environment.

<p>3D plotting and the GUI are mostly experimental additions still in functional testing. They mainly use VPython and wxPython, indirectly relying on OpenGL. I am considering using OpenGL through VTK or directly to gain more flexibility in 3D visualization and GUI design. Some functionality is still being prepared, and I consider this an important future pillar of analysis support. In practice, however, there is only one developer working on this as a side project, so implementation lags far behind the plans. A reasonably useful 3D visualization of Bader analysis results has been implemented, including supercell support. For other purposes, visualization with VESTA or p4vasp is currently preferable.

## Development History and Current Status

<p>The project grew from many independent AWK, Perl, and C programs for conversion, plotting, and analysis that I wrote gradually over roughly 15 years, from graduate school through my postdoctoral period. I tried, as far as possible, to give these programs similar interfaces and complementary functionality. As the number of supported calculation codes and the overall codebase grew, however, development as a coherent whole began to break down. I therefore began porting the tools to Python for my own convenience and enjoyment, implementing the framework independently.

<p>Framework development solves many of these maintenance problems. Readers familiar with ASE may recognize similarities; in terms of functionality, this project can be regarded as a budget version of ASE. Basic operations such as reading and writing structures from reader classes, and calling functionality as functions or methods, resemble ASE. Instance creation and the multiparadigm approach are natural patterns of Python frameworks generally, not necessarily imitation of ASE. In that sense, the similarities are a natural consequence of Python OOP. (Indeed, my impression is that ASE itself relies heavily on functions rather than class/method/inheritance-based OOP procedures.) The internal architecture is entirely different. Still, the basic functionality is currently much more limited than ASE's and may look rather modest. When development began, I did not know ASE well. Looking back, ASE is by far the leading, industry-standard Python framework for integrated computational workflows; in Europe and the United States, many first-principles codes are expected to support it. There is probably little need for an equivalent alternative. Developing a similar independent framework may have involved wasted effort, but independent development has its own benefits.

<p>Its significance, above all, is that it is my own code for my own convenience, which gives it value distinct from ASE. Providing a <b>development environment</b> for quickly implementing functions I need is the central purpose. A distinguishing point is support for less-common Japanese codes and analyses not covered by ASE. I have also developed many utilities, including visualization tools. From a user's perspective, these bundled tools may be more valuable than the framework itself.

<p>Professor Kotani also developed a Python framework called XtalEdit, probably with better support for Japanese codes, although development seems to have stalled. Unlike my analysis-centered approach, XtalEdit focuses on group-theoretical structure generation; ASE naturally provides similar functionality. Integrated Python simulation frameworks may inevitably end up following the older ASE and becoming simplified versions of it. Unless motivated by personal satisfaction, computational physicists might be better off not writing such frameworks themselves. For support of less-common codes and functions, contributing to ASE or branching from it may be healthier.

<p>If the goal is Japanese-code support with a GUI, C-Tools, promoted by communities such as CMSI and included in MateriAppsLive, may be appropriate. Its GUI is relatively simple and its features still basic, but it meets many minimum needs, including structural conversion for less-common Japanese codes. Professor Kotani's XtalEdit, although no longer actively developed, also has a Java UI. Either may be useful. The GUI in this framework currently falls short of these tools, and there is little intention to catch up.

### Current Limitations and Unsupported Features

<p>Many older analysis and calculation-support tools written in AWK, Perl, and C have not been ported at all, particularly support for KANSAI-92, LmtART, Mark's LMTO, and FHI-AIMS. Since I have not used those codes recently, I currently have no plans to support them. Even for VASP, only some of the old functionality has been implemented. HiLAPW support, for example, has barely progressed beyond basic structural conversion; I have not used HiLAPW in six or seven years.

<p>The greatest problem is that my design policy for the integrated framework continues to change. My limited skills and their evolution, particularly my growing understanding of OOP design, have not been matched by sufficient refactoring. Without proper refactoring soon, development risks becoming unmanageable. The framework and tools contain roughly 50,000 lines of code, and maintenance is becoming difficult. I would like to carry out substantial refactoring and simplify the codebase, but the number of supported codes and functions is still increasing, and development cannot keep pace.

To organize these successive additions, version 0.1.0 reorganized namespaces and internal call relationships on the basis of existing classes. This work is separate from adding calculation codes or changing analysis methods; the immediate priority is to make existing processing easier to understand and maintain.

### Name

<p>The framework is currently called StructureAnalysisEnvironment (SAE), a name I chose before learning of ASE (Atomic Simulation Environment). In retrospect, I think this name is <B>unacceptable</B>, since even I confuse it with ASE. I plan to change it eventually, but lacking a better idea it may remain. Recently I have tended to abbreviate it SAEnv rather than SAE.

### ASE Modules and CIF Support

<p>Unfortunately, some limited group-theoretical functionality currently uses ASE modules. As I become more familiar with ASE, the value of my own framework can seem questionable, but independent implementations of some of these functions are progressing and I intend eventually to remove ASE dependencies from the core framework. Time is limited, however, and ASE currently works perfectly well, which makes replacing it hard to prioritize. The framework also cannot directly read and write CIF files. I am undecided whether to rely on ASE, PyCifRW, or a partial independent implementation. CIF conversion utilities using ASE are already bundled among the tools, so this is not a major practical problem for users. For general CIF conversion, [cif2cell](http://sourceforge.net/projects/cif2cell/) is probably ahead in supported formats, convenience, and recognition; it also uses PyCifRW rather than implementing CIF parsing independently. In practice, passing CIF files through VESTA handles most cases, so my motivation is admittedly limited, but seamless support remains important.

### Future Plans

<p>I intend to expand <b>group-theoretical functionality</b> and use it as a foundation for band unfolding. This was originally planned as a flagship feature, but finding the existing [unfolding](http://www.ifm.liu.se/theomod/compphys/band-unfolding/) code reduced my motivation, since it already implements much of what I had intended. The foundational framework grew far beyond expectations and continues to expand, so work on unfolding itself has stopped. Existing unfolding tools involve cumbersome procedures, however, and even a convenient wrapper could be valuable for analysis. I am considering that direction. Since developing a <b>platform for developing analysis methods</b> is a central goal, improved group theory remains essential. Naturally, a foundation alone is not enough; practical tools must continue to be built around it.

I consider it important to develop analysis and structure-building tools that are not tied to particular calculation codes. Even reconstructing core-electron information from PAW wavefunctions is not something I am eager to implement in Fortran now. I want to eliminate code-specific dependencies from peripheral processing as much as possible.

With ASE already available, the main opportunities for originality and usefulness in this kind of project are probably <b>support for less-common calculation codes</b>, <b>original analysis functions</b>, and <b>better GUI functionality</b>. I expect to continue expanding the first two, including original implementations. I will add GUI functionality when necessary, but it will probably remain relatively minimal. Partly as a hobby, I am also developing cross-platform interfaces with wxPython and wxWidgets, including native GUIs in C++ as well as Python.

How much effort goes into each area remains to be seen. Unfortunately, I may be moving away from work involving numerical calculations for a while, so development may not progress very quickly.
