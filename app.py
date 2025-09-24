import streamlit as st
import pandas as pd
import re
from collections import Counter
from textblob import TextBlob
from wordcloud import WordCloud
import matplotlib.pyplot as plt
import time
import base64
import io

# -------------------------------
# Custom CSS for Ultra Modern UI
# -------------------------------

def inject_custom_css():
    st.markdown("""
    <style>
    /* Modern Color Palette */
    :root {
        --primary-gradient: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        --secondary-gradient: linear-gradient(135deg, #f093fb 0%, #f5576c 100%);
        --accent-gradient: linear-gradient(135deg, #4facfe 0%, #00f2fe 100%);
        --success-gradient: linear-gradient(135deg, #43e97b 0%, #38f9d7 100%);
        --warning-gradient: linear-gradient(135deg, #fa709a 0%, #fee140 100%);
        --dark-gradient: linear-gradient(135deg, #0c0c0c 0%, #1a1a2e 50%, #16213e 100%);
        --card-gradient: linear-gradient(135deg, rgba(255,255,255,0.1) 0%, rgba(255,255,255,0.05) 100%);
        --dark-bg: #0a0a0a;
        --darker-bg: #050505;
        --card-bg: rgba(30, 30, 46, 0.7);
        --card-hover: rgba(40, 40, 60, 0.8);
        --accent-color: #64ffda;
        --text-primary: #f0f0f0;
        --text-secondary: #a0a0c0;
        --success-color: #00d4aa;
        --warning-color: #ffb74d;
        --error-color: #ff6b6b;
        --shadow-lg: 0 25px 50px rgba(0, 0, 0, 0.5);
        --shadow-md: 0 15px 30px rgba(0, 0, 0, 0.4);
        --shadow-sm: 0 8px 20px rgba(0, 0, 0, 0.3);
        --border-radius: 16px;
        --border-radius-sm: 12px;
    }
    
    /* Main app styling */
    .stApp {
        background: var(--dark-gradient);
        color: var(--text-primary);
        font-family: 'Inter', 'Segoe UI', system-ui, sans-serif;
        min-height: 100vh;
    }
    
    /* Modern header with animated gradient */
    .main-header {
        font-size: 4rem;
        font-weight: 900;
        background: linear-gradient(45deg, #ff6b6b, #feca57, #48dbfb, #ff9ff3, #ff6b6b);
        background-size: 400% 400%;
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
        margin-bottom: 0.5rem;
        text-align: center;
        padding: 1rem 0;
        letter-spacing: -1px;
        animation: gradientShift 8s ease infinite;
        position: relative;
        text-shadow: 0 0 30px rgba(255, 107, 107, 0.3);
    }
    
    @keyframes gradientShift {
        0% { background-position: 0% 50% }
        50% { background-position: 100% 50% }
        100% { background-position: 0% 50% }
    }
    
    .sub-header {
        font-size: 1.5rem;
        color: var(--text-secondary);
        margin-bottom: 3rem;
        text-align: center;
        line-height: 1.6;
        font-weight: 400;
        max-width: 800px;
        margin-left: auto;
        margin-right: auto;
        background: linear-gradient(135deg, var(--text-primary) 0%, var(--text-secondary) 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
        padding: 0 2rem;
    }
    
    /* Glass morphism cards with improved styling */
    .card {
        background: var(--card-gradient);
        backdrop-filter: blur(25px);
        border: 1px solid rgba(255, 255, 255, 0.15);
        padding: 2.5rem;
        border-radius: var(--border-radius);
        box-shadow: var(--shadow-lg);
        margin-bottom: 2rem;
        transition: all 0.4s cubic-bezier(0.175, 0.885, 0.32, 1.275);
        position: relative;
        overflow: hidden;
    }
    
    .card::before {
        content: '';
        position: absolute;
        top: 0;
        left: -100%;
        width: 100%;
        height: 100%;
        background: linear-gradient(90deg, transparent, rgba(255, 255, 255, 0.1), transparent);
        transition: left 0.8s;
    }
    
    .card:hover::before {
        left: 100%;
    }
    
    .card:hover {
        transform: translateY(-8px);
        box-shadow: var(--shadow-lg), 0 0 40px rgba(102, 126, 234, 0.3);
        border-color: rgba(102, 126, 234, 0.4);
    }
    
    /* Modern buttons with improved gradient */
    .stButton button {
        background: var(--primary-gradient);
        color: white;
        border: none;
        padding: 1.2rem 2.5rem;
        border-radius: 50px;
        font-weight: 700;
        transition: all 0.4s cubic-bezier(0.175, 0.885, 0.32, 1.275);
        width: 100%;
        font-size: 1.1rem;
        position: relative;
        overflow: hidden;
        letter-spacing: 0.5px;
        box-shadow: var(--shadow-md);
        backdrop-filter: blur(10px);
    }
    
    .stButton button::before {
        content: '';
        position: absolute;
        top: 0;
        left: -100%;
        width: 100%;
        height: 100%;
        background: linear-gradient(90deg, transparent, rgba(255, 255, 255, 0.2), transparent);
        transition: left 0.6s;
    }
    
    .stButton button:hover::before {
        left: 100%;
    }
    
    .stButton button:hover {
        transform: translateY(-3px);
        box-shadow: 0 15px 30px rgba(102, 126, 234, 0.4);
    }
    
    /* Enhanced keyword grid with modern buttons */
    .keyword-grid {
        display: grid;
        grid-template-columns: repeat(auto-fill, minmax(150px, 1fr));
        gap: 15px;
        margin-top: 25px;
    }
    
    .keyword-btn {
        background: var(--card-gradient);
        backdrop-filter: blur(15px);
        border: 1px solid rgba(255, 255, 255, 0.1);
        border-radius: 12px;
        padding: 1.2rem 1rem;
        text-align: center;
        transition: all 0.3s ease;
        cursor: pointer;
        box-shadow: var(--shadow-sm);
        display: flex;
        flex-direction: column;
        justify-content: center;
        align-items: center;
        height: 80px;
        position: relative;
        overflow: hidden;
    }
    
    .keyword-btn::before {
        content: '';
        position: absolute;
        top: 0;
        left: -100%;
        width: 100%;
        height: 100%;
        background: linear-gradient(90deg, transparent, rgba(255, 255, 255, 0.1), transparent);
        transition: left 0.5s;
    }
    
    .keyword-btn:hover::before {
        left: 100%;
    }
    
    .keyword-btn:hover {
        transform: translateY(-5px) scale(1.03);
        box-shadow: 0 10px 25px rgba(0, 0, 0, 0.3);
    }
    
    .keyword-btn.high {
        border-left: 4px solid #ff6b6b;
        background: linear-gradient(135deg, rgba(255, 107, 107, 0.15), rgba(255, 107, 107, 0.05));
    }
    
    .keyword-btn.medium {
        border-left: 4px solid #feca57;
        background: linear-gradient(135deg, rgba(254, 202, 87, 0.15), rgba(254, 202, 87, 0.05));
    }
    
    .keyword-btn.low {
        border-left: 4px solid #48dbfb;
        background: linear-gradient(135deg, rgba(72, 219, 251, 0.15), rgba(72, 219, 251, 0.05));
    }
    
    .keyword-btn .word {
        font-size: 1.1rem;
        font-weight: 800;
        margin-bottom: 5px;
        color: var(--text-primary);
    }
    
    .keyword-btn .count {
        font-size: 0.9rem;
        font-weight: 600;
        opacity: 0.8;
    }
    
    .keyword-btn.high .word { color: #ff6b6b; }
    .keyword-btn.medium .word { color: #feca57; }
    .keyword-btn.low .word { color: #48dbfb; }
    
    /* Scrollable containers */
    .scroll-container {
        max-height: 600px;
        overflow-y: auto;
        padding: 1.5rem;
        border-radius: var(--border-radius-sm);
        background: rgba(30, 30, 46, 0.5);
        border: 1px solid rgba(255, 255, 255, 0.1);
        backdrop-filter: blur(20px);
    }
    
    /* Custom scrollbar */
    .scroll-container::-webkit-scrollbar {
        width: 8px;
    }
    
    .scroll-container::-webkit-scrollbar-track {
        background: rgba(30, 30, 46, 0.5);
        border-radius: 10px;
    }
    
    .scroll-container::-webkit-scrollbar-thumb {
        background: var(--primary-gradient);
        border-radius: 10px;
    }
    
    /* Enhanced sentiment badges */
    .sentiment-badge {
        font-weight: 700;
        padding: 0.6rem 1.2rem;
        border-radius: 25px;
        display: inline-block;
        font-size: 0.9rem;
        backdrop-filter: blur(15px);
        border: 2px solid;
        text-transform: uppercase;
        letter-spacing: 1px;
        box-shadow: var(--shadow-sm);
    }
    
    .positive {
        background: linear-gradient(135deg, rgba(16, 185, 129, 0.25), rgba(16, 185, 129, 0.15));
        color: #10b981;
        border-color: rgba(16, 185, 129, 0.4);
    }
    
    .neutral {
        background: linear-gradient(135deg, rgba(245, 158, 11, 0.25), rgba(245, 158, 11, 0.15));
        color: #f59e0b;
        border-color: rgba(245, 158, 11, 0.4);
    }
    
    .negative {
        background: linear-gradient(135deg, rgba(239, 68, 68, 0.25), rgba(239, 68, 68, 0.15));
        color: #ef4444;
        border-color: rgba(239, 68, 68, 0.4);
    }
    
    /* Modern comment items */
    .comment-item {
        padding: 1.8rem;
        margin: 1.5rem 0;
        background: rgba(30, 30, 46, 0.6);
        border-radius: var(--border-radius-sm);
        border-left: 4px solid var(--accent-color);
        box-shadow: var(--shadow-sm);
        transition: all 0.4s cubic-bezier(0.175, 0.885, 0.32, 1.275);
        position: relative;
        overflow: hidden;
        backdrop-filter: blur(15px);
        border: 1px solid rgba(255, 255, 255, 0.1);
    }
    
    .comment-item::before {
        content: '';
        position: absolute;
        top: 0;
        left: -100%;
        width: 100%;
        height: 100%;
        background: linear-gradient(90deg, transparent, rgba(255, 255, 255, 0.05), transparent);
        transition: left 0.6s;
    }
    
    .comment-item:hover::before {
        left: 100%;
    }
    
    .comment-item:hover {
        transform: translateY(-3px);
        box-shadow: var(--shadow-md);
        background: rgba(30, 30, 46, 0.8);
        border-color: rgba(102, 126, 234, 0.3);
    }
    
    /* Enhanced metric cards */
    .metric-card {
        background: var(--card-gradient);
        color: white;
        padding: 2rem 1.5rem;
        border-radius: var(--border-radius);
        text-align: center;
        margin: 0.8rem;
        height: 150px;
        display: flex;
        flex-direction: column;
        justify-content: center;
        align-items: center;
        box-shadow: var(--shadow-md);
        transition: all 0.4s cubic-bezier(0.175, 0.885, 0.32, 1.275);
        border: 1px solid rgba(255, 255, 255, 0.1);
        backdrop-filter: blur(15px);
        position: relative;
        overflow: hidden;
    }
    
    .metric-card::before {
        content: '';
        position: absolute;
        top: -50%;
        left: -50%;
        width: 200%;
        height: 200%;
        background: linear-gradient(45deg, transparent, rgba(255, 255, 255, 0.05), transparent);
        transform: rotate(45deg);
        transition: all 0.6s;
    }
    
    .metric-card:hover::before {
        transform: rotate(45deg) translate(50%, 50%);
    }
    
    .metric-card:hover {
        transform: translateY(-5px);
        box-shadow: var(--shadow-lg), 0 0 30px rgba(102, 126, 234, 0.2);
        border-color: rgba(102, 126, 234, 0.3);
    }
    
    .metric-card h3 {
        font-size: 1rem;
        margin: 0;
        opacity: 0.9;
        font-weight: 600;
        color: var(--text-secondary);
        letter-spacing: 0.5px;
    }
    
    .metric-card h2 {
        font-size: 2.8rem;
        margin: 0.8rem 0 0 0;
        font-weight: 800;
        background: var(--primary-gradient);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
    }
    
    /* Section headers */
    .section-header {
        font-size: 2rem;
        font-weight: 800;
        background: var(--primary-gradient);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
        margin-bottom: 1.5rem;
        padding-bottom: 0.8rem;
        border-bottom: 2px solid rgba(102, 126, 234, 0.3);
        letter-spacing: -0.5px;
    }
    
    /* Tab styling */
    .stTabs [data-baseweb="tab-list"] {
        gap: 1rem;
        background: rgba(30, 30, 46, 0.6);
        padding: 0.8rem;
        border-radius: var(--border-radius-sm);
        border: 1px solid rgba(255, 255, 255, 0.1);
        backdrop-filter: blur(20px);
    }
    
    .stTabs [data-baseweb="tab"] {
        background: transparent;
        border-radius: var(--border-radius-sm);
        padding: 1rem 2rem;
        color: var(--text-secondary);
        font-weight: 700;
        transition: all 0.4s cubic-bezier(0.175, 0.885, 0.32, 1.275);
        border: 1px solid transparent;
        letter-spacing: 0.5px;
    }
    
    .stTabs [aria-selected="true"] {
        background: var(--primary-gradient);
        color: white;
        box-shadow: var(--shadow-md);
        border: 1px solid rgba(102, 126, 234, 0.3);
    }
    
    /* Progress bar styling */
    .stProgress > div > div > div > div {
        background: var(--primary-gradient);
        border-radius: 10px;
    }
    
    /* Download button special styling */
    .download-btn {
        background: var(--success-gradient) !important;
    }
    
    .reset-btn {
        background: var(--warning-gradient) !important;
    }
    
    /* Empty state enhancements */
    .empty-state {
        text-align: center;
        padding: 4rem 2rem;
        background: rgba(30, 30, 46, 0.6);
        border-radius: var(--border-radius);
        border: 2px dashed rgba(102, 126, 234, 0.4);
        color: var(--text-secondary);
        backdrop-filter: blur(20px);
        margin: 2rem 0;
    }
    
    /* Enhanced animations */
    @keyframes float {
        0%, 100% { transform: translateY(0px); }
        50% { transform: translateY(-10px); }
    }
    
    @keyframes pulse {
        0%, 100% { transform: scale(1); }
        50% { transform: scale(1.05); }
    }
    
    .floating {
        animation: float 3s ease-in-out infinite;
    }
    
    .pulse {
        animation: pulse 2s ease-in-out infinite;
    }
    
    /* Enhanced loading animation */
    .loading-container {
        position: fixed;
        bottom: 0;
        left: 0;
        width: 100%;
        background: rgba(10, 10, 15, 0.95);
        padding: 1.5rem;
        border-top: 2px solid rgba(102, 126, 234, 0.4);
        z-index: 1000;
        backdrop-filter: blur(25px);
        box-shadow: 0 -5px 20px rgba(0, 0, 0, 0.5);
    }
    
    .loading-step {
        display: flex;
        align-items: center;
        margin: 1rem 0;
        color: var(--text-primary);
        font-size: 1.1rem;
        font-weight: 600;
    }
    
    .loading-icon {
        margin-right: 1rem;
        font-size: 1.3rem;
        width: 25px;
        text-align: center;
        animation: pulse 1.5s ease-in-out infinite;
    }
    
    .loading-bar {
        height: 6px;
        background: rgba(102, 126, 234, 0.3);
        border-radius: 3px;
        margin-top: 0.8rem;
        overflow: hidden;
    }
    
    .loading-progress {
        height: 100%;
        background: var(--primary-gradient);
        border-radius: 3px;
        transition: width 0.4s ease;
    }
    
    /* File uploader styling */
    .stFileUploader {
        background: rgba(30, 30, 46, 0.6);
        border-radius: var(--border-radius-sm);
        padding: 2rem;
        border: 2px dashed rgba(102, 126, 234, 0.4);
        backdrop-filter: blur(15px);
    }
    
    /* Enhanced word cloud container */
    .wordcloud-container {
        background: rgba(30, 30, 46, 0.6);
        border-radius: var(--border-radius);
        padding: 1.5rem;
        border: 1px solid rgba(102, 126, 234, 0.3);
        backdrop-filter: blur(20px);
        box-shadow: var(--shadow-md);
    }
    
    /* Responsive improvements */
    @media (max-width: 768px) {
        .main-header {
            font-size: 2.5rem;
        }
    
        .metric-card {
            padding: 1.5rem 1rem;
            height: 120px;
            margin: 0.5rem;
        }
    
        .metric-card h2 {
            font-size: 2.2rem;
        }
    
        .loading-container {
            padding: 1rem;
        }
    
        .section-header {
            font-size: 1.5rem;
        }
    
        .keyword-grid {
            grid-template-columns: repeat(auto-fill, minmax(120px, 1fr));
        }
    }
    </style>
    """, unsafe_allow_html=True)

