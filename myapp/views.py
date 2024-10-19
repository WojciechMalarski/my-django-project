
import requests
import pandas as pd
from django.shortcuts import render,redirect
from django.http import HttpResponse
from .models import MarketData  # Model danych rynkowych
from datetime import datetime
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import numpy as np
import base64
from io import BytesIO
from django.shortcuts import render
from django.utils import timezone
from collections import Counter

def home_view(request):
    if request.method == 'POST':
        session = request.POST['session']
        pair = request.POST['pair']
        buy_sell = request.POST['buy_sell']
        time_frame = request.POST['time_frame']
        win_lose = request.POST['win_lose']
        lot_size = request.POST['lot_size']
        closed_pips = request.POST['closed_pips']
        
        # Tworzenie nowego wpisu
        MarketData.objects.create(
            session=session,
            pair=pair,
            buy_sell=buy_sell,
            time_frame=time_frame,
            win_lose=win_lose,
            lot_size=lot_size,
            closed_pips=closed_pips,
        )
        
        # Przekierowanie po dodaniu wpisu
        return redirect('home')

    # Zbieranie danych do wykresu
    entries = MarketData.objects.all()
    results = [entry.win_lose for entry in entries]
    count_results = Counter(results)
    
    # Przygotowanie danych do wykresu
    labels = count_results.keys()
    values = count_results.values()

    # Tworzenie wykresu
    plt.figure(figsize=(10, 5))
    plt.bar(labels, values, color=['green', 'red'])
    plt.title('Ilość wygranych i przegranych')
    plt.xlabel('Wynik')
    plt.ylabel('Ilość')

    # Zapisz wykres do bufora
    buf = BytesIO()
    plt.savefig(buf, format='png')
    plt.close()
    buf.seek(0)

    # Konwertowanie wykresu do base64
    image_png = base64.b64encode(buf.getvalue()).decode('utf-8')
    market_data = MarketData.objects.all()
    return render(request, 'home.html', {'entries': entries, 'chart': image_png,'market_data': market_data})




def add_market_data(request):
    if request.method == 'POST':
        date = request.POST.get('date')
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