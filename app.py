import streamlit as st
from streamlit_chat import message
import requests
from audiorecorder import audiorecorder

if 'messages' not in st.session_state:
    st.session_state['messages'] = []

chat_url = "http://localhost:8000/transcribe"

def chat(text):
    user_turn = {"role":"user", "content": text}
    messages = st.session_state['messages']
    resp = requests.post(chat_url, json={"messages" : messages + [user_turn]})
    assistant_turn = resp.json()

    st.session_state['messages'].append(user_turn)
    st.session_state['messages'].append(assistant_turn)

st.title('오디오 서비스')

row1 = st.container() # 위젯의 상하 위치를 지정해 주기 위해서 사용(질문은 아래에 )
row2 = st.container() # 위젯의 상하 위치를 지정해 주기 위해서 사용(챗 내용은 위에)

with row2:
    # input_text = st.text_input("You")
    # if input_text:
    #     chat(input_text)
    audio = audiorecorder("Click to record", "Recording...")
    if len(audio)>0:
        st.audio(audio.tobytes())

with row1:
    for i, msg_obj in enumerate(st.session_state['messages']):
        msg = msg_obj['content']
        is_user = False
        if i % 2 == 0:
            is_user = True
        message(msg, is_user=is_user, key=f"chat_{i}") #각 화자마다 메세지가 2개 이상이 되면 에러가 나기 때문에 각 메세지를 key로 구분해줘야함

