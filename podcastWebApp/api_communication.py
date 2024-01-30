import requests
from api_secrets import API_KEY_ASSEMBLYAI
import time

#upload

#endpoints
upload_endpoint = "https://api.assemblyai.com/v2/upload"
transcript_endpoint = "https://api.assemblyai.com/v2/transcript"
headers = {'authorization': API_KEY_ASSEMBLYAI}

def upload(filename):
    def read_file(filename, chunk_size = 5242880):
        with open(filename, 'rb') as _file:
            while True:
                data = _file.read(chunk_size)
                if not data:
                    break
                yield data
    upload_response = requests.post(upload_endpoint,
                            headers=headers,
                            data= read_file(filename))


    audio_url = upload_response.json()['upload_url']
    return audio_url



#transcribe
def transcribe(audio_url):
    transcript_request = {"audio_url": audio_url}
    transcript_response = requests.post(transcript_endpoint, json= transcript_request, headers=headers)
    job_id = transcript_response.json()['id']
    return job_id





#poll
def poll(transcript_id):
    polling_endpoint = transcript_endpoint + '/' + transcript_id
    polling_responnse = requests.get(polling_endpoint, headers=headers)
    return polling_responnse.json()

def get_transcription_result_url(audio_url):
    transcript_id = transcribe(audio_url)
    while True:
        data = poll(transcript_id)
        if data['status'] == 'completed':
            return data, None
        elif data['status'] == 'error':
            return data, data['error']
        
        print('wating 30 secs...')
        time.sleep(30)

#save transcript

def save_transcript(audio_url,filename):
    data, error = get_transcription_result_url(audio_url)

    if data:
        text_filename = filename + ".txt"
        with open(text_filename, 'w') as f:
            f.write(data['text'])
        print('transcription saved')
    elif error:
        print('error occured', error)
