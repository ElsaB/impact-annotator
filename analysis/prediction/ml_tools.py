import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as seaborn
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
    metrics = cross_validate(model, X, y, cv=cv_strategy, scoring=['accuracy', 'roc_auc', 'f1', 'average_precision'], return_train_score=True, return_estimator=True, n_jobs=n_jobs, error_score='raise')
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
# also adds the predicted probability for each sample and the true value
# only used in run_model()
def get_other_metrics(metrics, X, y, cv_strategy):

    # create empty list for the new metrics
    ## predicted probability metrics
    metrics['y_test']      = [[] for i in range(metrics.shape[0])]
    metrics['y_predicted'] = [[] for i in range(metrics.shape[0])]

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



# print the average test set accuracy, test ROC AUC and test F1-score for a given metrics DataFrame
def print_mean_metrics(metrics):
    # test set mean metrics and 95% confidence interval on the metrics estimate (= 1.96 x standard_deviation)
    print('▴ Mean accuracy    : %0.3f ± %0.3f' % (metrics.test_accuracy.mean()         , 1.96 * metrics.test_accuracy.std()))
    print('▴ Mean ROC AUC     : %0.3f ± %0.3f' % (metrics.test_roc_auc.mean()          , 1.96 * metrics.test_roc_auc.std()))
    print('▴ Mean F1-score    : %0.3f ± %0.3f' % (metrics.test_f1.mean()               , 1.96 * metrics.test_f1.std()))
    print('▴ Average precision: %0.3f ± %0.3f' % (metrics.test_average_precision.mean(), 1.96 * metrics.test_average_precision.std()))



# print multiple metrics values for the train and test set accross each folds, including the grid search metrics when a grid_search was performed
# set detailed_grid_search_metrics to True when you want the detailed grid search metrics
def print_fold_metrics(metrics, detailed_grid_search_metrics=False):
    
    # boolean variable being True if the metrics DataFrame contains grid search metrics
    grid_search = hasattr(metrics.iloc[0], 'gs_best_parameters')

    print('Fold #: [fit_time | score_time]')
    print('  → accuracy     : [test_accuracy      | train_accuracy     ]')
    print('  → ROC AUC      : [test_roc_auc       | train_roc_auc      ]')
    print('  → F1-score     : [test_f1_score      | train_f1_score     ]')
    print('  → avg precision: [test_avg_precision | train_avg_precision]')

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
        print('  → accuracy     : [%.3f | %.3f]' % (fold_metrics.test_accuracy         , fold_metrics.train_accuracy))
        print('  → ROC AUC      : [%.3f | %.3f]' % (fold_metrics.test_roc_auc          , fold_metrics.train_roc_auc ))
        print('  → F1-score     : [%.3f | %.3f]' % (fold_metrics.test_f1               , fold_metrics.train_f1      ))
        print('  → avg precision: [%.3f | %.3f]' % (fold_metrics.test_average_precision, fold_metrics.train_average_precision))

        if grid_search:
            print('  → best hyperparameters: %s' % fold_metrics.gs_best_parameters)

            if detailed_grid_search_metrics:
                for mean, std, param in zip(fold_metrics.gs_cv_results['mean_test_score'],
                                            fold_metrics.gs_cv_results['std_test_score'],
                                            fold_metrics.gs_cv_results['params']):
                    print('      %0.3f ± %0.3f for %s' % (mean, 1.96 * std, param))



# plot ROC curve, PR curve and predicted probability distribution side by side
def plot_threshold_decision_metrics(metrics, figsize=(30, 10), plot_thresholds=True):
    fig, (ax0, ax1, ax2) = plt.subplots(1, 3, figsize=figsize)

    legend_size = figsize[0] / 3 * 1.5

    plot_roc(metrics, ax0, legend_size, plot_thresholds)
    plot_precision_recall(metrics, ax1, legend_size, plot_thresholds)
    plot_probability_distribution(metrics, ax2, legend_size)



