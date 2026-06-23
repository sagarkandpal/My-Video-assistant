import streamlit as st
import os
import re
import tempfile
import datetime

st.set_page_config(
    page_title="NexaMind · Meeting Intelligence",
    page_icon="🧠",
    layout="wide",
    initial_sidebar_state="collapsed",
)

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=DM+Sans:wght@300;400;500;600&family=Space+Mono:wght@400;700&display=swap');

:root {
  --bg-primary:    #0b0f1a;
  --bg-secondary:  #111827;
  --bg-card:       #141c2e;
  --border-subtle: rgba(255,255,255,0.07);
  --border-glow:   rgba(99,179,237,0.3);
  --text-primary:  #e8edf5;
  --text-secondary:#94a3b8;
  --text-muted:    #4a5568;
  --font-main:     'DM Sans', sans-serif;
  --font-mono:     'Space Mono', monospace;
}

html, body, [data-testid="stAppViewContainer"] {
  background: var(--bg-primary) !important;
  font-family: var(--font-main) !important;
  color: var(--text-primary) !important;
}

#MainMenu, footer, header { visibility: hidden; }
[data-testid="stToolbar"] { display: none; }
.block-container { padding: 2rem 2.5rem 4rem !important; max-width: 1280px; }

@keyframes fadeUp {
  from { opacity: 0; transform: translateY(14px); }
  to   { opacity: 1; transform: translateY(0); }
}