# -------------------------------
# Utility Functions
# -------------------------------

def create_sample_data():
    """Create a larger and more varied sample data for demonstration"""
    comments = [
        "I really love this product! It's absolutely fantastic and exceeded my expectations.",
        "She is very kind and helpful. The customer service was exceptional throughout.",
        "This is just amazing, I am impressed with the quality and attention to detail.",
        "He was not happy with the service. The delivery was delayed without any notification.",
        "They are doing a great job with the new updates. The interface is much more user-friendly now.",
        "The movie was very boring and too long. I wouldn't recommend it to anyone.",
        "I think it could have been better with more features and better performance.",
        "We are going to the park tomorrow. The weather forecast looks perfect for outdoor activities.",
        "This phone is really fast and smooth. The battery life is impressive compared to previous models.",
        "It was an unnecessary delay in delivery. The communication could have been much better.",
        "Excellent service and quick response time. Highly recommended for anyone looking for quality.",
        "The product arrived damaged and the return process was complicated.",
        "Outstanding customer support! They went above and beyond to help me.",
        "Average experience, nothing special but also nothing terrible.",
        "The quality is exceptional and the price is very reasonable for what you get.",
        "The customer service was dreadful, and the staff were rude. I will not be returning.",
        "I was quite disappointed with the result. It didn't meet the standards promised.",
        "The app is easy to use, but the constant crashes are a major problem.",
        "A positive experience overall, but the shipping was slower than expected.",
        "This is a great tool for our team. The collaboration features are top-notch.",
        "The food was delicious, but the portion sizes were way too small for the price.",
        "The support team was quick to resolve my issue. Very satisfied.",
        "This product is a total game-changer. The innovation is truly remarkable.",
        "Not what I expected. The quality is subpar and the design is outdated.",
        "The new update is buggy and has made the system very difficult to navigate.",
        "The website is so easy to use. I found what I needed in seconds.",
        "The delivery was incredibly fast and the packaging was excellent. Highly satisfied.",
        "I experienced some bugs after the latest update. It has become quite unstable.",
        "The staff were polite and resolved my issue quickly. Great experience.",
        "Poor quality material and the color was not as advertised. Very disappointing.",
        "This is my favorite app. The user interface is intuitive and efficient.",
        "The price is a bit high for what you get, but the performance is unmatched.",
        "I had a terrible experience with customer support. They were not helpful at all.",
        "The product is fine, but the shipping cost was exorbitant. I won't order again.",
        "They are very responsive to feedback and keep improving the product.",
        "The design is sleek and modern. It looks fantastic on my desk.",
        "The service was slow, and the food was cold. Definitely not a good experience.",
        "I am so impressed with the quality and durability. This product will last for years.",
        "The installation was a nightmare. The instructions were confusing and incomplete.",
        "This is a brilliant solution to a common problem. I wish I had found it sooner.",
        "I'm disappointed with the battery life. It drains much faster than expected.",
        "The new features are great, but the overall speed has decreased significantly.",
        "Customer service was rude and unhelpful. They didn't listen to my problem.",
        "The product arrived late and there was no tracking information available.",
        "I was expecting more for the price. It's an okay product, but nothing special.",
        "Excellent value for money. The features are top-tier for this price range.",
        "The company is very transparent and communicates clearly with their customers.",
        "The performance is not as good as promised. I've had many issues with it.",
        "This is a wonderful addition to my collection. The craftsmanship is beautiful.",
        "I'm so frustrated with the constant glitches. It's a waste of my time.",
        "The product is outstanding! I have no complaints at all.",
        "The delivery was incredibly fast and the packaging was excellent. Highly satisfied.",
        "This is a great tool for our team. The collaboration features are top-notch.",
        "The support team was quick to resolve my issue. Very satisfied.",
        "Outstanding customer support! They went above and beyond to help me.",
        "The food was delicious, but the portion sizes were way too small for the price.",
        "The new update is buggy and has made the system very difficult to navigate.",
        "The installation was a nightmare. The instructions were confusing and incomplete.",
        "The website is so easy to use. I found what I needed in seconds.",
        "Poor quality material and the color was not as advertised. Very disappointing.",
        "The performance is not as good as promised. I've had many issues with it.",
        "I am so impressed with the quality and durability. This product will last for years.",
        "This product is a total game-changer. The innovation is truly remarkable.",
        "The company is very transparent and communicates clearly with their customers."
    ]
    return comments

