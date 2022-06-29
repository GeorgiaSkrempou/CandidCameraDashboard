import glob
import os
from pathlib import Path
from zipfile import ZipFile
import imageio

import cv2
from boto3 import session
from dotenv import load_dotenv

load_dotenv()

ACCESS_ID = os.environ["ACCESS_ID"]
SECRET_KEY = os.environ["SECRET_KEY"]
SPACES_URL = "https://ams3.digitaloceanspaces.com"


def download_file(now):
    # initiate session with spaces
    spaces_session = session.Session()
    client = spaces_session.client("s3",
                                   region_name="ams3",
                                   endpoint_url=SPACES_URL,
                                   aws_access_key_id=ACCESS_ID,
                                   aws_secret_access_key=SECRET_KEY)

    my_photos = client.list_objects(Bucket='mononokeros')['Contents']

    for photo in my_photos:
        client.download_file('mononokeros', f"{photo['Key']}",
                             f"./main/tmp_cache_files/{now}/{photo['Key']}")


def zip_ze_file(folder_to_compress, path_to_archive, filetype):
    with ZipFile(path_to_archive, 'w') as new_zip:
        for file in folder_to_compress.rglob(filetype):
            relative_path = file.relative_to(folder_to_compress)
            new_zip.write(filename=file, arcname=relative_path)


def timelapse(now):
    img_array = []

    folder_to_images = Path(f'./main/tmp_cache_files/{now}/picamera_photos/')
    folder_to_timelapse = Path(f'./main/tmp_cache_files/{now}/timelapse')

    for filename in sorted(glob.glob(f'{folder_to_images}/*jpeg')):
        img = cv2.imread(filename)
        height, width, layers = img.shape
        size = (width, height)
        img_array.append(img)

    out = cv2.VideoWriter(f'{folder_to_timelapse}/{now}timelapse.avi', cv2.VideoWriter_fourcc(*'DIVX'), 7, size)

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
