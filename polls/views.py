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
            file = request.data.get('fileup')
            staticPrefix = "static"
            filename = str(file)
            print ("filename",filename)

            filepath = 'images/' + filename
            with default_storage.open(filepath, 'wb+') as destination:
                for chunk in file.chunks():
                    # print ("chunk",chunk)
                    destination.write(chunk)
                    print ("desdestination",destination )

            # getting results
            results = model(filepath)
            print ("results",results)
            # for croping

            _, result_dir = results.crop(save=True)

            # converting detection result to json format
            data = results.pandas().xyxy[0].to_json(orient="records")
            print ("data",data)

            # normalizing result_dir
            tmp = finders.find(result_dir)
            print ("tmp",tmp)

            searched_loc = finders.searched_locations
            print ("searched_loc",searched_loc)

            modified_res_loc = os.path.relpath(tmp, searched_loc[0])
            print ("modified_res_loc",modified_res_loc)

            result_dir = str(result_dir.as_posix())
            print ("result_dir",result_dir)


            data = json.loads(data)
            print ("data",data)

            unique_fruits = {}
            for fruit in data:
                unique_fruits[fruit.get('name')] = []
                print ("unique_fruits",unique_fruits)


            for fruit in unique_fruits:
                file_list = os.listdir(result_dir+'/crops/'+fruit)
                unique_fruits[fruit] = file_list
                print ("file_list",file_list)


            name_confidence = []
            final_data = []
            i  = 0
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
                i = i + 1
                if i > 4:
                    break

            resultant_data = {
                "data": final_data,
                "actual_image_url": staticPrefix + '/'+modified_res_loc+'/'+filename
            }

            return render(request,"home.html",{'context':final_data})

        except:

            # return JsonResponse({
            #     "data": [],
            #     "actual_image_url": ""
            # }, status=500)
            return render(request,"home.html",{'context1':"Some Error Occur"})

def home(request):

    return render(request,"home.html")