from rest_framework import routers

from users.views import UserViewset, BarberViewSet
from barber_shop.views import CompanysViewSet, SchedulesViewSet
from about_us.views import AboutUsViewSet
from prices.views import PricesViewSet

router = routers.DefaultRouter(trailing_slash=False)

router.register(r'users', UserViewset, basename='users')
router.register(r'barbers', BarberViewSet, basename='barbers')
router.register(r'prices', PricesViewSet, basename='prices')
router.register(r'companys', CompanysViewSet, basename='companys')
router.register(r'schedules', SchedulesViewSet, basename='schedules')
router.register(r'about_us', AboutUsViewSet, basename='about_us')
