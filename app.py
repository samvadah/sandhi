import streamlit as st
import pandas as pd
from vaakya_sandhi import vaakya_sandhi

st.set_page_config(
    page_title="सन्धीराट्",
    layout="centered"
)

# Language Toggle in Sidebar
lang = st.sidebar.radio("भाषा / Language", ["संस्कृतम्", "English"])

if lang == "संस्कृतम्":
    t_title = "सन्धीराट्"
    t_subtitle = "पाणिनीयसूत्राणाम् आधारेण संस्कृतपदानां वाक्येषु सन्धिं कुरुत।"
    t_img_prompt = "चित्रमस्ति वा? <a href='https://ocr.sanskritdictionary.com/' target='_blank'>sanskritcr</a> द्वारा पाठे परिवर्तयतु"
    t_input_label = "संस्कृतवाक्यम् अत्र लिखतु (पदानि पृथक् कृत्वा):"
    t_btn = "सन्धिं कुरु"
    t_result = "सन्धियुक्तं वाक्यम्"
    t_summary = "सङ्क्षेपः"
    t_prakriya = "प्रक्रिया"
    t_settings = "सन्धि-विकल्पाः"
    t_warn = "कृपया योग्यं संस्कृतवाक्यं लिखतु।"
    t_lopa = "लोपः शाकल्यस्य (उदा. द्वावपि -> द्वा अपि)"
    t_vaa = "वा शरि (उदा. तपस्स्वाध्याय -> तपः स्वाध्याय)"
    t_yaro = "यरोऽनुनासिके (उदा. एतद् मुरारिः -> एतन्मुरारिः)"
    t_shashcho = "शशछोऽटि (उदा. तद् शिवः -> तच्छिवः)"
    t_jhayo = "झयो होऽन्यतरस्याम् (उदा. वाग् हरिः -> वाग्घरिः)"
    t_disclaimer_title = "सूचनम्"
else:
    t_title = "सन्धीराट्"
    t_subtitle = "Conjugate multiple words of Sanskrit together based on Paninian sutras."
    t_img_prompt = "Have an image? Convert it to text via <a href='https://ocr.sanskritdictionary.com/' target='_blank'>sanskritcr</a>"
    t_input_label = "Enter Sanskrit Sentence (space separated words):"
    t_btn = "Generate Sandhi"
    t_result = "Sandhi-fied text"
    t_summary = "Summary"
    t_prakriya = "Prakriya (Derivation)"
    t_settings = "Sandhi Settings"
    t_warn = "Please enter a valid Sanskrit sentence."
    t_lopa = "Apply लोपः शाकल्यस्य (e.g., द्वावपि -> द्वा अपि)"
    t_vaa = "Apply वा शरि (e.g., तपस्स्वाध्याय -> तपः स्वाध्याय)"
    t_yaro = "Apply यरोऽनुनासिके (e.g., एतद् मुरारिः -> एतन्मुरारिः)"
    t_shashcho = "Apply शशछोऽटि (e.g., तद् शिवः -> तच्छिवः)"
    t_jhayo = "Apply झयो होऽन्यतरस्याम् (e.g., वाग् हरिः -> वाग्घरिः)"
    t_disclaimer_title = "Disclaimer & Notes"

st.title(t_title)
st.markdown(t_subtitle)

# Sidebar Settings
st.sidebar.header(t_settings)

lopa_shakalyasya = st.sidebar.checkbox(t_lopa, value=True) # Set to True to fix कः इति -> क इति
vaa_shari = st.sidebar.checkbox(t_vaa, value=True)
yaro_anunasike = st.sidebar.checkbox(t_yaro, value=True)
shashcho_ati = st.sidebar.checkbox(t_shashcho, value=True)
jhayo_ho = st.sidebar.checkbox(t_jhayo, value=True)

settings = {
    "lopa_shakalyasya": lopa_shakalyasya,
    "vaa_shari": vaa_shari,
    "yaro_anunasike": yaro_anunasike,
    "shashcho_ati": shashcho_ati,
    "jhayo_ho": jhayo_ho
}

st.markdown(t_img_prompt, unsafe_allow_html=True)

