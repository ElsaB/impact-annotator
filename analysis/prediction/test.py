import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as seaborn
from sklearn.metrics import roc_curve, confusion_matrix, precision_recall_curve
from sklearn.model_selection import cross_validate, learning_curve
import time

from sklearn.metrics import f1_score, average_precision_score
from sklearn.metrics import auc, roc_auc_score



def run_model_detailed_CV(model, X, y, cv_strategy):
    print('Run model with detailed CV...')

    metrics = pd.DataFrame(index=range(cv_strategy.get_n_splits()),
                           columns=['fit_time', 'score_time',
                                    'test_accuracy', 'train_accuracy',
                                    'test_roc_auc', 'train_roc_auc',
                                    'test_f1', 'train_f1',
                                    'test_average_precision', 'train_average_precision',
                                    'estimator'])
    metrics.index.name = 'fold_number'


    for i, (train_index, test_index) in enumerate(cv_strategy.split(X, y)):
        print('  - fold %d/%d...' % (i + 1, cv_strategy.get_n_splits()), end='')
        (X_train, X_test) = (X.iloc[train_index], X.iloc[test_index])
        (y_train, y_test) = (y.iloc[train_index], y.iloc[test_index])


        # Fit model
        start = time.time()

        model.fit(X_train, y_train)
        y_train_pred = model.predict_proba(X_train)[:, 1]
        y_test_pred  = model.predict_proba(X_test) [:, 1]

        metrics.iloc[i].fit_time = time.time() - start


        # Get scores
        start = time.time()

        # accuracy
        metrics.iloc[i].train_accuracy = np.mean(model.predict(X_train) == y_train)
        metrics.iloc[i].test_accuracy  = np.mean(model.predict(X_test)  == y_test)

        # accuracy
        metrics.iloc[i].train_f1 = f1_score(y_train, model.predict(X_train))
        metrics.iloc[i].test_f1  = f1_score(y_test,  model.predict(X_test))

        # estimator
        metrics.iloc[i].estimator = model



        if hasattr(metrics.estimator.iloc[0], 'best_params_'):
            metrics.iloc[i]['gs_best_parameters'] = model.best_params_
            metrics.iloc[i]['gs_cv_results'] = model.cv_results_

        metrics.iloc[i].score_time = time.time() - start

        print(' done! (%.2fs)' % (metrics.iloc[i].fit_time + metrics.iloc[i].score_time))


    get_other_metrics(metrics, X, y, cv_strategy, detailed_cv=True)
    metrics.drop('estimator', axis=1, inplace=True)


    return metrics


# add to metrics the necessary metrics to compute later the ROC curve, precision-recall curve and confusion matrix for each fold
# also adds the predicted probability for each sample and the true value
# only used in run_model()
def get_other_metrics(metrics, X, y, cv_strategy):

    # create empty list for the new metrics
    new_columns = ['y_test', 'y_predicted',
                   'test_fpr', 'test_tpr', 'roc_thresh',
                   'precision', 'recall', 'pr_thresh',
                   'confusion_matrix']

    for col in new_columns:
        metrics[col] = [[] for i in range(metrics.shape[0])]


    # for each fold
    for i, (train_index, test_index) in enumerate(cv_strategy.split(X, y)):
        (X_train, X_test) = (X.iloc[train_index], X.iloc[test_index])
        (y_train, y_test) = (y.iloc[train_index], y.iloc[test_index])
        
        ## predicted probability metrics
        metrics.at[i, 'y_test']      = y_test.values
        metrics.at[i, 'y_predicted'] = metrics.iloc[i].estimator.predict_proba(X_test)[:,1]

        ## ROC metrics       
        fpr, tpr, roc_thresholds = roc_curve(metrics.at[i, 'y_test'], metrics.iloc[i].y_predicted)
        metrics.at[i, 'test_fpr']   = fpr
        metrics.at[i, 'test_tpr']   = tpr
        metrics.at[i, 'roc_thresh'] = roc_thresholds

        ## precision-recall metrics       
        precision, recall, pr_thresholds = precision_recall_curve(metrics.at[i, 'y_test'], metrics.iloc[i].y_predicted)
        metrics.at[i, 'precision'] = precision
        metrics.at[i, 'recall']    = recall
        metrics.at[i, 'pr_thresh'] = pr_thresholds

        ## confusion matrix metrics
        #y_pred_25 = (metrics.iloc[i].y_predicted >= 0.25)
        #y_pred_50 = (metrics.iloc[i].y_predicted >= 0.5) # equivalent to y_pred_05 = metrics.iloc[i].estimator.predict(X_test):
        #y_pred_75 = (metrics.iloc[i].y_predicted >= 0.75)            

        metrics.at[i, 'confusion_matrix'] = confusion_matrix(y_test, metrics.iloc[i].estimator.predict(X_test))


        if detailed_cv:
            print("lol")
            metrics.at[i, 'test_roc_auc'] = auc(fpr, tpr)
            print(auc(fpr, tpr), metrics.iloc[i].test_roc_auc)

            y_predicted_train = metrics.iloc[i].estimator.predict_proba(X_train)[:,1]
            fpr, tpr, roc_thresholds = roc_curve(y_train.values, y_predicted_train)
            metrics.iloc[i].train_roc_auc = auc(fpr, tpr)

            metrics.at[i, 'test_average_precision'] = average_precision_score(metrics.at[i, 'y_test'], metrics.iloc[i].y_predicted)
            metrics.at[i, 'train_average_precision'] = average_precision_score(y_train.values, y_predicted_train)











