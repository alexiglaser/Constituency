# To use a PyPy kernel
FROM giodegas/pypy-jupyter:latest

# need to be root to install system packages
USER root

# package dependencies
RUN apt-get update \
    && apt-get -qqy install lsb-release gnupg2 build-essential 

# cleanup
RUN rm -rf /var/lib/apt/lists/*

# # install custom packages
RUN pip install --upgrade 'pip'
RUN pip install 'pandas==0.25.3'
RUN pip install "joblib==0.14.1"
RUN pip install "interruptingcow==0.8"
