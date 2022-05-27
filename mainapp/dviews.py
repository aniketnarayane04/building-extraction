from django.shortcuts import render
from mainapp.forms import buildingForm
from mainapp.models import building
# Create your views here.
import os
from django.conf import settings
import base64
from io import BytesIO
from django.core.files.storage import FileSystemStorage
from PIL import Image
import numpy as np
import matplotlib.pyplot as plt
import tensorflow as tf
from tensorflow import Graph

from tensorflow import keras
model = keras.models.load_model('./models/indian_unet_membrane.hdf5')

def index(request):
    return render(request, 'index.html')

def input(request):
    if request.method == 'POST':  
        form = buildingForm(request.POST, request.FILES)  
        if form.is_valid():  
            form.save()  
  
            # Getting the current instance object to display in the template  
            img_object = form.instance  
            image = building.objects.all().last()

            return render(request, 'input.html', {'form': form, 'img_obj': img_object, 'image':image})  
    else:  
        form = buildingForm() 
  
    return render(request, 'input.html', {'form': form})  

def output(request):
    if request.method == 'POST':  
        form = buildingForm(request.POST, request.FILES)  
        if form.is_valid():  
            form.save()  
  
            # Getting the current instance object to display in the template  
            img_object = form.instance  
            image = building.objects.all().last()
            image_name = image.ip_image.url
            image_name = image_name.split("/")
            image_name = image_name[-1]
            test_path = 'C:\\Users\\Aniket\\Desktop\\project website\\buildingx\\media\\'+image_name
            print(test_path)       
            # print(test_path)
            # base_dir =settings.MEDIA_ROOT    
            # test_path = os.path.join(base_dir, test_path)
            # test_path = r"C:\\Users\\Aniket\\Desktop\\project website\\buildingx\\media\\102.png"
            test_img = tf.keras.preprocessing.image.load_img(test_path,target_size=(256,256))
            x = tf.keras.preprocessing.image.img_to_array(test_img)

            x = np.expand_dims(x,axis=0)
            
            pred = model.predict(x)
            
            data_img = (pred.squeeze()*255).astype(np.uint8)
            img = Image.fromarray(data_img, mode='L')
            # img.show()
            filename = 'media\\output\\'+image_name
            img.save(filename)

            # with open(img, "rb") as image_file:
            #     base64string = base64.b64encode(image_file.read())
            # buffered = BytesIO()
            # img.save(buffered, format="JPEG")
            # img_str = base64.b64encode(buffered.getvalue())

            context = {'op_image':image_name}
            return render(request, 'output.html', context)
    else:  
        form = buildingForm() 
    return render(request, 'output.html')
    