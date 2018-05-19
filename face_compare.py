import face_recognition

image1 = face_recognition.load_image_file("data/test2.png")
image2 = face_recognition.load_image_file("data/test2.png")

face_encoding1 = face_recognition.face_encodings(image1)[0]
face_encoding2 = face_recognition.face_encodings(image2)[0]

results = face_recognition.compare_faces([face_encoding1], face_encoding2)
print results