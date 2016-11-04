#!/bin/bash
#
# name: prepareModel.sh
# date: 04 Nov 16
# auth: Zach Hartwig
# mail: hartwig@psfc.mit.edu
#
# desc: Bash script to automate preparation of the DAGMCSourceTesting
#       model. The steps include Cubit, post-Cubit faceting, making
#       the model watertight, and then UWUW processing for materials

# Run Cubit in batch with the prescripted journal file
cubit -batch -nographics -nojournal -information off DAGMCSourceTesting.jou

# Facet the geometry in pre-processing
dagmc_preproc DAGMCSourceTesting.sat -o DAGMCSourceTesting.h5m

# Make the model watertight (i.e. patch and seal entire model)
make_watertight DAGMCSourceTesting.h5m
mv DAGMCSourceTesting_zip.h5m DAGMCSourceTesting.h5m

# Incorporate pre-assigned materials from the Materials database
uwuw_preproc DAGMCSourceTesting.h5m -l Materials.h5m -o DAGMCSourceTesting.h5m
