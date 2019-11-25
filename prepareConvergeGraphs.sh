if [ $# -lt 2 ]; then
    echo "EXAMPLE: ./prepareConvergenceGraphs.sh [algorithm] [dataset] [coding] [type]"
    exit 1
fi


alg=$1
dataset=$2
coding=$3
cls="knn"

type=$4

path="drawData"




if [ -f avgFit.dat ]; then
    rm avgFit.dat
fi

if [ -f avgFeats.dat ]; then
    rm avgFeats.dat
fi

touch avgFit.dat avgFeats.dat

if [ $dataset == "all" ]; then
    for dat in "adult" "breast-cancer" "credit-approval" "gas" "german" "ionosphere" "libras" "sonar" "lymph" "mushroom" "optic" "semeion" "spect" "splice" "vehicle"; do
        for run in `seq 1 30`; do 
            cat "converge/$dat-$alg-$coding-42-30-$cls-$type-$run.conv" | awk '{print $2}' | tail -n +2 > tmp1.dat                       
            cat "converge/$dat-$alg-$coding-42-30-$cls-$type-$run.conv" | awk '{print $3}' | tail -n +2 > tmp2.dat      
            paste avgFit.dat tmp1.dat > tmp.dat && mv tmp.dat avgFit.dat
            paste avgFeats.dat tmp2.dat > tmp.dat && mv tmp.dat avgFeats.dat
            
        done
    done
    cat avgFit.dat | sed 's/\t/,/g' | sed 's/^,//g' > tmp.dat && mv tmp.dat avgFit.dat
    cat avgFeats.dat | sed 's/\t/,/g' | sed 's/^,//g' > tmp.dat && mv tmp.dat avgFeats.dat
    mv avgFit.dat "$path/converge-obj-$alg-$coding-all-$cls-$type.dat"
    mv avgFeats.dat "$path/converge-feats-$alg-$coding-all-$cls-$type.dat"

    python prepareConvergeGraphs.py "$path/converge-obj-$alg-$coding-all-$cls-$type.dat" > "$path/converge-obj-$alg-$coding-all-$cls-$type-processed.dat"
    python prepareConvergeGraphs.py "$path/converge-feats-$alg-$coding-all-$cls-$type.dat" > "$path/converge-feats-$alg-$coding-all-$cls-$type-processed.dat"

else
    for run in `seq 1 30`; do 
        cat "converge/$dataset-$alg-$coding-42-30-$cls-$type-$run.conv" | awk '{print $2}' | tail -n +2 > tmp1.dat                       
        cat "converge/$dataset-$alg-$coding-42-30-$cls-$type-$run.conv" | awk '{print $3}' | tail -n +2 > tmp2.dat
        paste avgFit.dat tmp1.dat > tmp.dat && mv tmp.dat avgFit.dat
        paste avgFeats.dat tmp2.dat > tmp.dat && mv tmp.dat avgFeats.dat           
    done
    cat avgFit.dat | sed 's/\t/,/g' | sed 's/^,//g' > tmp.dat && mv tmp.dat avgFit.dat
    cat avgFeats.dat | sed 's/\t/,/g' | sed 's/^,//g' > tmp.dat && mv tmp.dat avgFeats.dat
    mv avgFit.dat "$path/converge-obj-$alg-$coding-$dataset-$cls-$type.dat" 
    mv avgFeats.dat "$path/converge-feats-$alg-$coding-$dataset-$cls-$type.dat"

    python prepareConvergeGraphs.py "$path/converge-obj-$alg-$coding-$dataset-$cls-$type.dat" > "$path/converge-obj-$alg-$coding-$dataset-$cls-$type-processed.dat"
    python prepareConvergeGraphs.py "$path/converge-feats-$alg-$coding-$dataset-$cls-$type.dat" > "$path/converge-feats-$alg-$coding-$dataset-$cls-$type-processed.dat"    

fi
