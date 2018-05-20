class Person():
    id = int()
    sharpness = float()
    sum_index = float()
    encodings = list()

    def __init__(self, id, sharpness, sum_index, encodings):
        self.id = id
        self.sharpness = sharpness
        self.sum_index = sum_index
        self.encodings = encodings

    def getSumIndex(self):
        return self.sum_index
        
