#!/bin/bash

if [ -f t ]; then #Preden začnem znova, pobriši vse datoteke od prej
    rm t
fi

cls="knn"

for coding in "bin" "real"; do
    #echo "Coding: $coding"
    for alg in "de" "abc" "pso" "ga"; do
        #echo "Algorithm: $alg"
        for database in "adult" "breast-cancer" "credit-approval" "gas" "german" "ionosphere" "libras" "sonar" "lymph" "mushroom" "optic" "semeion" "spect" "splice" "vehicle"; do
            #echo "Database: $database"
            for type in "filter" "wrapper"; do
                #echo "Type: $type"
                if [ ! -f results/$coding-$alg-$cls-$database-$type.dat ] || [ $(cat results/$coding-$alg-$cls-$database-$type.dat| grep "Overall" | wc -l) -lt 1 ]; then
                    echo "mising experiment $coding-$alg-$cls-$database-$type.dat"
                    break
                fi

                lower=$(cat results/$coding-$alg-$cls-$database-$type.dat | grep -n "Classification" | sed 's/:/\ /g' | awk '{print $1}')
                upper=$(cat results/$coding-$alg-$cls-$database-$type.dat | grep -n "Overall" | sed 's/:/\ /g' | awk '{print $1}')
                #echo $lower 
                cat results/$coding-$alg-$cls-$database-$type.dat | sed -n "$((lower+1)),$((upper-1)) p" | sed 's/\[//g'| sed 's/\]//g' | sed 's/,//g' > t
                #cat t
                
                ClassifAccuracyAllRuns=$(cat t | awk '{print $1}' | xargs | sed 's/^/c(/g'| sed 's/$/)/g' | sed 's/\ /,/g')
                NumFeaturesAllRuns=$(cat t | awk '{print $2}' | xargs | sed 's/^/c(/g'| sed 's/$/)/g' | sed 's/\ /,/g')
                #echo $ClassifAccuracyAllRuns
                #echo $NumFeaturesAllRuns
                

                featureStats=$(echo "summary($NumFeaturesAllRuns)" | R --vanilla --quiet)  
                featureStats=$(echo $featureStats | awk '{print $11" "$13" "$14" "$16}')   
                #echo $featureStats

                ClassifStats=$(echo "summary($ClassifAccuracyAllRuns)" | R --vanilla --quiet)
                ClassifStats=$(echo $ClassifStats | awk '{print $11" "$13" "$14" "$16}')      
                #echo $ClassifStats
                
                #echo "tukaj $ClassifAccuracyAllRuns"
                sdAccuracy=$(echo "sd($ClassifAccuracyAllRuns)" | R --vanilla --quiet)
                sdAccuracy=$(echo $sdAccuracy | awk '{print $4}')

                sdFeatures=$(echo "sd($NumFeaturesAllRuns)" | R --vanilla --quiet)
                
                sdFeatures=$(echo $sdFeatures | awk '{print $4}')
                
                #echo "$coding $cls $alg $database $(echo $ClassifStats | awk '{print $3}') $sdAccuracy $(echo $featureStats | awk '{print $3}') $sdFeatures"
                echo "$type $coding $cls alg-$alg $database $ClassifStats $sdAccuracy $featureStats $sdFeatures"
                
                #min median mean max sd
                #echo $ClassifStats $featureStats
                #exit
            done
            rm t
        done #| xargs | sed 's/\ /\n/g'> $coding-$alg.res
    done #| xargs | sed 's/\ /\n/g' > $coding.res
done


