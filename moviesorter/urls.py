from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('local-frame', views.local_frame, name='local_frame'),
    path('submit-order', views.submit_order, name='submit_order'),
    path('request-frames', views.request_frames, name='request_frames'),
]