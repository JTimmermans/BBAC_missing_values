# BBAC missing value imputation

Python matrix imputation implementation of the [Bregman Block Average Co-clustering (BBAC) algorithm](http://www.jmlr.org/papers/volume8/banerjee07a/banerjee07a.pdf). Currently excecuted using the R functionality from [fnyanez](https://github.com/fnyanez/bbac).

## Getting Started

### Requirements
The packages used are:
* python 3.6.8
* numpy 1.15.4
* rpy2 2.9.4
* seaborn 0.9.0

See the [requirements](requirements.txt) for full list of dependencies.

Before deployment set the correct path to both your R environment, and the location of the bbac.r repository in [rpy2_setup.py](rpy2_setup.py).

### Example

Input:
```python
from BBAC_classes import *
from rpy2_setup import *
import numpy as np

# Generate synthethic data with missing value (0 in this case)
list_of_list = [[2.5, 3.0, 3.2, 5.1, 5.3],
                [2.5, 3.2, 3.0, 5.0, 5.5],
                [5.2, 5.2, 0, 3.1, 3.2],
                [0, 5.0, 5.0, 3.2, 3.1],
                [5.0, 5.2, 5.1, 0, 3.1],
                [7.8, 8.0, 8.0, 5.2, 5.3],
                [7.5, 7.8, 7.6, 5.1, 5.2]]


# Create array from lists and convert to rpy2-array
array = np.array(list_of_list)
Z = numpy_to_r(array)

# Use the prediction algorithm
test = BBAC(Z, n_cltr_r=3, n_cltr_c=2, distance='e')
test.coclustering()
test.predict()
print(test.Z_imputed)

# Visualize results and save as .png
test.visualize(path='C:\yourpath', outname='test', xlabel='Columns', ylabel='Rows')
```

Output:
```python
[[2.5        3.         3.2        5.1        5.3       ]
 [2.5        3.2        3.         5.         5.5       ]
 [5.2        5.2        4.87630952 3.1        3.2       ]
 [4.5607326  5.         5.         3.2        3.1       ]
 [5.         5.2        5.1        4.47345238 3.1       ]
 [7.8        8.         8.         5.2        5.3       ]
 [7.5        7.8        7.6        5.1        5.2       ]]
```
Original matrix with missing values as grey blocks                                                                                      | Imputed matrix
:--------:|:---------:
![Alt text](/images/test_Z.png?raw=true "Original matrix with missing values as grey blocks")  | ![Alt text](/images/test_Z_imputed.png?raw=true "Imputed matrix")


## Authors

* **Joris Timmermans** - *Initial work* - [GitHub](https://github.com/JTimmermans)

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details

## Acknowledgments

* Hat tip to anyone whose code was used
* Inspiration
* etc

## To Do
* A lot
* More
* Add a license.md
