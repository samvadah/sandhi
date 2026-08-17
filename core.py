import pandas as pd
from functools import lru_cache
from akshara.varnakaarya import get_vinyaasa, get_shabda

# ==========================================
# 1. VARNA CONSTANTS
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

def get_sthiti(df_list):
    return df_list[-1]["स्थिति"]

def remove_avasaana(s):
    for ii in range(len(s)):
        if s[ii] == " ":
            del s[ii]
            return s
    return s

def aadesh(s, ii, aa):
    del s[ii]
    s[ii:ii] = get_vinyaasa(aa)
    return s

def pre_processing(df_list):
    return get_vinyaasa(df_list[-1]["स्थिति"])

def post_processing(df_list, s, name, number):
    s = get_shabda(s)
    t = f"[[{name} ({number})]]"
    df_list.append({"स्थिति": s, "सूत्र": t})
    return df_list

def तस्य_लोपः(df_list, ii=None):
    s = pre_processing(df_list)
    # Safely removes the marker regardless of shifting indices
    if "उँ" in s:
        s.remove("उँ")
    elif "उ" in s and "ँ" in s:
        s.remove("उ")
        s.remove("ँ")
    elif ii is not None and ii < len(s):
        del s[ii]
    return post_processing(df_list, s, "तस्य लोपः", "1.3.9")

def इको_यणचि(df_list):
    s = pre_processing(df_list)
    s = remove_avasaana(s)
    yan_map = {"इ": "य्", "ई": "य्", "उ": "व्", "ऊ": "व्", "ऋ": "र्", "ॠ": "र्", "ऌ": "ल्"}
    for ii in range(len(s) - 1):
        if s[ii] in expand_pratyahaara("इक्") and s[ii + 1] in expand_pratyahaara("अच्"):
            if s[ii] in yan_map:
                s = aadesh(s, ii, yan_map[s[ii]])
                return post_processing(df_list, s, "इको यणचि", "6.1.77")
    return df_list

def एचोऽयवायावः(df_list):
    s = pre_processing(df_list)
    ayav_map = {"ए": "अय्", "ओ": "अव्", "ऐ": "आय्", "औ": "आव्"}
    for ii in range(len(s) - 1):
        if (s[ii] in expand_pratyahaara("एच्") and s[ii + 1] in expand_pratyahaara("अच्")) or (
            s[ii] in expand_pratyahaara("एच्") and s[ii + 1] == " " and len(s) > ii + 2 and s[ii + 2] in expand_pratyahaara("अच्")
        ):
            if s[ii] in ayav_map:
                aa = ayav_map[s[ii]]
                del s[ii]
                s[ii:ii] = get_vinyaasa(aa)
                df_list = post_processing(df_list, s, "एचोऽयवायावः", "6.1.78")
                if " " in s:
                    df_list = लोपः_शाकल्यस्य(df_list)
                return df_list
    return df_list

def आद्गुणः(df_list):
    s = pre_processing(df_list)
    gun_map = {"इ": "ए", "ई": "ए", "उ": "ओ", "ऊ": "ओ", "ऋ": "अर्", "ॠ": "अर्", "ऌ": "अल्"}
    for ii in range(len(s) - 1):
        if (s[ii] in ["अ", "आ"] and s[ii + 1] in expand_pratyahaara("अच्")) or (
            s[ii] in ["अ", "आ"] and s[ii + 1] == " " and len(s) > ii + 2 and s[ii + 2] in expand_pratyahaara("अच्")
        ):
            break
    else:
        return df_list

    if s[ii + 1] == " ": del s[ii + 1]
    temp = s[ii + 1]
    del s[ii + 1]

    if temp in gun_map:
        s = aadesh(s, ii, gun_map[temp])
        df_list = post_processing(df_list, s, "आद्गुणः", "6.1.87")
    return df_list

def वृद्धिरेचि(df_list):
    s = pre_processing(df_list)
    vriddhi_map = {"ए": "ऐ", "ऐ": "ऐ", "ओ": "औ", "औ": "औ"}
    for ii in range(len(s) - 1):
        if (s[ii] in ["अ", "आ"] and s[ii + 1] in expand_pratyahaara("एच्")) or (
            s[ii] in ["अ", "आ"] and s[ii + 1] == " " and len(s) > ii + 2 and s[ii + 2] in expand_pratyahaara("एच्")
        ):
            break
    else:
        return df_list

    if s[ii + 1] == " ": del s[ii + 1]
    temp = s[ii + 1]
    del s[ii + 1]

    if temp in vriddhi_map:
        s = aadesh(s, ii, vriddhi_map[temp])
        df_list = post_processing(df_list, s, "वृद्धिरेचि", "6.1.88")
    return df_list

