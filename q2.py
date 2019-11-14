import sys
import cs3311
from collections import defaultdict

conn = cs3311.connect()

incommon = 2;
codes = defaultdict(list)
result = []

if len(sys.argv) == 2:
	incommon = int(sys.argv[1])
	if (incommon < 2 or incommon > 10):
		print("ERROR:[incommon] must be between 2 and 10")
		sys.exit(1)

# fetch course code
cur = conn.cursor()
cur.execute(
    """
    SELECT code
    FROM Subjects s
    GROUP BY code
    ORDER BY code
	"""
)

# aggregate course code
for tup in cur.fetchall():
	code = tup[0]
	num = code[4:]
	codes[num].append(code[:4])

# format result string
for num,letters in codes.items():
	if (len(letters) == incommon):
		s = num + ":"
		for i in letters:
			s += " " + i
		result.append(s)

# sort and print result
result.sort()
for i in result:
	print (i)

cur.close()
conn.close()

