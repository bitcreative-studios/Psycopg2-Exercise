# COMP3311 19T3 Assignment 3
import sys
import cs3311
import time
from collections import defaultdict
start_time = time.time()

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
# classes_choice = defaultdict(set)
cc = [{}, {}, {}]
courses = [defaultdict(list), defaultdict(list), defaultdict(list)]

# put fetch result into dictionary
for tup in cur.fetchall():
	print(tup)
	timetable[tup[0]].append(tup[1:])
	# classes_choice[tup[1]].add(tup[5])
	# courses[course_code.index(tup[1])][tup[2]].append(tup[3:])
	if (tup[2] in cc[course_code.index(tup[1])].keys()):
		continue
	cc[course_code.index(tup[1])][tup[2]] = tup[5]

# sort timetable according to meeting start time
for key, value in timetable.items():
	timetable[key] = sorted(value, key=lambda c: c[2])

timetable_final = defaultdict(list)
for key, value in timetable.items():
	for i in value:
		# print(i[4], cc[course_code.index(i[0])][i[1]])
		if (i[4] == cc[course_code.index(i[0])][i[1]]):
			timetable_final[key].append(i)

printDict(timetable_final)
print("----------------")
# printDict(classes_choice)
# for i in range(len(course_code)):
# 	print(course_code[i])
# 	printDict(courses[i])
print(course_code)
print(cc)

cur.close()
conn.close()



print("---- {} seconds -----".format(time.time() - start_time))