def अकः_सवर्णे_दीर्घः(df_list):
    s = pre_processing(df_list)
    for ii in range(len(s) - 1):
        if (s[ii] in expand_pratyahaara("अक्") and s[ii + 1] in expand_pratyahaara("अक्")) or (
            s[ii] in expand_pratyahaara("अक्") and s[ii + 1] == " " and len(s) > ii + 2 and s[ii + 2] in expand_pratyahaara("अक्")
        ):
            break
    else:
        return df_list

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
        df_list = post_processing(df_list, s, "अकः सवर्णे दीर्घः", "6.1.101")
    return df_list

def एङः_पदान्तादति(df_list):
    s = pre_processing(df_list)
    if " " in s:
        ii = s.index(" ")
        if ii >= 1 and len(s) > ii + 1 and s[ii - 1] in expand_pratyahaara("एङ्") and s[ii + 1] == "अ":
            del s[ii]
            aadesh(s, ii, "ऽ")
            df_list = post_processing(df_list, s, "एङः पदान्तादति", "6.1.109")
    return df_list

def अतो_रोरप्लुतादप्लुते(df_list):
    s = pre_processing(df_list)
    if " " in s:
        ii = s.index(" ")
        if ii >= 2 and len(s) > ii + 1 and s[ii - 2] == "अ" and s[ii + 1] == "अ" and s[ii - 1] == "र्":
            aadesh(s, ii - 1, " उ")
            df_list = post_processing(df_list, s, "अतो रोरप्लुतादप्लुते", "6.1.113")
            df_list = आद्गुणः(df_list)
            df_list = एङः_पदान्तादति(df_list)
    return df_list

def हशि_च(df_list):
    s = pre_processing(df_list)
    if " " in s:
        ii = s.index(" ")
        if ii >= 2 and len(s) > ii + 1 and s[ii - 2] == "अ" and s[ii + 1] in expand_pratyahaara("हश्") and s[ii - 1] == "र्":
            aadesh(s, ii - 1, " उ")
            df_list = post_processing(df_list, s, "हशि च", "6.1.114")
            df_list = आद्गुणः(df_list)
    return df_list

def एतत्तदोः_सुलोपोऽकोरनञ्समासे_हलि(df_list):
    s = pre_processing(df_list)
    if " " in s:
        ii = s.index(" ")
        if ii >= 1 and len(s) > ii + 1 and s[ii - 1] == "स्" and s[ii + 1] in expand_pratyahaara("हल्"):
            del s[ii - 1]
            df_list = post_processing(df_list, s, "एतत्तदोः सुलोपोऽकोरनञ्समासे हलि", "6.1.132")
    return df_list

def एङि_पररूपम्(df_list):
    s = pre_processing(df_list)
    if " " in s:
        ii = s.index(" ")
        if len(s) > ii + 1:
            temp = s[ii + 1]
            del s[ii + 1]
            s = aadesh(s, ii - 1, temp)
            if " " in s:
                s.remove(" ")
            df_list = post_processing(df_list, s, "एङि पररूपम्", "6.1.94")
    return df_list

def छे_च(df_list):
    s = pre_processing(df_list)
    if " " in s:
        ii = s.index(" ")
        s.insert(ii, "च्")
        s.remove(" ")
        df_list = post_processing(df_list, s, "छे च", "6.1.73")
    return df_list

def रो_रि(df_list):
    s = pre_processing(df_list)
    if " " in s:
        ii = s.index(" ")
        if ii >= 1 and len(s) > ii + 1 and s[ii - 1] == "र्" and s[ii + 1] == "र्":
            del s[ii - 1]
            df_list = post_processing(df_list, s, "रो रि", "8.3.14")
            
            s = pre_processing(df_list)
            if " " in s:
                ii = s.index(" ")
                prev_vowel = s[ii - 1]
                if prev_vowel in ["अ", "इ", "उ"]:
                    aa = {"अ": "आ", "इ": "ई", "उ": "ऊ"}[prev_vowel]
                    s = aadesh(s, ii - 1, aa)
                    df_list = post_processing(df_list, s, "ढ्रलोपे पूर्वस्य दीर्घोऽणः", "6.3.111")
    return df_list

