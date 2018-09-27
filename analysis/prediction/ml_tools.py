import pandas as pd
import numpy as np
from sklearn.metrics import roc_curve, auc, roc_auc_score
from scipy import interp
import time



def run_model(model, X, y, cv_strategy, grid_search = False, print_fold_metrics = False, print_grid_search_metrics = False, plot_roc = False, ax = None):
    
    if print_fold_metrics:
        print("Fold #: [fit_time | score_time]\n",
          "  → accuracy: [test_accuracy | train_accuracy]\n",
          "  → ROC AUC : [test_roc_auc  | train_roc_auc]\n")
        
    metrics = pd.DataFrame(index = range(cv_strategy.get_n_splits()),
                           columns = ['fit_time', 'score_time',
                                      'train_accuracy', 'test_accuracy',
                                      'train_roc_auc', 'test_roc_auc',
                                      'test_fpr', 'test_tpr',
                                      'best_parameters'])
    metrics.index.name = 'fold_number'
    
    i = 0
    
    # for each fold
    for train_index, test_index in cv_strategy.split(X, y):
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
        metrics.iloc[i].train_accuracy = model.score(X_train, y_train)
        metrics.iloc[i].test_accuracy  = model.score(X_test , y_test)

        # auc
        fpr, tpr, thresholds = roc_curve(y_train, y_train_pred) # fpr: false positive rate, tpr: true positive rate
        metrics.iloc[i].train_roc_auc = auc(fpr, tpr)

        fpr, tpr, thresholds = roc_curve(y_test , y_test_pred)
        metrics.iloc[i].test_roc_auc = auc(fpr, tpr)
        metrics.iloc[i].test_fpr = fpr
        metrics.iloc[i].test_tpr = tpr
    
        metrics.iloc[i].score_time = time.time() - start
        
        if print_fold_metrics:
            print("Fold %d: [%.2fs | %.2fs]\n"    % (i, metrics.iloc[i].fit_time  , metrics.iloc[i].score_time) +
                  "  → accuracy: [%.3f | %.3f]\n" % (metrics.iloc[i].test_accuracy, metrics.iloc[i].train_accuracy) +
                  "  → ROC AUC : [%.3f | %.3f]"   % (metrics.iloc[i].test_roc_auc , metrics.iloc[i].train_roc_auc))
        
        if grid_search:
            metrics.iloc[i].best_parameters = model.best_params_
            print("  → Best parameters : %r"   % model.best_params_)

            if print_grid_search_metrics:
                for mean, std, parameters in zip(model.cv_results_['mean_test_score'],
                                                 model.cv_results_['std_test_score'],
                                                 model.cv_results_['params']):
                    print("    %0.2f ± %0.2f for %r" % (mean, 1.96 * std, parameters))

        i += 1
    
    print()
    
    # mean metrics and 95% confidence interval on the metrics estimate (= 1.96 x standard_deviation)
    print("## Mean accuracy: %0.2f ± %0.2f\n" % (metrics.test_accuracy.mean(), 1.96 * metrics.test_accuracy.std()) +
          "## Mean ROC AUC : %0.2f ± %0.2f"   % (metrics.test_roc_auc.mean() , 1.96 * metrics.test_roc_auc.std()))
    
    
    # strongly inspired by http://scikit-learn.org/stable/auto_examples/model_selection/plot_roc_crossval.html
    if plot_roc:
        mean_fpr = np.linspace(0, 1, 100) # [0, 0.01, 0.02, ..., 0.09]
        tprs = [] # True Positive Rate for each fold
        
        # plot fold ROC
        for i in range(cv_strategy.get_n_splits()):
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
        ax.legend(loc = "lower right", prop = {'size': 10})
    
    
    metrics.drop(['test_fpr', 'test_tpr'], axis = 1, inplace = True)
    
    return (metrics)
