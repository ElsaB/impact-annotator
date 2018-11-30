## Info
- 41,000 variants
- 440 patients
- 9 cancer types
- AUC announced 0.98 but need to retrain the model on TCGA data..


## Similarities
- Paired tumor normal
- Somatic vs artefact
- Manually reviewed knowledge database


## Differences
- On raw output of variant caller
- Also heme tumor not only solid tumor
- 4 classes: somatic, ambiguous, fail, germline
- Different sequencing methods (capture, exome, genome sequencing)
- Features:
    - cancer type (useful only for solid vs liquid?)
    - base quality
    - mapping quality
- Reduce bias on calls otherwise subject to inter-reviewers instability → reviewer study on:
    - Feature importance for reviewers compared to algos
    - Inter-variability
- Identify reviewers errors with the use of the algorithm


## To improve
- Raw output of variant caller too easy
- Machine learning: only 3 models, no grid search on hyperparameters..
- Need to retrain on new data, otherwise really bad results (AUC ~ 0.8)
- Drivers ? -> play on clinical perspective, from the patient to the clinical report
- Not easy (not .maf file), easier features -> could play on this
- Not unified by patient/mutation ?