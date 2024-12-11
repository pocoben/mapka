from django.db import models
from django.contrib.auth.models import User

class UserInfo(models.Model):
    # Define choices for Polish provinces with tags
    WOJEWODZTWO_CHOICES = [
        ('PL-DS', 'Dolnośląskie'),
        ('PL-KP', 'Kujawsko-Pomorskie'),
        ('PL-LU', 'Lubelskie'),
        ('PL-LB', 'Lubuskie'),
        ('PL-LD', 'Łódzkie'),
        ('PL-MA', 'Małopolskie'),
        ('PL-MZ', 'Mazowieckie'),
        ('PL-OP', 'Opolskie'),
        ('PL-PK', 'Podkarpackie'),
        ('PL-PD', 'Podlaskie'),
        ('PL-PM', 'Pomorskie'),
        ('PL-SL', 'Śląskie'),
        ('PL-SK', 'Świętokrzyskie'),
        ('PL-WN', 'Warmińsko-Mazurskie'),
        ('PL-WP', 'Wielkopolskie'),
        ('PL-ZP', 'Zachodniopomorskie'),
    ]

    PLEC_CHOICES = [
        ('m', 'mężczyzna'),
        ('k', 'kobieta')
    ]

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    wojewodztwo = models.CharField(max_length=32, choices=WOJEWODZTWO_CHOICES)
    plec = models.CharField(max_length=32, choices=PLEC_CHOICES)
    clickCount = models.IntegerField(default=0)
    wiek = models.IntegerField(default=0)
    
    @property
    def wojewodztwo_code(self):
        # Return the province tag (e.g., 'PL-DS') directly from the wojewodztwo field
        return self.wojewodztwo

    def __str__(self):
        # Display the username with both province name and code
        province_name = dict(self.WOJEWODZTWO_CHOICES).get(self.wojewodztwo, "Unknown Province")
        return f"{self.user.username} - {province_name} ({self.wojewodztwo_code})"