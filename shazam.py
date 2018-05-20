import face_recognition
import numpy as np
from PIL import Image

from person import Person

SEARCH_THRESHOLD = float(0.10)

class Shazam():

	def __init__(self):
		self.next_id = int()
		self.personList = list()
		self.sorted_sum_index = list()

	def sortSumIndexes(self):
		self.sorted_sum_index = sorted(self.personList,
										key=lambda shell:shell.getSumIndex())

	def checkInRange(self, val, first, last):
		return (val >= first) and (val <= last)

	def addPerson(self, person):
		self.personList.append(person)
		self.sortSumIndexes()

	def checkIfImageExists():
    		
	
	def lookUpSumIndex(self, item):
		a_list = self.sorted_sum_index

		if(type(Person) is type(item)):
			index = item.getSumIndex()
		else:
			index = item

		first = abs( index - (SEARCH_THRESHOLD/float(2)) )
		last = abs( index + (SEARCH_THRESHOLD/float(2)) )

		start_index=0
		end_index =len(a_list)-1

		start_found = False
		for i in range(len(a_list)):
			val = a_list[i].getSumIndex()
			if self.checkInRange(val, first, end_index):
				start_index = i
				start_found = True
				break

		end_found = False
		for i in range(len(a_list)):
			val = a_list[ end_index - i].getSumIndex()
			if self.checkInRange(val, 0, last):
				end_index = end_index - i
				end_found = True
				break

		if(start_found and end_found):
			print str(start_index)+" - "+str(end_index)
			if start_index == end_index:
				return [a_list[start_index]]
			elif end_index < len(a_list)-1:
				return a_list[start_index : end_index+1]
			return a_list[start_index : end_index]
		else:
			return None

if __name__ == "__main__":
	shazam = Shazam()

	p1 = Person(0, 6, 1.39, [])
	p2 = Person(1, 5, 1.44, [])
	p3 = Person(2, 4, 1.57, [])
	p4 = Person(3, 3, 1.68, [])
	p5 = Person(4, 7, 1.22, [])
	p6 = Person(5, 8, 1.18, [])
	p7 = Person(6, 8, 1.9, [])
	p8 = Person(3, 3, 1.63, [])
	p9 = Person(3, 3, 1.60, [])
	p10 = Person(3, 3, 1.7, [])

	shazam.addPerson(p1)
	shazam.addPerson(p2)
	shazam.addPerson(p3)
	shazam.addPerson(p4)
	shazam.addPerson(p5)
	shazam.addPerson(p6)
	shazam.addPerson(p7)
	shazam.addPerson(p8)
	shazam.addPerson(p9)
	shazam.addPerson(p10)

	x = shazam.lookUpSumIndex(1.65)
	for l in x:
		print l.getSumIndex()