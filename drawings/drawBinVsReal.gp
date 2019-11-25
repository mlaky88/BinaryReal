reset
set term png truecolor 13
set termopt enhanced
set style data points

set xtics ("bDE" 1,"bABC" 3,"bPSO" 5,"bGA" 7, "rDE" 9, "rABC" 11, "rPSO" 13, "rGA" 15)



set xrange [0:16]
set xlabel "Algorithms"
set yrange [1.5:8.0]
set ylabel "Average Rank differences"
set grid
set output outputFile
plot rankFile using 1:2:($2-0.6061):($2+0.6061) ls 4 lc 1 lw 2 with errorbars title "" 

