# USAGE
# python recognize_faces_image.py --encodings encodings.pickle --image examples/example_01.png 

# import the necessary packages
import face_recognition
import argparse
import pickle
import cv2
import numpy

def resizeImg(scale:int, img):
    width = int(img.shape[1] * scale / 100)
    height = int(img.shape[0] * scale / 100)
    dim = (width, height)
    # resize image
    resized = cv2.resize(img, dim, interpolation = cv2.INTER_AREA)
    return resized

# construct the argument parser and parse the arguments
ap = argparse.ArgumentParser()
ap.add_argument("-e", "--encodings", required=True,
	help="path to serialized db of facial encodings")
ap.add_argument("-i", "--image", required=True,
	help="path to input image")
ap.add_argument("-d", "--detection-method", type=str, default="cnn",
	help="face detection model to use: either `hog` or `cnn`")
args = vars(ap.parse_args())

# load the known faces and embeddings
print("[INFO] loading encodings...")
data = pickle.loads(open(args["encodings"], "rb").read())

# load the input image and convert it from BGR to RGB
image = cv2.imread(args["image"])
image = resizeImg(300,image)
rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

# detect the (x, y)-coordinates of the bounding boxes corresponding
# to each face in the input image, then compute the facial embeddings
# for each face
print("[INFO] recognizing faces...")
boxes = face_recognition.face_locations(rgb,
	model=args["detection_method"])
encodings = face_recognition.face_encodings(rgb, boxes)

# loop over the facial embeddings
for (i, encoding) in enumerate(encodings):
	# attempt to match each face in the input image to our known
	# encodings
	matches = face_recognition.face_distance(data["encodings"],
		encoding)
	
	#find index of minimum value
	result = numpy.where(matches == numpy.amin(matches))
	distance = matches[result]
	if distance > 0.7:
		name = "Unknown"
		(top, right, bottom, left) = boxes[i]
		cv2.rectangle(image, (left, top), (right, bottom), (0, 0, 255), 2)
		y = top - 15 if top - 15 > 15 else top + 15
		cv2.putText(image, name, (left, y), cv2.FONT_HERSHEY_SIMPLEX,
			0.75, (0, 0, 255), 2)
	else:
		# this should make the name that associated with the minimum distance
		name = data["names"][int(result[0])]
		ogName = data["names"][int(result[0])]
		
		(top, right, bottom, left) = boxes[i]
		cv2.rectangle(image, (left, top), (right, bottom), (255, 255, 0), 2)
		y = top - 15 if top - 15 > 15 else top + 15
		cv2.putText(image, name, (left, y), cv2.FONT_HERSHEY_SIMPLEX,
			0.75, (255, 255, 0), 2)
		
		print("Probably: {}".format(name))
		print("[1] Similarity to {} : {}".format(name,distance))
		# Making this loop 10x to show top 10 similar
		for x in range(9):
			matches = numpy.delete(matches, int(result[0]))
		
			result = numpy.where(matches == numpy.amin(matches))
			distance = matches[result]
		
			name = data["names"][int(result[0])]
			print("[{}] Similarity to {} : {}".format((x+2),name,distance))

# show the output image
cv2.imshow("Image", image)
cv2.waitKey(0)