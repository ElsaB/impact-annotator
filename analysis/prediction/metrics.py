import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as seaborn

from sklearn.metrics import roc_curve, precision_recall_curve, confusion_matrix
from sklearn.model_selection import cross_validate, learning_curve
import time

class Metrics():

    def __init__(self, model=None, X=None, y=None, cv_strategy=None, groups=None, scoring=['average_precision', 'roc_auc', 'precision', 'recall', 'f1', 'accuracy'], n_jobs=1, run_model=True,
                 read_from_pkl=False, path=None):

        self.scoring = scoring

        if not read_from_pkl:
            self.number_of_folds = cv_strategy.get_n_splits()

            self.metrics = pd.DataFrame(index=range(self.number_of_folds),
                                        columns=['fit_time', 'score_time', 'estimator'] +
                                                ['train_{}'.format(score_name) for score_name in scoring] +
                                                ['test_{}'.format(score_name) for score_name in scoring] +
                                                ['gs_best_parameters', 'gs_cv_results'] + 
                                                ['y_test', 'y_proba_pred', 'y_class_pred',
                                                 'test_fpr', 'test_tpr', 'roc_thresh',
                                                 'precision', 'recall', 'pr_thresh',
                                                 'confusion_matrix'])
            self.metrics.index.name = 'fold_number'

            self.model = model
            self.groups = groups
            self.X = X
            self.y = y
            self.cv_strategy = cv_strategy
            
            self.n_jobs = n_jobs

            if run_model:
                self.run_model()
        else:
            self.metrics = pd.read_pickle(path)
            self.number_of_folds = self.metrics.shape[0]


    # display the self.metrics DataFrame
    def display(self):
        display(self.metrics)


    def get_metrics(self):
        return self.metrics

    def save(self):
        self.metrics.to_pickle('metrics.pkl')

    # run the given model with the given parameters
    # return a pandas DataFrame object containing all the relevant metrics, including the grid search metrics when a grid_search was performed
    def run_model(self):
        print('Run model...', end='')
        start = time.time()

        # get cross validation metrics
        results = cross_validate(self.model, self.X, self.y, groups=self.groups, cv=self.cv_strategy, scoring=self.scoring,
                                 return_train_score=True, return_estimator=True, n_jobs=self.n_jobs, error_score='raise')
        self.metrics.update(pd.DataFrame(results))

        # get grid search metrics if the model seems to have performed a grid search
        if hasattr(self.metrics.iloc[0]['estimator'], 'best_params_'):
            self.metrics['gs_best_parameters'] = self.metrics['estimator'].apply(lambda x: x.best_params_)
            self.metrics['gs_cv_results']      = self.metrics['estimator'].apply(lambda x: x.cv_results_)


        # get ROC curve, precision-recall curve and confusion matrix, warning this implies:
        # - creating the cross-validation folds again
        # - re-testing the fitted model on the test folds
        self._get_other_metrics()


        # we remove the estimators from the metrics because they can be quite memory-expensive (for random forest with a lot of trees for example)
        self.metrics.drop('estimator', axis=1, inplace=True)


        print(' done! ({:.2f}s)'.format(time.time() - start))
    


    # add to metrics the necessary metrics to compute later the ROC curve, precision-recall curve and confusion matrix for each fold
    # also adds the predicted probability, the predicted class for each sample and the true value
    # only used in run_model()
    def _get_other_metrics(self):
        # for each fold
        for i, (train_index, test_index) in enumerate(self.cv_strategy.split(self.X, self.y, groups=self.groups)):
            (X_train, X_test) = (self.X.iloc[train_index], self.X.iloc[test_index])
            (y_train, y_test) = (self.y.iloc[train_index], self.y.iloc[test_index])

            fold_metrics = self.metrics.iloc[i].copy(deep=False)
            
            ## predicted probability metrics
            fold_metrics['y_test']       = y_test.values
            fold_metrics['y_proba_pred'] = fold_metrics['estimator'].predict_proba(X_test)[:,1]
            fold_metrics['y_class_pred'] = fold_metrics['estimator'].predict(X_test)

            ## ROC metrics       
            fpr, tpr, roc_thresholds = roc_curve(fold_metrics['y_test'], fold_metrics['y_proba_pred'])
            fold_metrics['test_fpr']   = fpr
            fold_metrics['test_tpr']   = tpr
            fold_metrics['roc_thresh'] = roc_thresholds

            ## precision-recall metrics       
            precision, recall, pr_thresholds = precision_recall_curve(fold_metrics['y_test'], fold_metrics['y_proba_pred'])
            fold_metrics['precision'] = precision
            fold_metrics['recall']    = recall
            fold_metrics['pr_thresh'] = pr_thresholds

            ## confusion matrix metrics
            #y_pred_25 = (metrics.iloc[i].y_proba_pred >= 0.25)
            #y_pred_50 = (metrics.iloc[i].y_proba_pred >= 0.5) # equivalent to y_pred_05 = metrics.iloc[i].estimator.predict(X_test):
            #y_pred_75 = (metrics.iloc[i].y_proba_pred >= 0.75)            

            fold_metrics['confusion_matrix'] = confusion_matrix(fold_metrics['y_test'], fold_metrics['y_class_pred'])



    # print the average test set accuracy, test ROC AUC and test F1-score for a given metrics DataFrame
    def print_mean(self):
        # test set mean metrics and standard_deviation over the folds
        for score_name in self.scoring:
            test_scores = self.metrics['test_{}'.format(score_name)]
            print('▴ Mean {:17}: {:.3f} ± {:.3f}'.format(score_name, test_scores.mean(), test_scores.std()))



    # print multiple metrics values for the train and test set accross each folds, including the grid search metrics when a grid_search was performed
    # set detailed_grid_search_metrics to True when you want the detailed grid search metrics
    def print_fold_details(self, detailed_grid_search_metrics=False):
        
        # boolean variable being True if the metrics DataFrame contains grid search metrics
        grid_search = not pd.isnull(self.metrics.iloc[0]['gs_best_parameters'])

        print('Fold #: [fit_time | score_time]')
        print('  → score_name_1: [test_score_1 | train_score_1]')
        print('  → score_name_2: [test_score_2 | train_score_2]')
        print('  → ...')


        if grid_search:
            print('  → best hyperparameters: {\'hyperparameter_name_1\': best_value, ...}')

            if detailed_grid_search_metrics:
                print('     - mean_test_score ± std_test_score for {hyperparameters_set #1}')
                print('     - mean_test_score ± std_test_score for {hyperparameters_set #2}')
                print('     - ...')

        print()

        # for each fold
        for i, fold_metrics in self.metrics.iterrows():
            print('Fold {}: [{:.2f}s | {:.2f}s]'.format(i + 1, fold_metrics.fit_time, fold_metrics.score_time))

            for score_name in self.scoring:
                print('  → {:17}: [{:.3f} | {:.3f}]'.format(score_name, fold_metrics['test_{}'.format(score_name)], fold_metrics['train_{}'.format(score_name)]))

            if grid_search:
                print('  → best hyperparameters: {}'.format(fold_metrics['gs_best_parameters']))

                if detailed_grid_search_metrics:
                    for mean, std, param in zip(fold_metrics.gs_cv_results['mean_test_score'],
                                                fold_metrics.gs_cv_results['std_test_score'],
                                                fold_metrics.gs_cv_results['params']):
                        print('     - {:.3f} ± {:.3f} for {}'.format(mean, std, param))



    # plot ROC curve, PR curve and predicted probability distribution side by side
    def plot_threshold_decision_curves(self, figsize=(30, 10), plot_thresholds=True, show_folds_legend=True):
        fig, (ax0, ax1, ax2) = plt.subplots(1, 3, figsize=figsize)

        legend_size = figsize[0] / 3 * 1.5

        self.plot_roc(ax0, legend_size, plot_thresholds, show_folds_legend)
        self.plot_precision_recall(ax1, legend_size, plot_thresholds, show_folds_legend)
        self.plot_probability_distribution(ax2, legend_size)



    # plot ROC curve for each fold (and the associated threshold) and a mean ROC curve
    # strongly inspired by http://scikit-learn.org/stable/auto_examples/model_selection/plot_roc_crossval.html
    def plot_roc(self, ax, legend_size, plot_thresholds=True, show_folds_legend=True):
        # set plot
        ax.set_title('ROC curve for {} folds'.format(self.number_of_folds))
        ax.set_xlabel('false positive rate')
        ax.set_ylabel('true positive rate  |  threshold value')
        ax.set_xlim(-0.05, 1.05)
        ax.set_ylim(-0.05, 1.05)
        

        mean_fpr = np.linspace(0, 1, 101) # [0, 0.01, 0.02, ..., 0.09, 1.0]
        tprs = [] # true positive rate list for each fold


        # for each fold
        for i, fold_metrics in self.metrics.iterrows():
            fpr, tpr, thresholds = fold_metrics['test_fpr'], fold_metrics['test_tpr'], fold_metrics['roc_thresh']

            # because the length of fpr and tpr vary with the fold (size of thresholds  = nunique(y_pred[:, 1]) + 1), we can't just do
            # fprs.append(fpr) and tprs.append(tpr)
            # we use a linear interpolation to find the values of fpr for a 101 chosen tpr values
            tprs.append(np.interp(mean_fpr, fpr, tpr))
            tprs[-1][0] = 0.0 # threshold > 1 for the first point (ie the last tpr value, we correct the interpolation)

            # plot ROC curve
            if show_folds_legend:
                label = 'ROC fold %d (AUC = %0.3f)' % (i + 1, fold_metrics['test_roc_auc'])
            else:
                label = None
            plt = ax.plot(fpr, tpr, linewidth=0.6, alpha=0.4, label=label)

            # plot thresholds
            if plot_thresholds:
                thresholds[0] = 1.001 # value is > 1, we set it just above one for the graphic
                ax.plot(fpr, thresholds, linewidth=0.6, alpha=0.4, color=plt[0].get_color())

        
        # plot baseline
        ax.plot([0, 1], [0, 1], '--r', linewidth=0.5, alpha=1, label='random')


        # plot mean ROC
        mean_tpr = np.mean(tprs, axis=0)
        ax.plot(mean_fpr, mean_tpr, 'b', linewidth=2,
                label='mean ROC (AUC = {:.3f} ± {:.3f})'.format(self.metrics['test_roc_auc'].mean(), self.metrics['test_roc_auc'].std()))


        # plot mean ROC std
        std_tpr = np.std(tprs, axis=0)
        ax.fill_between(mean_fpr, mean_tpr - std_tpr, mean_tpr + std_tpr, color='blue', alpha=0.15,
                         label='mean ROC ± 1 std. dev.')


        ax.legend(loc='lower right', prop={'size': legend_size})



    # plot Precision-Recall curve (PR) for each fold (and the associated threshold) and a mean PR curve
    # strongly inspired by previous function
    # see https://classeval.wordpress.com/introduction/introduction-to-the-precision-recall-plot/
    # WARNING: for simplicity we use linear interpolation but this is wrong (cf. previous website)
    def plot_precision_recall(self, ax, legend_size, plot_thresholds=True, show_folds_legend=True):
        # set plot
        ax.set_title('Precision-Recall curve for {} folds'.format(self.number_of_folds))
        ax.set_xlabel('recall')
        ax.set_ylabel('precision  |  threshold value')
        ax.set_xlim(-0.05, 1.05)
        ax.set_ylim(-0.05, 1.05)
        

        mean_recall = np.linspace(0, 1, 101) # [0, 0.01, 0.02, ..., 0.09, 1.0]
        precisions = [] # precision value list for each fold


        # for each fold
        for i, fold_metrics in self.metrics.iterrows():
            precision, recall, thresholds = fold_metrics['precision'], fold_metrics['recall'], fold_metrics['pr_thresh']
            
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
            if show_folds_legend:
                label = 'PR fold %d (AP = %0.3f)' % (i + 1, fold_metrics['test_average_precision'])
            else:
                label = None
            plt = ax.plot(recall, precision, linewidth=0.6, alpha=0.4, label=label)

            # plot thresholds
            if plot_thresholds:
                # cf last comment on sklearn documentation, there's no threshold for the first point so we don't plot it
                ax.plot(recall[:-1], thresholds, linewidth=0.6, alpha=0.4, color=plt[0].get_color())
            

        # plot baseline
        # see website
        positive_number = self.metrics['y_test'].apply(lambda x: sum(x)).sum()
        negative_number = self.metrics['y_test'].apply(lambda x: sum(~x)).sum()
        positive_proportion = positive_number / (positive_number + negative_number)
        ax.plot([0, 1], [positive_proportion, positive_proportion], '--r', linewidth=0.5, alpha=1, label='random')


        # plot mean PR
        mean_precision = np.mean(precisions, axis=0)
        ax.plot(mean_recall, mean_precision, 'b', linewidth=2,
                label='mean PR (AP = {:.3f} ± {:.3f})'.format(self.metrics['test_average_precision'].mean(), self.metrics['test_average_precision'].std()))


        # plot mean PR std
        std_precision = np.std(precisions, axis=0)
        ax.fill_between(mean_recall, mean_precision - std_precision, mean_precision + std_precision, color='blue', alpha=0.15,
                         label='mean PR ± 1 std. dev.')


        ax.legend(loc='lower left', prop={'size': legend_size})



    # plot predicted probability distribution for True and False class
    def plot_probability_distribution(self, ax, legend_size):
        # concatenate y_test and y_predicted list from each fold
        y_test      = [value for y_test_fold_list      in self.metrics['y_test']      for value in y_test_fold_list]
        y_predicted = [value for y_predicted_fold_list in self.metrics['y_proba_pred'] for value in y_predicted_fold_list]

        dd = pd.DataFrame({'true_class': y_test, 'predicted_probability': y_predicted})

        # plot predicted probability by class
        seaborn.distplot(dd[dd['true_class'] == True]['predicted_probability'], bins=100,
                         ax=ax, label='True',
                         kde_kws={'bw': 0.01, 'alpha': 1},
                         hist_kws={'alpha': 0.2})
        seaborn.distplot(dd[dd['true_class'] == False]['predicted_probability'], bins=100,
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
    def plot_confusion_matrix(self, figsize=(20, 3), legend_size=12):
        # set plot
        plt.figure(figsize=figsize)

        # for each fold
        for i, fold_metrics in self.metrics.iterrows():
            cm = pd.DataFrame(fold_metrics['confusion_matrix'], index=['False', 'True'], columns=['False', 'True'])
            
            plt.subplot(1, self.number_of_folds, i + 1)
            plt.title('fold {}'.format(i + 1))
            
            prop = pd.DataFrame(cm.values / (cm.sum(axis = 1)[:, np.newaxis]), index=['False', 'True'], columns=['False', 'True'])
            labels = prop.applymap(lambda x: '{:.1f}%'.format(100 * x)) + cm.applymap(lambda x: ' ({})'.format(x))
            
            # plot confusion matrix
            seaborn.heatmap(prop, annot=labels, fmt='s', cmap=plt.cm.Blues, vmin=0, vmax=1, annot_kws={"size": legend_size})



    # work in progress...
    def plot_mean_confusion_matrix(self, figsize=(6, 5), legend_size=16):
        # set plot
        plt.figure(figsize=figsize)
        plt.title('mean confusion matrix over {} folds'.format(self.number_of_folds))
        
        cms = [fold_metrics['confusion_matrix'] for i, fold_metrics in self.metrics.iterrows()]

        mean_cm = pd.DataFrame(np.mean(cms, axis = 0), index=['False', 'True'], columns=['False', 'True'])
        std_cm  = pd.DataFrame(np.std(cms, axis = 0) , index=['False', 'True'], columns=['False', 'True'])
        
        prop = pd.DataFrame(mean_cm.values / (mean_cm.sum(axis = 1)[:, np.newaxis]), index=['False', 'True'], columns=['False', 'True'])
        pstd = pd.DataFrame(std_cm.values  / (mean_cm.sum(axis = 1)[:, np.newaxis]), index=['False', 'True'], columns=['False', 'True'])
        
        labels = prop.applymap(lambda x: '{:.1f}%'.format(100 * x))   + mean_cm.applymap(lambda x: ' ({:.1f})'.format(x)) + '\n' +\
                 pstd.applymap(lambda x: '± {:.1f}%'.format(100 * x)) + std_cm.applymap(lambda x: ' (± {:.1f})'.format(x))
        
        # plot confusion matrix
        seaborn.heatmap(prop, annot=labels, fmt='s', cmap=plt.cm.Blues, vmin=0, vmax=1, annot_kws={"size": legend_size})



    # plot a subplot for each paramater p
    # for each subplot:
    #   plot a scatter line for each fold with:
    #   - x: the parameter p values, the other parameters are fixed to their best values for the fold
    #   - y: grid search score for this fold and this parameters set (ie moving parameter p and other parameters fixed)
    def plot_grid_search_results(self, plot_error_bar = True):
        # get hyper_parameters list
        hyper_parameters = list(self.metrics.iloc[0]['gs_best_parameters'].keys())
        
        # boiler plate code to get the number of folds in the nested cross-validation
        n_folds_nested_cross_validation = len([key for key in self.metrics.iloc[0]['gs_cv_results'].keys() if key.startswith('split') and key.endswith('_test_score')])
        print('%d hyperparameters tuned for %d different folds (over a %d-fold nested cross-validation):' % (len(hyper_parameters), self.number_of_folds, n_folds_nested_cross_validation))
        
        # print the parameters grid
        max_param_name_length = max([len(p) for p in hyper_parameters])
        for p in hyper_parameters:
            print('  → {}: {}'.format(p.ljust(max_param_name_length), np.unique(self.metrics.iloc[0].gs_cv_results['param_{}'.format(p)])))

        # print the best parameters for each fold
        print('Best hyperparameters for each fold:')
        for i, fold_metrics in self.metrics.iterrows():
            print('fold {}: {}'.format(i, fold_metrics['gs_best_parameters']))


        # we plot one subplot of size 10x10 per hyperparameter
        plt.figure(figsize = (10 * len(hyper_parameters), 10))

        # for each hyperparameter
        for (plot_id, moving_parameter) in enumerate(hyper_parameters):
            # get fixed parameters list
            fix_parameters = [p for p in hyper_parameters if p != moving_parameter]

            plt.subplot(1, len(hyper_parameters), plot_id + 1)
            plt.title('Varying "{}" with {} fixed to its(their) best value(s) for each fold'.format(moving_parameter, fix_parameters))
            plt.ylabel('score')
            plt.xlabel(moving_parameter)

            # for each fold
            for fold_number in range(self.number_of_folds):
                # get the grid search results for this fold
                fold_metric = pd.DataFrame(self.metrics.iloc[fold_number]['gs_cv_results'])

                # only keep the best hyperparameters values for this fold
                for p in fix_parameters:
                    fold_metric = fold_metric.iloc[np.where(fold_metric['param_{}'.format(p)] == self.metrics.iloc[fold_number]['gs_best_parameters'][p])]

                x = fold_metric['param_{}'.format(moving_parameter)]
                y = fold_metric['mean_test_score']
                
                # plot score curve
                plot = plt.plot(x, y, '-o', markersize=10, alpha = 0.6, label='fold {}'.format(fold_number + 1))

                # plot special marker for the highest value
                plt.plot(x[y.idxmax()], y.max(), 'o',  alpha = 0.6, markersize=20, color=plot[0].get_color())

                # plot error bars
                if plot_error_bar:
                    plt.errorbar(x, y, yerr=fold_metric['std_test_score'], capsize=5, label=None, ecolor=plot[0].get_color(), fmt = 'none', alpha = 0.5)
                
            plt.legend(loc='lower right', prop={'size': 15})




    # plot learning curves
    # strongly inspired by http://scikit-learn.org/stable/auto_examples/model_selection/plot_learning_curve.html
    def get_learning_curves_metrics(self, train_sizes=np.linspace(0.1, 1, 10), scoring='roc_auc', n_jobs=1):
        print('Run learning curves computation...', end='')
        start = time.time()

        self.lc_train_sizes, self.lc_train_scores, self.lc_test_scores = learning_curve(self.model, self.X, self.y,
                                                                                        train_sizes=train_sizes, cv=self.cv_strategy,
                                                                                        n_jobs=n_jobs, error_score='raise')

        print(' done! ({:.2f}s)'.format(time.time() - start))



    # work in progress...
    def plot_learning_curves(self, figsize=(10, 10)):
        # set plot
        plt.figure(figsize=figsize)
        plt.title('Learning curves')
        plt.xlabel('Number of training examples')
        plt.ylabel('ROC AUC score')

        train_scores_mean = np.mean(self.lc_train_scores, axis=1)
        test_scores_mean  = np.mean(self.lc_test_scores , axis=1)
        test_scores_std   = np.std(self.lc_test_scores  , axis=1)
        train_scores_std  = np.std(self.lc_train_scores , axis=1)

         # plot metrics and their standard deviations
        plt.plot(self.lc_train_sizes, train_scores_mean, 'o-', color='r', markersize = 10, label='mean train score')
        plt.plot(self.lc_train_sizes, test_scores_mean , 'o-', color='g', markersize = 10, label='mean test score')
        plt.fill_between(self.lc_train_sizes, train_scores_mean - train_scores_std, train_scores_mean + train_scores_std,
                         alpha=0.1, color='r', label='mean train score ± 1 std. dev.')
        plt.fill_between(self.lc_train_sizes, test_scores_mean - test_scores_std, test_scores_mean + test_scores_std,
                         alpha=0.1, color='g', label='mean test score ± 1 std. dev.')
        
        plt.legend(loc='best', prop={'size': figsize[0] * 1.5})



    # work in progress...
    # This is *gini importance* (and not the mean decrease accuracy), see https://stackoverflow.com/questions/15810339/how-are-feature-importances-in-randomforestclassifier-determined>
    def plot_features_importance(self, random_forest=False, figsize=(20, 8)):
        print('Fit model...', end='')
        start = time.time()

        self.model.fit(self.X, self.y)

        print(' done! ({:.2f}s)'.format(time.time() - start))
        

        feature_importance = pd.DataFrame({'value': self.model.feature_importances_.tolist()}, index=self.X.columns.tolist())
        feature_importance.sort_values(by='value', axis=0, inplace=True)
        
        if random_forest:
            feature_importance['inter_tree_variability'] = np.std([tree.feature_importances_ for tree in self.model.estimators_], axis=0)
        else:
            feature_importance['inter_tree_variability'] = 0
        
        plt.figure(figsize=figsize)
        
        plt.subplot(1, 2, 1)
        feature_importance.tail(15).value.plot.barh(width=0.85, xerr=feature_importance.tail(15)['inter_tree_variability'], linewidth=0)
            
        plt.subplot(1, 2, 2)
        feature_importance.value.plot.barh(width=0.85, xerr=feature_importance['inter_tree_variability'], linewidth=0)
        plt.tight_layout()

