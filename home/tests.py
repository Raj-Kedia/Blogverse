from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User
from blog.models import Post

class HomeTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(username='existinguser', password='password123', email='ex@example.com')
        
    def test_signup_username_already_exists(self):
        """Signing up with an existing username should show an error and redirect."""
        response = self.client.post(reverse('handleSignUp'), {
            'username': 'existinguser',
            'email': 'new@example.com',
            'fname': 'New',
            'lname': 'User',
            'pass1': 'password123',
            'pass2': 'password123'
        })
        self.assertRedirects(response, reverse('home'))
        # Get session messages
        messages = list(response.wsgi_request._messages)
        self.assertEqual(len(messages), 1)
        self.assertIn("Username already exists", messages[0].message)

    def test_search_results_found(self):
        """Search view returns correct post based on query."""
        post = Post.objects.create(title='Django Tips and Tricks', content='Learn Django step by step.', author='existinguser', slug='django-tips')
        
        response = self.client.get(f"{reverse('search')}?query=Django")
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Django Tips and Tricks')
        self.assertNotContains(response, 'No search results')

    def test_search_no_results(self):
        """Search view handles no match query gracefully."""
        response = self.client.get(f"{reverse('search')}?query=Python")
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'No search results')