.grad-text {
  background: linear-gradient(135deg, #63b3ed 0%, #7c8cf8 50%, #b794f4 100%);
  -webkit-background-clip: text; -webkit-text-fill-color: transparent; background-clip: text;
}

.nexacard {
  background: var(--bg-card);
  border: 1px solid var(--border-subtle);
  border-radius: 16px;
  padding: 1.75rem;
  box-shadow: 0 8px 32px rgba(0,0,0,0.4);
  animation: fadeUp 0.4s ease both;
  position: relative; overflow: hidden;
  margin-bottom: 1rem;
}
.nexacard::before {
  content: ''; position: absolute; top: 0; left: 0; right: 0; height: 1px;
  background: linear-gradient(90deg, transparent, rgba(99,179,237,0.4), transparent);
}

.pill {
  display: inline-flex; align-items: center;
  padding: 3px 10px; border-radius: 999px; font-size: 0.7rem;
  font-weight: 600; letter-spacing: 0.04em; text-transform: uppercase;
  font-family: var(--font-mono);
}
.pill-cyan    { background: rgba(99,179,237,0.12);  color: #63b3ed; border: 1px solid rgba(99,179,237,0.25); }
.pill-emerald { background: rgba(79,209,165,0.12);  color: #4fd1a5; border: 1px solid rgba(79,209,165,0.25); }
.pill-violet  { background: rgba(183,148,244,0.12); color: #b794f4; border: 1px solid rgba(183,148,244,0.25); }
.pill-amber   { background: rgba(246,173,85,0.12);  color: #f6ad55; border: 1px solid rgba(246,173,85,0.25); }
.pill-indigo  { background: rgba(124,140,248,0.12); color: #7c8cf8; border: 1px solid rgba(124,140,248,0.25); }

.section-header { display: flex; align-items: center; gap: 12px; margin-bottom: 1.25rem; }
.section-icon { width: 34px; height: 34px; border-radius: 8px; display: flex; align-items: center; justify-content: center; font-size: 1rem; }
.section-title { font-size: 0.82rem; font-weight: 600; letter-spacing: 0.1em; text-transform: uppercase; font-family: var(--font-mono); }

.summary-text {
  font-size: 0.95rem; line-height: 1.8; color: var(--text-primary);
  background: var(--bg-secondary); border: 1px solid var(--border-subtle);
  border-radius: 10px; padding: 1.25rem 1.5rem;
}

.chat-wrap { max-height: 420px; overflow-y: auto; display: flex; flex-direction: column; gap: 1rem; padding: 0.25rem; }
.chat-msg { display: flex; gap: 10px; align-items: flex-start; }
.chat-msg.user { flex-direction: row-reverse; }
.avatar { width: 32px; height: 32px; border-radius: 50%; display: flex; align-items: center; justify-content: center; font-size: 0.75rem; flex-shrink: 0; font-weight: 700; }
.avatar-ai   { background: linear-gradient(135deg,#63b3ed,#7c8cf8); color: #0b0f1a; }
.avatar-user { background: linear-gradient(135deg,#b794f4,#fc8181); color: #0b0f1a; }
.bubble { padding: 0.7rem 1rem; border-radius: 14px; max-width: 78%; font-size: 0.88rem; line-height: 1.6; }
.bubble-ai   { background: var(--bg-secondary); border: 1px solid var(--border-subtle); color: var(--text-primary); border-top-left-radius: 3px; }
.bubble-user { background: rgba(99,179,237,0.12); border: 1px solid rgba(99,179,237,0.2); color: var(--text-primary); border-top-right-radius: 3px; }
.chat-time   { font-size: 0.65rem; color: var(--text-muted); font-family: var(--font-mono); margin-top: 3px; display: block; }

/* ALL buttons — proper visible style */
.stButton > button {
  background: #141c2e !important;
  color: #94a3b8 !important;
  border: 1px solid rgba(255,255,255,0.1) !important;
  border-radius: 10px !important;
  font-family: 'DM Sans', sans-serif !important;
  font-weight: 600 !important;
  font-size: 0.88rem !important;
  padding: 0.6rem 1.2rem !important;
  width: 100% !important;
  transition: all 0.2s ease !important;
}
.stButton > button:hover {
  background: rgba(99,179,237,0.1) !important;
  border-color: rgba(99,179,237,0.4) !important;
  color: #63b3ed !important;
}

/* Nav buttons — tall */
div[data-testid="stHorizontalBlock"] .stButton > button {
  height: 80px !important;
  font-size: 1rem !important;
  display: flex !important;
  flex-direction: column !important;
  align-items: center !important;
  justify-content: center !important;
  gap: 4px !important;
  padding: 0.5rem !important;
}

/* Analyze button — primary */
[data-testid="stButton-primary"] > button,
button[kind="primary"] {
  background: linear-gradient(135deg, #1e3a5f, #1a2d4d) !important;
  color: #63b3ed !important;
  border-color: rgba(99,179,237,0.4) !important;
}
[data-testid="stButton-primary"] > button:hover,
button[kind="primary"]:hover {
  background: linear-gradient(135deg, #1e4a7a, #1a3a63) !important;
  color: #ffffff !important;
}

.stTextInput > div > div > input {
  background: var(--bg-secondary) !important;
  border: 1px solid var(--border-subtle) !important;
  border-radius: 10px !important; color: var(--text-primary) !important;
  font-family: var(--font-main) !important;
}
.stTextInput > div > div > input:focus { border-color: #63b3ed !important; }
.stTextInput label, .stSelectbox label { color: var(--text-secondary) !important; font-size: 0.85rem !important; }

.stSelectbox > div > div {
  background: var(--bg-secondary) !important;
  border: 1px solid var(--border-subtle) !important;
  border-radius: 10px !important; color: var(--text-primary) !important;
}

[data-testid="stFileUploader"] {
  border: 2px dashed rgba(99,179,237,0.25) !important;
  border-radius: 14px !important; background: rgba(99,179,237,0.03) !important;
}

.stProgress > div > div > div > div { background: linear-gradient(90deg, #63b3ed, #7c8cf8) !important; }
.stTabs [data-baseweb="tab-list"] { background: var(--bg-secondary) !important; border-radius: 10px !important; padding: 4px !important; }
.stTabs [data-baseweb="tab"] { background: transparent !important; color: var(--text-secondary) !important; border-radius: 8px !important; }
.stTabs [aria-selected="true"] { background: var(--bg-card) !important; color: #63b3ed !important; }
.stTabs [data-baseweb="tab-border"] { display: none !important; }

::-webkit-scrollbar { width: 5px; }
::-webkit-scrollbar-track { background: var(--bg-primary); }
::-webkit-scrollbar-thumb { background: #2d3748; border-radius: 3px; }
</style>
""", unsafe_allow_html=True)

# ── Session state ──────────────────────────────────────────────────────────────
if "result"       not in st.session_state: st.session_state.result       = None
if "chat_history" not in st.session_state: st.session_state.chat_history = []
if "rag_chain"    not in st.session_state: st.session_state.rag_chain    = None
if "error_msg"    not in st.session_state: st.session_state.error_msg    = None
if "active_tab"   not in st.session_state: st.session_state.active_tab   = "Summary"

# ══════════════════════════════════════════════════════════════════════════════
#  HELPERS
# ══════════════════════════════════════════════════════════════════════════════
def clean_text(t):
    t = re.sub(r'\*{1,3}(.*?)\*{1,3}', r'\1', t)
    t = re.sub(r'#+\s*', '', t)
    t = re.sub(r'`{1,3}', '', t)
    t = re.sub(r'_{1,2}(.*?)_{1,2}', r'\1', t)
    t = re.sub(r'\[(.*?)\]\(.*?\)', r'\1', t)
    return t.strip()

def parse_sections(raw, max_points=8):
    lines = raw.strip().splitlines()
    sections, current_title, current_points = [], None, []
    bullet_re = re.compile(r'^[\s]*[-•*]\s+|^\s*\d+[.)]\s+')
    for line in lines:
        line = line.strip()
        if not line: continue
        is_header = bool(re.match(r'^#{1,4}\s+', line)) or \
                    bool(re.match(r'^\*{2}.+\*{2}$', line)) or \
                    (line.endswith(':') and len(line) < 60 and not bullet_re.match(line))
        if is_header:
            if current_points: sections.append({"title": current_title, "points": current_points})
            current_title, current_points = clean_text(line.rstrip(':')), []
        elif bullet_re.match(line):
            pt = clean_text(re.sub(r'^[\s\-•*\d.)]+', '', line).strip())
            if pt: current_points.append(pt)
        else:
            cleaned = clean_text(line)
            if cleaned and len(cleaned) < 200: current_points.append(cleaned)
    if current_points: sections.append({"title": current_title, "points": current_points})
    seen = set()
    for s in sections:
        unique = []
        for p in s["points"]:
            key = p[:60].lower()
            if key not in seen: seen.add(key); unique.append(p)
        s["points"] = unique[:max_points]
    if not sections:
        pts = [clean_text(l.strip()) for l in raw.splitlines() if l.strip()]
        sections = [{"title": None, "points": pts[:max_points]}]
    return sections

def render_sections(sections, dot_color, max_total=8):
    html, count = "", 0
    for sec in sections:
        if count >= max_total: break
        if sec["title"]:
            html += f'<div style="font-size:0.72rem;font-weight:700;letter-spacing:0.1em;text-transform:uppercase;color:{dot_color};font-family:var(--font-mono);margin:0.85rem 0 0.4rem;padding-bottom:4px;border-bottom:1px solid rgba(255,255,255,0.06);">{sec["title"]}</div>'
        for pt in sec["points"]:
            if count >= max_total: break
            html += f'<div style="display:flex;align-items:baseline;gap:8px;padding:0.32rem 0;border-bottom:1px solid rgba(255,255,255,0.04);"><span style="width:6px;height:6px;border-radius:50%;background:{dot_color};flex-shrink:0;margin-top:6px;display:inline-block;"></span><span style="font-size:0.87rem;line-height:1.5;color:#c8d3e0;">{pt}</span></div>'
            count += 1
    return html, count

# ══════════════════════════════════════════════════════════════════════════════
#  HEADER
# ══════════════════════════════════════════════════════════════════════════════
st.markdown("""
<div style="margin-bottom:2rem;">
  <div style="font-family:'Space Mono',monospace;font-size:0.7rem;color:#4a5568;letter-spacing:0.12em;text-transform:uppercase;margin-bottom:1rem;display:flex;align-items:center;gap:8px;">
    <div style="width:6px;height:6px;background:#63b3ed;border-radius:50%;"></div>
    NexaMind · v1.0 · Meeting Intelligence
  </div>
  <h1 style="font-size:clamp(1.6rem,4vw,2.5rem);font-weight:700;line-height:1.15;letter-spacing:-0.03em;margin:0 0 0.5rem;">
    <span class="grad-text">AI-Powered</span> Meeting Assistant
  </h1>
  <p style="font-size:0.95rem;color:#64748b;margin:0;line-height:1.6;">
    Paste a YouTube link or upload a file — get summary, action items, decisions and chat with it.
  </p>
</div>
""", unsafe_allow_html=True)

# ══════════════════════════════════════════════════════════════════════════════
#  INPUT CARD
# ══════════════════════════════════════════════════════════════════════════════
st.markdown('<div class="nexacard">', unsafe_allow_html=True)
st.markdown('<div class="section-header"><div class="section-icon" style="background:rgba(99,179,237,0.1);">📥</div><span class="section-title" style="color:#63b3ed;">Input Source</span></div>', unsafe_allow_html=True)

tab_upload, tab_url = st.tabs(["📁  Upload File", "🔗  YouTube / URL"])

with tab_upload:
    uploaded_file = st.file_uploader(
        "Drop your video or audio file here",
        type=["mp4", "mp3", "wav", "m4a", "webm", "mkv", "avi"],
        label_visibility="collapsed",
    )
    if uploaded_file:
        st.success(f"✅ {uploaded_file.name} · {uploaded_file.size/1024/1024:.1f} MB")

with tab_url:
    youtube_url = st.text_input(
        "Paste URL",
        placeholder="https://www.youtube.com/watch?v=...",
        label_visibility="collapsed",
        key="yt_url_input",
    )

st.markdown('</div>', unsafe_allow_html=True)

# ── Language + Analyze ────────────────────────────────────────────────────────
c1, c2, c3 = st.columns([2, 2, 1])
with c1:
    language = st.selectbox("🌐 Language", ["english", "hinglish"], key="lang")
with c2:
    st.markdown("<div style='height:28px'></div>", unsafe_allow_html=True)
    run_btn = st.button("🚀  Analyze", use_container_width=True, type="primary")
with c3:
    st.empty()

if st.session_state.error_msg:
    st.error(f"❌ {st.session_state.error_msg}")

# ══════════════════════════════════════════════════════════════════════════════
#  PROCESSING
# ══════════════════════════════════════════════════════════════════════════════
if run_btn:
    source_input, tmp_path = None, None

    if uploaded_file is not None:
        suffix = os.path.splitext(uploaded_file.name)[-1]
        with tempfile.NamedTemporaryFile(delete=False, suffix=suffix) as tmp:
            tmp.write(uploaded_file.read())
            tmp_path = tmp.name
            source_input = tmp_path
    elif st.session_state.get("yt_url_input", "").strip():
        source_input = st.session_state["yt_url_input"].strip()

    if not source_input:
        st.warning("⚠️ Please upload a file or paste a YouTube URL first.")
    else:
        st.session_state.result = None
        st.session_state.chat_history = []
        st.session_state.rag_chain = None
        st.session_state.error_msg = None
        st.session_state.active_tab = "Summary"

        progress_bar = st.progress(0)
        status_box = st.empty()

        def show_status(pct, msg):
            status_box.markdown(f"""
            <div style="padding:0.6rem 1rem;background:rgba(99,179,237,0.06);border:1px solid rgba(99,179,237,0.15);border-radius:10px;font-size:0.85rem;color:#94a3b8;">
              ⚙️ {msg}
            </div>""", unsafe_allow_html=True)
            progress_bar.progress(pct)

        try:
            from dotenv import load_dotenv; load_dotenv()

            show_status(0.08, "Extracting audio…")
            from utilities.audio_precessor import process_audio
            chunks = process_audio(source_input)

            show_status(0.22, "Transcribing speech…")
            from core.transcriber import transcribe_all
            transcript = transcribe_all(chunks, language)

            show_status(0.40, "Generating title…")
            from core.summarizer import generate_title, summarize
            title = generate_title(transcript)

            show_status(0.54, "Summarising…")
            summary = summarize(transcript)

            show_status(0.66, "Extracting action items…")
            from core.extractor import extract_action_items, extract_decision_points, extract_questions
            action_items = extract_action_items(transcript)

            show_status(0.76, "Finding key decisions…")
            decisions = extract_decision_points(transcript)

            show_status(0.84, "Surfacing questions…")
            questions = extract_questions(transcript)

            show_status(0.93, "Building RAG index…")
            from core.rag_engine import build_rag_chain
            rag_chain = build_rag_chain(transcript)

            show_status(1.00, "Done!")

            st.session_state.result = {
                "title": title, "transcript": transcript,
                "summary": summary, "action_items": action_items,
                "key_decisions": decisions, "open_questions": questions,
            }
            st.session_state.rag_chain = rag_chain

        except Exception as e:
            st.session_state.error_msg = str(e)
        finally:
            if tmp_path and os.path.exists(tmp_path):
                os.remove(tmp_path)

        status_box.empty()
        progress_bar.empty()
        st.rerun()

# ══════════════════════════════════════════════════════════════════════════════
#  RESULTS
# ══════════════════════════════════════════════════════════════════════════════
if st.session_state.result:
    r = st.session_state.result

    # Title
    st.markdown(f"""
    <div style="margin:1rem 0 1.5rem;padding:1rem 1.25rem;
                background:linear-gradient(135deg,rgba(99,179,237,0.07),rgba(124,140,248,0.07));
                border:1px solid rgba(99,179,237,0.18);border-radius:12px;">
      <div style="font-size:0.65rem;font-family:'Space Mono',monospace;letter-spacing:0.1em;text-transform:uppercase;color:#4a5568;margin-bottom:4px;">📌 Meeting Title</div>
      <div style="font-size:1.15rem;font-weight:600;color:#e8edf5;">{r['title']}</div>
    </div>
    """, unsafe_allow_html=True)

    # ── Big Nav Buttons ───────────────────────────────────────────────────────
    tabs_config = [
        ("📋", "Summary"),
        ("✅", "Action Items"),
        ("🔑", "Decisions"),
        ("❓", "Questions"),
        ("📜", "Transcript"),
        ("💬", "Chat"),
    ]

    tab_colors = {
        "Summary":      "#63b3ed",
        "Action Items": "#4fd1a5",
        "Decisions":    "#b794f4",
        "Questions":    "#f6ad55",
        "Transcript":   "#94a3b8",
        "Chat":         "#7c8cf8",
    }

    cols = st.columns(6, gap="small")
    for i, (icon, label) in enumerate(tabs_config):
        with cols[i]:
            if st.button(f"{icon}\n{label}", key=f"nav_{label}", use_container_width=True):
                st.session_state.active_tab = label
                st.rerun()

    # Highlight active tab
    active = st.session_state.active_tab
    active_color = tab_colors.get(active, "#63b3ed")
    active_idx = [t[1] for t in tabs_config].index(active)
    highlight_css = f"""
    <style>
    div[data-testid="stHorizontalBlock"] > div:nth-child({active_idx+1}) .stButton > button {{
        border-color: {active_color} !important;
        color: {active_color} !important;
        background: rgba(99,179,237,0.07) !important;
    }}
    </style>
    """
    st.markdown(highlight_css, unsafe_allow_html=True)

    st.markdown("<div style='margin-top:1.25rem'></div>", unsafe_allow_html=True)

    # ── Content ───────────────────────────────────────────────────────────────
    if active == "Summary":
        st.markdown('<div class="nexacard"><div class="section-header"><div class="section-icon" style="background:rgba(99,179,237,0.1);">📋</div><span class="section-title" style="color:#63b3ed;">Summary</span><span class="pill pill-cyan" style="margin-left:auto;">Auto-generated</span></div>', unsafe_allow_html=True)
        st.markdown(f'<div class="summary-text">{r["summary"]}</div>', unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)

    elif active == "Action Items":
        act_sections = parse_sections(r["action_items"], max_points=10)
        act_html, n_act = render_sections(act_sections, "#4fd1a5", 10)
        st.markdown(f'<div class="nexacard"><div class="section-header"><div class="section-icon" style="background:rgba(79,209,165,0.1);">✅</div><span class="section-title" style="color:#4fd1a5;">Action Items</span><span class="pill pill-emerald" style="margin-left:auto;">{n_act} tasks</span></div>{act_html}</div>', unsafe_allow_html=True)

    elif active == "Decisions":
        dec_sections = parse_sections(r["key_decisions"], max_points=10)
        dec_html, n_dec = render_sections(dec_sections, "#b794f4", 10)
        st.markdown(f'<div class="nexacard"><div class="section-header"><div class="section-icon" style="background:rgba(183,148,244,0.1);">🔑</div><span class="section-title" style="color:#b794f4;">Key Decisions</span><span class="pill pill-violet" style="margin-left:auto;">{n_dec} items</span></div>{dec_html}</div>', unsafe_allow_html=True)

    elif active == "Questions":
        q_sections = parse_sections(r["open_questions"], max_points=10)
        q_html, n_q = render_sections(q_sections, "#f6ad55", 10)
        st.markdown(f'<div class="nexacard"><div class="section-header"><div class="section-icon" style="background:rgba(246,173,85,0.1);">❓</div><span class="section-title" style="color:#f6ad55;">Open Questions</span><span class="pill pill-amber" style="margin-left:auto;">{n_q} shown</span></div>{q_html}</div>', unsafe_allow_html=True)

    elif active == "Transcript":
        st.markdown('<div class="nexacard"><div class="section-header"><div class="section-icon" style="background:rgba(148,163,184,0.1);">📜</div><span class="section-title" style="color:#94a3b8;">Full Transcript</span></div>', unsafe_allow_html=True)
        st.markdown(f'<div style="font-family:\'Space Mono\',monospace;font-size:0.78rem;line-height:1.9;color:#94a3b8;padding:1rem;background:#111827;border-radius:10px;max-height:520px;overflow-y:auto;white-space:pre-wrap;">{r["transcript"]}</div>', unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)

    elif active == "Chat":
        st.markdown('<div class="nexacard"><div class="section-header"><div class="section-icon" style="background:rgba(124,140,248,0.1);">💬</div><span class="section-title" style="color:#7c8cf8;">Chat with Your Meeting</span><span class="pill pill-indigo" style="margin-left:auto;">RAG · AI</span></div>', unsafe_allow_html=True)

        if st.session_state.chat_history:
            bubble_html = ""
            for msg in st.session_state.chat_history:
                ts = msg.get("time", "")
                if msg["role"] == "user":
                    bubble_html += f'<div class="chat-msg user"><div class="avatar avatar-user">You</div><div><div class="bubble bubble-user">{msg["content"]}</div><span class="chat-time" style="text-align:right;display:block;">{ts}</span></div></div>'
                else:
                    bubble_html += f'<div class="chat-msg"><div class="avatar avatar-ai">AI</div><div><div class="bubble bubble-ai">{msg["content"]}</div><span class="chat-time">{ts}</span></div></div>'
            st.markdown(f'<div class="chat-wrap">{bubble_html}</div>', unsafe_allow_html=True)
        else:
            st.markdown('<div style="text-align:center;padding:2rem;color:#4a5568;"><div style="font-size:2rem;margin-bottom:8px;">🤖</div><div style="font-size:0.85rem;">Ask anything about this meeting.</div></div>', unsafe_allow_html=True)

        st.markdown('</div>', unsafe_allow_html=True)

        cc, sc = st.columns([6, 1])
        with cc:
            user_input = st.text_input("Q", placeholder="e.g. What were the main decisions?", label_visibility="collapsed", key="chat_input")
        with sc:
            send_btn = st.button("Send ➤", use_container_width=True)

        if send_btn and user_input.strip():
            ts = datetime.datetime.now().strftime("%H:%M")
            st.session_state.chat_history.append({"role": "user", "content": user_input.strip(), "time": ts})
            with st.spinner("Thinking…"):
                try:
                    from core.rag_engine import ask_question
                    answer = ask_question(st.session_state.rag_chain, user_input.strip())
                except Exception as e:
                    answer = f"⚠️ Error: {e}"
            st.session_state.chat_history.append({"role": "assistant", "content": answer, "time": ts})
            st.rerun()

# Footer
st.markdown('<div style="text-align:center;padding:3rem 0 1rem;font-size:0.7rem;color:#2d3748;font-family:\'Space Mono\',monospace;letter-spacing:0.06em;">NEXAMIND · MEETING INTELLIGENCE · BUILT WITH STREAMLIT</div>', unsafe_allow_html=True)