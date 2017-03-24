from django.contrib import admin
from .models import Voter, Admin, Contestant

admin.site.register(Voter)
admin.site.register(Admin)
admin.site.register(Contestant)