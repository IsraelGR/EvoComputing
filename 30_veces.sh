#!/bin/bash
echo -e "Aptitud" "\t\t|X1" "\t\t\t|X2" "\t\t\t|X3" "\t\t\t|X4" "\t\t\t|X5" >> Praxis_8.txt
echo "------------------------|-----------------------|-----------------------|-----------------------|-----------------------|-----------------------" >> Praxis_8.txt
#echo -e "Aptitud" "\t\t|X1" "\t\t\t|X2" >> Praxis_8.txt
#echo "------------------------|-----------------------|-----------------------" >> Praxis_8.txt
for i in `seq 1 30`;
    do
        echo Corrida No. $i
        echo Corrida No. $i >> Praxis_8.txt
        python genetisch.py >> Praxis_8.txt
        echo -e "\n" >> Praxis_8.txt
    done

    cat Praxis_8.txt
