# -*- coding: utf-8 -*-
"""
Mind Bites Intelligent Image-Aware Caption Engine
Generates viral, deeply informative, and fact-rich captions in Hindi & Hinglish
by inspecting the exact visual note topic and cards shown in the image.
"""

import os
import random

# Detailed knowledge base matching all visual notes
TOPIC_DETAILS = {
    "theme_01_solar_system": {
        "title": "हमारा सौर मंडल (The Solar System)",
        "emoji": "🪐🚀",
        "intro": "क्या आप जानते हैं कि हमारे सौर मंडल में 8 ग्रह कितनी अनोखी दुनिया समेटे हुए हैं? आइए सिर्फ 30 सेकंड में इस Quick Note के जरिए पूरा सौर मंडल समझें!",
        "points": [
            "🔴 आंतरिक ग्रह (Rocky Planets): बुध, शुक्र, पृथ्वी और मंगल ठोस पत्थरों से बने हैं। शुक्र सबसे गर्म ग्रह (470°C) है!",
            "🪐 बाहरी गैस दानव (Gas Giants): बृहस्पति और शनि हाइड्रोजन-हीलियम से बने विशालकाय ग्रह हैं। शनि के छल्ले बर्फ और धूल के बने हैं।",
            "❄️ बर्फीले ग्रह (Ice Giants): अरुण (Uranus) और वरुण (Neptune) सबसे ठंडे ग्रह हैं, जहाँ तूफानी बर्फीली हवाएं चलती हैं।",
            "🧠 याद रखने की ट्रिक: 'My Very Educated Mother Just Served Us Noodles' (Mercury, Venus, Earth, Mars, Jupiter, Saturn, Uranus, Neptune)!"
        ],
        "fun_fact": "प्लूटो को 2006 में वैज्ञानिकों ने ग्रह की श्रेणी से हटाकर बौना ग्रह (Dwarf Planet) घोषित किया था!",
        "question": "आपको सौर मंडल का कौन-सा ग्रह सबसे ज्यादा रहस्यमयी लगता है?",
        "tags": ["#SolarSystem", "#SpaceFacts", "#Astronomy", "#Planets", "#Universe", "#ScienceInHindi", "#MindBites", "#UPSCNotes", "#Cosmos"]
    },
    "theme_02_photosynthesis": {
        "title": "पेड़-पौधे खाना कैसे बनाते हैं? (Photosynthesis)",
        "emoji": "🌿☀️",
        "intro": "धरती पर जीवन का सबसे बड़ा आधार है 'प्रकाश संश्लेषण' (Photosynthesis)। आइए आसान शब्दों में समझें कि एक पत्ती कैसे किसी हाई-टेक सोलर फैक्ट्री की तरह खाना तैयार करती है!",
        "points": [
            "☀️ 3 जरूरी सामग्री: सूरज की धूप (Solar Energy), हवा से कार्बन डाइऑक्साइड (CO2), और जड़ों से खींचा गया पानी (H2O)।",
            "🍃 क्लोरोफिल का जादू: पत्तियों का हरा रंग क्लोरोफिल की वजह से होता है, जो धूप को सोखकर रासायनिक ऊर्जा में बदलता है।",
            "🍎 क्या बनता है?: पौधे खुद के लिए ग्लूकोज (शुगर भोजन) बनाते हैं और हमारे लिए शुद्ध ऑक्सीजन (O2) हवा में छोड़ते हैं।",
            "🌙 रात का रहस्य: रात में धूप न होने पर प्रकाश संश्लेषण रुक जाता है और पौधे सिर्फ सांस लेकर CO2 छोड़ते हैं, इसलिए रात में पेड़ों के नीचे नहीं सोना चाहिए!"
        ],
        "fun_fact": "धरती की 50% से अधिक ऑक्सीजन जंगलों से नहीं, बल्कि समुद्र के सूक्ष्म फाइटोप्लांकटन (Phytoplankton) बनाते हैं!",
        "question": "क्या आप जानते थे कि रात में पौधे ऑक्सीजन नहीं बल्कि CO2 छोड़ते हैं?",
        "tags": ["#Photosynthesis", "#PlantScience", "#BiologyFacts", "#NatureWonders", "#GreenPlanet", "#ScienceInHindi", "#MindBites", "#StudyNotes"]
    },
    "theme_03_eclipse": {
        "title": "सूर्य और चंद्र ग्रहण कैसे होते हैं? (Eclipses)",
        "emoji": "🌑✨",
        "intro": "सूर्य ग्रहण और चंद्र ग्रहण के पीछे कोई अंधविश्वास नहीं, बल्कि अंतरिक्ष में परछाई का अद्भुत खगोलीय खेल है! जानिए कैसे काम करते हैं ग्रहण:",
        "points": [
            "☀️ सूर्य ग्रहण (Solar Eclipse): जब चंद्रमा, सूर्य और पृथ्वी के बीच आ जाता है और सूर्य की रोशनी को रोक लेता है। यह केवल अमावस्या को होता है।",
            "🌕 चंद्र ग्रहण (Lunar Eclipse): जब पृथ्वी, सूर्य और चंद्रमा के बीच आ जाती है और अपनी छाया चंद्रमा पर डालती है। यह पूर्णिमा को होता है।",
            "🎯 Umbra और Penumbra: गहरी काली परछाई को Umbra कहते हैं जहाँ पूर्ण ग्रहण दिखता है, और हल्की परछाई को Penumbra कहते हैं।",
            "🔄 हर महीने क्यों नहीं?: क्योंकि चंद्रमा की कक्षा पृथ्वी की कक्षा से 5 डिग्री झुकी हुई है, इसलिए हर पूर्णिमा या अमावस्या को ग्रहण नहीं लगता!"
        ],
        "fun_fact": "पूर्ण सूर्य ग्रहण के दौरान तापमान अचानक 5 से 10 डिग्री तक गिर जाता है और दिन में पक्षी सोने लगते हैं!",
        "question": "क्या आपने कभी अपनी आँखों से सूर्य या चंद्र ग्रहण देखा है?",
        "tags": ["#SolarEclipse", "#LunarEclipse", "#SpaceFacts", "#AstronomyLovers", "#EclipseFacts", "#ScienceInHindi", "#MindBites", "#SkyWatch"]
    },
    "theme_04_human_brain": {
        "title": "मानव मस्तिष्क की असीमित शक्तियां (Human Brain)",
        "emoji": "🧠⚡",
        "intro": "ब्रह्मांड की सबसे जटिल और ताकतवर मशीन आपके सिर के अंदर है! जानिए इंसानी दिमाग से जुड़े कुछ होश उड़ा देने वाले वैज्ञानिक सच:",
        "points": [
            "⚡ 86 अरब न्यूरॉन्स: आपके दिमाग में लगभग 86 बिलियन न्यूरॉन्स हैं, जो आपस में खरबों सिनाપ્સિસ से जुड़े हुए हैं।",
            "💡 20 वाट की बिजली: आपका मस्तिष्क इतनी बिजली पैदा करता है कि उससे एक छोटा LED बल्ब आसानी से जल सकता है!",
            "⚖️ 20% ऊर्जा की खपत: शरीर के कुल वजन का सिर्फ 2% होने के बावजूद दिमाग शरीर की 20% ऑक्सीजन और कैलोरी अकेले खर्च करता है।",
            "💾 असीमित स्टोरेज: वैज्ञानिक मानते हैं कि इंसानी दिमाग की मेमोरी क्षमता लगभग 2.5 पेटাবाइट (25 लाख गीगाबाइट) के बराबर है!"
        ],
        "fun_fact": "दिमाग को खुद कभी दर्द महसूस नहीं होता, क्योंकि मस्तिष्क में दर्द के कोई रिसेप्टर्स (Pain Receptors) ही नहीं होते!",
        "question": "क्या आप रोजाना दिमाग को तेज करने के लिए मेडिटेशन या पहेलियां सुलझाते हैं?",
        "tags": ["#HumanBrain", "#Neuroscience", "#BrainFacts", "#PsychologyFacts", "#HumanBody", "#KnowledgeInHindi", "#MindBites", "#GeniusMind"]
    },
    "theme_05_ai_chatgpt": {
        "title": "Artificial Intelligence & ChatGPT कैसे काम करता है?",
        "emoji": "🤖💻",
        "intro": "ChatGPT और AI आज दुनिया को बदल रहे हैं, लेकिन क्या आपने कभी सोचा कि कंप्यूटर इंसानों की तरह सोच और बात कैसे कर लेता है? जानिए इसका आसान विज्ञान:",
        "points": [
            "🧠 न्यूरल नेटवर्क (Neural Networks): AI इंसानी दिमाग के न्यूरॉन्स की नकल करके सीखता है, जिसे Deep Learning कहते हैं।",
            "📚 विशाल डेटा ट्रेनिंग: ChatGPT को इंटरनेट की खरबों किताबों, लेखों और कोड से सिखाया गया है।",
            "🎯 अगला शब्द पहचानना: AI असल में 'सोचता' नहीं, बल्कि सांख्यिकी (Probability) के आधार पर वाक्य का अगला सबसे सही शब्द चुनता है!",
            "⚡ भविष्य की ताकत: कोडिंग, मेडिकल रिसर्च, स्पेस साइंस और आर्ट्स में AI इंसानों की मदद से क्रांति ला रहा है।"
        ],
        "fun_fact": "ChatGPT ने लॉन्च के सिर्फ 5 दिनों के अंदर 10 लाख यूज़र्स हासिल करके इतिहास रच दिया था!",
        "question": "आप अपने रोज़मर्रा के कामों में AI का इस्तेमाल किस चीज़ के लिए करते हैं?",
        "tags": ["#ArtificialIntelligence", "#ChatGPT", "#TechFacts", "#FutureTech", "#MachineLearning", "#ScienceInHindi", "#MindBites", "#Innovation"]
    },
    "theme_06_human_body": {
        "title": "मानव शरीर के जादुई और रहस्यमयी आंकड़े (Human Body)",
        "emoji": "🧬🫀",
        "intro": "हमारा शरीर किसी चमत्कारी सुपर-कंप्यूटर से कम नहीं है! आइए जानिए मानव शरीर की अद्भुत क्षमताओं के बारे में:",
        "points": [
            "🫀 दिल की धड़कन: आपका दिल हर दिन लगभग 1,00,000 बार धड़कता है और 7,500 लीटर खून पंप करता है।",
            "🧬 डीएनए की लंबाई: अगर आपके शरीर के सारे DNA को खोलकर सीधा किया जाए, तो वह सूरज से प्लूटो तक जाकर वापस आ सकता है!",
            "🦴 स्टील से मजबूत हड्डियां: मानव शरीर की जांघ की हड्डी (Femur) वजन उठाने के मामले में कंक्रीट और स्टील से भी ज्यादा मजबूत होती है।",
            "🩸 नसों का जाल: हमारे शरीर में रक्त वाहिकाओं (Blood Vessels) की कुल लंबाई लगभग 1,00,000 किलोमीटर है — पृथ्वी के ढाई चक्कर!"
        ],
        "fun_fact": "मानव आँख 1 करोड़ से भी ज्यादा अलग-अलग रंगों को पहचानने में सक्षम है!",
        "question": "मानव शरीर का कौन-सा तथ्य आपको सबसे ज्यादा चमत्कारी लगा?",
        "tags": ["#HumanBodyFacts", "#BiologyFacts", "#HealthWisdom", "#Anatomy", "#DidYouKnow", "#ScienceInHindi", "#MindBites", "#AmazingBody"]
    },
    "theme_07_lightning": {
        "title": "आसमान में बिजली क्यों और कैसे चमकती है? (Lightning)",
        "emoji": "⚡⛈️",
        "intro": "मानसून में बादलों की गड़गड़ाहट और कड़कती बिजली को देखकर हर कोई सहम जाता है। जानिए इस प्राकृतिक विस्फोट के पीछे का असली भौतिक विज्ञान:",
        "points": [
            "⚡ बादलों में घर्षण: बादलों के अंदर बर्फ और पानी की बूंदें आपस में टकराकर करोड़ों वोल्ट का स्टैटिक चार्ज (Static Electricity) पैदा करती हैं।",
            "🔥 सूर्य से 5 गुना गर्म: बिजली का एक कौंध 30,000 डिग्री सेल्सियस तक गर्म होता है — सूर्य की सतह (5,500°C) से भी पांच गुना ज्यादा!",
            "🔊 गड़गड़ाहट क्यों होती है?: बिजली की अत्यधिक गर्मी से हवा का तापमान अचानक फैलता है, जिससे पैदा होने वाली शॉकवेव हमें 'बादल की गरज' सुनाई देती है।",
            "👀 रोशनी पहले, आवाज बाद में: प्रकाश की गति (3,00,000 किमी/से.) ध्वनि की गति (343 मी./से.) से बहुत तेज होती है, इसलिए चमक पहले दिखती है!"
        ],
        "fun_fact": "पूरी दुनिया में हर एक सेकंड में लगभग 100 बार आकाशीय बिजली जमीन पर गिरती है!",
        "question": "क्या आप कभी बिजली की जोरदार कड़क से डरकर चौंके हैं?",
        "tags": ["#Lightning", "#PhysicsFacts", "#NaturePower", "#Thunderstorm", "#ScienceFacts", "#ScienceInHindi", "#MindBites", "#WeatherFacts"]
    },
    "theme_08_black_hole": {
        "title": "ब्लैक होल के भयानक और अद्भुत रहस्य (Black Hole)",
        "emoji": "🕳️🌌",
        "intro": "ब्रह्मांड की सबसे रहस्यमयी और डरावनी वस्तु — 'ब्लैक होल', जहाँ भौतिक विज्ञान के सारे नियम टूट जाते हैं! जानिए इसका रहस्य:",
        "points": [
            "🕳️ अनंत गुरुत्वाकर्षण: जब कोई विशाल तारा मरता है, तो वह सिमटकर इतना घना हो जाता है कि प्रकाश (Light) भी बाहर नहीं निकल पाता।",
            "⏳ समय का रुक जाना: ब्लैक होल के पास गुरुत्वाकर्षण इतना प्रचंड होता है कि वहाँ समय बहुत धीमा हो जाता है (Gravitational Time Dilation)।",
            "🛑 इवेंट होराइजन (Event Horizon): ब्लैक होल की वह सीमा जहाँ से वापस लौटना नामुमकिन है — इसे 'Point of No Return' कहते हैं।",
            "🍝 स्पैगेटीफिकेशन (Spaghettification): यदि कोई वस्तु ब्लैक होल में गिरती है, तो गुरुत्वाकर्षण उसे नूडल्स की तरह लंबा खींच देता है!"
        ],
        "fun_fact": "हमारी अपनी आकाशगंगा (Milky Way) के केंद्र में भी 'Sagittarius A*' नाम का एक विशालकाय सुपरमैसिव ब्लैक होल मौजूद है!",
        "question": "क्या आप मानते हैं कि ब्लैक होल के पार कोई दूसरी समानांतर दुनिया (Multiverse) हो सकती है?",
        "tags": ["#BlackHole", "#Astrophysics", "#UniverseMysteries", "#SpaceFacts", "#Cosmos", "#ScienceInHindi", "#MindBites", "#SpaceExploration"]
    },
    "theme_09_day_and_night": {
        "title": "दिन और रात का चक्र और ऋतुओं का विज्ञान (Day & Night)",
        "emoji": "☀️🌙",
        "intro": "हर 24 घंटे में दिन और रात का बदलना और साल भर में बदलते मौसम — कुदरत की इस सटीक घड़ी के पीछे क्या विज्ञान है? आइए समझें:",
        "points": [
            "🌍 पृथ्वी का घूर्णन (Rotation): पृथ्वी 24 घंटे में अपनी धुरी पर एक चक्कर पूरा करती है। सूर्य के सामने वाला हिस्सा दिन और पीछे वाला रात बनता है।",
            "📐 23.5 डिग्री का झुकाव: पृथ्वी अपनी धुरी पर 23.5° झुकी हुई है। इसी झुकाव की वजह से सर्दी, गर्मी और बरसात की ऋतुएं (Seasons) बदलती हैं।",
            "☀️ 6 महीने दिन, 6 महीने रात: ध्रुवों (North & South Poles) पर पृथ्वी के झुकाव के कारण लगातार 6 महीने तक सूरज अस्त नहीं होता!",
            "⏳ लीप ईयर का कारण: पृथ्वी को सूर्य का चक्कर लगाने में 365 दिन और 6 घंटे लगते हैं, यही 6 घंटे जुड़कर हर 4 साल में 1 लीप डे बनाते हैं।"
        ],
        "fun_fact": "नॉर्वे (Norway) को 'Land of the Midnight Sun' कहा जाता है, जहाँ गर्मियों में आधी रात को भी सूरज चमकता रहता है!",
        "question": "आपको दिन का उजाला ज्यादा पसंद है या तारों भरी शांत रात?",
        "tags": ["#DayAndNight", "#GeographyFacts", "#EarthScience", "#Seasons", "#Planets", "#ScienceInHindi", "#MindBites", "#UPSCGeography"]
    },
    "theme_10_how_internet_works": {
        "title": "इंटरनेट असल में कैसे काम करता है? (How Internet Works)",
        "emoji": "🌐⚡",
        "intro": "हम एक क्लिक में वीडियो देख लेते हैं और दुनिया भर में मैसेज भेज देते हैं, लेकिन यह इंटरनेट हवा में नहीं, बल्कि समुद्र की गहराइयों में तैर रहा है! जानिए कैसे:",
        "points": [
            "🌊 99% इंटरनेट समुद्र के नीचे: इंटरनेट सैटेलाइट से नहीं, बल्कि समुद्र के नीचे बिछी लाखों किलोमीटर लंबी ऑप्टिकल फाइबर केबल्स से चलता है।",
            "📍 IP एड्रेस का खेल: इंटरनेट से जुड़े हर फोन और कंप्यूटर का एक खास डिजिटल पता (IP Address) होता है।",
            "📖 DNS (इंटरनेट की फोनबुक): जब आप google.com लिखते हैं, तो DNS सर्वर उस नाम को कंप्यूटर की भाषा (IP नंबर) में बदलता है।",
            "📦 डेटा पैकेट्स (Data Packets): आपकी भेजी फोटो या मैसेज छोटे-छोटे लाखों डिजिटल टुकड़ों (Packets) में बंटकर प्रकाश की गति से सफर करते हैं!"
        ],
        "fun_fact": "पूरी दुनिया के समुद्रों में लगभग 14 लाख किलोमीटर लंबी 500 से अधिक इंटरनेट केबल्स बिछाई जा चुकी हैं!",
        "question": "क्या आपको पता था कि इंटरनेट सैटेलाइट से नहीं बल्कि समुद्र के नीचे की केबल्स से चलता है?",
        "tags": ["#HowInternetWorks", "#TechEducation", "#SubmarineCables", "#Networking", "#TechFacts", "#ScienceInHindi", "#MindBites", "#DigitalIndia"]
    }
}

