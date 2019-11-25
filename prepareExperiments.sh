#!/bin/bash



    for cls in "knn"; do
        for coding in "bin" "real"; do
            for alg in "de" "abc" "pso" "ga"; do
                for database in "adult" "breast-cancer" "credit-approval" "gas" "vehicle" "semeion" "ionosphere" "german" "libras" "lymph" "mushroom" "optic" "sonar" "spect" "splice"; do
                    for evaltype in "wrapper"; do
                        echo "\"./run.py -np 30 -maxg 100 -algorithm $alg -seed 42 -learn Data/weka-discrete/$database-train-processed.arff -test Data/weka-discrete/$database-test-processed.arff -coding $coding -jsonfile json/$database -classifier $cls -evaltype $evaltype > results/$coding-$alg-$cls-$database-$evaltype.dat\""                    
                    done
                done
            done
        done
    done

#python run.py -learn Data/weka-discrete/breast-cancer-train-processed.arff -test Data/weka-discrete/breast-cancer-test-processed.arff -np 10 -maxg 500 -algorithm de -coding real -classifier knn -evaltype filter -jsonfile data.json
