from django.urls import path 
from .views import *


urlpatterns = [
    path('', index, name='index'),
    path('marine_log/', marine_diary_view, name='marine-view'),
    path('report/', report_view, name='report-view'),
    path('report/top-10-fishing-qty-on-24h/', top_10_fishing_api, name='top-10-fishing-24h'),
    path('report/search/', search_report_view, name='report-search'),
    path('report/search-top-10-fish/', search_top_10_fishing_api, name='search-top-10-fish'),

    # Journal
    path('journal/', journal_view, name='journal-view'),
    path('journal/auto-generate-pdf/<pk>/', generate_journal_pdf, name='generate-journal-pdf'),
    path('journal/view_journal_pdf/<pk>/', journal_pdf_view, name='journal_pdf'),
    path('journal/search/', search_journal_view, name='search-journal'),

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
    path('shipowners/delete/<pk>/', delete_shipowners_view, name='delete-shipowners'),

    path('account/', account_view, name='account-view'),
    path('account/add-new/', add_new_account_view, name='add-account'),
    path('account/edit/<pk>/', edit_account_view, name='edit-account'),
    path('account/search/', search_account_view, name='search-account'),
    path('account/delete/<pk>/', delete_account_view, name='delete-account'),

    # path('provider-home/', provider_home_view, name='provider-home'),
    path('equipment/add-new/', add_new_equipment_view, name='add-equipment'),
    path('equipment/edit/<pk>/', edit_equipment_view, name='edit-equipment'),
    path('equipment/search/', search_equipment_view, name='search-equipment'),
    path('equipment/delete/<pk>/', delete_equipment_view, name='delete-equipment'),
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
