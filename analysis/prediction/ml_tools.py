import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as seaborn
from scipy import interp
from sklearn.metrics import roc_curve, confusion_matrix, precision_recall_curve
from sklearn.model_selection import cross_validate, learning_curve
import time

# run_model_old() only
from sklearn.metrics import auc, roc_auc_score



# run the given model with the given parameters
# return a pandas DataFrame object containing all the relevant metrics, including the grid search metrics when a grid_search was performed
def run_model(model, X, y, cv_strategy, n_jobs=1):
    print('Run model...', end='')
    start = time.time()


    # get cross validation metrics
    metrics = cross_validate(model, X, y, cv=cv_strategy, scoring=['accuracy', 'roc_auc', 'f1'], return_train_score=True, return_estimator=True, n_jobs=n_jobs, error_score='raise')
    metrics = pd.DataFrame(metrics)
    metrics.index.name = 'fold_number'

    # get grid search metrics if the model seems to have performed a grid search
    if hasattr(metrics.estimator.iloc[0], 'best_params_'):
        metrics['gs_best_parameters'] = metrics.estimator.apply(lambda x: x.best_params_)
        metrics['gs_cv_results']      = metrics.estimator.apply(lambda x: x.cv_results_)

    # get ROC curve, precision-recall curve and confusion matrix, warning this implies:
    # - creating the cross-validation folds again
    # - re-testing the fitted model on the test folds
    get_other_metrics(metrics, X, y, cv_strategy)


    # we remove the estimators from the metrics because they can be quite memory-expensive (for random forest with a lot of trees for example)
    metrics.drop('estimator', axis=1, inplace=True)


    print(' done! (%.2fs)' % (time.time() - start))
        
    return metrics



# add to metrics the necessary metrics to compute later the ROC curve, precision-recall curve and confusion matrix for each fold
# only used in run_model()
def get_other_metrics(metrics, X, y, cv_strategy):

    # create empty list for the new metrics
    ## ROC metrics
    metrics['test_fpr']   = [[] for i in range(metrics.shape[0])]
    metrics['test_tpr']   = [[] for i in range(metrics.shape[0])]
    metrics['roc_thresh'] = [[] for i in range(metrics.shape[0])]

    ## precision-recall metrics
    metrics['precision'] = [[] for i in range(metrics.shape[0])]
    metrics['recall']    = [[] for i in range(metrics.shape[0])]
    metrics['pr_thresh'] = [[] for i in range(metrics.shape[0])]

    ## confusion matrix metrics
    metrics['confusion_matrix'] = [[] for i in range(metrics.shape[0])]


    # for each fold
    for i, (train_index, test_index) in enumerate(cv_strategy.split(X, y)):
        (X_train, X_test) = (X.iloc[train_index], X.iloc[test_index])
        (y_train, y_test) = (y.iloc[train_index], y.iloc[test_index])
        
        y_test_pred  = metrics.iloc[i].estimator.predict_proba(X_test)[:, 1]

        ## ROC metrics       
        fpr, tpr, roc_thresholds = roc_curve(y_test, y_test_pred)
        metrics.at[i, 'test_fpr']   = fpr
        metrics.at[i, 'test_tpr']   = tpr
        metrics.at[i, 'roc_thresh'] = roc_thresholds

        ## precision-recall metrics       
        precision, recall, pr_thresholds = precision_recall_curve(y_test, y_test_pred)
        metrics.at[i, 'precision'] = precision
        metrics.at[i, 'recall']    = recall
        metrics.at[i, 'pr_thresh'] = pr_thresholds

        ## confusion matrix metrics
        #y_pred_25 = (y_test_pred >= 0.25)
        #y_pred_50 = (y_test_pred >= 0.5) # equivalent to y_pred_05 = metrics.iloc[i].estimator.predict(X_test):
        #y_pred_75 = (y_test_pred >= 0.75)

        metrics.at[i, 'confusion_matrix'] = confusion_matrix(y_test, metrics.iloc[i].estimator.predict(X_test))


# print the average test set accuracy, test ROC AUC and test F1-score for a given metrics DataFrame
def print_mean_metrics(metrics):
    # test set mean metrics and 95% confidence interval on the metrics estimate (= 1.96 x standard_deviation)
    print('▴ Mean accuracy: %0.3f ± %0.3f' % (metrics.test_accuracy.mean(), 1.96 * metrics.test_accuracy.std()))
    print('▴ Mean ROC AUC : %0.3f ± %0.3f' % (metrics.test_roc_auc.mean() , 1.96 * metrics.test_roc_auc.std()))
    print('▴ Mean F1-score: %0.3f ± %0.3f' % (metrics.test_f1.mean()      , 1.96 * metrics.test_f1.std()))



