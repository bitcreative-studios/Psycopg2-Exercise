# COMP3311 19T3 Assignment 3
import sys
import cs3311
# import time
from collections import defaultdict
# start_time = time.time()

conn = cs3311.connect()
cur = conn.cursor()

# TODO

#===================== helper function =====================
def hours(num):
	return int(int(num) * 100 + (num - int(num)) * 60)

def printDict(dict):
	for key, value in dict.items():
		print(key)
		for i in value:
			print(i)
		print('')

def outputTimetable(timetable):
	result = []
	total_hours = 0;
	for key, value in timetable.items():
		start_time = -1
		end_time = -1
		result.append('  {}'.format(key))
		for v in value:
			if (start_time < 0):
				start_time = int(v[2]/100) + (v[2]%100)/60
			end_time = int(v[3]/100) + (v[3]%100)/60
			result.append('    {} {}: {}-{}'.format(v[0], v[1], v[2], v[3]))
		total_hours += (end_time - start_time + 2)

	print("Total hours: {}".format(total_hours))
	print('\n'.join(result))	

def clash(start1, end1, start2, end2):
	if (start2 >= end1 or end2 <= start1):
		return False
	else:
		return True 

# sort timetable according to meeting start time
def sortTimeTable(timetable):
	for key, value in timetable.items():
		timetable[key] = sorted(value, key=lambda c: c[2])

# return the index of the course code in list "course_code"
def course_index(code):
	return course_code.index(code)

def clear_clash(timetable):
	has_clash = 0
	for key, value in timetable.items():
		prev = None
		for v in value:
			if (prev != None):
				if (clash(v[2], v[3], prev[2], prev[3])):
					# print("clash",v,prev)
					next_class = find_next_class(v[2],v[3],v[0],v[1],v[4])
					if (next_class != None):
						remove_class(v[4], value)
						add_new_class(next_class, timetable)

						has_clash = 1
						return has_clash
			prev = v
	return has_clash

def find_next_class(start, end, code, cType, cId):
	find = 0
	prev = None
	for tup in classes[course_index(code)][cType]:
		# if find the clash course, select the next course
		if (find == 1 and prev != None):
			# if the current class not clash with the src class
			if (tup[5] != cId and not clash(start,end,tup[3],tup[4])):
				return tup

		if (find == 0 and tup[5] == cId):
			find = 1
			prev = tup

	return None 

# remove class with same id from a list of tuple
def remove_class(cId,timetable):
	for tup in timetable:
		if (tup[-1] == cId):
			timetable.remove(tup)

def add_new_class(new_class, timetable):
	c = classes[course_index(new_class[1])][new_class[2]]
	for tup in c:
		if (tup[5] == new_class[5]):
			if(c.index(tup) == (len(c)-1) or c.index(tup) == (len(c)-2)):
				continue
			timetable[new_class[0]].append(new_class[1:])

def remove_duplicate(timetable):
	dup = 0
	for key, value in timetable.items():
		while (1):
			dup = 0
			prev = None
			for v in value:
				if (prev == None):
					prev = v
					continue

				if (prev!= None and v == prev):
					value.remove(v)
					dup = 1
				else:
					prev = v
			if (dup == 0):
				break
#====================================================
course_string = []
course_code = []
if len(sys.argv) > 1:
	for a in sys.argv[1:]:
		course_string.append("s.code = '" + a + "'")
		course_code.append(a)
else:
	course_string = ["s.code = 'COMP1511'", "s.code = 'MATH1131'"]

terms_query = " or ".join(course_string) 
cur.execute (
	"""
	SELECT m.day, s.code, ct.name, m.start_time, m.end_time, min(m.class_id)
	FROM Meetings m
	JOIN Classes c on m.class_id = c.id
	JOIN ClassTypes ct on ct.id = c.type_id
	JOIN Courses co on co.id = c.course_id
	JOIN Terms t on t.id = co.term_id
	JOIN Subjects s on s.id = co.subject_id
	WHERE t.name = '19T3' and ({})
	group by s.code, m.day, ct.name, m.start_time, m.end_time
	ORDER BY m.day, m.start_time
	""".format(terms_query)
)

timetable = defaultdict(list)
# initializing three list for three courses
cc = [{}, {}, {}]
classes = [defaultdict(list), defaultdict(list), defaultdict(list)]

# put fetch result into dictionary
for tup in cur.fetchall():
	# print(tup)
	day = tup[0]
	course = tup[1]
	cType = tup[2]
	start = tup[3]
	end = tup[4]
	cId = tup[5] 
	timetable[day].append(tup[1:])

	# add the class into list according to class type
	classes[course_index(course)][cType].append(tup)
	# if the class has been selectd, ignore, else add id to the corresponding course list
	if (tup[2] in cc[course_index(tup[1])].keys()):
		continue

	else:
		cc[course_code.index(tup[1])][tup[2]] = tup[5]


sortTimeTable(timetable)
# print("-------------------classes---------------")
# for course in classes:
# 	# print(course_code[classes.index(course)])
# 	for key, value in course.items():
# 		print(key)
# 		for v in value:
# 			print(v)
# print("----------------end classes------------")


# select course and put in final timetable
timetable_final = defaultdict(list)
for key, value in timetable.items():
	for i in value:
		# print(i[4], cc[course_code.index(i[0])][i[1]])
		if (i[4] == cc[course_code.index(i[0])][i[1]]):
			timetable_final[key].append(i)

# print("----------timetable_final----------")
# printDict(timetable_final)
# print("--------------------------------")

# clear clash
has_clash = 1
for i in range(100):
	has_clash = clear_clash(timetable_final)
	sortTimeTable(timetable_final)
	if (has_clash == 0):
		break

remove_duplicate(timetable_final)

cur.close()
conn.close()

outputTimetable(timetable_final)

# print("---- {} seconds -----".format(time.time() - start_time))

