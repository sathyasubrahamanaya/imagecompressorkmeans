from fastapi import APIRouter, Depends, UploadFile,Form
from fastapi.responses import FileResponse
from PIL import Image
import datetime
import io


import os

from app.models import User
from app.security import get_current_user
from fastapi.background import BackgroundTasks

from app.image_compressor import FastImageCompressor
import time
encrpyt_router = APIRouter()

def clean_up(folder):
    try:
        time.sleep(300)
        print("cleaning up ---------->",folder)
        for file in os.listdir(folder):
            os.remove(f"{folder}/{file}")
    except Exception as e:
        print(e)

def convert_jpg(uploaded_image_bytes,sub_name="input",save_in_path:str="tempfiles"):
    image =Image.open(io.BytesIO(uploaded_image_bytes))
    image_path_str = f"{save_in_path}/image_{sub_name}{datetime.datetime.now().timestamp()}.jpg"
    image.save(image_path_str)
    return image_path_str

@encrpyt_router.post("/compress")
async def encrpyt_images(input_image:UploadFile,target_size=Form(default=0.25),K:int=Form(default=100),max_iter:int = Form(default=4),current_user:User = Depends(get_current_user),backgroud_tasks: BackgroundTasks= BackgroundTasks() ):
    if not os.path.exists(f"userspace/{current_user.username}"):
        os.mkdir(f"userspace/{current_user.username}")
        os.mkdir(f"userspace/{current_user.username}/tempfiles")
        
    user_space_path = "userspace/{current_user.username}"
    current_folder_path = f"userspace/{current_user.username}/tempfiles"
    input_image_path =convert_jpg(await input_image.read(),save_in_path=current_folder_path)
    output_image_path = f"{current_folder_path}/output_image{datetime.datetime.now().timestamp()}.jpg"
    compressor =  FastImageCompressor(target_size,K, max_iter)
    compressor.compress(input_image_path,output_image_path)
    backgroud_tasks.add_task(clean_up,current_folder_path)
    return FileResponse(output_image_path,filename="output.png",media_type="application/image")
    
    


    



