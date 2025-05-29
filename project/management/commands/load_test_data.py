import random

from django.core.management.base import BaseCommand
from django.contrib.auth.models import User

from ads.models import Ad

DESCRIPTIONS = [
    'В хорошем состоянии', 'Почти не использовался',
    'Небольшие следы использования', 'Все работает отлично',
    'Без дефектов', 'Нужен небольшой ремонт',
    'Полностью исправен', 'Отличное состояние',
    'Использовался бережно', 'Есть незначительные царапины',
]


class Command(BaseCommand):
    help = 'Создает 10 тестовых пользователей с 2 объявлениями у каждого'

    def handle(self, *args, **options):
        User.objects.filter(username__startswith='test_user_').delete()

        categories = [choice[0] for choice in Ad.CATEGORY_CHOICES]
        conditions = [choice[0] for choice in Ad.CONDITION_CHOICES]

        for i in range(10):
            username = f'test_user_{i+1}'
            password = f'password{i+1}'
            user = User.objects.create_user(
                username=username,
                password=password,
                email=f'test{i+1}@example.com'
            )

            for j in range(2):
                title = f"Объявление №{i+1}-{j+1}"
                description = f"{random.choice(DESCRIPTIONS)}."
                
                Ad.objects.create(
                    user=user,
                    title=title,
                    description=description,
                    category=random.choice(categories),
                    condition=random.choice(conditions)
                )

        print('Успешно создано 10 пользователей с 20 объявлениями!')
