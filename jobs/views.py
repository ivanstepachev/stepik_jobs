from django.http import HttpResponseNotFound, HttpResponseServerError
from django.shortcuts import render

from jobs.models import Company, Specialty, Vacancy


def main_view(request):
    specialties = Specialty.objects.all()
    companies = Company.objects.all()
    context = {'specialties': specialties, 'companies': companies}
    return render(request, 'jobs/index.html', context)


def vacancies_all(request):
    vacancies = Vacancy.objects.all()
    context = {'vacancies': vacancies}
    return render(request, 'jobs/vacancies.html', context)


def vacancies_cat(request, specialty):
    try:
        category = Specialty.objects.get(code=specialty)
    except Specialty.DoesNotExist:
        return custom_handler404(request, HttpResponseNotFound)
    else:
        vacancies = Vacancy.objects.filter(specialty__code=specialty)
        name_of_cat = category.title
        context = {'vacancies': vacancies, 'name_of_cat': name_of_cat}
        return render(request, 'jobs/vacancies.html', context)


def company_detail(request, id):
    try:
        company = Company.objects.get(id=id)
    except Company.DoesNotExist:
        return custom_handler404(request, HttpResponseNotFound)
    else:
        vacancies_of_company = company.vacancies.all()
        context = {'company': company, 'vacancies_of_company': vacancies_of_company}
        return render(request, 'jobs/company.html', context)


def vacancy_detail(request, id):
    try:
        vacancy = Vacancy.objects.get(id=id)
    except Vacancy.DoesNotExist:
        return custom_handler404(request, HttpResponseNotFound)
    else:
        context = {'vacancy': vacancy}
        return render(request, 'jobs/vacancy.html', context)


def custom_handler404(request, exception):
    return HttpResponseNotFound("Упс, ошибка 404")


def custom_handler500(request):
    return HttpResponseServerError("Упс, ошибка 500")
