#!/usr/bin/env bash

run_comb_check() {
    N=$1
    P=$2
    echo "N={$N}, P={$P}:\n"
    time python hw1cs561f2018.py $N $P
}

N=2
P=1
while [ "$N" != 4 ]
do
    while [ "$P" <= "$N" ]
    do
        run_comb_check $N $P
        P=$(($P+1))
    done
    N=$(($N+1))
done