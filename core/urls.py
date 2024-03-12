from django.urls import path 
from .views import *


urlpatterns = [
    path('', index, name='index'),
    path('marine_log/', marine_diary_view, name='marine-view'),
    path('report/', report_view, name='report-view'),
    path('report/top-10-fishing-qty-on-24h/', top_10_fishing_api, name='top-10-fishing-24h'),

    # Journal
    path('journal/', journal_view, name='journal-view'),
    path('journal/auto-generate-pdf/<pk>/', generate_journal_pdf, name='generate-journal-pdf'),
    path('journal/view_journal_pdf/<pk>/', journal_pdf_view, name='journal_pdf'),

    # Device: ship
    path('device/', device_view, name='device-view'),
    path('device/add-new-device/', add_new_device_view, name='add-device'),
    path('device/edit-device/<pk>/', edit_device_view, name='edit-device'),
    path('device/delete-device/<pk>/', delete_device_view, name='delete-device'),
    path('device/search/', search_device_view, name='search-device'),
    path('device/download/<number>/', download_device_data, name='download-device-data'),

    path('shipowners/', shipowners_view, name='shipowners-view'),
    path('shipowners/search/', search_shipowners_view, name='search-shipowners'),
    path('shipowners/add-new-shipowner/', add_shipowners_view, name='add-shipowners'),
    path('shipowners/edit-shipowner/<pk>&<user_type>/', edit_shipowners_view, name='edit-shipowners'),

    path('account/', account_view, name='account-view'),
]

# Authentication
urlpatterns += [
    path('login/', login_view, name='login'),
    path('logout/', logout_view, name='logout'),
]

# RESTful API
urlpatterns += [
    path('api/location/<pk>/', get_location_view_api, name='get-location-api'),
    path('api/all-location/', get_all_location_api, name='all-location'),
    path('api/get-marine-log/', get_ship_location_api, name='marine-log-api'),
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