def झलां_जशोऽन्ते(df_list):
    s = pre_processing(df_list)
    
    # Original exact logic from Simplify branch
    if " " in s:
        ii = s.index(" ")
        if ii >= 1 and s[ii - 1] in expand_pratyahaara("झल्"):
            word_str = get_shabda(s[:ii])
            if word_str.endswith("राज्") or word_str.endswith("भ्राज्"): aa = "ड्" 
            elif s[ii - 1] in ["च्", "छ्", "ज्", "झ्"]: aa = "ग्"
            elif s[ii - 1] in ["क्", "ख्", "ग्", "घ्", "ह्"]: aa = "ग्"
            elif s[ii - 1] in ["ट्", "ठ्", "ड्", "ढ्", "ष्"]: aa = "ड्"
            elif s[ii - 1] in ["त्", "थ्", "द्", "ध्", "स्"]: aa = "द्"
            elif s[ii - 1] in ["प्", "फ्", "ब्", "भ्"]: aa = "ब्"
            elif s[ii - 1] == "श्": aa = "ड्"
            else: aa = s[ii - 1] 
            s = aadesh(s, ii - 1, aa)

    elif len(s) > 0 and s[-1] in expand_pratyahaara("झल्"):
        ii = len(s)
        word_str = get_shabda(s[:ii])
        if word_str.endswith("राज्") or word_str.endswith("भ्राज्"): aa = "ड्"
        elif s[ii - 1] in ["च्", "छ्", "ज्", "झ्"]: aa = "ग्"
        elif s[ii - 1] in ["क्", "ख्", "ग्", "घ्", "ह्"]: aa = "ग्"
        elif s[ii - 1] in ["ट्", "ठ्", "ड्", "ढ्", "ष्"]: aa = "ड्"
        elif s[ii - 1] in ["त्", "थ्", "द्", "ध्", "स्"]: aa = "द्"
        elif s[ii - 1] in ["प्", "फ्", "ब्", "भ्"]: aa = "ब्"
        elif s[ii - 1] == "श्": aa = "ड्"
        else: aa = s[ii - 1]
        s = aadesh(s, ii - 1, aa)

    df_list = post_processing(df_list, s, "झलां जशोऽन्ते", "8.2.39")

    # Original full nested cascade from Simplify branch
    if " " in s:
        ii = s.index(" ")
        l1 = ["स्", "त्", "थ्", "द्", "ध्", "न्"]
        l2 = ["श्", "च्", "छ्", "ज्", "झ्", "ञ्"]
        l3 = ["ष्", "ट्", "ठ्", "ड्", "ढ्", "ण्"]

        if ii >= 1 and len(s) > ii + 1:
            if (s[ii - 1] in l1 and s[ii + 1] in l2) or (s[ii - 1] in l2 and s[ii + 1] in l1):
                df_list = स्तोः_श्चुना_श्चुः(df_list)
            elif (s[ii - 1] in l1 and s[ii + 1] in l3) or (s[ii - 1] in l3 and s[ii + 1] in l1):
                df_list = ष्टुना_ष्टुः(df_list)

    s = pre_processing(df_list)
    if " " in s:
        ii = s.index(" ")
        if ii >= 1 and len(s) > ii + 1:
            if s[ii - 1] in expand_pratyahaara("यर्") and s[ii + 1] in expand_pratyahaara("ञम्"):
                df_list = यरोऽनुनासिकेऽनुनासिको_वा(df_list)
        
        # State refreshes to gracefully handle moving indices
        s = pre_processing(df_list)
        ii = s.index(" ") if " " in s else -1
        if ii >= 1 and len(s) > ii + 1:
            if s[ii + 1] in expand_pratyahaara("खर्"):
                df_list = खरि_च(df_list)
        
        s = pre_processing(df_list)
        ii = s.index(" ") if " " in s else -1
        if ii >= 1 and len(s) > ii + 1:
            if s[ii + 1] == "ल्":
                df_list = तोर्लि(df_list)

        s = pre_processing(df_list)
        ii = s.index(" ") if " " in s else -1
        if ii >= 1 and len(s) > ii + 1:
            if s[ii - 1] in expand_pratyahaara("झय्") and s[ii + 1] == "श्":
                df_list = शशछोऽटि(df_list)
                
        s = pre_processing(df_list)
        ii = s.index(" ") if " " in s else -1
        if ii >= 1 and len(s) > ii + 1:
            if s[ii - 1] in expand_pratyahaara("झय्") and s[ii + 1] == "ह्":
                df_list = झयो_होऽन्यतरस्याम्(df_list)

    elif " " not in s:
        df_list = वाऽवसाने(df_list)
        
    return df_list

