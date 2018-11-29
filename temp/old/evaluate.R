library('parallel')
library('ROCR')

# CROSS-VALIDATION
runCV <- function(mypredictor, labelTrain, variantTrain, nfolds=5, nrepeats=10, seed=5396, mc.cores=1, strategy="none", ...) {
    # function that run "mypredictor" on a CV setting
    #
    # output a list of size the number of CV experiments (eg 50) (= nfolds x nrepeats)
    # each entry of the list is itself a list with 2 entries: "proba" and "ref"
    # "proba" contains the vector of predicted probabilities
    # "ref" contains the labels of the fold test set

    # Set random number generator seed
    set.seed(seed)

    # Make folds
    n = nrow(variantTrain)
    folds <- list()
    for (i in seq(nrepeats)) {
        folds <- c(folds,split(sample(seq(n)), rep(1:nfolds, length = n)))
    }
    nexp = length(folds) # the total number CV of experiments

    # Parallel CV
    print("start CV")
    print(strategy)
    rescv = mclapply(seq(nexp),
                   FUN=function(iexp) {
                       cat(".")
                       vTrain = variantTrain[-folds[[iexp]],,drop=F]
                       vTest = variantTrain[folds[[iexp]],,drop=F]
                       lTrain = labelTrain[-folds[[iexp]]]
                       lTest = labelTrain[folds[[iexp]]]
                       if (strategy=="none") {
                           proba = mypredictor(variantTrain=vTrain, variantTest=vTest, labelTrain=lTrain, ...)
                       } else if (strategy=="impute") {
                           proba = predictorImpute(variantTrain=vTrain, variantTest=vTest, labelTrain=lTrain, mypredictor=mypredictor, ...)
                       } else {
                           print("wrong strategy! try again!")
                       }
                       res.fold = list(proba=proba, ref=lTest)
                       return(res.fold)
                   },
                   mc.cores=mc.cores
                   )

    return(rescv)

}

# EVALUATE CV
evaluateCVwithROCR <- function(resCV, measure="acc", x.measure="cutoff", positiveClass="real") {
    # example of usage: 
    #    - measure="tpr", x.measure="fpr" ---> ROC curve
    #    - measure="auc", x.measure="cutoff" ---> AUC
    # proba
    #list.pred = lapply(resCV, function(c) 1-c[[1]])
    list.pred = lapply(resCV, function(c) c[[1]])
    # ref
    list.ref = lapply(resCV, function(c) c[[2]])
    uu = unique(unlist(list.ref))
    mylevel = c(positiveClass,uu[uu!=positiveClass])
    list.ref = lapply(list.ref, function(x) factor(x, levels=mylevel))
    # object
    pred.obj = prediction(list.pred, list.ref)
    # evaluate
    perf.obj = performance(pred.obj, measure=measure, x.measure=x.measure)
    return(perf.obj)
}


# LEAVE-ONE-OUT
LeaveOneOut <- function(mypredictor, labelTrain, variantTrain, mc.cores=1, ...) {

    res.proba = mclapply(1:length(labelTrain),
                   FUN=function(j) {
                       cat(".")
                       mypred = mypredictor(variantTrain=variantTrain[-j,,drop=F], variantTest=variantTrain[j,,drop=F], labelTrain=labelTrain[-j], ...) 
                       return(mypred)
                   },
                   mc.cores=mc.cores
                   )

    return(unlist(res.proba))

}
