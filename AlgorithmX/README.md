# AlgorithmX

As stated before we will to form the merged constituencies we will use the [Exact Cover](https://en.wikipedia.org/wiki/Exact_cover) problem and [Knuth's Algorithm X](https://en.wikipedia.org/wiki/Knuth%27s_Algorithm_X) to solve it. In order to speed things up we found taht using a [PyPy](https://en.wikipedia.org/wiki/PyPy) kernel sped things up considerably (up to 4-5 times faster for some of the larger problems). As the PyPy kernel is a different implementation of Python we needed to have a separate set up for this part of the project.

1. Once the Docker container has been built, run the container instance 
    ```
    docker run -it -p 8888:8888 -v "$PWD":/home/work <TAG> /bin/bash
    ```
    where "TAG" is the tag name given to the container.
1. launch jupyter notebook server inside the container: 
    ```
    jupyter notebook --allow-root --ip=0.0.0.0 --no-browser
    ```
1. Open the notebook in the usual manner. Once there go to the 'home/work/' folder which should have mounted your local directory.
1. To check if the PyPy kernel is running, open a notebook and run the following command:
    ```
    import sys
    sys.version
    ```
    which should read something like `'3.5.3 (928a4f70d3de, Feb 08 2019, 10:42:58)\n[PyPy 7.0.0 with GCC 6.2.0 20160901]'`.


Many thanks to Giovanni De Gasperis who set up the initial code to run a Jupyter notebook with a PyPy kernel [here](https://github.com/giodegas/docker-pypy-jupyter) and [here](https://hub.docker.com/r/giodegas/pypy-jupyter). 