def ससजुषो_रुः(df_list):
    s = pre_processing(df_list)
    if " " in s and s.index(" ") >= 1 and s[s.index(" ") - 1] == "स्": 
        ii = s.index(" ") - 1
    elif len(s) > 0 and s[-1] == "स्": 
        ii = len(s) - 1
    else: 
        return df_list
        
    s = aadesh(s, ii, "रुँ")
    df_list = post_processing(df_list, s, "ससजुषो रुः", "8.2.66")
    df_list = तस्य_लोपः(df_list)
    return df_list

def नश्छव्यप्रशान्(df_list):
    s = pre_processing(df_list)
    if " " in s:
        ii = s.index(" ")
        if ii >= 1 and len(s) > ii + 1 and s[ii - 1] == "न्" and s[ii + 1] in expand_pratyahaara("छव्"):
            s = aadesh(s, ii - 1, "रुँ")
            s.insert(ii - 1, "ं")
            df_list = post_processing(df_list, s, "नश्छव्यप्रशान्", "8.3.7")
            df_list = तस्य_लोपः(df_list)
            df_list = खरवसानयोर्विसर्जनीयः(df_list)
    return df_list

def खरवसानयोर्विसर्जनीयः(df_list):
    s = pre_processing(df_list)
    modified = False
    if " " in s:
        ii = s.index(" ")
        if ii >= 1 and len(s) > ii + 1 and s[ii - 1] == "र्" and s[ii + 1] in expand_pratyahaara("खर्"):
            aadesh(s, ii - 1, "ः")
            modified = True
    elif len(s) > 0 and s[-1] == "र्":
        aadesh(s, len(s) - 1, "ः")
        modified = True

    if modified:
        df_list = post_processing(df_list, s, "खरवसानयोर्विसर्जनीयः", "8.3.15")

    s = pre_processing(df_list)
    if " " in s:
        ii = s.index(" ")
        if len(s) > ii + 2 and s[ii + 2] in expand_pratyahaara("शर्"):
            df_list = शर्परे_विसर्जनीयः(df_list)
        elif len(s) > ii + 1 and s[ii + 1] in expand_pratyahaara("शर्"):
            if ACTIVE_SETTINGS.get("vaa_shari", True):
                df_list = वा_शरि(df_list)
            else:
                df_list = विसर्जनीयस्य_सः(df_list)
        elif len(s) > ii + 1 and s[ii + 1] in ["क्", "ख्", "प्", "फ्"]:
            df_list = कुप्वोः_कपौ_च(df_list)
        elif len(s) > ii + 1:
            df_list = विसर्जनीयस्य_सः(df_list)
    return df_list

def भोभगोअघोअपूर्वस्य_योऽशि(df_list):
    s = pre_processing(df_list)
    if " " in s:
        ii = s.index(" ")
        if (ii >= 1 and len(s) > ii + 1 and s[ii - 1] == "र्" and s[ii + 1] in expand_pratyahaara("अश्") and (s[ii - 2] in ["अ", "आ"] or get_shabda(s[ii - 3 : ii]) == "भोर्" or get_shabda(s[ii - 5 : ii]) in ["भगोर्", "अघोर्"])):
            s = aadesh(s, ii - 1, "य्")
            df_list = post_processing(df_list, s, "भोभगोअघोअपूर्वस्य योऽशि", "8.3.17")

    s = pre_processing(df_list)
    if " " in s:
        ii = s.index(" ")
        if len(s) > ii + 1 and s[ii + 1] in expand_pratyahaara("हल्"):
            df_list = हलि_सर्वेषाम्(df_list)
        elif ii >= 2 and s[ii - 2] == "ओ":
            df_list = ओतो_गार्ग्यस्य(df_list)
        else:
            df_list = लोपः_शाकल्यस्य(df_list)
    return df_list