default_text = "अत्र अपि मुनिः उवाच भोः अच्युत तव औदार्यम् अति उत्तमम् गौः गच्छति यदि अपि सु आगतम् पितृ आज्ञा कर्तृ इह अद्य एव महा ऋषिः अस्ति। वाक् मयम् षट् मुखः तत् जलम् दिक् अन्तः जगत् ईशः पश्यति बालकः हसति नरः अत्र गै अकः पौ अकः च ने अनम् करोति। तत् लयः तत् शिवः रामः टीकते उद् डयनम् तत् चकार वृक्ष छाया किम् करोति देवाः इह अतः एव सः गच्छति एषः विष्णुः। प्र एजते उप ओषति अमी अश्वाः भानुः भाति पुनः रमते हरिः रयः कः चित् धनुः टङ्कारः निः सारः दुः खम् प्राक् नास्ति। मनस् रथः नमः ते पुनः च रामः षष्ठः बालः तरति सम् कल्पः सम् भवः चित् मयम् वाक् हरिः सुप् अन्तम्। मातुः कृपा पितुः इच्छा भ्रातुः धनम् सर्वम् अत्र अस्ति विद्वान् लिखति तान् जयेत् हसन् चकितः सम्राट् गच्छति अप् जम्। गौः अश्वः च पशोः अन्नम् नृपः जयति मुनिः ईक्षते साधुः उवाच मातृ ऋणम् च गो अग्रम् नौ इह वधु आगमनम् भवति।"

input_text = st.text_area(t_input_label, value=default_text, height=200)

def transliterate_to_iast(text):
    mapping = {
        'अ':'a', 'आ':'ā', 'इ':'i', 'ई':'ī', 'उ':'u', 'ऊ':'ū', 'ऋ':'ṛ', 'ॠ':'ṝ', 'ऌ':'ḷ', 'ॡ':'ḹ',
        'ए':'e', 'ऐ':'ai', 'ओ':'o', 'औ':'au',
        'क्':'k', 'ख्':'kh', 'ग्':'g', 'घ्':'gh', 'ङ्':'ṅ',
        'च्':'c', 'छ्':'ch', 'ज्':'j', 'झ्':'jh', 'ञ्':'ñ',
        'ट्':'ṭ', 'ठ्':'ṭh', 'ड्':'ḍ', 'ढ्':'ḍh', 'ण्':'ṇ',
        'त्':'t', 'थ्':'th', 'द्':'d', 'ध्':'dh', 'न्':'n',
        'प्':'p', 'फ्':'ph', 'ब्':'b', 'भ्':'bh', 'म्':'m',
        'य्':'y', 'र्':'r', 'ल्':'l', 'व्':'v',
        'श्':'ś', 'ष्':'ṣ', 'स्':'s', 'ह्':'h',
        'ं':'ṃ', 'ः':'ḥ', 'ँ':'m̐', 'ऽ':"'"
    }
    try:
        from akshara.varnakaarya import get_vinyaasa
        words = text.split()
        out = []
        for w in words:
            if w in ['।', '॥']:
                out.append('.' if w == '।' else '..')
                continue
            try:
                vin = get_vinyaasa(w)
                out.append("".join([mapping.get(x, x) for x in vin]))
            except:
                out.append(w)
        return " ".join(out)
    except:
        return text

if st.button(t_btn, type="primary"):
    if input_text.strip():
        try:
            result, summary, prakriya = vaakya_sandhi(input_text, settings)
            
            st.subheader(t_result)
            # st.code automatically gives a convenient copy-to-clipboard button
            st.code(result, language=None)
            
            st.caption(f"**IAST:** {transliterate_to_iast(result)}")
            
            with st.expander(t_summary):
                st.dataframe(summary, use_container_width=True)
            
            with st.expander(t_prakriya):
                st.dataframe(prakriya, use_container_width=True)
            
        except Exception as e:
            st.error(f"Error processing text: {e}")
    else:
        st.warning(t_warn)

st.markdown("---")
with st.expander(t_disclaimer_title):
    st.markdown(
        "<div style='color: gray; font-size: 0.9em;'>"
        "<strong>External Sandhi Only:</strong> This tool is meant for external sandhi (पदान्त) between separate words. It is not designed for internal sandhi (अपदान्त) like <em>ने + अनं = नयनं</em>.<br><br>"
        "<strong>Rendering Note:</strong> Correct forms are like विद्वाल्ँलिखति but we show विद्वाँल्लिखति due to standard font rendering limitations.<br><br>"
        "<strong>Ashtadhyayi Completeness:</strong> While this engine covers the vast majority of classical Sandhi rules (अच्, हल्, विसर्ग), Panini's Ashtadhyayi contains over 4,000 sutras. Rare exceptions, Vedic rules, and specific word-bound sandhis may still be added in the future to make it absolutely perfect.<br><br>"
        "<div style='text-align: center; margin-top: 15px;'>"
        "<a href='mailto:samvadah@proton.me' style='text-decoration: none; padding: 5px 10px; background-color: #f0f2f6; border-radius: 5px; color: black; margin-right: 10px;'>Report via Mail</a>"
        "<a href='https://github.com/samvadah/sandhi/issues' target='_blank' style='text-decoration: none; padding: 5px 10px; background-color: #f0f2f6; border-radius: 5px; color: black;'>Open GitHub Issue</a>"
        "</div>"
        "</div>", 
        unsafe_allow_html=True
    )
