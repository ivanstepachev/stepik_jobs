from django.db.models import Q
from django.http import HttpResponseNotFound, HttpResponseServerError, Http404
from django.shortcuts import get_object_or_404, redirect, render
from django.views import View

from jobs.forms import ApplicationForm, SearchForm
from jobs.models import Application, Company, Specialty, Vacancy


def main_view(request):
    specialties = Specialty.objects.all()
    companies = Company.objects.all()
    form = SearchForm()
    context = {'specialties': specialties, 'companies': companies, 'form': form}
    return render(request, 'jobs/public/index.html', context)


def vacancies_all(request):
    vacancies = Vacancy.objects.all()
    context = {'vacancies': vacancies}
    return render(request, 'jobs/public/vacancies.html', context)


def vacancies_cat(request, specialty):
    category = get_object_or_404(Specialty, code=specialty)
    vacancies = Vacancy.objects.filter(specialty__code=specialty)
    name_of_cat = category.title
    context = {'vacancies': vacancies, 'name_of_cat': name_of_cat}
    return render(request, 'jobs/public/vacancies.html', context)


def company_detail(request, company_id):
    company = get_object_or_404(Company, id=company_id)
    vacancies_of_company = company.vacancies.all()
    context = {'company': company, 'vacancies_of_company': vacancies_of_company}
    return render(request, 'jobs/public/company.html', context)


def vacancy_detail(request, vacancy_id):
    if request.method == 'POST':
        application_form = ApplicationForm(request.POST)
        if application_form.is_valid():
            Application.objects.create(
                written_username=application_form.cleaned_data['written_username'],
                written_phone=application_form.cleaned_data['written_phone'],
                written_cover_letter=application_form.cleaned_data['written_cover_letter'],
                vacancy=Vacancy.objects.get(id=vacancy_id),
                user=request.user,
            )
            return redirect('/vacancies/{}/send'.format(vacancy_id))
        else:
            raise Http404
    else:
        vacancy = get_object_or_404(Vacancy, id=vacancy_id)
        application_form = ApplicationForm
        context = {'vacancy': vacancy, 'application_form': application_form}
        return render(request, 'jobs/public/vacancy.html', context)


class VacancyView(View):
    def post(self, request, vacancy_id, *args, **kwargs):
        application_form = ApplicationForm(request.POST)
        if application_form.is_valid():
            Application.objects.create(
                written_username=application_form.cleaned_data['written_username'],
                written_phone=application_form.cleaned_data['written_phone'],
                written_cover_letter=application_form.cleaned_data['written_cover_letter'],
                vacancy=Vacancy.objects.get(id=vacancy_id),
                user=request.user,
            )
            return redirect('/vacancies/{}/send'.format(vacancy_id))
        else:
            raise Http404

    def get(self, request, vacancy_id, *args, **kwargs):
        vacancy = get_object_or_404(Vacancy, id=vacancy_id)
        application_form = ApplicationForm
        context = {'vacancy': vacancy, 'application_form': application_form}
        return render(request, 'jobs/public/vacancy.html', context)


def application_send(request, vacancy_id):
    return render(request, 'jobs/public/sent.html')


def search_view(request, search):
    form = SearchForm()
    s = request.GET.get('s')
    vacancies = Vacancy.objects.filter(Q(title__icontains=s) | Q(description__icontains=s) | Q(skills__icontains=s))
    context = {'vacancies': vacancies, 'form': form}
    return render(request, 'jobs/public/search.html', context)


def custom_handler404(request, exception):
    return HttpResponseNotFound("Упс, ошибка 404")


def custom_handler500(request):
    return HttpResponseServerError("Упс, ошибка 500")
