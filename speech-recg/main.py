import requests
from api_secret import API_KEY_ASSEMBLYAI
import sys

#endpoints
upload_endpoint = "https://api.assemblyai.com/v2/upload"
transcript_endpoint = "https://api.assemblyai.com/v2/transcript"

#upload
filename = sys.argv[1]

def read_file(filename, chunk_size = 5242880):
    with open(filename, 'rb') as _file:
        while True:
            data = _file.read(chunk_size)
            if not data:
                break
            yield data
headers = {'authorization': API_KEY_ASSEMBLYAI}
response = requests.post(upload_endpoint,
                         headers=headers,
                         data= read_file(filename))

print(response.json())

audio_url = response.json()['upload_url']

#transcript
json = {"audio_url": audio_url}
response = requests.post(transcript_endpoint, json= json, headers=headers)
print(response.json())

