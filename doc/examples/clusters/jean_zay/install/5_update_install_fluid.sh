#!/bin/bash
set -e

cd $WORK/Dev/fluiddyn
hg pull
hg up cluster-jean-zay # cluster-jean-zay should be replaced by default when merged
make clean
pip install -e .

# TODO: Remove the line with transonic when fix-bug-mpi-barrier-jean-zay is merged
cd $WORK/Dev/transonic
hg pull
hg up fix-bug-mpi-barrier-jean-zay
make clean
pip install -e .

cd $WORK/Dev/fluidfft
hg pull
hg up default
# pip install -e .   seems to run something with mpi, which is forbidden
python setup.py develop
# TODO: QUESTION for Vincent: does this work for fluidfft?
# pip install -e . --no-build-isolation

cd $WORK/Dev/fluidsim
make cleanall
# --no-build-isolation to use pythran already installed in the environment
pip install -e . --no-build-isolation
pytest fluidsim

cd doc/examples/clusters/jean_zay/
