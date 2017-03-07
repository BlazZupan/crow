# CROW 
============
A scalable implementation of non-negative matrix tri-factorization for multi-processor and multi-GPU environments.

### Quick Setup ###
-------------------

The fastest method is to use provided docker images. If you don't have docker 
installed, please refer to the [Setup manual](https://github.com/acopar/crow/blob/master/docs/setup.md)

```sh
    docker pull acopar/crow:latest
```

Crow docker images makes use of the following external volumes. 
- crow: path to the crow source code 
- data: path to directory with data, mounted read-only.
- cache: path to directory, where the application stores intermediate files. 
Note that cache can take several gigabytes, depending on your data. You can 
safely clean this folder, but note that it may take some time to process the data again. 
- results: this is where the factorized data will be stored.

#### Using docker-compose
First, set location to the crow source code.
```sh
    git clone https://github.com/acopar/crow crow
    cd crow
```
In the same directory as docker-compose.yml provide links to other folders.
```sh
    ln -s <path-to-your-data-folder> data
    mkdir /tmp/crow-cache
    ln -s /tmp/crow-cache cache
    mkdir results
```

```sh
   nvidia-docker-compose up
```

#### Run docker manually

If you run docker container as standalone application, instead of using docker-compose, 
you need to provide path to external volumes manually. 

```sh
   docker run -v <source-dir>:/home/mpirun/crow 
             -v <data-dir>:/home/mpirun/data:ro
             -v <cache-dir>:/home/mpirun/cache 
             -v <results-dir>:/home/mpirun/results
             --rm -it acopar/crow /bin/bash
```

### Test your configuration ###
-------------------------------

Once you have the environment up and running, you can use this script to test if everything works correctly.
```sh
    crow-test
```
This generates a small random dataset and tries to factorize it.

### Data format ###
-------------------
The data can be provided in csv in row-column-value format (regardless of data sparsity). Each row 
in csv file represents one non-zero value in the matrix. In each row, the first column represents index at
first dimension **i**, second column index of second dimension **j** and third column represents the value 
of data matrix **X** at location X[i,j].

For example, consider this 2D matrix:
```
    [[1, 0, 0], [5, 5, 0]]
```
Corresponding data file would look like this:
```
    0,0,1
    1,0,5
    1,1,5
```

### Command line arguments ###
-------------------------

The program takes the following arguments:
- -a: factorization rank, for example k=20, or k=20,l=30 if the factorization ranks differ.
- -b: block configuration, for example 2x2.
- -e: calculate and print error function in each iteration. 
- -g: use this argument to use GPUs. By default, only CPU cores will be used.
- -i: maximum number of iterations.
- -p: parallelization degree: must be equal or less than the number of blocks. 
- -r: update rules. Use nmtf_long for non-orthogonal or nmtf_ding for orthogonal NMTF.
- -s: Use sparse data structures. Do not use this if the matrix density is larger than 10%.
- Last argument is path to data file.

### Usage examples ###
-----------------

Serial configuration using one core, run for 100 iterations.

    crow -i 100 -a k=20 ../data/data.csv

Example usage for 4-GPU run with 2x2 block configuration and factorization rank 20.

    crow -g -p 4 -b 2x2 -a k=20 -i 100 ../data/data.csv

