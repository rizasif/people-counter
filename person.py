import math

MALE=1
FEMALE=0

class Person():
    id = int()
    no_of_apperance = int()
    sharpness = float()
    sum_index = float()
    encodings = list()
    pil_image = None
    img_array = list()
    gender_sum = int()
    age_sum = int()
    timestamp = float()

    def __init__(self, sharpness, sum_index, encodings, img_array, timestamp, pil_image=-1, id=-1):
        self.id = id
        self.sharpness = sharpness
        self.sum_index = sum_index
        self.encodings = encodings
        self.img_array = img_array
        if not pil_image == -1:
            self.pil_image = pil_image
        self.no_of_apperance = 0
        self.timestamp = timestamp

    def getSummary(self):
        return {
            'id': self.id,
            'apprearence': self.no_of_apperance,
            'image sharpness': self.sharpness,
            'encoding sum': self.sum_index,
            'gender_sum': self.gender_sum,
            'age_sum': self.age_sum,
            'gender': self.getGender(),
            'age': self.getAge(),
            'timestamp': self.timestamp,
            'filename': self.getFilename()
        }

    def getFilename(self):
        timestamp = str(self.getTimestamp()).split(":")
        last = str(int(float(timestamp[2])))
        return  str(self.getId()) + "_" + timestamp[0] + ":" + timestamp[1] + ":" + last + ".jpg"

    def setTimestamp(self, timestamp):
        self.timestamp = timestamp
    
    def getTimestamp(self):
        return self.timestamp

    def getSumIndex(self):
        return self.sum_index

    def setId(self, id):
        self.id = id
    
    def getId(self):
        return self.id

    def getEncoding(self):
        return self.encodings

    def getSharpness(self):
        return self.sharpness

    def incrementApperance(self):
        self.no_of_apperance += 1

    def updateApprerance(self, val):
        self.no_of_apperance = val

    def getApperance(self):
        return self.no_of_apperance

    def clearPilImage(self):
        self.pil_image = None

    def getPilImage(self):
        assert(self.pil_image)
        return self.pil_image

    def saveImage(self, directory_name):
        assert(directory_name[len(directory_name)-1] == "/")
        assert(self.pil_image)
        assert(self.id > -1)

        if self.pil_image:
            self.pil_image.save(directory_name + self.getFilename(), format="JPEG")
        else:
            print ("WARNING: PIL Image Already Cleared")

    def setGender(self, isMale):
        if isMale:
            self.gender_sum += MALE
        else:
            self.gender_sum += FEMALE

    def getGender(self):
        score = float(self.gender_sum)/float(self.no_of_apperance)
        if score >= 0.5: #0.05
            return MALE
        else:
            return FEMALE

    def getGenderSum(self):
        return self.gender_sum

    def putGender(self, gender_sum):
        self.gender_sum = gender_sum

    def setAge(self, age):
        assert(age > 0)
        self.age_sum += age
        # if self.age_sum > age:
        #     self.age_sum = age

    def getAge(self):
        # return float(self.age_sum)/float(self.no_of_apperance)

        # val = float(self.age_sum)/float(self.no_of_apperance)
        # val += 2.0
        # return val*abs(math.log(val))

        val = float(self.age_sum)/float(self.no_of_apperance)
        return val

    def getAgeSum(self):
        return self.age_sum

    def putAge(self, age_sum):
        self.age_sum = age_sum
        
