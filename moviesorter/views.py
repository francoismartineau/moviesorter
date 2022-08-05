import random
import os
import uuid
from django.shortcuts import render
from django.http import FileResponse, JsonResponse

from .movies_access import get_cloud_list, get_cloud_movie_titles, get_cloud_frames

def index(request):
    context = {}
    cloud_list = get_cloud_list()
    context['movie_titles'] = get_cloud_movie_titles(cloud_list)
    if request.method == 'GET' and 'movie_title' in request.GET:
        context['movie_title'] = request.GET['movie_title']
        context['frames'] = get_cloud_frames(cloud_list, context['movie_title'])
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