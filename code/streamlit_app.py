import random
from io import BytesIO

import streamlit as st
from gtts import gTTS
from streamlit_mic_recorder import speech_to_text

# Set Streamlit app page configurations - Icon & URL Display
st.set_page_config(
        page_title="Hindi Bolo",
        page_icon="🦄"
    )

# Set Streamlit app Title & Header
st.title("Hindi Pronunciation Practice")
st.subheader("Let's have fun with Hindi words! :microphone:", divider=True)

# Dictionary of Hindi words categorized by topics
hindi_words_by_topic = {
    "Greetings": ["नमस्ते", "धन्यवाद", "शुभकामनाएं", "अलविदा", "स्वागत है", "जन्मदिन मुबारक", "कृपया"],
    "Family": ["माँ", "पिता", "भाई", "बहन", "दादी", "दादा", "नानी", "नाना", "चाचा", "चाची"],
    "Animals/Birds": ['खरगोश', "कुत्ता", "बिल्ली", "गाय", "घोड़ा", "हाथी", "शेर", "मोर", "तोता", "कौआ", "चिड़िया"],
    "Fruits/Vegetables": ["सेब", "केला", "आम", "संतरा", "गाजर", "टमाटर", "आलू", "प्याज", "मटर", "भिंडी"],
    "Actions": ["खाना", "पीना", "सोना", "उठना", "चलना", "दौड़ना", "कूदना", "बैठना", "पढ़ना", "लिखना"],
    "Places": ["स्कूल", "घर", "बाजार", "पार्क", "मंदिर", "मस्जिद", "चर्च", "हॉस्पिटल", "पुस्तकालय", "पार्क"],
    "Occupation": ["डॉक्टर", "अध्यापक", "इंजीनियर", "किसान", "पुलिस", "नर्स", "वकील", "दुकानदार", "मजदूर", "सैनिक"],
    "Things": ["किताब", "कंप्यूटर", "कुर्सी", "टेबल", "पेन", "पेंसिल", "कप", "गिलास", "बोतल", "घड़ी"],
    "Numbers": ["एक", "दो", "तीन", "चार", "पाँच", "छह", "सात", "आठ", "नौ", "दस"],
    "Colors": ["लाल", "नीला", "हरा", "पीला", "काला", "सफेद", "गुलाबी", "बैंगनी", "भूरा", "नारंगी"]
}

# Select a topic
selected_topic = st.selectbox("First, Select a Topic :one:", list(hindi_words_by_topic.keys()))

# Initialize session state for target_word and recognized_word
if 'target_word' not in st.session_state:
    st.session_state.target_word = random.choice(hindi_words_by_topic[selected_topic])

st.write("Next, click the button below to change to a new word! :radio_button:")
# Button to change the target word
if st.button("Change Word", use_container_width=True, type='primary'):
    st.session_state.target_word = random.choice(hindi_words_by_topic[selected_topic])

# Generate audio (speech) for the selected text
tts = gTTS(text=st.session_state.target_word, lang='hi')

# Convert gTTS object to byte stream
audio_bytes = BytesIO()
tts.write_to_fp(audio_bytes)
audio_bytes.seek(0)

# Play target pronunciation
st.write("Please listen carefully to the pronunciation :female-teacher:")
st.audio(audio_bytes, format='audio/mpeg')

# Apply CSS
st.markdown('''
<style>
    .stApp {
        background-color: #ffd1d8;
    }
    h1 {
        color: black;
    }
    h3 {
        color: black;
    }
    div.stApp {
        color: black;
    }
    p {
        color: black;
        font-size: 20px !important;
    }    
    .stButton>button {
        background-color: #B6FFF4 !important;
        border: none !important;
    }
    .stButton>button:hover {
        border: 1px solid #000000 !important;
    }
</style>
''', unsafe_allow_html=True)

# Prompt response pronunciation
st.write("Now, record your pronunciation of what you heard :studio_microphone:")
recognized_word = speech_to_text(
    language='hi',
    start_prompt="Start recording",
    stop_prompt="Stop recording",
    just_once=False,
    use_container_width=True,  
    callback=None,
    args=(),
    kwargs={},
    key=None  # No unique key needed
)

# Update session state with recognized word
if recognized_word:
    # Log the target and response words for debugging
    st.write(f"Target word: {st.session_state.target_word}")
    st.write(f"Recognized word: {recognized_word}")

    # Perform comparison target vs response for feedback
    if recognized_word == st.session_state.target_word:
        st.write(f"Great job! You pronounced {recognized_word} correctly.")
        st.balloons()
    else:
        st.write("Hmm, that wasn't quite right. Let's try again.")