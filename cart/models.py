from django.db import models
from django.contrib.auth.models import User
from movies.models import Movie

class Cart(models.Model):
    CART_CHOICES = [
        (1, "Cart 1"),
        (2, "Cart 2"),
        (3, "Cart 3"),
    ]
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    cart_number = models.IntegerField(choices=CART_CHOICES)
    movies = models.ManyToManyField(Movie, blank=True)

    def __str__(self):
        return f"{self.user.username} - Cart {self.cart_number}"

class Order(models.Model):
    id = models.AutoField(primary_key=True)
    total = models.IntegerField()
    date = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return str(self.id) + ' - ' + self.user.username

class Item(models.Model):
    id = models.AutoField(primary_key=True)
    price = models.IntegerField()
    quantity = models.IntegerField()
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE)

    def __str__(self):
        return str(self.id) + ' - ' + self.movie.name
