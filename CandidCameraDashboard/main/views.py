import os
from datetime import datetime
from os import path
from pathlib import Path

from django.http import HttpResponse, Http404
from django.shortcuts import render

from .utils import download_file, zip_ze_file, timelapse, video_to_gif


def home(request):
    return render(request, template_name='main/home.html')


def download_photos(request):
    now = datetime.now().strftime('%Y-%m-%d')
    dwnld_file_path_to_check = f'./main/tmp_cache_files/{now}'
    if not path.exists(dwnld_file_path_to_check):
        os.makedirs(f'{dwnld_file_path_to_check}/picamera_photos')

        download_file(now)
        zip_ze_file(folder_to_compress=Path(f'./main/tmp_cache_files/{now}'),
                    path_to_archive=Path(f'./main/tmp_cache_files/{now}/picamera_photos.zip'), filetype='*jpeg')

    if path.exists(f'./main/tmp_cache_files/{now}/picamera_photos.zip'):
        zip_file_path = f'./main/tmp_cache_files/{now}/picamera_photos.zip'
        zip_file = open(zip_file_path, 'rb')
        response = HttpResponse(zip_file, content_type='application/zip')
        response['Content-Disposition'] = 'attachment; filename=picamera_photos.zip'
        return response
    return Http404


def download_timelapse(request):
    now = datetime.now().strftime('%Y-%m-%d')
    dwnld_file_path_to_check = f'./main/tmp_cache_files/{now}'
    tmlps_file_path_to_check = f'{dwnld_file_path_to_check}/timelapse'
    if not path.exists(dwnld_file_path_to_check):
        os.makedirs(f'{dwnld_file_path_to_check}/picamera_photos')
        download_file(now)

    if not path.exists(tmlps_file_path_to_check):
        os.makedirs(tmlps_file_path_to_check)
        timelapse(now)
        zip_ze_file(folder_to_compress=Path(f'./main/tmp_cache_files{now}/timelapse'),
                    path_to_archive=Path(f'./main/tmp_cache_files/{now}timelapse.zip'), filetype='*avi')
        zip_file_path = f'./main/tmp_cache_files/{now}timelapse.zip'
        zip_file = open(zip_file_path, 'rb')
        response = HttpResponse(zip_file, content_type='application/zip')
        response['Content-Disposition'] = f'attachment; filename={now}timelapse.zip'
        return response
    return Http404


def video(request):
    path_to_check = './media/timelapse.gif'
    if not path.exists(path_to_check):
        video_to_gif(input_filepath='./main/tmp_cache_files/timelapse/timelapse.avi',
                     output_filepath='./media/timelapse.gif')
    return render(request, template_name='main/video.html')
