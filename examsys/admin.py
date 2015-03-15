from django.contrib import admin

# Register your models here.
from examsys.models import *

admin.site.register(Question)
admin.site.register(User)
admin.site.register(Test)
admin.site.register(TestToQuestion)