def preprocess_text(comments, stopwords):
    all_text = " ".join(comments)
    words = re.findall(r'\b\w+\b', all_text.lower())
    filtered_words = [w for w in words if w not in stopwords and len(w) > 2]
    word_counts = Counter(filtered_words)
    return dict(sorted(word_counts.items(), key=lambda x: x[1], reverse=True))

def highlight_word(text, word):
    return re.sub(fr"(?i)\b({word})\b", r"**\1**", text)

def analyze_sentiment(comment):
    blob = TextBlob(comment)
    polarity = blob.sentiment.polarity
    if polarity > 0.2:
        return "😊 Positive", polarity, "positive"
    elif polarity < -0.2:
        return "😞 Negative", polarity, "negative"
    else:
        return "😐 Neutral", polarity, "neutral"

def get_sentiment_stats(comments):
    sentiments = [analyze_sentiment(comment) for comment in comments]
    positive_count = sum(1 for s in sentiments if s[2] == "positive")
    negative_count = sum(1 for s in sentiments if s[2] == "negative")
    neutral_count = sum(1 for s in sentiments if s[2] == "neutral")
    return positive_count, negative_count, neutral_count

def show_loading_animation(step, progress, message):
    """Display enhanced loading animation at the bottom of the screen"""
    icons = ["📊", "📝", "😊", "🔑", "✨"]
    st.markdown(f"""
    <div class="loading-container">
        <div class="loading-step">
            <span class="loading-icon">{icons[step-1] if step <= len(icons) else "✓"}</span>
            <span>{message}</span>
        </div>
        <div class="loading-bar">
            <div class="loading-progress" style="width: {progress}%"></div>
        </div>
    </div>
    """, unsafe_allow_html=True)

