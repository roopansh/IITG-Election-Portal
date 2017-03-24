import csv
import random
from django.utils.encoding import smart_str
from django.contrib.auth.hashers import make_password
from django.contrib.auth.models import User
from vote.models import Contestant, Voter

CHARS = "abcdefghjkmnpqrstuvwxyABCDEFGHJKLMNPQRSTUVWXY3456789"

def csv_to_voter():
	csvfile = open('voter.csv', 'r')
	reader = csv.reader(csvfile, quoting=csv.QUOTE_ALL)
	for i, row in enumerate(reader):
		username = smart_str(row[0])
		category = smart_str(row[1])
		hostel = smart_str(row[2])
		dept = smart_str(row[3])
		voter = Voter(username=username,
			category=category,
			hostel=hostel,
			dept=dept
		)
		voter.save()

def csv_to_contestants():
	csvfile = open('contestant.csv', 'r')
	reader = csv.reader(csvfile, quoting=csv.QUOTE_ALL)
	for i, row in enumerate(reader):
		user = User.objects.create(username = row[2].split('@')[0], 
			password="".join(random.choice(CHARS) for _ in range(8)), 
			is_active = True, 
			first_name = row[0].upper()
		)
		contestant = Contestant.objects.create(user = user, post = row[1], agenda1 = row[3], agenda2 = row[4], agenda3 = row[5], agenda4 = row[6], pic = "contestants/" + row[7] + ".jpg",  random_suppling = 0)


csv_to_voter()
csv_to_contestants()