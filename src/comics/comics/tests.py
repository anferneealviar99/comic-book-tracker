from django.test import TestCase
from comics.models import UserComic, ComicBook
from accounts.models import CustomUser

class UserModelTestCase(TestCase):
    
    def setUp(self):
        """Create test data before each test run"""
        self.user = CustomUser.objects.create_user(username='testuser', password='testpass123')
        self.comic = ComicBook.objects.create(comic_id='123', title='Test Comic #1', series='Test Series',
                                              number=1, series_year='2026', publisher='Test Pub')
        self.user_comic = UserComic.objects.create(
            user=self.user,
            comic=self.comic
        )
        

    def test_status_update(self):
        self.assertEqual(self.user_comic.status, 'WANT')
        
        self.user_comic.status = 'COLLECTED'
        self.user_comic.save()
        
        updated_comic = UserComic.objects.get(id=self.user_comic.id)
        self.assertEqual(updated_comic.status, 'COLLECTED')
        
    def test_unique_together_constraint(self):
        """Test that a user cannot follow the same comic twice"""
        with self.assertRaises(Exception):
            UserComic.objects.create(
                user=self.user,
                comic=self.comic,
                status='WANT'
            )