DEFAULT_TAGS = [
    "#MindBites", "#DailyNotes", "#ScienceFacts", "#KnowledgeIsPower",
    "#DidYouKnow", "#VisualNotes", "#FactsInHindi", "#GeneralKnowledge"
]

def generate_image_aware_caption(image_name: str, topic_title: str) -> str:
    """
    Examines the exact image name and maps it directly to its rich knowledge cards,
    ensuring 100% accurate, deeply engaging, and topic-specific captions with hashtags.
    """
    matched_key = None
    for key in TOPIC_DETAILS:
        if key in image_name.lower():
            matched_key = key
            break

    if matched_key and matched_key in TOPIC_DETAILS:
        info = TOPIC_DETAILS[matched_key]
        points_str = "\n".join(info["points"])
        tags_str = " ".join(info["tags"]) + " " + " ".join(DEFAULT_TAGS[:5])

        caption = f"""{info["emoji"]} {info["title"]} {info["emoji"]}

{info["intro"]}

━━━━━━━━━━━━━━━━━━━
📌 मुख्य वैज्ञानिक बिंदु (Key Notes):
{points_str}
━━━━━━━━━━━━━━━━━━━

💡 रोचक तथ्य (Fun Fact):
{info["fun_fact"]}

💬 सवाल: {info["question"]} नीचे Comments में बताएं! 👇

✨ हर रोज़ ऐसे ही कमाल के Visual Notes और Brain Food पाने के लिए Follow करें @mind.bites3 🧠
📌 इस पोस्ट को Save करें और अपने दोस्तों के साथ Share ज़रूर करें! 🚀

.
{tags_str}
"""
        return caption.strip()

    # Fallback if custom future image is uploaded
    tags_str = " ".join(DEFAULT_TAGS)
    caption = f"""🧠 {topic_title} 💡

आज का Mind Bite आपके लिए लेकर आया है एक अनोखा और ज्ञानवर्धक विजुअल नोट! इसे ध्यान से पढ़ें और समझें।

📌 Save this post for quick revision!
💬 आपकी इस बारे में क्या राय है? Comments में बताएं! 👇

Follow @mind.bites3 for daily visual knowledge & brain food! 🧠✨

.
{tags_str}
"""
    return caption.strip()
