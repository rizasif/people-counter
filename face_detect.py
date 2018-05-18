import face_recognition
from PIL import Image

image = face_recognition.load_image_file("data/test.png")
faces = face_recognition.face_locations(image)

print faces

for location in faces:
	top, right, bottom, left = location
	print "Face Location {} {} {} {}".format(top,right,bottom,left)

	face_image = image[top:bottom, left:right]
	pil_image = Image.fromarray(face_image)
	pil_image.show()

# if len(faces) == 0:
# 	print "No faces found"
 
# else:
# 	print faces
# 	print faces.shape
# 	print "Number of faces detected: " + str(faces.shape[0])
 
# 	for (x,y,w,h) in faces:
# 		cv2.rectangle(image,(x,y),(x+w,y+h),(0,255,0),1)
 
# 	cv2.rectangle(image, ((0,image.shape[0] -25)),(270, image.shape[0]), (255,255,255), -1)
# 	cv2.putText(image, "Number of faces detected: " + str(faces.shape[0]), (0,image.shape[0] -10), cv2.FONT_HERSHEY_TRIPLEX, 0.5,  (0,0,0), 1)
 
# 	cv2.imshow('Image with faces',image)
# 	cv2.waitKey(0)
# 	cv2.destroyAllWindows()
	