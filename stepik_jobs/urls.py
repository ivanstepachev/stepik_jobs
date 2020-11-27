from django.contrib import admin
from django.urls import path

from jobs import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.main_view),
    path('vacancies/', views.vacancies_all),
    path('vacancies/cat/<str:specialty>/', views.vacancies_cat),
    path('companies/<int:id>/', views.company_detail),
    path('vacancies/<int:id>/', views.vacancy_detail),
]

handler404 = 'jobs.views.custom_handler404'
handler500 = 'jobs.views.custom_handler500'
