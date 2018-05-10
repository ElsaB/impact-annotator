# impact-annotator

**Build an automatic annotator of driver mutations from IMPACT data.**

The structure of the repo is the following:

- **data**

raw data and main processed data.

this should not be versionned.

processed data should be reproducible from raw data.

- **doc**

usefull documentation, biblo, slides for talks...

- **src**

main scripts that are used across analysis.
eg: predictors, cross-validation scripts, evaluation scripts.

- **analysis**

folder where you design and run analysis.
this should be split into several sub-folders.
eg:
	- description
	- predictions
	- validation

I suggest that within those sub-folders we create entry folder in the form YYMMDD.


- **results**

folder where we summarize the main results in a mardown.

the markdown should have entries in the form YYMMDD that can point to other markdown from the analysis part.
