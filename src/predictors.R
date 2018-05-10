# ---------------------------------- #
# 2-CLASS CLASSIFICATION PREDICTORS
# ---------------------------------- #
#
# In this file we have predictor functions, that take at least 3 arguments:
#
#	- variantTrain : n*p matrix of descriptors for n training variants
#	- variantTest : m*p matrix of descriptors for m test variants
#	- labelTrain : n 2-class labels on the n training variants
#
# and that output a vector of m probabilities for the test variants
#
# NB: probability = probability of belonging to the positive class (eg. "driver")


# ---------------------------------- #
# constant classification
# ---------------------------------- #
predictorConstant <- function(variantTrain, variantTest, labelTrain, positiveClass="driver") {

    pred.random = rep(0, nrow(variantTest))

    return(pred.random)
}

# ---------------------------------- #
# random classification
# ---------------------------------- #
predictorRandom <- function(variantTrain, variantTest, labelTrain, positiveClass="driver", pp=NULL) {

    if (is.null(pp)) {
        pp = table(labelTrain)[positiveClass] / length(labelTrain)
    }
    pred.silly = rbinom(n=nrow(variantTest), size=1, prob=pp)
    print(pred.silly)

    return(pred.silly)
}

# ---------------------------------- #
# random forest classification
# ---------------------------------- #
library(randomForest)
# basic random forest
predictorRF <- function(variantTrain, variantTest, labelTrain, positiveClass="driver", ntree=500) {

    # Train a random forest model
    model.rf = randomForest(variantTrain, factor(labelTrain), ntree = ntree)
    # Make predictions and output probabilities
    pred.rf = predict(model.rf, variantTest, type="prob")[,positiveClass]

    return(pred.rf)
}
# preditor RF with balanced sampling 
predictorRFstrata <- function(variantTrain, variantTest, labelTrain, positiveClass="driver", ntree=500) {

    # Size of the positive minority class
    nMin = sum(labelTrain==positiveClass)
    # Train a random forest model
    model.rf = randomForest(x=variantTrain, y=factor(labelTrain), ntree = ntree, sampsize=c(nMin,nMin))
    # Make predictions and output probabilities
    pred.rf = predict(model.rf, variantTest, type="prob")[,positiveClass]

    return(pred.rf)
}


# ---------------------------------- #
# SVM classification
# ---------------------------------- #
#library(kernlab)
predictorSVM <- function(variantTrain, variantTest, labelTrain, positiveClass="driver") {
    # TODO
}

# ---------------------------------- #
# Logistic classification
# ---------------------------------- #
library(glmnet)
predictorLogistic <- function(variantTrain, variantTest, labelTrain, positiveClass="driver", alpha=1) {
    # alpha=1 --> l1 penalty
    # alpha=2 --> l2 penalty
    # alpha=1/2 --> elastic net

    # Train a logistic model with internal cross validation
    cvfit = cv.glmnet(as.matrix(variantTrain), factor(labelTrain), family = "binomial", type.measure = "auc", alpha=alpha)
    # Make predictions and output probabilities
    proba.log = predict(cvfit, newx = as.matrix(variantTest), s = "lambda.1se", type="response")
    if( which(levels(factor(labelTrain))==positiveClass)==1 ) { proba.log = 1-proba.log } # probability of being a driver 

    return(proba.log)
}

# --------------------------------------------- #
# impute EXAC missing data and use all dataset
# --------------------------------------------- #
predictorImpute <- function(variantTrain, variantTest, labelTrain,
                            mypredictor=predictorRF,
                            list.features.hybrid=c("MAX.MAF","NB.POP"), ...) {

    if (list.features.hybrid[1] %in% colnames(variantTrain)) {
        # Learn missing info while merging train and test sets
        ioktrain = which(apply(variantTrain[,list.features.hybrid,drop=F],1,function(v) sum(is.na(v)))==0)
        inatrain = which(apply(variantTrain[,list.features.hybrid,drop=F],1,function(v) sum(is.na(v)))==length(list.features.hybrid))
        ioktest = which(apply(variantTest[,list.features.hybrid,drop=F],1,function(v) sum(is.na(v)))==0)
        inatest = which(apply(variantTest[,list.features.hybrid,drop=F],1,function(v) sum(is.na(v)))==length(list.features.hybrid))
        # The training and testing dataset for the data imputation
        missingTrain = rbind(variantTrain[ioktrain,-match(list.features.hybrid, colnames(variantTrain)),drop=F],
                             variantTest[ioktest,-match(list.features.hybrid, colnames(variantTest)),drop=F])
        missingTest = rbind(variantTrain[inatrain,-match(list.features.hybrid, colnames(variantTrain)),drop=F],
                            variantTest[inatest,-match(list.features.hybrid, colnames(variantTest)),drop=F])

        for (missing.features in list.features.hybrid) {
            missingResponse = c(variantTrain[ioktrain,missing.features], variantTest[ioktest, missing.features])
            # Train a random forest model
            model.rf = randomForest(missingTrain, missingResponse, ntree = 500)
            # Make predictions and output values
            pred.rf = predict(model.rf, missingTest)
            # Fill the initial data sets
            variantTrain[inatrain,missing.features] = pred.rf[1:length(inatrain)]
            if (length(inatest)>0) {
                variantTest[inatest,missing.features] = pred.rf[(length(inatrain)+1):length(pred.rf)]
            }
        }
    }

    # Once you have imputed the missing data you can go for your prediction using all information (included predicted)
    pred = mypredictor(variantTrain=variantTrain, variantTest=variantTest, labelTrain=labelTrain, ...)

    return(pred)
}
