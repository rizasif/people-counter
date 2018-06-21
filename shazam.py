import numpy as np
import pandas as pd
from person import Person
import algorithm as Al
import gender_age_eval as GA

SEARCH_THRESHOLD = float(0.5)
PERSON_THRESHOLD = 10
OPTIMAL_SHARPNESS = float(6.0)
THRESH_SHARPNESS = float(3.0)

SAVE_DIRECTORY = "data/faces/"

IMAGE_SIZE = 160

class Shazam():

	def __init__(self):
		self.next_id = int()
		self.personList = list()
		self.sorted_sum_index = list()

		print("Loading GA Model")
		GA.load_session()

	def sortSumIndexes(self):
		self.sorted_sum_index = sorted(self.personList,
										key=lambda shell:shell.getSumIndex())

	def checkInRange(self, val, first, last):
		return (val >= first) and (val <= last)

	def getNumOfPersons(self):
		return len(self.personList)

	def incrementApperance(self, index):
		# self.personList[index].incrementApperance()
		self.sorted_sum_index[index].incrementApperance()
		self.personList = self.sorted_sum_index

	def getGenderAge(self, image):
		# gray = image.convert('L')
		gray = image.resize((IMAGE_SIZE,IMAGE_SIZE))
		gray.load()
		data = np.asarray( gray, dtype="int32" )
		print("Loaded Image Data Shape: ", data.shape)
		# ages, genders = GA.eval([data])
		ages, genders = GA.eval_image([data])
		return ages[0], genders[0]

	def updatePerson(self, new_person, index):
		p = self.personList[index]
		p.incrementApperance()
		new_person.setId(p.getId())
		new_person.setTimestamp(p.getTimestamp())
		new_person.updateApprerance(p.getApperance())
		age, gender = self.getGenderAge(new_person.getPilImage())
		new_person.setAge(int(age))
		new_person.setGender( (int(gender) == 1) )
		new_person.saveImage(SAVE_DIRECTORY)
		new_person.clearPilImage()
		# self.personList[index] = new_person
		self.sorted_sum_index[index] = new_person
		self.personList = self.sorted_sum_index
		self.sortSumIndexes()

	# def addPerson(self, person):
	# 	person.clearPilImage()
	# 	self.personList.append(person)
	# 	self.sortSumIndexes()

	def updateCriteria(self, best, novel):
		# return best < novel
		# return abs(best - OPTIMAL_SHARPNESS) < abs(novel - OPTIMAL_SHARPNESS)
		return (novel > best)

	def additionCriteria(self, sharpness):
		return sharpness > THRESH_SHARPNESS

	def addNewPerson(self, person):
		if self.additionCriteria(person.getSharpness()):
			person.setId(self.next_id)
			person.updateApprerance(1)
			age, gender = self.getGenderAge(person.getPilImage())
			person.setAge(int(age))
			person.setGender( (int(gender) == 1) )
			person.saveImage(SAVE_DIRECTORY)
			person.clearPilImage()
			self.next_id += 1
			self.personList.append(person)
			self.sortSumIndexes()
	
	def lookUpSumIndex(self, item):
		a_list = self.sorted_sum_index

		if(isinstance(item, Person)):
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
			if self.checkInRange(val, first, a_list[end_index].getSumIndex()):
				start_index = i
				start_found = True
				break

		end_found = False
		for i in range(len(a_list)):
			val = a_list[ end_index - i].getSumIndex()
			if self.checkInRange(val, a_list[0].getSumIndex(), last):
				end_index = end_index - i
				end_found = True
				break

		if(start_found and end_found):
			# print str(start_index)+" - "+str(end_index)
			if start_index == end_index:
				return start_index, [a_list[start_index]]
			elif end_index < len(a_list)-1:
				return start_index,a_list[start_index : end_index+1]
			return start_index,a_list[start_index : end_index]
		else:
			return None, None

	def ProcessImage(self, image, timestamp):
		person_list = Al.getFaces(image, timestamp)
		for k in range(len(person_list)):
			p = person_list[k]
			# match_start_index, matches = self.lookUpSumIndex(p)
			match_start_index = 0
			matches = self.sorted_sum_index
			if matches:
				match_codes = [x.getEncoding() for x in matches]
				match_results = Al.compare(p.getEncoding(), match_codes)
				
				positive_matches = list()
				best_match = None
				best_match_val = 1000
				best_match_index = 0
				for i in range(len(matches)):
					if match_results[i]:
						positive_matches.append(i)
						pm = matches[i]
						new_val = abs(pm.getSumIndex() - p.getSumIndex())
						if best_match_val > new_val:
							best_match_val = new_val
							best_match = pm
							best_match_index = i
				if best_match:
					if self.updateCriteria(best_match.getSharpness() , p.getSharpness()):
						print ("start={}, k={}, t={}".format(match_start_index, best_match_index, len(self.sorted_sum_index)))
						self.updatePerson(p, match_start_index + best_match_index)
					else:
						self.incrementApperance(match_start_index + best_match_index)
				else:
					self.addNewPerson(p)
			else:
				self.addNewPerson(p)

	def printResults(self):
		print ("Total People: ", len(self.personList))

		p = self.personList[0]
		print ("Example Person: \n {} \n------".format(p.getSummary()))

	def saveResults(self):
		pdList = list()
		for p in self.personList:
			pdList.append(p.getSummary())

		df = pd.DataFrame(pdList)
		# print df
		df.to_csv("results.csv")
		print("Results Written to results.csv")

if __name__ == "__main__":
	shazam = Shazam()

	# p1 = Person(0, 6, 1.39, [])
	# p2 = Person(1, 5, 1.44, [])
	# p3 = Person(2, 4, 1.57, [])
	# p4 = Person(3, 3, 1.68, [])
	# p5 = Person(4, 7, 1.22, [])
	# p6 = Person(5, 8, 1.18, [])
	# p7 = Person(6, 8, 1.9, [])
	# p8 = Person(3, 3, 1.63, [])
	# p9 = Person(3, 3, 1.60, [])
	# p10 = Person(3, 3, 1.7, [])

	# shazam.addPerson(p1)
	# shazam.addPerson(p2)
	# shazam.addPerson(p3)
	# shazam.addPerson(p4)
	# shazam.addPerson(p5)
	# shazam.addPerson(p6)
	# shazam.addPerson(p7)
	# shazam.addPerson(p8)
	# shazam.addPerson(p9)
	# shazam.addPerson(p10)

	# x = shazam.lookUpSumIndex(1.65)
	# for l in x:
	# 	print l.getSumIndex()

	test_images = ['test.png', 'test2.png', 'test3.png', 'test4.png',
					 'test5.png', 'test6.png', 'test7.png']
	
	for t in test_images:
		print ("Processing Image: ", t)
		image = Al.read_image_from_disk(t)
		shazam.ProcessImage(image)

	# shazam.printResults()
	shazam.saveResults()