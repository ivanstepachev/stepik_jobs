import os
import django

os.environ['DJANGO_SETTINGS_MODULE'] = 'stepik_jobs.settings'
django.setup()

import datetime
from jobs.models import Company, Specialty, Vacancy
from jobs.data import jobs, companies, specialties

if __name__ == '__main__':
    for company in companies:
        Company.objects.create(
            name=company['title'],
            location=company['location'],
            logo='https://place-hold.it/100x60',
            description=company['description'],
            employee_count=company['employee_count'],
        )

    for specialty in specialties:
        Specialty.objects.create(
            code=specialty['code'],
            title=specialty['title'],
            picture='https://place-hold.it/100x60',
        )

    for job in jobs:
        date_list = job['posted'].split('-')
        Vacancy.objects.create(
            title=job['title'],
            specialty=Specialty.objects.get(code=job['specialty']),
            company=Company.objects.get(id=int(job['company'])),
            skills=job['skills'],
            description=job['description'],
            salary_min=job['salary_from'],
            salary_max=job['salary_to'],
            published_at=datetime.date(int(date_list[0]), int(date_list[1]), int(date_list[2])),
        )
