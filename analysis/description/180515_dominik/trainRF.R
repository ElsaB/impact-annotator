library('ROCR')
library('randomForest')
source('~/code/impact-annotator/src/evaluate.R')
source('~/code/impact-annotator/src/predictors.R')

# load variantTrain.corr, labelTrain.subset
load('~/code/impact-annotator/data/trainingData.Balanced.RData')

labelTrain.subset.str <- rep("non-real", length(labelTrain.subset))
labelTrain.subset.str[labelTrain.subset] <- "real"

myrf <- randomForest(variantTrain.corr, factor(labelTrain.subset.str), ntree = 500)


rfCV <- runCV(predictorRF, labelTrain.subset.str, variantTrain.corr,  nfolds=5, 
nrepeats=5, positiveClass="real") 
save(myrf, rfCV, file='~/code/impact-annotator/data/rfCVcomplete.balanced.RData')