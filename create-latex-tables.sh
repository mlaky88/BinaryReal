#!/bin/bash

coding=$1
disc=$2
classifier=$3
method=$4
if [ $method == "wrapper" ]; then
    file="../experiments-wrapper/wrap-mean+std-feats.res"
elif [ $method == "filter" ]; then
    file="../experiments-filter/filt-mean+std-feats.res"
fi

echo "\begin{table*}"
echo "\scriptsize"
echo "\centering"
echo "\caption{Discretization: $disc, $coding algorithms. $classifier classifier}"
echo "\label{tab:result-$(echo "$disc" | awk '{ print tolower($1) }')-$coding-$classifier}"
echo "\resizebox{45em}{!}{ "
echo "\setlength{\tabcolsep}{0.3em}"
echo "\begin{tabular}{>{\centering}m{1.3cm}|cc|cc|cc|cc|}"
echo "\cline{2-9}"
echo -n "\multirowcell{2}{\tiny $\mathit{$classifier}$\\\\ \tiny $\mathit{$disc}$}"
echo "& \multicolumn{2}{c|}{ABC\$_{$coding}$} & \multicolumn{2}{c|}{DE\$_{$coding}$} & \multicolumn{2}{c|}{GA\$_{$coding}$} & \multicolumn{2}{c|}{PSO\$_{$coding}$} \\\\ \cline{2-9}"
echo "& Acc.&\#Feat. & Acc.&\#Feat. &Acc.&\#Feat. & Acc.&\#Feat. \\\\ \hline"
for j in "credit" "libras" "parkinsons" "breast" "sonar" "musk1" "ionosphere" "semeion" "german"; do 
    for i in "abc" "de" "ga" "pso"; do 
        if [ $i == "abc" ]; then
            p=$j
            echo -n "${p^} & " >> output 
        fi
        echo -n "$(cat $file | grep "alg-$i" | grep "$coding" | grep "$disc" | grep $j | grep $classifier| awk '{print $6*100,$7" "$8" "$9" "}') " >> x
        cat $file | grep "alg-$i" | grep "$coding" | grep "$disc" | grep $j |grep $classifier | awk '{printf("%.2f$\\pm$%.4f & %.1f$\\pm$%.2f & ",$6*100,$7,$8,$9);}' >> output 
    done #|  xargs 
    
    max=$(cat x | awk '{for(j=1;j<=16;j+=4) printf(" %.2f ",$j);}' | sed 's/\  /\ /g' | sed 's/\ /\n/g' | sort -r | head -n 1)
    #echo $max
    cat output | sed -e "s/$max/\\\\bf $max/g" | sed 's/\&\ $/\\\\/g'
    #cat output
    rm x output
    echo
    #exit
done 

echo "\hline"
#echo "Best& & & & & & & & \\\\"
echo "\end{tabular}}"
echo "\end{table*}"

