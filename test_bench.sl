#!/bin/bash
#SBATCH --ntasks=1
#SBATCH --time=00:20:00
#SBATCH --out=HW1b.out

WORK_HOME=/auto/rcf-40/liangsiq/cs561
cd $WORK_HOME
source /usr/usc/python/2.7.6/setup.sh
python ./test_bench.py 
