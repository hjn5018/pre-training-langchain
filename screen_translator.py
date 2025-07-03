import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageEnhance
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

# ✅ 화면 OCR 영역 (1920x1080 해상도 기준)
OCR_REGION = (250, 400, 1130, 300)

# ✅ EasyOCR 초기화
reader = easyocr.Reader(['ch_sim', 'en'])

# ✅ 이미지 전처리 함수 (그레이스케일 + 대비 강화)
def preprocess_image(pil_img):
    gray = pil_img.convert("L")
    enhancer = ImageEnhance.Contrast(gray)
    enhanced = enhancer.enhance(2.5)  # 대비 강화 (2.5~3.0 추천)
    return enhanced

# ✅ GPT 번역 함수
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

# ✅ OCR + GPT 번역 처리
def process_text():
    try:
        text_box.delete('1.0', tk.END)
        text_box.insert(tk.END, "처리 중...\n")

        # 스크린샷 찍기
        screenshot = pyautogui.screenshot(region=OCR_REGION)

        # 이미지 전처리
        processed_img = preprocess_image(screenshot)

        # OCR 실행
        results = reader.readtext(processed_img, detail=0)
        extracted_text = " ".join(results).strip()

        if not extracted_text:
            text_box.insert(tk.END, "텍스트를 인식하지 못했습니다.")
            return

        # GPT 번역
        translated = translate_with_gpt(extracted_text)

        # 출력
        text_box.delete('1.0', tk.END)
        text_box.insert(tk.END, f"[OCR 결과]\n{extracted_text}\n\n[GPT 번역 결과]\n{translated}")

    except Exception as e:
        text_box.insert(tk.END, f"\n[오류 발생] {e}")

# ✅ 버튼 스레드 실행
def on_click():
    threading.Thread(target=process_text).start()

# ✅ Tkinter UI 구성
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
