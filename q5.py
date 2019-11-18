import sys
import connection
from collections import defaultdict

conn = connection.connect()
cur = conn.cursor()
buildings = defaultdict(list)

code = "COMP1521"

if len(sys.argv) == 2:
	code = sys.argv[1]

cur.execute(
	"""
	SELECT ct.name, c.tag, c.quota, count(distinct person_id)
	FROM Classes c 
	JOIN ClassTypes ct on ct.id = c.type_id
	JOIN Class_Enrolments ce on ce.class_id = c.id
	JOIN Courses co on co.id = c.course_id
	JOIN Subjects s on s.id = co.subject_id
	WHERE co.term_id = 5199 and s.code='{}'
	GROUP BY ct.name, c.tag, c.quota
	""".format(code)
)

for tup in cur.fetchall():
	percentage = round((tup[3]/tup[2])*100)
	if (percentage < 50):
		s = "{} {} is {}% full".format(tup[0], tup[1], percentage)
		print(" ".join(s.split()))

cur.close()
conn.close()



