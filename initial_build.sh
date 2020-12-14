#!/bin/bash

source setup.sh

# Get globes:
wget https://www.mpi-hd.mpg.de/personalhomes/globes/download/globes-3.2.16.tar.gz
tar xfvz globes-3.2.16.tar.gz
cd globes-3.2.16
# Stupid hack to get this to compile on macosx
sed -i -e '718d;719d;720d' lib/stdio.in.h
./configure --prefix=${GLOBES_BUILD_DIR}
make install
cd -

# Get DUNE CDR globes configuration:
curl https://arxiv.org/src/1606.09550v1 --output arXiv-1606-09550v1.tar.gz
mkdir arXiv-1606-09550v1
tar xfvz arXiv-1606-09550v1.tar.gz -C arXiv-1606-09550v1
ln -s arXiv-1606-09550v1/anc/anc_files/DUNE_GLoBES_Configs/* .

# Build globes executable
make
