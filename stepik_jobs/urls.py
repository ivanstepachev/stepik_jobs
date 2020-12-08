from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import LogoutView
from django.urls import path, re_path

from jobs.views import public, employer, applicant, authorization

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', public.main_view, name='main'),
    path('vacancies/', public.vacancies_all, name='vacancies'),
    path('vacancies/cat/<str:specialty>/', public.vacancies_cat, name='vacancies_cat'),
    path('companies/<int:company_id>/', public.company_detail, name='company_detail'),
    path('vacancies/<int:vacancy_id>/', public.VacancyView.as_view(), name='vacancy_detail'),
    path('vacancies/<int:vacancy_id>/send', public.application_send),

    path('mycompany/', login_required(employer.CompanySettingsView.as_view(), login_url='/login'), name='company'),
    path('mycompany/create', login_required(employer.CompanyCreateView.as_view(),
                                            login_url='/login'), name='company_create'),
    path('mycompany/vacancies/', employer.company_vacancies, name='company_vacancies'),
    path('mycompany/vacancies/create',
         login_required(employer.VacancyCreateView.as_view(), login_url='/login'), name='company_vacancy_create'),
    path('mycompany/vacancies/<int:vacancy_id>/',
         login_required(employer.VacancySettingsView.as_view(), login_url='/login'), name='vacancy_settings'),

    path('myresume/', applicant.resume_edit, name='resume'),
    path('myresume/create', applicant.resume_create, name='resume_create'),
    path('login/', authorization.LoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('register/', authorization.RegisterView.as_view(), name='register'),
]

urlpatterns += [
    re_path(r'^search/(?P<search>.*)$', public.search_view, name='search'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

handler404 = 'jobs.views.public.custom_handler404'
handler500 = 'jobs.views.public.custom_handler500'
