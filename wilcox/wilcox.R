
#HOW TO RUN:
#R --vanilla --quiet --slave < do_wilcoxon.R --args input_file best_column 

library(xtable)
defaultW <- getOption("warn")
options(warn = -1) 
args <- commandArgs(TRUE)

file <- args[1] #file name to be processed (must have headers, of algorithms: DEbin or DEreal
texName <- args[2]
tableFile <- read.delim(file,header=TRUE,sep=","); #read table
nCols <- ncol(tableFile) #number of columns

#algs <- as.list(strsplit(args[3],",")[[1]])
#print(tableFile)
#print(nCols)
results <- matrix(1:(nCols*nCols), nrow = nCols, ncol = nCols)

for (i in 1:nCols) {
    x = tableFile[,c(colnames(tableFile)[i])]
    #print(x)
    for (j in i:nCols) {
        if (i == j) {results[i,j] = NaN; next}
        y = tableFile[,c(colnames(tableFile)[j])]
        #print(sprintf("Comparing columns %d and %d",i,j)[1])
        
        p_val <- wilcox.test(x,y,int.conf=0.95,paired=T,correct=FALSE,alternative="t")$p.value
        #print("---------------------------------------------")
        #print(p_val)
        if (p_val < 0.05) {
            results[i,j] <- toString(expression("\u2020"))
            results[j,i] <- toString(expression("\u2020"))

        }
        else {
            results[i,j] <- toString(p_val)
            results[j,i] <- toString(p_val)
        }
        #results[j,i] <- NaN
    #wTest2 <- wilcox.test(Y,X,int.conf=0.95,paired=T,correct=FALSE,conf.int=TRUE,alternative="l")
        
    }
}
#colnames(tableFile)
dimnames(results) <- list(colnames(tableFile),colnames(tableFile))
#print(results)

print(xtable(results), only.contents=TRUE, include.rownames=T, include.colnames=T, floating=F,file = texName)
options(warn = defaultW)
