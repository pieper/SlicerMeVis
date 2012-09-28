isEmpty(Slicer_General_PRI_INCLUDED) {
  message ( loading Slicer_General.pri )
}
# **InsertLicense** code
# -----------------------------------------------------------------------------
# Slicer_General prifile
#
# \file    Slicer_General.pri
# \author  Steve Pieper
# \date    2012-09-26
#
# 
#
# -----------------------------------------------------------------------------

# include guard against multiple inclusion
isEmpty(Slicer_General_PRI_INCLUDED) {

Slicer_General_PRI_INCLUDED = 1

# -- System -------------------------------------------------------------

include( $(MLAB_MeVis_Foundation)/Configuration/SystemInit.pri )

# -- Define local PACKAGE variables -------------------------------------

PACKAGE_ROOT    = $$(MLAB_Slicer_General)
PACKAGE_SOURCES = "$$(MLAB_Slicer_General)"/Sources

# Add package library path
LIBS          += -L"$${PACKAGE_ROOT}"/lib

# -- Projects -------------------------------------------------------------

# NOTE: Add projects below to make them available to other projects via the CONFIG mechanism

# You can use this example template for typical projects:
#MLMyProject {
#  CONFIG_FOUND += MLMyProject
#  INCLUDEPATH += $${PACKAGE_SOURCES}/ML/MLMyProject
#  win32:LIBS += MLMyProject$${d}.lib
#  unix:LIBS += -lMLMyProject$${d}
#}

# -- ML Projects -------------------------------------------------------------

# -- Inventor Projects -------------------------------------------------------

# -- Shared Projects ---------------------------------------------------------

# End of projects ------------------------------------------------------------

}