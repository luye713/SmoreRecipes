
from django.shortcuts import render, redirect
from django.views.generic import ListView, DetailView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.contrib.auth import login
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import User, Trip, Recipe, Ingredient, Instruction, Equipment, Category
from .forms import TripForm

# HOME
def home(request):
    return redirect('recipe_list', category='all', equipment='all')


def signup(request):
    error_message = ''
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('index')
        else:
            error_message = 'Invalid sign up - try again'
    form = UserCreationForm()
    context = {'form': form, 'error_message': error_message}
    return render(request, 'registration/signup.html', context)



# TRIP
@login_required
def trip_list(request):
    trips = Trip.objects.filter(user=request.user)
    return render(request, 'main_app/trip_list.html', { 'trips': trips })

class trip_create(LoginRequiredMixin, CreateView):
    model = Trip
    fields = ['name', 'destination', 'start_date', 'end_date']
    def form_valid(self, form):
        form.instance.user = self.request.user 
        return super().form_valid(form)

@login_required
def trip_detail(request, trip_id):
    trip = Trip.objects.filter(id=trip_id, user=request.user).first()
    return render(request, 'main_app/trip_detail.html', { 'trip': trip })

class trip_delete(LoginRequiredMixin, DeleteView):
    model = Trip
    success_url = '/trips/'



# RECIPE
@login_required
def recipe_list(request, category, equipment):
    if category == 'all':
        if equipment == 'all':
            recipes = Recipe.objects.all()
        else:
            recipes = Recipe.objects.filter(equipments__name__startswith=equipment)
    else:
        if equipment == 'all':
            recipes = Recipe.objects.filter(categories__name__startswith=category)
        else:
            recipes = Recipe.objects.filter(categories__name__startswith=category, equipments__name__startswith=equipment)
    categories = Category.objects.all()
    equipments = Equipment.objects.all()

    return render(request, 'main_app/recipe_list.html', {
        'categories': categories,
        'equipments': equipments,
        'recipes': recipes,
        'selected_category': category,
        'selected_equipment': equipment[0:4]
    })

@login_required
def recipe_detail(request, recipe_id):
    recipe = Recipe.objects.get(id=recipe_id)
    categories = Category.objects.filter(id__in = recipe.categories.all().values_list('id'))
    equipments = Equipment.objects.filter(id__in = recipe.equipments.all().values_list('id'))
    trips = Trip.objects.filter(user=request.user)
    return render(request, 'main_app/recipe_detail.html', {
        'recipe': recipe,
        'categories': categories,
        'equipments': equipments,
        'trips': trips,
    })


@login_required
def recipe_choose(request, recipe_id):
    trips = Trip.objects.filter(user=request.user)
    recipe = Recipe.objects.get(id=recipe_id)
    return render(request, 'main_app/recipe_choose.html', { 'trips': trips, 'recipe': recipe })


@login_required
def recipe_save(request, trip_id, recipe_id):
    Trip.objects.get(id=trip_id).recipes.add(recipe_id)
    return redirect('recipe_detail', recipe_id=recipe_id)



# EQUIPMENT





