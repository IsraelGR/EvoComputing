#!/bin/bash
echo -e "Aptitud" "\t\t|X1" "\t\t\t|X2" "\t\t\t|X3" "\t\t\t|X4" >> Praxis_2.txt
echo "------------------------|-----------------------|-----------------------|-----------------------|-------------------" >> Praxis_2.txt
#echo -e "Aptitud" "\t\t|X1" "\t\t\t|X2" >> Praxis_2.txt
#echo "------------------------|-----------------------|-----------------------" >> Praxis_2.txt
for i in `seq 1 30`;
    do
        echo Corrida No. $i >> Praxis_2.txt
        python genetisch.py >> Praxis_2.txt
        echo -e "\n" >> Praxis_2.txt
    done

    cat Praxis_2.txt