def process_uploaded_file(uploaded_file):
    """Process uploaded file and extract comments"""
    comments = []
    
    if uploaded_file is not None:
        if uploaded_file.name.endswith('.csv'):
            df = pd.read_csv(uploaded_file)
            comment_columns = ['comment', 'comments', 'text', 'feedback', 'review', 'message', 'content']
            for col in comment_columns:
                if col in df.columns:
                    comments = df[col].dropna().astype(str).tolist()
                    break
            if not comments and len(df.columns) > 0:
                comments = df.iloc[:, 0].dropna().astype(str).tolist()
        
        elif uploaded_file.name.endswith('.txt'):
            content = uploaded_file.getvalue().decode("utf-8")
            comments = [line.strip() for line in content.split('\n') if line.strip()]
        
        elif uploaded_file.name.endswith(('.xlsx', '.xls')):
            df = pd.read_excel(uploaded_file)
            comment_columns = ['comment', 'comments', 'text', 'feedback', 'review', 'message', 'content']
            for col in comment_columns:
                if col in df.columns:
                    comments = df[col].dropna().astype(str).tolist()
                    break
            if not comments and len(df.columns) > 0:
                comments = df.iloc[:, 0].dropna().astype(str).tolist()
    
    return comments

def get_keyword_color_class(frequency, max_frequency):
    """Get different color classes based on frequency"""
    if max_frequency == 0:
        return "low"
    ratio = frequency / max_frequency
    if ratio > 0.7:
        return "high"
    elif ratio > 0.4:
        return "medium"
    else:
        return "low"

