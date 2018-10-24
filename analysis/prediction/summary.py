import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as seaborn
from scipy.stats import ttest_rel

from metrics import Metrics

# work in progress...
class Summary():

    def __init__(self, scoring=['average_precision', 'roc_auc', 'precision', 'recall', 'f1', 'accuracy']):

        self.metrics_dict = {}

        self.columns_score_mean = ['test_{}_mean'.format(score_name) for score_name in scoring]
        self.columns_score_std  = ['test_{}_std'.format(score_name)  for score_name in scoring]


        self.summary = pd.DataFrame(columns=self.columns_score_mean + self.columns_score_std + ['color'])
        self.summary.index.name = 'metrics_name'

        self.scoring = scoring


    # display the self.summary DataFrame
    def display(self, highlight_max=True):
        if highlight_max:
            display(self.summary[self.columns_score_mean].style.highlight_max(axis=0, color='salmon').set_precision(3))
        else:
            display(self.summary)


    def add(self, metrics, metrics_name, color):
        self.metrics_dict[metrics_name] = metrics

        self.summary.loc[metrics_name] = [metrics.get_metrics()['test_{}'.format(score_name)].mean() for score_name in self.scoring] +\
                                         [metrics.get_metrics()['test_{}'.format(score_name)].std() for score_name in self.scoring] +\
                                         [color]


    def plot_h(self, figsize=(10, 12)):
        summary_transpose = self.summary.copy().iloc[::-1].transpose().iloc[::-1]

        fig, ax = plt.subplots(1, 1, figsize=figsize)


        mean_metrics = summary_transpose.loc[self.columns_score_mean]
        std_metrics  = summary_transpose.loc[self.columns_score_std]
        std_metrics.index = mean_metrics.index

        mean_metrics.plot.barh(ax=ax, width=0.85, color=self.summary.iloc[::-1]['color'],
                               xerr=std_metrics, error_kw={'ecolor': 'black', 'capsize': 2}, linewidth=0)
            
        # print text results
        for rect in ax.patches:
            ax.text(rect.get_width() + 0.01 + std_metrics.max().max(), rect.get_y() + rect.get_height() / 2,
                    '{:.3f}'.format(rect.get_width()), ha='left', va='center', color=rect.get_facecolor(), fontsize=13)

        # invert legend order
        handles, labels = ax.get_legend_handles_labels()
        ax.legend(handles[::-1], labels[::-1], loc='center left', bbox_to_anchor=(1, 0.5), prop={'size': 18})
        ax.set_xlim(right=1.1)



    def plot(self, figsize=(20, 10)):
        summary_transpose = self.summary.copy().transpose()

        fig, ax = plt.subplots(1, 1, figsize=figsize)

        mean_metrics = summary_transpose.loc[self.columns_score_mean]
        std_metrics  = summary_transpose.loc[self.columns_score_std]
        std_metrics.index = mean_metrics.index

        mean_metrics.plot.bar(ax=ax, width=0.85, color=self.summary['color'],
                               yerr=std_metrics, error_kw={'ecolor': 'black', 'capsize': 1.5}, linewidth=0)
            
        # print text results
        for rect in ax.patches:
            ax.text(rect.get_x() + rect.get_width() / 2, rect.get_height() + 0.01 + std_metrics.max().max(),
                    '{:.3f}'.format(rect.get_height()), ha='center', va='bottom', color=rect.get_facecolor(), fontsize=10, rotation=55)

        xmin, xmax = ax.get_xlim()
        plt.plot(ax.get_xlim(), [1.0, 1.0], '--', alpha=0.5, linewidth=1, color='navy')
        plt.xticks(rotation=0)
        plt.legend(loc='center left', bbox_to_anchor=(1, 0.5), prop={'size': 18})
        plt.ylim(top=1.1)


    def save(self, summary_name):
        self.summary.to_pickle(summary_name)


    def load(self, path):
        self.summary = pd.read_pickle(path)


    def plot_cv_curves(self, figsize=(7, 7), scoring=None):
        if not scoring:
            scoring = self.scoring[::-1]

        plt.figure(figsize=(figsize[0] * len(scoring), figsize[1]))

        for i, score_name in enumerate(scoring):
            plt.subplot(1, len(scoring), i + 1)
            plt.title(score_name)

            j = 0
            for metrics_name, metrics in self.metrics_dict.items():
                metrics.get_metrics()['test_{}'.format(score_name)].plot(style='-o', linewidth=0, label=metrics_name, alpha=0.7, color=self.summary.iloc[j]['color'])
                j += 1

        plt.legend()


    def plot_2_vs_2(self, figsize=(4, 7), scoring=None)
        if not scoring:
            scoring = self.scoring

        plt.figure(figsize=(figsize[0] * len(scoring), figsize[1]))

        for i, score_name in enumerate(scoring):
            plt.subplot(1, len(scoring), i + 1)
            plt.title(score_name)

            metric_x = self.metrics_dict.values[0].get_metrics()['test_{}'.format(score_name)]
            metric_y = self.metrics_dict.values[0].get_metrics()['test_{}'.format(score_name)]

            plt.plot(metric_x, metric_y, style='o', alpha=0.7, label='rel')
            plt.plot(plt.gca().get_xlim(), plt.gca().get_ylim())
            print(ttest_rel(metric_x, metric_y))

        plt.legend()





