# AlgorithmX

As stated before we will to form the merged constituencies we will use the [Exact Cover](https://en.wikipedia.org/wiki/Exact_cover) problem and [Knuth's Algorithm X](https://en.wikipedia.org/wiki/Knuth%27s_Algorithm_X) to solve it. In order to speed things up we found taht using a [PyPy](https://en.wikipedia.org/wiki/PyPy) kernel sped things up considerably (up to 7 times fast for some of the larger problems). As the PyPy kernel is a different implementation of Python we needed to have a separate set up for this part of the project.

1. Once the Docker container has been built create and run the container instance
`docker run -it -p 8888:8888 -v "$PWD":/home/work <TAG> /bin/bash`
1. launch jupyter notebook server inside the container:
`jupyter notebook --allow-root --ip=0.0.0.0 --no-browser`



Many thanks to Giovanni De Gasperis who set up the code to run a Jupyter notebook with a PyPy kernel [here](https://github.com/giodegas/docker-pypy-jupyter). 