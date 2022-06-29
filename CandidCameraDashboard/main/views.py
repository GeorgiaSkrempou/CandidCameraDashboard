import os

from django.http import HttpResponse
from django.shortcuts import render


def home(request):
    return render(request, template_name='main/home.html')


def download_photos(request):
    zip_file_path = '/home/georgia/codes/CCDashboard/CandidCameraDashboard/main/tmp_cache_files/picamera_photos.zip'
    zip_file = open(zip_file_path, 'rb')
    response = HttpResponse(zip_file, content_type='application/zip')
    response['Content-Disposition'] = 'attachment; filename=picamera_photos.zip'
    return response
