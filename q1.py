import connection
conn = connection.connect()

cur = conn.cursor()
cur.execute(
    """
    SELECT s.code, c.quota, count(ce.person_id)
	From Courses c
	JOIN Subjects s on c.subject_id = s.id
	JOIN Course_Enrolments ce on c.id = ce.course_id
	WHERE c.quota > 50 and c.term_id = 5199
	GROUP BY c.id,course_id, s.code
	ORDER BY s.code
	"""
)

for tup in cur.fetchall():
	if (tup[2] > tup[1]):
		percentage = round((tup[2]/tup[1])*100)
		print("{} {}%".format(tup[0], percentage))


cur.close()
conn.close()
