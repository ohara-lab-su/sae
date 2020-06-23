
try:
    from copyright import *
except Exception:
    from StructureAnalysisEnvironment.copyright import *

#
# general class
#
from .Read import *

#
# class for VASP (+alpha)
#
from .vasp import *
# from .vasp.ReadVaspOutcar import *
# from .vasp.ReadVaspDoscar import *
# from .vasp.ReadVaspXdat import *
# from .vasp.ReadVaspVasprun import *
# from .vasp.ReadVaspOszicar import *
# from .vasp.ReadVaspEigenval import *
# from .vasp.ReadVaspKpoints import *
# from .vasp.ReadVaspSymdat import *
# from .vasp.ReadVaspProcar import *
# from .vasp.ReadVaspPoscar import *
# from .vasp.ReadVaspIncar import *
# from .vasp.ReadVaspAcf import *
# from .vasp.ReadVaspPotcar import *
# from .vasp.ReadVaspChgcar import *

#
# LOBSTER,COHP for VASP
#
from .lob import *
# from .lob.ReadLobCohp import *
# from .lob.ReadLobDos import *
# from .lob.ReadLobOut import *

#
# class for OpenMX
#
from .mx import *
# from .mx.ReadMd import *
# from .mx.ReadMxVps import *
# from .mx.ReadMxVpsList import *
#
# from .mx.ReadMxDatMethod import *
# from .mx.ReadMxDat import *
# from .mx.ReadMxOut import *
# from .mx.ReadMxDftscf import *
# from .mx.ReadMxDosMethod import *
# from .mx.ReadMxTdos import *
# from .mx.ReadMxPdos import *

#
# class for WIEN2k
#
from .wien2k import *
# from .wien2k.ReadWienDos import *
# from .wien2k.ReadWienOutput0 import *
# from .wien2k.ReadWienOutputt import *
# from .wien2k.ReadWienXspec import *
# from .wien2k.ReadWienTxspec import *
# from .wien2k.ReadWienScf import *

#
# class for HiLAPW
#
from .hilapw import *
# from .hilapw.ReadHiSets import *

#
# class for PWScf (Quantum ESPRESSO)
#
from .pwscf import *
# from .pwscf.ReadPwIn import *
# from .pwscf.ReadPwOut import *
# from .pwscf.ReadPwTdos import *
# from .pwscf.ReadPwPdos import *
# from .pwscf.ReadPwXanes import *

#
# class for FDMNES
#
from .fdm import *

# from .fdm.ReadFdmTxt import *
# from .fdm.ReadFdmConv import *
# from .fdm.ReadFdmInp import *
# from .fdm.ReadFdmBav import *
# from .fdm.ReadFdmSd import *
# from .fdm.ReadFdmFdmfile import *

#
# class for RMC
#
from .rmc import *
#from .rmc.ReadRmcpotCfg import *

#
# class for Athena
from .athena import *
# from .athena.ReadAthenaNor import *

#
# class for PF format
#
from .pf import *
# from .pf.ReadPfformat import *

