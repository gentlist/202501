from flask import Flask, request
import os

app = Flask(__name__)

# 定义上传文件的保存目录
UPLOAD_FOLDER = 'uploads'
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

# 配置允许上传的文件类型
ALLOWED_EXTENSIONS = {'mp3', 'wav', 'ogg'}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/upload-audio', methods=['GET', 'POST'])
def upload_audio():
    if request.method == 'GET':
        return 'This endpoint is used for uploading audio files via POST method.'
    if 'audio' not in request.files:
        return 'No audio part in the request', 400
    file = request.files['audio']
    if file.filename == '':
        return 'No selected file', 400
    if file and allowed_file(file.filename):
        file.save(os.path.join(UPLOAD_FOLDER, file.filename))
        return 'File uploaded successfully', 200
    return 'Invalid file type', 400

if __name__ == '__main__':
    app.run(debug=False)