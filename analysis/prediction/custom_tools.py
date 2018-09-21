def setup_environment():
    print("Setup environment...", end = "")
    import numpy as np
    import pandas as pd
    import matplotlib
    import matplotlib.pyplot as plt
    import seaborn as sns

    sns.set()

    matplotlib.rcParams['figure.figsize'] = (5, 4)
    matplotlib.rcParams['figure.dpi'] = 200

    print(" done!")



def get_table(serie):
    table = serie.value_counts().to_frame()
    table.rename(columns={table.columns[0]: 'count_'}, inplace = True)
    table['freq_'] = table.apply(lambda x: (x / sum(table.count_) * 100).round(1).astype(str) + "%", axis = 0)
    
    return (table)


def print_count(numerator, denominator):
    print("%d/%d (%.2f%%)" % (numerator, denominator, 100 * numerator / denominator))