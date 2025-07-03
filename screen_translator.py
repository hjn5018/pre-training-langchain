import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageEnhance
import pyautogui
import easyocr
import threading
from openai import OpenAI
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

from dotenv import load_dotenv
import os

load_dotenv()
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

# ✅ OpenAI API 클라이언트
client = OpenAI(api_key =OPENAI_API_KEY) 

# ✅ OCR 영역
OCR_REGION = (250, 400, 1130, 300)

# ✅ OCR 초기화
reader = easyocr.Reader(['ch_sim', 'en'])

# ✅ 추천 데이터 준비
df1 = pd.read_excel("엘리시아 모음-3.xlsx")
df2 = pd.read_excel("신생 - 개조버전.xlsx", header=None, skiprows=1)
df2.columns = ['캐릭터', '효과 요약', '분류']

combined_df = pd.concat([df1, df2], ignore_index=True)
combined_df = combined_df.dropna(subset=['캐릭터', '효과 요약'])
combined_df['text'] = combined_df['캐릭터'].astype(str) + " " + combined_df['효과 요약'].astype(str)

vectorizer = TfidfVectorizer()
tfidf_matrix = vectorizer.fit_transform(combined_df['text'])

# ✅ 카드 추천 함수
def recommend_cards_based_on_text(user_text, top_n=3):
    user_vec = vectorizer.transform([user_text])
    similarities = cosine_similarity(user_vec, tfidf_matrix).flatten()
    top_indices = similarities.argsort()[::-1][:top_n]

    recommendations = []
    for idx in top_indices:
        name = combined_df.iloc[idx]['캐릭터']
        desc = combined_df.iloc[idx]['효과 요약']
        score = round(similarities[idx], 2)
        recommendations.append((name, desc, score))

    return recommendations

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

# ✅ 이미지 전처리

def preprocess_image(pil_img):
    gray = pil_img.convert("L")
    enhancer = ImageEnhance.Contrast(gray)
    return enhancer.enhance(2.5)

# ✅ OCR + GPT + 추천

def process_text():
    try:
        text_box.delete('1.0', tk.END)
        text_box.insert(tk.END, "처리 중...\n")

        screenshot = pyautogui.screenshot(region=OCR_REGION)
        processed_img = preprocess_image(screenshot)
        processed_img.save("capture.png")

        results = reader.readtext("capture.png", detail=0)
        extracted_text = " ".join(results).strip()

        if not extracted_text:
            text_box.insert(tk.END, "텍스트를 인식하지 못했습니다.")
            return

        translated = translate_with_gpt(extracted_text)

        text_box.delete('1.0', tk.END)
        text_box.insert(tk.END, f"[OCR 결과]\n{extracted_text}\n\n[GPT 번역 결과]\n{translated}")

        # 카드 추천
        recommendations = recommend_cards_based_on_text(translated)
        recommendation_text = "\n\n[추천 카드]\n"
        for name, desc, score in recommendations:
            recommendation_text += f"✔ {name} (유사도 {score})\n  - {desc.strip()[:60]}...\n"

        text_box.insert(tk.END, recommendation_text)

    except Exception as e:
        text_box.insert(tk.END, f"\n[오류 발생] {e}")

# ✅ UI 구성

def on_click():
    threading.Thread(target=process_text).start()

window = tk.Tk()
window.title("워크래프트3 GPT 번역 + 추천기")
window.geometry("600x500")
window.configure(bg='black')

label = tk.Label(window, text="워크래프트3 실시간 카드 번역 + 추천", font=("맑은 고딕", 16), bg='black', fg='white')
label.pack(pady=10)

btn = ttk.Button(window, text="OCR + GPT 번역 + 추천", command=on_click)
btn.pack(pady=10)

text_box = tk.Text(window, wrap='word', font=("맑은 고딕", 12), height=20)
text_box.pack(padx=10, pady=10, fill='both', expand=True)

window.mainloop()

