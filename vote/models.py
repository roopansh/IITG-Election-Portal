from django.db import models
from django.contrib.auth.models import User


class Admin(models.Model):
	user = models.OneToOneField(User, on_delete=models.CASCADE)
	def __str__(self):
		return self.user.username


class Voter(models.Model):
    username = models.CharField(max_length=100)
    CATEGORY = (('0','UG-Boy'),
    			('1','UG-Girl'),
    			('2','PG-Boy'),
    			('3','PG-Girl'))
    category = models.CharField(max_length=1,choices=CATEGORY)
    vp_status = models.BooleanField(default=False) #0 is not voted 1 is voted
    tech_status = models.BooleanField(default=False) #0 is not voted 1 is voted
    cult_status = models.BooleanField(default=False) #0 is not voted 1 is voted
    hostel_status = models.BooleanField(default=False) #0 is not voted 1 is voted
    welf_status = models.BooleanField(default=False) #0 is not voted 1 is voted
    sports_status = models.BooleanField(default=False) #0 is not voted 1 is voted
    gsen_status = models.BooleanField(default=False) #0 is not voted 1 is voted
    bsen_status = models.BooleanField(default=False) #0 is not voted 1 is voted
    sail_status = models.BooleanField(default=False) #0 is not voted 1 is voted
    cbs_status = models.BooleanField(default=False) #0 is not voted 1 is voted
    
    logout_time = models.DateTimeField(blank=True, null=True)
    login_time = models.DateTimeField(blank=True, null=True)
    hostel = models.CharField(max_length=50, default='MANAS')
    dept = models.CharField(max_length=50, default='CSE')

    def __str__(self):
        return self.username


# contestants in the elections
class Contestant(models.Model):
	user = models.OneToOneField(User, on_delete=models.CASCADE)

	CATEGORY = (
		('VP', 'Vice President'),
		('HAB', 'General Secretary of Hostel Affairs Board'),
		('UGS', 'Under Graduate Senator'),
		('PGS','Post Graduate Senator '),
		('GS','Girl Senator'),
		('Tech','General Secretary of Technical Board'),
		('Cult','General Secretary of Cultural Board'),
		('Welfare','General Secretary of Students\' Welfare Board'),
		('Sports','General Secretary of Sports Board'),
		('SAIL','General Seceratry of SAIL'),
		('CBS','General Seceratry of CBS'),
	)

	post = models.CharField(max_length=7, choices=CATEGORY)
	agenda1 = models.CharField(max_length=1000)
	agenda2 = models.CharField(max_length=1000)
	agenda3 = models.CharField(max_length=1000)
	agenda4 = models.CharField(max_length=1000)
	vote_count = models.IntegerField(default=0)
	pic = models.CharField(max_length=1000)
	random_suppling = models.IntegerField(default=0)
	
	def __str__(self):
		return self.user.username + " for " + self.post