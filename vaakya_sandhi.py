import pandas as pd
from akshara.varnakaarya import get_vinyaasa, get_shabda

from pratyaahaara import expand_pratyahaara
from varna import avasaana
from sutra import *
import sutra

def vaakya_sandhi(sentence: str, settings: dict = None):
    sutra.ACTIVE_SETTINGS = settings or {}

    prakriya = pd.DataFrame(columns=["स्थिति", "सूत्र"])
    sandhi_summary = pd.DataFrame(columns=["पद समूह", "सूत्राणि", "संधि-कृत रूप"])

    dd = []
    flag = 0
    temp = ""

    mm = sentence.split(" ")

    for ii in range(len(mm) - 1):
        primary = mm[ii]

        if flag == 1:
            flag = 0
            primary = temp

        if primary[-1] == "ः":
            if primary in ["पुनः", "प्रातः", "अन्तः", "स्वः"]:
                primary = get_shabda(get_vinyaasa(primary[:-1] + "र्"))
            else:
                primary = get_shabda(get_vinyaasa(primary[:-1] + "स्"))

        if primary in avasaana:
            continue

        secondary = mm[ii + 1]

        if secondary in avasaana:
            s = primary
            sv = []
        else:
            s = primary + " " + secondary
            sv = get_vinyaasa(secondary)

        df = pd.DataFrame(columns=["स्थिति", "सूत्र"])
        row = {"स्थिति": s, "सूत्र": "-"}
        df = pd.concat([df, pd.DataFrame([row])], ignore_index=True)

        ss = get_vinyaasa(s)
        pv = get_vinyaasa(primary)

        if pv[-1] in expand_pratyahaara("अच्"):
            if secondary in avasaana:
                pass
            elif sv[0] in expand_pratyahaara("हल्"):
                if pv[-1] in ["अ", "इ", "उ", "ऋ", "ऌ"] and sv[0] == "छ्":
                    df = छे_च(df)
            else:
                if pv[-1] in expand_pratyahaara("एङ्") and sv[0] == "अ":
                    df = एङः_पदान्तादति(df)
                elif pv[-1] in ["अ", "आ"] and sv[0] in ["ए", "ओ"] and primary in ["प्र", "अप", "अव", "उप", "परा"]:
                    df = एङि_पररूपम्(df)
                elif (pv[-1] == sv[0] and pv[-1] in expand_pratyahaara("अक्")) or (
                    set((pv[-1], sv[0])) in [
                        set(("अ", "आ")), set(("इ", "ई")), set(("उ", "ऊ")),
                        set(("ऋ", "ॠ")), set(("ऋ", "ऌ")), set(("ॠ", "ऌ")),
                    ]
                ):
                    df = अकः_सवर्णे_दीर्घः(df)
                elif pv[-1] in ["अ", "आ"] and sv[0] in expand_pratyahaara("एच्"):
                    df = वृद्धिरेचि(df)
                elif pv[-1] in ["अ", "आ"] and sv[0] in expand_pratyahaara("अक्"):
                    df = आद्गुणः(df)
                elif pv[-1] in expand_pratyahaara("एच्") and sv[0] in expand_pratyahaara("अच्"):
                    df = एचोऽयवायावः(df)
                elif pv[-1] in expand_pratyahaara("इक्") and sv[0] in expand_pratyahaara("अच्"):
                    df = इको_यणचि(df)
        else:
            if (
                secondary not in avasaana
                and (mm[ii] in ["सस्", "एषस्", "सः", "एषः"] or primary in ["सस्", "एषस्"])
                and sv[0] in expand_pratyahaara("हल्")
            ):
                df = एतत्तदोः_सुलोपोऽकोरनञ्समासे_हलि(df)
            elif pv[-1] == "स्":
                df = ससजुषो_रुः(df)
                if secondary in avasaana:
                    df = खरवसानयोर्विसर्जनीयः(df)
                else:
                    if sv[0] in expand_pratyahaara("खर्"):
                        df = खरवसानयोर्विसर्जनीयः(df)
                    else:
                        if primary in ["भोस्", "भगोस्", "अघोस्"]:
                            df = भोभगोअघोअपूर्वस्य_योऽशि(df)
                        elif pv[-2] == "अ":
                            if sv[0] == "अ":
                                df = अतो_रोरप्लुतादप्लुते(df)
                            elif sv[0] in expand_pratyahaara("हश्"):
                                df = हशि_च(df)
                            else:
                                df = भोभगोअघोअपूर्वस्य_योऽशि(df)
                        elif pv[-2] == "आ":
                            df = भोभगोअघोअपूर्वस्य_योऽशि(df)
                        elif sv[0] == "र्":
                            df = रो_रि(df)
            else:
                if pv[-1] in expand_pratyahaara("झल्"):
                    df = झलां_जशोऽन्ते(df)
                elif secondary not in avasaana and pv[-1] == "र्" and sv[0] == "र्":
                    df = रो_रि(df)
                elif pv[-1] == "र्" and (secondary in avasaana or sv[0] in expand_pratyahaara("खर्")):
                    df = खरवसानयोर्विसर्जनीयः(df)
                elif secondary in avasaana:
                    pass
                elif pv[-1] == "म्" and secondary not in avasaana:
                    if sv[0] in expand_pratyahaara("हल्"):
                        df = मोऽनुस्वारः(df)
                elif secondary not in avasaana and pv[-1] == "न्" and sv[0] in expand_pratyahaara("छव्"):
                    df = नश्छव्यप्रशान्(df)
                elif secondary not in avasaana and pv[-1] == "न्" and sv[0] == "ल्":
                    df = तोर्लि(df)
                elif secondary not in avasaana and pv[-1] == "न्" and sv[0] in ["श्", "च्", "छ्", "ज्", "झ्", "ञ्"]:
                    df = स्तोः_श्चुना_श्चुः(df)
                elif secondary not in avasaana and pv[-1] in expand_pratyahaara("हल्") and sv[0] in expand_pratyahaara("अच्"):
                    if pv[-1] in expand_pratyahaara("ङम्") and pv[-2] in ["अ", "इ", "उ", "ऋ", "ऌ"]:
                        df = ङमो_ह्रस्वादचि_ङमुण्नित्यम्(df)

        r = get_sthiti(df)

        if " " in r:
            dd.extend(get_vinyaasa(r.split(" ")[0]))
            dd.append(" ")
        else:
            if secondary in avasaana:
                dd.extend(get_vinyaasa(r))
                dd.append(" ")
                dd.append(secondary)
            else:
                flag = 1
                temp = r

        if not df.empty:
            prakriya = pd.concat([prakriya, df], ignore_index=True)

        sutra_list = list(df["सूत्र"])
        sutra_series = " ".join(sutra_list)

        row = {"पद समूह": s, "सूत्राणि": sutra_series, "संधि-कृत रूप": r}
        sandhi_summary = pd.concat([sandhi_summary, pd.DataFrame([row])], ignore_index=True)

    if flag == 1:
        dd.extend(get_vinyaasa(temp))
        dd.append(" ")
    elif len(mm) > 0:
        last_word = mm[-1]
        if last_word not in avasaana:
            if not any(last_word.endswith(av) for av in avasaana if av != " "):
                dd.extend(get_vinyaasa(last_word))
                dd.append(" ")
            else:
                for av in avasaana:
                    if av != " " and last_word.endswith(av):
                        word_part = last_word[: -len(av)]
                        if word_part:
                            dd.extend(get_vinyaasa(word_part))
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

        ee = get_shabda(ee)
    else:
        ee = ""

    prakriya.to_csv("prakriya.csv", index=False)
    sandhi_summary.to_csv("sandhi_summary.csv", index=False)

    return [ee, sandhi_summary, prakriya]