# plot ROC curve for each fold (and the associated threshold) and a mean ROC curve
# strongly inspired by http://scikit-learn.org/stable/auto_examples/model_selection/plot_roc_crossval.html
def plot_roc(metrics, ax, legend_size, plot_thresholds=True):
    # set plot
    ax.set_title('ROC curve')
    ax.set_xlabel('false positive rate')
    ax.set_ylabel('true positive rate  |  threshold value')
    ax.set_xlim(-0.05, 1.05)
    ax.set_ylim(-0.05, 1.05)
    

    mean_fpr = np.linspace(0, 1, 101) # [0, 0.01, 0.02, ..., 0.09, 1.0]
    tprs = [] # true positive rate list for each fold


    # for each fold
    for i, fold_metrics in metrics.iterrows():
        fpr, tpr, thresholds = fold_metrics.test_fpr.copy(), fold_metrics.test_tpr.copy(), fold_metrics.roc_thresh.copy()

        # because the length of fpr and tpr vary with the fold (size of thresholds  = nunique(y_pred[:, 1]) + 1), we can't just do
        # fprs.append(fpr) and tprs.append(tpr)
        # we use a linear interpolation to find the values of fpr for a 101 chosen tpr values
        tprs.append(np.interp(mean_fpr, fpr, tpr))
        tprs[-1][0] = 0.0 # threshold > 1 for the first point (ie the last tpr value, we correct the interpolation)

        # plot ROC curve
        plt = ax.plot(fpr, tpr, linewidth=0.6, alpha=0.4,
                      label='ROC fold %d (AUC = %0.3f)' % (i + 1, fold_metrics.test_roc_auc))

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
# see https://classeval.wordpress.com/introduction/introduction-to-the-precision-recall-plot/
# WARNING: for simplicity we use linear interpolation but this is wrong (cf. previous website)
def plot_precision_recall(metrics, ax, legend_size, plot_thresholds=True):
    # set plot
    ax.set_title('Precision-Recall curve')
    ax.set_xlabel('recall')
    ax.set_ylabel('precision  |  threshold value')
    ax.set_xlim(-0.05, 1.05)
    ax.set_ylim(-0.05, 1.05)
    

    mean_recall = np.linspace(0, 1, 101) # [0, 0.01, 0.02, ..., 0.09, 1.0]
    precisions = [] # precision value list for each fold


    # for each fold
    for i, fold_metrics in metrics.iterrows():
        precision, recall, thresholds = fold_metrics.precision.copy(), fold_metrics.recall.copy(), fold_metrics.pr_thresh.copy()
        
        # correct first point precision to make a horizontal line between first and second point
        # from the sklearn documentation: "The last precision and recall values are 1. and 0. respectively and do not have a corresponding
        # threshold. This ensures that the graph starts on the y axis."
        # this methodology is advised by the website quoted at the beginning
        precision[-1] = precision[-2]


        # because the length of precision and recall vary with the fold (size of thresholds  = nunique(y_pred[:, 1]) + 1), we can't just do
        # precisions.append(precision) and recalls.append(recall)
        # we use a linear interpolation to find the values of precision for a 101 chosen recall values
        # WARNING: this is wrong, this choice has been made for simplicity
        # aslo, the documentation for np.interp asks the coordinates where we want to interpolate the values to be sorted, these explains the need to do [::-1]
        # for both recall and precision
        precisions.append(np.interp(mean_recall, recall[::-1], precision[::-1]))

        # plot PR curve
        plt = ax.plot(recall, precision, linewidth=0.6, alpha=0.4,
                      label='PR fold %d (AP = %0.3f)' % (i + 1, fold_metrics.test_average_precision))

        # plot thresholds
        if plot_thresholds:
            # cf last comment on sklearn documentation, there's no threshold for the first point so we don't plot it
            ax.plot(recall[:-1], thresholds, linewidth=0.6, alpha=0.4, color=plt[0].get_color())
        

    # plot baseline
    # see website
    positive_number = metrics.y_test.apply(lambda x: sum(x)).sum()
    negative_number = metrics.y_test.apply(lambda x: sum(~x)).sum()
    positive_proportion = positive_number / (positive_number + negative_number)
    ax.plot([0, 1], [positive_proportion, positive_proportion], '--r', linewidth=0.5, alpha=1, label='random')


    # plot mean PR
    mean_precision = np.mean(precisions, axis=0)
    ax.plot(mean_recall, mean_precision, 'b', linewidth=2,
            label='mean PR (AP = %0.3f $\pm$ %0.3f)' % (metrics.test_average_precision.mean(), 1.96 * metrics.test_average_precision.std()))


    # plot mean PR std
    std_precision = np.std(precisions, axis=0)
    ax.fill_between(mean_recall, mean_precision - std_precision, mean_precision + std_precision, color='blue', alpha=0.15,
                     label='mean PR $\pm$ 1 std. dev.')



    ax.legend(loc='lower left', prop={'size': legend_size})



