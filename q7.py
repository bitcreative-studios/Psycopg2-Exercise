import sys
import ass3

import time
start_time = time.time()

conn = ass3.connect()
cur = conn.cursor()

term = "19T1"

if len(sys.argv) == 2:
	if (sys.argv[1] in ['19T1', '19T2', '19T3']):
		term = sys.argv[1]
	else:
		print("ERROR: [term] must be one of '19T1', '19T2', '19T3'")
		sys.exit(1)

cur.execute(
	"""
	SELECT r.code, (m.end_time-m.start_time) as length, m.weeks_binary, m.day, m.start_time, m.end_time
	FROM Rooms r
	JOIN Meetings m on m.room_id = r.id
	JOIN Classes c on c.id = m.class_id
	JOIN Courses co on co.id = c.course_id
	JOIN Terms t on co.term_id = t.id
	WHERE t.name = '19T1' and r.code like 'K-%'
	-- GROUP BY r.code, t.name, m.weeks_binary, m.end_time, m.start_time
	ORDER BY r.code
	""".format(term)
)

count = 0
res = cur.fetchall()
prev = None
length = 0
count_room = 0;
wk = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]

for room in res:
	# for the first room in fetched database
	if (prev is None):
		prev = room[0]
		count_room = 1

	# if changing to anothr room, determine if the room is underused and reset length and booked week
	elif (prev != room[0]):
		count_room += 1
		prev = room[0]
		# num_wk = 0
		# for w in wk:
		# 	num_wk += w

		# if (num_wk != 0):
		# 	length = length/int(num_wk);
		# 	print(length)
		length = length/10
		print(length)
		if (length < 2000):
			count += 1
		length = 0
		wk = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]

	for idx, val in enumerate(wk):
		# print (idx, val, int(room[2][idx]))
		wk[idx] = val or int(room[2][idx])
		length += (int(room[1]) * int(room[2][idx]))
	# print(wk)
	# print(room[2])

print("-----------------")
print(count/count_room)
print("underused rooms:", count)
print("total rooms:", count_room)

cur.close()
conn.close()

print("---- {} seconds -----".format(time.time() - start_time))
# SELECT r.code,	 m.start_time, m.end_time, (m.end_time-m.start_time) as length, m.weeks_binary
# FROM Rooms r
# JOIN Meetings m on m.room_id = r.id
# JOIN Classes c on c.id = m.class_id
# JOIN Courses co on co.id = c.course_id
# JOIN Terms t on co.term_id = t.id
# WHERE t.name = '19T3' and r.code like 'K-%'
# GROUP BY r.code, t.name, m.start_time, m.end_time, m.weeks_binary
# ORDER BY r.code