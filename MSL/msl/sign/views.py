from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse
from .models import Signimg
from .models import Label
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse 
from django.core.files.base import ContentFile
import cv2, numpy as np
import mediapipe as mp
from django.core.paginator import Paginator as paginator
from django.core.files.base import ContentFile 
import base64, re
from .models import Label, Signimg, Capture
from PIL import Image
import matplotlib.pyplot as plt
import io
from .hand_recognition import detect_hand_gesture

# Create your views here.
# HTTP response - add some basic text in the website

def index(request):
    # getting data from the database
    latest_labels = Label.objects.order_by('pub_date')
    # output = ", ".join(l.label_txt for l in latest_labels)
    context = {
        # creating a library
        'latest_labels': latest_labels
    }
    # passing the value of latest labels
    return render(request, 'sign/index.html', context)

# detail view
# def detail(request, label_id):
    # label = get_object_or_404(Label, pk = label_id)
#     signimg_list = label.signimg_set.all().order_by('-uploaded_at')
    # paginator = Paginator(signimg_list, 3)  # Show 5 images per page

    # pg_num = request.GET.get('page')
    # page_obj = paginator.get_page(pg_num)
    # label = Label.objects.all() #Fetch all the labels
    # return HttpResponse("This is the detail view of the label: %s" % label_id)
    # return render(request, 'sign/detail.html', {'label':label})
# , 'page_obj': page_obj 

def detail(request, label_id):
    return HttpResponse("This is the detail view of the label: %s" % label_id)


# def detail(request):
#     label = Label.objects.all() #Fetch all the labels
#     # return HttpResponse("This is the detail view of the label: %s" % label_id)
#     return render(request, 'sign/detail.html', {'label':label})


# result view
def results(request, label_id):
    return HttpResponse("this is the result of the result of label: %s" % label_id)

# image view
def image(request, label_id):
    return HttpResponse("signing image %s" % label_id)

def addImg(request):
    return render()

# dictionary view
def dictionary(request, label_id):
    label = get_object_or_404(Label, pk=label_id)
    signimg_list = label.signimg_set.all().order_by('-uploaded_at')
    return render(request, 'sign/dictionary.html', {'label': label, 'signimg_list': signimg_list})


def gallery(request):
    items = Signimg.objects.order_by('-uploaded_at')
    return render(request, 'gallery.html', {'items': items})


# to upload the captured image from webcam into the database
@csrf_exempt
def upload_image(request):
    if request.method == 'POST':
        image_data = request.POST.get('image')
        label_id = request.POST.get('label_id')
        
        if image_data and label_id:
            # Decode the base64 image data
            format, imgstr = image_data.split(';base64,')
            ext = format.split('/')[-1]
            image = ContentFile(base64.b64decode(imgstr), name=f'temp_image.{ext}')
            
            # Get the label object
            label = get_object_or_404(Label, pk=label_id)
            
            # Create a new Signimg instance
            signimg_instance = Signimg(signimg_img=image, label=label)
            signimg_instance.save()
            
            return JsonResponse({'status': 'success', 'message': 'Image uploaded successfully!'})
        else:
            return JsonResponse({'status': 'error', 'message': 'Invalid data provided.'})
    
    return JsonResponse({'status': 'error', 'message': 'Invalid request method.'})


# to capture the video from the webcam and upload it to the database
@csrf_exempt
def upload_video(request):
    if request.method == 'POST':
        video_data = request.FILES.get('video')
        label_id = request.POST.get('label_id')
        
        if video_data and label_id:
            # Get the label object
            label = get_object_or_404(Label, pk=label_id)
            
            # Create a new Signimg instance
            signimg_instance = Signimg(video=video_data, label=label)
            signimg_instance.save()
            
            return JsonResponse({'status': 'success', 'message': 'Video uploaded successfully!'})
        else:
            return JsonResponse({'status': 'error', 'message': 'Invalid data provided.'})
    
    return JsonResponse({'status': 'error', 'message': 'Invalid request method.'})


@csrf_exempt
def webcam_save(request):
    if request.method == 'POST':
        import json
        body = json.loads(request.body)
        data = body.get('data', '')
        header, b64 = data.split(',', 1)
        mime = header.split(';')[0]
        ext = mime.split('/')[1]  # 'png' or 'webm'
        file_data = base64.b64decode(b64)
        cap = Capture()
        if ext in ('png', 'jpeg', 'jpg'):
            cap.photo.save(f'cap.{ext}', ContentFile(file_data))
        else:
            cap.video.save(f'cap.{ext}', ContentFile(file_data))
        cap.save()
        return JsonResponse({'id': cap.id})
    return JsonResponse({'error': 'invalid'} , status=400)


def webcam_page(request):
    return render(request, 'webcam.html')


# show signimg
def show_signimg(request):
    signimg_list = Signimg.objects.all().order_by('-uploaded_at')
    paginator = paginator(signimg_list, 10)  # Show 10 images per page
    page_num = request.GET.get('page')
    page_obj = paginator.get_page(page_num)
    
    return render(request, 'sign/show_signimg.html', {'page_obj': page_obj})

# to display text to images
def check_letter(request):
    text_input = request.POST.get('text_input', '').strip().lower()
   
    images_list = []

    # Create a figure and axis
    for char in text_input:
        signimg = Signimg.objects.filter(label__label_txt=char).first()
        if signimg:
            # signimg.signimg_img is the image field in Signimg model
            img = signimg.signimg_img
            if img:
                try:
                    # Convert the image to a format suitable for display
                    image = Image.open(img)
                    images_list.append((char, image))
                except Exception as e:
                    print(f"Error processing image for character '{char}': {e}")
        else:
            print(f"No image found for character '{char}'")
        
        

        signimg = Signimg.objects.filter(label__label_txt=char).first()
        # If the signimg exists and has an image, process it
        if signimg and signimg.signimg_img:
            try:
                # Convert the image to a format suitable for display
                image = Image.open(signimg.signimg_img)
                images_list.append((char, image))
                message = f"Image for character '{char}' processed successfully."
            
            except Exception as e:
                print(f"Error processing image for character '{char}': {e}")

    # Create a figure to display the images
    if images_list:
        fig, axes = plt.subplots(1, len(images_list), figsize=(15, 5))
        if len(images_list) == 1:
            axes = [axes]
        
        for ax, (char, img) in zip(axes, images_list):
            ax.imshow(img)
            ax.set_title(char)
            ax.axis('off')
            
        plt.suptitle("Text to Images", fontsize=16)
        plt.tight_layout()
        plt.show()
    
    if not text_input:
        return HttpResponse("No text input provided.")

    return HttpResponse("Images displayed successfully.")

@csrf_exempt
def detect(request):
    data = json.loads(request.body)
    image_data = data['image'].split(',')[1]
    img_bytes = base64.b64decode(image_data)
    img = Image.open(io.BytesIO(img_bytes))
    img_np = cv2.cvtColor(np.array(img), cv2.COLOR_RGB2BGR)

    gesture = detect_hand_gesture(img_np)
    return JsonResponse({'gesture': gesture})
