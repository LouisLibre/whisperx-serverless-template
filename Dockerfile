# Must use a Cuda version 11+
FROM pytorch/pytorch:1.11.0-cuda11.3-cudnn8-runtime

WORKDIR /

RUN apt-get update && \
    apt-get install -y git ffmpeg && \
    apt-get install -y ffmpeg && \
    apt-get install -y libsndfile1 && \
    apt-get clean

# Install python packages
RUN pip3 install --upgrade pip
ADD requirements.txt requirements.txt
RUN pip3 install -r requirements.txt

# Add your model weight files 
# (in this case we have a python script)
ADD download.py .
RUN python3 download.py

# We add the banana boilerplate here
ADD app.py .

EXPOSE 8000

CMD python3 -u app.py
