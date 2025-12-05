import streamlit as st
import cv2
from PIL import Image
import base64
import io
import numpy as np
from datetime import datetime
import requests
import json

# ==========================
# PAGE SETTINGS
# ==========================
st.set_page_config(layout="wide", page_title="OCR Extractor")

# ==========================
# DARK THEME CSS
# ==========================
dark_css = """
<style>
    body {
        background-color: #0d1117;
        color: #c9d1d9;
    }
    .main-title {
        font-size: 38px;
        font-weight: 700;
        text-align: center;
        color: #58a6ff;
        padding: 15px 0 5px 0;
    }
    .sub-header {
        font-size: 20px;
        font-weight: 600;
        margin-top: 15px;
        color: #79c0ff;
    }
    .time-box {
        background: #161b22;
        padding: 12px;
        border-radius: 8px;
        font-size: 16px;
        border-left: 5px solid #238636;
        margin-top: 15px;
        color: #c9d1d9;
    }
    .stTextArea textarea {
        background-color: #0d1117 !important;
        color: #c9d1d9 !important;
        border: 1px solid #30363d;
    }
</style>
"""
st.markdown(dark_css, unsafe_allow_html=True)

st.markdown("<div class='main-title'>AI OCR Extractor</div>", unsafe_allow_html=True)


# ==========================
# FAST FUNCTIONS
# ==========================
def fast_resize(img, max_dim=1200):
    h, w = img.shape[:2]
    if max(h, w) > max_dim:
        scale = max_dim / max(h, w)
        img = cv2.resize(img, None, fx=scale, fy=scale, interpolation=cv2.INTER_AREA)
    return img


def fast_preprocess(img):
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    final = cv2.adaptiveThreshold(
        gray, 255,
        cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
        cv2.THRESH_BINARY,
        17, 7
    )
    return final


# ==========================
# FILE UPLOAD UI
# ==========================
uploaded_file = st.file_uploader("📤 Upload your image", type=["jpg", "jpeg", "png"])

# Start time
start_time = datetime.now()


if uploaded_file:

    start_time = datetime.now()
    status_box = st.info("🔄 Processing image… Please wait")

    # Convert to OpenCV
    file_bytes = np.asarray(bytearray(uploaded_file.read()), dtype=np.uint8)
    img = cv2.imdecode(file_bytes, 1)

    img = fast_resize(img)
    final = fast_preprocess(img)
    pil_image = Image.fromarray(final)

    # Encode base64
    buffered = io.BytesIO()
    pil_image.save(buffered, format="PNG")
    image_base64 = base64.b64encode(buffered.getvalue()).decode("utf-8")

    payload = {
        "model": "qwen2.5vl:3b",
        "prompt": "Extract all text exactly as shown in the image. Do NOT guess or repeat.",
        "images": [image_base64],
    }

    response = requests.post(
        "http://localhost:11434/api/generate",
        json=payload,
        stream=True
    )

    full_text = ""
    stream_placeholder = st.empty()   # ONLY THIS updates during stream

    # 🔥 STREAMING — SAFE (NO text_area inside loop)
    for line in response.iter_lines():
        if line:
            data = json.loads(line.decode("utf-8"))
            if "response" in data:
                full_text += data["response"]
                # stream_placeholder.markdown(
                #     f"```\n{full_text}\n```")
                

    end_time = datetime.now()
    diff_time = end_time - start_time

    status_box.success("✅ OCR Completed Successfully!")

    # ==========================
    # FINAL UI (NO DUPLICATE IDs)
    # ==========================
    col1, col2 = st.columns(2)

    with col1:
        st.markdown("<div class='sub-header'>📸 Uploaded Image</div>", unsafe_allow_html=True)
        st.image(pil_image, use_container_width=True)

    with col2:
        st.markdown("<div class='sub-header'>📝 Extracted Text</div>", unsafe_allow_html=True)
        st.text_area("OCR Output", full_text, height=500, key="final_ocr_output")

    # ==========================
    # TIME SUMMARY
    # ==========================
   # End time
end_time = datetime.now()
time_taken = (end_time - start_time).total_seconds()

# 🔲 Rectangle button-style box
st.markdown(
    f"""
    <div style="
        padding: 12px 20px;
        background-color: #1e90ff;
        color: white;
        font-size: 20px;
        font-weight: bold;
        text-align: center;
        border-radius: 8px;
        width: 250px;
        ">
        ⏱ Time Taken: {time_taken:.2f} sec
    </div>
    """,
    unsafe_allow_html=True
)
