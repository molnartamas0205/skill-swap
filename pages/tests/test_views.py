from django.test import TestCase
from django.urls import reverse
from tutoring.models import TutoringService, Category, CustomUser  

class StaticViewTests(TestCase):
    def test_home_view(self):
        response = self.client.get(reverse('home'))  
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'home.html')

    def test_about_view(self):
        response = self.client.get(reverse('about'))  
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'about.html')


class SearchSubjectsViewTests(TestCase):
    def setUp(self):
        self.category = Category.objects.create(name="Mathematics")
        
        self.user = CustomUser.objects.create_user(
            username='testuser', 
            password='password',
            email='testuser@example.com',  
            full_name='Test User'  
        )
        
        self.tutor1 = TutoringService.objects.create(
            title="Algebra Tutor",
            category=self.category,
            price=20.00,
            user=self.user  
        )
        self.tutor2 = TutoringService.objects.create(
            title="Geometry Tutor",
            category=self.category,
            price=25.00,
            user=self.user  
        )

    def test_search_valid_query(self):
        response = self.client.post(reverse('search-subjects'), {'searched': 'Algebra'})
        self.assertEqual(response.status_code, 200)
        self.assertIn(self.tutor1, response.context['tutors'])
        self.assertNotIn(self.tutor2, response.context['tutors'])

    def test_search_invalid_query(self):
        response = self.client.post(reverse('search-subjects'), {'searched': 'Physics'})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.context['tutors']), 0)

    def test_search_empty_query(self):
        response = self.client.post(reverse('search-subjects'), {'searched': ''})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.context['tutors']), 0)

    def test_search_get_request(self):
        response = self.client.get(reverse('search-subjects'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'search_subjects.html')


class CategoryListViewTests(TestCase):

    def setUp(self):
        self.category1 = Category.objects.create(name="Mathematics")
        self.category2 = Category.objects.create(name="Physics")

    def test_category_list_view(self):
        
        response = self.client.get(reverse('categories')) 
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'categories.html')
        self.assertIn(self.category1, response.context['categories'])
        self.assertIn(self.category2, response.context['categories'])


class CategoryDetailViewTests(TestCase):

    def setUp(self):
        self.category = Category.objects.create(name="Mathematics")
        
        self.user = CustomUser.objects.create_user(
            username='testuser', 
            password='password',
            email='testuser@example.com',  
            full_name='Test User'  
        )
        
        self.tutor1 = TutoringService.objects.create(
            title="Algebra Tutor",
            category=self.category,
            price=20.00,
            user=self.user 
        )
        self.tutor2 = TutoringService.objects.create(
            title="Geometry Tutor",
            category=self.category,
            price=25.00,
            user=self.user  
        )

    def test_category_detail_view(self):
        response = self.client.get(reverse('category_detail', args=[self.category.name])) 
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'category_detail.html')
        self.assertEqual(response.context['category'], self.category)
        self.assertIn(self.tutor1, response.context['tutors'])
        self.assertIn(self.tutor2, response.context['tutors'])

    def test_category_detail_view_not_found(self):
        response = self.client.get(reverse('category_detail', args=['NonExistentCategory']))  
        self.assertEqual(response.status_code, 404)
