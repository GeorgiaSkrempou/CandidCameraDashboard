from django.urls import path

from .views import home, download_photos, download_timelapse

app_name = 'main'

urlpatterns = [
    path('', home, name='home'),
    path('download_photos/', download_photos, name='download_photos'),
    path('download_timelapse/', download_timelapse, name='download_timelapse')
]
