import face_recognition
import numpy as np
from PIL import Image

THRESHOLD_NORMALIZER = float(50)
THRESHOLD_WEIGHT = float(1.0)

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
    val = THRESHOLD_WEIGHT + (val/THRESHOLD_NORMALIZER)
    return val

def get_result(p1,p2):
    print "Checking {} : {}".format(p1,p2)

    image1 = face_recognition.load_image_file("../data/" + p1)
    image2 = face_recognition.load_image_file("../data/" + p2)

    face_encoding1 = face_recognition.face_encodings(image1)[0]
    face_encoding2 = face_recognition.face_encodings(image2)[0]

    face_encoding1 = np.array(face_encoding1)
    face_encoding2 = np.array(face_encoding2)

    # b = calculate_beleif(image1, image2)
    # print "Belief Factor: ", b

    s1 = get_sharpness(image1)
    s2 = get_sharpness(image2)

    bs1 = threshold(s1)
    bs2 = threshold(s2)

    # print "Image1 Belief: ", bs1
    # print "Image2 Belief: ", bs2

    face_encoding1 = face_encoding1*bs1
    face_encoding2 = face_encoding2*bs2

    print "Sharpness Image1: ", s1
    print "Image1 Sum: ", np.sqrt(np.sum(face_encoding1**2))
    print "Sharpness Image2: ", s2
    print "Image2 Sum: ", np.sqrt(np.sum(face_encoding2**2))

    results = face_recognition.compare_faces([face_encoding1], face_encoding2)
    # print results
    return results[0]


#--------------------------------------------------
typeA = ['faceA1.png', 'faceA2.png', 'faceA3.png']
typeB = ['faceB1.png', 'faceB2.png']
typeC = ['faceC1.png', 'faceC2.png', 'faceC3.png']
typeD = ['faceD1.png', 'faceD2.png']
typeE = ['faceE1.png', 'faceE2.png']
typeF = ['faceF1.png', 'faceF2.png', 'faceF3.png']
typeG = ['faceG1.png', 'faceG2.png', 'faceG3.png']
typeH = ['faceH1.png', 'faceH2.png']
typeI = ['faceI1.png', 'faceI2.png']

AllTypes = [typeA, typeB, typeC, typeD, typeE, typeF, typeG, typeH, typeI]

total = 0
false_negatives = 0
for type in AllTypes:
    if(len(type) == 2):
        if not get_result(type[0], type[1]):
            false_negatives += 1
            # print "False"
        total += 1
    elif(len(type) == 3):
        if not get_result(type[0], type[1]):
            false_negatives += 1
            # print "False"
        if not get_result(type[1], type[2]):
            false_negatives += 1
            # print "False"
        if not get_result(type[0], type[2]):
            false_negatives += 1
            # print "False"
        total += 3
print "\nFalse Negatives {} of {}".format(false_negatives, total)

total = 0
false_positives = 0
for i in range(len(AllTypes)):
    otype = AllTypes.pop()
    for subOType in otype:
        for cType in AllTypes:
            for subCType in cType:
                if get_result(subOType, subCType):
                   false_positives += 1
                #    print "False"
                total += 1 

print "False Positives {} of {}".format(false_positives, total)
