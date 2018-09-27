## conda

Proceed ([y]/n)? y
```bash
conda create --name impact-annotator_env python=3.6 ipython nb_conda_kernels numpy matplotlib seaborn scikit-learn pandas graphviz
source activate impact-annotator_env


source deactivate
conda env remove --name impact-annotator_env
```

YOu can check that it worked by running "!conda env list" in jupyter lab

## virtualenvwrapper
```bash
# ~/.bashrc
source `which virtualenvwrapper.sh`
```

```bash
mkvirtualenv --python=python3.6 impact-annotator_env
pip install ipython nb_conda_kernels numpy matplotlib seaborn scikit-learn pandas graphviz


workon impact-annotator_env


deactivate
rmvirtualenv impact-annotator_env
```

python 3.6
| package      | version |
| ------------ | ------- |
| ipython      | 6.5.0   |
| numpy        | 1.15.1  |
| matplotlib   | 3.0.0   |
| seaborn      | 0.9.0   |
| scikit-learn | 0.19.2  |
| pandas       | 0.23.4  |
...