# print multiple metrics values for the train and test set accross each folds, including the grid search metrics when a grid_search was performed
# set detailed_grid_search_metrics to True when you want the detailed grid search metrics
def print_fold_metrics(metrics, detailed_grid_search_metrics=False):
    
    # boolean variable being True if the metrics DataFrame contains grid search metrics
    grid_search = hasattr(metrics.iloc[0], 'gs_best_parameters')

    print('Fold #: [fit_time | score_time]')
    print('  → accuracy: [test_accuracy | train_accuracy]')
    print('  → ROC AUC : [test_roc_auc  | train_roc_auc] ')
    print('  → F1-score: [test_f1_score | train_f1_score]')

    if grid_search:
        print('  → best hyperparameters: {\'first_hyperparameter_name\': best_value, ...}')

        if detailed_grid_search_metrics:
            print('      mean_test_score ± 1.96 * std_test_score for {hyperparameters_set #1}')
            print('      mean_test_score ± 1.96 * std_test_score for {hyperparameters_set #2}')
            print('      ...')

    print()

    # for each fold
    for i, fold_metrics in metrics.iterrows():
        print('Fold %d: [%.2fs | %.2fs]' % (i + 1, fold_metrics.fit_time, fold_metrics.score_time))
        print('  → accuracy: [%.3f | %.3f]' % (fold_metrics.test_accuracy, fold_metrics.train_accuracy))
        print('  → ROC AUC : [%.3f | %.3f]' % (fold_metrics.test_roc_auc , fold_metrics.train_roc_auc ))
        print('  → F1-score: [%.3f | %.3f]' % (fold_metrics.test_f1      , fold_metrics.train_f1      ))

        if grid_search:
            print('  → best hyperparameters: %s' % fold_metrics.gs_best_parameters)

            if detailed_grid_search_metrics:
                for mean, std, param in zip(fold_metrics.gs_cv_results['mean_test_score'],
                                            fold_metrics.gs_cv_results['std_test_score'],
                                            fold_metrics.gs_cv_results['params']):
                    print('      %0.3f ± %0.3f for %s' % (mean, 1.96 * std, param))



# plot ROC curve and PR curve side_by_side
def plot_roc_and_precision_recall(metrics, figsize=(20, 10), plot_thresholds=True):
    fig, (ax0, ax1) = plt.subplots(1, 2, figsize=figsize)
    plot_roc(metrics, ax0, figsize[0] / 2 * 1.5, plot_thresholds)
    plot_precision_recall(metrics, ax1, figsize[0] / 2 * 1.5, plot_thresholds)



# plot ROC curve for each fold (and the associated threshold) and a mean ROC curve
# strongly inspired by http://scikit-learn.org/stable/auto_examples/model_selection/plot_roc_crossval.html
def plot_roc(metrics, ax, legend_size, plot_thresholds=True):
    # set plot
    ax.set_title('ROC curve')
    ax.set_xlabel('false positive rate')
    ax.set_ylabel('true positive rate  |  threshold value')
    

    mean_fpr = np.linspace(0, 1, 101) # [0, 0.01, 0.02, ..., 0.09, 1.0]
    tprs = [] # true positive rate list for each fold


    # for each fold
    for i, fold_metrics in metrics.iterrows():
        fpr, tpr, thresholds = fold_metrics.test_fpr, fold_metrics.test_tpr, fold_metrics.roc_thresh
        
        # because the length of fpr and tpr vary with the fold (size of thresholds  = nunique(y_pred[:, 1]) + 1), we can't just do
        # fprs.append(fpr) and tprs.append(tpr)
        # we use a linear interpolation to find the values of fpr for a 101 tpr chosen values
        tprs.append(interp(mean_fpr, fpr, tpr))
        tprs[-1][0] = 0.0 # threshold > 1 for the first point (ie the last tpr value)

        # plot ROC curve
        plt = ax.plot(fpr, tpr, linewidth=0.6, alpha=0.4,
                      label='ROC fold %d (AUC = %0.3f)' % (i, fold_metrics.test_roc_auc))

        # plot thresholds
        if plot_thresholds:
            thresholds[0] = 1.001 # value is > 1, we set it just above one for the graphic
            ax.plot(fpr, thresholds, linewidth=0.6, alpha=0.4, color=plt[0].get_color())

    
    # plot baseline
    ax.plot([0, 1], [0, 1], '--r', linewidth=0.5, alpha=1, label='random')


    # plot mean ROC
    mean_tpr = np.mean(tprs, axis=0)
    ax.plot(mean_fpr, mean_tpr, 'b', linewidth=2,
            label='mean ROC (AUC = %0.3f $\pm$ %0.3f)' % (metrics.test_roc_auc.mean(), 1.96 * metrics.test_roc_auc.std()))


    # plot mean ROC std
    std_tpr = np.std(tprs, axis=0)
    ax.fill_between(mean_fpr, mean_tpr - std_tpr, mean_tpr + std_tpr, color='blue', alpha=0.15,
                     label='mean ROC $\pm$ 1 std. dev.')


    ax.legend(loc='lower right', prop={'size': legend_size})



