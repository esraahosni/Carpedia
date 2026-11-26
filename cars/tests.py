from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse

from .models import Car, Favourite


def make_car(**kw):
    data = dict(brand='BMW', condition='new', model_name='M3', year=2024, price=50000,
                engine='3.0L', horsepower=480, fuel_type='Petrol', transmission='Auto',
                description='x', main_image='cars/x.jpg')
    data.update(kw)
    return Car.objects.create(**data)


class PublicPagesTests(TestCase):
    def test_pages_load(self):
        make_car()
        for name in ['home', 'car_list', 'new_cars', 'used_cars', 'about_us', 'register']:
            self.assertEqual(self.client.get(reverse(name)).status_code, 200, name)

    def test_filter(self):
        make_car()
        r = self.client.get(reverse('car_list'), {'brand': 'bmw', 'max_price': 60000})
        self.assertContains(r, 'M3')


class ActionSafetyTests(TestCase):
    def setUp(self):
        self.admin = User.objects.create_user('admin', password='pw12345!', is_staff=True)
        self.user = User.objects.create_user('bob', password='pw12345!')
        self.car = make_car()

    def test_delete_car_requires_post(self):
        self.client.force_login(self.admin)
        self.client.get(reverse('delete_car', args=[self.car.pk]))
        self.assertTrue(Car.objects.filter(pk=self.car.pk).exists())
        self.client.post(reverse('delete_car', args=[self.car.pk]))
        self.assertFalse(Car.objects.filter(pk=self.car.pk).exists())

    def test_non_admin_cannot_promote(self):
        self.client.force_login(self.user)
        self.client.post(reverse('promote_user', args=[self.user.pk]))
        self.user.refresh_from_db()
        self.assertFalse(self.user.is_staff)

    def test_promote_get_does_nothing(self):
        self.client.force_login(self.admin)
        self.client.get(reverse('promote_user', args=[self.user.pk]))
        self.user.refresh_from_db()
        self.assertFalse(self.user.is_staff)

    def test_favourite_toggle_post_only(self):
        self.client.force_login(self.user)
        self.client.get(reverse('toggle_favourite', args=[self.car.pk]))
        self.assertEqual(Favourite.objects.count(), 0)
        self.client.post(reverse('toggle_favourite', args=[self.car.pk]))
        self.assertEqual(Favourite.objects.count(), 1)
        self.client.post(reverse('toggle_favourite', args=[self.car.pk]))
        self.assertEqual(Favourite.objects.count(), 0)

    def test_favourite_ignores_external_referer(self):
        self.client.force_login(self.user)
        r = self.client.post(reverse('toggle_favourite', args=[self.car.pk]),
                             HTTP_REFERER='https://evil.example/')
        self.assertRedirects(r, reverse('car_list'), fetch_redirect_response=False)

    def test_profile_shows_favourite_image(self):
        Favourite.objects.create(user=self.user, car=self.car)
        self.client.force_login(self.user)
        self.assertContains(self.client.get(reverse('profile')), 'cars/x.jpg')

    def test_admin_pages_render_forms(self):
        self.client.force_login(self.admin)
        self.assertContains(self.client.get(reverse('manage_cars')), 'method="post"')
        self.assertContains(self.client.get(reverse('user_management')), 'csrfmiddlewaretoken')


class SeedTests(TestCase):
    def test_seed_is_idempotent_and_renders(self):
        from django.core.management import call_command
        call_command('seed_cars'); call_command('seed_cars')
        self.assertEqual(Car.objects.count(), 10)
        r = self.client.get(reverse('car_list'))
        self.assertContains(r, 'images/seed/')


class PublicDetailAndStatsTests(TestCase):
    def test_detail_is_public_and_home_stats_are_real(self):
        from django.core.management import call_command
        call_command('seed_cars')
        car = Car.objects.first()
        r = self.client.get(reverse('car_detail', args=[car.pk]))
        self.assertEqual(r.status_code, 200)
        r = self.client.get(reverse('home'))
        self.assertEqual(r.context['total_cars'], 10)
        self.assertNotContains(r, '10K+')
