import pandas as pd
from functools import lru_cache
from akshara.varnakaarya import get_vinyaasa, get_shabda

# ==========================================
# 1. VARNA LOGIC
# ==========================================
svara = list("अआइईउऊऋॠऌएऐओऔ")
maatraa = list("ािीुूृॄॢेैोौ")
anunaasika_svara = "अँ आँ इँ ईँ उँ ऊँ ऋँ ॠँ ऌँ एँ ऐँ ओँ औँ".split()
vyanjana = "क् ख् ग् घ् ङ् च् छ् ज् झ् ञ् ट् ठ् ड् ढ् ण् त् थ् द् ध् न् प् फ् ब् भ् म् य् र् ल् व् श् ष् स् ह्".split()
vyanjana_with_akaara = list("कखगघङचछजझञटठडढणतथदधनपफबभमयरलवशषसह")
avasaana = [" ", "।", "॥"]
maaheshwar_suutra = "अ इ उ ण् ऋ ऌ क् ए ओ ङ् ऐ औ च् ह य व र ट् ल ण् ञ म ङ ण न म् झ भ ञ् घ ढ ध ष् ज ब ग ड द श् ख फ छ ठ थ च ट त व् क प य् श ष स र् ह ल्".split()

maatraa_to_svara = dict(zip(maatraa, svara[1:]))
svara_to_maatraa = dict(zip(svara[1:], maatraa))

# ==========================================
# 2. PRATYAAHAARA LOGIC
# ==========================================
@lru_cache(maxsize=None)
def expand_pratyahaara(p):
    assert len(p) == 3
    assert p[2] == "्"

    start = p[0]
    stop = p[1] + p[2]

    i = maaheshwar_suutra.index(start)
    j = maaheshwar_suutra.index(stop)
    r = maaheshwar_suutra[i:j]

    it = [x for x in r if x in vyanjana]
    for ii in it:
        r.remove(ii)

    rr = [x + "्" if x in vyanjana_with_akaara else x for x in r]

    if "अ" in rr: rr.append("आ")
    if "इ" in rr: rr.append("ई")
    if "उ" in rr: rr.append("ऊ")

    return rr

# ==========================================
# 3. SUTRA LOGIC
# ==========================================
ACTIVE_SETTINGS = {}

def get_sthiti(df):
    return df[-1]["स्थिति"]

def remove_avasaana(s):
    f = 0
    for ii in range(len(s)):
        if s[ii] == " ":
            f = ii
            del s[f]
            return s
    return s

def aadesh(s, ii, aa):
    del s[ii]
    s[ii:ii] = get_vinyaasa(aa)
    return s

def pre_processing(df):
    return get_vinyaasa(df[-1]["स्थिति"])

def post_processing(df, s, name, number):
    s = get_shabda(s)
    t = f"[[{name} ({number})]]"
    df.append({"स्थिति": s, "सूत्र": t})
    return df

def तस्य_लोपः(df, ii):
    s = pre_processing(df)
    del s[ii]
    return post_processing(df, s, "तस्य लोपः", "1.3.9")

def इको_यणचि(df):
    s = pre_processing(df)
    s = remove_avasaana(s)
    yan_map = {"इ": "य्", "ई": "य्", "उ": "व्", "ऊ": "व्", "ऋ": "र्", "ॠ": "र्", "ऌ": "ल्"}
    for ii in range(len(s) - 1):
        if s[ii] in expand_pratyahaara("इक्") and s[ii + 1] in expand_pratyahaara("अच्"):
            if s[ii] in yan_map:
                s = aadesh(s, ii, yan_map[s[ii]])
                return post_processing(df, s, "इको यणचि", "6.1.77")
    return df

def एचोऽयवायावः(df):
    s = pre_processing(df)
    ayav_map = {"ए": "अय्", "ओ": "अव्", "ऐ": "आय्", "औ": "आव्"}
    for ii in range(len(s) - 1):
        if (s[ii] in expand_pratyahaara("एच्") and s[ii + 1] in expand_pratyahaara("अच्")) or (
            s[ii] in expand_pratyahaara("एच्") and s[ii + 1] == " " and s[ii + 2] in expand_pratyahaara("अच्")
        ):
            if s[ii] in ayav_map:
                aa = ayav_map[s[ii]]
                del s[ii]
                s[ii:ii] = get_vinyaasa(aa)
                df = post_processing(df, s, "एचोऽयवायावः", "6.1.78")
                if " " in s:
                    df = लोपः_शाकल्यस्य(df)
                return df
    return df

