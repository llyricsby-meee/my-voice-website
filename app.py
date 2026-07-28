import gradio as gr
from TTS.api import TTS
import os

print("Loading AI Model...")
# Coqui XTTS v2 मॉडल जो एकदम नेचुरल वॉइस क्लोन करता है
tts = TTS("tts_models/multilingual/multi-dataset/xtts_v2", gpu=False)

def clone_my_voice(text, audio_sample, language):
    """
    यह फंक्शन टेक्स्ट और तुम्हारी आवाज़ का सैंपल लेकर क्लोन ऑडियो बनाएगा।
    इसे वेबसाइट से भी चला सकते हैं और किसी भी बोट से API के ज़रिए कॉल कर सकते हैं।
    """
    output_path = "generated_voice.wav"
    
    if audio_sample is None:
        # अगर कोई नया सैंपल नहीं दिया, तो डिफॉल्ट वाली यूज़ होगी
        audio_sample = "my_voice.wav"

    tts.tts_to_file(
        text=text,
        file_path=output_path,
        speaker_wav=audio_sample,
        language=language
    )
    return output_path

# सुंदर वेबसाइट इंटरफ़ेस (UI) जो खुद ब खुद API भी बना देगा
demo = gr.Interface(
    fn=clone_my_voice,
    inputs=[
        gr.Textbox(label="यहाँ अपना टेक्स्ट लिखें (Text to convert)", placeholder="कुछ भी टाइप करें..."),
        gr.Audio(label="अपनी आवाज़ का सैंपल (.wav upload करें)", type="filepath"),
        gr.Dropdown(choices=["hi", "en"], value="hi", label="भाषा (Language)")
    ],
    outputs=gr.Audio(label="क्लोन हुई आवाज़ (Generated Voice)"),
    title="🎙️ My Personal Voice Cloning Hub",
    description="यह वेबसाइट खुद की आवाज़ क्लोन करने और उसे API के रूप में इस्तेमाल करने के लिए है।"
)

if __name__ == "__main__":
    # Render के पोर्ट के हिसाब से ऑटोमैटिक लाइव हो जाएगा
    port = int(os.environ.get("PORT", 7860))
    demo.launch(server_name="0.0.0.0", server_port=port)
    
