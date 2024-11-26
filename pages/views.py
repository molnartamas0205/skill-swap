from django.shortcuts import render
from django.http import HttpResponse
from tutoring.models import TutoringService

# Create your views here.
def home_view(request, *args, **kwargs):
    return render(request, 'home.html', {})

def about_view(request, *args, **kwargs):
    return render(request, 'about.html', {})

def search_subjects_view(request):
    if request.method == "POST":
        searched = request.POST['searched']
        subjects = TutoringService.objects.filter(title__contains=searched)

        return render(request, 'search_subjects.html', 
        {
            'searched': searched,
            'subjects': subjects
        })
    else:
        return render(request, 'search_subjects.html', {})