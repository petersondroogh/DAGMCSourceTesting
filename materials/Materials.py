# name: Material.py
# date: 04 Nov 16
# auth: Zach Hartwig
# mail: hartwig@psfc.mit.edu
#
# desc: Python script that generates a PyNE HDF5 formatted binary file
#       that creates a complete materials library for DAGMC neutronics
#       calculations. Materials are taken from a dummy MCNP input deck.

# MCNP cross section library identifier
fendl3 = "30c"

# Flag for verbose output
verbose = True

# Set the input (MCNP) and output (HDF5) file names
input_mcnp_file = "Materials.mcnp"
output_hdf5_file = "Materials.h5m"


##################
# Module imports #
##################

import os
from pyne.material import MaterialLibrary
from pyne import mcnp as pyne_mcnp
from pyne.nucname import mcnp as nucname_mcnp 


#############
# Functions #
#############

# Function to set the MCNP isotopic cross section data library for a
# material. With this function, all isotopes of the material are
# assigned the same cross section library identifier

def set_xs_library(material, xs_identifier):

    # Empty dictionary
    table_ids = {}

    # Iterate through each isotope in the material and assigned it the
    # cross section library identifier
    for key in material:
        zaid = str(key)
        table_ids.update({str(nucname_mcnp(zaid)) : xs_identifier})
    material.metadata["table_ids"] = table_ids

    # Optionally output material information
    if(verbose):
        print material
        print material.mcnp()

    # Return the material
    return material


##############################
# Import materials from MCNP #
##############################

mat = pyne_mcnp.mats_from_inp(input_mcnp_file)


###################################
# Update materials for PyNE/DAGMC #
###################################

# Add necessary data to the MCNP materials

mat[1].density = 8.9
mat[1].metadata = {"name":"CuCrZr","density_unit":"g/cm3"}
mat[1] = set_xs_library(mat[1], fendl3)

# Remove the pre-existing library file
os.system('rm Materials.h5m -f')

# Create a PyNE materials library object
mat_lib = MaterialLibrary(mat)

# Write the PyNE materials library to an HDF5 file for use in
# DAGMC. Note that the datapath and nucpath must have the fixed
# directory structure in order for DAGMC to find the materials
mat_lib.write_hdf5(output_hdf5_file,
                   datapath='/materials',
                   nucpath='/nucid')
