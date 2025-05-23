from django.db import models
from django.conf import settings


class Ad(models.Model):
    CATEGORY_CHOICES = [
        ('books', 'Книги'),
        ('clothes', 'Одежда'),
        ('appliances', 'Бытовая техника'),
        ('furniture', 'Мебель'),
        ('toys', 'Игрушки'),
        ('other', 'Другое'),
    ]

    CONDITION_CHOICES = [
        ('new', 'Новый'),
        ('old', 'Старый'),
    ]

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='ad',
    )
    title = models.CharField(max_length=200)
    description = models.TextField()
    image_url = models.URLField(blank=True)
    category = models.CharField(
        max_length=50,
        choices=CATEGORY_CHOICES,
        default='other',
    )
    condition = models.CharField(
        max_length=10,
        choices=CONDITION_CHOICES,
        default='new',
    )
    created_at = models.DateTimeField(auto_now_add=True)


class ExchangeProposal(models.Model):
    STATUS_CHOICES = [
        ('pending', 'ожидает'),
        ('accepted', 'принята'),
        ('rejected', 'отклонена'),
    ]

    ad_sender = models.ForeignKey(
        Ad,
        on_delete=models.CASCADE,
        related_name='ad_sender',
    )
    ad_receiver = models.ForeignKey(
        Ad,
        on_delete=models.CASCADE,
        related_name='ad_receiver',
    )
    comment = models.TextField(blank=True)
    status = models.CharField(
        max_length=10,
        choices=STATUS_CHOICES,
        default='pending',
    )
    created_at = models.DateTimeField(auto_now_add=True)
