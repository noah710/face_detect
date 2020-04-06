in linux, run

xhost +local:root

docker build -f Dockerfile -t image_name .

docker run -it -v ~/SOME_DIR_TO_MOUNT:/MOUNT_POINT --user="root" --env="DISPLAY" --volume="/etc/group:/etc/group:ro" --volume="/etc/passwd:/etc/passwd:ro" --volume="/etc/shadow:/etc/shadow:ro" --volume="/etc/sudoers.d:/etc/sudoers.d:ro" --volume="/tmp/.X11-unix:/tmp/.X11-unix:rw" --env QT_X11_NO_MITSHM=1 IMAGE_NAME

cd to face_detect (mount it like -v ~/desktop/face_detect:/face_detect above ^)

python3 recognize_faces_image.py -e lfw.pickle -i PHOTO_OF_AL_GORE -d hog

^ this should open a window in your vm when it runs with the photo and identified face
