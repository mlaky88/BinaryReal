
#HOW TO RUN:
#R --vanilla --quiet --slave < do_wilcoxon.R --args input_file best_column 

args <- commandArgs(TRUE)

file <- args[1] #file name
comp <- args[2] #which is best by friedman
t <- read.delim(file,header=TRUE,sep=","); #read table
cols <- ncol(t) #number of columns

algs <- as.list(strsplit(args[3],",")[[1]])



y <- paste("A",comp,sep="")
Y <- t[,c(y)]
print(t)
for (i in 1:cols) {
  x <- paste("A",i,sep="")
  val <- as.numeric(strtoi(comp))
  if (val == i) {
    print ("Ignoring ! ... ")
  }else {
    X <- t[, c(x)]
    print (paste(algs[val]," vs ",algs[i]))
    wTest1 <- wilcox.test(Y,X,int.conf=0.95,paired=T,correct=FALSE,conf.int=TRUE,alternative="t")
    wTest2 <- wilcox.test(Y,X,int.conf=0.95,paired=T,correct=FALSE,conf.int=TRUE,alternative="l")
    print (wTest1)
    print (wTest2)
  }
}
