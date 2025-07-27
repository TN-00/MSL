from django.urls import path, include, re_path
from django.conf import settings
from django.conf.urls.static import static 
from . import views

app_name = 'sign'

urlpatterns = [
    # path('', views.index, name='index'),
    # # 127.0.0.1/sign/
    # path(r"^(?P<label_id>[0-9]+)/$", views.detail, name='detail'),
    # # 127.0.0.1/polls/1
    # path(r"^(?P<label_id>[0-9]+)/results$", views.results, name='results'),
    # # 127.0.0.1/polls/1/results
    # path(r"^(?P<label_id>[0-9]+)/image$", views.image, name='image'), 
    # # dictionary to pass the label_id to the image view
    # path('addImg/', views.addImg, name='addImg'),
    # # dicitonaty.html
    # path('dictionary/<int:label_id>/', views.dictionary, name='dictionary'),

    path('', views.index, name='index'),
    path('<int:label_id>/', views.detail, name='detail'),
    path('<int:label_id>/results/', views.results, name='results'),
    path('<int:label_id>/image/', views.image, name='image'),
    path('<int:label_id>/dictionary/', views.dictionary, name='dictionary'),
    path('addImg/', views.addImg, name='addImg'),
    # webcam upload
    path('webcam/', views.webcam_page, name='webcam'),
    path('webcam/save/', views.webcam_save, name='webcam_save'),

  
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT) # This line serves media files during development