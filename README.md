# 🤖 Chat with Eva – RAG-based AI PDF Assistant

#### Chat with Eva is an AI-powered RAG-based assistant that helps you interact with your PDF documents in a conversational interface. Upload a PDF file, ask questions, and let Eva find and generate accurate answers using the document content.
---
## Demo Video:
[![Watch the demo](https://img.youtube.com/vi/4a3ZeawoBlY/hqdefault.jpg)](https://www.youtube.com/watch?v=4a3ZeawoBlY)

---

## 🧠 What is RAG?

RAG (Retrieval-Augmented Generation) is a technique that combines:
- Document retrieval → finds relevant content from uploaded PDFs
- Answer generation → forms meaningful, human-like answers

Eva uses this RAG approach to search the PDF and give intelligent responses instead of just keyword-matching.

---

## 💡 Key Features

- Upload any PDF file
- AI agent “Eva” reads & remembers the document
- RAG-based retrieval: Finds the best-matching content
- Conversational chat UI
- Smooth, dark-themed UI (TailwindCSS)
- Fast response with instant feedback
- Easy to integrate with Gemini / GPT / LangChain (Future-ready)

---

## 📁 Project Structure

<img width="650" height="806" alt="image" src="https://github.com/user-attachments/assets/6def7237-afb5-49f3-a93a-9016e7252812" />

--- 

Chat-with-Eva/
│
├── app.py               → Flask backend - routing + PDF handling  
├── storage.py           → Shared variables (pdf, user msg, response)  
├── requirements.txt     → Python dependencies  
├── uploads/             → Uploaded PDFs stored here  
└── templates/  
    └── index.html       → Frontend UI (TailwindCSS + JS)  

---

## 🔧 Setup Instructions

### 1. Clone the Repository

git clone https://github.com/Sanketx125/Chat-with-Eva.git  
cd Chat-with-Eva  

### 2. Create Virtual Environment

python -m venv venv

# Activate:
# Windows:
venv\Scripts\activate

# macOS/Linux:
source venv/bin/activate

### 3. Install Required Packages

pip install -r requirements.txt

### 4. Run the Flask App

python app.py

Now open your browser and go to:  
http://127.0.0.1:5000

---

## 🔍 How RAG Works Here

Eva performs basic RAG in this way:

1. PDF is uploaded and converted to plain text  
2. When the user asks a question:  
   - A retrieval step matches content from the PDF using keyword logic (or vector search in advanced versions)  
3. Eva returns a meaningful AI-generated or rule-based answer  

You can later plug in models like:
- LangChain + FAISS  
- Gemini Pro (Google)  
- GPT-4 / LlamaIndex  

---

## 🛠 Tech Stack

Backend: Flask (Python)  
PDF Parsing: PyMuPDF (fitz)  
Frontend: TailwindCSS + JavaScript  
AI Pattern: Retrieval-Augmented Generation (RAG)  


---

## 🌟 Show Some ❤️

If you like this project:

⭐ Star the repository  
🍴 Fork it and improve  
🧩 Build more features on Eva  

---

## 👩‍💻 Author

Made with ❤️ by Sanket Mane  
Eva is waiting to read your PDFs 😄
