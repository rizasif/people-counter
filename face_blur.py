import face_recognition
import numpy as np
from PIL import Image

image = face_recognition.load_image_file("data/faceA3.png")

pil_image = Image.fromarray(image)
pil_image = pil_image.convert('L')
array = np.asarray(pil_image, dtype=np.int32)

gy, gx = np.gradient(array)
gnorm = np.sqrt(gx**2 + gy**2)
sharpness = np.average(gnorm)

print sharpness