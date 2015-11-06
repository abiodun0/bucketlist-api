import unittest
import time
from datetime import datetime
from app import create_app, db
from app.models import User, Item, Bucketlist


class UserModelTestCase(unittest.TestCase):
    def setUp(self):
        self.app = create_app('testing')
        self.app_context = self.app.app_context()
        self.app_context.push()
        db.create_all()
        self.user = User(email="abiodun@golden0.com",password="passes")
        self.user.save()
        self.bucket_item = Bucketlist(name="Bucket List 1", user_id=self.user.id)
        self.bucket_item.save()

        self.item = Item(name="Needs of bucket items", bucketlist_id=self.bucket_item.id)
        self.item.save()

    def tearDown(self):
        db.session.remove()
        db.drop_all()
        self.app_context.pop()

    def test_for_data_exsitence(self):
        bucketlist = Bucketlist.query.all()
        self.assertEqual(len(bucketlist),1)
    def test_for_data_exsitence(self):
        self.bucket_item.delete()
        bucketlist = Bucketlist.query.all()
        self.assertNotEqual(len(bucketlist),1)

    def test_for_edit_feature(self):
        self.item.edit("My Test Item")
        self.item.save()
        self.bucket_item.edit("My Test Item")
        self.bucket_item.save()

        self.assertEqual(self.bucket_item.name, "My Test Item")
        self.assertEqual(self.item.name, "My Test Item")

    def test_password_setter(self):
        u = User(password='cat')
        self.assertTrue(u.password_hash is not None)

    def test_no_password_getter(self):
        u = User(password='cat')
        with self.assertRaises(AttributeError):
            u.password

    def test_password_salts_are_random(self):
        u = User(password='cat')
        u2 = User(password='cat')
        self.assertTrue(u.password_hash != u2.password_hash)

    def test_user_str(self):
        user = str(self.user)
        self.assertIsNotNone(user)

    def test_for_to_json(self):
        user_json = self.user.to_json()
        bucket_json = self.bucket_item.to_json()
        item_json = self.item.to_json()
        self.assertIsNotNone(item_json)
        self.assertIsNotNone(bucket_json)
        self.assertIsNotNone(user_json)
