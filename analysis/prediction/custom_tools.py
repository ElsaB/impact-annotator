from IPython.display import Markdown, display
import pandas as pd

# print markdown string in the notebook
def print_md(string, color=None):
    string = string.replace('\t', '&emsp;')
    string = string.replace('\n', '<br>')
    if color:
        string = '<span style="color:' + color + '">' + string + '</span>'

    display(Markdown(string))


# return a count and frequency table of a categorical pandas Serie
def get_table(data):
    # get the count and convert to dataframe
    table = data.value_counts().to_frame()

    # rename the first column
    table.rename(columns={table.columns[0]: 'count_'}, inplace=True)

    # create the frequency column
    table['freq_'] = table.apply(lambda x: (x / sum(table.count_) * 100).round(1).astype(str) + "%", axis=0)
    
    return table


# print custom proportion of numerator / denominator
# ex: print_count(5, 10) → "5/10 (50.00%)"
def print_count(numerator, denominator):
    print("%d/%d (%.2f%%)" % (numerator, denominator, 100 * numerator / denominator))


def unlist(l):
    return [x for sublist in l for x in sublist]