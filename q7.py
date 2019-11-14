import sys
import ass3
import time


def count_usage(end_time, start_time, weeks_binary):
	result = 0
	end_time = int(end_time/100) + (end_time%100)/60
	start_time = int(start_time/100) + (start_time%100)/60;
	length = end_time - start_time
	for idx, val in enumerate(weeks_binary):
		# print (idx, val, int(room[2][idx]))
		# wk[idx] = val or int(room[2][idx])
		result += (length * int(weeks_binary[idx]))
	# print(result, length)
	return result;

start_time = time.time()

conn = ass3.connect()
cur1 = conn.cursor()
cur2 = conn.cursor()

term = "19T1"

if len(sys.argv) == 2:
	if (sys.argv[1] in ['19T1', '19T2', '19T3']):
		term = sys.argv[1]
	else:
		print("ERROR: [term] must be one of '19T1', '19T2', '19T3'")
		sys.exit(1)


cur1.execute("SELECT count(distinct id) FROM Rooms r WHERE r.code ilike 'K-%'")
count_room = cur1.fetchone()
count_room = count_room[0]
cur1.execute("SELECT distinct id FROM Rooms r WHERE r.code ilike 'K-%' order by r.id")
room = cur1.fetchone()
# print (count_room)

cur2.execute(
	"""
		SELECT  total_room.id, m.end_time, m.start_time, m.weeks_binary, m.day, t.name
		FROM Meetings m 
		JOIN (SELECT r.id
				FROM Rooms r
				WHERE r.code ilike 'K-%') as total_room on total_room.id = m.room_id
		JOIN Classes c on c.id = m.class_id
		JOIN Courses co on co.id = c.course_id
		JOIN Terms t on co.term_id = t.id
		where t.name = '{}'
		ORDER BY total_room.id
	""".format(term)
)

count = 0
tup = cur2.fetchone()
prev = tup[0];
length = 0
i = 0
wk = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]

while (i < count_room):
	# if room i has booking in this term
	if (tup is None and length == 0):
		i += 1
		# print(room[0])#, ", i is", i)
		room = cur1.fetchone()
		count += 1
		continue

	# if the room i has no booking this term, fetch next room number
	if (tup is None or tup[0] != room[0]):
		length = length / 10
		if (length < 20):
			count += 1
			# go to next room
			# print(room[0], "under")#, ", next is", tup[0], "i is", i)
		else:
			pass
			# print(room[0], "ok")#, ", next is", tup[0], "i is", i)

		room = cur1.fetchone()
		i += 1
		length = 0


	else:
		if(tup[5] != term):
			continue
		# print("-------comes to", room[0], ", length is", length, ", i is", i, '-----------')

		# if still the record from prev room
		weeks_binary = tup[3]
		length += count_usage(tup[1], tup[2], weeks_binary[:10])
		# if (tup[0] == 100684):
		# 	print(tup[0], tup[1], tup[2], tup[3], tup[4], tup[5], length)
		# fetch the next tuple
		tup = cur2.fetchone()

	



# print("-----------------")
print("{}%".format(round((count*100/count_room),1)))
# print("underused rooms:", count)
# print("total rooms:", count_room)

cur1.close()
cur2.close()
conn.close()
#
# print("---- {} seconds -----".format(time.time() - start_time))



