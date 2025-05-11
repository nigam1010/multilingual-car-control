A Python-based GUI application that controls an IoT car using both voice commands and button inputs. Supports commands in English, Hindi, and Japanese using the Vosk speech recognition library, and communicates with an ESP32 over MQTT.

## 🌟 Features

- 🎙️ Voice recognition in English, Hindi, and Japanese
- 📦 MQTT protocol for secure cloud communication (via HiveMQ Cloud)
- 🖱️ GUI control with direction buttons
- 🔄 Real-time status updates

## 🛠️ Technologies Used

- Python
- Vosk (offline voice recognition)
- PyAudio
- Tkinter
- Paho MQTT
- HiveMQ Cloud MQTT Broker

## 📁 Project Structure

main.py

model/

├── vosk-model-small-en-us-0.15/

├── vosk-model-small-hi-0.22/

└── vosk-model-small-ja-0.22/

## 🧪 Requirements

See `requirements.txt`.

To install:

pip install -r requirements.txt

## 🚀 How to Run

1. Install dependencies
2. Ensure the `model/` directory contains all Vosk language models as listed above
3. Run:

## 🗣️ Supported Voice Commands

| Command | Variants (English / Hindi / Japanese) |
| --- | --- |
| Forward | forward, move, aage, आगे, 進め, 前 |
| Backward | back, peeche, पीछे, 後ろ, 戻る |
| Left | left, baayein, बाएं, 左 |
| Right | right, daayein, दाएं, 右 |
| Stop | stop, halt, ruk, रुको, 止まれ, やめて |

## 🔐 MQTT Settings (configured in `main.py`)

- Broker: `3f5b9bccedc34823b47f445f5346db10.s1.eu.hivemq.cloud`
- Port: `8883` (SSL)
- Username: `knigam`
- Topic: `esp32/command`

⚠️ **Note:** Credentials are for demo use. Consider using environment variables for security.

## 📷 GUI Preview

A simple Tkinter interface with direction buttons and a status indicator.

## 📄 License

MIT License
