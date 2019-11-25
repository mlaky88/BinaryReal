if [ $# -lt 2 ]; then
    echo "EXAMPLE: ./mergeConvergePlots.sh [dataset] [coding] [type]"
    exit 1
fi


dataset=$1
coding=$2
cls="knn"
type=$3

path="drawData"

touch drawobj.dat drawfeats.dat
for alg in "de" "pso" "abc" "ga"; do
    if [ ! -f "$path/converge-obj-$alg-$coding-$dataset-$cls-$type-processed.dat" ]; then
        echo "Results for algorithm $alg is missing"
        echo "Missing file: converge-obj-$alg-$coding-$dataset-$cls-$type-processed.dat"
        echo "Running ./prepareConvergeGraphs with appropriate settings"
        ./prepareConvergeGraphs.sh $alg $dataset $coding $type

        #rm drawobj.dat drawfeats.dat
        #exit 
    fi
    paste drawobj.dat "$path/converge-obj-$alg-$coding-$dataset-$cls-$type-processed.dat" > tmp1.dat && mv tmp1.dat drawobj.dat
    paste drawfeats.dat "$path/converge-feats-$alg-$coding-$dataset-$cls-$type-processed.dat" > tmp1.dat && mv tmp1.dat drawfeats.dat
done


#now draw

cat drawobj.dat | sed 's/\t/,/g' | sed 's/^,//g' > tmp1.dat && mv tmp1.dat drawobj.dat
cat drawfeats.dat | sed 's/\t/,/g' | sed 's/^,//g' > tmp1.dat && mv tmp1.dat drawfeats.dat
python plotConvergeGraphs.py drawobj.dat obj $dataset $coding $type
python plotConvergeGraphs.py drawfeats.dat feats $dataset $coding $type
rm drawobj.dat drawfeats.dat



