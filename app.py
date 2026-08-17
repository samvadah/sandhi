import streamlit as st
import pandas as pd
import streamlit.components.v1 as components
from core import vaakya_sandhi

st.set_page_config( page_title="सन्धीराट्", layout="centered")

# Language Toggle in Sidebar
lang = st.sidebar.radio("भाषा / Language", ["संस्कृतम्", "English"])

if lang == "संस्कृतम्":
    t_title = "सन्धीराट्"
    t_subtitle = "पाणिनीयसूत्रैः पदानि सन्धत्त।"
    t_img_prompt = "चित्रमस्ति चेत् <a href='https://ocr.sanskritdictionary.com/' target='_blank'>चित्रपाठयन्त्रेण</a> पाठरूपेण परिवर्त्यताम्।"
    t_input_label = "पृथक्पदैः संस्कृतवाक्यमत्र लिख्यताम्।"
    t_btn = "सन्धिर्विधीयताम्"
    t_result = "सन्धियुक्तरूपम्"
    t_convert = "लिप्यन्तरणम्"
    t_summary = "सारः"
    t_prakriya = "प्रक्रिया"
    t_settings = "सन्धिविकल्पाः"
    t_warn = "कृपया शुद्धं संस्कृतवाक्यं प्रदीयताम् ।"
    t_lopa = "लोपः शाकल्यस्य (द्वावपि -> द्वा अपि)"
    t_vaa = "वा शरि (तपस्स्वाध्याय -> तपः स्वाध्याय)"
    t_yaro = "यरोऽनुनासिके (एतद् मुरारिः -> एतन्मुरारिः)"
    t_shashcho = "शशछोऽटि (तद् शिवः -> तच्छिवः)"
    t_jhayo = "झयो होऽन्यतरस्याम् (वाग् हरिः -> वाग्घरिः)"
    t_disclaimer_title = "सूचनम्"
    t_disclaimer_body = (
        "<strong>पदान्तसन्धिरेवायम्।</strong> अयं तन्त्रांशः पृथक्पदानां सन्धये एव निर्मितः न तु पदान्तर्गतसन्धये यथा ने अनम् नयनम् ।<br><br>"
        "<strong>दर्शनदोषः।</strong> विद्वाल्ँलिखति इति शुद्धरूपं तथापि टङ्कणयन्त्रस्य दर्शनदोषवशात् विद्वाँल्लिखति इति प्रदर्श्यते ।<br><br>"
        "<strong>अष्टाध्यायीपूर्णता।</strong> अयं तन्त्रांशः प्रायः सर्वानपि शास्त्रीयसन्धीन् करोति तथापि अष्टाध्याय्यां सहस्राधिकानि सूत्राणि सन्ति अतः केचन वैदिकसन्धयः अपवादसन्धयः च अग्रे योजयिष्यन्ते ।<br><br>"
        "<strong>दोषावलोकनम्।</strong> यत्र कुत्रापि दोषाः दृश्यन्ते सद्य एव विद्युत्पत्रेण गिड्ढब्जालस्थले वा सूच्यताम् ।<br><br>"
        "<div style='text-align: center; margin-top: 15px;'>"
        "<a href='mailto:samvadah@proton.me' style='text-decoration: none; padding: 5px 10px; background-color: #f0f2f6; border-radius: 5px; color: black; margin-right: 10px;'>विद्युत्पत्रम्</a>"
        "<a href='https://github.com/samvadah/sandhi/issues' target='_blank' style='text-decoration: none; padding: 5px 10px; background-color: #f0f2f6; border-radius: 5px; color: black;'>गिड्ढब्जालस्थलम्</a>"
        "</div>"
    )