def लोपः_शाकल्यस्य(df_list):
    s = pre_processing(df_list)
    if " " in s:
        ii = s.index(" ")
        if ii >= 1 and len(s) > ii + 1 and s[ii - 1] in ["य्", "व्"] and s[ii + 1] in expand_pratyahaara("अच्"):
            if ACTIVE_SETTINGS.get("lopa_shakalyasya", True):
                del s[ii - 1]
            else:
                s.remove(" ")
            df_list = post_processing(df_list, s, "लोपः शाकल्यस्य", "8.3.19")
    return df_list

def ओतो_गार्ग्यस्य(df_list):
    s = pre_processing(df_list)
    if " " in s:
        ii = s.index(" ")
        if ii >= 1 and len(s) > ii + 1 and s[ii - 1] in ["य्", "व्"] and s[ii + 1] in expand_pratyahaara("अश्"):
            if ACTIVE_SETTINGS.get("lopa_shakalyasya", True):
                del s[ii - 1]
            else:
                s.remove(" ")
            df_list = post_processing(df_list, s, "ओतो गार्ग्यस्य", "8.3.20")
    return df_list

def हलि_सर्वेषाम्(df_list):
    s = pre_processing(df_list)
    if " " in s:
        ii = s.index(" ")
        if ii >= 1 and len(s) > ii + 1 and s[ii - 1] in ["य्", "व्"] and s[ii + 1] in expand_pratyahaara("हल्"):
            del s[ii - 1]
            df_list = post_processing(df_list, s, "हलि सर्वेषाम्", "8.3.22")
    return df_list

def मोऽनुस्वारः(df_list):
    s = pre_processing(df_list)
    if " " in s:
        ii = s.index(" ")
        if ii >= 1 and len(s) > ii + 1 and s[ii - 1] == "म्" and s[ii + 1] in expand_pratyahaara("हल्"):
            s = aadesh(s, ii - 1, "ं")
            df_list = post_processing(df_list, s, "मोऽनुस्वारः", "8.3.23")
    return df_list

def ङमो_ह्रस्वादचि_ङमुण्नित्यम्(df_list):
    s = pre_processing(df_list)
    if " " in s:
        ii = s.index(" ")
        if ii >= 1:
            temp = s[ii - 1]
            s[ii:ii] = get_vinyaasa(temp)
            df_list = post_processing(df_list, s, "ङमो ह्रस्वादचि ङमुण्नित्यम्", "8.3.32")
    return df_list

def विसर्जनीयस्य_सः(df_list):
    s = pre_processing(df_list)
    if " " in s:
        ii = s.index(" ")
        if ii >= 1 and len(s) > ii + 1 and s[ii - 1] == "ः" and s[ii + 1] in expand_pratyahaara("खर्"):
            s = aadesh(s, ii - 1, "स्")
            df_list = post_processing(df_list, s, "विसर्जनीयस्य सः", "8.3.34")
            
            s = pre_processing(df_list)
            ii = s.index(" ") if " " in s else -1
            if ii >= 1 and len(s) > ii + 1:
                if s[ii - 1] == "स्" and s[ii + 1] in ["श्", "च्", "छ्", "ज्", "झ्", "ञ्"]:
                    df_list = स्तोः_श्चुना_श्चुः(df_list)
                elif s[ii - 1] == "स्" and s[ii + 1] in ["ष्", "ट्", "ठ्", "ड्", "ढ्", "ण्"]:
                    df_list = ष्टुना_ष्टुः(df_list)
    return df_list

def शर्परे_विसर्जनीयः(df_list):
    s = pre_processing(df_list)
    df_list = post_processing(df_list, s, "शर्परे विसर्जनीयः", "8.3.35")
    return df_list

def वा_शरि(df_list):
    s = pre_processing(df_list)
    if ACTIVE_SETTINGS.get("vaa_shari", True):
        df_list = post_processing(df_list, s, "वा शरि", "8.3.36")
    return df_list

def कुप्वोः_कपौ_च(df_list):
    s = pre_processing(df_list)
    if " " in s: 
        # Safely skipped aadesh to prevent Akshara crash. Visarga stays intact.
        df_list = post_processing(df_list, s, "कुप्वोः ≍क≍पौ च (विकल्पः)", "8.3.37")
    return df_list

