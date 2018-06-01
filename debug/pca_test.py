import face_recognition
import numpy as np


image1 = face_recognition.load_image_file("../data/faceC1.png")
image2 = face_recognition.load_image_file("../data/faceC2.png")

face_encoding1 = face_recognition.face_encodings(image1)[0]
face_encoding2 = face_recognition.face_encodings(image2)[0]

face_encoding1 = np.array(face_encoding1)
face_encoding2 = np.array(face_encoding2)

print pca(face_encoding1)