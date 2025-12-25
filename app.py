import streamlit as st
import os, requests, textwrap, time
from gtts import gTTS
from openai import OpenAI
from moviepy import AudioFileClip, TextClip, CompositeVideoClip, ImageClip, ColorClip

# --- 1. SETUP & STYLE ---
st.set_page_config(page_title="News Video Studio", layout="centered")

# Professional clean UI (No AI stickers)
st.markdown("""
    <style>
    .stButton>button { width: 100%; border-radius: 8px; height: 3em; background-color: #007BFF; color: white; }
    .stSelectbox label { font-weight: bold; font-size: 18px; }
    </style>
    """, unsafe_allow_html=True)

# Important Paths
os.environ["IMAGEMAGICK_BINARY"] = r"C:\Program Files\ImageMagick-7.1.1-Q16-HDRI\magick.exe"
FONT_PATH = r"C:\Windows\Fonts\arial.ttf"
OUTPUT_DIR = "outputs"
os.makedirs(OUTPUT_DIR, exist_ok=True)

# --- 2. THE LOGIC ---

def load_top_stories(api_key):
    """Fetches the top 10 trending articles."""
    url = f"https://newsapi.org/v2/top-headlines?language=en&pageSize=10&apiKey={api_key}"
    try:
        r = requests.get(url).json()
        return r.get("articles", [])
    except:
        return []

def render_final_video(script, image_url, progress_bar):
    """Handles the heavy lifting of video creation."""
    # Voice
    progress_bar.progress(40, text=" Recording professional narration...")
    audio_path = os.path.join(OUTPUT_DIR, "voice.mp3")
    gTTS(script).save(audio_path)
    audio = AudioFileClip(audio_path)
    
    # Duration Lock (Target ~30s)
    MASTER_DUR = audio.duration
    progress_bar.progress(60, text=f" Designing {int(MASTER_DUR)}s video...")

    # Background
    bg = ColorClip(size=(720, 1280), color=(20, 20, 20)).with_duration(MASTER_DUR)
    clips = [bg]

    # Main Image
    if image_url:
        try:
            img_data = requests.get(image_url, timeout=5).content
            img_path = os.path.join(OUTPUT_DIR, "news_thumb.jpg")
            with open(img_path, "wb") as f: f.write(img_data)
            
            img = ImageClip(img_path).resized(width=680).with_position(("center", 280)).with_duration(MASTER_DUR)
            clips.append(img)
        except: pass

    # Professional Overlays
    header = TextClip(text="BREAKING NEWS", font=FONT_PATH, font_size=80, color="white", bg_color="red"
                     ).with_position(("center", 140)).with_duration(MASTER_DUR)
    
    wrapped = textwrap.fill(script, width=30)
    caption = TextClip(text=wrapped, font=FONT_PATH, font_size=42, color="yellow"
                      ).with_position(("center", 920)).with_duration(MASTER_DUR)
    
    clips.extend([header, caption])

    # Export
    progress_bar.progress(85, text=" Finalizing high-quality MP4...")
    final = CompositeVideoClip(clips).with_audio(audio)
    out_path = os.path.join(OUTPUT_DIR, "studio_output.mp4")
    final.write_videofile(out_path, fps=24, codec="libx264", logger=None)
    
    final.close()
    audio.close()
    return out_path

# --- 3. THE INTERFACE ---

st.title(" News Video Studio")
st.write("Fetch headlines, select a story, and generate a 30-second news reel.")

# Sidebar Keys
with st.sidebar:
    st.header("Setup")
    n_key = st.text_input("NewsAPI Key", type="password")
    o_key = st.text_input("OpenAI Key", type="password")

# Initialization of Session State
if 'news_list' not in st.session_state:
    st.session_state.news_list = []

# Step 1: Fetch News
if st.button(" Step 1: Fetch Top 10 Headlines"):
    if not n_key:
        st.error("Enter NewsAPI key first!")
    else:
        with st.spinner("Scanning world news..."):
            st.session_state.news_list = load_top_stories(n_key)
            if st.session_state.news_list:
                st.success(f"Found {len(st.session_state.news_list)} trending stories!")
            else:
                st.error("No news found. Check your API key.")

# Step 2: Select News
if st.session_state.news_list:
    titles = [a.get('title') for a in st.session_state.news_list]
    selected_title = st.selectbox(" Step 2: Choose your story", options=titles)
    
    # Get the full article data for the selection
    selected_article = next(a for a in st.session_state.news_list if a.get('title') == selected_title)
    
    # Step 3: Generate Video
    if st.button(" Step 3: Create 30s Video"):
        if not o_key:
            st.error("Enter OpenAI key first!")
        else:
            status = st.progress(0, text="Initializing AI...")
            
            # 1. AI Script (Strict 75-80 words for 30 seconds)
            status.progress(20, text=" Drafting concise news script...")
            client = OpenAI(api_key=o_key)
            prompt = f"Write a 60-word professional news script for: {selected_title}. Focus on the facts. Dramatic tone."
            
            res = client.chat.completions.create(
                model="gpt-4o-mini",
                messages=[{"role": "user", "content": prompt}]
            )
            script = res.choices[0].message.content.strip()
            
            # 2. Render
            video_url = render_final_video(script, selected_article.get("urlToImage"), status)
            
            status.progress(100, text="✨ Production Complete!")
            time.sleep(1)
            status.empty()
            
            # Show Results
            st.divider()
            col1, col2 = st.columns(2)
            with col1:
                st.video(video_url)
                st.download_button(" Download MP4", open(video_url, "rb"), "news_broadcast.mp4")
            with col2:
                st.subheader("Broadcast Script")
                st.info(script)
                st.write(f"⏱ **Length:** ~30s |  **Words:** {len(script.split())}")