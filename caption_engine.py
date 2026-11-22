# -*- coding: utf-8 -*-
"""
Mind Bites Intelligent Topic-Aware Caption Engine
Generates viral, deeply informative, and fact-rich captions in Hindi & Hinglish
by inspecting the exact visual note topic and cards rendered in the image.
"""

DEFAULT_TAGS = [
    "#MindBites", "#DailyNotes", "#ScienceFacts", "#KnowledgeIsPower",
    "#DidYouKnow", "#VisualNotes", "#FactsInHindi", "#GeneralKnowledge",
    "#DailyLearning", "#Curiosity", "#EducationFirst"
]

def generate_topic_caption(topic: dict) -> str:
    """
    Takes the topic object and generates a rich, viral caption
    matching the exact content, points, and fun fact in the image.
    """
    title = topic.get("title", "Daily Quick Knowledge Note")
    subtitle = topic.get("subtitle", "")
    cards = topic.get("cards", [])
    fun_fact = topic.get("fun_fact", "")
    custom_tags = topic.get("tags", [])

    # Format points from the 4 cards
    points_lines = []
    for card in cards:
        heading = card.get("heading", "")
        points = card.get("points", [])
        if points:
            points_lines.append(f"📌 {heading}: {points[0]}")

    points_str = "\n".join(points_lines)
    all_tags = custom_tags + [t for t in DEFAULT_TAGS if t not in custom_tags][:6]
    tags_str = " ".join(all_tags)

    caption = f"""🧠 {title} 💡
{subtitle}

━━━━━━━━━━━━━━━━━━━
📝 मुख्य वैज्ञानिक बिंदु (Quick Notes):
{points_str}
━━━━━━━━━━━━━━━━━━━

💡 रोचक तथ्य (Did You Know?):
{fun_fact}

💬 इस बारे में आपकी क्या राय है? हमें नीचे Comments में बताएं! 👇
📌 इस पोस्ट को Save करें और अपने दोस्तों के साथ Share ज़रूर करें! 🚀

Follow @mind.bites3 for daily visual wisdom & brain food! 🧠✨

.
{tags_str}
"""
    return caption.strip()