def आद्गुणः(df):
    s = pre_processing(df)
    gun_map = {"इ": "ए", "ई": "ए", "उ": "ओ", "ऊ": "ओ", "ऋ": "अर्", "ॠ": "अर्", "ऌ": "अल्"}
    for ii in range(len(s) - 1):
        if (s[ii] in ["अ", "आ"] and s[ii + 1] in expand_pratyahaara("अच्")) or (
            s[ii] in ["अ", "आ"] and s[ii + 1] == " " and s[ii + 2] in expand_pratyahaara("अच्")
        ):
            break
    else:
        return df

    if s[ii + 1] == " ": del s[ii + 1]
    temp = s[ii + 1]
    del s[ii + 1]

    if temp in gun_map:
        s = aadesh(s, ii, gun_map[temp])
        df = post_processing(df, s, "आद्गुणः", "6.1.87")
    return df

def वृद्धिरेचि(df):
    s = pre_processing(df)
    vriddhi_map = {"ए": "ऐ", "ऐ": "ऐ", "ओ": "औ", "औ": "औ"}
    for ii in range(len(s) - 1):
        if (s[ii] in ["अ", "आ"] and s[ii + 1] in expand_pratyahaara("एच्")) or (
            s[ii] in ["अ", "आ"] and s[ii + 1] == " " and s[ii + 2] in expand_pratyahaara("एच्")
        ):
            break
    else:
        return df

    if s[ii + 1] == " ": del s[ii + 1]
    temp = s[ii + 1]
    del s[ii + 1]

    if temp in vriddhi_map:
        s = aadesh(s, ii, vriddhi_map[temp])
        df = post_processing(df, s, "वृद्धिरेचि", "6.1.88")
    return df

def अकः_सवर्णे_दीर्घः(df):
    s = pre_processing(df)
    for ii in range(len(s) - 1):
        if (s[ii] in expand_pratyahaara("अक्") and s[ii + 1] in expand_pratyahaara("अक्")) or (
            s[ii] in expand_pratyahaara("अक्") and s[ii + 1] == " " and s[ii + 2] in expand_pratyahaara("अक्")
        ):
            break
    else:
        return df

    if s[ii + 1] == " ": del s[ii + 1]
    temp = s[ii + 1]
    del s[ii + 1]

    aa = None
    if temp in ["अ", "आ"] and s[ii] in ["अ", "आ"]: aa = "आ"
    elif temp in ["इ", "ई"] and s[ii] in ["इ", "ई"]: aa = "ई"
    elif temp in ["उ", "ऊ"] and s[ii] in ["उ", "ऊ"]: aa = "ऊ"
    elif temp in ["ऋ", "ॠ", "ऌ"] and s[ii] in ["ऋ", "ॠ", "ऌ"]: aa = "ॠ"
    
    if aa:
        aadesh(s, ii, aa)
        df = post_processing(df, s, "अकः सवर्णे दीर्घः", "6.1.101")
    return df

def एङः_पदान्तादति(df):
    s = pre_processing(df)
    if " " in s:
        ii = s.index(" ")
        if s[ii - 1] in expand_pratyahaara("एङ्") and s[ii + 1] == "अ":
            del s[ii]
            aadesh(s, ii, "ऽ")
            df = post_processing(df, s, "एङः पदान्तादति", "6.1.109")
    return df

def अतो_रोरप्लुतादप्लुते(df):
    s = pre_processing(df)
    if " " in s:
        ii = s.index(" ")
        if s[ii - 2] == "अ" and s[ii + 1] == "अ" and s[ii - 1] == "र्":
            aadesh(s, ii - 1, " उ")
            df = post_processing(df, s, "अतो रोरप्लुतादप्लुते", "6.1.113")
            df = आद्गुणः(df)
            df = एङः_पदान्तादति(df)
    return df

def हशि_च(df):
    s = pre_processing(df)
    if " " in s:
        ii = s.index(" ")
        if (s[ii - 2] == "अ" and s[ii + 1] in expand_pratyahaara("हश्") and s[ii - 1] == "र्"):
            aadesh(s, ii - 1, " उ")
            df = post_processing(df, s, "हशि च", "6.1.114")
            df = आद्गुणः(df)
    return df

