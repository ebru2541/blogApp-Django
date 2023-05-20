from faker import Faker
from django.contrib.auth.models import User
from .models import Category, Post

def run():
    fake = Faker(['tr-TR'])
    categories = ('Gezi', 'Yemek', 'Spor', 'Ekonomi')

    for category in categories:
        new_category = Category.objects.create(name=category)
        for _ in range(50):
            Post.objects.create(
                title = fake.sentence(),
                content = fake.text(),
                category = new_category,
                user = User.objects.first()
            )

    print('Finished')
