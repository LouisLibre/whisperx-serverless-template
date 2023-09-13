# This file is used to verify your http server acts as expected
# Run it with `python3 test.py``

import requests
from io import BytesIO
import base64
import banana_dev as client

my_model = client.Client(
    api_key="57327466-8213-495b-a28e-6d7c28b4dfde",
    model_key="fb7e5f11-d9e9-4c05-88e2-06de05a304cf",
    url="https://whisperx-serverless-template-lmi2r62857.run.banana.dev",
)

#Needs test.mp3 file in directory
with open(f'test.mp3','rb') as file:
    mp3bytes = BytesIO(file.read())
mp3 = base64.b64encode(mp3bytes.getvalue()).decode("ISO-8859-1")
model_payload = {"language": "en", "mp3BytesString":mp3}

result, meta = my_model.call("/", inputs)

print(result)