def एतत्तदोः_सुलोपोऽकोरनञ्समासे_हलि(df):
    s = pre_processing(df)
    if " " in s:
        ii = s.index(" ")
        if s[ii - 1] == "स्" and s[ii + 1] in expand_pratyahaara("हल्"):
            del s[ii - 1]
            df = post_processing(df, s, "एतत्तदोः सुलोपोऽकोरनञ्समासे हलि", "6.1.132")
    return df

def एङि_पररूपम्(df):
    s = pre_processing(df)
    if " " in s:
        ii = s.index(" ")
        temp = s[ii + 1]
        del s[ii + 1]
        s = aadesh(s, ii - 1, temp)
        if " " in s:
            s.remove(" ")
        df = post_processing(df, s, "एङि पररूपम्", "6.1.94")
    return df

def छे_च(df):
    s = pre_processing(df)
    if " " in s:
        ii = s.index(" ")
        s.insert(ii, "च्")
        s.remove(" ")
        df = post_processing(df, s, "छे च", "6.1.73")
    return df

def रो_रि(df):
    s = pre_processing(df)
    if " " in s:
        ii = s.index(" ")
        if s[ii - 1] == "र्" and s[ii + 1] == "र्":
            del s[ii - 1]
            df = post_processing(df, s, "रो रि", "8.3.14")
            
            s = pre_processing(df)
            ii = s.index(" ")
            prev_vowel = s[ii - 1]
            if prev_vowel in ["अ", "इ", "उ"]:
                aa = {"अ": "आ", "इ": "ई", "उ": "ऊ"}[prev_vowel]
                s = aadesh(s, ii - 1, aa)
                df = post_processing(df, s, "ढ्रलोपे पूर्वस्य दीर्घोऽणः", "6.3.111")
    return df

def झलां_जशोऽन्ते(df):
    s = pre_processing(df)
    jash_map = {
        "च्": "ग्", "छ्": "ग्", "ज्": "ग्", "झ्": "ग्",
        "क्": "ग्", "ख्": "ग्", "ग्": "ग्", "घ्": "ग्", "ह्": "ग्",
        "ट्": "ड्", "ठ्": "ड्", "ड्": "ड्", "ढ्": "ड्", "ष्": "ड्",
        "त्": "द्", "थ्": "द्", "द्": "द्", "ध्": "द्", "स्": "द्",
        "प्": "ब्", "फ्": "ब्", "ब्": "ब्", "भ्": "ब्", "श्": "ड्"
    }
    modified = False
    
    if " " in s:
        ii = s.index(" ")
        if s[ii - 1] in expand_pratyahaara("झल्"):
            word_str = get_shabda(s[:ii])
            aa = "ड्" if word_str.endswith("राज्") or word_str.endswith("भ्राज्") else jash_map.get(s[ii - 1], s[ii - 1])
            s = aadesh(s, ii - 1, aa)
            modified = True
            
    elif len(s) > 0 and s[-1] in expand_pratyahaara("झल्"):
        ii = len(s)
        word_str = get_shabda(s[:ii])
        aa = "ड्" if word_str.endswith("राज्") or word_str.endswith("भ्राज्") else jash_map.get(s[ii - 1], s[ii - 1])
        s = aadesh(s, ii - 1, aa)
        modified = True

    if modified:
        df = post_processing(df, s, "झलां जशोऽन्ते", "8.2.39")

    s = pre_processing(df)
    if " " in s:
        ii = s.index(" ")
        l1 = ["स्", "त्", "थ्", "द्", "ध्", "न्"]
        l2 = ["श्", "च्", "छ्", "ज्", "झ्", "ञ्"]
        l3 = ["ष्", "ट्", "ठ्", "ड्", "ढ्", "ण्"]

        if (s[ii - 1] in l1 and s[ii + 1] in l2) or (s[ii - 1] in l2 and s[ii + 1] in l1):
            df = स्तोः_श्चुना_श्चुः(df)
        elif (s[ii - 1] in l1 and s[ii + 1] in l3) or (s[ii - 1] in l3 and s[ii + 1] in l1):
            df = ष्टुना_ष्टुः(df)

        s = pre_processing(df)
        if " " in s:
            ii = s.index(" ")
            if s[ii - 1] in expand_pratyahaara("यर्") and s[ii + 1] in expand_pratyahaara("ञम्"):
                df = यरोऽनुनासिकेऽनुनासिको_वा(df)
            if s[ii + 1] in expand_pratyahaara("खर्"):
                df = खरि_च(df)
            if s[ii + 1] == "ल्":
                df = तोर्लि(df)
            if s[ii - 1] in expand_pratyahaara("झय्") and s[ii + 1] == "ह्":
                df = झयो_होऽन्यतरस्याम्(df)

    elif " " not in s:
        df = वाऽवसाने(df)
    return df