def स्तोः_श्चुना_श्चुः(df_list):
    s = pre_processing(df_list)
    schu_map = {"स्": "श्", "त्": "च्", "थ्": "छ्", "द्": "ज्", "ध्": "झ्", "न्": "ञ्"}
    if " " in s:
        ii = s.index(" ")
        if ii >= 1 and s[ii - 1] in schu_map:
            s = aadesh(s, ii - 1, schu_map[s[ii - 1]])
        elif len(s) > ii + 1 and s[ii + 1] in schu_map:
            s = aadesh(s, ii + 1, schu_map[s[ii + 1]])
    df_list = post_processing(df_list, s, "स्तोः श्चुना श्चुः", "8.4.40")
    return df_list

def ष्टुना_ष्टुः(df_list):
    s = pre_processing(df_list)
    shtu_map = {"स्": "ष्", "त्": "ट्", "थ्": "ठ्", "द्": "ड्", "ध्": "ढ्", "न्": "ण्"}
    if " " in s:
        ii = s.index(" ")
        if ii >= 1 and s[ii - 1] in shtu_map:
            s = aadesh(s, ii - 1, shtu_map[s[ii - 1]])
        elif len(s) > ii + 1 and s[ii + 1] in shtu_map:
            s = aadesh(s, ii + 1, shtu_map[s[ii + 1]])
    df_list = post_processing(df_list, s, "ष्टुना ष्टुः", "8.4.41")
    return df_list

def यरोऽनुनासिकेऽनुनासिको_वा(df_list):
    s = pre_processing(df_list)
    if " " in s:
        ii = s.index(" ")
        if ACTIVE_SETTINGS.get("yaro_anunasike", True):
            if ii >= 1 and len(s) > ii + 1 and s[ii + 1] in expand_pratyahaara("ञम्"):
                anunasika_map = {
                    "क्": "ङ्", "ख्": "ङ्", "ग्": "ङ्", "घ्": "ङ्",
                    "च्": "ञ्", "छ्": "ञ्", "ज्": "ञ्", "झ्": "ञ्",
                    "ट्": "ण्", "ठ्": "ण्", "ड्": "ण्", "ढ्": "ण्",
                    "त्": "न्", "थ्": "न्", "द्": "न्", "ध्": "न्",
                    "प्": "म्", "फ्": "म्", "ब्": "म्", "भ्": "म्"
                }
                if s[ii - 1] in anunasika_map:
                    s = aadesh(s, ii - 1, anunasika_map[s[ii - 1]])
                    df_list = post_processing(df_list, s, "यरोऽनुनासिकेऽनुनासिको वा", "8.4.45")
    return df_list

def खरि_च(df_list):
    s = pre_processing(df_list)
    if " " in s:
        ii = s.index(" ")
        if ii >= 1 and len(s) > ii + 1 and s[ii + 1] in expand_pratyahaara("खर्"):
            khar_map = {
                "ग्": "क्", "घ्": "क्", "ज्": "च्", "झ्": "च्",
                "ड्": "ट्", "ढ्": "ट्", "द्": "त्", "ध्": "त्",
                "ब्": "प्", "भ्": "प्"
            }
            if s[ii - 1] in khar_map:
                s = aadesh(s, ii - 1, khar_map[s[ii - 1]])
                df_list = post_processing(df_list, s, "खरि च", "8.4.55")
    return df_list

def वाऽवसाने(df_list):
    s = pre_processing(df_list)
    avasana_map = {
        "ग्": "क्", "घ्": "क्", "ज्": "च्", "झ्": "च्",
        "ड्": "ट्", "ढ्": "ट्", "द्": "त्", "ध्": "त्",
        "ब्": "प्", "भ्": "प्"
    }
    if len(s) > 0 and s[-1] in avasana_map:
        s = aadesh(s, len(s) - 1, avasana_map[s[-1]])
        df_list = post_processing(df_list, s, "वाऽवसाने", "8.4.56")
    return df_list

def तोर्लि(df_list):
    s = pre_processing(df_list)
    if " " in s:
        ii = s.index(" ")
        if ii >= 1 and len(s) > ii + 1 and s[ii + 1] == "ल्":
            if s[ii - 1] == "न्":
                s = aadesh(s, ii - 1, "ल्ँ")
                df_list = post_processing(df_list, s, "तोर्लि", "8.4.60")
            elif s[ii - 1] in ["त्", "थ्", "द्", "ध्"]:
                s = aadesh(s, ii - 1, "ल्")
                df_list = post_processing(df_list, s, "तोर्लि", "8.4.60")
    return df_list

