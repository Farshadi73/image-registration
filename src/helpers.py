import os
# import sys
import time
import SimpleITK as sitk
from sewar.full_ref import mse

def read_images(path):
    
    images = {};
    
    for filename in os.listdir(path):

        name, ext = os.path.splitext(filename);
               
        split = name.split('_')
        
        img = os.path.join(path, filename)
        
        if img is not None:
            
            prefix  = split[0]
            postfix = split[1]
            
            
            if not prefix in images:
                
                images[prefix] = {}
            
            
            images[prefix][postfix] = img
    
    return images;
    

def process_items(images, start, end):
    
    result = {}
    
    for res in range(start, end+1):

        for key in images:

            image = images[key]
            item  = process_item(image["1"], image["2"], res)
            
            print(item)
            
            result[key] = item
    return result
    
    
def process_item(image1, image2, res):
           
    fixed  = sitk.ReadImage(image1)
    moving = sitk.ReadImage(image2)
        
    parameters = sitk.GetDefaultParameterMap('translation')
    parameters['NumberOfResolutions'] = [str(res)] 
    
    start = time.time()

    imageFilter = sitk.ElastixImageFilter()
    imageFilter.SetFixedImage(fixed)
    imageFilter.SetMovingImage(moving)
    imageFilter.SetParameterMap(parameters)
    imageFilter.Execute()
    
    end = time.time()
    
    result = elastixImageFilter.GetResultImage()
    
    return {"cost": end - start, "sim": 0}

