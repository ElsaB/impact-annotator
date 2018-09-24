import numpy as np
import pandas as pd
import matplotlib
import seaborn as sns

print("Setup environment...", end = "")

pd.set_option('display.max_rows', 200)
pd.set_option('display.max_columns', 200)
pd.set_option('display.max_colwidth', 1000)

matplotlib.rcParams['figure.figsize'] = (5, 4)
matplotlib.rcParams['figure.dpi'] = 300

sns.set()


print(" done!")
