import numpy as np
import pandas as pd
import matplotlib
import matplotlib.pyplot as plt
import seaborn as sns


print('Setup environment...', end='')


# set jupyter notebook pandas dataframe output parameters
pd.set_option('display.max_rows', 200)
pd.set_option('display.max_columns', 200)
pd.set_option('display.max_colwidth', 1000)

# set jupyter notebook matplotlib figure output parameters
matplotlib.rcParams['figure.dpi'] = 100
matplotlib.rcParams['figure.figsize'] = (10, 4)

# set the graphics style
sns.set()




print(' done!')
