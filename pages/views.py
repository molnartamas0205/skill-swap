from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse
from tutoring.models import TutoringService, Category
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

def category_list_view(request):
    categories = Category.objects.all()
    return render(request, 'categories.html', {'categories': categories})

def category_detail_view(request, category_name):
    category = get_object_or_404(Category, name=category_name)
    tutors = TutoringService.objects.filter(category=category)
    return render(request, 'category_detail.html', {
        'category': category,
        'tutors': tutors
    })