import pandas as pd
from akshara.varnakaarya import get_vinyaasa, get_shabda
from pratyaahaara import expand_pratyahaara
from varna import avasaana
from sutra import *
import sutra

def eng_to_devanagari(text):
    mapping = str.maketrans('0123456789', '०१२३४५६७८९')
    return str(text).translate(mapping)

def safe_vinyaasa(word):
    if "ॐ" in word:
        word = word.replace("ॐ", "ओम्")
    try:
        return get_vinyaasa(word)
    except:
        return None

def safe_shabda(vinyaasa_list):
    try:
        return get_shabda(vinyaasa_list)
    except:
        return "".join(vinyaasa_list)

def vaakya_sandhi(sentence: str, settings: dict = None, lang: str = "संस्कृतम्"):
    sutra.ACTIVE_SETTINGS = settings or {}

    col_sthiti = "स्थिति"
    col_sutra = "सूत्र"
    col_words = "पदसमूहः" if lang == "संस्कृतम्" else "Words"
    col_sutrani = "सूत्राणि" if lang == "संस्कृतम्" else "Sutras"
    col_result = "सन्धियुक्तरूपम्" if lang == "संस्कृतम्" else "Sandhi Form"

    prakriya = pd.DataFrame(columns=[col_sthiti, col_sutra])
    sandhi_summary = pd.DataFrame(columns=[col_words, col_sutrani, col_result])

    dd = []
    flag = 0
    temp = ""

    # Strip excessive spaces and clean
    mm = [w for w in sentence.replace("ॐ", "ओम्").strip().split() if w]
    
    if not mm:
        return ["", pd.DataFrame(), pd.DataFrame()]

    for ii in range(len(mm) - 1):
        primary = mm[ii]

        if flag == 1:
            flag = 0
            primary = temp

        pv = safe_vinyaasa(primary)
        if not pv:
            dd.append(primary)
            dd.append(" ")
            continue

        if primary[-1] == "ः":
            if primary in ["पुनः", "प्रातः", "अन्तः", "स्वः"]:
                primary = safe_shabda(safe_vinyaasa(primary[:-1] + "र्"))
            else:
                primary = safe_shabda(safe_vinyaasa(primary[:-1] + "स्"))
            pv = safe_vinyaasa(primary)

        if primary in avasaana:
            continue

        secondary = mm[ii + 1]

        if secondary in avasaana:
            s = primary
            sv = []
        else:
            s = primary + " " + secondary
            sv = safe_vinyaasa(secondary)
            if not sv: sv = []

        df = pd.DataFrame(columns=[col_sthiti, col_sutra])
        row = {col_sthiti: s, col_sutra: "-"}
        df = pd.concat([df, pd.DataFrame([row])], ignore_index=True)

        if pv and sv:
            if pv[-1] in expand_pratyahaara("अच्"):
                if secondary in avasaana:
                    pass
                elif sv[0] in expand_pratyahaara("हल्"):
                    if pv[-1] in ["अ", "इ", "उ", "ऋ", "ऌ"] and sv[0] == "छ्":
                        df = छे_च(df, col_sthiti, col_sutra)
                else:
                    if pv[-1] in expand_pratyahaara("एङ्") and sv[0] == "अ":
                        df = एङः_पदान्तादति(df, col_sthiti, col_sutra)
                    elif pv[-1] in ["अ", "आ"] and sv[0] in ["ए", "ओ"] and primary in ["प्र", "अप", "अव", "उप", "परा"]:
                        df = एङि_पररूपम्(df, col_sthiti, col_sutra)
                    elif (pv[-1] == sv[0] and pv[-1] in expand_pratyahaara("अक्")) or (
                        set((pv[-1], sv[0])) in [
                            set(("अ", "आ")), set(("इ", "ई")), set(("उ", "ऊ")),
                            set(("ऋ", "ॠ")), set(("ऋ", "ऌ")), set(("ॠ", "ऌ")),
                        ]
                    ):
                        df = अकः_सवर्णे_दीर्घः(df, col_sthiti, col_sutra)
                    elif pv[-1] in ["अ", "आ"] and sv[0] in expand_pratyahaara("एच्"):
                        df = वृद्धिरेचि(df, col_sthiti, col_sutra)
                    elif pv[-1] in ["अ", "आ"] and sv[0] in expand_pratyahaara("अक्"):
                        df = आद्गुणः(df, col_sthiti, col_sutra)
                    elif pv[-1] in expand_pratyahaara("एच्") and sv[0] in expand_pratyahaara("अच्"):
                        df = एचोऽयवायावः(df, col_sthiti, col_sutra)
                    elif pv[-1] in expand_pratyahaara("इक्") and sv[0] in expand_pratyahaara("अच्"):
                        df = इको_यणचि(df, col_sthiti, col_sutra)
            else:
                if (
                    secondary not in avasaana
                    and (mm[ii] in ["सस्", "एषस्", "सः", "एषः"] or primary in ["सस्", "एषस्"])
                    and sv[0] in expand_pratyahaara("हल्")
                ):
                    df = एतत्तदोः_सुलोपोऽकोरनञ्समासे_हलि(df, col_sthiti, col_sutra)
                elif pv[-1] == "स्":
                    df = ससजुषो_रुः(df, col_sthiti, col_sutra)
                    if secondary in avasaana:
                        df = खरवसानयोर्विसर्जनीयः(df, col_sthiti, col_sutra)
                    else:
                        if sv[0] in expand_pratyahaara("खर्"):
                            df = खरवसानयोर्विसर्जनीयः(df, col_sthiti, col_sutra)
                        else:
                            if primary in ["भोस्", "भगोस्", "अघोस्"]:
                                df = भोभगोअघोअपूर्वस्य_योऽशि(df, col_sthiti, col_sutra)
                            elif pv[-2] == "अ":
                                if sv[0] == "अ":
                                    df = अतो_रोरप्लुतादप्लुते(df, col_sthiti, col_sutra)
                                elif sv[0] in expand_pratyahaara("हश्"):
                                    df = हशि_च(df, col_sthiti, col_sutra)
                                else:
                                    df = भोभगोअघोअपूर्वस्य_योऽशि(df, col_sthiti, col_sutra)
                            elif pv[-2] == "आ":
                                df = भोभगोअघोअपूर्वस्य_योऽशि(df, col_sthiti, col_sutra)
                            elif sv[0] == "र्":
                                df = रो_रि(df, col_sthiti, col_sutra)
                else:
                    if pv[-1] in expand_pratyahaara("झल्"):
                        df = झलां_जशोऽन्ते(df, col_sthiti, col_sutra)
                    elif secondary not in avasaana and pv[-1] == "र्" and sv[0] == "र्":
                        df = रो_रि(df, col_sthiti, col_sutra)
                    elif pv[-1] == "र्" and (secondary in avasaana or sv[0] in expand_pratyahaara("खर्")):
                        df = खरवसानयोर्विसर्जनीयः(df, col_sthiti, col_sutra)
                    elif secondary in avasaana:
                        pass
                    elif pv[-1] == "म्" and secondary not in avasaana:
                        if sv[0] in expand_pratyahaara("हल्"):
                            df = मोऽनुस्वारः(df, col_sthiti, col_sutra)
                    elif secondary not in avasaana and pv[-1] == "न्" and sv[0] in expand_pratyahaara("छव्"):
                        df = नश्छव्यप्रशान्(df, col_sthiti, col_sutra)
                    elif secondary not in avasaana and pv[-1] == "न्" and sv[0] == "ल्":
                        df = तोर्लि(df, col_sthiti, col_sutra)
                    elif secondary not in avasaana and pv[-1] == "न्" and sv[0] in ["श्", "च्", "छ्", "ज्", "झ्", "ञ्"]:
                        df = स्तोः_श्चुना_श्चुः(df, col_sthiti, col_sutra)
                    elif secondary not in avasaana and pv[-1] in expand_pratyahaara("हल्") and sv[0] in expand_pratyahaara("अच्"):
                        if pv[-1] in expand_pratyahaara("ङम्") and pv[-2] in ["अ", "इ", "उ", "ऋ", "ऌ"]:
                            df = ङमो_ह्रस्वादचि_ङमुण्नित्यम्(df, col_sthiti, col_sutra)

        r = list(df[col_sthiti])[-1]

        if " " in r:
            dd.extend(safe_vinyaasa(r.split(" ")[0]) or list(r.split(" ")[0]))
            dd.append(" ")
        else:
            if secondary in avasaana:
                dd.extend(safe_vinyaasa(r) or list(r))
                dd.append(" ")
                dd.append(secondary)
            else:
                flag = 1
                temp = r

        if not df.empty:
            prakriya = pd.concat([prakriya, df], ignore_index=True)

        sutra_list = list(df[col_sutra])
        sutra_series = " ".join(sutra_list)

        row = {col_words: s, col_sutrani: sutra_series, col_result: r}
        sandhi_summary = pd.concat([sandhi_summary, pd.DataFrame([row])], ignore_index=True)

    if flag == 1:
        dd.extend(safe_vinyaasa(temp) or list(temp))
        dd.append(" ")
    elif len(mm) > 0:
        last_word = mm[-1]
        if last_word not in avasaana:
            if not any(last_word.endswith(av) for av in avasaana if av != " "):
                dd.extend(safe_vinyaasa(last_word) or list(last_word))
                dd.append(" ")
            else:
                for av in avasaana:
                    if av != " " and last_word.endswith(av):
                        word_part = last_word[: -len(av)]
                        if word_part:
                            dd.extend(safe_vinyaasa(word_part) or list(word_part))
                            dd.append(" ")
                        dd.append(av)
                        break

    if len(dd) > 0:
        ee = [dd[0]]
        for i in range(1, len(dd) - 1):
            if (dd[i] == " " and dd[i - 1] in expand_pratyahaara("हल्") and dd[i + 1] not in avasaana):
                pass
            else:
                ee.append(dd[i])
        if len(dd) > 1:
            ee.append(dd[-1])

        punctuation_marks = ["।", "॥"]
        i = 0
        while i < len(ee):
            if ee[i] in punctuation_marks:
                if i > 0 and ee[i - 1] != " ":
                    ee.insert(i, " ")
                    i += 1
                if i < len(ee) - 1 and ee[i + 1] != " ":
                    ee.insert(i + 1, " ")
                    i += 1
            i += 1

        ee = safe_shabda(ee)
    else:
        ee = ""

    ee = " ".join(ee.split())
    ee = ee.replace(" ।", "।").replace("।", " । ")
    ee = ee.replace(" ॥", "॥").replace("॥", " ॥ ")
    ee = " ".join(ee.split())

    if lang == "संस्कृतम्":
        prakriya[col_sutra] = prakriya[col_sutra].apply(eng_to_devanagari)
        sandhi_summary[col_sutrani] = sandhi_summary[col_sutrani].apply(eng_to_devanagari)

    return [ee, sandhi_summary, prakriya]
