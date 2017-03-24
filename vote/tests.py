import csv
csv_filepathname = '/home/dash/Election/csvs/new_result.csv'
dataReader = csv.reader(open(csv_filepathname), delimiter=',', quotechar='"')

for row in dataReader:
	print row[0]
	break