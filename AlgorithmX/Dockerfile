# FROM buildpack-deps:buster

# # ensure local pypy is preferred over distribution pypy
# ENV PATH /usr/local/bin:$PATH

# # http://bugs.python.org/issue19846
# # > At the moment, setting "LANG=C" on a Linux system *fundamentally breaks Python 3*, and that's not OK.
# ENV LANG C.UTF-8

# # runtime dependencies
# RUN apt-get update && apt-get install -y --no-install-recommends \
# 		tcl \
# 		tk \
# 	&& rm -rf /var/lib/apt/lists/*

# ENV PYPY_VERSION 7.3.0

# RUN set -ex; \
# 	\
# # this "case" statement is generated via "update.sh"
# 	dpkgArch="$(dpkg --print-architecture)"; \
# 	case "${dpkgArch##*-}" in \
# # amd64
# 		amd64) pypyArch='linux64'; sha256='d3d549e8f43de820ac3385b698b83fa59b4d7dd6cf3fe34c115f731e26ad8856' ;; \
# # arm64v8
# 		arm64) pypyArch='aarch64'; sha256='b900241bca7152254c107a632767f49edede99ca6360b9a064141267b47ef598' ;; \
# # i386
# 		i386) pypyArch='linux32'; sha256='7045b295d38ba0b5ee65bd3f078ca249fcf1de73fedeaab2d6ad78de2eab0f0e' ;; \
# # ppc64le
# 		ppc64el) pypyArch='ppc64le'; sha256='d6f3b701313df69483b43ebdd21b9652ae5e808b2eea5fbffe3b74b82d2e7433' ;; \
# # s390x
# 		s390x) pypyArch='s390x'; sha256='0fe2f7bbf42ea88b40954d7de773a43179a44f40656f2f58201524be70699544' ;; \
# 		*) echo >&2 "error: current architecture ($dpkgArch) does not have a corresponding PyPy $PYPY_VERSION binary release"; exit 1 ;; \
# 	esac; \
# 	\
# 	savedAptMark="$(apt-mark showmanual)"; \
# 	apt-get update; \
# 	apt-get install -y --no-install-recommends \
# # sometimes "pypy3" itself is linked against libexpat1 / libncurses5, sometimes they're ".so" files in "/usr/local/lib_pypy"
# 		libexpat1 \
# 		libncurses5 \
# # (so we'll add them temporarily, then use "ldd" later to determine which to keep based on usage per architecture)
# 	; \
# 	\
# 	wget -O pypy.tar.bz2 "https://bitbucket.org/pypy/pypy/downloads/pypy3.6-v${PYPY_VERSION}-${pypyArch}.tar.bz2" --progress=dot:giga; \
# 	echo "$sha256 *pypy.tar.bz2" | sha256sum -c; \
# 	tar -xjC /usr/local --strip-components=1 -f pypy.tar.bz2; \
# 	find /usr/local/lib-python -depth -type d -a \( -name test -o -name tests \) -exec rm -rf '{}' +; \
# 	rm pypy.tar.bz2; \
# 	\
# # smoke test
# 	pypy3 --version; \
# 	\
# 	if [ -f /usr/local/lib_pypy/_ssl_build.py ]; then \
# # on pypy3, rebuild ffi bits for compatibility with Debian Stretch+ (https://github.com/docker-library/pypy/issues/24#issuecomment-409408657)
# 		cd /usr/local/lib_pypy; \
# 		pypy3 _ssl_build.py; \
# # TODO rebuild other cffi modules here too? (other _*_build.py files)
# 	fi; \
# 	\
# 	apt-mark auto '.*' > /dev/null; \
# 	[ -z "$savedAptMark" ] || apt-mark manual $savedAptMark > /dev/null; \
# 	find /usr/local -type f -executable -exec ldd '{}' ';' \
# 		| awk '/=>/ { print $(NF-1) }' \
# 		| sort -u \
# 		| xargs -r dpkg-query --search \
# 		| cut -d: -f1 \
# 		| sort -u \
# 		| xargs -r apt-mark manual \
# 	; \
# 	apt-get purge -y --auto-remove -o APT::AutoRemove::RecommendsImportant=false; \
# 	rm -rf /var/lib/apt/lists/*; \
# # smoke test again, to be sure
# 	pypy3 --version; \
# 	\
# 	find /usr/local -depth \
# 		\( \
# 			\( -type d -a \( -name test -o -name tests \) \) \
# 			-o \
# 			\( -type f -a \( -name '*.pyc' -o -name '*.pyo' \) \) \
# 		\) -exec rm -rf '{}' +

# # if this is called "PIP_VERSION", pip explodes with "ValueError: invalid truth value '<VERSION>'"
# ENV PYTHON_PIP_VERSION 20.0.2
# # https://github.com/pypa/get-pip
# ENV PYTHON_GET_PIP_URL https://github.com/pypa/get-pip/raw/d59197a3c169cef378a22428a3fa99d33e080a5d/get-pip.py
# ENV PYTHON_GET_PIP_SHA256 421ac1d44c0cf9730a088e337867d974b91bdce4ea2636099275071878cc189e

# RUN set -ex; \
# 	\
# 	wget -O get-pip.py "$PYTHON_GET_PIP_URL"; \
# 	echo "$PYTHON_GET_PIP_SHA256 *get-pip.py" | sha256sum --check --strict -; \
# 	\
# 	pypy3 get-pip.py \
# 		--disable-pip-version-check \
# 		--no-cache-dir \
# 		"pip==$PYTHON_PIP_VERSION" \
# 	; \
# # smoke test
# 	pip --version; \
# 	\
# 	find /usr/local -depth \
# 		\( \
# 			\( -type d -a \( -name test -o -name tests \) \) \
# 			-o \
# 			\( -type f -a \( -name '*.pyc' -o -name '*.pyo' \) \) \
# 		\) -exec rm -rf '{}' +; \
# 	rm -f get-pip.py

# CMD ["pypy3"]

# FROM pypy:3

# WORKDIR /usr/src/app

# COPY requirements.txt ./
# RUN pip install --no-cache-dir -r requirements.txt

# COPY . .

# CMD [ "pypy3"]

# To use with the data science stuff
FROM jupyter/datascience-notebook:latest
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