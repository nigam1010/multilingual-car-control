import pyaudio
import vosk
import json
import re
import threading
import tkinter as tk
import paho.mqtt.client as mqtt
import os

# === Load VOSK Models ===
models = {
    "en": vosk.Model("model/vosk-model-small-en-us-0.15"),
    "hi": vosk.Model("model/vosk-model-small-hi-0.22"),
    "ja": vosk.Model("model/vosk-model-small-ja-0.22")
}

recognizers = {
    lang: vosk.KaldiRecognizer(model, 16000) for lang, model in models.items()
}

# === MQTT Settings ===
broker_address = "3f5b9bccedc34823b47f445f5346db10.s1.eu.hivemq.cloud"
port = 8883
username = "knigam"
password = "1234567Ka"
topic = "esp32/command"

client = mqtt.Client("voice_control")
client.username_pw_set(username, password)
client.tls_set()

# === Command Variations ===
commands = {
    "forward": ["forward", "ahead", "move", "go", "aage", "आगे", "進め", "前"],
    "backward": ["backward", "back", "reverse", "peeche", "पीछे", "後ろ", "戻る"],
    "left": ["left", "turn left", "baayein", "बाएं", "左"],
    "right": ["right", "turn right", "daayein", "दाएं", "右"],
    "stop": ["stop", "halt", "ruk", "रुको", "止まれ", "やめて"]
}

def get_command(text):
    text = text.lower()
    for cmd, variations in commands.items():
        for v in variations:
            if v in text:
                return cmd
    return None

# === MQTT Callbacks ===
def on_connect(client, userdata, flags, rc):
    if rc == 0:
        update_status("MQTT Connected", "green")
    else:
        update_status(f"MQTT Failed (code {rc})", "red")

client.on_connect = on_connect

def send_command(cmd):
    if client.is_connected():
        client.publish(topic, cmd)
        update_status(f"Sent: {cmd}", "blue")
    else:
        update_status("MQTT not connected", "red")

# === Vosk Listener Thread ===
def listen_for_commands():
    p = pyaudio.PyAudio()
    stream = p.open(format=pyaudio.paInt16, channels=1, rate=16000,
                    input=True, frames_per_buffer=8000)
    stream.start_stream()

    while True:
        data = stream.read(4000, exception_on_overflow=False)
        for lang, recognizer in recognizers.items():
            if recognizer.AcceptWaveform(data):
                result = json.loads(recognizer.Result())
                text = result.get('text', '')
                if text:
                    cmd = get_command(text)
                    if cmd:
                        send_command(cmd)
                        break  # stop checking other models once command is found

def start_voice_thread():
    threading.Thread(target=listen_for_commands, daemon=True).start()

# === GUI Setup ===
def update_status(message, color):
    status_label.config(text=message, fg=color)

root = tk.Tk()
root.title("Voice + Button Car Controller")
root.geometry("320x400")

tk.Label(root, text="IoT Car Controller", font=("Helvetica", 16)).pack(pady=10)

tk.Button(root, text="↑ Forward", width=20, height=2, command=lambda: send_command("forward")).pack(pady=5)
tk.Button(root, text="← Left", width=20, height=2, command=lambda: send_command("left")).pack(pady=5)
tk.Button(root, text="→ Right", width=20, height=2, command=lambda: send_command("right")).pack(pady=5)
tk.Button(root, text="↓ Backward", width=20, height=2, command=lambda: send_command("backward")).pack(pady=5)
tk.Button(root, text="■ Stop", width=20, height=2, bg="red", fg="white", command=lambda: send_command("stop")).pack(pady=5)

status_label = tk.Label(root, text="Connecting to MQTT...", fg="orange")
status_label.pack(pady=15)

client.connect(broker_address, port)
client.loop_start()
start_voice_thread()

root.mainloop()
