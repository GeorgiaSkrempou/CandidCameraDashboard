import glob
import os
import re
from pathlib import Path
from zipfile import ZipFile

import cv2
import imageio
from boto3 import session
from dotenv import load_dotenv

load_dotenv()

ACCESS_ID = os.environ["ACCESS_ID"]
SECRET_KEY = os.environ["SECRET_KEY"]
SPACES_URL = "https://ams3.digitaloceanspaces.com"


def download_file(now, plant):
    # initiate session with spaces
    spaces_session = session.Session()
    client = spaces_session.client("s3",
                                   region_name="ams3",
                                   endpoint_url=SPACES_URL,
                                   aws_access_key_id=ACCESS_ID,
                                   aws_secret_access_key=SECRET_KEY)

    my_photos = client.list_objects(Bucket='mononokeros')['Contents']

    for photo in my_photos:
        if plant == "proud_boy":
            if re.findall(r"image(.*)_", photo['Key']):
                client.download_file('mononokeros', f"{photo['Key']}",
                                     f"./main/tmp_cache_files/{now}/proud_boy/{photo['Key']}")
        elif plant == "resurrected_boy":
            if re.findall(r"resurrected_succulent(.*)_", photo['Key']):
                client.download_file('mononokeros', f"{photo['Key']}",
                                     f"./main/tmp_cache_files/{now}/resurrected_boy/{photo['Key']}")


def zip_ze_file(folder_to_compress, path_to_archive, filetype):
    with ZipFile(path_to_archive, 'w') as new_zip:
        for file in folder_to_compress.rglob(filetype):
            relative_path = file.relative_to(folder_to_compress)
            new_zip.write(filename=file, arcname=relative_path)


def timelapse(now, plant, folder_to_images, folder_to_timelapse):
    img_array = []

    for filename in sorted(glob.glob(f'{folder_to_images}/*jpeg')):
        img = cv2.imread(filename)
        height, width, layers = img.shape
        size = (width, height)
        img_array.append(img)

    out = cv2.VideoWriter(f'{folder_to_timelapse}/{now}_{plant}_timelapse.avi', cv2.VideoWriter_fourcc(*'DIVX'), 7, size)

    for i in range(len(img_array)):
        out.write(img_array[i])

    out.release()


def video_to_gif(input_filepath, output_filepath):
    reader = imageio.get_reader(input_filepath)
    fps = reader.get_meta_data()['fps']
    writer = imageio.get_writer(output_filepath, fps=fps)

    for i, im in enumerate(reader):
        writer.append_data(im)

    writer.close()
