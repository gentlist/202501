import pyaudio
import wave
import keyboard
import threading

# 音频录制参数
CHUNK = 1024
FORMAT = pyaudio.paInt16
CHANNELS = 1
RATE = 44100
WAVE_OUTPUT_FILENAME = "output.wav"

# 初始化 PyAudio
p = pyaudio.PyAudio()

frames = []
recording = threading.Event()
stream = None


def on_space_press(event):
    global stream
    if event.name == 'space':
        if not recording.is_set():
            # 开始录制
            print("* 开始录制")
            stream = p.open(format=FORMAT,
                            channels=CHANNELS,
                            rate=RATE,
                            input=True,
                            frames_per_buffer=CHUNK)
            recording.set()
        else:
            # 停止录制
            print("* 录制结束")
            recording.clear()
            try:
                if stream.is_active():
                    stream.stop_stream()
                stream.close()
            except AttributeError:
                pass


# 监听空格键事件
keyboard.on_press(on_space_press)

print("按空格键开始录制，再次按空格键停止录制。")

while True:
    if recording.is_set():
        try:
            data = stream.read(CHUNK)
            frames.append(data)
        except OSError as e:
            print(f"读取音频数据时出错: {e}")
            break
    if not recording.is_set() and frames:
        break

# 终止 PyAudio
p.terminate()

# 保存音频数据为 .wav 文件
wf = wave.open(WAVE_OUTPUT_FILENAME, 'wb')
wf.setnchannels(CHANNELS)
wf.setsampwidth(p.get_sample_size(FORMAT))
wf.setframerate(RATE)
wf.writeframes(b''.join(frames))
wf.close()

print(f"音频已保存为 {WAVE_OUTPUT_FILENAME}")