# Custom stopwords
stopwords = {
    "i", "me", "my", "myself", "we", "our", "ours", "ourselves", "you", "your", "yours", "yourself", "yourselves",
    "he", "him", "his", "himself", "she", "her", "hers", "herself", "it", "its", "itself", "they", "them", "their", "theirs", "themselves",
    "what", "which", "who", "whom", "this", "that", "these", "those", "am", "is", "are", "was", "were", "be", "been", "being",
    "have", "has", "had", "having", "do", "does", "did", "doing", "a", "an", "the", "and", "but", "if", "or", "because", "as", "until",
    "while", "of", "at", "by", "for", "with", "about", "against", "between", "into", "through", "during", "before", "after", "above",
    "below", "to", "from", "up", "down", "in", "out", "on", "off", "over", "under", "again", "further", "then", "once", "here", "there",
    "when", "where", "why", "how", "all", "any", "both", "each", "few", "more", "most", "other", "some", "such", "no", "nor", "not",
    "only", "own", "same", "so", "than", "too", "very", "s", "t", "can", "will", "just", "don", "should", "now", "d", "ll", "m", "o",
    "re", "ve", "y", "ma", "but", "etc", "e.g", "i.e", "would", "could", "shall"
}

# -------------------------------
# Enhanced Streamlit UI
# -------------------------------