else:
    t_title = "Sandhify"
    t_subtitle = "Conjugate multiple words of Sanskrit together based on Paninian sutras."
    t_img_prompt = "Have an image? Convert it to text via <a href='https://ocr.sanskritdictionary.com/' target='_blank'>sanskritcr</a>"
    t_input_label = "Enter Sanskrit Sentence (space separated words):"
    t_btn = "Generate Sandhi"
    t_result = "Sandhi-fied text"
    t_convert = "Script Converter"
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
    t_disclaimer_body = (
        "<strong>External Sandhi Only:</strong> This tool is meant for external sandhi (पदान्त) between separate words. It is not designed for internal sandhi (अपदान्त) like <em>ने + अनं = नयनं</em>.<br><br>"
        "<strong>Rendering Note:</strong> Correct forms are like विद्वाल्ँलिखति but we show विद्वाँल्लिखति due to standard font rendering limitations.<br><br>"
        "<strong>Ashtadhyayi Completeness:</strong> While this engine covers the vast majority of classical Sandhi rules (अच्, हल्, विसर्ग), Panini's Ashtadhyayi contains over 4,000 sutras. Rare exceptions, Vedic rules, and specific word-bound sandhis may still be added in the future to make it absolutely perfect.<br><br>"
        "<strong>Report Mistakes:</strong> If you spot any mistakes, please report them immediately to the email or GitHub issues below.<br><br>"
        "<div style='text-align: center; margin-top: 15px;'>"
        "<a href='mailto:samvadah@proton.me' style='text-decoration: none; padding: 5px 10px; background-color: #f0f2f6; border-radius: 5px; color: black; margin-right: 10px;'>Report via Mail</a>"
        "<a href='https://github.com/samvadah/sandhi/issues' target='_blank' style='text-decoration: none; padding: 5px 10px; background-color: #f0f2f6; border-radius: 5px; color: black;'>Open GitHub Issue</a>"
        "</div>"
    )

st.title(t_title)
st.markdown(t_subtitle)

# Sidebar Settings
st.sidebar.header(t_settings)

lopa_shakalyasya = st.sidebar.checkbox(t_lopa, value=True)
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

input_text = st.text_area(t_input_label, value=default_text, height=150, label_visibility="visible")

def eng_to_devanagari(text):
    mapping = str.maketrans('0123456789', '०१२३४५६७८९')
    return str(text).translate(mapping)

if st.button(t_btn, type="primary"):
    if input_text.strip():
        try:
            result, summary, prakriya = vaakya_sandhi(input_text, settings, lang)
            
            st.subheader(t_result)
            st.code(result, language=None)
            
            with st.expander(t_convert):
                aksharamukha_html = f"""
                <div style="font-family: sans-serif; padding: 10px;">
                    <p style="font-size: 0.9em; color: gray;">Select a script below to convert the Sandhi text.</p>
                    <select class="aksharamukha-button" style="margin-bottom: 15px; padding: 6px; border-radius: 5px; border: 1px solid #ccc; cursor: pointer;"></select>
                    <div class="aksharamukha-text" style="font-size: 1.1em; padding: 15px; background-color: #f9f9f9; border-radius: 5px; border: 1px solid #ddd; word-wrap: break-word;">
                        {result}
                    </div>
                </div>
                <script src="https://cdn.jsdelivr.net/gh/virtualvinodh/aksharamukha/aksharamukha-web-plugin/aksharamukha-v3.js?source=Devanagari&class=aksharamukha-text"></script>
                """
                components.html(aksharamukha_html, height=250, scrolling=True)
            
            if lang == "संस्कृतम्":
                prakriya.columns = ["स्थितिः", "सूत्रम्"]
                summary.columns = ["पदसमूहः", "सूत्राणि", "सन्धियुक्तरूपम्"]
                
                prakriya.insert(0, "क्रमः", range(1, len(prakriya) + 1))
                summary.insert(0, "क्रमः", range(1, len(summary) + 1))
                
                prakriya["क्रमः"] = prakriya["क्रमः"].astype(str).apply(eng_to_devanagari)
                summary["क्रमः"] = summary["क्रमः"].astype(str).apply(eng_to_devanagari)
            else:
                prakriya.columns = ["State", "Sutra"]
                summary.columns = ["Words", "Sutras", "Sandhi Form"]
                
                prakriya.insert(0, "No.", range(1, len(prakriya) + 1))
                summary.insert(0, "No.", range(1, len(summary) + 1))
                
                prakriya["No."] = prakriya["No."].astype(str)
                summary["No."] = summary["No."].astype(str)
            
            with st.expander(t_summary):
                st.dataframe(summary, use_container_width=True, hide_index=True)
            
            with st.expander(t_prakriya):
                st.dataframe(prakriya, use_container_width=True, hide_index=True)
            
        except Exception as e:
            st.error(f"Error processing text: {e}")
    else:
        st.warning(t_warn)

st.markdown("---")
with st.expander(t_disclaimer_title):
    st.markdown(f"<div style='color: gray; font-size: 0.9em;'>{t_disclaimer_body}</div>", unsafe_allow_html=True)