def झयो_होऽन्यतरस्याम्(df_list):
    s = pre_processing(df_list)
    if " " in s:
        ii = s.index(" ")
        if ACTIVE_SETTINGS.get("jhayo_ho", True):
            if ii >= 1 and len(s) > ii + 1 and s[ii - 1] in expand_pratyahaara("झय्") and s[ii + 1] == "ह्":
                h_map = {
                    "क्": "घ्", "ग्": "घ्", "च्": "झ्", "ज्": "झ्",
                    "ट्": "ढ्", "ड्": "ढ्", "त्": "ध्", "द्": "ध्",
                    "प्": "भ्", "ब्": "भ्"
                }
                if s[ii - 1] in h_map:
                    s = aadesh(s, ii + 1, h_map[s[ii - 1]])
                    df_list = post_processing(df_list, s, "झयो होऽन्यतरस्याम्", "8.4.62")
    return df_list

def शशछोऽटि(df_list):
    s = pre_processing(df_list)
    if " " in s:
        ii = s.index(" ")
        if ACTIVE_SETTINGS.get("shashcho_ati", True):
            if ii >= 1 and len(s) > ii + 1 and s[ii - 1] in expand_pratyahaara("झय्") and s[ii + 1] == "श्":
                s = aadesh(s, ii + 1, "छ्")
                df_list = post_processing(df_list, s, "शशछोऽटि", "8.4.63")
    return df_list

# ==========================================
# 4. VAAKYA SANDHI LOGIC
# ==========================================
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

