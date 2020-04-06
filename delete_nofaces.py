from imutils import paths
import face_recognition
import argparse
import pickle
import cv2
import os
import time

# this script will delete all pics with no face in it in a given directory
# use this to prepare a dataset for encoding


def resizeImg(scale:int, img):
    width = int(img.shape[1] * scale / 100)
    height = int(img.shape[0] * scale / 100)
    dim = (width, height)
    # resize image
    resized = cv2.resize(img, dim, interpolation = cv2.INTER_AREA)
    return resized

def drawBoxes(boxes, img):
    for (top, right, bottom, left) in boxes:
        # draw the predicted face name on the image
        cv2.rectangle(img, (left, top), (right, bottom), (0, 255, 0), 2)
        y = top - 15 if top - 15 > 15 else top + 15
        cv2.putText(img, "face", (left, y), cv2.FONT_HERSHEY_SIMPLEX,
            0.75, (0, 255, 0), 2)
    return img

ap = argparse.ArgumentParser()
ap.add_argument("-i", "--dataset", required=True,
    help="path to input directory of faces + images")
args = vars(ap.parse_args())

raw_path = args["dataset"]
imgPaths = list(paths.list_images(raw_path)) #this should be pointing to dataset

deleted = saved = skipped = 0

# iterate through every image found in the provided dataset
for (i, imagePath) in enumerate(imgPaths):
    img = cv2.imread(imagePath)
    rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    if (rgb.shape[0] > 5000) or (rgb.shape[1] > 5000):
        print("Big boi, skipping!")
        skipped += 1
        os.remove(imagePath)
        print("Saved " + str(saved) + " | Deleted " + str(deleted) + " | Skipped " + str(skipped))
        continue
    boxes = face_recognition.face_locations(rgb, number_of_times_to_upsample=0, model="cnn") # again, GPU is a teeny bop so no upsampling 
    if len(boxes) == 0:
        print(str(imagePath) + " is empty! Removing...\n")
        os.remove(imagePath)
        deleted += 1
        print("Saved " + str(saved) + " | Deleted " + str(deleted) + " | Skipped " + str(skipped))
        continue

    # show the output image
    # img = drawBoxes(boxes, img)
    #resized = resizeImg(25,img)
    #cv2.imshow(imagePath, resized)
    #print("should be showing " + imagePath)
    #cv2.waitKey(0)
    #cv2.destroyAllWindows()
    print("Saving " + imagePath)
    print("Saved " + str(saved) + " | Deleted " + str(deleted) + " | Skipped " + str(skipped))
    saved += 1

