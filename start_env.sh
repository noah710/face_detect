#!/bin/sh

# filth
#xhost +local:root
#nvidia-docker run -it -v ~/faceDetect:/faceDetect --net=host --ipc=host -e DISPLAY="$DISPLAY" --volume="/tmp/.X11-unix:/tmp/.X11-unix:rw" --env QT_X11_NO_MITSHM=1 noah/face_recognition_ws

nvidia-docker run -it -v ~/faceDetect:/faceDetect --user="root" --env="DISPLAY" --volume="/etc/group:/etc/group:ro" --volume="/etc/passwd:/etc/passwd:ro" --volume="/etc/shadow:/etc/shadow:ro" --volume="/etc/sudoers.d:/etc/sudoers.d:ro" --volume="/tmp/.X11-unix:/tmp/.X11-unix:rw" --env QT_X11_NO_MITSHM=1 noah/face_recognition_ws
