import re
import sys
import cs3311
# import time
# start_time = time.time()

conn = cs3311.connect()
cur = conn.cursor()

cur.execute("SELECT weeks, id FROM Meetings")

for tup in cur.fetchall():
	text = ['0','0','0','0','0','0','0','0','0','0','0']
	# deal with string
	if (re.match("^([0-9]-?,?)+$",tup[0])):
		# print('time: ' + tup[0])
		wks = tup[0].split(',')
		for wk in wks:
			if '-' in wk:
				nums = wk.split('-')
				for i in range(int(nums[0]), int(nums[1]) + 1):
					i -= 1
					text[i] = '1'
			else:
				text[int(wk) - 1] = '1'

	else:
		assert(('N' in tup[0]) or ('<' in tup[0]))

	# updata weeks_binary text
	try:
		cur.execute("""
			UPDATE Meetings
	    	SET weeks_binary = '{}'
	    	WHERE id = {}
			""".format((''.join(text)), tup[1])
		)
	except Exception as e:
		print("Error updating {}".tup[1])
		print(e)

cur.close()
conn.commit()
conn.close()

# print("---- {} seconds -----".format(time.time() - start_time))