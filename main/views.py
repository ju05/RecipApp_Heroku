from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required, user_passes_test
from .models import Ingredient, Recipe, UserProfile
from .forms import ProfileForm, RecipeForm, SignUpForm, AddEventForm
from django.db.models import Q
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.views import generic
from quickstart import create_event
import datetime

def home(request):
    total_recipes = Recipe.objects.all().count()
    context = {
        'title':'Homepage',
        'total_recipes': total_recipes
    }    
    return render(request, 'home.html', context)

# -------------------------------------SIGNIN SIGNUP ------------------------------
def signup(request): 
    context = {'form': SignUpForm} 

    if request.method =='POST':
        form_filled = SignUpForm(request.POST)    
        
        if form_filled.is_valid():         
            username = form_filled.cleaned_data.get('username') 
            password = form_filled.cleaned_data.get('password1') 
            user = authenticate(username=username, password=password)
            print('hello')
            form_filled.save()  
            UserProfile.objects.create(user_id = user.id)
            login(request, user) 
            return redirect('update_profile') 
        else:
            print(form_filled.errors)
            return render(request, 'signup.html', {'form': form_filled})    
    return render(request, 'signup.html', context) 

def signin(request):
    if request.user.is_authenticated:
        return redirect('homepage')

    if request.method == 'POST':
        fill_form = AuthenticationForm(request.POST)
        username = fill_form.cleaned_data['username']
        password = fill_form.cleaned_data['password1']
        print(username, password)
        # Authernticate
        user = authenticate(username = username, password = password)
        if user is not None:            
            login(request, user)
            return redirect('update_profile')
        else:
            return render(request, 'login.html', {'form': AuthenticationForm(request.POST)})
    
    else:
        return render(request, 'login.html', {'form': AuthenticationForm})


# ------------------------------------PROFILE VIEWS--------------------------------
def update_profile(request):
    
    profile = request.user.userprofile
    form = ProfileForm(request.POST or None, instance=profile)
    context = {'form': form} 

    if form.is_valid():
        form.save()
        return redirect('profile')

    return render(request, 'update_profile.html', context)


def profile(request):
    user = request.user
    profile = user.userprofile        
    context = {'profile': profile}

    return render(request, 'profile.html', context)

# ---------------------------------- SEARCH BAR ----------------------------------------

def search(request):    
    recipes = Recipe.objects.all()    
    if request.method == 'GET':
        query = request.GET.get('search')
        title_results = recipes.filter(Q(title__icontains=query))
        desc_results = recipes.filter(Q(description__icontains=query))        
        inst_results = recipes.filter(Q(instructions__icontains=query))
        results = title_results.union(desc_results, inst_results)
       
    if request.GET.get("15min"):
        query = '15 min'
        results = Recipe.objects.filter(prep_time = '15')     
    elif request.GET.get("Meal"):             
        query = request.GET.get("Meal")
        results = Recipe.objects.filter(Q(type__icontains=query))
    elif request.GET.get("Healthy"): 
        print
        query = 'Healthy'
        results = Recipe.objects.filter(very_healthy = True)
    elif request.GET.get("Diet"):         
        query = request.GET.get("Diet")
        veggie_results = Recipe.objects.filter(veggie = True)
        veggie_results = Recipe.objects.filter(vegan = True)
        glu_free_results = Recipe.objects.filter(gluten_free = True) 
        results = veggie_results.union(veggie_results,glu_free_results)  

    total = results.count()

    #paginate results
    paginator = Paginator(results, 3)
    page = request.GET.get("page")
    try:
        results = paginator.page(page)
    except PageNotAnInteger:
        results = paginator.page(1)
    except EmptyPage:
        results = paginator.page(paginator.num_pages)

    context = {'query': query, 'results': results, 'total':total}
    return render(request, "search.html", context)   

# --------------------------------------------------RECIPES VIEWS----------------------------------------------------------------------------

def detail(request, id):    
    recipe = Recipe.objects.filter(id = id)[0]   
    
    context = {'recipe':recipe, 'form': AddEventForm}
    return render(request, 'detail.html', context)

@login_required
def add_favorite(request, id):
    recipe = Recipe.objects.filter(id = id)
    if recipe.favorites.filter(id=request.user.id).exists():
        recipe.favorites.remove(request.user)
    else:
        recipe.favorites.add(request.user)
    return redirect('favorites.html')

@login_required
def favorites_list(request):
    favorites = Recipe.objects.filter(favorite=request.user)
    return render(request, 'favorites.html', {'favorites': favorites})

@login_required 
def add_to_calendar(request, id):
    recipe = Recipe.objects.get(id = id)
    context = {'recipe':recipe, 'form': AddEventForm}

    if request.method == 'POST':
        request.session['recipe_id'] = str(recipe.id)
               
        create_event(request)

    return render(request, 'add_to_calendar.html', context)

# ------------------------------------------------------CHEFS GROUP --------------------------------------------------------------------
@login_required
def add_recipe(request):
    context = ({'form': RecipeForm, 'ingredients': Ingredient})

    if request.method == 'POST':
        form_filled = RecipeForm(request.POST)
        if form_filled.is_valid():
            form_filled.save()
            return redirect('home')
        else:
            print(form_filled.errors)
    
    return render(request, 'add_recipe.html', context)


