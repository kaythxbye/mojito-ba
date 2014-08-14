#!/bin/sh

# test list
cd ../../openflow
cp list_chain.c udatapath/chain.c
make clean
make
sudo make install

cd ../mojito/eval
sudo ./test_executor.py -a "list"

# test bitvector
cd ../../openflow
cp bv_chain.c udatapath/chain.c
cp bv_nojit.c udatapath/bv_types.c
make clean
make
sudo make install

cd ../mojito/eval
sudo ./test_executor.py -a "simple_bv"

# test jit
cd ../../openflow
cp bv_chain.c udatapath/chain.c
cp bv_jit.c udatapath/bv_types.c
make clean
make
sudo make install

cd ../mojito/eval
sudo ./test_executor.py -a "jit"

