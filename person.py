class Person():
    id = int()
    no_of_apperance = int()
    sharpness = float()
    sum_index = float()
    encodings = list()
    pil_image = None
    img_array = list()

    def __init__(self, sharpness, sum_index, encodings, img_array, pil_image=-1, id=-1):
        self.id = id
        self.sharpness = sharpness
        self.sum_index = sum_index
        self.encodings = encodings
        self.img_array = img_array
        if not pil_image == -1:
            self.pil_image = pil_image
        self.no_of_apperance = 0

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

    def saveImage(self, directory_name):
        assert(directory_name[len(directory_name)-1] == "/")
        assert(self.pil_image)
        assert(self.id > -1)

        if self.pil_image:
            self.pil_image.save(directory_name + str(self.id) + ".jpg", format="JPEG")
        else:
            print "WARNING: PIL Image Already Cleared"
        
