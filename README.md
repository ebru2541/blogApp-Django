### BLOGAPP

## Django proje kurulumu:

```py
- python -m venv env
- ./env/Scripts/activate
- pip install djangorestframework
- pip install python-decouple
- pip freeze > requirements.txt
- django-admin startproject main .
- python manage.py runserver
```

###### Repodan çektiğimiz bir projeyi requirements deki indirilen paket/versiyonları ile birlikte install etmek için kullanılacak komut ->

```py
- python -m venv env
- ./env/Scripts/activate
- pip install -r requirements.txt
```

- .gitignore ve .env dosyalarını oluştur.
- settings.py daki SECRET_KEY ' i config ile .env ye ekle

settings.py

```py
from decouple import config
SECRET_KEY = config('SECRET_KEY')
```

.env

```py
SECRET_KEY =django-insecure-&2_9wl^*c1v&z-x0g121-qceca2nm&tys+=a_!$9(6x28vech&
```

- bir app oluştur ->

```powershell
- python manage.py startapp blog
```

- ilk iş app i ve rest_framework paketini settings.py daki INSTALLED_APP e ekle ->

settings.py

```py
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    # myapp
    'blog',
    # 3rd party packages
    'rest_framework',
]
```

# model oluşturma

blog / models.py

```py
from django.db import models
from django.contrib.auth.models import User

class Category(models.Model):
    name=models.CharField(verbose_name='Kategori Adı', max_length=50)

    class Meta:
        verbose_name='Blog Kategori'
        verbose_name_plural='Kategoriler'

    def __str__(self):
        return self.name

class Post(models.Model):
    # kullanıcı silinince o kullanıcıya ait modelde silinir CASCADE. Buradaki user djangonun oluşturduğu yerleşik user import edilerek kullanılır
    user=models.ForeignKey(User, verbose_name='Kullanıcı Adı', on_delete=models.CASCADE)
    category=models.ForeignKey(Category,verbose_name='Kategori Adı', on_delete=models.CASCADE)
    title=models.CharField(verbose_name='Başlık' ,max_length=50)
    content=models.TextField(verbose_name='İçerik')
    created_date=models.DateTimeField(verbose_name='Oluşturulma T.' ,auto_now_add=True)
    updated_date=models.DateTimeField(verbose_name='Güncelllenme T.' ,auto_now=True)

    class Meta:
        verbose_name='Blog Yazısı'
        verbose_name_plural='Blog Yazıları'

    def __str__(self):
        return  f'{self.category}- {self.title}'

```

# olusturulan modeller admin e eklenir böylece admin panelde görürüz

```py
from django.contrib import admin

# Register your models here.

from .models import Category, Post

admin.site.register(Category)
admin.site.register(Post)

```

# python manage.py makemigrations

# python manage.py migrate

# serializer oluşturma

blog / serializers.py

```py

from rest_framework import serializers
from .models import Category, Post


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        exclude = []

#? bu haliyle olursa user ve category nin sadece id si olur
class PostsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        exclude = []

#! nested serializer
class PostSerializer(serializers.ModelSerializer):
    #? user ın str ve id si yazar
    user = serializers.StringRelatedField()
    user_id = serializers.IntegerField()

    #? category ın str ve id si yazar
    category = serializers.StringRelatedField()
    category_id = serializers.IntegerField()

    class Meta:
        model = Post
        exclude = [
            # 'created_date',
            # 'updated_date',
        ]

```

# view oluşturma

blog / views.py

```py

from rest_framework.viewsets import ModelViewSet
from .serializers import (
    Category ,CategorySerializer,
    Post, PostSerializer , PostsSerializer
)

class CategoryView(ModelViewSet):
    queryset=Category.objects.all()
    serializer_class=CategorySerializer


class PostView(ModelViewSet):
    queryset=Post.objects.all()
    serializer_class=PostSerializer



class PostsView(ModelViewSet):
    queryset=Post.objects.all()
    serializer_class=PostsSerializer

```

# urls oluşturma

main / urls.py

```py

from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('user/', include('user.urls')),
    path('blog/', include('blog.urls'))
]
```

blog / urls.py

```py
from rest_framework.routers import DefaultRouter
from .views import CategoryView, PostView, PostsView

router=DefaultRouter()
router.register('category', CategoryView)
router.register('post', PostView)
router.register('posts', PostsView)


urlpatterns =router.urls

```

# User oluşturma : djangonun yerleşik user sistemindeki kullanacağız user app oluştur. model kısmında bişey yaapmayacağız ekleme yapmak istersek serializer de yapılır

# python manage.py startapp blog

user / seriallizer.py

```py
from rest_framework import serializers
from django.contrib.auth.models import User

class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        # data da görmek istemediklerimiz
        exclude = [
            # "password",
            "last_login",
            "date_joined",
            "groups",
            "user_permissions",
        ]

#! password şifreli yazabilmek için
    def validate(self, attrs):
        from django.contrib.auth.password_validation import validate_password #paswordu doğrulama fonksiyonu
        from django.contrib.auth.hashers import make_password # passwordu şifreleme fonksiyonu
        password = attrs['password'] # Password al.
        validate_password(password) # Validation'dan geçir.
        attrs.update(
            {
                'password': make_password(password) # Password şifrele ve güncelle.
            }
        )
        return super().validate(attrs) # Orjinal methodu çalıştır.
```

# Token ile şifreleme

main /settings.py

```py
INSTALL_APPS=[
    'rest_framework.authtoken'
]
```

- python.manage.py makemigrations
- python manage-py migrate

main /settings.py

```py
REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': ['rest_framework.authentication.TokenAuthentication'],
    'DEFAULT_PERMISSION_CLASSES': ['rest_framework.permissions.IsAuthenticatedOrReadOnly'],

}

```

user / urls.py

```py
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import UserView
from rest_framework.authtoken.views import obtain_auth_token

# ----------------------------------------------------------------
# Logout function:
from rest_framework.decorators import api_view
from rest_framework.response import Response
@api_view(['GET', 'POST'])
def logout(request):
    request.user.auth_token.delete() # Token Sil.
    return Response({"message": 'User Logout: Token Deleted'})
# ----------------------------------------------------------------


router = DefaultRouter()
router.register('', UserView)

urlpatterns = [
    path('', include(router.urls)),
    path('login', obtain_auth_token), # login yaparken token alır
    path('logout', logout),
]

```
