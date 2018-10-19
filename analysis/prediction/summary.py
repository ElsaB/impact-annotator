import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as seaborn

from metrics import *

class Summary():

    def __init__(self, scoring=['accuracy', 'f1', 'roc_auc', 'average_precision']):

        self.columns_score_mean = ['test_{}_mean'.format(score_name) for score_name in scoring]
        self.columns_score_std  = ['test_{}_std'.format(score_name)  for score_name in scoring]


        self.summary = pd.DataFrame(columns=self.columns_score_mean + self.columns_score_std + ['color'])
        self.summary.index.name = 'metrics_name'

        self.scoring = scoring


    # display the self.summary DataFrame
    def display(self, highlight_max=True):
        if highlight_max:
            display(self.summary[self.columns_score_mean].style.highlight_max(axis=0, color='yellow').set_precision(3))
        else:
            display(self.summary)


    def add(self, metrics, metrics_name, color):
        self.summary.loc[metrics_name] = [metrics.get_metrics()['test_{}'.format(score_name)].mean() for score_name in self.scoring] +\
                                         [metrics.get_metrics()['test_{}'.format(score_name)].std() for score_name in self.scoring] +\
                                         [color]


    def plot(self, figsize=(10, 12)):
        summary_transpose = self.summary.copy().iloc[::-1].transpose().iloc[::-1]
        
        fig, ax = plt.subplots(1, 1, figsize=figsize)
        #if not colors:
        #    colors = ['darkblue', 'purple', 'grey', 'maroon', 'crimson', 'salmon', 'darkgoldenrod', 'seagreen', 'mediumseagreen']


        mean_metrics = summary_transpose.loc[self.columns_score_mean]
        std_metrics  = summary_transpose.loc[self.columns_score_std]

        mean_metrics.plot.barh(ax=ax, width=0.85, color=self.summary.iloc[::-1]['color'],
                               xerr=std_metrics, error_kw={'ecolor': 'black', 'capsize': 2})
            
        # print text results
        for rect in ax.patches:
            ax.text(rect.get_width() + 0.01 + std_metrics.max().max(), rect.get_y() + rect.get_height() / 2,
                    '{:.3f}'.format(rect.get_width()), ha='left', va='center', color=rect.get_facecolor(), fontsize=13)

        # invert legend order
        handles, labels = ax.get_legend_handles_labels()
        ax.legend(handles[::-1], labels[::-1], loc='center left', bbox_to_anchor=(1, 0.5), prop={'size': 18})
        ax.set_xlim(right=1.05)