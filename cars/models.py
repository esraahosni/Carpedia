from django.db import models
from django.contrib.auth.models import User

class Brand(models.Model):
    name = models.CharField(max_length=100)
    logo = models.ImageField(upload_to='brands/')

    def __str__(self):
        return self.name


class CarType(models.Model):
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name


class Car(models.Model):
    CONDITION_CHOICES = [
        ('new', 'New'),
        ('used', 'Used'),
    ]

    brand = models.CharField(max_length=100)
    condition = models.CharField(max_length=10, choices=CONDITION_CHOICES, default='used')
    model_name = models.CharField(max_length=100)
    year = models.IntegerField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    engine = models.CharField(max_length=100)
    horsepower = models.IntegerField()
    fuel_type = models.CharField(max_length=50)
    transmission = models.CharField(max_length=50)
    description = models.TextField()
    main_image = models.ImageField(upload_to='cars/')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.brand} {self.model_name}"

    @property
    def image_url(self):
        """Seed photos live in static/images/seed (they persist on Vercel);
        uploaded photos use the normal media storage."""
        name = self.main_image.name if self.main_image else ''
        if not name:
            return ''
        if name.startswith('seed/'):
            from django.templatetags.static import static
            return static('images/' + name)
        return self.main_image.url


class CarImage(models.Model):
    car = models.ForeignKey(
        Car,
        related_name='images',
        on_delete=models.CASCADE
    )
    image = models.ImageField(upload_to='cars/gallery/')


class Favourite(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='favourites')
    car = models.ForeignKey(Car, on_delete=models.CASCADE, related_name='favourited_by')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'car')

    def __str__(self):
        return f"{self.user.username} ♥ {self.car}"