# SmartFoodSupplyChainMonitoringSystem

This advises the ideal storage temperature for food items based on the current temperature readings from an Arduino and optimal food storage temperatures using OpenAI's GPT-3.5 model.

## Features
Temperature Monitoring: Reads temperature data from an Arduino connected via a serial port.

OpenAI Integration: Uses OpenAI's GPT-3.5 to generate advice on the ideal storage temperature for a given food item.

Text-to-Speech: Converts the OpenAI response into speech using EdgeTTS.

Multilingual Support: Supports multiple languages (English, Spanish, French) for text-to-speech output.

Gradio Interface: Provides a web-based interface for easy interaction.

## Requirements
- Python 3.7+
- Libraries: `gradio`, `openai`, `pyserial`, `edge_tts`, `statistics`, `uuid`, `asyncio`, `os`

## Installation
1. Clone the repository:
   ```bash
   git clone https://github.com/Chaitanya-Kante/SmartFoodSupplyChainMonitoringSystem.git
