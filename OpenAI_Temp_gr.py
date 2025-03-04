import serial
import openai
import os
import statistics
import uuid
import asyncio
import edge_tts
import gradio as gr

# Set up the OpenAI API key
openai.api_key = os.getenv("OPENAI_API_KEY") 
# Set up the serial connection (adjust the port and baud rate as needed)
try:
    ser = serial.Serial('COM3', 9600)  # Replace 'COM3' with your Arduino's serial port
    print("Serial port opened successfully!")
except serial.SerialException as e:
    print(f"Error opening serial port: {e}")
    exit()

def read_temperatures(num_readings=20):
    """Read a specified number of temperature readings from the Arduino and return them as a list."""
    temperatures = []
    print("Reading temperatures from Arduino...")
    while len(temperatures) < num_readings:
        if ser.in_waiting > 0:
            # Read the temperature data from the serial port
            temp_data = ser.readline().decode('utf-8').strip()
            try:
                # Convert the temperature data to a float
                temperature = float(temp_data)
                temperatures.append(temperature)
                print(f"Reading {len(temperatures)}: {temperature} °C")
            except ValueError:
                print("Invalid temperature data received:", temp_data)
    return temperatures

def calculate_median(temperatures):
    """Calculate the median of a list of temperatures."""
    median_temperature = statistics.median(temperatures)
    return round(median_temperature, 2)

def call_openai_api(food_item, temperature):
    """Call the OpenAI API to generate a response in English."""
    client = openai.OpenAI(api_key=openai.api_key)  # Initialize the OpenAI client
    prompt = f"The current temperature is {temperature}°C. Where should be the {food_item} storage temperature for better shelflife?"
    response = client.chat.completions.create(
        model="gpt-3.5-turbo",  # Use the GPT-3.5 model
        messages=[{"role": "system", "content": "You are a helpful assistant. Also mention the current temperature."},
                  {"role": "user", "content": prompt}],
        max_tokens=150,  # Limit the response length
    )
    return response.choices[0].message.content.strip()

async def text_to_speech(text, lang='en'):
    """Convert text to speech using EdgeTTS."""
    # Get the user's temporary folder path
    temp_folder = os.getenv('TEMP')  # Get the system temp folder

    # Create a temporary file with a unique name in the temp folder
    output_file = os.path.join(temp_folder, f"output_{uuid.uuid4()}.mp3")

    # Map language to EdgeTTS voice
    voice_mapping = {
        'en': 'en-US-JennyNeural',  # English
        'es': 'es-ES-ElviraNeural',  # Spanish
        'fr': 'fr-FR-DeniseNeural',  # French
    }
    voice = voice_mapping.get(lang, 'en-US-JennyNeural')  # Default to English if language not found

    # Generate speech using EdgeTTS
    communicate = edge_tts.Communicate(text, voice)
    await communicate.save(output_file)

    return output_file

# Gradio Interface
def process_input(food_item, lang):
    # Read 20 temperature values from Arduino
    temperatures = read_temperatures(20)

    # Calculate the median temperature
    median_temperature = calculate_median(temperatures)
    print(f"Median Temperature: {median_temperature} °C")

    # Call OpenAI API
    response = call_openai_api(food_item, median_temperature)
    print("OpenAI Response:", response)

    # Add the median temperature to the response
    full_response = f"Current Temperature: {median_temperature}°C\n\n{response}"

    # Convert the response to speech using EdgeTTS
    audio_file = asyncio.run(text_to_speech(full_response, lang=lang))

    return full_response, audio_file

# Gradio Interface Layout
iface = gr.Interface(
    fn=process_input,
    inputs=[gr.Textbox(label="Enter the food item:"), 
            gr.Dropdown(label="Select language:", choices=["en", "es", "fr"], value="en")],
    outputs=[gr.Textbox(label="OpenAI Response"), 
             gr.Audio(label="Generated Speech")],
    title="Smart Food Supply Chain Monitoring System",
    description="Enter a food item and select a language to get advice on its storage temperature."
)

# Launch the Gradio interface
iface.launch(share=True)  # Run locally without creating a public link
