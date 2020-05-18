# To use with the data science stuff
# FROM jupyter/base-notebook:latest
FROM giodegas/pypy-jupyter:latest

# ENV CLOUD_SDK_VERSION 240.0.0
# RUN bash Anaconda3-2018.12-Linux-x86_64.sh -b && \
#     echo "export PATH="/root/anaconda3/bin:$PATH"" >> ~/.bashrc && \
#     /bin/bash -c "source ~/.bashrc"
# ENV PATH /root/anaconda3/bin:$PATH
# RUN conda update --all

# need to be root to install system packages
USER root

# package dependencies
RUN apt-get update \
    && apt-get -qqy install lsb-release gnupg2 build-essential 

# cleanup
RUN rm -rf /var/lib/apt/lists/*

# # # install custom packages
# RUN conda install --quiet --yes \
#     'libgfortran=3.0.0' \
#     'simplegeneric=0.8.1' \
#     'geopandas=0.6.3' \
#     'seaborn=0.10.0'

RUN pip install --upgrade 'pip'
RUN pip install 'pandas==0.25.3'
# RUN pip install 'time'

# install latest Jupyterlab
# RUN pip install 'jupyterlab==1.2.4a0'
# RUN pip install 'jupyterlab==2.0.0a0' 

# switching back to jovyan
# USER jovyan