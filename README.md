<div align="center">

# 👑 सन्धीराट् (Sandhify)
### High-Precision Paninian Sanskrit Sandhi & Prakriya Derivation Engine

[![Streamlit App](https://static.streamlit.io/badges/streamlit_badge_black_white.svg)](https://sandhify.streamlit.app/)
[![Python 3.9+](https://img.shields.io/badge/python-3.9+-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)
[![GitHub stars](https://img.shields.io/github/stars/samvadah/sandhi?style=social)](https://github.com/samvadah/sandhi)

<p align="center">
  <b>A rule-based Sanskrit Computational Linguistics engine that executes full-sentence Padanta Sandhi (पदान्त सन्धि) according to Panini's <i>Ashtadhyayi</i> with step-by-step grammatical derivations (प्रक्रिया).</b>
</p>

[Live Demo](https://sandhify.streamlit.app/) • [Features](#-key-features) • [Installation](#-quickstart) • [Python Usage](#-python-api-usage) • [Supported Sutras](#-covered-ashtadhyayi-sutras)

</div>

---

## 📖 Overview

**सन्धीराट् (Sandhify)** is an open-source Sanskrit computational engine designed to conjugate space-separated Sanskrit words (*Padas*) in complete sentences according to classical Paninian grammar (*Vyakarana*). 

Unlike statistical/ML models that produce hallucinations, **सन्धीराट्** is 100% **rule-based and deterministic**, providing:
1. The **exact sandhi-fied text** (सन्धियुक्त रूपम्).
2. A **summary table** of all word boundaries analyzed.
3. A **complete step-by-step grammatical derivation** (*Prakriya* / प्रक्रिया) citing the exact *Ashtadhyayi* Sutra numbers (e.g., *इको यणचि ६.१.७७*, *झलां जशोऽन्ते ८.२.३९*).

---

## ✨ Key Features

- 📜 **Strict Paninian Compliance:** Implements classical rules for *Ach Sandhi* (vowels), *Hal Sandhi* (consonants), and *Visarga Sandhi*.
- 🔍 **Step-by-Step Prakriya (प्रक्रिया):** View intermediate phonetic transformations with referenced Sutra numbers at each transition.
- ⚙️ **Configurable Vaikalpika (Optional) Sandhis:** Toggle optional rules directly from the sidebar:
  - *लोपः शाकल्यस्य* (8.3.19) — *द्वावपि* vs *द्वा अपि*
  - *वा शरि* (8.3.36) — *तपस्स्वाध्याय* vs *तपः स्वाध्याय*
  - *यरोऽनुनासिकेऽनुनासिको वा* (8.4.45) — *एतद् मुरारिः* vs *एतन्मुरारिः*
  - *शशछोऽटि* (8.4.63) — *तद् शिवः* vs *तच्छिवः*
  - *झयो होऽन्यतरस्याम्* (8.4.62) — *वाग् हरिः* vs *वाग्घरिः*
  - *वा पदान्तस्य* (8.4.59) — *सं कल्पः* vs *सङ्कल्पः*
- 🌐 **Multi-Script Transliteration:** Instant script conversion powered by [Aksharamukha](https://aksharamukha.appspot.com/) (Devanagari, IAST, Telugu, Kannada, Malayalam, Bengali, Grantha, etc.).
- 🌐 **Bilingual Interface:** Toggle the entire UI seamlessly between **संस्कृतम्** and **English**.

---

## 🚀 Quickstart

### Run with Streamlit Locally

1. **Clone the repository:**
   ```bash
   git clone https://github.com/samvadah/sandhi.git
   cd sandhi
   ```

2. **Create a virtual environment & install dependencies:**
   ```bash
   python -m venv venv
   source venv/bin/activate    # On Windows: venv\Scripts\activate
   pip install -r requirements.txt
   ```

3. **Launch the web app:**
   ```bash
   streamlit run app.py
   ```

---

## 💻 Python API Usage

You can import and use the engine in your own Sanskrit NLP pipelines, bots, or research scripts without launching the web UI:

```python
from core import vaakya_sandhi

# Input Sanskrit sentence (space-separated words)
sentence = "अत्र अपि मुनिः उवाच तत् शिवः सम् कल्पः"

# Optional Paninian settings (all default to True / False as standard)
settings = {
    "lopa_shakalyasya": True,
    "vaa_shari": True,
    "yaro_anunasike": True,
    "shashcho_ati": True,
    "jhayo_ho": True,
    "anusvarasya_yayi": True,
}

# Generate Sandhi, Summary DataFrame, and Step-by-Step Prakriya DataFrame
result_text, summary_df, prakriya_df = vaakya_sandhi(sentence, settings=settings, lang="संस्कृतम्")

print("Sandhi Output:")
print(result_text)
# Output: अत्रापि मुनिरुवाच तच्छिवः सङ्कल्पः

print("\nGrammatical Derivations (Prakriya):")
print(prakriya_df)
```

---

## 📚 Covered Ashtadhyayi Sutras

| Sutra (सूत्रम्) | Number | Rule Type | Description |
| :--- | :--- | :--- | :--- |
| **इको यणचि** | 6.1.77 | अच् सन्धि | *Ik* vowels replaced by *Yan* before vowels |
| **एचोऽयवायावः** | 6.1.78 | अच् सन्धि | *Ech* vowels replaced by *ay, av, āy, āv* |
| **आद्गुणः** | 6.1.87 | अच् सन्धि | *a/ā* + vowel results in *Guna* |
| **वृद्धिरेचि** | 6.1.88 | अच् सन्धि | *a/ā* + *Ech* results in *Vriddhi* |
| **अकः सवर्णे दीर्घः** | 6.1.101 | अच् सन्धि | Homorganic vowels lengthen (*Savarna Deergha*) |
| **एङः पदान्तादति** | 6.1.109 | अच् सन्धि | *e/o* + short *a* results in Avagraha (ऽ) |
| **अतो रोरप्लुतादप्लुते** | 6.1.113 | विसर्ग सन्धि | *aḥ* + *a* turns into *o'ऽ* |
| **हशि च** | 6.1.114 | विसर्ग सन्धि | *aḥ* + voiced consonant turns into *o* |
| **एतत्तदोः सुलोपः...** | 6.1.132 | विसर्ग सन्धि | Dropping of *s/ḥ* for *saḥ / eṣaḥ* before consonants |
| **छे च** | 6.1.73 | हल् सन्धि | Short vowel + *ch* adds augment *c* (*Tuk*) |
| **रो रि / ढ्रलोपे...** | 8.3.14 / 6.3.111 | विसर्ग सन्धि | Elision of *r* before *r* and lengthening of prior vowel |
| **ससजुषो रुः** | 8.2.66 | विसर्ग सन्धि | Pada-final *s* transforms into *Ru (r)* |
| **झलां जशोऽन्ते** | 8.2.39 | हल् सन्धि | Non-nasal stops turn into voiced unaspirated stops (*Jash*) |
| **मोऽनुस्वारः** | 8.3.23 | हल् सन्धि | Pada-final *m* becomes Anusvara (*ṃ*) before consonants |
| **खरवसानयोर्विसर्जनीयः** | 8.3.15 | विसर्ग सन्धि | *r* becomes Visarga (*ḥ*) before *Khar* or pause |
| **लोपः शाकल्यस्य** | 8.3.19 | अच् सन्धि | Optional elision of *y/v* before vowels |
| **स्तोः श्चुना श्चुः** | 8.4.40 | हल् सन्धि | Dental to Palatal assimilation (*Schutva*) |
| **ष्टुना ष्टुः** | 8.4.41 | हल् सन्धि | Dental to Retroflex assimilation (*Shtutva*) |
| **यरोऽनुनासिकेऽनुनासिको वा** | 8.4.45 | हल् सन्धि | Consonants assimilate to class nasal |
| **खरि च** | 8.4.55 | हल् सन्धि | De-voicing of stops before voiceless consonants (*Chartva*) |
| **तोर्लि** | 8.4.60 | हल् सन्धि | Dental stops assimilate to *l* (with nasalization for *n*) |
| **झयो होऽन्यतरस्याम्** | 8.4.62 | हल् सन्धि | Voiced aspirate substitution for *h* after stops |
| **शशछोऽटि** | 8.4.63 | हल् सन्धि | *ś* becomes *ch* after stops |
| **वा पदान्तस्य** | 8.4.59 | हल् सन्धि | Optional conversion of Anusvara to matching nasal |

---

## 🛠️ Tech Stack & Dependencies

- **[Python](https://www.python.org/)** — Core rule engine implementation
- **[Streamlit](https://streamlit.io/)** — Fast, interactive frontend web application
- **[Pandas](https://pandas.pydata.org/)** — Structured derivation tables and data handling
- **[Akshara](https://pypi.org/project/akshara/)** — Phonetic parsing & varna-vyavastha representation
- **[Aksharamukha](https://github.com/virtualvinodh/aksharamukha)** — Multi-script Indic transliteration engine

---

## 🤝 Contributing & Feedback

Contributions, feature suggestions, and rule additions are welcome!

1. Fork the repository.
2. Create your feature branch (`git checkout -b feature/NewRule`).
3. Commit your changes (`git commit -m 'Add support for Vartika ...'`).
4. Push to the branch (`git push origin feature/NewRule`).
5. Open a Pull Request.

If you find an edge case or mistake in derivation, please [Open an Issue](https://github.com/samvadah/sandhi/issues) or email [samvadah@proton.me](mailto:samvadah@proton.me).

---

## 📄 License

Distributed under the **MIT License**. See `LICENSE` for more information.

<div align="center">
  <sub>Built with ❤️ for Sanskrit Computational Linguistics by <a href="https://github.com/samvadah">Samvadah</a></sub>
</div>
