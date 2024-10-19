from django.db import models

class MarketData(models.Model):
    date = models.DateTimeField(auto_now_add=True)  # Automatyczne dodawanie daty
    session = models.CharField(max_length=100)
    pair = models.CharField(max_length=100)
    buy_sell = models.CharField(max_length=10, choices=[('buy', 'Buy'), ('sell', 'Sell')])
    time_frame = models.CharField(max_length=50)
    win_lose = models.CharField(max_length=10, choices=[('win', 'Win'), ('lose', 'Lose')])
    lot_size = models.CharField(max_length=10, choices=[('half', 'Half'), ('full', 'Full')])
    closed_pips = models.IntegerField()

    def __str__(self):
        return f"{self.date} - {self.pair} - {self.win_lose}"