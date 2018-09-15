# Basketball Gradient Ascent

The code repository for our CMSAC Reproducible Research Competition submission.

# IMPORTANT - For Reproducability
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
the full analysis, one must move the .7z files from the data mirror we used from [this
repository](https://github.com/sealneaward/nba-movement-data/tree/master/data).
