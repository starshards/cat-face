# -*- coding=utf-8 -*-
import os
import cv2
import time
from flask import Flask, request, url_for, send_from_directory

basepath = os.path.dirname(__file__)

notcatPath = basepath + "/haarcascades/haarcascade_frontalface_alt.xml"
notfaceCascade = cv2.CascadeClassifier(notcatPath)

catPath = basepath + "/haarcascades/haarcascade_frontalcatface.xml"
faceCascade = cv2.CascadeClassifier(catPath)

ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg', 'gif'])

app = Flask(__name__)
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024

html = '''
    <!DOCTYPE html>
    <meta name="viewport" content="width="device-width,initial-scale=1"/>
    <title>猫脸检测</title>
    <h1>猫脸检测</h1>
    <form method=post enctype=multipart/form-data>
         <input type=file name=file>
         <input type=submit value=upload>
    </form>
    '''

def hasMan(img, scale=(1.3, 3, (350,350))):
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    faces = notfaceCascade.detectMultiScale(
        gray,
        scaleFactor=scale[0],
        minNeighbors=scale[1],
        minSize=scale[2],
        flags=cv2.CASCADE_SCALE_IMAGE
    )
    return faces

def hasCat(img, scale=(1.3, 3, (350, 350))):
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    # 猫脸检测
    faces = faceCascade.detectMultiScale(
        gray,
        scaleFactor=scale[0],
        minNeighbors=scale[1],
        minSize=scale[2],
        flags=cv2.CASCADE_SCALE_IMAGE
    )
    return faces

def pointCats(img, faces, name):
    if faces is not ():
        for (x, y, w, h) in faces:
            cv2.rectangle(img, (x, y), (x + w, y + h), (0, 0, 255), 2)
    #       cv2.putText(img,'cat',(x,y-7), 3, 1.2, (0, 255, 0), 2, cv2.LINE_AA)
        cv2.imwrite(basepath + '/static/' + name, img)
    return img

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS


@app.route('/uploads/<filename>')
def uploaded_file(filename):
    basepath = os.path.dirname(__file__)
    return send_from_directory(basepath + '/static/',
                               filename)


@app.route('/', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        file = request.files['file']
        if file and allowed_file(file.filename):
            t = str(int(time.time()))
            filename = t+'.jpg'
            basepath = os.path.dirname(__file__)
            file.save(basepath + '/static/' + filename)
            img = cv2.imread(basepath + '/static/' + filename)
            scale = (1.05, 22, (175, 175))
            manface = hasMan(img, scale)
            filenames = 'c' + t + '.jpg'
            if manface is ():
                faces = hasCat(img, scale)
                img = pointCats(img, faces, filenames)
                if faces is():
                    file_url = url_for('uploaded_file', filename=filename)
                else:
                    file_url = url_for('uploaded_file', filename=filenames)
            else:
                file_url = url_for('uploaded_file', filename=filename)
            return html + '<br><img src=' + file_url + '>'
    return html

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)