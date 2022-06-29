from pathlib import Path

from django.http import HttpResponse
from django.shortcuts import render

from .utils import download_file, zip_ze_file, timelapse


def home(request):
    return render(request, template_name='main/home.html')


def download_photos(request):
    download_file()
    zip_ze_file(folder_to_compress=Path('./main/tmp_cache_files'),
                path_to_archive=Path('./main/tmp_cache_files/picamera_photos.zip'), filetype='*jpeg')
    zip_file_path = './main/tmp_cache_files/picamera_photos.zip'
    zip_file = open(zip_file_path, 'rb')
    response = HttpResponse(zip_file, content_type='application/zip')
    response['Content-Disposition'] = 'attachment; filename=picamera_photos.zip'
    return response


def download_timelapse(request):
    download_file()
    timelapse()
    zip_ze_file(folder_to_compress=Path('./main/tmp_cache_files'),
                path_to_archive=Path('./main/tmp_cache_files/timelapse.zip'), filetype='*avi')
    zip_file_path = './main/tmp_cache_files/timelapse.zip'
    zip_file = open(zip_file_path, 'rb')
    response = HttpResponse(zip_file, content_type='application/zip')
    response['Content-Disposition'] = 'attachment; filename=timelapse.zip'
    return response


def video(request):
    video_path = '/home/georgia/codes/CCDashboard/CandidCameraDashboard/main/tmp_cache_files/timelapse/timelapse.avi'
    context = {
        'video_path': video_path
    }
    return render(request, template_name='main/video.html', context=context)
