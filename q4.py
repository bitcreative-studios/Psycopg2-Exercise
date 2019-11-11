import sys
import ass3
from collections import defaultdict

conn = ass3.connect()
buildings = defaultdict(list)
prefix = "ENGG"
prev = None

cur = conn.cursor()

if len(sys.argv) == 2:
	prefix = sys.argv[1]

cur.execute(
	"""
	SELECT t.name, s.code, count(distinct ce.person_id)
	FROM Course_Enrolments ce 
	JOIN Courses c on ce.course_id = c.id
	JOIN Subjects s on c.subject_id = s.id
	JOIN Terms t on t.id = c.term_id
	WHERE s.code like '{}%'
	GROUP BY t.name, s.code
	ORDER BY t.name, s.code
	""".format(prefix)
)

for tup in cur.fetchall():
	# see if getting to next term
	if prev is None:
		prev = tup[0] 
		print(tup[0])
	else:
		if (tup[0] != prev):
			print(tup[0])
			prev = tup[0]

	# print courses and num of students
	print(" {}({})".format(tup[1], tup[2]))

cur.close()
conn.close()



