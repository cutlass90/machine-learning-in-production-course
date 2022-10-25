from fastapi import FastAPI, File, UploadFile, Form
import requests

app = FastAPI()

@app.post("/train")
def train(media: UploadFile = File(...)):
    data = {
        'images': media,
        'chekpoint_path': chekpoint_path,
    }
    response = requests.post('http://127.0.0.1:8000/train', files=data)
    print(response)
    write_event2db(event_type='train started', user_id, time, checkpount_path)



@app.get("/generate-image")
def generate_image(prompt_id):
    pass