# BBAC missing value imputation

Python matrix imputation implementation of the [Bregman Block Average Co-clustering (BBAC) algorithm](http://www.jmlr.org/papers/volume8/banerjee07a/banerjee07a.pdf). Currently BBAC statistics are calculated using the R repository from [fnyanez](https://github.com/fnyanez/bbac), small adjustments have been made to incorporate the full capability of the W matrix.

## Getting Started

### Requirements
The packages used are:
* python 3.6.8
* numpy 1.15.4
* rpy2 2.9.4
* seaborn 0.9.0

See the [requirements](requirements.txt) for full list of dependencies.

Before deployment set the correct path to your R environment in [rpy2_setup.py](rpy2_setup.py).

### Example

Input:
```python
    from BBAC_classes import *

    # Generate synthethic data, 0's indicate missing values
    list_of_list = [[2.5, 3.0, 3.2, 5.1, 5.3],
                    [2.5, 3.2, 3.0, 5.0, 0.0],
                    [5.0, 5.2, 5.1, 3.2, 3.1],
                    [5.2, 5.2, 0.0, 3.1, 3.2],
                    [0.0, 5.0, 5.0, 3.2, 3.1],
                    [7.8, 8.0, 8.0, 5.2, 5.3],
                    [7.5, 7.8, 7.6, 5.1, 0.0]]

    # Create array from lists and convert to rpy2-array
    array = np.array(list_of_list)
    Z = numpy_to_r(array)

    # Use the prediction algorithm
    test = BBAC(Z, n_cltr_r=3, n_cltr_c=2, distance='d', scheme=2)
    test.coclustering()
    test.predict()
    
    # Visualize arrays and print imputed array
    test.visualize(path=r'D:\g_drive\Gima\Thesis\Media', outname='test', xlabel='Columns', ylabel='Rows')
    print(test.Z_imputed)
```

Output:
```python
[[2.5 3.  3.2 5.1 5.3]
 [2.5 3.2 3.  5.  5.5]
 [5.  5.2 5.1 5.2 3.1]
 [5.2 5.2 5.2 3.1 3.2]
 [5.2 5.  5.  3.2 3.1]
 [7.8 8.  8.  5.2 5.3]
 [7.5 7.8 7.6 5.1 5.2]]
```
Original matrix with missing values as grey blocks                                                                                      | Imputed matrix
:--------:|:---------:
![Alt text](/images/Z.png?raw=true "Original matrix with missing values as grey blocks")  | ![Alt text](/images/Z_imputed.png?raw=true "Imputed matrix")


## Authors

* **Joris Timmermans** - *Initial work* - [GitHub](https://github.com/JTimmermans)

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details

## Acknowledgments

* [Fnyanez](https://github.com/fnyanez/bbac) for implementing the BBAC algorithm in R.
* Raul Zurita-Milla for supervising the project as part of my MSC thesis. 