def main():
    # Inject custom CSS
    inject_custom_css()
    
    # Page configuration
    st.set_page_config(
        page_title="JurisMind",
        page_icon="🧠",
        layout="wide",
        initial_sidebar_state="expanded"
    )
    
    # Header section with enhanced design
    st.markdown('<h1 class="main-header">JurisMind</h1>', unsafe_allow_html=True)
    st.markdown('<p class="sub-header">Advanced sentiment analysis, keyword extraction, and interactive visualizations for customer feedback</p>', unsafe_allow_html=True)
    
    # Initialize session state
    if "comments" not in st.session_state:
        st.session_state.comments = []
    if "processing" not in st.session_state:
        st.session_state.processing = False
    if "selected_word" not in st.session_state:
        st.session_state.selected_word = None
    if "file_processed" not in st.session_state:
        st.session_state.file_processed = False
    
    # File upload section
    with st.container():
        st.markdown("### 📁 Upload Your Data File")
        st.markdown('<p style="color: var(--text-secondary); margin-bottom: 2rem; font-size: 1.1rem;">Upload a CSV, Excel, or text file containing customer comments for analysis.</p>', unsafe_allow_html=True)
        
        uploaded_file = st.file_uploader(
            "Choose a file", 
            type=['csv', 'txt', 'xlsx', 'xls'],
            label_visibility="collapsed"
        )
        
        if st.button("🚀 Analyze Data", use_container_width=True, key="analyze_btn"):
            st.session_state.processing = True
            st.session_state.comments = []
            st.session_state.selected_word = None
            
            placeholder = st.empty()
            
            if uploaded_file is not None:
                with placeholder.container():
                    show_loading_animation(1, 20, "📊 Parsing uploaded data file...")
                time.sleep(1.5)
                
                comments = process_uploaded_file(uploaded_file)
                
                with placeholder.container():
                    show_loading_animation(2, 40, "📝 Processing comments...")
                time.sleep(1.5)
                
            else:
                with placeholder.container():
                    show_loading_animation(1, 20, "📊 Generating sample dataset...")
                time.sleep(1.5)
                
                comments = create_sample_data()
                
                with placeholder.container():
                    show_loading_animation(2, 40, "📝 Processing sample comments...")
                time.sleep(1.5)
            
            with placeholder.container():
                show_loading_animation(3, 60, "😊 Performing sentiment analysis...")
            time.sleep(1.5)
            
            with placeholder.container():
                show_loading_animation(4, 80, "🔑 Extracting keywords and patterns...")
            time.sleep(1.5)
            
            with placeholder.container():
                show_loading_animation(5, 100, "✨ Generating insights and visualizations...")
            time.sleep(1.5)
            
            st.session_state.comments = comments
            st.session_state.file_processed = True
            st.session_state.processing = False
            placeholder.empty()
            st.success("✅ Analysis completed successfully!")
            st.rerun()
    
    if st.session_state.processing:
        show_loading_animation(1, 50, "Processing your data...")
    
    if st.session_state.comments and not st.session_state.processing:
        comments = st.session_state.comments
        word_counts = preprocess_text(comments, stopwords)
        positive_count, negative_count, neutral_count = get_sentiment_stats(comments)
        
        st.markdown('<div style="margin: 3rem 0;">', unsafe_allow_html=True)
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.markdown(f'''
            <div class="metric-card">
                <h3>📊 Total Comments</h3>
                <h2>{len(comments)}</h2>
            </div>
            ''', unsafe_allow_html=True)
        
        with col2:
            st.markdown(f'''
            <div class="metric-card">
                <h3>😊 Positive</h3>
                <h2>{positive_count}</h2>
            </div>
            ''', unsafe_allow_html=True)
        
        with col3:
            st.markdown(f'''
            <div class="metric-card">
                <h3>😐 Neutral</h3>
                <h2>{neutral_count}</h2>
            </div>
            ''', unsafe_allow_html=True)
        
        with col4:
            st.markdown(f'''
            <div class="metric-card">
                <h3>😞 Negative</h3>
                <h2>{negative_count}</h2>
            </div>
            ''', unsafe_allow_html=True)
        
        st.markdown('</div>', unsafe_allow_html=True)
        
        tab1, tab2, tab3 = st.tabs(["📝 Comments Analysis", "🔑 Keyword Explorer", "📊 Visualizations"])
        
        with tab1:
            st.markdown('<div class="section-header">Recent Comments</div>', unsafe_allow_html=True)
            col1, col2 = st.columns([1, 1], gap="large")
            
            with col1:
                if comments:
                    with st.container(height=600):
                        for i, comment in enumerate(comments[:20]):
                            sentiment_text, polarity, sentiment_class = analyze_sentiment(comment)
                            st.markdown(f'''
                            <div class="comment-item">
                                <div style="font-size: 0.9rem; color: var(--text-secondary); margin-bottom: 0.8rem; display: flex; justify-content: space-between;">
                                    <span>Comment #{i+1}</span>
                                    <span>Polarity: {polarity:.3f}</span>
                                </div>
                                <div style="color: var(--text-primary); font-size: 1.1rem; line-height: 1.7; margin: 1.2rem 0; font-weight: 500;">{comment}</div>
                                <div class="sentiment-badge {sentiment_class}">{sentiment_text}</div>
                            </div>
                            ''', unsafe_allow_html=True)
            
            with col2:
                st.markdown('<div class="section-header">Sentiment Distribution</div>', unsafe_allow_html=True)
                
                fig, ax = plt.subplots(figsize=(10, 8), facecolor='#0a0a0a')
                sentiments = [positive_count, neutral_count, negative_count]
                labels = ['Positive', 'Neutral', 'Negative']
                colors = ['#10b981', '#f59e0b', '#ef4444']
                explode = (0.05, 0.02, 0.05)
                
                ax.pie(
                    sentiments, explode=explode, labels=labels, colors=colors, 
                    autopct='%1.1f%%', startangle=90, shadow=True,
                    textprops={'color': 'white', 'fontsize': 12, 'fontweight': 'bold'}
                )
                
                ax.axis('equal')
                plt.title('Sentiment Distribution', fontsize=16, fontweight='bold', pad=30, color='white')
                plt.tight_layout()
                st.pyplot(fig)
        
        with tab2:
            st.markdown('<div class="section-header">Keyword Explorer</div>', unsafe_allow_html=True)
            col1, col2 = st.columns([1, 1], gap="large")
            
            with col1:
                st.markdown('### 📋 Keyword List')
                keywords = list(word_counts.items())[:30]
                max_freq = max([f for _, f in keywords]) if keywords else 0

                with st.container(height=600):
                    # Use Streamlit buttons to update state directly
                    for i, (word, freq) in enumerate(keywords):
                        if st.button(f"{word.capitalize()} ({freq})", key=f"btn_{word}", use_container_width=True):
                            st.session_state.selected_word = word
                            st.rerun()
            
            with col2:
                if st.session_state.selected_word:
                    st.markdown(f'<div class="section-header">Comments containing: "{st.session_state.selected_word}"</div>', unsafe_allow_html=True)
                    
                    # Filter comments using a case-insensitive check
                    matching_comments = [c for c in comments if st.session_state.selected_word.lower() in c.lower()]
                    
                    if matching_comments:
                        with st.container(height=600):
                            for i, comment in enumerate(matching_comments):
                                highlighted_comment = highlight_word(comment, st.session_state.selected_word)
                                sentiment_text, polarity, sentiment_class = analyze_sentiment(comment)
                                
                                st.markdown(f'''
                                <div class="comment-item">
                                    <div style="font-size: 0.9rem; color: var(--text-secondary); margin-bottom: 0.8rem;">Match #{i+1}</div>
                                    <div style="color: var(--text-primary); font-size: 1.1rem; line-height: 1.7; margin: 1.2rem 0; font-weight: 500;">{highlighted_comment}</div>
                                    <div class="sentiment-badge {sentiment_class}">{sentiment_text} (Pol: {polarity:.3f})</div>
                                </div>
                                ''', unsafe_allow_html=True)
                    else:
                        st.info("No comments found containing this keyword.")
                else:
                    st.markdown('<div class="section-header">Keyword Insights</div>', unsafe_allow_html=True)
                    st.info("👆 Click on any keyword to see related comments and sentiment analysis")
        
        with tab3:
            st.markdown('<div class="section-header">Advanced Visualizations</div>', unsafe_allow_html=True)
            col1, col2 = st.columns([2, 1], gap="large")
            
            with col1:
                st.markdown('<div class="section-header">Word Cloud Visualization</div>', unsafe_allow_html=True)
                
                if word_counts:
                    wc = WordCloud(
                        width=1200, 
                        height=600, 
                        background_color=None,
                        mode="RGBA",
                        colormap="plasma",
                        max_words=150,
                        relative_scaling=0.5,
                        collocations=False,
                        prefer_horizontal=0.7,
                        min_font_size=10,
                        max_font_size=150,
                        random_state=42
                    ).generate_from_frequencies(word_counts)
                    
                    fig, ax = plt.subplots(figsize=(14, 7), facecolor='#0a0a0a')
                    ax.imshow(wc, interpolation="bilinear")
                    ax.axis("off")
                    ax.set_title("Keyword Frequency Cloud", fontsize=20, pad=20, fontweight='bold', color='white')
                    fig.patch.set_facecolor('#0a0a0a')
                    plt.tight_layout()
                    st.pyplot(fig, use_container_width=True)
            
            with col2:
                st.markdown('<div class="section-header">Top 15 Keywords</div>', unsafe_allow_html=True)
                
                if word_counts:
                    with st.container(height=600):
                        for word, freq in list(word_counts.items())[:15]:
                            st.markdown(f'''
                            <div style="padding: 1.2rem; margin: 0.8rem 0; background: rgba(30, 30, 46, 0.7); border-radius: 12px; border-left: 4px solid #667eea; backdrop-filter: blur(15px);">
                                <div style="font-weight: 700; color: var(--text-primary); font-size: 1.1rem; margin-bottom: 0.3rem;">{word.capitalize()}</div>
                                <div style="font-size: 0.9rem; color: var(--text-secondary); font-weight: 600;">{freq} occurrences</div>
                            </div>
                            ''', unsafe_allow_html=True)
        
        st.markdown('<div class="section-header">Export & Actions</div>', unsafe_allow_html=True)
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            df = pd.DataFrame({
                'comment': comments,
                'sentiment': [analyze_sentiment(comment)[0] for comment in comments],
                'polarity': [analyze_sentiment(comment)[1] for comment in comments]
            })
            csv = df.to_csv(index=False)
            st.download_button(
                label="💾 Export Full Analysis to CSV",
                data=csv,
                file_name="complete_analysis.csv",
                mime="text/csv",
                use_container_width=True,
                key="download_btn"
            )
        
        with col2:
            if st.button("🔄 Reset & Clear Analysis", key="reset_btn", use_container_width=True):
                st.session_state.comments = []
                st.session_state.file_processed = False
                st.rerun()
        
        with col3:
            if st.button("📊 Analyze New Data", key="new_analysis_btn", use_container_width=True):
                st.session_state.comments = []
                st.session_state.file_processed = False
                st.rerun()
    
    elif not st.session_state.comments and not st.session_state.processing:
        st.markdown('''
        <div class="empty-state">
            <h3 style="color: var(--text-primary); margin-bottom: 2rem; font-size: 2.2rem; background: var(--primary-gradient); -webkit-background-clip: text; -webkit-text-fill-color: transparent; font-weight: 800;">🚀 Ready to Analyze Customer Feedback?</h3>
            <p style="color: var(--text-secondary); margin-bottom: 2rem; font-size: 1.2rem; line-height: 1.6;">Upload your data file or click "Analyze Data" to automatically generate sample data and unlock powerful AI-driven insights.</p>
            <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 1.5rem; text-align: left; max-width: 800px; margin: 0 auto;">
                <div style="padding: 1.5rem; background: rgba(30, 30, 46, 0.7); border-radius: 16px; border: 1px solid rgba(102, 126, 234, 0.3);">
                    <div style="font-size: 2rem; margin-bottom: 1rem;">😊</div>
                    <div style="font-weight: 700; color: var(--text-primary); font-size: 1.2rem; margin-bottom: 0.5rem;">Sentiment Analysis</div>
                    <div style="color: var(--text-secondary); font-size: 0.9rem;">AI-powered emotion detection with polarity scoring</div>
                </div>
                <div style="padding: 1.5rem; background: rgba(30, 30, 46, 0.7); border-radius: 16px; border: 1px solid rgba(102, 126, 234, 0.3);">
                    <div style="font-size: 2rem; margin-bottom: 1rem;">🔑</div>
                    <div style="font-weight: 700; color: var(--text-primary); font-size: 1.2rem; margin-bottom: 0.5rem;">Keyword Extraction</div>
                    <div style="color: var(--text-secondary); font-size: 0.9rem;">Automatic theme identification with frequency weighting</div>
                </div>
                <div style="padding: 1.5rem; background: rgba(30, 30, 46, 0.7); border-radius: 16px; border: 1px solid rgba(102, 126, 234, 0.3);">
                    <div style="font-size: 2rem; margin-bottom: 1rem;">☁️</div>
                    <div style="font-weight: 700; color: var(--text-primary); font-size: 1.2rem; margin-bottom: 0.5rem;">Word Clouds</div>
                    <div style="color: var(--text-secondary); font-size: 0.9rem;">Visual frequency analysis with interactive elements</div>
                </div>
                <div style="padding: 1.5rem; background: rgba(30, 30, 46, 0.7); border-radius: 16px; border: 1px solid rgba(102, 126, 234, 0.3);">
                    <div style="font-size: 2rem; margin-bottom: 1rem;">📊</div>
                    <div style="font-weight: 700; color: var(--text-primary); font-size: 1.2rem; margin-bottom: 0.5rem;">Export Results</div>
                    <div style="color: var(--text-secondary); font-size: 0.9rem;">Downloadable insights in multiple formats</div>
                </div>
            </div>
        </div>
        ''', unsafe_allow_html=True)

if __name__ == "__main__":
    main()