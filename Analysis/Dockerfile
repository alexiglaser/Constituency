FROM jupyter/datascience-notebook:lab-2.1.1

ENV CLOUD_SDK_VERSION 240.0.0

# need to be root to install system packages
USER root

# package dependencies
RUN apt-get update \
    && apt-get -qqy install lsb-release gnupg2 build-essential

# cleanup
RUN rm -rf /var/lib/apt/lists/*

# install custom packages
RUN conda install --quiet --yes \
    # 'libgfortran=3.0.0' \
    # 'simplegeneric=0.8.1' \
    'geopandas=0.6.3' \
    'seaborn=0.10.0'

# RUN conda create -y -n jlab2.0.0 -c conda-forge notebook jupyterlab ipywidgets
# RUN conda activate jlab2.0.0
# RUN jupyter labextension install @jupyter-widgets/jupyterlab-manager

# install latest Juipyterlab
# RUN pip install 'jupyterlab==1.2.4'
# RUN pip install 'jupyterlab==2.1.1'

# switching back to jovyan
USER jovyan