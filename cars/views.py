from django.core.paginator import Paginator
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth.models import User
from .forms import StyledUserCreationForm, CarForm
from .models import Car, Favourite


# Create your views here.

def home(request):
    new_cars = Car.objects.filter(condition='new').order_by('-created_at')[:4]
    used_cars = Car.objects.filter(condition='used').order_by('-created_at')[:4]

    return render(request, 'cars/home.html', {
        'new_cars': new_cars,
        'used_cars': used_cars,
    })

@login_required
def profile(request):
    favourites = Favourite.objects.filter(user=request.user).select_related('car')
    return render(request, 'cars/profile.html', {'favourites': favourites})


def car_list(request, condition=None):
    cars = Car.objects.all()
    if condition:
        cars = cars.filter(condition=condition)

    brand = request.GET.get('brand')
    year = request.GET.get('year')
    fuel_type = request.GET.get('fuel_type')
    max_price = request.GET.get('max_price')

    if brand:
        cars = cars.filter(brand__icontains=brand)
    if year:
        cars = cars.filter(year=year)
    if fuel_type:
        cars = cars.filter(fuel_type__icontains=fuel_type)
    if max_price:
        cars = cars.filter(price__lte=max_price)

    paginator = Paginator(cars, 9)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    favourited_ids = []
    if request.user.is_authenticated:
        favourited_ids = list(Favourite.objects.filter(user=request.user).values_list('car_id', flat=True))

    return render(request, 'cars/car_list.html', {
        'page_obj': page_obj,
        'condition': condition,
        'favourited_ids': favourited_ids,
    })
    
@login_required    
def car_detail(request, pk):
    car = get_object_or_404(Car, pk=pk)
    is_favourited = False
    if request.user.is_authenticated:
        is_favourited = Favourite.objects.filter(user=request.user, car=car).exists()
    return render(request, 'cars/car_detail.html', {'car': car, 'is_favourited': is_favourited})

def about_us(request):
    return render(request, 'cars/about_us.html')

def register(request):
    if request.method == 'POST':
        form = StyledUserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Account created successfully! You can now log in.')
            return redirect('login')
    else:
        form = StyledUserCreationForm()
    return render(request, 'cars/register.html', {'form': form})


@user_passes_test(lambda u: u.is_staff)
def add_car(request):
    if request.method == 'POST':
        form = CarForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, 'Car added successfully!')
            return redirect('manage_cars')
    else:
        form = CarForm()
    return render(request, 'cars/add_car.html', {'form': form})

@user_passes_test(lambda u: u.is_staff)
def edit_car(request, pk):
    car = get_object_or_404(Car, pk=pk)
    if request.method == 'POST':
        form = CarForm(request.POST, request.FILES, instance=car)
        if form.is_valid():
            form.save()
            messages.success(request, 'Car updated successfully!')
            return redirect('manage_cars')
    else:
        form = CarForm(instance=car)
    return render(request, 'cars/add_car.html', {'form': form, 'editing': True})

@user_passes_test(lambda u: u.is_staff)
def delete_car(request, pk):
    car = get_object_or_404(Car, pk=pk)
    car.delete()
    messages.success(request, 'Car deleted.')
    return redirect('manage_cars')

@user_passes_test(lambda u: u.is_staff)
def manage_cars(request):
    cars = Car.objects.all().order_by('-created_at')
    return render(request, 'cars/manage_cars.html', {'cars': cars})

@user_passes_test(lambda u: u.is_staff)
def user_management(request):
    users = User.objects.all().order_by('-date_joined')
    return render(request, 'cars/user_management.html', {'users': users})

@user_passes_test(lambda u: u.is_staff)
def promote_user(request, user_id):
    u = get_object_or_404(User, pk=user_id)
    u.is_staff = True
    u.save()
    messages.success(request, f'{u.username} promoted to Admin.')
    return redirect('user_management')

@user_passes_test(lambda u: u.is_staff)
def demote_user(request, user_id):
    u = get_object_or_404(User, pk=user_id)
    if u != request.user:
        u.is_staff = False
        u.save()
        messages.success(request, f'{u.username} demoted to User.')
    return redirect('user_management')

@user_passes_test(lambda u: u.is_staff)
def delete_user(request, user_id):
    u = get_object_or_404(User, pk=user_id)
    if u != request.user:
        u.delete()
        messages.success(request, 'User deleted.')
    return redirect('user_management')

    
@login_required
def profile(request):
    favourites = Favourite.objects.filter(user=request.user).select_related('car')
    return render(request, 'cars/profile.html', {
        'favourites': favourites,
    })

@login_required
def toggle_favourite(request, pk):
    car = get_object_or_404(Car, pk=pk)
    fav, created = Favourite.objects.get_or_create(user=request.user, car=car)
    if not created:
        fav.delete()
        messages.success(request, 'Removed from favourites.')
    else:
        messages.success(request, 'Added to favourites!')
    return redirect(request.META.get('HTTP_REFERER', 'car_list'))