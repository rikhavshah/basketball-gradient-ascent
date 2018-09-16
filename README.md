# Basketball Gradient Ascent

The code repository for our CMSAC Reproducible Research Competition submission.

# IMPORTANT - For Reproducability
## Cleaning/Extracting the Data
To be able to run the Python3.6 code, the following external Python package dependencies exist:
* numpy
* tqdm
* pandas

The rest of the python packages (os, subprocess, etc) come built in with Python3.6. A necessary shell package that we
used to extract data from the .7z zip files into .json files was with [p7zip](https://www.7-zip.org/download.html). Note
that on a Mac system, this can be installed via HomeBrew with
```{bash}
brew install p7zip
```
To reproduce our analysis, start in the
[DataCleaning](https://github.com/rikhavshah/basketball-gradient-ascent/tree/master/DataCleaning) directory. Due to
GitHub limits and data size, we have included one compressed set of SportVU data as an example. In order to reproduce
the full analysis, one must move the .7z files from the data mirror we used from [this external
repository](https://github.com/sealneaward/nba-movement-data/tree/master/data) into the DataCleaning directory. The
[shots.csv](https://github.com/rikhavshah/basketball-gradient-ascent/blob/master/DataCleaning/shots/shots.csv) file is
also pulled from there and used as our starting point.

The
current
[corresponding_moments.csv](https://github.com/rikhavshah/basketball-gradient-ascent/blob/master/DataCleaning/corresponding_moments.csv)
and
[corresponding_moments_cleaned.csv](https://github.com/rikhavshah/basketball-gradient-ascent/blob/master/DataCleaning/corresponding_moments_cleaned.csv)
files show the resultant output given the sample .7z file. After moving all the SportVU data into the DataCleaning
directory and running the
[DataCleaningMain.py](https://github.com/rikhavshah/basketball-gradient-ascent/blob/master/DataCleaning/DataCleaningMain.py)
script, these output files will be in the correct format for the rest of our analysis.
## Probability Map
To reproduce the probability mesh, one simply needs to run the ProbabilityMapMain.py file from the
[ProbabilityMap](https://github.com/rikhavshah/basketball-gradient-ascent/tree/master/ProbabilityMap) directory. The
data relevant shot data is already extracted from the shot.csv files and putin the directory as well as a numpy array
stored in ProbabilityMap/shot_data.py.
## Defensive Coverage
For this section, the code is written and visualized in R. Required packages are written into the code and run on R
version 3.5.1. To reproduce our results, take the output csv files from DataCleaning that contain the shots and moments,
and move them into the DefensiveCoverage directory, then run the calculation script first, followed by the analysis
script for the visuals.
## Gradient Ascent
For this section, the Python code is supplied in Jupyter notebooks in the [GradientAnalysis]() directory. Simply opening the files in there will allow the
notebooks to run, given that the data is supplied as well.
