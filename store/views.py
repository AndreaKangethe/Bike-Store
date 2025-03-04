from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth.forms import UserCreationForm
from django.db.models import Q  # ✅ Import for filtering
from .models import Bike, CartItem, Review
from .forms import BikeForm, ProfileUpdateForm, UserUpdateForm

def register(request):
    if request.method == "POST":
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            messages.success(request, 'Registration successful! You can now log in.')
            return redirect('login')
        else:
            messages.error(request, 'There was an error in your registration. Please try again.')
    else:
        form = UserCreationForm()

    return render(request, 'store/register.html', {'form': form})


@login_required
def profile(request):
    if request.method == 'POST':
        user_form = UserUpdateForm(request.POST, instance=request.user)
        profile_form = ProfileUpdateForm(request.POST, request.FILES, instance=request.user.profile)

        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            messages.success(request, 'Your profile has been updated!')
            return redirect('profile')
    else:
        user_form = UserUpdateForm(instance=request.user)
        profile_form = ProfileUpdateForm(instance=request.user.profile)

    return render(request, 'store/profile.html', {'user_form': user_form, 'profile_form': profile_form})


@login_required
def increase_quantity(request, item_id):
    cart_item = get_object_or_404(CartItem, id=item_id, user=request.user)
    cart_item.quantity += 1
    cart_item.save()
    return redirect('view_cart')


@login_required
def decrease_quantity(request, item_id):
    cart_item = get_object_or_404(CartItem, id=item_id, user=request.user)
    if cart_item.quantity > 1:
        cart_item.quantity -= 1
        cart_item.save()
    else:
        cart_item.delete()
    return redirect('view_cart')


def checkout(request):
    return render(request, 'store/checkout.html')


def home(request):
    query = request.GET.get('q', '')
    selected_brand = request.GET.get('brand', '')
    sort_option = request.GET.get('sort', '')

    brands = Bike.objects.values_list('brand', flat=True).distinct()

    bikes = Bike.objects.all()
    if query:
        bikes = bikes.filter(Q(name__icontains=query) | Q(model__icontains=query))
    if selected_brand:
        bikes = bikes.filter(brand=selected_brand)

    if sort_option == 'price_asc':
        bikes = bikes.order_by('price')
    elif sort_option == 'price_desc':
        bikes = bikes.order_by('-price')

    return render(request, 'store/home.html', {
        'bikes': bikes,
        'brands': brands,
        'query': query,
        'selected_brand': selected_brand,
        'sort': sort_option,
    })


@login_required
def bike_detail(request, bike_id):
    bike = get_object_or_404(Bike, id=bike_id)
    reviews = Review.objects.filter(bike=bike)

    if request.method == "POST":
        comment = request.POST.get("comment", "").strip()
        rating = request.POST.get("rating", 5)

        if comment:
            Review.objects.create(user=request.user, bike=bike, comment=comment, rating=int(rating))
            return redirect('bike_detail', bike_id=bike.id)

    return render(request, 'store/bike_detail.html', {'bike': bike, 'reviews': reviews})


@login_required
def add_to_cart(request, bike_id):
    bike = get_object_or_404(Bike, id=bike_id)
    cart_item, created = CartItem.objects.get_or_create(user=request.user, bike=bike)

    if not created:
        cart_item.quantity += 1
        cart_item.save()

    return redirect('view_cart')


@login_required
def view_cart(request):
    cart_items = CartItem.objects.filter(user=request.user)
    total_price = sum(item.quantity * item.bike.price for item in cart_items)

    return render(request, 'store/cart.html', {
        'cart_items': cart_items,
        'total_price': total_price,
    })


@login_required
def add_review(request, bike_id):
    if request.method == "POST":
        bike = get_object_or_404(Bike, id=bike_id)
        comment = request.POST.get("comment", "").strip()
        rating = request.POST.get("rating", 5)

        if comment:
            Review.objects.create(
                user=request.user,
                bike=bike,
                comment=comment,
                rating=int(rating)
            )

        return redirect('bike_detail', bike_id=bike.id)
    return redirect('bike_detail', bike_id=bike_id)


@login_required
def add_bike(request):
    if request.method == 'POST':
        form = BikeForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('home')
    else:
        form = BikeForm()

    return render(request, 'store/add_bike.html', {'form': form})
