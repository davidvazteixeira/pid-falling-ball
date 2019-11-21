def interval(start, end, step=1):
	yield start
	while start < end:
		start += step
		yield start
