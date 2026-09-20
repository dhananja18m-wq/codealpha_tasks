from django.test import TestCase, Client
from django.urls import reverse

class Phase1SocialMediaTests(TestCase):
    def setUp(self):
        self.client = Client()

    def test_home_page_status_and_template(self):
        response = self.client.get(reverse('home'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'home.html')
        self.assertTemplateUsed(response, 'base.html')
        self.assertTemplateUsed(response, 'components/post_card.html')

    def test_home_page_feed_content(self):
        response = self.client.get(reverse('home'))
        posts = response.context['posts']
        self.assertEqual(len(posts), 3)
        # Check first post details
        self.assertEqual(posts[0]['username'], 'nathanrsl')
        self.assertIn("Nature's beauty", posts[0]['caption'])
        self.assertIn("12.3K", posts[0]['formatted_likes'])
        self.assertGreater(len(posts[0]['comments']), 0)
        # Verify DOM elements
        content = response.content.decode('utf-8')
        self.assertIn('Aura', content)
        self.assertIn('like-btn', content)
        self.assertIn('Add a comment...', content)
        self.assertIn('likes-count', content)

    def test_profile_page_status_and_content(self):
        response = self.client.get(reverse('profile'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'profile.html')
        self.assertTemplateUsed(response, 'base.html')

        profile = response.context['profile']
        self.assertEqual(profile['username'], 'rachelflow')
        self.assertEqual(profile['full_name'], 'Rachel Flowear')
        self.assertEqual(profile['posts_count'], 240)
        self.assertEqual(profile['formatted_followers'], '47.3K')
        self.assertEqual(profile['formatted_following'], '32K')
        self.assertEqual(len(profile['posts']), 6)

        content = response.content.decode('utf-8')
        self.assertIn('Rachel Flowear', content)
        self.assertIn('@rachelflow', content)
        self.assertIn('profileFollowBtn', content)
        self.assertIn('profile-posts-grid', content)

    def test_navigation_strictly_home_and_profile(self):
        response = self.client.get(reverse('home'))
        content = response.content.decode('utf-8')
        # Home & Profile navigation present
        self.assertIn('href="/"', content)
        self.assertIn('href="/profile/"', content)
        # Strict Phase 1 scope: Ensure no out-of-scope nav items
        self.assertNotIn('href="/explore"', content)
        self.assertNotIn('href="/messages"', content)
        self.assertNotIn('href="/notifications"', content)
        self.assertNotIn('href="/reels"', content)

    def test_static_assets_referenced(self):
        response = self.client.get(reverse('home'))
        content = response.content.decode('utf-8')
        self.assertIn('/static/css/main.css', content)
        self.assertIn('/static/css/animations.css', content)
        self.assertIn('/static/js/app.js', content)