# plot Precision-Recall curve (PR) for each fold (and the associated threshold) and a mean PR curve
# strongly inspired by previous function
def plot_precision_recall(metrics, ax, legend_size, plot_thresholds=True):
    # set plot
    ax.set_title('Precision-Recall curve')
    ax.set_xlabel('recall')
    ax.set_ylabel('precision  |  threshold value')
    

    mean_precision = np.linspace(0, 1, 101) # [0, 0.01, 0.02, ..., 0.09, 1.0]
    recalls = [] # recalls value list for each fold


    # for each fold
    for i, fold_metrics in metrics.iterrows():
        precision, recall, thresholds = fold_metrics.precision, fold_metrics.recall, fold_metrics.pr_thresh
        
        # because the length of precision and recall vary with the fold (size of thresholds  = nunique(y_pred[:, 1]) + 1), we can't just do
        # precisions.append(precision) and recalls.append(recall)
        # we use a linear interpolation to find the values of precision for a 101 recall chosen values
        recalls.append(interp(mean_precision, precision, recall))

        # plot PR curve
        plt = ax.plot(precision, recall, linewidth=0.6, alpha=0.4,
                      label='PR fold %d' % i)

        # plot thresholds
        if plot_thresholds:
            thresholds = np.append(thresholds, 1.0)
            ax.plot(recall[:len(recall)], thresholds, linewidth=0.6, alpha=0.4, color=plt[0].get_color())
        

    # plot mean PR
    mean_recall = np.mean(recalls, axis=0)
    ax.plot(mean_precision, mean_recall, 'b', linewidth=2, label='mean PR')


    # plot mean PR std
    std_recall = np.std(recalls, axis=0)
    ax.fill_between(mean_precision, mean_recall - std_recall, mean_recall + std_recall, color='blue', alpha=0.15,
                     label='mean PR $\pm$ 1 std. dev.')


    ax.legend(loc='lower left', prop={'size': legend_size})



# plot confusion matrix for each fold
def plot_confusion_matrix(metrics):
    # set plot
    plt.figure(figsize = (4 * metrics.shape[0], 3))

    # for each fold
    for i, fold_metrics in metrics.iterrows():
        cm = pd.DataFrame(fold_metrics.confusion_matrix, index=['False', 'True'], columns=['False', 'True'])
        
        plt.subplot(1, metrics.shape[0], i + 1)
        plt.title('fold %d' % (i + 1))
        
        prop = pd.DataFrame(cm.values / (cm.sum(axis = 1)[:, np.newaxis]), index=['False', 'True'], columns=['False', 'True'])
        labels = prop.applymap(lambda x: '%d%%' % (100 * x)) + cm.applymap(lambda x: ' (%d)' % x)
        
        # plot confusion matrix
        seaborn.heatmap(prop, annot=labels, fmt='s', cmap=plt.cm.Blues, vmin=0, vmax=1, annot_kws={"size": 13})



# old run_model(), not safe to use, not commented, will be removed soon
# the whole cross-validation and metrics evaluation was done by hand without using cross_validate
def run_model_old(model, X, y, cv_strategy, grid_search=False):
    print('Run model')

    metrics = pd.DataFrame(index=range(cv_strategy.get_n_splits()),
                           columns=['fit_time', 'score_time',
                                    'train_accuracy', 'test_accuracy',
                                    'train_roc_auc', 'test_roc_auc',
                                    'test_fpr', 'test_tpr',
                                    'gs_best_parameters', 'gs_cv_results'])
    metrics.index.name = 'fold_number'
    
    i = 0
    
    # for each fold
    for train_index, test_index in cv_strategy.split(X, y):
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

        # auc
        fpr, tpr, thresholds = roc_curve(y_train, y_train_pred) # fpr: false positive rate, tpr: true positive rate
        metrics.iloc[i].train_roc_auc = auc(fpr, tpr)

        fpr, tpr, thresholds = roc_curve(y_test , y_test_pred)
        metrics.iloc[i].test_roc_auc = auc(fpr, tpr)
        metrics.iloc[i].test_fpr = fpr
        metrics.iloc[i].test_tpr = tpr
    
        if grid_search:
            metrics.iloc[i].gs_best_parameters = model.best_params_
            metrics.iloc[i].gs_cv_results = model.cv_results_

        metrics.iloc[i].score_time = time.time() - start

        print(' done! (%.2fs)' % (metrics.iloc[i].fit_time + metrics.iloc[i].score_time))

        i += 1
        
    return metrics



