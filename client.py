import requests

audio_file_path = 'output.wav'
url = 'http://127.0.0.1:5000/upload-audio'

try:
    with open(audio_file_path, 'rb') as audio_file:
        files = {'audio': audio_file}
        response = requests.post(url, files=files)
        if response.status_code == 200:
            print("上传成功:", response.text)
        else:
            print(f"上传失败，状态码: {response.status_code}, 错误信息: {response.text}")
except FileNotFoundError:
    print(f"File {audio_file_path} not found.")
except requests.exceptions.RequestException as e:
    print(f"请求发生异常: {e}")