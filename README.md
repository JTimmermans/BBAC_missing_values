# BBAC missing value imputation

Python matrix imputation implementation of the [http://www.jmlr.org/papers/volume8/banerjee07a/banerjee07a.pdf](Bregman Block Average Co-clustering (BBAC) algorithm). Currently excecuted using the R functionality from [fnyanez](https://github.com/fnyanez/bbac).

## Getting Started

These instructions will get you a copy of the project up and running on your local machine for development and testing purposes. See deployment for notes on how to deploy the project on a live system.

### Prerequisites

What things you need to install the software and how to install them

```
Give examples
```

### Installing

A step by step series of examples that tell you how to get a development env running

Say what the step will be

```
Give the example
```

And repeat
```
until finished
```

End with an example of getting some data out of the system or using it for a little demo

## Examples

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
```

Output:
```python
[[2.5        3.         3.2        5.1        5.3       ]
 [2.5        3.2        3.         5.         5.5       ]
 [5.2        5.2        6.20142857 3.1        3.2       ]
 [5.19380952 5.         5.         3.2        3.1       ]
 [5.         5.2        5.1        5.79857143 3.1       ]
 [7.8        8.         8.         5.2        5.3       ]
 [7.5        7.8        7.6        5.1        5.2       ]]
```


## Authors

* **Joris Timmermans** - *Initial work* - [GitHub](https://github.com/JTimmermans)

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE.md) file for details

## Acknowledgments

* Hat tip to anyone whose code was used
* Inspiration
* etc

## To Do
* A lot
* More
* Add a license.md
