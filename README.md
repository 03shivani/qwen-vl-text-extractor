# qwen-vl-text-extractor
AI OCR Extractor is a fast, local OCR app built with Streamlit and powered by the Qwen 2.5 VL 3B model via Ollama. It converts images to clean text instantly with zero cloud use. Designed for low-capacity systems, but easily upgradeable to larger, more accurate models like 7B, 14B, or newer VLMs.

## 🚀 Features

- **Local OCR Processing** – No cloud required, secure for confidential data.
- **Fast Image-to-Text Conversion** – Real-time streaming of extracted text.
- **Smart Preprocessing Pipeline** – Auto-resize, grayscale, and adaptive thresholding for better OCR results.
- **Dark-Themed UI** – Modern, sleek interface built with Streamlit.
- **Model Upgradeable** – Easily switch to larger, more accurate VLMs via Ollama.

---

## 🛠 Tech Stack

- **Python**  
- **Streamlit** – Web UI  
- **OpenCV** – Image preprocessing  
- **Pillow (PIL)** – Image handling  
- **NumPy** – Array operations  
- **Requests** – Model API communication  
- **Ollama** – Local model runtime  

---

Install Ollama

Follow the instructions at [Ollama Docs](https://ollama.com/docs/installation)

download the model : ollama pull qwen2.5vl:3b 

---
Run the App

streamlit run qwen_vit.py
