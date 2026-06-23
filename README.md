# 🎥 AI Video Assistant

An AI-powered Video Assistant that allows users to analyze video content using Large Language Models (LLMs). The system processes videos, generates transcripts, stores semantic embeddings in a vector database, and enables natural language question answering over video content.

---

## 🚀 Features

✅ Download videos from supported sources

✅ Extract and process audio

✅ Generate accurate transcripts

✅ Create semantic embeddings

✅ Store embeddings in a vector database

✅ Retrieve relevant context using RAG

✅ Ask questions about video content

✅ Streamlit-based user interface

---

## 🏗️ Architecture

```text
Video URL/File
       │
       ▼
Video Downloader
       │
       ▼
Audio Extraction
       │
       ▼
Transcription
       │
       ▼
Text Chunking
       │
       ▼
Embedding Generation
       │
       ▼
Vector Database
       │
       ▼
User Question
       │
       ▼
Retriever
       │
       ▼
LLM Response
```

---

## 📂 Project Structure

```text
my-video-assistant/
│
├── core/
│   ├── transcription logic
│   ├── embedding generation
│   └── retrieval pipeline
│
├── downloaders/
│   ├── video download modules
│
├── utilities/
│   ├── helper functions
│   └── preprocessing utilities
│
├── vector_db/
│   ├── stored embeddings
│
├── main.py
├── mainUI.py
├── requirements.txt
├── .env
└── README.md
```

---

## ⚙️ Tech Stack

- Python
- Streamlit
- OpenAI / Gemini / Groq API
- LangChain
- Vector Database
- Sentence Transformers
- Whisper (if used)
- FAISS / ChromaDB (if used)

---

## 🛠️ Installation

### Clone Repository

```bash
git clone https://github.com/yourusername/ai-video-assistant.git
cd ai-video-assistant
```

### Create Virtual Environment

```bash
python -m venv .venv
```

### Activate Environment

Windows:

```bash
.venv\Scripts\activate
```

Linux / Mac:

```bash
source .venv/bin/activate
```

### Install Dependencies

```bash
pip install -r requirements.txt
```

---

## 🔑 Environment Variables

Create a `.env` file in the root directory.

```env
OPENAI_API_KEY=your_api_key
GROQ_API_KEY=your_api_key
GOOGLE_API_KEY=your_api_key
```

Add only the keys required by your implementation.

---

## ▶️ Running the Application

### Launch Streamlit UI

```bash
streamlit run mainUI.py
```

### Run Backend Script

```bash
python main.py
```

---

## 💡 Example Workflow

1. Provide a video URL or upload a video.
2. The system downloads and processes the video.
3. Audio is extracted and transcribed.
4. Transcript is converted into embeddings.
5. Embeddings are stored in the vector database.
6. Users ask questions about the video.
7. Relevant context is retrieved.
8. The LLM generates accurate answers.

---

## 📸 Demo

### Home Screen

_Add screenshot here_

### Question Answering

_Add screenshot here_

### Generated Transcript

_Add screenshot here_

---

## 🎯 Use Cases

- YouTube Video Analysis
- Lecture Summarization
- Meeting Analysis
- Research Videos
- Educational Content Search
- Knowledge Retrieval from Long Videos

---

## 🔒 Security

Sensitive files are excluded using `.gitignore`.

```gitignore
.venv/
.env
__pycache__/
```

---

## 📈 Future Improvements

- Multi-video knowledge base
- Hybrid Search (BM25 + Vector Search)
- Agentic RAG
- Citation-based responses
- Multi-language support
- Real-time video processing

---

## 🤝 Contributing

Contributions are welcome.

1. Fork the repository
2. Create a feature branch
3. Commit your changes
4. Push to GitHub
5. Open a Pull Request

---

## 👨‍💻 Author

**Sagar Kandpal**

Passionate about AI Engineering, Generative AI, RAG Systems, and AI Agents.

GitHub: https://github.com/yourusername

LinkedIn: https://linkedin.com/in/yourprofile
