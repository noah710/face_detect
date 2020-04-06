from imutils import paths
import face_recognition
import argparse
import cv2
import os
import time

def drawBoxes(boxes, img):
    for (top, right, bottom, left) in boxes:
        # draw the predicted face name on the image
        cv2.rectangle(img, (left, top), (right, bottom), (0, 255, 0), 2)
        y = top - 15 if top - 15 > 15 else top + 15
        cv2.putText(img, "face", (left, y), cv2.FONT_HERSHEY_SIMPLEX,
            0.75, (0, 255, 0), 2)
    return img

def resizeImg(scale:int, img):
    width = int(img.shape[1] * scale / 100)
    height = int(img.shape[0] * scale / 100)
    dim = (width, height)
    # resize image
    resized = cv2.resize(img, dim, interpolation = cv2.INTER_AREA)
    return resized

def main():
    # This script takes in pictures with a face/s
    #   If name is known, suggest name and ask for confirmation
    #   If name is unknown, ask name and add to database for that name

    # ***Will not save encodings!

    ap = argparse.ArgumentParser()
    ap.add_argument("-i", "--images", required=True,
        help="path to input directory of images")
    args = vars(ap.parse_args())

    # need to figure out how to store names and encoding together
    knownEncodings = []
    knownNames = []

    imagePaths = list(paths.list_images(args["images"]))

    for (i, imagePath) in enumerate(imagePaths):
        # read in image as rgb
        # Turns out my images already are rgb. I left the var name as rgb for simplicity
        rgb = cv2.imread(imagePath) #cv2.cvtColor(cv2.imread(imagePath), cv2.COLOR_BGR2RGB) 

        # I'm resizing the pictures to hopefully process them faster
        while ((rgb.shape[1]*rgb.shape[0]) > 2000*2000):
            rgb = resizeImg(75,rgb)

        # get bounding boxes of faces in image
        boxes = face_recognition.face_locations(rgb, number_of_times_to_upsample=0, model="cnn") #TODO: Batch processing

        # get encodings of all faces in boxes
        if len(boxes) == 0: # This shouldnt happen if you use my dataset prep script
            print("[WARN] Image has no faces : {}".format(imagePath))
            while (rgb.shape[1] > 600) and (rgb.shape[0] > 600):
                rgb = resizeImg(80,rgb)
            cv2.imshow("Empty Image", rgb)
            cv2.waitKey(0)
            cv2.destroyAllWindows()
            continue
        encodings = face_recognition.face_encodings(rgb, boxes)

        for (j, encoding) in enumerate(encodings):
            # here we should first check if we've seen this encoding before
            # we can skip this for now and just save the encodings

            # copy the original image so it only shows one box at a time, then draw boxes on the copy
            img = rgb.copy()
            drawBoxes(boxes[j:j+1], img)
            while (img.shape[1] > 600) and (img.shape[0] > 600):
                img = resizeImg(80,img)

            cv2.imshow(imagePath, img)
            print("Showing " + imagePath)
            actionIn = cv2.waitKey(0)
            cv2.destroyAllWindows()

            # you can press s to skip a picture
            if actionIn == ord("s"):
                print("Skipping picture!")
                break
            
            # here we check if we've seen this face before
            matches = face_recognition.compare_faces(knownEncodings, encoding, 
                tolerance=0.5)
            
            # if we've found a match
            foundFlag = False
            name = "Unknown"
            if True in matches:
                matchedIdxs = [i for (i, b) in enumerate(matches) if b] # these idxs should correspond injectively to knownNames
                counts = {} # make this dict to store how many times we've seen each name
                for i in matchedIdxs:
                    name = knownNames[i]
                    counts[name] = counts.get(name, 0) + 1 # if counts[name] is None, return 0, otherwise increment
                name = max(counts, key=counts.get)
                foundFlag = True
            
            if foundFlag:
                nameInput = input("Is this {}? (y/n) ".format(name))
                if nameInput == "n":
                    # ask for name from last shown pic
                    name = input("Whats the name?: ")
            else:
                name = input("Face not found. Whats the name?: ")

            # you can also skip a face with s
            if name == "s":
                print("Skipping face!")
                continue

            # add the encoding and name to arrays injectively
            knownEncodings.append(encoding)
            knownNames.append(name)

if __name__ == "__main__":
    main()