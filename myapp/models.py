from django.db import models

class MarketData(models.Model):
    date = models.DateField()
    time = models.TimeField()
    session = models.CharField(max_length=50)
    pair = models.CharField(max_length=20)
    buy_sell = models.CharField(max_length=4)
    time_frame = models.CharField(max_length=20)
    win_lose = models.CharField(max_length=4)
    lot_size = models.FloatField()
    closed_pips = models.IntegerField()

    def __str__(self):
        return f"{self.pair} - {self.buy_sell} ({self.date} {self.time})"