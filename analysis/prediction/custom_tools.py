from IPython.display import Markdown, display
import pandas as pd

def print_md(string):
    string = string.replace('\ ', '&nbsp;')
    string = string.replace('\t', '&emsp;')
    string = string.replace('\n', '<br>')
    display(Markdown(string))


def check_conda_env(env_name):
    try:
        if env_name != 'impact-annotator_env':
            raise Exception("⚠️ <span style='color:red'>Please activate the **impact-annotator_env** conda environment to work with this notebook:</span>\n"
                            "\t\t\ \ <span style='color:blue'>$ source activate impact-annotator_env</span>\n"
                            "\t\t\ \ current environment: " + env_name)
        else:
            print_md("✅ <span style='color:green'>Working on **impact-annotator_env** conda environment.</span>")
    except Exception as e:
        print_md(str(e))


def get_table(serie):
    table = serie.value_counts().to_frame()
    table.rename(columns={table.columns[0]: 'count_'}, inplace = True)
    table['freq_'] = table.apply(lambda x: (x / sum(table.count_) * 100).round(1).astype(str) + "%", axis = 0)
    
    return (table)


def print_count(numerator, denominator):
    print("%d/%d (%.2f%%)" % (numerator, denominator, 100 * numerator / denominator))
