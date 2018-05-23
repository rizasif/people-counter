import face_recognition
import numpy as np
from person import Person
from PIL import Image

THRESHOLD_NORMALIZER = float(75)

def read_image_from_disk(name):
		return face_recognition.load_image_file("data/" + name)

def getSumIndex(encoding):
    return np.sqrt(np.sum(encoding**2))

def threshold(val):
    val = float(1) + (val/THRESHOLD_NORMALIZER)
    return val

def getEncoding(image, sharpness):
	encoding = face_recognition.face_encodings(image)
	# print "encoding: ", encoding
	if len(encoding) == 0:
		return None

	encoding = encoding[0]
	encoding = np.array(encoding)
	
	thresh = threshold(sharpness)
	return encoding*thresh

def getPilImage(image):
	pil_image = Image.fromarray(image)
	return pil_image

def get_sharpness(pil_image):
	pil_image = pil_image.convert('L')
	array = np.asarray(pil_image, dtype=np.int32)
	
	gy, gx = np.gradient(array)
	gnorm = np.sqrt(gx**2 + gy**2)
	sharpness = np.average(gnorm)
	return float(sharpness)

def getFaces(image):
	'''for each face returns top, right, bottom, left'''
	faces = face_recognition.face_locations(image)
	person_list = list()
	for location in faces:
		top, right, bottom, left = location
		# print "Face Location {} {} {} {}".format(top,right,bottom,left)
		face_image = image[top:bottom, left:right]
		pil_image = getPilImage(face_image)

		'''Calculating Params'''
		face_sharpness = get_sharpness(pil_image)
		face_encoding = getEncoding(face_image, face_sharpness)

		if face_encoding is None:
			print "Face Encoding Failed"
			continue

		face_sum_index = getSumIndex(face_encoding)

		person = Person(sharpness=face_sharpness, sum_index=face_sum_index,
						encodings=face_encoding, pil_image=pil_image, img_array=face_image)
		person_list.append(person)
	return person_list

def compare(encoding, matching_list_of_encodings):
	return face_recognition.compare_faces(matching_list_of_encodings, encoding)