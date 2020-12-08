from django.contrib import admin

from .models import Application, Company, Specialty, Vacancy, Resume, Grade


admin.site.register(Application)
admin.site.register(Company)
admin.site.register(Specialty)
admin.site.register(Vacancy)
admin.site.register(Grade)
admin.site.register(Resume)
