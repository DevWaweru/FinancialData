from django.db import models

# Create your models here.
class Market(models.Model):
    ticker = models.CharField(max_length=50)
    company = models.CharField(max_length=100)
    sector = models.CharField(max_length=50)
    industry = models.CharField(max_length=50)
    country = models.CharField(max_length=100)
    price = models.DecimalField(max_digits=6, decimal_places=2)
    change = models.DecimalField(max_digits=6,decimal_places=2)
    volume = models.IntegerField()
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.company

    @classmethod
    def get_all(cls):
        portfolios = Market.objects.all()
        return portfolios