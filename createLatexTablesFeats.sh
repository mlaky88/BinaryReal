#!/bin/bash

function determineBestFeats {
    binValue=$1
    realValue=$2
    binStd=$3
    realStd=$4

    local sign="<"
    if [ $(echo "$binValue < $realValue" | bc) == 1 ]; then              
            sign=">"
    elif [ $(echo "$binValue == $realValue" | bc) == 1 ]; then
        if [ $(echo "$binStd == $realStd" | bc) == 1 ]; then 
                sign="="
        elif [ $(echo "$binStd > $realStd" | bc) == 1 ]; then
            sign="<"
        else 
            sign=">"
        fi
    fi
    echo $sign
}

function determineBestCls {
    binValue=$1
    realValue=$2
    binStd=$3
    realStd=$4

    local sign=">"
    if [ $(echo "$binValue < $realValue" | bc) == 1 ]; then              
            sign="<"
    elif [ $(echo "$binValue == $realValue" | bc) == 1 ]; then
        if [ $(echo "$binStd == $realStd" | bc) == 1 ]; then 
                sign="="
        elif [ $(echo "$binStd > $realStd" | bc) == 1 ]; then
            sign=">"
        else 
            sign="<"
        fi
    fi
    echo $sign
}

#TEST1
binValue=1.0
realValue=1.0
binStd=0.0
realStd=0.0

binValueCls=0.0
realValueCls=1.0
binStdCls=0.0
realStdCls=0.0
#echo -n "TEST 1 $=$ "
feats=$(determineBestFeats $binValue $realValue $binStd $realStd)
cls=$(determineBestCls $binValueCls $realValueCls $binStdCls $realStdCls)
#echo "$feats $cls"


#TEST2
binValue=0.0
realValue=1.0
binStd=0.0
realStd=0.0
#echo -n "TEST 2 $>$ "
#determineBestFeats $binValue $realValue $binStd $realStd

#TEST3
binValue=1.0
realValue=0.0
binStd=0.0
realStd=0.0
#echo -n "TEST 3 $<$ "
#determineBestFeats $binValue $realValue $binStd $realStd

#TEST4
binValue=1.0
realValue=1.0
binStd=1.0
realStd=0.0
#echo -n "TEST 4 $<$ "
#determineBestFeats $binValue $realValue $binStd $realStd
#exit
#TEST5

#TEST5

#TEST6

if [ $# -lt 2 ]; then
    echo "EXAMPLE: ./createLatexTablesFeats.sh [type] [dataset] "
    exit 1
fi

type=$1
file="$2" #Preveri format

countBin=(0 0 0 0)
countReal=(0 0 0 0)
echo "\begin{table*}"
echo "\scriptsize"
echo "\centering"
echo "\caption{Comparison of feature subset reduction for binary and real-coded algorithms for $type-based feature selection.}"
echo "\label{tab:result-reduction-$type}"
echo "%\resizebox{45em}{!}{ "
echo "\setlength{\tabcolsep}{0.3em}"
echo "\begin{tabular}{>{\centering}m{1.3cm}|c>{\centering}m{0.3cm}c|c>{\centering}m{0.3cm}c|c>{\centering}m{0.3cm}c|c>{\centering}m{0.3cm}c|}"
echo "\cline{2-13}"
echo -n "\multirowcell{2}{}"
echo "& \multicolumn{3}{c|}{ABC} & \multicolumn{3}{c|}{DE} & \multicolumn{3}{c|}{GA} & \multicolumn{3}{c|}{PSO} \\\\ \cline{2-13}"
echo "& Binary && Real & Binary && Real & Binary && Real & Binary && Real \\\\ \hline"
for j in "adult" "breast-cancer" "credit-approval" "gas" "german" "ionosphere" "libras" "sonar" "lymph" "mushroom" "optic" "semeion" "spect" "splice" "vehicle"; do 
    k=0
    for i in "abc" "de" "ga" "pso"; do 
        if [ $i == "abc" ]; then
            p=$j
            echo -n "${p^} " >> outputVal 
        fi
        echo -n "$(cat $file | grep "alg-$i"     | grep bin  | grep $j | grep $type | awk '{print $8*100,$10" "}') " >> x
        echo -n "$(cat $file | grep "alg-$i"     | grep real | grep $j | grep $type | awk '{print $8*100,$10" "}') " >> x
        binValueCls=$(cat $file | grep "alg-$i"  | grep bin  | grep $j | grep $type | awk '{print $8}')
        realValueCls=$(cat $file | grep "alg-$i" | grep real | grep $j | grep $type | awk '{print $8}')


        binStdCls=$(cat $file | grep "alg-$i"    | grep bin  | grep $j | grep $type | awk '{print $10}')
        realStdCls=$(cat $file | grep "alg-$i"   | grep real | grep $j | grep $type | awk '{print $10}')

        binValue=$(cat $file | grep "alg-$i"     | grep bin  | grep $j | grep $type | awk '{print $13}')
        realValue=$(cat $file | grep "alg-$i"    | grep real | grep $j | grep $type | awk '{print $13}')
        binStd=$(cat $file | grep "alg-$i"       | grep bin  | grep $j | grep $type | awk '{print $15}')
        realStd=$(cat $file | grep "alg-$i"      | grep real | grep $j | grep $type | awk '{print $15}')
        
        
        feats=$(determineBestFeats $binValue $realValue $binStd $realStd)
        cls=$(determineBestCls $binValueCls $realValueCls $binStdCls $realStdCls)
        #if [ $feats = $cls ]; then
        #    feats="!"
        #    cls=""
        #fi
        #echo "CLS = $binValueCls $binStdCls || $realValueCls $realStdCls"
        #echo "FEATS = $binValue $binStd  || $realValue $realStd"
        #echo $cls $feats
        
        
        #cat $file | grep "alg-$i" | grep bin | grep "$disc" | grep $j |grep $classifier | awk -v s="$sign" '{printf("%.2f$\\pm$%.2f & \\multirowcell{2}{%s} & ",$6*100,$7,s);}' >> outputVal 
        #cat $file | grep "alg-$i" | grep real | grep "$disc" | grep $j |grep $classifier | awk '{printf("%.2f$\\pm$%.2f & ",$6*100,$7);}' >> outputVal

        cat $file | grep "alg-$i" | grep bin  | grep $j |grep $type | awk -v s1="$feats" -v s2="$cls" '{printf("%.2f$\\pm$%.2f & $%s%s$ & ",$13,$15,s1,s2);}' >> outputFeat
        cat $file | grep "alg-$i" | grep real | grep $j |grep $type | awk '{printf("%.2f$\\pm$%.2f & ",$13,$15);}' >> outputFeat
    done #|  xargs 

    max=$(cat x | awk '{for(j=1;j<=16;j+=2) printf(" %.2f ",$j);}' | sed 's/\  /\ /g' | sed 's/\ /\n/g' | sort -r | head -n 1)
    #echo $max
    cat outputVal  #| sed 's/\&\ $/\\\\/g'
    
    echo -n "&"    
    cat outputFeat  | sed 's/\&\ $/\\\\/g'
    #cat outputVal
    

    
    #cat output
    rm x outputVal outputFeat
    echo
    #exit
done 

echo "\hline"
#echo -n "Best "
#for i in `seq 0 3`; do
#    echo -n "& $(echo ${countBin[$i]}) && $(echo ${countReal[$i]}) "
#done
#echo "\\\\ \\hline"

echo "\end{tabular}%}"
echo "\end{table*}"

