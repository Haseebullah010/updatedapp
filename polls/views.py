from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.core.files.storage import default_storage
from django.http import HttpResponse, JsonResponse
import torch
import json
import os
from django.shortcuts import render

from django.contrib.staticfiles import finders

model = torch.hub.load('yolov5', 'yolov5s', source='local', device='cpu')

# def index(request):
#   print(request.data)
#   imgs="test1.jpg"
#   results = model(imgs)
#   # print(a)
#   # print(results.pandas().xyxy[0]["name"])
#   data = results.pandas().xyxy[0]
#   data = data.to_json(orient="split")
#   data = json.loads(data)
#   print(data)
#   return JsonResponse(data)


class ReceiveImages(APIView):
    print ("in function")
    def post(self, request, format=None):

        try:
            file = request.data.get('file')
            staticPrefix = "static"
            filename = str(file)

            filepath = 'images/' + filename
            with default_storage.open(filepath, 'wb+') as destination:
                for chunk in file.chunks():
                    destination.write(chunk)

            # getting results
            results = model(filepath)

            # for croping

            _, result_dir = results.crop(save=True)

            # converting detection result to json format
            data = results.pandas().xyxy[0].to_json(orient="records")

            # normalizing result_dir
            tmp = finders.find(result_dir)
            searched_loc = finders.searched_locations
            modified_res_loc = os.path.relpath(tmp, searched_loc[0])

            result_dir = str(result_dir.as_posix())

            data = json.loads(data)
            unique_fruits = {}
            for fruit in data:
                unique_fruits[fruit.get('name')] = []

            for fruit in unique_fruits:
                file_list = os.listdir(result_dir+'/crops/'+fruit)
                unique_fruits[fruit] = file_list

            name_confidence = []
            final_data = []
            for record in data:
                name_confidence.append({
                    "name": record.get('name'),
                    "confidence": record.get('confidence')
                })
                final_data.append({
                    "name": record.get('name'),
                    "confidence": record.get('confidence'),
                    "image_url": staticPrefix+'/' + modified_res_loc + '/crops/' + record.get('name') + '/' + unique_fruits[record.get('name')].pop(0)
                })

            resultant_data = {
                "data": final_data,
                "actual_image_url": staticPrefix + '/'+modified_res_loc+'/'+filename
            }

            return render(request,"home.html",{'context':name_confidence})

        except:

            # return JsonResponse({
            #     "data": [],
            #     "actual_image_url": ""
            # }, status=500)
            return render(request,"home.html",{'context1':"Some Error Occur"})

def home(request):

    return render(request,"home.html")