def ससजुषो_रुः(df):
    s = pre_processing(df)
    if " " in s and s[s.index(" ") - 1] == "स्": ii = s.index(" ") - 1
    elif s[-1] == "स्": ii = len(s) - 1
    else: return df
    s = aadesh(s, ii, "रुँ")
    df = post_processing(df, s, "ससजुषो रुः", "8.2.66")
    return तस्य_लोपः(df, ii + 1)

def नश्छव्यप्रशान्(df):
    s = pre_processing(df)
    if " " in s:
        ii = s.index(" ")
        if s[ii - 1] == "न्" and s[ii + 1] in expand_pratyahaara("छव्"):
            s = aadesh(s, ii - 1, "रुँ")
            s[ii - 1 : ii - 1] = "ं"
            df = post_processing(df, s, "नश्छव्यप्रशान्", "8.3.7")
            df = तस्य_लोपः(df, ii + 1)
            df = खरवसानयोर्विसर्जनीयः(df)
    return df

def खरवसानयोर्विसर्जनीयः(df):
    s = pre_processing(df)
    modified = False
    if " " in s:
        ii = s.index(" ")
        if s[ii - 1] == "र्" and s[ii + 1] in expand_pratyahaara("खर्"):
            aadesh(s, ii - 1, "ः")
            modified = True
    elif s[-1] == "र्":
        aadesh(s, len(s) - 1, "ः")
        modified = True

    if modified:
        df = post_processing(df, s, "खरवसानयोर्विसर्जनीयः", "8.3.15")

    s = pre_processing(df)
    if " " in s:
        ii = s.index(" ")
        if s[ii + 2] in expand_pratyahaara("शर्"):
            df = शर्परे_विसर्जनीयः(df)
        elif s[ii + 1] in expand_pratyahaara("शर्"):
            if ACTIVE_SETTINGS.get("vaa_shari", True):
                df = वा_शरि(df)
            else:
                df = विसर्जनीयस्य_सः(df)
        elif s[ii + 1] in ["क्", "ख्", "प्", "फ्"]:
            df = कुप्वोः_कपौ_च(df)
        else:
            df = विसर्जनीयस्य_सः(df)
    return df

def भोभगोअघोअपूर्वस्य_योऽशि(df):
    s = pre_processing(df)
    if " " in s:
        ii = s.index(" ")
        if (s[ii - 1] == "र्" and s[ii + 1] in expand_pratyahaara("अश्") and (s[ii - 2] in ["अ", "आ"] or get_shabda(s[ii - 3 : ii]) == "भोर्" or get_shabda(s[ii - 5 : ii]) in ["भगोर्", "अघोर्"])):
            s = aadesh(s, ii - 1, "य्")
            df = post_processing(df, s, "भोभगोअघोअपूर्वस्य योऽशि", "8.3.17")

    s = pre_processing(df)
    if " " in s:
        ii = s.index(" ")
        if s[ii + 1] in expand_pratyahaara("हल्"):
            df = हलि_सर्वेषाम्(df)
        elif s[ii - 2] == "ओ":
            df = ओतो_गार्ग्यस्य(df)
        else:
            df = लोपः_शाकल्यस्य(df)
    return df

def लोपः_शाकल्यस्य(df):
    s = pre_processing(df)
    if " " in s:
        ii = s.index(" ")
        if s[ii - 1] in ["य्", "व्"] and s[ii + 1] in expand_pratyahaara("अच्"):
            if ACTIVE_SETTINGS.get("lopa_shakalyasya", True):
                del s[ii - 1]
            else:
                s.remove(" ")
            df = post_processing(df, s, "लोपः शाकल्यस्य", "8.3.19")
    return df

def ओतो_गार्ग्यस्य(df):
    s = pre_processing(df)
    if " " in s:
        ii = s.index(" ")
        if s[ii - 1] in ["य्", "व्"] and s[ii + 1] in expand_pratyahaara("अश्"):
            if ACTIVE_SETTINGS.get("lopa_shakalyasya", True):
                del s[ii - 1]
            else:
                s.remove(" ")
            df = post_processing(df, s, "ओतो गार्ग्यस्य", "8.3.20")
    return df

