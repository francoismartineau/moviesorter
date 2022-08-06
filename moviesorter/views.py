import random
import os
import uuid
from django.shortcuts import render
from django.http import FileResponse, JsonResponse

from .movies_access import get_cloud_list, get_cloud_movie_titles, get_cloud_frames

def index(request):
    context = {}
    context['movie_titles'] = get_cloud_movie_titles()
    if request.method == 'GET' and 'movie_title' in request.GET:
        context['movie_title'] = request.GET['movie_title']
        #context['frames'] = get_cloud_frames(context['movie_title'])
    #else:
        #context['nth_selected'] = None #0 # random.randint(0, len(context['movie_titles'])-1)
    response = render(request, 'index.html', context)
    return response

def local_frame(request):
    time = request.GET['time']
    dir = os.path.join('static', 'moviesorter', 'frames', request.session['session_id'])
    path = os.path.join(dir, time+'.jpg')
    file = open(path, 'rb')
    return FileResponse(file)

def submit_order(request):
    result = {}
    if request.method == 'POST' and 'frame_times[]' in request.POST:
        frame_times = request.POST.getlist('frame_times[]')
        sorted = all(int(frame_times[i]) <= int(frame_times[i+1]) for i in range(len(frame_times) - 1))
        if sorted:
            result["success"] = True
            result["text"] = "Good job!"
        else:
            result["success"] = False
            result["text"] = "Wrong order."
    return JsonResponse(result)

def request_frames(request):
    result = {'frames': []}
    if request.method == 'POST':
        movie_title = request.POST.get('movie-title')
        except_cloudinary_ids = request.POST.getlist('except-cloudinary-ids[]')
        """init_qty = 3
        is_init = len(except_cloudinary_ids) == 0
        if is_init:
            qty = init_qty
        else:
            qty = 2 #len(except_cloudinary_ids) - init_qty + 1"""
        qty = 2
        result['frames'] = get_cloud_frames(movie_title, qty, except_cloudinary_ids)
    return JsonResponse(result)