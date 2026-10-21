from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.utils import timezone
from .forms import PreGameForm, EventForm
from theme_manager.models import Theme
from .models import Event

# Create your views here.
def index(request):
    today = timezone.localdate()
    eventos_periodos = []

    for deslocamento in range(-1, 2):
        indice = today.year * 12 + (today.month - 1) + deslocamento
        ano = indice // 12
        mes = indice % 12 + 1

        evento = Event.objects.filter(
            month=mes,
            year=ano,
        ).first()

        eventos_periodos.append({
            "mes": mes,
            "ano": ano,
            "evento": evento,
        })
    
    return render(request, "game_manager/home.html", {"eventos_periodos": eventos_periodos})

def pre_game(request):
    today = timezone.localdate()
    month = today.month
    year = today.year

    if month != 12:
        next_month = month + 1
        next_year = year
    else:
        next_month = 1
        next_year = year + 1

    evento_atual = Event.objects.filter(
        month=month,
        year=year,
    ).first()

    evento_seguinte = Event.objects.filter(
        month=next_month,
        year=next_year,
    ).first()

    event_dates = [
        (
            f"{year}-{month:02d}",
            f"{month:02d}/{year}",
        ),
        (
            f"{next_year}-{next_month:02d}",
            f"{next_month:02d}/{next_year}",
        ),
    ]

    if request.method == "POST":
        form = PreGameForm(
            request.POST,
            event_dates=event_dates,
        )

        if form.is_valid():
            selected_date = form.cleaned_data["event_date"]
            selected_year, selected_month = map(
                int,
                selected_date.split("-"),
            )

            request.session["config_game"] = {
                "is_padoru": form.cleaned_data["padoru"],
                "available": form.cleaned_data["available"],
                "month": selected_month,
                "year": selected_year,
            }

            return redirect("game")
    else:
        form = PreGameForm(event_dates=event_dates)

    return render(
        request,
        "game_manager/pre_game.html",
        {
            "form": form,
            "evento_atual": evento_atual,
            "evento_seguinte": evento_seguinte,
            "mes_atual": month,
            "ano_atual": year,
            "mes_seguinte": next_month,
            "ano_seguinte": next_year,
        },
    )

def game(request):
    config = request.session.get("config_game")

    if not config:
        return redirect("pre_game")

    if config["is_padoru"] and config["available"]:

        themes = Theme.objects.filter(
            is_padoru = config["is_padoru"],
            available = config["available"]
        )

    elif config["is_padoru"]:
        themes = Theme.objects.filter(
            is_padoru = config["is_padoru"]
        )

    elif config["available"]:
        themes = Theme.objects.filter(
            available = config["available"]
        )

    else:
        themes = Theme.objects.all()

    return render(
        request,
        "game_manager/game.html",
        {
            "themes": themes,
            "month" : config["month"],
            "year"  : config["year"]
        },
    )

def pos_game(request):
    if request.method == "POST":
        month = request.POST.get("month")
        year = request.POST.get("year")

        if not month or not year:
            return render(request, "game_manager/failed.html", {"reason": "Algo deu errado com o envio da data!"})
        
        event = Event.objects.filter(
            month = month,
            year = year
        ).first()

        if event:
            form = EventForm(request.POST, instance=event)
        else:
            form = EventForm(request.POST)

        if form.is_valid():
            form.save()
            return redirect("home")
        
        return render(request, "game_manager/failed.html", {"reason": "Formulário inválido, rever informações enviadas"})

    return redirect("pre_game")

def game_history(request):
    pass
