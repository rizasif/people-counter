import face_recognition
import numpy as np
from PIL import Image

def get_sharpness(image):
    pil_image = Image.fromarray(image)
    pil_image = pil_image.convert('L')
    array = np.asarray(pil_image, dtype=np.int32)

    gy, gx = np.gradient(array)
    gnorm = np.sqrt(gx**2 + gy**2)
    sharpness = np.average(gnorm)
    return float(sharpness)

def calculate_beleif(image1, image2):
    s1 = get_sharpness(image1)
    s2 = get_sharpness(image2)
    d = abs(s1 - s2)
    if d==0:
        d =1
    return float(d)/float(100)

def threshold(val):
    val = float(1) + (val/float(75))
    return val

def get_result(p1,p2,p3):
    # print "Checking {} : {}".format(p1,p2)

    image1 = face_recognition.load_image_file("../data/" + p1)
    image2 = face_recognition.load_image_file("../data/" + p2)
    image3 = face_recognition.load_image_file("../data/" + p3)

    face_encoding1 = face_recognition.face_encodings(image1)[0]
    face_encoding2 = face_recognition.face_encodings(image2)[0]
    face_encoding3 = face_recognition.face_encodings(image3)[0]

    face_encoding1 = np.array(face_encoding1)
    face_encoding2 = np.array(face_encoding2)
    face_encoding3 = np.array(face_encoding3)

    # b = calculate_beleif(image1, image2)
    # print "Belief Factor: ", b

    s1 = get_sharpness(image1)
    s2 = get_sharpness(image2)
    s3 = get_sharpness(image3)

    # print "Original Image1 Belief: ", s1
    # print "Original Image2 Belief: ", s2

    bs1 = threshold(s1)
    bs2 = threshold(s2)
    bs3 = threshold(s3)

    # print "Image1 Belief: ", bs1
    # print "Image2 Belief: ", bs2

    face_encoding1 = face_encoding1*bs1
    face_encoding2 = face_encoding2*bs2
    face_encoding3 = face_encoding3*bs3

    print "Image1 Sum: ", np.sqrt(np.sum(face_encoding1**2))
    print "Image2 Sum: ", np.sqrt(np.sum(face_encoding2**2))
    print "Image3 Sum: ", np.sqrt(np.sum(face_encoding3**2))

    results = face_recognition.compare_faces([face_encoding2, face_encoding3], face_encoding1)
    # print "results: ", results
    return results


#--------------------------------------------------
typeA = ['faceA1.png', 'faceA2.png', 'faceA3.png']
typeB = ['faceB1.png', 'faceB2.png']
typeC = ['faceC1.png', 'faceC2.png', 'faceC3.png']
typeD = ['faceD1.png', 'faceD2.png']
typeE = ['faceE1.png', 'faceE2.png']

AllTypes = [typeA, typeB, typeC, typeD, typeE]

print get_result(typeA[0], typeB[1], typeB[0])
