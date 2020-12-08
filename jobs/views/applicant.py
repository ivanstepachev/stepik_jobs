from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect, Http404
from django.shortcuts import redirect, render

from jobs.forms import ResumeForm
from jobs.models import Resume


@login_required(login_url='/login/')
def resume_edit(request):
    try:
        resume = Resume.objects.get(user=request.user)
    except Resume.DoesNotExist:
        return render(request, 'jobs/applicant/resume-create.html')
    else:
        if request.method == 'POST':
            resume_form = ResumeForm(request.POST)
            if resume_form.is_valid():
                resume.name = resume_form.cleaned_data['name']
                resume.surname = resume_form.cleaned_data['surname']
                resume.status = resume_form.cleaned_data['status']
                resume.salary = resume_form.cleaned_data['salary']
                resume.specialty = resume_form.cleaned_data['specialty']
                resume.grade = resume_form.cleaned_data['grade']
                resume.education = resume_form.cleaned_data['education']
                resume.experience = resume_form.cleaned_data['experience']
                resume.portfolio = resume_form.cleaned_data['portfolio']
                resume.save()
                messages.success(request, 'success')
                return HttpResponseRedirect(request.path_info)
            else:
                raise Http404
        else:
            resume_form = ResumeForm(
                initial={'name': resume.name, 'surname': resume.surname, 'status': resume.status,
                         'salary': resume.salary, 'specialty': resume.specialty, 'grade': resume.grade,
                         'education': resume.education, 'experience': resume.experience, 'portfolio': resume.portfolio},
            )
            context = {'resume_form': resume_form}
            return render(request, 'jobs/applicant/resume-edit.html', context)


@login_required(login_url='/login/')
def resume_create(request):
    if request.method == 'POST':
        resume_form = ResumeForm(request.POST)
        if resume_form.is_valid():
            Resume.objects.create(
                name=resume_form.cleaned_data['name'],
                surname=resume_form.cleaned_data['surname'],
                status=resume_form.cleaned_data['status'],
                salary=resume_form.cleaned_data['salary'],
                specialty=resume_form.cleaned_data['specialty'],
                grade=resume_form.cleaned_data['grade'],
                education=resume_form.cleaned_data['education'],
                experience=resume_form.cleaned_data['experience'],
                portfolio=resume_form.cleaned_data['portfolio'],
                user=request.user,
            )
            return redirect(resume_edit)
        else:
            raise Http404
    else:
        resume_form = ResumeForm()
        context = {'resume_form': resume_form}
        return render(request, 'jobs/applicant/resume-edit.html', context)
