import glob
import os
from zipfile import ZipFile

from boto3 import session
from dotenv import load_dotenv

load_dotenv()  # a function that reads the .env file and stores those variables in os.env and makes them environment variables

ACCESS_ID = os.environ["ACCESS_ID"]
SECRET_KEY = os.environ["SECRET_KEY"]
SPACES_URL = "https://ams3.digitaloceanspaces.com"


def download_file():
    # initiate session with spaces
    spaces_session = session.Session()
    client = spaces_session.client("s3",
                                   region_name="ams3",
                                   endpoint_url=SPACES_URL,
                                   aws_access_key_id=ACCESS_ID,
                                   aws_secret_access_key=SECRET_KEY)

    my_photos = client.list_objects(Bucket='mononokeros')['Contents']

    for photo in my_photos:
        client.download_file('mononokeros', f"{photo['Key']}", f"tmp_cache_files/{photo['Key']}")


def main():
    directory = 'tmp_cache_files/picamera_photos'
    with ZipFile('tmp_cache_files/picamera_photos.zip', 'w') as new_zip:
        for file in glob.glob(f'{directory}/*jpeg'):
            new_zip.write(filename=file)


if __name__ == '__main__':
    main()

# download_file()
