from django.shortcuts import render
from django.http import HttpResponse
from tutoring.models import TutoringService
from fuzzywuzzy import fuzz
def home_view(request, *args, **kwargs):
    return render(request, 'home.html', {})

def about_view(request, *args, **kwargs):
    return render(request, 'about.html', {})

def search_subjects_view(request):
    if request.method == "POST":
        searched = request.POST['searched']
       
        tutors = TutoringService.objects.all() 
        filtered_tutors = []
        for tutor in tutors:
            if fuzz.partial_ratio(searched.lower(), tutor.title.lower()) > 70 or fuzz.partial_ratio(searched.lower(), tutor.category.name.lower()) > 70:  
             filtered_tutors.append(tutor)

        return render(request, 'search_subjects.html', {
            'searched': searched,
            'tutors': filtered_tutors
        })
    else:
        return render(request, 'search_subjects.html', {})