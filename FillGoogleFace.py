ver1x = 0
ver1y = 0
ver2x = 0
ver2y = 0
import re

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
    print('Faces:')
        
    for face in faces:
        print('anger: {}'.format(likelihood_name[face.anger_likelihood]))
        print('joy: {}'.format(likelihood_name[face.joy_likelihood]))
        print('surprise: {}'.format(likelihood_name[face.surprise_likelihood]))
        
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
            
        ver1y = ver1y+(ver2y-ver1y)/2
        print(ver1x)
        print(ver1y)
        print(ver2x)
        print(ver2y)
        vertices = (['({},{})'.format(vertex.x, vertex.y)
                    for vertex in face.bounding_poly.vertices])
        
        print('face bounds: {}'.format(','.join(vertices)))
        
    if response.error.message:
        raise Exception(
            '{}\nFor more info on error messages, check: '
            'https://cloud.google.com/apis/design/errors'.format(
                response.error.message))
    return [ver1x,ver1y,ver2x,ver2y]

from PIL import Image
a = detect_faces("Face1.jpg")
img = Image.open("Face1.jpg")
#img_rs = img.resize((100, 200))
from PIL import ImageDraw
d = ImageDraw.Draw(img)
d.rectangle([(ver1x,ver1y),(ver2x,ver2y)], fill='white', outline='white',  width=6)
img.save('Face1_Mask.png')
img.show()
