import subprocess
import os
import random
import urllib.parse
import urllib.request, json
from pathlib import Path

MOVIES_DIR = r"D:\FILMS"
base_dir = Path(__file__).resolve().parent.parent
FRAMES_DIR = os.path.join(base_dir, 'static', 'moviesorter','frames')
VID_EXTS = [".avi", ".mkv", ".mp4"]
IMG_W = 500
FRAME_QTY = 3

CLOUD_LIST_URL = "https://res.cloudinary.com/frizambisme/image/list/movie_sorter.json"
CLOUD_IMG_URL = "https://res.cloudinary.com/frizambisme/image/upload/v{version}/{public_id}.{ext}"

# -------------------------------
def set_frames_dir(path):
    global FRAMES_DIR
    FRAMES_DIR = path

def set_frames_qty(qty):
    global FRAME_QTY
    FRAME_QTY = qty

# -------------------------------
def choose_a_movie_title():
    movie_titles = get_movie_titles()
    return random.choice(movie_titles)

# -------------------------------
def get_movie_titles(cloud=False):
    if cloud:
        cloud_list = get_cloud_list()
        movie_titles = get_cloud_movie_titles(cloud_list)
    else:
        movie_titles = get_local_movie_titles()
    return movie_titles

def get_local_movie_titles():
    movie_titles = []
    for movie_title in os.listdir(MOVIES_DIR):
        d = os.path.join(MOVIES_DIR, movie_title)
        if os.path.isdir(d) and contains_video_file(d):
             movie_titles.append(movie_title)
    return movie_titles

def get_dir_video_file(d):
    video_path = ''
    for f in os.listdir(d):
        for ext in VID_EXTS:
            if f.endswith(ext):
                video_path = os.path.join(d, f)
                return video_path
contains_video_file = get_dir_video_file

# -------------------------------
def get_movie_path(movie_title):
    movie_path = None
    for t in os.listdir(MOVIES_DIR):
        if t == movie_title:
            movie_dir = os.path.join(MOVIES_DIR, movie_title)
            movie_path = os.path.join(movie_dir, get_dir_video_file(movie_dir))
            break
    return movie_path


# -------------------------------
def make_frames(movie_title):
    clear_frames()
    movie_path = get_movie_path(movie_title)
    duration = get_duration(movie_path)
    frame_times = []
    for _ in range(FRAME_QTY):
        time = get_random_time(duration)
        frame_times.append(time)
        make_frame(time, movie_path)
    return frame_times

def get_duration(movie_path):
    args = "ffprobe -v error -show_entries format=duration -of default=noprint_wrappers=1:nokey=1".split()
    args.append('{}'.format(movie_path))
    duration = run_command(args)
    duration = duration.split(".")[0]
    return duration

def get_frames_qty(qty):
    if qty == "":
        global FRAME_QTY
        qty = FRAME_QTY
    return qty

def get_random_time(duration):
    return random.randint(0, int(duration))

def make_frame(time, movie_path):
    def format_time(time):
        h = time // (60*60)
        time -= h * (60*60)
        m = time // 60
        time -= m * 60
        s = time
        formated_time = "{:02d}:{:02d}:{:02d}".format(h, m, s)
        return formated_time
    os.makedirs(FRAMES_DIR, exist_ok=True)
    image_path = os.path.join(FRAMES_DIR, "{:05d}.jpg".format(time))
    formated_time = format_time(time)
    resize = "-vf scale={}:-1".format(IMG_W)
    args = "ffmpeg -ss {0} -i \"{1}\" -frames:v 1 {3} -q:v 2  \"{2}\"".format(formated_time, movie_path, image_path, resize)
    return run_command(args)

# -------------------------------
def run_command(args):
    output = subprocess.run(args, capture_output=True, shell=True)
    return output.stdout.decode("utf-8")

def clear_frames():
    if os.path.isdir(FRAMES_DIR):
        for f in os.listdir(FRAMES_DIR):
            if f.endswith('.jpg'):
                f = os.path.join(FRAMES_DIR, f)
                os.remove(f)


# -------------------------------
def get_cloud_list():
    cloud_list = {}
    with urllib.request.urlopen(CLOUD_LIST_URL) as url:
        data = json.loads(url.read().decode())
        for image in data['resources']:
            public_id = image['public_id']
            version = image['version']
            ext = image['format']
            movie_title = get_movie_title_from_public_id(public_id)
            if movie_title not in cloud_list:
                cloud_list[movie_title] = []
            image_url = get_image_url(version, public_id, ext)
            cloud_list[movie_title].append(image_url)
    return cloud_list

def get_cloud_movie_titles(cloud_list):
    return list(cloud_list.keys())

def get_movie_title_from_public_id(public_id):
    url_movie_title = public_id.split('/')[1]
    movie_title = urllib.parse.unquote(url_movie_title)
    return movie_title

def get_image_url(version, public_id, ext):
    public_id = urllib.parse.quote(public_id)
    return CLOUD_IMG_URL.format(version=version, public_id=public_id, ext=ext)

def get_cloud_frames(cloud_list, movie_title):
    frames = []
    random.shuffle(cloud_list[movie_title])
    for _ in range(FRAME_QTY):
        url = cloud_list[movie_title].pop()
        time = url.split('/')[-1].split('.')[0]
        frames.append({'url': url, 'time': time})
    return frames


# -------------------------------
if __name__ == "__main__":
    movie_title = choose_a_movie_title()
    make_frames(movie_title)

# https://res.cloudinary.com/frizambisme/image/upload/v1659359359/moviesorter/Natural%2520Born%2520Killers/2543.jpg
# https://res.cloudinary.com/frizambisme/image/upload/v1659359359/moviesorter/Natural%20Born%20Killers/2543.jpg