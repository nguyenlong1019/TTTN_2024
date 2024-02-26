from django.urls import path 
from .views import *


urlpatterns = [
    path('', index, name='index'),
    path('report/', report_view, name='report-view'),
    path('journal/', journal_view, name='journal-view'),
    path('device/', device_view, name='device-view'),
    path('shipowners/', shipowners_view, name='shipowners-view'),
    path('account/', account_view, name='account-view'),
]

# Authentication
urlpatterns += [
    path('login/', login_view, name='login'),
    path('logout/', logout_view, name='logout'),
]

# Mobile API 
urlpatterns += [
    path('mobile-api/test/', test_api_mobile, name='test-mobile-api'),
    path('mobile-api/realtime-location/', ship_realtime_location, name='realtime-location'),
    path('mobile-api/ships/', ship_name_list, name='ships'),
    path('mobile-api/ship-location-logs/', ship_location_log, name='logs'),
    path('mobile-api/mining-log/', mining_log, name='mining-log'),
    path('mobile-api/login/', login_mobile, name='mobile-login'),
]
