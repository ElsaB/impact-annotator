import numpy as np
import pandas as pd
import matplotlib
import matplotlib.pyplot as plt
import seaborn as sns

print("Setup environment...", end = "")

# Set jupyter lab pandas dataframe output parameters
pd.set_option('display.max_rows', 200)
pd.set_option('display.max_columns', 200)
pd.set_option('display.max_colwidth', 1000)

# Set jupyter lab matplotlib figure output parameters
matplotlib.rcParams['figure.dpi'] = 100;
matplotlib.rcParams['figure.figsize'] = (10, 4)

sns.set()

print(" done!")
