# Smart Food Supply Chain Monitoring System

This system advises the ideal storage temperature for food items based on the current environment temperature readings from an Arduino and optimal food storage temperatures using OpenAI's GPT-3.5 model.

## Features

### Temperature Reading
- The DHT11 temperature sensor reads 20 temperature values from the Arduino and calculates the median temperature.

### OpenAI Integration
- The median temperature and a user-provided food item are sent to OpenAI's GPT-3.5 model.
- OpenAI generates a response with advice on the ideal storage temperature for the food item.

### Text-to-Speech
- The OpenAI response is converted into speech using EdgeTTS.
- The speech is generated in the selected language (English, Spanish, or French).

### Gradio Interface
- Users can interact with the system via a web-based interface.
- Enter a food item and select a language to get advice on its storage temperature.

## Configuration

### OpenAI API Key
Set the `OPENAI_API_KEY` environment variable with your OpenAI API key.

### Serial Port
Update the `ser = serial.Serial('COM3', 9600)` line in `app.py` with the correct serial port for your Arduino.

### Languages
The system supports English (`en`), Spanish (`es`), and French (`fr`). You can add more languages by updating the `voice_mapping` dictionary in the `text_to_speech` function.

## Requirements
- Python 3.7+
- Libraries: `gradio`, `openai`, `pyserial`, `edge_tts`, `statistics`, `uuid`, `asyncio`, `os`

