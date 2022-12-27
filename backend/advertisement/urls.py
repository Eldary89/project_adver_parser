from rest_framework.routers import DefaultRouter

from .views import AdvertisementModelViewSet


app_name = 'advertisement'
router = DefaultRouter()

router.register(r"", AdvertisementModelViewSet, "advertisements")
urlpatterns = router.urls

urlpatterns += [

]
