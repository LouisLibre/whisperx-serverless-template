# Do not edit if deploying to Banana Serverless
# This file is boilerplate for the http server, and follows a strict interface.

# Instead, edit the init() and inference() functions in app.py

from potassium import Potassium, Request, Response
import torch
import whisperx
import os
import subprocess
import base64
from io import BytesIO

app = Potassium("server")

def extract_segments(segments_list):
    resp = []
    for seg in segments_list:
        resp.append({
            'start': seg['start'],
            'end': seg['end'],
            'text': seg['text']
        })
    return resp

# @app.init runs at startup, and loads models into the app's context
@app.init
def init():
    device = torch.device("cuda") if torch.cuda.is_available() else torch.device("cpu")
    model = whisperx.load_model("large", device)
    print(f"CUDA available? {torch.cuda.is_available()}, device: {device}")

    context = {
        "model": model
    }

    return context

# @app.handler runs for every call
@app.handler("/")
def handler(context: dict, request: Request) -> Response:
    prompt = request.json.get("prompt")
    model = context.get("model")
    device = torch.device("cuda") if torch.cuda.is_available() else torch.device("cpu")

    try:
        model_inputs = response.json.loads(request.json)
    except:
        model_inputs = request.json

    language = model_inputs.get("language", None)
    mp3BytesString = model_inputs.get('mp3BytesString', None)
    if mp3BytesString == None:
        return response.json({'message': "No input provided"})

    mp3Bytes = BytesIO(base64.b64decode(mp3BytesString.encode("ISO-8859-1")))
    audio_file_name = "input.mp3"
    with open(audio_file_name,'wb') as file:
        file.write(mp3Bytes.getbuffer())

    # Run the model
    result = model.transcribe(audio_file_name, language=language)

    # load alignment model and metadata
    model_a, metadata = whisperx.load_align_model(language_code=result["language"], device=device)
    result_aligned = whisperx.align(result["segments"], model_a, metadata, audio_file_name, device)
    os.remove(audio_file_name)

    response = {
        'word_segments': result_aligned["word_segments"],
        'paragraphs': extract_segments(result_aligned['segments'])
    }

    return Response(
        json = {"outputs": response},
        status=200
    )

if __name__ == "__main__":
    app.serve()
