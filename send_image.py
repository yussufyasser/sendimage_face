import face_recognition
import cv2
import numpy as np
from google.cloud import firestore
from google.oauth2 import service_account

from flask import Flask, request, jsonify
import base64
from io import BytesIO
from PIL import Image
from flask_cors import CORS

credentials = service_account.Credentials.from_service_account_file(
    'face-1731f-firebase-adminsdk-0gs2t-650494e905.json'
)
db = firestore.Client(credentials=credentials)
collection_ref = db.collection('faces')

def encode_image(img,name):
    try:
        rgb_image=cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        face_encodings = face_recognition.face_encodings(rgb_image, face_recognition.face_locations(rgb_image) )[0]
        s_face_encodings=np.array2string(face_encodings)[1:-1]

        doc_data = {
            'name': name,
            'face': s_face_encodings
        }

        collection_ref.add(doc_data)
        return True
        
    except IndexError:
        return False

app = Flask(__name__)
CORS(app)  

@app.route('/send_image', methods=['POST'])
def send_image_endpoint():

    data = request.get_json()
    image_data = data['image']
    name=data['name']
    image_bytes = base64.b64decode(image_data)
    image =np.array(  Image.open(BytesIO(image_bytes)) )

    mes=encode_image(image,name)
    s=''
    if mes:
        s='1'
    else:
        s='0'


    return jsonify({'message': s}), 200

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=9000, use_reloader=False)