# plot a subplot for each paramater p
# for each subplot:
#   plot a scatter line for each fold with:
#   - x: the parameter p values, the other parameters are fixed to their best values for the fold
#   - y: grid search score for this fold and this parameters set (ie moving parameter p and other parameters fixed)
def plot_grid_search_results(metrics, plot_error_bar = True):
    # get hyper_parameters list
    hyper_parameters = list(metrics.iloc[0].gs_best_parameters.keys())
    
    # boiler plate code to get the number of folds in the nested cross-validation
    n_folds_nested_cross_validation = len([key for key in metrics.iloc[0].gs_cv_results.keys() if key.startswith('split') and key.endswith('_test_score')])
    print('%d hyperparameters tuned for %d different folds (over a %d-fold nested cross-validation):' % (len(hyper_parameters), metrics.shape[0], n_folds_nested_cross_validation))
    
    # print the parameters grid
    max_param_name_length = max([len(p) for p in hyper_parameters])
    for p in hyper_parameters:
        print('  → %s: %s' % (p.ljust(max_param_name_length), np.unique(metrics.iloc[0].gs_cv_results['param_%s' % p])))

    # print the best parameters for each fold
    print('Best hyperparameters for each fold:')
    for i, fold_metrics in metrics.iterrows():
        print('fold %d: %s' % (i, fold_metrics.gs_best_parameters))


    # we plot one subplot of size 10x10 per hyperparameter
    plt.figure(figsize = (10 * len(hyper_parameters), 10))

    # for each hyperparameter
    for (plot_id, moving_parameter) in enumerate(hyper_parameters):
        # get fixed parameters list
        fix_parameters = [p for p in hyper_parameters if p != moving_parameter]

        plt.subplot(1, len(hyper_parameters), plot_id + 1)
        plt.title("Varying '%s' with %s fixed to its(their) best value(s) for each fold" % (moving_parameter, fix_parameters))
        plt.ylabel("score")
        plt.xlabel(moving_parameter)

        # for each fold
        for fold_number in range(metrics.shape[0]):
            # get the grid search results for this fold
            fold_metric = pd.DataFrame(metrics.iloc[fold_number].gs_cv_results)

            # only keep the best hyperparameters values for this fold
            for p in fix_parameters:
                fold_metric = fold_metric.iloc[np.where(fold_metric['param_%s' % p] == metrics.iloc[fold_number].gs_best_parameters[p])]

            x = fold_metric['param_%s' % moving_parameter]
            y = fold_metric['mean_test_score']
            
            # plot score curve
            plot = plt.plot(x, y, '-o', markersize=10, alpha = 0.6, label='fold %d' % (fold_number + 1))

            # plot special marker for the highest value
            plt.plot(x[y.idxmax()], y.max(), 'o',  alpha = 0.6, markersize=20, color=plot[0].get_color())

            # plot error bars
            if plot_error_bar:
                plt.errorbar(x, y, yerr=fold_metric['std_test_score'], capsize=5, label=None, ecolor=plot[0].get_color(), fmt = 'none', alpha = 0.5)
            
        plt.legend(loc='lower right', prop={'size': 15})



# plot learning curves
# strongly inspired by http://scikit-learn.org/stable/auto_examples/model_selection/plot_learning_curve.html
def plot_learning_curves(model, X, y, cv_strategy, figsize=(10, 10)):
    # set plot
    plt.figure(figsize=figsize)
    plt.title('Learning curves')
    plt.xlabel('Number of training examples')
    plt.ylabel('ROC AUC score')

    # get metrics
    train_sizes, train_scores, test_scores = learning_curve(model, X, y, train_sizes=np.linspace(0.1, 1, 10), scoring='roc_auc', cv=cv_strategy, n_jobs=5, error_score='raise')
    train_scores_mean = np.mean(train_scores, axis=1)
    test_scores_mean  = np.mean(test_scores , axis=1)
    test_scores_std   = np.std(test_scores  , axis=1)
    train_scores_std  = np.std(train_scores , axis=1)

    # plot metrics and their standard deviations
    plt.plot(train_sizes, train_scores_mean, 'o-', color='r', markersize = 10, label='mean train score')
    plt.plot(train_sizes, test_scores_mean , 'o-', color='g', markersize = 10, label='mean test score')
    plt.fill_between(train_sizes, train_scores_mean - train_scores_std, train_scores_mean + train_scores_std,
                     alpha=0.1, color='r', label='mean train score $\pm$ 1 std. dev.')
    plt.fill_between(train_sizes, test_scores_mean - test_scores_std, test_scores_mean + test_scores_std,
                     alpha=0.1, color='g', label='mean test score  $\pm$ 1 std. dev.')
    
    plt.legend(loc='best', prop={'size': figsize[0] * 1.5})

