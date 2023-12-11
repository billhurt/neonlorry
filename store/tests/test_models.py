from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse

from store.models import Category, Product


class TestCategoriesModel(TestCase):

    def setUp(self):
        self.data1 = Category.objects.create(name='django', slug='django')

    def test_category_model_entry(self):
        """
        Test Category model data insertion/types/field attributes
        This tests that the name and slug from the setUp function are correctly added/matches
        to the Category model/database
        """
        data = self.data1
        """
        data below - is tested against Category model
        """
        self.assertTrue(isinstance(data, Category))
        self.assertEqual(str(data), 'django')

    def test_category_url(self):
        """
        Test category model slug and URL reverse
        """
        data = self.data1
        response = self.client.post(
            reverse('store:category_list', args=[data.slug]))
        self.assertEqual(response.status_code, 200)


class TestProductsModel(TestCase):

    def setUp(self):
        Category.objects.create(name='django', slug='django')
        User.objects.create(username='_billhurt')
        self.data1 = Product.objects.create(
            category_id=1,
            title="Bramhope Brew",
            created_by_id=1,
            slug='bramhope-brew',
            price='9.99',
            image='dave'
        )

    def test_products_model_entry(self):
        """
        Test Product model data insertion/types/field attributes
        """
        data = self.data1
        """
        This data is entered into test database during setUp function.
        We can access this instance again for this test
        """
        self.assertTrue(isinstance(data, Product))
        self.assertEqual(str(data), 'Bramhope Brew')
