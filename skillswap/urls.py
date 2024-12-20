"""
URL configuration for skillswap project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from pages.views import home_view, about_view, search_subjects_view, category_list_view, category_detail_view
from tutoring.views import login_view, register_view, logout_view, tutor_list_view, create_advertisement_view


urlpatterns = [
    path('home/', home_view, name='home'),
    path('about/', about_view, name='about'),
    path('login/', login_view, name='login'),
    path('register/', register_view, name='register'),
    path('logout/', logout_view, name='logout'),
    path('tutors/', tutor_list_view, name='tutors'),
    path('create/', create_advertisement_view, name = "create_advertisement"),
    path('admin/', admin.site.urls), #Keep admin at bottom
    path('search_subjects/', search_subjects_view, name='search-subjects'),
    path('categories/', category_list_view, name='categories'),
    path('categories/<str:category_name>/', category_detail_view, name='category_detail'),
]
