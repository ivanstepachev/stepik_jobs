from django.contrib.auth.models import User
from django.db import models

from stepik_jobs.settings import MEDIA_COMPANY_IMAGE_DIR, MEDIA_SPECIALITY_IMAGE_DIR


class Company(models.Model):
    name = models.CharField(max_length=64)
    location = models.CharField(max_length=64)
    logo = models.ImageField(upload_to=MEDIA_COMPANY_IMAGE_DIR, null=True, blank=True)
    description = models.TextField()
    employee_count = models.IntegerField()
    owner = models.OneToOneField(User, null=True, blank=True,
                                 on_delete=models.PROTECT, related_name='company')

    class Meta:
        verbose_name_plural = 'companies'

    def __str__(self):
        return self.name.capitalize()


class Specialty(models.Model):
    code = models.CharField(max_length=64)
    title = models.CharField(max_length=64)
    picture = models.ImageField(upload_to=MEDIA_SPECIALITY_IMAGE_DIR)

    class Meta:
        verbose_name_plural = 'specialties'

    def __str__(self):
        return self.code.capitalize()


class Vacancy(models.Model):
    title = models.CharField(max_length=64)
    specialty = models.ForeignKey(Specialty, on_delete=models.CASCADE, related_name="vacancies")
    company = models.ForeignKey(Company, on_delete=models.CASCADE, related_name="vacancies")
    skills = models.TextField()
    description = models.TextField()
    salary_min = models.IntegerField()
    salary_max = models.IntegerField()
    published_at = models.DateField()

    class Meta:
        verbose_name_plural = 'vacancies'

    def __str__(self):
        return '{} : {}'.format(self.company.name.capitalize(), self.title)

    def skills_in_str(self):
        return self.skills.replace(',', ' •')


class Application(models.Model):
    written_username = models.CharField(max_length=64)
    written_phone = models.CharField(max_length=20)
    written_cover_letter = models.TextField()
    vacancy = models.ForeignKey(Vacancy, on_delete=models.CASCADE, related_name='applications')
    user = models.ForeignKey(User, null=True, blank=True,
                             on_delete=models.CASCADE, related_name='applications')

    def __str__(self):
        return 'Отклик от {} для {}'.format(self.written_username, self.vacancy)


class Grade(models.Model):
    title = models.CharField(max_length=64)
    code = models.CharField(max_length=64)

    def __str__(self):
        return '{} ({})'.format(self.title, self.code)


class Resume(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='resumes')
    name = models.CharField(max_length=64)
    surname = models.CharField(max_length=64)
    status = models.BooleanField(default=True)
    salary = models.IntegerField()
    specialty = models.ForeignKey(Specialty, on_delete=models.CASCADE, related_name='resumes')
    grade = models.ForeignKey(Grade, on_delete=models.CASCADE, related_name='resumes')
    education = models.TextField()
    experience = models.TextField()
    portfolio = models.URLField()

    def __str__(self):
        return 'Резюме от {} ({} {})'.format(self.user, self.name, self.surname)
