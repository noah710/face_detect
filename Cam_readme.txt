in linux, run
xhost +local:root
docker build -f Dockerfile -t image_name .
docker run -it -v ~/SOME_DIR_TO_MOUNT:/MOUNT_POINT --user="root" --env="DISPLAY" --volume="/etc/group:/etc/group:ro" --volume="/etc/passwd:/etc/passwd:ro" --volume="/etc/shadow:/etc/shadow:ro" --volume="/etc/sudoers.d:/etc/sudoers.d:ro" --volume="/tmp/.X11-unix:/tmp/.X11-unix:rw" --env QT_X11_NO_MITSHM=1 IMAGE_NAME
