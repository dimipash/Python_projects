from gtts import gTTS
import os

text = 'Hello World!'
output = gTTS(text=text, lang='en', slow=False)
output.save('hello.mp3')

os.system("start hello.mp3")