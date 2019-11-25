if [ $# -lt 1 ]; then
    echo "EXAMPLE: ./prepareFriedman.sh [file]"
    exit 1
fi


file=$1

function createLatexTableCD () {
    type=$1
    
    CD=0.6061

    echo "\begin{table*}[!ht]"
    echo "\centering"
    echo "\subfloat[kNN]{"
    echo "\begin{minipage}{0.49\textwidth}"
    echo "\begin{tabular}{ | r | r | r | c | c | c | c |}"
    echo "\hline"
    echo "\multirow{2}{*}{Alg.} & \multirow{2}{*}{Fri.} & \multicolumn{2}{|c|}{Nemenyi} & \multicolumn{2}{|c|}{Wilcoxon} \\\\ \cline{3-6}"
    echo "& & CD & S. & \$p\$-value & S. \\\\"
    echo "\hline"

    algRankSmall=$(cat CD.txt | awk '{print $2}' | sort | head -n1)
    algNameSmall=$(cat CD.txt | grep -n $algRankSmall | sed 's/:/\ /g' | awk '{print $2}')
    #echo $algNameSmall


    wTest=$(echo -n $(echo $algNameSmall | cut -c2-);if [ $(echo $algNameSmall | cut -c1) == "b" ]; then echo -n "bin"; else echo -n "real"; fi ; echo -n "$type")
    
    #echo $algRankSmall
    #cat $2 | grep 

    while IFS= read -r row; do
        algName=$(echo $row | awk '{print $1}')
        algRank=$(echo $row | awk '{print $2}')
        echo -n $(echo $algName | cut -c2- | tr a-z A-Z)
        
        echo -n "\$_{"
        if [ $(echo $algName | cut -c1) == "b" ]; then
            echo -n "bin"
        else
            echo -n "real"
        fi
        echo -n "}$ & $(echo "scale=2;$algRank/1" | bc -l) & ["

        echo -n "$(echo "scale=2;($algRank-$CD)/1" | bc), $(echo "scale=2;($algRank+$CD)/1" | bc) ] & "

        #še wilcox testi tukaj


        if [ "$algRank" == "$algRankSmall" ]; then
            echo -n "\$\\ddagger\$ & \$\\infty\$ & \$\\ddagger\$ \\\\"
        else
            echo -n "& & \\\\"
        fi

        echo

        #echo "$row"
    done < "CD.txt"

    echo "\hline"
    echo "\end{tabular}"
    echo "\end{minipage}}"
    echo "\subfloat[kNN]{\begin{minipage}{0.49\textwidth}\includegraphics[width=0.99\textwidth]{images/???}\end{minipage}}"
    echo "\caption{Nemenyi and Wilcoxon post-hoc test results for $type-based feature selection with the kNN classifier.}"
    
}



function doFriedman () {
    lines=$(cat friedmanData/Friedman.dat | wc -l)
    echo "Number of observations: $lines"
    cat friedmanData/Friedman.dat | sed 's/\t/\ /g' | sed 's/\ /,/g' | sed "2,$lines s/^/D/g" | sed "1,1 s/^/Alg/g" > tmp.dat && mv tmp.dat friedmanData/Friedman.dat
    java -cp Friedman Friedman friedmanData/Friedman.dat > friedmanData/outputFriedman.tex &
    sleep 2
    kill -9 $!
    beginRanks=$(cat friedmanData/outputFriedman.tex | grep -n "Algorithm&Ranking" | sed 's/:/\ /g' | awk '{print $1+2}')
    echo $beginRanks
    cat friedmanData/outputFriedman.tex | sed -n "$beginRanks,$((beginRanks+7))p" | sed 's/\&/\ /g' | sed 's/\\\\//g' | sed 's/bin-*/b/g' | sed 's/real-/r/g' > friedmanData/Friedman.ranks
    cat friedmanData/Friedman.ranks | sed 's/[br][a-z]*//g' | awk 'BEGIN{i=-1} /.*/{printf "%d% s\n",i+2,$0; i+=2}' > friedmanData/Friedman.gp
}


function bin-vs-real () {
    for type in "filter" "wrapper"; do
        if [ -f friedmanData/Friedman.dat ]; then
            rm friedmanData/Friedman.dat
        fi
        touch friedmanData/Friedman.dat
        header=""
        for coding in "bin" "real"; do
            for alg in "de" "abc" "pso" "ga"; do
                paste friedmanData/Friedman.dat "$coding-$alg-$type.dat" > tmp.dat && mv tmp.dat friedmanData/Friedman.dat
                header="$header$alg$coding$type,"
            done
        done
        doFriedman
        fileName="wilcox/$type-bin-real.tex"
        wilcox $header $fileName
        python fix-ranks.py friedmanData/Friedman.gp > tmp.dat && mv tmp.dat friedmanData/Friedman.gp


        paste friedmanData/Friedman.ranks friedmanData/Friedman.gp | awk '{print $1" "$4}' > CD.txt
        createLatexTableCD $type $fileName
        

        gnuplot -e "rankFile='friedmanData/Friedman.gp'; outputFile='$type-bin-real.png'" drawings/drawBinVsReal.gp
        for i in `seq 1 5`; do 
            echo
        done
        exit
    done
}

function filter-vs-wrapper () {
    for coding in "bin" "real"; do
        if [ -f friedmanData/Friedman.dat ]; then
            rm friedmanData/Friedman.dat
        fi
        touch friedmanData/Friedman.dat
        header=""
        for type in "filter" "wrapper"; do
            for alg in "de" "abc" "pso" "ga"; do
                paste friedmanData/Friedman.dat "$coding-$alg-$type.dat" > tmp.dat && mv tmp.dat friedmanData/Friedman.dat
                header="$header$alg$coding$type,"
            done
        done
        doFriedman
        fileName="wilcox/$coding-filter-wrapper.tex"
        wilcox $header $fileName    
        python fix-ranks.py friedmanData/Friedman.gp > tmp.dat && mv tmp.dat friedmanData/Friedman.gp    

        paste friedmanData/Friedman.ranks friedmanData/Friedman.gp | awk '{print $1" "$4}' > CD.txt
        createLatexTableCD $coding

        gnuplot -e "rankFile='friedmanData/Friedman.gp'; outputFile='$coding-filter-wrapper.png'; xAxisLabels='$coding'" drawings/drawFilterVsWrapper.gp
        for i in `seq 1 5`; do 
            echo
        done
    done 
}



function wilcox () {
    sed -i "1s/.*/$1/" friedmanData/Friedman.dat
    sed -i "s/D,//" friedmanData/Friedman.dat
    sed -i "s/,$//" friedmanData/Friedman.dat

    R --vanilla --quiet --slave < wilcox/wilcox.R --args "friedmanData/Friedman.dat" $2


    cat $2 | sed -r 's/([a-z]+)(bin|real)(filter|wrapper)(.*)/\U\1$_{\L\2}$\4/g' | sed 's/\(\.[0-9][0-9]\)[0-9]*/\1/g' | sed 's/nan/\$\\infty\$/g' > x; mv x $2

}

###################################################
#BEGIN SCRIPT

#1. Prvo imam filter bin vs filter real
#2. Drugo imam wrapper bin vs filter real
#3. Tretje imam filter vs wrapper bin
#4. Četrto imam filter vs wrapper real
for type in "filter" "wrapper"; do
    for coding in "bin" "real"; do
        for alg in "de" "abc" "pso" "ga"; do        
            echo "$coding-$alg" > "$coding-$alg-$type.dat"
            cat $file | grep $coding | grep "alg-$alg" | grep "$type" | awk '{print 1-$6" "1-$7" "1-$8" "1-$9" "$10}' | xargs | sed 's/\ /\n/g' >> "$coding-$alg-$type.dat"
        done
    done
done

#1. in 2. 
bin-vs-real
#3. in 4. 
filter-vs-wrapper
#Počisti
for type in "filter" "wrapper"; do
    for alg in "de" "abc" "pso" "ga"; do
        rm "$coding-$alg-$type.dat"
    done
done