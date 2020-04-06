# This is a sample Dockerfile you can modify to deploy your own app based on face_recognition on the GPU
# In order to run Docker in the GPU you will need to install Nvidia-Docker: https://github.com/NVIDIA/nvidia-docker

# CUDA 10.1 and up does not work with this package
FROM python:3.6-stretch

# Install face recognition dependencies

RUN apt update -y; apt install -y \
git \
cmake \
pkg-config \
wget \
build-essential \
libsm6 \
libxext6 \
libxrender-dev \
vim 

RUN pip3 install scikit-build numpy 

# Install compilers

RUN apt install -y software-properties-common
RUN add-apt-repository ppa:ubuntu-toolchain-r/test
RUN apt update -y; apt install -y gcc-6 g++-6

RUN update-alternatives --install /usr/bin/gcc gcc /usr/bin/gcc-6 50
RUN update-alternatives --install /usr/bin/g++ g++ /usr/bin/g++-6 50

#Install dlib 

RUN git clone -b 'v19.16' --single-branch https://github.com/davisking/dlib.git
RUN cd /dlib && mkdir build

RUN cd /dlib/build && cmake .. -DCMAKE_CXX_COMPILER=g++-6 -DCMAKE_CC_COMPILER=gcc-6 && cmake --build . --config Release
RUN cd /dlib; python3 /dlib/setup.py install --yes USE_AVX_INSTRUCTIONS

# Install the face recognition package

RUN pip3 install face_recognition opencv-python imutils

RUN touch /entrypoint.sh && echo "#!/bin/sh\n/bin/bash" > /entrypoint.sh && chmod +x /entrypoint.sh
ENTRYPOINT ["/entrypoint.sh"]