# plot predicted probability distribution for True and False class
def plot_probability_distribution(metrics, ax, legend_size):
    # concatenate y_test and y_predicted list from each fold
    y_test      = [value for y_test_fold_list      in metrics.y_test      for value in y_test_fold_list]
    y_predicted = [value for y_predicted_fold_list in metrics.y_predicted for value in y_predicted_fold_list]

    dd = pd.DataFrame({'true_class': y_test, 'predicted_probability': y_predicted})

    # plot predicted probability by class
    seaborn.distplot(dd.predicted_probability[dd.true_class == True], bins=100,
                     ax=ax, label='True',
                     kde_kws={'bw': 0.01, 'alpha': 1},
                     hist_kws={'alpha': 0.2})
    seaborn.distplot(dd.predicted_probability[dd.true_class == False], bins=100,
                     ax=ax, label='False',
                     kde_kws={'bw': 0.01, 'alpha': 1},
                     hist_kws={'alpha': 0.2})

    # set plot parameters
    ax.set_xlim(0, 1)
    ax.set_title('predicted probability density by class')
    ax.set_xlabel('predicted probability')
    ax.set_ylabel('density')
    ax.legend(loc='upper center', prop={'size': legend_size});



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
def plot_learning_curves(model, X, y, cv_strategy, figsize=(10, 10), n_jobs=1):
    print('Run learning curves computation...', end='')
    start = time.time()

    # set plot
    plt.figure(figsize=figsize)
    plt.title('Learning curves')
    plt.xlabel('Number of training examples')
    plt.ylabel('ROC AUC score')

    # get metrics
    train_sizes, train_scores, test_scores = learning_curve(model, X, y, train_sizes=np.linspace(0.1, 1, 10), scoring='roc_auc', cv=cv_strategy, n_jobs=n_jobs, error_score='raise')
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

    print(' done! (%.2fs)' % (time.time() - start))



# work in progress...
def add_metrics_to_summary(summary, metrics, name):
    summary.loc[name] = [metrics.test_accuracy.mean(), metrics.test_roc_auc.mean(), metrics.test_f1.mean(), metrics.test_average_precision.mean(),
                         metrics.test_accuracy.std() , metrics.test_roc_auc.std() , metrics.test_f1.std() , metrics.test_average_precision.std()]


# work in progress...
def compare_models(data, colors=None, metrics=['test_accuracy', 'test_f1', 'test_roc_auc', 'test_average_precision'], figsize=(10, 12), error_bars=True):
    display(data[['%s_mean' % m for m in metrics]].style.highlight_max(axis=0, color='yellow').set_precision(3))
    data = data.copy()
    data = data.iloc[::-1].transpose().iloc[::-1]
    
    fig, ax = plt.subplots(1, 1, figsize=figsize)
    if not colors:
        colors = ['darkblue', 'purple', 'grey', 'maroon', 'crimson', 'salmon', 'darkgoldenrod', 'seagreen', 'mediumseagreen']

    metrics_mean = data.loc[['%s_mean' % m for m in metrics]]
    if error_bars:
        metrics_std  = data.loc[['%s_std'  % m for m in metrics]]
    else:
        metrics_std = pd.DataFrame(0, index=data.index, columns=data.columns)

    metrics_std.index = metrics_mean.index

    metrics_mean.plot.barh(ax=ax, width=0.85, color=colors, xerr=metrics_std, error_kw={'ecolor': 'black', 'capsize': 2})
        
    # print text results
    for rect in ax.patches:
        ax.text(rect.get_width() + 0.01 + metrics_std.max().max(), rect.get_y() + rect.get_height() / 2,
                '%.3f' % rect.get_width(), ha='left', va='center', color=rect.get_facecolor(), fontsize=13)

    # invert legend order
    handles, labels = ax.get_legend_handles_labels()
    ax.legend(handles[::-1], labels[::-1], loc='center left', bbox_to_anchor=(1, 0.5), prop={'size':18})
    ax.set_xlim(right=1.05)






