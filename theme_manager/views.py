from django.shortcuts import render, redirect, get_object_or_404
from .models import Theme
from .forms import ThemeForm

# Create your views here.

# List all themes
def index(request):
    themes = Theme.objects.all()
    return render(request, "theme_manager/index.html", {"themes": themes})

# Create a theme
def create_theme(request):
    if request.method == 'POST':
        form = ThemeForm(request.POST)

        if form.is_valid():
            form.save()
            return redirect('theme_home')
    else:
        form = ThemeForm()

    return render(request, 'theme_manager/theme_form.html', {
        'form': form
    })

# Show details of a theme
def show_theme(request, theme_id):
    theme = get_object_or_404(Theme, id=theme_id)
    return render(request, "theme_manager/theme_show.html", {"theme": theme})

# Update a theme

# Update a theme
def update_theme(request, theme_id):
    theme = get_object_or_404(Theme, id=theme_id)

    if request.method == 'POST':
        form = ThemeForm(request.POST, instance=theme)

        if form.is_valid():
            form.save()
            return redirect('theme_home')
    else:
        form = ThemeForm(instance=theme)

    return render(request, 'theme_manager/theme_form.html', {
        'form': form,
    })


# Asks confirmation and delete a theme
def delete_theme(request, theme_id):
    theme = get_object_or_404(Theme, id=theme_id)
    if request.method == 'POST':
        theme.delete()
        return redirect('theme_list')

    return render(request, 'theme_manager/theme_delete.html', {
        'theme': theme
    })

