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
#        "version_name":        ## can be "exam" by default, or "version_a" or "practice"
#        {
#           "exam_file": "filename" or None        
#           "solution_file" : "filename" or None
#        }
#      }
#    }
#  }
# } 
data = {} 

seasons = ["fall", "summer", "spring"] # uses this order
exams = ["exam1", "exam2", "exam3", "final"] # uses this order

table_head = "|Semester|Exam 1|Exam 2|Exam 3|Final|\n|:---:|:---:|:---:|:---:|:---:|\n"
output = table_head # build it up


def store(year, season, exam, version_name, soln, filename):
	"""store data into datastructure"""
	
	if year not in data :
		data[year] = {}
	
	if season not in data[year]:
		data[year][season] = {}
		
	if exam not in data[year][season]:
		data[year][season][exam] = {}

	if version_name not in data[year][season][exam]:
		data[year][season][exam][version_name] = {}

	if soln: # is a solution
		data[year][season][exam][version_name]["solution_file"] = filename
	else:
		data[year][season][exam][version_name]["exam_file"] = filename
	
	
	


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

	
	soln = True if parts[-1]=="sol" else False

	# check for exam version_name
	if len(parts) == 3:
		version_name = "exam"
	if len(parts) > 3 and parts[3] != 'sol':
		version_name = parts[3]

	#print(year, season, exam, soln)
	#print(filename)

	store(year, season, exam, version_name, soln, filename)

# pprint.pprint(data)

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
						
					# handle version_names
					for version_name in data[year][season][exam]:

						if "exam_file" in data[year][season][exam][version_name]:
							if addcomma:
								row += ", "

							filename = data[year][season][exam][version_name]["exam_file"]
							row += "[{}](./exams/{}.pdf)".format(version_name.capitalize(), filename)
							addcomma = True

							
						if "solution_file" in data[year][season][exam][version_name]:
							if addcomma:
								row += ", "
								
							filename = data[year][season][exam][version_name]["solution_file"]
							row += "[{}](./exams/{}.pdf)".format(version_name.capitalize() + " solutions", filename)
						
							addcomma = True
					
					# done this exam
					row += " | "
				
				else: # if don't have this exam, still need to separate column
					row += " | "
			row += "\n"
			#print(row)
			output += row			
		
print(output)
