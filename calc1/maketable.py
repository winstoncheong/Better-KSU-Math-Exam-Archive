#!python

import os
import pprint

# data design:
# {
#  "year" : 
#  {
#    "season" : 
#    {
#      "exam#" :
#      {
#        "blank" : "filename",
#        "solns" : "filename",
#      }
#    }
#  }
# } 
data = {} 

seasons = ["fall", "summer", "spring"] # uses this order
exams = ["exam1", "exam2", "exam3", "final"] # uses this order

table_head = "|Semester|Exam 1|Exam 2|Exam 3|Final|\n|:---:|:---:|:---:|:---:|:---:|\n"
output = table_head # build it up


def store(year, season, exam, soln, filename):
	"""store data into datastructure"""

	if year not in data :
		data[year] = {}

	if season not in data[year]:
		data[year][season] = {}

	if exam not in data[year][season]:
		data[year][season][exam] = {}

	if soln: # is a solution
		data[year][season][exam]["solns"] = filename
	else:
		data[year][season][exam]["blank"] = filename





files = sorted(os.listdir("./exams/")) # for when in the actual directory

# for testing:
#f = open("filenames.txt", "r")
#files = list(f.readlines())
#f.close()

files.reverse()

filtered = list(filter(lambda x : ".pdf" in x, files))
# print(list(filtered))

for filename in filtered:
	filename = filename.strip() # needed for testing
	filename = filename.replace('.pdf','')

	parts = filename.split('-')
	year = parts[0]
	season = parts[1]
	exam = parts[2]

	soln = True if len(parts)==4 else False

	#print(year, season, exam, soln)
	#print(filename)

	store(year, season, exam, soln, filename)

#pprint.pprint(data)

# TODO read from data structure to create table
for year in sorted(data.keys(), reverse=True):
	for season in seasons:
		if season in data[year]:
			row = "| {} {} | ".format(year, season.capitalize()) 


			#print(year,season)
			#for exam in sorted(data[year][season].keys()):
				#print(year, season, exam)

			# construct the row for the season
			for exam in exams: 
				if exam in data[year][season]:
					addcomma = False # comma to separate the blank from the solutions when printing table

					if "blank" in data[year][season][exam]:
						filename = data[year][season][exam]["blank"]
						row += "[Exam](./exams/{}.pdf)".format(filename)
						addcomma = True

					if "solns" in data[year][season][exam]:
						if addcomma:
							row += ", "

						filename = data[year][season][exam]["solns"]
						row += "[Solutions](./exams/{}.pdf)".format(filename)


					# done this exam
					row += " | "

				else: # if don't have this exam, still need to separate column
					row += " | "
			row += "\n"
			#print(row)
			output += row			

print(output)
