from IPython.display import Markdown, display
import pandas as pd


# print markdown string in the notebook
# notebook only!
def print_md(string):
    string = string.replace('\ ', '&nbsp;')
    string = string.replace('\t', '&emsp;')
    string = string.replace('\n', '<br>')
    display(Markdown(string))


# print an error if the current conda environment is not the project conda environment
def check_conda_env(env_name):
    if env_name == 'impact-annotator_env':
        print_md("✅ <span style='color:green'>Working on **impact-annotator_env** conda environment.</span>")
    else:
        print_md("⚠️ <span style='color:red'>Please activate the **impact-annotator_env** conda environment to work with this notebook:</span>\n"
                 "\t\t\ \ <span style='color:blue'>$ source activate impact-annotator_env</span>\n"
                 "\t\t\ \ current environment: " + env_name)


# return a count and frequency table of a categorical serie
def get_table(serie):
    # get the count and convert to dataframe
    table = serie.value_counts().to_frame()

    # rename the first column
    table.rename(columns={table.columns[0]: 'count_'}, inplace=True)

    # create the frequency column
    table['freq_'] = table.apply(lambda x: (x / sum(table.count_) * 100).round(1).astype(str) + "%", axis=0)
    
    return table


# print custom proportion of numerator / denominator
# print_count(5, 10) → "5/10 (50.00%)"
def print_count(numerator, denominator):
    print("%d/%d (%.2f%%)" % (numerator, denominator, 100 * numerator / denominator))