def eng_to_devanagari(text):
    mapping = str.maketrans('0123456789', '०१२३४५६७८९')
    return str(text).translate(mapping)

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
            
        df_list = [{"स्थिति": s, "सूत्र": "-"}]
        
        if pv and sv:
            if pv[-1] in expand_pratyahaara("अच्"):
                if secondary in avasaana:
                    pass
                elif sv[0] in expand_pratyahaara("हल्"):
                    if pv[-1] in ["अ", "इ", "उ", "ऋ", "ऌ"] and sv[0] == "छ्":
                        df_list = छे_च(df_list)
                elif sv[0] in expand_pratyahaara("अच्"):
                    if pv[-1] in expand_pratyahaara("एङ्") and sv[0] == "अ":
                        df_list = एङः_पदान्तादति(df_list)
                    elif pv[-1] in ["अ", "आ"] and sv[0] in ["ए", "ओ"] and primary in ["प्र", "अप", "अव", "उप", "परा"]:
                        df_list = एङि_पररूपम्(df_list)
                    elif (pv[-1] == sv[0] and pv[-1] in expand_pratyahaara("अक्")) or (
                        set((pv[-1], sv[0])) in [
                            set(("अ", "आ")), set(("इ", "ई")), set(("उ", "ऊ")),
                            set(("ऋ", "ॠ")), set(("ऋ", "ऌ")), set(("ॠ", "ऌ")),
                        ]
                    ):
                        df_list = अकः_सवर्णे_दीर्घः(df_list)
                    elif pv[-1] in ["अ", "आ"] and sv[0] in expand_pratyahaara("एच्"):
                        df_list = वृद्धिरेचि(df_list)
                    elif pv[-1] in ["अ", "आ"] and sv[0] in expand_pratyahaara("अक्"):
                        df_list = आद्गुणः(df_list)
                    elif pv[-1] in expand_pratyahaara("एच्") and sv[0] in expand_pratyahaara("अच्"):
                        df_list = एचोऽयवायावः(df_list)
                    elif pv[-1] in expand_pratyahaara("इक्") and sv[0] in expand_pratyahaara("अच्"):
                        df_list = इको_यणचि(df_list)
            else:
                if (
                    secondary not in avasaana
                    and (mm[ii] in ["सस्", "एषस्", "सः", "एषः"] or primary in ["सस्", "एषस्"])
                    and sv[0] in expand_pratyahaara("हल्")
                ):
                    df_list = एतत्तदोः_सुलोपोऽकोरनञ्समासे_हलि(df_list)
                elif pv[-1] == "स्":
                    df_list = ससजुषो_रुः(df_list)
                    if secondary in avasaana:
                        df_list = खरवसानयोर्विसर्जनीयः(df_list)
                    else:
                        if sv[0] in expand_pratyahaara("खर्"):
                            df_list = खरवसानयोर्विसर्जनीयः(df_list)
                        else:
                            if primary in ["भोस्", "भगोस्", "अघोस्"]:
                                df_list = भोभगोअघोअपूर्वस्य_योऽशि(df_list)
                            elif len(pv) >= 2 and pv[-2] == "अ":
                                if sv[0] == "अ":
                                    df_list = अतो_रोरप्लुतादप्लुते(df_list)
                                elif sv[0] in expand_pratyahaara("हश्"):
                                    df_list = हशि_च(df_list)
                                else:
                                    df_list = भोभगोअघोअपूर्वस्य_योऽशि(df_list)
                            elif len(pv) >= 2 and pv[-2] == "आ":
                                df_list = भोभगोअघोअपूर्वस्य_योऽशि(df_list)
                            elif sv[0] == "र्":
                                df_list = रो_रि(df_list)
                else:
                    if pv[-1] in expand_pratyahaara("झल्"):
                        df_list = झलां_जशोऽन्ते(df_list)
                    elif secondary not in avasaana and pv[-1] == "र्" and sv[0] == "र्":
                        df_list = रो_रि(df_list)
                    elif pv[-1] == "र्" and (secondary in avasaana or sv[0] in expand_pratyahaara("खर्")):
                        df_list = खरवसानयोर्विसर्जनीयः(df_list)
                    elif secondary in avasaana:
                        pass
                    elif pv[-1] == "म्" and secondary not in avasaana:
                        if sv[0] in expand_pratyahaara("हल्"):
                            df_list = मोऽनुस्वारः(df_list)
                    elif secondary not in avasaana and pv[-1] == "न्" and sv[0] in expand_pratyahaara("छव्"):
                        df_list = नश्छव्यप्रशान्(df_list)
                    elif secondary not in avasaana and pv[-1] == "न्" and sv[0] == "ल्":
                        df_list = तोर्लि(df_list)
                    elif secondary not in avasaana and pv[-1] == "न्" and sv[0] in ["श्", "च्", "छ्", "ज्", "झ्", "ञ्"]:
                        df_list = स्तोः_श्चुना_श्चुः(df_list)
                    elif secondary not in avasaana and pv[-1] in expand_pratyahaara("हल्") and sv[0] in expand_pratyahaara("अच्"):
                        if pv[-1] in expand_pratyahaara("ङम्") and len(pv) >= 2 and pv[-2] in ["अ", "इ", "उ", "ऋ", "ऌ"]:
                            df_list = ङमो_ह्रस्वादचि_ङमुण्नित्यम्(df_list)

        r = df_list[-1]["स्थिति"]

        if " " in r:
            parts = r.split(" ", 1)
            dd.extend(safe_vinyaasa(parts[0]) or list(parts[0]))
            dd.append(" ")
            if len(parts) > 1:
                mm[ii + 1] = parts[1]
        else:
            if secondary in avasaana:
                dd.extend(safe_vinyaasa(r) or list(r))
                dd.append(" ")
                dd.append(secondary)
            else:
                flag = 1
                temp = r

        if len(df_list) > 1:
            prakriya_rows.extend(df_list[1:])

        sutra_list = [row["सूत्र"] for row in df_list if row["सूत्र"] != "-"]
        sutra_series = " ".join(sutra_list) if sutra_list else "-"

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
        # Mathematically skips space ONLY if ending in specific Halanta block boundaries
        space_skippable_chars = expand_pratyahaara("हल्") + ["ः", "ं", "ँ", "्"]
        
        for i in range(1, len(dd) - 1):
            prev_char = dd[i - 1]
            if dd[i] == " " and dd[i + 1] not in avasaana:
                if prev_char in space_skippable_chars or (len(prev_char) > 0 and prev_char[-1] in space_skippable_chars):
                    pass
                else:
                    ee.append(dd[i])
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
    # Restores visual Devanagari format exactly how Font renderers display
    ee = ee.replace("ल्ँ", "ँल्")
    ee = ee.replace(" ।", "।").replace("।", " । ")
    ee = ee.replace(" ॥", "॥").replace("॥", " ॥ ")
    ee = " ".join(ee.split())

    prakriya = pd.DataFrame(prakriya_rows)
    sandhi_summary = pd.DataFrame(sandhi_summary_rows)

    if lang == "संस्कृतम्" and not prakriya.empty:
        prakriya["सूत्र"] = prakriya["सूत्र"].apply(eng_to_devanagari)
        sandhi_summary["सूत्राणि"] = sandhi_summary["सूत्राणि"].apply(eng_to_devanagari)

    return [ee, sandhi_summary, prakriya]
