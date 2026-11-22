# -*- coding: utf-8 -*-
"""
Mind Bites Caption Engine
Generates viral, engaging captions in Hindi & Hinglish for daily visual notes.
"""

import random

HOOKS = [
    "🧠 आज का Mind Bite: क्या आप यह रोचक तथ्य जानते थे? 💡",
    "📝 Quick Visual Note: सिर्फ 30 सेकंड में जानिए यह कमाल का रहस्य! 🔍",
    "✨ Knowledge Booster: दिमाग की बत्ती जला देने वाला आज का Quick Note! 🚀",
    "💡 Did You Know? विज्ञान और कुदरत का यह अनोखा सच आपको हैरान कर देगा! 🤯",
    "🔬 Mind Bites Daily: आसान शब्दों और विजुअल्स में समझिए यह जरूरी ज्ञान! 📚"
]

CALL_TO_ACTIONS = [
    "👉 अगर कुछ नया सीखने को मिला तो इस पोस्ट को Save करें और दोस्तों के साथ Share जरूर करें! 🚀",
    "💬 आपकी इस बारे में क्या राय है? हमें Comments में जरूर बताएं! 👇",
    "✨ हर रोज़ ऐसे ही कमाल के Visual Notes और Mind Bites पाने के लिए Follow करें @mind.bites3 🧠",
    "📌 Save this post for quick revision and share with someone who loves learning! 💡"
]

HASHTAGS = [
    "#MindBites", "#DailyNotes", "#QuickKnowledge", "#ScienceFacts",
    "#FactsInHindi", "#KnowledgeIsPower", "#DidYouKnow", "#Curiosity",
    "#VisualLearning", "#BrainFood", "#StudyHacks", "#HindiFacts",
    "#AmazingFacts", "#GeneralKnowledge", "#EducationFirst", "#Mindset"
]

def generate_mind_bites_caption(topic_title: str) -> str:
    hook = random.choice(HOOKS)
    cta = random.choice(CALL_TO_ACTIONS)
    tags = " ".join(random.sample(HASHTAGS, min(12, len(HASHTAGS))))
    
    caption = f"""{hook}

📌 Topic: {topic_title}

{cta}

Follow @mind.bites3 for your daily dose of visual brain food! 🧠✨

.
{tags}
"""
    return caption.strip()
