# News Video Studio

**News Video Studio** is an AI-powered automated video generator built with Python and Streamlit. It fetches trending news headlines, uses GPT-4o to draft a viral-style script, creates a voiceover, and stitches everything into a professional 30-second vertical video suitable for Shorts, Reels, or TikTok.

## Features

* **Live News Integration:** Fetches top 10 trending stories in real-time using [NewsAPI](https://newsapi.org/).
* **AI Scripting:** Uses **OpenAI GPT-4o** to generate concise, dramatic, factual scripts (approx. 60 words).
* **Auto-Narration:** Generates professional voiceovers using Google Text-to-Speech (gTTS).
* **Video Compositing:** Automatically assembles background, article thumbnails, headlines, and captions using **MoviePy**.
* **Interactive UI:** Clean, professional interface built with **Streamlit**.

## Prerequisites

Before running the application, ensure you have the following installed:

1.  **Python 3.8+**
2.  **ImageMagick:** Required for MoviePy to render text.
    * *Download:* [ImageMagick for Windows](https://imagemagick.org/script/download.php#windows)
    * *Important:* During installation, check the box **"Install legacy utilities (e.g. convert)"**.
3.  **API Keys:**
    * **OpenAI API Key** (for script generation).
    * **NewsAPI Key** (for fetching headlines).

## Installation

1.  **Clone the repository** (or save your script):
    ```bash
    git clone [https://github.com/AbhishekAwasthi565/NewsFlow-AI](https://github.com/AbhishekAwasthi565/NewsFlow-AI)
    cd NewsFlow-AI-main
    ```

2.  **Install Python Dependencies:**
    Create a `requirements.txt` file or run the following command directly:
    ```bash
    pip install streamlit moviepy requests gtts openai
    ```

## Configuration (Crucial Step)

Because the code uses absolute file paths for Windows, you **must** verify the following paths in your Python file match your system:

1.  **ImageMagick Path:**
    Look for this line in the code and ensure it points to your `magick.exe`:
    ```python
    os.environ["IMAGEMAGICK_BINARY"] = r"C:\Program Files\ImageMagick-7.1.1-Q16-HDRI\magick.exe"
    ```

2.  **Font Path:**
    Look for this line and ensure the font exists:
    ```python
    FONT_PATH = r"C:\Windows\Fonts\arial.ttf"
    ```
    *(If you are on Mac/Linux, change this to a valid system font path).*

## Usage

1.  **Run the App:**
    ```bash
    streamlit run app.py
    ```

2.  **Navigate the UI:**
    * Open your browser (usually `http://localhost:8501`).
    * **Sidebar:** Enter your **NewsAPI Key** and **OpenAI API Key**.
    * **Step 1:** Click **Fetch Top 10 Headlines**.
    * **Step 2:** Select a story from the dropdown menu.
    * **Step 3:** Click **Create 30s Video**.

3.  **Result:**
    * The app will display the generated video.
    * You can download the MP4 file directly.
    * The generated script is displayed for review.

## Project Structure

```text
news-video-studio/
│
├── app.py              # Main application source code
├── outputs/            # Generated assets (mp3, jpg, mp4)
│   ├── voice.mp3
│   ├── news_thumb.jpg
│   └── studio_output.mp4
└── README.md           # Documentation
