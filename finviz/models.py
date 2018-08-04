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

    class Meta:
        ordering = ('id',)

    @classmethod
    def get_all(cls):
        portfolios = Market.objects.all()
        return portfolios
    
    @classmethod
    def get_top_earners(cls, date):
        earners = Market.objects.filter(date__date=date).order_by('-change')[:10]
        return earners
    
    @classmethod
    def get_by_country(cls, country, date):
        portfolios = Market.objects.filter(country=country, date__date=date)
        return portfolios

    @classmethod
    def get_earners_by_country(cls, country, date):
        portfolios = Market.objects.filter(country=country, date__date=date).order_by('-change')[:10]
        return portfolios

    @classmethod
    def get_today(cls, date):
        portfolios = Market.objects.filter(date__date=date)
        return portfolios