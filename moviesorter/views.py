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
        success = all(int(frame_times[i]) <= int(frame_times[i+1]) for i in range(len(frame_times) - 1))
        result["success"] = success
        
        def affect_score(request, success, frames_qty):
            score = int(request.POST.get('score', 0))
            if success:
                score += frames_qty*10
            else:
                score -= 5
            return score
        result["score"] = affect_score(request, success, len(frame_times))
        def update_best_score(request, score):
            best_scores = request.session.get('best_scores', {})
            movie_title = request.POST.get('movie_title')
            best_score = best_scores.get(movie_title, 0)
            if score > best_score:
                best_score = score
                best_scores[movie_title] = best_score
                request.session['best_scores'] = best_scores
                request.session.modified = True
            return best_score
        result["bestScore"] = update_best_score(request, result["score"])

        result["text"] = { True: "Good job!",
            False: "Wrong order."}[success]

    return JsonResponse(result)

def request_frames(request):
    result = {'frames': []}
    if request.method == 'POST':
        movie_title = request.POST.get('movie-title')
        except_cloudinary_ids = request.POST.getlist('except-cloudinary-ids[]')
        qty = 2
        result['frames'] = get_cloud_frames(movie_title, qty, except_cloudinary_ids)
    return JsonResponse(result)

def request_best_score(request):
    best_scores = request.session.get('best_scores', {})
    movie_title = request.POST.get('movie_title')
    best_score = best_scores.get(movie_title, 0)
    result = {'bestScore': best_score}
    return JsonResponse(result)