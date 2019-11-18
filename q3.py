import sys
import connection 
from collections import defaultdict

conn = connection.connect()
buildings = defaultdict(list)
prefix = "ENGG";

if len(sys.argv) == 2:
	prefix = sys.argv[1]

cur = conn.cursor()

cur.execute(
	"""
	SELECT b.name, s.code
	From Meetings m
	JOIN Rooms r on m.room_id = r.id 
	JOIN Buildings b on r.within = b.id
	JOIN Classes cl on m.class_id = cl.id
	JOIN Courses co on cl.course_id = co.id
	JOIN Subjects s on co.subject_id = s.id
	WHERE co.term_id = 5196 and s.code like '{}%'
	GROUP BY b.name, s.code
	ORDER BY b.name
	""".format(prefix)
)

for tup in cur.fetchall():
	buildings[tup[0]].append(tup[1])

# print out result
for building, courses in sorted(buildings.items()):
	print(building)
	for c in courses:
		print(" {}".format(c))

cur.close()
conn.close()

