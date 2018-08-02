:construction: *work in progress* :construction:

# impact-annotator

**Build an automatic annotator of driver mutations from IMPACT data.**

***

The structure of the repository is the following:

### data
Raw data and main processed data.

This should not be versionned.

Processed data should be reproducible from raw data.

### doc
Useful documentation, biblio, slides for talks...

### src
Main scripts that are used across analysis eg: predictors, cross-validation scripts, evaluation scripts.

### analysis
Folder where you design and run analysis.

This should be split into several sub-folders:
* description
* prediction
* validation

I suggest that within those sub-folders we create entry folder in the form YYMMDD.


### results

Folder where we summarize the main results in a mardown (notebook.md).

The markdown should have entries in the form YYMMDD that can point to other markdowns from the analysis part.
