ver1x = 0
ver1y = 0
ver2x = 0
ver2y = 0
import re
import os
import cv2


def detect_faces(path):
    """Detects faces in an image."""
    from google.cloud import vision
    import io
    client = vision.ImageAnnotatorClient()
    
    with io.open(path, 'rb') as image_file:
        content = image_file.read()

    image = vision.types.Image(content=content)
   

    response = client.face_detection(image=image)
    faces = response.face_annotations

    # Names of likelihood from google.cloud.vision.enums
    likelihood_name = ('UNKNOWN', 'VERY_UNLIKELY', 'UNLIKELY', 'POSSIBLE',
                           'LIKELY', 'VERY_LIKELY')
    #print('Faces:')
   
    for face in faces:
     #   print('anger: {}'.format(likelihood_name[face.anger_likelihood]))
     #   print('joy: {}'.format(likelihood_name[face.joy_likelihood]))
     #   print('surprise: {}'.format(likelihood_name[face.surprise_likelihood]))
       # for face.landmarks_key in face.landmarks:
        #    print(face.landmarks_key)
        print(face.landmarks)
        print(face.bounding_poly)
        for i, vertex in enumerate(face.bounding_poly.vertices,0):
            if i == 0 :
                global ver1x
                global ver1y
                ver1x = vertex.x #左上のx座標
                ver1y = vertex.y #左上のy座標
            
            if i == 2 :
                global ver2x
                global ver2y
                ver2x = vertex.x #右下のx座標
                ver2y = vertex.y #右下のy座標
            
        ver1y = ver1y+(ver2y-ver1y)/1.7
        vertices = (['({},{})'.format(vertex.x, vertex.y)
                    for vertex in face.bounding_poly.vertices])
        
       # print('face bounds: {}'.format(','.join(vertices)))
        
    if response.error.message:
        raise Exception(
            '{}\nFor more info on error messages, check: '
            'https://cloud.google.com/apis/design/errors'.format(
                response.error.message))
    return (ver1x,ver1y),(ver2x,ver2y)

def main():
    data_dir_path = u"./data_dir"
    data_save_path= u"./data_save"
    file_list = os.listdir(r'./data_dir/')
    file_save_list = os.listdir(r'./data_save/')
    
    for file_name in file_list:
        if file_name != '.DS_Store':
            root, ext = os.path.splitext(file_name)
            if ext == u'.png' or u'.jpeg' or u'.jpg':
                abs_name = data_dir_path + '/' + file_name
                image = cv2.imread(abs_name)
                #以下各画像に対する処理
                from PIL import Image
                a,b= detect_faces(abs_name)
                img = Image.open(abs_name)
                from PIL import ImageDraw
                d = ImageDraw.Draw(img)
                d.rectangle([a,b], fill='white', outline='white',  width=1)
                abs_name_end = data_save_path + '/' + 'end_' + file_name
                img.save(abs_name_end)
                img.show()

main()
