import streamlit as st
import pandas as pd
from vaakya_sandhi import vaakya_sandhi

st.set_page_config(
    page_title="Sanskrit Sandhi Generator",
    page_icon="🕉️",
    layout="centered"
)

st.title("Sanskrit Sentence Sandhi Generator")
st.markdown("Generate Sandhi for Sanskrit sentences based on Paninian Sutras.")

# Sidebar for Settings
st.sidebar.header("⚙️ Sandhi Settings")
st.sidebar.markdown("Configure optional rules (विकल्प):")

lopa_shakalyasya = st.sidebar.checkbox(
    "Apply लोपः शाकल्यस्य (e.g., द्वावपि -> द्वा अपि)", 
    value=False,
    help="When enabled, drops the 'य्' or 'व्' before vowels optionally according to 8.3.19."
)

vaa_shari = st.sidebar.checkbox(
    "Apply वा शरि (e.g., तपस्स्वाध्याय -> तपः स्वाध्याय)", 
    value=False,
    help="When enabled, preserves the visarga before sh-varga consonants according to 8.3.36."
)

settings = {
    "lopa_shakalyasya": lopa_shakalyasya,
    "vaa_shari": vaa_shari
}

input_text = st.text_area("Enter Sanskrit Sentence (space separated words):", value="अत्र आगतः अस्मि शिवः अहम् ।")

if st.button("Generate Sandhi", type="primary"):
    if input_text.strip():
        try:
            result, summary, prakriya = vaakya_sandhi(input_text, settings)
            
            st.subheader("✨ Sandhi Result")
            st.success(result)
            
            st.subheader("📊 Summary")
            st.dataframe(summary, use_container_width=True)
            
            st.subheader("📜 Prakriya (Derivation)")
            st.dataframe(prakriya, use_container_width=True)
            
        except Exception as e:
            st.error(f"Error processing text: {e}")
    else:
        st.warning("Please enter a valid Sanskrit sentence.")

# Footer
st.markdown("---")
st.markdown(
    "<div style='text-align: center; color: gray;'>"
    "Report mistakes to <a href='mailto:samvadah@proton.me'>samvadah@proton.me</a>"
    "</div>", 
    unsafe_allow_html=True
)
