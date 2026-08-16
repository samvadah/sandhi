import streamlit as st
import pandas as pd
from vaakya_sandhi import vaakya_sandhi

st.set_page_config(
    page_title="सन्धीराट्",
    layout="centered"
)

st.title("सन्धीराट्")
st.markdown("Generate Sandhi for Sanskrit sentences based on Paninian Sutras.")

# Sidebar for Settings
st.sidebar.header("Sandhi Settings")
st.sidebar.markdown("Configure optional rules (विकल्प):")

lopa_shakalyasya = st.sidebar.checkbox(
    "लोपः शाकल्यस्य (e.g., द्वावपि -> द्वा अपि)", 
    value=False,
    help="When enabled, optionally drops the 'य्' or 'व्' before vowels."
)

vaa_shari = st.sidebar.checkbox(
    "वा शरि (e.g., तपस्स्वाध्याय -> तपः स्वाध्याय)", 
    value=True,
    help="When enabled, preserves the visarga before sh-varga consonants. If disabled, converts to स्."
)

yaro_anunasike = st.sidebar.checkbox(
    "यरोऽनुनासिके (e.g., एतद् मुरारिः -> एतन्मुरारिः)",
    value=True,
    help="When enabled, optionally nasalizes the final consonant before nasals."
)

shashcho_ati = st.sidebar.checkbox(
    "शशछोऽटि (e.g., तद् शिवः -> तच्छिवः)",
    value=True,
    help="When enabled, optionally replaces 'श्' with 'छ्'."
)

jhayo_ho = st.sidebar.checkbox(
    "झयो होऽन्यतरस्याम् (e.g., वाग् हरिः -> वाग्घरिः)",
    value=True,
    help="When enabled, optionally assimilates 'ह्' to the preceding consonant's 4th letter."
)

settings = {
    "lopa_shakalyasya": lopa_shakalyasya,
    "vaa_shari": vaa_shari,
    "yaro_anunasike": yaro_anunasike,
    "shashcho_ati": shashcho_ati,
    "jhayo_ho": jhayo_ho
}

input_text = st.text_area("Enter Sanskrit Sentence (space separated words):", value="अत्र आगतः अस्मि शिवः अहम् ।")

if st.button("Generate Sandhi", type="primary"):
    if input_text.strip():
        try:
            result, summary, prakriya = vaakya_sandhi(input_text, settings)
            
            st.subheader("Sandhi Result")
            st.code(result, language=None)
            
            with st.expander("Summary"):
                st.dataframe(summary, use_container_width=True)
            
            with st.expander("Prakriya (Derivation)"):
                st.dataframe(prakriya, use_container_width=True)
            
        except Exception as e:
            st.error(f"Error processing text: {e}")
    else:
        st.warning("Please enter a valid Sanskrit sentence.")

# Footer
st.markdown("---")
st.markdown(
    "<div style='text-align: center; color: gray; font-size: 0.9em;'>"
    "<strong>Note:</strong> Correct forms are like विद्वाल्ँलिखति but we show विद्वाँल्लिखति for rendering issues.<br><br>"
    "<em>While this engine covers the vast majority of classical Sandhi rules (अच्, हल्, विसर्ग), "
    "Panini's Ashtadhyayi contains over 4,000 sutras. Rare exceptions, Vedic rules, and specific word-bound Sandhis may still be added in the future to make it absolutely perfect.</em><br><br>"
    "Report mistakes to <a href='mailto:samvadah@proton.me'>samvadah@proton.me</a>"
    "</div>", 
    unsafe_allow_html=True
)