def हलि_सर्वेषाम्(df):
    s = pre_processing(df)
    if " " in s:
        ii = s.index(" ")
        if s[ii - 1] in ["य्", "व्"] and s[ii + 1] in expand_pratyahaara("हल्"):
            del s[ii - 1]
            df = post_processing(df, s, "हलि सर्वेषाम्", "8.3.22")
    return df

def मोऽनुस्वारः(df):
    s = pre_processing(df)
    if " " in s:
        ii = s.index(" ")
        if s[ii - 1] == "म्" and s[ii + 1] in expand_pratyahaara("हल्"):
            s = aadesh(s, ii - 1, "ं")
            df = post_processing(df, s, "मोऽनुस्वारः", "8.3.23")
    return df

def ङमो_ह्रस्वादचि_ङमुण्नित्यम्(df):
    s = pre_processing(df)
    if " " in s:
        ii = s.index(" ")
        temp = s[ii - 1]
        s[ii:ii] = get_vinyaasa(temp)
        df = post_processing(df, s, "ङमो ह्रस्वादचि ङमुण्नित्यम्", "8.3.32")
    return df

def विसर्जनीयस्य_सः(df):
    s = pre_processing(df)
    if " " in s:
        ii = s.index(" ")
        if s[ii - 1] == "ः" and s[ii + 1] in expand_pratyahaara("खर्"):
            aadesh(s, ii - 1, "स्")
            df = post_processing(df, s, "विसर्जनीयस्य सः", "8.3.34")
            
            s = pre_processing(df)
            ii = s.index(" ")
            if s[ii - 1] == "स्" and s[ii + 1] in ["श्", "च्", "छ्", "ज्", "झ्", "ञ्"]:
                df = स्तोः_श्चुना_श्चुः(df)
            elif s[ii - 1] == "स्" and s[ii + 1] in ["ष्", "ट्", "ठ्", "ड्", "ढ्", "ण्"]:
                df = ष्टुना_ष्टुः(df)
    return df

def शर्परे_विसर्जनीयः(df):
    s = pre_processing(df)
    return post_processing(df, s, "शर्परे विसर्जनीयः", "8.3.35")

def वा_शरि(df):
    s = pre_processing(df)
    return post_processing(df, s, "वा शरि", "8.3.36")

def कुप्वोः_कपौ_च(df):
    s = pre_processing(df)
    if " " in s:
        ii = s.index(" ")
        if s[ii - 1] == "ः" and s[ii + 1] in ["क्", "ख्"]:
            s = aadesh(s, ii - 1, "ᳲ")
        elif s[ii - 1] == "ः" and s[ii + 1] in ["प्", "फ्"]:
            s = aadesh(s, ii - 1, "ᳳ")
        df = post_processing(df, s, "कुप्वोः ≍क≍पौ च", "8.3.37")
    return df

def स्तोः_श्चुना_श्चुः(df):
    s = pre_processing(df)
    if " " in s:
        ii = s.index(" ")
        schu_map = {"स्": "श्", "त्": "च्", "थ्": "छ्", "द्": "ज्", "ध्": "झ्", "न्": "ञ्"}
        if s[ii - 1] in schu_map:
            s = aadesh(s, ii - 1, schu_map[s[ii - 1]])
        elif s[ii + 1] in schu_map:
            s = aadesh(s, ii + 1, schu_map[s[ii + 1]])
        df = post_processing(df, s, "स्तोः श्चुना श्चुः", "8.4.40")
    return df

def ष्टुना_ष्टुः(df):
    s = pre_processing(df)
    if " " in s:
        ii = s.index(" ")
        shtu_map = {"स्": "ष्", "त्": "ट्", "थ्": "ठ्", "द्": "ड्", "ध्": "ढ्", "न्": "ण्"}
        if s[ii - 1] in shtu_map:
            s = aadesh(s, ii - 1, shtu_map[s[ii - 1]])
        elif s[ii + 1] in shtu_map:
            s = aadesh(s, ii + 1, shtu_map[s[ii + 1]])
        df = post_processing(df, s, "ष्टुना ष्टुः", "8.4.41")
    return df

def यरोऽनुनासिकेऽनुनासिको_वा(df):
    s = pre_processing(df)
    if " " in s:
        ii = s.index(" ")
        if ACTIVE_SETTINGS.get("yaro_anunasike", True):
            anunasika_map = {
                "क्": "ङ्", "ख्": "ङ्", "ग्": "ङ्", "घ्": "ङ्",
                "च्": "ञ्", "छ्": "ञ्", "ज्": "ञ्", "झ्": "ञ्",
                "ट्": "ण्", "ठ्": "ण्", "ड्": "ण्", "ढ्": "ण्",
                "त्": "न्", "थ्": "न्", "द्": "न्", "ध्": "न्",
                "प्": "म्", "फ्": "म्", "ब्": "म्", "भ्": "म्"
            }
            if s[ii - 1] in anunasika_map:
                s = aadesh(s, ii - 1, anunasika_map[s[ii - 1]])
        df = post_processing(df, s, "यरोऽनुनासिकेऽनुनासिको वा", "8.4.45")
    return df

