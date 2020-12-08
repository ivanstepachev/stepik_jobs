from datetime import date

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect, Http404
from django.shortcuts import get_object_or_404, redirect, render
from django.views import View

from jobs.forms import CompanyForm, VacancyForm
from jobs.models import Company, Vacancy


class CompanySettingsView(View):

    def post(self, request):
        company = Company.objects.get(owner=request.user)
        company_form = CompanyForm(request.POST, request.FILES)
        if company_form.is_valid():
            changed_data = company_form.cleaned_data
            company.name = changed_data['name']
            company.location = changed_data['location']
            company.logo = changed_data['logo'] if changed_data['logo'] is not None else company.logo
            company.description = changed_data['description']
            company.employee_count = changed_data['employee_count']
            company.save()
            messages.success(request, 'success')
            return HttpResponseRedirect(request.path_info)
        else:
            raise Http404

    def get(self, request):
        try:
            company = Company.objects.get(owner=request.user)
        except Company.DoesNotExist:
            return render(request, 'jobs/employer/company-create.html')
        else:
            company_form = CompanyForm()
            company_form['name'].initial = company.name
            company_form['location'].initial = company.location
            company_form['logo'].initial = company.logo
            company_form['description'].initial = company.description
            company_form['employee_count'].initial = company.employee_count
            context = {'company': company, 'company_form': company_form}
            return render(request, 'jobs/employer/company-edit.html', context)


class CompanyCreateView(View):

    def post(self, request):
        company_form = CompanyForm(request.POST, request.FILES)
        if company_form.is_valid():
            Company.objects.create(
                name=company_form.cleaned_data['name'],
                location=company_form.cleaned_data['location'],
                logo=company_form.cleaned_data['logo'],
                description=company_form.cleaned_data['description'],
                employee_count=company_form.cleaned_data['employee_count'],
                owner=request.user,
            )
            messages.success(request, 'success')
            return redirect('company')
        else:
            raise Http404

    def get(self, request):
        if Company.objects.filter(owner=request.user):
            return redirect('company')
        else:
            company_form = CompanyForm()
            context = {'company_form': company_form}
            return render(request, 'jobs/employer/company-edit.html', context)


@login_required(login_url='/login/')
def company_vacancies(request):
    vacancies = Vacancy.objects.filter(company__owner=request.user)
    context = {'vacancies': vacancies}
    return render(request, 'jobs/employer/vacancy-list.html', context)


class VacancySettingsView(View):

    def post(self, request, vacancy_id):
        vacancy = Vacancy.objects.get(id=vacancy_id)
        vacancy_form = VacancyForm(request.POST)
        if vacancy_form.is_valid():
            vacancy.title = vacancy_form.cleaned_data['title']
            vacancy.specialty = vacancy_form.cleaned_data['specialty']
            vacancy.skills = vacancy_form.cleaned_data['skills']
            vacancy.description = vacancy_form.cleaned_data['description']
            vacancy.salary_min = vacancy_form.cleaned_data['salary_min']
            vacancy.salary_max = vacancy_form.cleaned_data['salary_max']
            vacancy.published_at = date.today()
            vacancy.save()
            messages.success(request, 'success')
            return HttpResponseRedirect(request.path_info)
        else:
            Http404

    def get(self, request, vacancy_id):
        vacancy = get_object_or_404(Vacancy, id=vacancy_id)
        if request.user == vacancy.company.owner:
            vacancy = Vacancy.objects.get(id=vacancy_id)
            vacancy_form = VacancyForm(
                initial={'title': vacancy.title, 'specialty': vacancy.specialty, 'skills': vacancy.skills,
                         'description': vacancy.description, 'salary_min': vacancy.salary_min,
                         'salary_max': vacancy.salary_max},
            )
            context = {'vacancy_form': vacancy_form, 'vacancy': vacancy}
            return render(request, 'jobs/employer/vacancy-edit.html', context)
        else:
            raise Http404


class VacancyCreateView(View):

    def post(self, request):
        vacancy_form = VacancyForm(request.POST)
        if vacancy_form.is_valid():
            Vacancy.objects.create(
                title=vacancy_form.cleaned_data['title'],
                specialty=vacancy_form.cleaned_data['specialty'],
                company=request.user.company,
                skills=vacancy_form.cleaned_data['skills'],
                description=vacancy_form.cleaned_data['description'],
                salary_min=vacancy_form.cleaned_data['salary_min'],
                salary_max=vacancy_form.cleaned_data['salary_max'],
                published_at=date.today(),
            )
            messages.success(request, 'success')
            return redirect(company_vacancies)
        else:
            raise Http404

    def get(self, request):
        if Company.objects.filter(owner=request.user).count() == 0:
            return redirect('company_create')
        else:
            vacancy_form = VacancyForm()
            context = {'vacancy_form': vacancy_form}
            return render(request, 'jobs/employer/vacancy-edit.html', context)
