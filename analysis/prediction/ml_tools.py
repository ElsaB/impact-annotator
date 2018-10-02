import pandas as pd
import numpy as np
from sklearn.metrics import roc_curve, auc, roc_auc_score
from scipy import interp
import time

# strongly inspired by http://scikit-learn.org/stable/auto_examples/model_selection/plot_roc_crossval.html
def plot_roc(metrics, ax, title = ""):
    mean_fpr = np.linspace(0, 1, 100) # [0, 0.01, 0.02, ..., 0.09]
    tprs = [] # True Positive Rate for each fold

    # plot fold ROC
    for i in range(metrics.shape[0]):
        fpr, tpr = metrics.iloc[i].test_fpr, metrics.iloc[i].test_tpr
        
        
        # because the length of fpr and tpr vary with the fold (size of thersholds  = nunique(y_pred[:, 1]) + 1), we can't just do
        # fprs.append(fpr) and tprs.append(tpr)
        tprs.append(interp(mean_fpr, fpr, tpr)) # linear interpolation to find the values for a 100 tpr
        tprs[-1][0] = 0.0 # threshold > 1 for the first point

        ax.plot(fpr, tpr, linewidth = 0.7, alpha = 0.5,
                label = 'ROC fold %d (AUC = %0.2f)' % (i,  metrics.iloc[i].test_roc_auc))
    

    # plot baseline
    ax.plot([0, 1], [0, 1], '--r', linewidth = 0.5, alpha = 0.8, label = 'random')


    # plot mean ROC
    mean_tpr = np.mean(tprs, axis = 0)
    ax.plot(mean_fpr, mean_tpr, 'b', linewidth = 1,
            label = 'mean ROC (AUC = %0.2f $\pm$ %0.2f)' % (metrics.test_roc_auc.mean(), 1.96 * metrics.test_roc_auc.std()))


    # plot mean ROC std
    std_tprs = np.std(tprs, axis = 0)
    ax.fill_between(mean_fpr, mean_tpr - std_tprs, mean_tpr + std_tprs, color = 'blue', alpha = 0.2,
                     label='$\pm$ 1 std. dev.')


    # set plot parameters
    ax.set_xlim([-0.05, 1.05])
    ax.set_ylim([-0.05, 1.05])
    ax.set_xlabel('False Positive Rate')
    ax.set_ylabel('True Positive Rate')
    ax.set_title(title)
    ax.legend(loc = "lower right", prop = {'size': 10})


def print_fold_metrics(metrics, grid_search = False):
    print("Fold #: [fit_time | score_time]\n",
          "  → accuracy: [test_accuracy | train_accuracy]\n",
          "  → ROC AUC : [test_roc_auc  | train_roc_auc]\n")

    # for each fold
    for i in range(metrics.shape[0]):
        print("Fold %d: [%.2fs | %.2fs]\n"    % (i + 1, metrics.iloc[i].fit_time  , metrics.iloc[i].score_time) +
              "  → accuracy: [%.2f | %.2f]\n" % (metrics.iloc[i].test_accuracy, metrics.iloc[i].train_accuracy) +
              "  → ROC AUC : [%.2f | %.2f]"   % (metrics.iloc[i].test_roc_auc , metrics.iloc[i].train_roc_auc))
        if grid_search:
            print("  → Best parameters : %r"   % metrics.iloc[i].gs_best_parameters)

            for mean, std, parameters in zip(metrics.iloc[i].gs_cv_results['mean_test_score'],
                                             metrics.iloc[i].gs_cv_results['std_test_score'],
                                             metrics.iloc[i].gs_cv_results['params']):
                print("    %0.2f ± %0.2f for %r" % (mean, 1.96 * std, parameters))

def print_grid_search_curves(metrics):
    n_folds = metrics.shape[0]

    fig, ax = plt.subplots(1, n_folds, figsize = (20, 6))


    for i in range(n_folds):
        roc_auc = metrics.iloc[i].gs_cv_results['mean_test_score']
        ax[i].plot(metrics.iloc[i].gs_cv_results['mean_test_score'], metrics.iloc[i].gs_cv_results['params'],
                   linewidth = 0.7, alpha = 0.5, label = 'fold %d' % (i + 1))


def print_mean_metrics(metrics):
    # mean metrics and 95% confidence interval on the metrics estimate (= 1.96 x standard_deviation)
    print("▴ Mean accuracy: %0.2f ± %0.2f\n" % (metrics.test_accuracy.mean(), 1.96 * metrics.test_accuracy.std()) +
          "▴ Mean ROC AUC : %0.2f ± %0.2f"   % (metrics.test_roc_auc.mean() , 1.96 * metrics.test_roc_auc.std()))



def run_model(model, X, y, cv_strategy, grid_search = False):
    print('Run model')

    metrics = pd.DataFrame(index = range(cv_strategy.get_n_splits()),
                           columns = ['fit_time', 'score_time',
                                      'train_accuracy', 'test_accuracy',
                                      'train_roc_auc', 'test_roc_auc',
                                      'test_fpr', 'test_tpr',
                                      'gs_best_parameters', 'gs_cv_results'])
    metrics.index.name = 'fold_number'
    
    i = 0
    
    # for each fold
    for train_index, test_index in cv_strategy.split(X, y):
        print('  - fold %d/%d...' % (i + 1, cv_strategy.get_n_splits()), end = '')
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

