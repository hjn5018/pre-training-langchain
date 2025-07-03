import tkinter as tk
from tkinter import ttk
import pyautogui
import easyocr
import threading
from openai import OpenAI

from dotenv import load_dotenv
import os
from openai import OpenAI

load_dotenv()
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
client = OpenAI(api_key =OPENAI_API_KEY) 

OCR_REGION = (250, 400, 1130, 300)

reader = easyocr.Reader(['ch_sim', 'en'])

def translate_with_gpt(text):
    prompt = f"다음 중국어 문장을 한국어로 번역해줘:\n\n{text}"
    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "You are a professional translator."},
            {"role": "user", "content": prompt}
        ],
        temperature=0.2
    )
    return response.choices[0].message.content.strip()

def process_text():
    try:
        text_box.delete('1.0', tk.END)
        text_box.insert(tk.END, "처리 중...\n")

        screenshot = pyautogui.screenshot(region=OCR_REGION)
        screenshot.save("capture.png")

        results = reader.readtext("capture.png", detail=0)
        extracted_text = " ".join(results).strip()

        if not extracted_text:
            text_box.insert(tk.END, "텍스트를 인식하지 못했습니다.")
            return

        translated = translate_with_gpt(extracted_text)

        text_box.delete('1.0', tk.END)
        text_box.insert(tk.END, f"[OCR 결과]\n{extracted_text}\n\n[GPT 번역 결과]\n{translated}")

    except Exception as e:
        text_box.insert(tk.END, f"\n[오류 발생] {e}")

def on_click():
    threading.Thread(target=process_text).start()

window = tk.Tk()
window.title("워크래프트3 GPT 번역기")
window.geometry("600x500")
window.configure(bg='black')

label = tk.Label(window, text="워크래프트3 실시간 카드 번역", font=("맑은 고딕", 16), bg='black', fg='white')
label.pack(pady=10)

btn = ttk.Button(window, text="OCR + GPT 번역 실행", command=on_click)
btn.pack(pady=10)

text_box = tk.Text(window, wrap='word', font=("맑은 고딕", 12), height=20)
text_box.pack(padx=10, pady=10, fill='both', expand=True)

window.mainloop()
