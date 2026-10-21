from django.shortcuts import render, redirect, get_object_or_404
from theme_manager.models import User
from .forms import UserForm

# Create your views here.

# List all users
def index(request):
    users = User.objects.all()
    return render(request, "user_manager/index.html", {"users": users})

# Create a user
def create_user(request):
    if request.method == 'POST':
        form = UserForm(request.POST)

        if form.is_valid():
            form.save()
            return redirect('user_home')
    else:
        form = UserForm()

    return render(request, 'user_manager/user_form.html', {
        'form': form
    })

# Show details of a user
def show_user(request, user_id):
    user = get_object_or_404(User, id=user_id)
    return render(request, "user_manager/user_show.html", {"user": user})

# Update a user
def update_user(request, user_id):
    user = get_object_or_404(User, id=user_id)

    if request.method == 'POST':
        form = UserForm(request.POST, instance=user)

        if form.is_valid():
            form.save()
            return redirect('user_home')
    else:
        form = UserForm(instance=user)

    return render(request, 'user_manager/user_form.html', {
        'form': form,
    })

# Asks confirmation and delete a user
def delete_user(request, user_id):
    user = get_object_or_404(User, id=user_id)
    if request.method == 'POST':
        user.delete()
        return redirect('user_list')

    return render(request, 'user_manager/user_delete.html', {
        'user': user
    })

