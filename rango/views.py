# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseRedirect
from .models import Category, Page, UserProfile, User
from forms import CategoryForms, PageForms, UserForm, UserProfileForm
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from datetime import datetime

# Create your views here.
def index(request):
    category_list   = Category.objects.all().order_by('-likes')[:5]
    most_viewed_page = Page.objects.all().order_by('-views')[:5]


    context = {
        'categories' : category_list,
        'most_viewed_page' : most_viewed_page,
    }

    #Get number of visits in the site using COOKIES.get()
    visits = request.session.get('visits')
    if not visits:
        visits = 1

    reset_last_visit_time = False

    last_visit = request.session.get('last_visit')
    if (last_visit):
        #get value of last visit
        last_visit_time = datetime.strptime(last_visit[:-7], "%Y-%m-%d %H:%M:%S")

        if ((datetime.now() - last_visit_time).seconds > 0):
            visits = visits + 1
            #update last visit
            reset_last_visit_time = True
    else:
        #No Cookie, so create it the curr date/time
        reset_last_visit_time = True

    if reset_last_visit_time:
        request.session['last_visit'] = str(datetime.now())
        request.session['visits'] = visits

    context['visits'] = visits
    response = render(request,'rango/index.html', context)

    return response

def about(request):
    if (request.session.get('visits')):
        count = request.session.get('visits')
    else:
        count = 0

    context = {
        'visits' : count,
    }
    response = render(request,'rango/about.html', context)
    return response
def category(request, slug):
    context = {}
    try:
        category = Category.objects.get(slug=slug)
        context['category_name'] = category.name

        pages = Page.objects.filter(category=category)
        context['pages'] = pages
        context['category'] = category
    except Category.DoesNotExist:
        # We get here if we didn't find the specified category.
        # Don't do anything - the template displays the "no category" message for us.
        pass
    return render(request, 'rango/category.html', context)
@login_required
def add_category(request):
    if request.method == 'POST':
        form = CategoryForms(request.POST)

        if (form.is_valid()):
            form.save(commit=True)
            return index(request)
        else:
            print (form.errors)
    else:
        form = CategoryForms

    return render(request, 'rango/add_category.html', {'form' : form})

@login_required
def add_page(request, slug):
    try:
        cat = Category.objects.get(slug=slug)
    except Category.DoesNotExist:
        cat = 'None'

    if request.method == 'POST':
        form = PageForms(request.POST)
        if form.is_valid():
            if cat:
                page = form.save(commit=False)
                page.category = cat
                page.views = 0
                page.save()
                #redirect back to the category page
                return redirect('/rango/category/'+cat.slug)
        else:
            print (form.errors)
    else:
        form = PageForms

    context = {
        'form':form,
        'category': cat,
    }

    return render(request, 'rango/add_page.html', context)

def register(request):
    registered = False

    if (request.method == 'POST'):
        user_form = UserForm(data = request.POST)
        profile_form = UserProfileForm(data = request.POST)
        if (user_form.is_valid() and profile_form.is_valid()):
            user = user_form.save()

            #hash password
            user.set_password(user.password)
            user.save()

            profile = profile_form.save(commit=False)
            profile.user = user

            if 'picture' in request.FILES:
                profile.picture = request.FILES['picture']

            profile.save()

            #Registration was successful.
            registered = True
        else:
            print (user_form.errors, profile_form.errors)
    else:
        user_form = UserForm()
        profile_form = UserProfileForm()

    context = {
        'user_form': user_form,
        'profile_form': profile_form,
        'registered': registered
    }
    return render(request, 'rango/register.html',context)

def register_profile(request):
    if request.method == 'POST':
        profile_form = UserProfileForm(request.POST)

        if (profile_form.is_valid()):
            profile = profile_form.save(commit=False)
            profile.user = request.user

            if 'picture' in request.FILES:
                profile.picture = request.FILES['picture']

            profile.save()

            return redirect('/rango/')
    else:
        form = UserProfileForm

    return render(request, 'registration/profile_registration.html', {'form' : form})

def login_user(request):
    if (request.method == 'POST'):
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(username = username, password = password)

        #User have correct credentials(Correct username & password)
        if (user):
            if (user.is_active):
                login(request, user)
                return HttpResponseRedirect('/rango/')
            else:
                # An inactive/disabled account was used
                return HttpResponse("Your Rango account is disabled.")
        else:
            return render(request, 'rango/login.html',{
            'login_message' : 'Invalid username or password',})
    else:
        return render(request, 'rango/login.html', {})

@login_required
def restricted(request):
     return render(request, 'rango/restricted.html')

@login_required
def user_logout(request):
    logout(request)
    return HttpResponseRedirect('/rango/')

def search(request):
    return render(request, 'rango/search.html')

def track_url(request):
    if request.method == 'GET':
        if 'page_id' in request.GET:
            page_id = request.GET['page_id']
            get_post = Page.objects.get(id = page_id)
            url = get_post.url
            get_post.views += 1
            get_post.save()
            return redirect(url)
        else:
            return redirect('/rango/')

def profile_page(request, username):
    context = {}
    users = User.objects.get(username = username)
    if(UserProfile.objects.all() > 0):
        profile = UserProfile.objects.get(user = users)
        context['profile'] = profile

    context['user'] = users
    context['curr_user'] = request.user

    return render(request, 'rango/profile.html', context)

@login_required
def edit_profile(request):
    context = {}
    if request.method == 'POST':
        #Get Profile Model
        user_profile = UserProfile.objects.get(user = request.user)
        #Get Values of Form
        profile_form = UserProfileForm(request.POST)
        if profile_form.is_valid():

            #If Website field have value change the old one, else, dont do anything
            if profile_form.cleaned_data['website']:
                user_profile.website = profile_form.cleaned_data['website']

            if 'picture' in request.FILES:
                user_profile.picture = request.FILES['picture']

            user_profile.save()
            return redirect('/rango/profile/'+str(request.user))

    else:
        context['form'] = UserProfileForm

    return render(request, 'rango/edit_profile.html', context)

@login_required
def like_category(request):
    cat_id = None;
    if request.method == 'GET':
        cat_id = request.GET['category_id']

    likes = 0
    if cat_id:
        cat = Category.objects.get(id = int(cat_id))
        if cat:
            likes = cat.likes + 1
            cat.likes = likes
            cat.save()
    return HttpResponse(likes)

def suggest_category(request):
    cat_list = []
    starts_with = ''
    if request.method == 'GET':
        starts_with = request.GET['suggestion']

    cat_list = get_category_list(8, starts_with)

    return render(request, 'rango/cats.html', {'cat_list': cat_list })

    
