#!/bin/bash
if [ $# -lt 2 ]; then
    echo "EXAMPLE: ./createLatexTablesCls.sh [type] [dataset] "
    exit 1
fi
type=$1
file=$2

countBin=(0 0 0 0)
countReal=(0 0 0 0)

\caption{}
\label{}
%\resizebox{45em}{!}{ 
\setlength{\tabcolsep}{0.3em}



echo "\begin{table*}[!htb]"
echo "\scriptsize"
echo "\centering"
echo "\caption{Classification results for binary and real-value coded algorithms after applying $type-based feature selection, using the kNN classifier.}"
echo "\label{tab:result-$type-knn}"
echo "\resizebox{45em}{!}{ "
echo "\setlength{\tabcolsep}{0.3em}"
echo "\begin{tabular}{>{\centering}m{1.3cm}|c>{\centering}m{0.3cm}c|c>{\centering}m{0.3cm}c|c>{\centering}m{0.3cm}c|c>{\centering}m{0.3cm}c|}"
echo "\cline{2-13}"
echo -n "\multirowcell{2}{}"
echo "& \multicolumn{3}{c|}{ABC\$_{}$} & \multicolumn{3}{c|}{DE\$_{}$} & \multicolumn{3}{c|}{GA\$_{}$} & \multicolumn{3}{c|}{PSO\$_{}$} \\\\ \cline{2-13}"
echo "& Binary && Real & Binary && Real & Binary && Real & Binary && Real \\\\ \hline"
for j in "adult" "breast-cancer" "credit-approval" "gas" "german" "ionosphere" "libras" "sonar" "lymph" "mushroom" "optic" "semeion" "spect" "splice" "vehicle"; do 
    k=0
    for i in "abc" "de" "ga" "pso"; do 
        if [ $i == "abc" ]; then
            p=$j
            echo -n "${p^} & " >> output 
        fi
        #echo "Dataset $j algorithm $i with $classifier"
        echo -n "$(cat $file  | grep "alg-$i" | grep bin  | grep $j | grep $type | awk '{print $8*100,$10" "}') " >> x
        echo -n "$(cat $file  | grep "alg-$i" | grep real | grep $j | grep $type | awk '{print $8*100,$10" "}') " >> x
        binValue=$(cat $file  | grep "alg-$i" | grep bin  | grep $j | grep $type | awk '{print $8}')
        realValue=$(cat $file | grep "alg-$i" | grep real | grep $j | grep $type | awk '{print $8}')
        binStd=$(cat $file    | grep "alg-$i" | grep bin  | grep $j | grep $type | awk '{print $10}')
        realStd=$(cat $file   | grep "alg-$i" | grep real | grep $j | grep $type | awk '{print $10}')
        sign="$<$"
        #echo "$j"
        #echo "binvalue $binValue"
        #echo "realvalue $realValue"
        if [ $(echo "$binValue > $realValue" | bc) == 1 ]; then
            sign="$>$"
            v=$(echo $(($(echo ${countBin[$k]})+1)))
            countBin[$k]=$v
        elif [ $(echo "$binValue == $realValue" | bc) == 1 ]; then
            if [ $(echo "$binStd == $realStd" | bc) == 1 ]; then
                sign="$=$"
            elif [ $(echo "$binStd < $realStd" | bc) == 1 ]; then
                sign="$<$"
                v=$(echo $(($(echo ${countReal[$k]})+1)))
                countReal[$k]=$v
            else 
                sign="$>$"
                v=$(echo $(($(echo ${countBin[$k]})+1)))
                countBin[$k]=$v
                #echo "$i $j"
            fi
        else
            #echo "$i $j"
            v=$(echo $(($(echo ${countReal[$k]})+1)))
            countReal[$k]=$v
            
        fi
        ((k++))
        cat $file | grep "alg-$i" | grep bin  | grep $j |grep $type | awk -v s="$sign" '{printf("%.2f$\\pm$%.4f & %s & ",$8*100,$10,s);}' >> output 
        cat $file | grep "alg-$i" | grep real | grep $j |grep $type | awk '{printf("%.2f$\\pm$%.4f & ",$8*100,$10);}' >> output 
    done #|  xargs 

    max=$(cat x | awk '{for(j=1;j<=16;j+=2) printf(" %.2f ",$j);}' | sed 's/\  /\ /g' | sed 's/\ /\n/g' | sort -r | head -n 1)
    #echo $max
    cat output | sed -e "s/$max/\\\\bf $max/g" | sed 's/\&\ $/\\\\/g'
    
    #cat output
    rm x output
    echo
    #exit
done 

echo "\hline"
echo -n "Best "
for i in `seq 0 3`; do
    echo -n "& $(echo ${countBin[$i]}) && $(echo ${countReal[$i]}) "
done
echo "\\\\ \\hline"

echo "\end{tabular}}"
echo "\end{table*}"

