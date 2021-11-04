from django.db import models


class Menu(models.Model):
    SALAD, MILK, EGG = ('salad', 'milk', 'egg')
    NEW, OLD = ('new', 'old')

    CATEGORY_STATE_CHOICES = (
        (SALAD, 'SALAD'),
        (MILK, 'MILK'),
        (EGG, 'EGG'),
    )

    BADGE_STATE_CHOICES = (
        (NEW, 'NEW'),
        (OLD, 'OLD')
    )

    category = models.CharField(max_length=30, choices=CATEGORY_STATE_CHOICES)
    name = models.CharField(max_length=50)
    description = models.CharField(max_length=200)
    isSold = models.BooleanField(default=False)
    badge = models.CharField(max_length=8, choices=BADGE_STATE_CHOICES, default=OLD)


class Item(models.Model):
    L, M, S = ('L', 'M', 'S')

    SIZE_STATE_CHOICES = (
        (L, 'L'),
        (M, 'M'),
        (S, 'S'),
    )

    name = models.CharField(max_length=50)
    size = models.CharField(max_length=10, choices=SIZE_STATE_CHOICES)
    price = models.IntegerField(default=0)
    isSold = models.BooleanField(default=False)
    menu = models.ForeignKey(Menu, on_delete=models.DO_NOTHING)


class Tag(models.Model):
    name = models.CharField(max_length=50)
    type = models.CharField(max_length=50)
    menu = models.ForeignKey(Menu, on_delete=models.DO_NOTHING)
