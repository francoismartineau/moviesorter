import os
import shutil               # delete movie folders
import importlib.util       # import cloudinary uploader script
import sys
import urllib.request, json
import urllib.error

from pathlib import Path
from moviesorter import movies_access
from dotenv import find_dotenv, load_dotenv
load_dotenv(find_dotenv())

uploader = None

MOVIES = ['Napoleon Dynamite', 'Harry Potter 1', 'Eraserhead', 'Toy Story']
FRAMES_DIR = os.path.join(Path(__file__).resolve().parent, 'movie_frames_container')
FRAMES_PER_MOVIE = 100
TAG = 'movie_sorter'

def import_uploader():
    cloudinary_upload_script = os.environ.get('CLOUDINARY_UPLOAD_SCRIPT')
    spec = importlib.util.spec_from_file_location("module.name", cloudinary_upload_script)
    global uploader
    uploader = importlib.util.module_from_spec(spec)
    sys.modules["module.name"] = uploader
    spec.loader.exec_module(uploader)
    uploader.authenticate_to_cloudinary()

def generate_all(upload=True):
    if upload:
        import_uploader()
    movies_access.set_frames_qty(FRAMES_PER_MOVIE)
    for movie_title in MOVIES:
        movie_frames_dir = os.path.join(FRAMES_DIR, movie_title)
        generate_movie_frames(movie_title, movie_frames_dir)
        if upload:
            upload_movie_frames(movie_title, movie_frames_dir)
    if upload:
        generate_client_assets_list()

def generate_movie_frames(movie_title, movie_frames_dir):
    movies_access.set_frames_dir(movie_frames_dir)
    movies_access.make_frames(movie_title)

def upload_movie_frames(movie_title, movie_frames_dir):
    exts = ['jpg']
    cloudinary_folder = 'moviesorter/' + movie_title
    tags = [TAG]
    print("will upload frames for:", movie_title)
    uploader.upload_files_from_folder(movie_frames_dir, exts, cloudinary_folder, tags)

def generate_client_assets_list():
    url = uploader.create_client_assets_list(TAG)
    return url

def clear_local():
    for f in os.listdir(FRAMES_DIR):
        path = os.path.join(FRAMES_DIR, f)
        shutil.rmtree(path)

def clear_cloud():
    if uploader == None:
        import_uploader()
    try:
        with urllib.request.urlopen(os.environ.get('CLOUD_LIST_URL')) as url:
            print('ok')
            data = json.loads(url.read().decode())
            for image in data['resources']:
                public_id = image['public_id']
                uploader.delete_file(public_id)
    except urllib.error.HTTPError as e:
        print("Can't clear cloud, maybe the assests list doesn't exist:", e)

if __name__ == '__main__':
    clear_local()
    clear_cloud()
    generate_all(upload=True)