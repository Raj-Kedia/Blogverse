from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User
from blog.models import Post

class BlogTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(username='testuser', password='password123', email='test@example.com')
        self.other_user = User.objects.create_user(username='otheruser', password='password123', email='other@example.com')
        
    def test_create_blog_anonymous_redirects(self):
        """Unauthenticated user should be redirected to login when trying to create a blog."""
        response = self.client.get(reverse('createblog'))
        self.assertEqual(response.status_code, 302)
        self.assertIn('/login', response.url)

    def test_create_blog_authenticated(self):
        """Authenticated user can create a blog post."""
        self.client.login(username='testuser', password='password123')
        response = self.client.post(reverse('createblog'), {
            'title': 'Test Blog Title',
            'content': 'This is a test content in markdown.'
        })
        # Check that it redirected to the newly created post
        post = Post.objects.get(title='Test Blog Title')
        self.assertRedirects(response, f"/blog/{post.slug}/")
        self.assertEqual(post.author, 'testuser')
        self.assertIn('<p>This is a test content in markdown.</p>', post.content)

    def test_create_blog_empty_validation(self):
        """Creating a blog with empty title or content should not save the post."""
        self.client.login(username='testuser', password='password123')
        # Empty title
        self.client.post(reverse('createblog'), {
            'title': '',
            'content': 'Some content'
        })
        self.assertEqual(Post.objects.count(), 0)
        
        # Empty content
        self.client.post(reverse('createblog'), {
            'title': 'Some Title',
            'content': ''
        })
        self.assertEqual(Post.objects.count(), 0)

    def test_edit_blog_anonymous_redirects(self):
        """Unauthenticated user should be redirected when trying to edit a blog."""
        post = Post.objects.create(title='My Post', content='Content', author='testuser', slug='my-post')
        response = self.client.get(f"{reverse('edit')}?sno={post.sno}")
        self.assertEqual(response.status_code, 302)

    def test_edit_blog_other_user_forbidden(self):
        """A user cannot edit another user's blog post."""
        post = Post.objects.create(title='My Post', content='Content', author='testuser', slug='my-post')
        self.client.login(username='otheruser', password='password123')
        response = self.client.get(f"{reverse('edit')}?sno={post.sno}")
        self.assertRedirects(response, reverse('home'))

    def test_edit_blog_author_success(self):
        """The author of a post can successfully edit it."""
        post = Post.objects.create(title='My Post', content='Content', author='testuser', slug='my-post')
        self.client.login(username='testuser', password='password123')
        
        # GET request to load the edit form
        response = self.client.get(f"{reverse('edit')}?sno={post.sno}")
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'My Post')
        
        # POST request to save changes
        response = self.client.post(f"{reverse('edit')}?sno={post.sno}", {
            'title': 'Updated Post Title',
            'content': 'Updated content in markdown.'
        })
        post.refresh_from_db()
        self.assertEqual(post.title, 'Updated Post Title')
        self.assertIn('<p>Updated content in markdown.</p>', post.content)
        self.assertRedirects(response, f"/blog/{post.slug}/")

    def test_viewprofile_routes_correctly(self):
        """Profile view renders successfully for a given username."""
        post = Post.objects.create(title='Author Post', content='Content', author='testuser', slug='author-post')
        
        response = self.client.get(f"{reverse('viewprofile')}?username=testuser")
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'testuser')
        self.assertContains(response, 'Author Post')

    def test_anonymous_login_redirect_back(self):
        """Redirect anonymous user to login and redirect back after successful login."""
        create_url = reverse('createblog')
        response = self.client.get(create_url)
        self.assertRedirects(response, f"{reverse('handleLogin')}?next={create_url}")
        
        login_url = f"{reverse('handleLogin')}?next={create_url}"
        response = self.client.post(login_url, {
            'loginusername': 'testuser',
            'loginpassword': 'password123'
        })
        self.assertRedirects(response, create_url)