def खरि_च(df):
    s = pre_processing(df)
    if " " in s:
        ii = s.index(" ")
        khar_map = {
            "ग्": "क्", "घ्": "क्", "ज्": "च्", "झ्": "च्",
            "ड्": "ट्", "ढ्": "ट्", "द्": "त्", "ध्": "त्",
            "ब्": "प्", "भ्": "प्"
        }
        if s[ii - 1] in khar_map:
            s = aadesh(s, ii - 1, khar_map[s[ii - 1]])
        df = post_processing(df, s, "खरि च", "8.4.55")
    return df

def वाऽवसाने(df):
    s = pre_processing(df)
    avasana_map = {
        "ग्": "क्", "घ्": "क्", "ज्": "च्", "झ्": "च्",
        "ड्": "ट्", "ढ्": "ट्", "द्": "त्", "ध्": "त्",
        "ब्": "प्", "भ्": "प्"
    }
    if s[-1] in avasana_map:
        s = aadesh(s, len(s) - 1, avasana_map[s[-1]])
        df = post_processing(df, s, "वाऽवसाने", "8.4.56")
    return df

def तोर्लि(df):
    s = pre_processing(df)
    if " " in s:
        ii = s.index(" ")
        if s[ii - 1] == "न्":
            s = aadesh(s, ii - 1, "ल्ँ")
        elif s[ii - 1] in ["त्", "थ्", "द्", "ध्"]:
            s = aadesh(s, ii - 1, "ल्")
        df = post_processing(df, s, "तोर्लि", "8.4.60")
    return df

def झयो_होऽन्यतरस्याम्(df):
    s = pre_processing(df)
    if " " in s:
        ii = s.index(" ")
        if ACTIVE_SETTINGS.get("jhayo_ho", True):
            h_map = {
                "क्": "घ्", "ग्": "घ्", "च्": "झ्", "ज्": "झ्",
                "ट्": "ढ्", "ड्": "ढ्", "त्": "ध्", "द्": "ध्",
                "प्": "भ्", "ब्": "भ्"
            }
            if s[ii - 1] in h_map:
                s = aadesh(s, ii + 1, h_map[s[ii - 1]])
        df = post_processing(df, s, "झयो होऽन्यतरस्याम्", "8.4.62")
    return df

def शशछोऽटि(df):
    s = pre_processing(df)
    if " " in s:
        ii = s.index(" ")
        if ACTIVE_SETTINGS.get("shashcho_ati", True):
            if s[ii + 1] == "श्":
                s = aadesh(s, ii + 1, "छ्")
        df = post_processing(df, s, "शशछोऽटि", "8.4.63")
    return df

# ==========================================
# 4. VAAKYA SANDHI LOGIC
# ==========================================
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
    global ACTIVE_SETTINGS
    ACTIVE_SETTINGS.clear()
    if settings:
        ACTIVE_SETTINGS.update(settings)
    
    prakriya_rows = []
    sandhi_summary_rows = []
    
    dd = []
    flag = 0
    temp = ""
    
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
            
        df = [{"स्थिति": s, "सूत्र": "-"}]
        
        if pv and sv:
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

        r = df[-1]["स्थिति"]

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

        if len(df) > 0:
            prakriya_rows.extend(df)

        sutra_list = [row["सूत्र"] for row in df]
        sutra_series = " ".join(sutra_list)

        sandhi_summary_rows.append({"पद समूह": s, "सूत्राणि": sutra_series, "संधि-कृत रूप": r})

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

    prakriya = pd.DataFrame(prakriya_rows)
    sandhi_summary = pd.DataFrame(sandhi_summary_rows)

    if lang == "संस्कृतम्" and not prakriya.empty:
        prakriya["सूत्र"] = prakriya["सूत्र"].apply(eng_to_devanagari)
        sandhi_summary["सूत्राणि"] = sandhi_summary["सूत्राणि"].apply(eng_to_devanagari)

    return [ee, sandhi_summary, prakriya]
