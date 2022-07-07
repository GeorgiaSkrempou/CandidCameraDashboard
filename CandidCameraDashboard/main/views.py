import os
from datetime import datetime
from os import path
from pathlib import Path

from django.http import HttpResponse
from django.shortcuts import render

from .utils import download_file, zip_ze_file, timelapse, video_to_gif


def home(request):
    return render(request, template_name='main/home.html')


def download_photos(request):
    now = datetime.now().strftime('%Y-%m-%d')
    tmp_filepath = f'./main/tmp_cache_files/{now}'

    if request.method == "POST":
        plant = request.POST['download']
        dwnld_filepath = f'{tmp_filepath}/{plant}/picamera_photos'
        zip_filepath = f'{dwnld_filepath}/{plant}.zip'
        zip_filename = f'{now}_{plant}_photos.zip'

    if not path.exists(zip_filepath):
        if not path.exists(dwnld_filepath):
            os.makedirs(f'{dwnld_filepath}')
            download_file(now, plant)

        zip_ze_file(folder_to_compress=Path(dwnld_filepath), path_to_archive=Path(zip_filepath), filetype='*jpeg')
    zip_file = open(zip_filepath, 'rb')

    response = HttpResponse(zip_file, content_type='application/zip')
    response['Content-Disposition'] = f'attachment; filename={zip_filename}'
    return response


def download_timelapse(request):
    now = datetime.now().strftime('%Y-%m-%d')
    tmp_filepath = f'./main/tmp_cache_files/{now}'

    if request.method == "POST":
        plant = request.POST['download']
        dwnld_filepath = f'{tmp_filepath}/{plant}/picamera_photos'
        tmlps_path = f'{tmp_filepath}/{plant}/timelapse'
        tmlps_filepath = f'{tmlps_path}/timelapse.avi'
        zip_filepath = f'{tmlps_path}/{plant}_timelapse.zip'
        timelapse_filename = f'{now}_{plant}_timelapse.zip'

    if not path.exists(zip_filepath):
        if not path.exists(tmlps_filepath):
            if not path.exists(tmlps_path):
                os.makedirs(tmlps_path)
                if not path.exists(dwnld_filepath):
                    os.makedirs(dwnld_filepath)
                    download_file(now, plant)
            timelapse(now, plant, dwnld_filepath, tmlps_path)
        zip_ze_file(folder_to_compress=Path(tmlps_path), path_to_archive=Path(zip_filepath), filetype='*avi')
    zip_file = open(zip_filepath, 'rb')
    response = HttpResponse(zip_file, content_type='application/zip')
    response['Content-Disposition'] = f'attachment; filename={timelapse_filename}'
    return response


def video(request):
    now = datetime.now().strftime('%Y-%m-%d')
    tmp_filepath = f'./main/tmp_cache_files/{now}'
    # dwnld_filepath = f'{tmp_filepath}/picamera_photos'
    # tmlps_path = f'{tmp_filepath}/timelapse'
    # tmlps_filepath = f'{tmlps_path}/{now}timelapse.avi'
    # output_filepath = f'./media/timelapse/{now}'
    # gif_filepath = f'{output_filepath}/timelapse.gif'

    if request.method == "POST":
        plant = request.POST['view']
        dwnld_filepath = f'{tmp_filepath}/{plant}/picamera_photos'
        tmlps_path = f'{tmp_filepath}/{plant}/timelapse'
        tmlps_filepath = f'{tmlps_path}/{now}_{plant}_timelapse.avi'
        output_filepath = f'./media/timelapse/{now}/{plant}'
        gif_filepath = f'{output_filepath}/{plant}_timelapse.gif'

    if not path.exists(gif_filepath):
        if not path.exists(output_filepath):
            os.makedirs(output_filepath)
        if not path.exists(tmlps_filepath):
            if not path.exists(tmlps_path):
                os.makedirs(tmlps_path)
            if not path.exists(dwnld_filepath):
                os.makedirs(dwnld_filepath)
                download_file(now, plant)
            timelapse(now, plant, dwnld_filepath, tmlps_path)
        video_to_gif(input_filepath=tmlps_filepath, output_filepath=gif_filepath)

    context = {'filepath': f'timelapse/{now}/{plant}/{plant}_timelapse.gif'}
    return render(request, template_name='main/video.html', context=context)
