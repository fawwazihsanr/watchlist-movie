import pdb

from django.test import TestCase

from api.factories import AccountFactory, WatchlistFactory
from core.repositories.ListRepository import ListRepository


class WatchlistTestClass(TestCase):
    def setUp(self):
        self.user = AccountFactory()

    def test_create_watchlist(self):
        data = {
            'name': 'testing',
            'description': 'testing description'
        }

        message, error = ListRepository.create_list(data, self.user)
        self.assertTrue(error)

        data = {
            'name': 'testing'
        }

        message, error = ListRepository.create_list(data, self.user)
        self.assertFalse(error)

    def test_get_list(self):
        self.watchlist = WatchlistFactory(username_id=self.user.id)
        message, error = ListRepository.get_list(self.user)
        self.assertTrue(error)

        self.watchlist.delete()
        message, error = ListRepository.get_list(self.user)
        self.assertFalse(message)

    def test_get_list_by_id(self):
        self.watchlist = WatchlistFactory(username_id=self.user.id)
        message, error = ListRepository.get_list_by_id(self.user, self.watchlist.watchlist_id)
        self.assertTrue(error)

        message, error = ListRepository.get_list_by_id(self.user, 10)
        self.assertFalse(error)
        self.assertEqual(message, 'Id doesnt exist')

    def test_update_list(self):
        self.watchlist = WatchlistFactory(username_id=self.user.id)
        data = {
            'description': 'update test'
        }
        message, error = ListRepository.update_list(data, self.user, self.watchlist.watchlist_id)
        self.assertTrue(error)

        self.watchlist.delete()
        message, error = ListRepository.update_list(data, self.user, 10)
        self.assertFalse(error)
        self.assertEqual(message, 'Watchlist doesnt exist')

    def test_delete_list(self):
        self.watchlist = WatchlistFactory(username_id=self.user.id)
        message, error = ListRepository.delete_list(self.user, self.watchlist.watchlist_id)
        self.assertTrue(error)

        self.watchlist.is_deleted = True
        self.watchlist.save()

        message, error = ListRepository.delete_list(self.user, self.user.id)
        self.assertFalse(error)
        self.assertEqual(message, 'Watchlist doesnt exist')
