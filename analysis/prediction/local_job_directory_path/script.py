print("Setup environment...", end = "")
import sys
sys.path.append("../../")

from ml_tools import *
from sklearn.naive_bayes import GaussianNB
print(" done!")

print("Run model...")
model_GaussianNB = GaussianNB()
X, y, cv_strategy = load_dataset("../../../../data")
metrics = run_model(model_GaussianNB, X, y, cv_strategy, print_fold_metrics = True)

print("Save metrics...", end = "")
metrics.to_csv("metrics.csv")
print(" done!")