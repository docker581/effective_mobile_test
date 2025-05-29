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
        ('new', 'Новый товар'),
        ('old', 'Б/у товар'),
    ]

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='ad',
        verbose_name='Пользователь',
    )
    title = models.CharField(max_length=200, verbose_name='Название')
    description = models.TextField(verbose_name='Описание')
    image_url = models.URLField(blank=True,
                                verbose_name='Ссылка на изображение')
    category = models.CharField(
        max_length=50,
        choices=CATEGORY_CHOICES,
        default='other',
        verbose_name='Категория',
    )
    condition = models.CharField(
        max_length=10,
        choices=CONDITION_CHOICES,
        default='new',
        verbose_name='Условие',
    )
    created_at = models.DateTimeField(auto_now_add=True,
                                      verbose_name='Создано')

    def __str__(self):
        return self.title


class ExchangeProposal(models.Model):
    STATUS_CHOICES = [
        ('pending', 'ожидает'),
        ('accepted', 'принята'),
        ('rejected', 'отклонена'),
    ]

    ad_sender = models.ForeignKey(
        Ad,
        on_delete=models.CASCADE,
        related_name='ad_sender_id',
        verbose_name='Отправитель',
    )
    ad_receiver = models.ForeignKey(
        Ad,
        on_delete=models.CASCADE,
        related_name='ad_receiver_id',
        verbose_name='Получатель',
    )
    comment = models.TextField(blank=True, verbose_name='Комментарий')
    status = models.CharField(
        max_length=10,
        choices=STATUS_CHOICES,
        default='pending',
        verbose_name='Статус',
    )
    created_at = models.DateTimeField(auto_now_add=True,
                                      verbose_name='Создано')

    def __str__(self):
        return f'Обмен: {self.ad_sender.title} -> {self.ad_receiver.title}'
