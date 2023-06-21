from fastapi import FastAPI, UploadFile, File
from typing import List
from pydantic import BaseModel
import openai

openai.api_key = "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"

def chat(messages):
   response = openai.ChatCompletion.create(model='gpt-3.5-turbo', messages=messages)
   resp_dict = response.to_dict_recursive() 
   #openai에서 제공하는 결과를 dictionary로 바꾸는데, 깊은 구조를 다 풀어서 받는 방법 to_dict_recursive()
   assistant_turn = resp_dict['choices'][0]['message']
   return assistant_turn #{"role":"assistant", "content":"~~~~~~~"}

app = FastAPI()

class Turn(BaseModel):
   role : str
   content : str

class Messages(BaseModel):
   messages : List[Turn]  # [{"role":"user", "content":"~~~~~~~"}, {"role":"assistant", "content":"~~~~~~~"}
                          # , {"role":"user", "content":"~~~~~~~"}, ... ...] 

@app.post("/chat", response_model=Turn) #response_model의 결과는 Turn object형태로 나간다고 명시
def post_chat(messages : Messages):
   messages = messages.dict()
   assistant_turn = chat(messages=messages['messages']) #messages가 딕셔너리 이기 때문에
   return assistant_turn

@app.post("/transcribe")
def transcribe_audio(audio_file: UploadFile=File(...)): #fastapi에서 업로드 파일을 받는 방식
   try:
      file_name = "tmp_audio_file.wav"
      with open(file_name, 'wb') as f:
         f.write(audio_file.file.read()) #local에 파일을 먼저 쓴다음

      with open(file_name, 'rb') as f: #파일을 읽어서
         transcription = openai.Audio.transcribe("whisper-1", f) #파일을 openai에 넘겨주면 텍스트로 작성함
      
      text = transcription['text']
   except Exception as e:
      print(e)
      text = f"음성인식에서 실패했습니다.{e}"
   return {"text": text}
