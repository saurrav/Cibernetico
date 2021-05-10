from django.contrib import admin
from .models import Employee,Doc,Patient,Brain,Comments,News,Drugs
# Register your models here.
admin.site.register(Employee)
admin.site.register(Doc)
admin.site.register(Patient)
admin.site.register(Brain)
admin.site.register(Comments)
admin.site.register(News)
admin.site.register(Drugs)
