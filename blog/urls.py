
from rest_framework.routers import DefaultRouter
from .views import CategoryView, PostView

router=DefaultRouter()
router.register('category', CategoryView)
router.register('post', PostView)

urlpatterns =router.urls
