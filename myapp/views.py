
import requests
import pandas as pd
from django.shortcuts import render,redirect
from django.http import HttpResponse
from .models import MarketData  # Model danych rynkowych
from datetime import datetime

def home_view(request):
    weather = None
    if request.method == 'POST' and 'city' in request.POST:
        city = request.POST.get('city')
        api_key = '1c6b720a7a30c794eb6d83ecc05f877c'
        url = f'http://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}&units=metric'
        response = requests.get(url)
        data = response.json()
        if response.status_code == 200:
            weather = {
                'city': data['name'],
                'temperature': data['main']['temp'],
                'description': data['weather'][0]['description'],
                'icon': data['weather'][0]['icon'],
            }

    market_data = MarketData.objects.all()

    return render(request, 'home.html', {'weather': weather, 'market_data': market_data})


def add_market_data(request):
    if request.method == 'POST':
        date = request.POST.get('date')
        time = request.POST.get('time')
        session = request.POST.get('session')
        pair = request.POST.get('pair')
        buy_sell = request.POST.get('buy_sell')
        time_frame = request.POST.get('time_frame')
        win_lose = request.POST.get('win_lose')
        lot_size = request.POST.get('lot_size')
        closed_pips = request.POST.get('closed_pips')

        # Dodanie danych do bazy
        MarketData.objects.create(
            date=date,
            time=time,
            session=session,
            pair=pair,
            buy_sell=buy_sell,
            time_frame=time_frame,
            win_lose=win_lose,
            lot_size=lot_size,
            closed_pips=closed_pips
        )
        
        # Przekierowanie do widoku przeglądu danych po dodaniu nowego wpisu
        return redirect('home')  # Przekierowuje do strony głównej, gdzie wyświetlane są dane rynkowe

def export_to_csv(request):
    market_data = MarketData.objects.all().values(
        'date', 'time', 'session', 'pair', 'buy_sell', 'time_frame', 'win_lose', 'lot_size', 'closed_pips'
    )
    df = pd.DataFrame(market_data)
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="market_data.csv"'
    df.to_csv(response, index=False)
    return response