import face_recognition
import numpy as np

<<<<<<< HEAD
image1 = face_recognition.load_image_file("../data/faceD1.png")
image2 = face_recognition.load_image_file("../data/faceA1.png")
=======
image1 = face_recognition.load_image_file("data/faceC1.png")
image2 = face_recognition.load_image_file("data/faceC2.png")
>>>>>>> cf275601db9868094fa3b19aad12370d23d59618

face_encoding1 = face_recognition.face_encodings(image1)[0]
face_encoding2 = face_recognition.face_encodings(image2)[0]

face_encoding1 = np.array(face_encoding1)
face_encoding2 = np.array(face_encoding2)

print "Image 1: ", np.sqrt(np.sum(face_encoding1**2))
print "Image 2: ", np.sqrt(np.sum(face_encoding2**2))

results = face_recognition.compare_faces([face_encoding1], face_encoding2)
print results