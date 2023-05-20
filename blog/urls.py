
from rest_framework.routers import DefaultRouter
from .views import CategoryView, PostView, PostsView

router=DefaultRouter()
router.register('category', CategoryView)
router.register('post', PostView)
router.register('posts', PostsView)


urlpatterns =router.urls
