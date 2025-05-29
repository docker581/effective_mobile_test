from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User
from django.contrib.messages import get_messages

from ..models import Ad, ExchangeProposal


class AdViewsTest(TestCase):
    def setUp(self):
        self.user1 = User.objects.create_user(
            username='testuser1',
            password='testpass123',
        )
        self.user2 = User.objects.create_user(
            username='testuser2',
            password='testpass123',
        )
        
        self.ad1 = Ad.objects.create(
            user=self.user1,
            title='Тестовое объявление 1',
            description='Описание тестового объявления 1',
            category='books',
            condition='new',
        )
        self.ad2 = Ad.objects.create(
            user=self.user2,
            title='Тестовое объявление 2',
            description='Описание тестового объявления 2',
            category='toys',
            condition='old',
        )
        
        self.client = Client()

    def test_index_view(self):
        response = self.client.get(reverse('index'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Тестовое объявление 1')
        self.assertContains(response, 'Тестовое объявление 2')

    def test_ad_detail_view(self):
        response = self.client.get(reverse('ad_detail', args=[self.ad1.pk]))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.ad1.title)
        self.assertContains(response, self.ad1.description)

    def test_ad_create_view(self):
        self.client.login(username='testuser1', password='testpass123')
        
        response = self.client.get(reverse('ad_create'))
        self.assertEqual(response.status_code, 200)
        
        data = {
            'title': 'Новое объявление',
            'description': 'Описание нового объявления',
            'category': 'books',
            'condition': 'new',
        }
        response = self.client.post(reverse('ad_create'), data)
        self.assertEqual(response.status_code, 302)  
        
        self.assertTrue(
            Ad.objects.filter(title='Новое объявление').exists()
        )

    def test_ad_edit_view(self):
        self.client.login(username='testuser1', password='testpass123')
        data = {
            'title': 'Измененное объявление',
            'description': 'Измененное описание',
            'category': 'books',
            'condition': 'new',
        }
        response = self.client.post(
            reverse('ad_edit', args=[self.ad1.pk]),
            data,
        )
        self.assertEqual(response.status_code, 302)
        updated_ad = Ad.objects.get(pk=self.ad1.pk)
        self.assertEqual(updated_ad.title, 'Измененное объявление')
        
        self.client.logout()
        self.client.login(username='testuser2', password='testpass123')
        response = self.client.post(
            reverse('ad_edit', args=[self.ad1.pk]),
            data,
        )
        self.assertEqual(response.status_code, 302)
        messages = list(get_messages(response.wsgi_request))
        self.assertIn('У вас нет прав на редактирование', 
                      str(messages[0]))

    def test_ad_delete_view(self):
        self.client.login(username='testuser2', password='testpass123')
        response = self.client.post(reverse('ad_delete', args=[self.ad1.pk]))
        self.assertEqual(response.status_code, 302)
        messages = list(get_messages(response.wsgi_request))
        self.assertIn('У вас нет прав на удаление', 
                      str(messages[0]))
        self.assertTrue(Ad.objects.filter(pk=self.ad1.pk).exists())

        self.client.logout()
        self.client.login(username='testuser1', password='testpass123')
        response = self.client.post(reverse('ad_delete', args=[self.ad1.pk]))
        self.assertEqual(response.status_code, 302)
        self.assertFalse(Ad.objects.filter(pk=self.ad1.pk).exists())


class ExchangeProposalViewsTest(TestCase):
    def setUp(self):
        self.user1 = User.objects.create_user(
            username='testuser1',
            password='testpass123',
        )
        self.user2 = User.objects.create_user(
            username='testuser2',
            password='testpass123',
        )
        
        self.ad1 = Ad.objects.create(
            user=self.user1,
            title='Объявление пользователя 1',
            description='Описание объявления 1',
            category='books',
            condition='new',
        )
        self.ad2 = Ad.objects.create(
            user=self.user2,
            title='Объявление пользователя 2',
            description='Описание объявления 2',
            category='toys',
            condition='old',
        )
        
        self.client = Client()

    def test_proposal_create_view(self):
        self.client.login(username='testuser1', password='testpass123')
        
        response = self.client.post(
            reverse('proposal_create', args=[self.ad1.pk]),
            {
                'ad_sender': self.ad1.pk,
                'ad_receiver': self.ad2.pk,
                'comment': 'Тестовый комментарий к предложению',
            }
        )
        self.assertEqual(response.status_code, 302)
        messages = list(get_messages(response.wsgi_request))
        self.assertIn('Вы не можете предложить обмен для своего', 
                      str(messages[0]))
        
        response = self.client.get(
            reverse('proposal_create', args=[self.ad2.pk])
        )
        self.assertEqual(response.status_code, 200)
        
        data = {
            'ad_sender': self.ad1.pk,
            'ad_receiver': self.ad2.pk,
            'comment': 'Тестовый комментарий к предложению',
        }
        response = self.client.post(
            reverse('proposal_create', args=[self.ad2.pk]),
            data,
        )
        self.assertEqual(response.status_code, 302)
        self.assertTrue(
            ExchangeProposal.objects.filter(
                ad_sender=self.ad1,
                ad_receiver=self.ad2
            ).exists()
        )

    def test_proposal_list_view(self):
        self.client.login(username='testuser1', password='testpass123')
        
        proposal = ExchangeProposal.objects.create(
            ad_sender=self.ad1,
            ad_receiver=self.ad2,
            comment='Тестовый комментарий',
            status='pending',
        )
        
        response = self.client.get(reverse('proposal_list'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Тестовый комментарий') 
