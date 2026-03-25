import os
from openai import OpenAI

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def log_event(prompt, status):
    with open("logs.txt", "a") as f:
        f.write(f"{prompt} -> {status}\n")

blocked_keywords = ["hack", "attack", "kill", "steal"]
injection_patterns = ["ignore previous instructions", "bypass", "override"]

def detect_intent(prompt):
    prompt = prompt.lower()
    for word in blocked_keywords:
        if word in prompt:
            return "unsafe"
    return "safe"

def detect_injection(prompt):
    prompt = prompt.lower()
    for pattern in injection_patterns:
        if pattern in prompt:
            return True
    return False

def generate_ai_response(prompt):
    try:
        response = client.chat.completions.create(
            model="gpt-4.1-mini",
            messages=[{"role": "user", "content": prompt}]
        )
        return response.choices[0].message.content

    except Exception:
        # fallback responses
        prompt_lower = prompt.lower()

        if "what is ai" in prompt_lower:
            return "Artificial Intelligence (AI) refers to machines that can perform tasks requiring human intelligence, such as learning and decision-making."

        elif "machine learning" in prompt_lower:
            return "Machine learning is a subset of AI where systems learn from data and improve over time."

        else:
            return "This is a valid query. The AI system would normally generate a helpful response here."

def process_prompt(prompt):
    # Injection check
    if detect_injection(prompt):
        log_event(prompt, "blocked")
        return (
            "🚫 Prompt injection detected.\n\n"
            "🤖 Safe Response: I cannot assist with that request, but I can explain cybersecurity basics.",
            "blocked (prompt injection)"
        )

    # Unsafe intent
    if detect_intent(prompt) == "unsafe":
        log_event(prompt, "blocked")
        return (
            "⚠️ Unsafe request detected.\n\n"
            "🤖 Safe Response: I cannot help with harmful activities, but I can guide you on ethical practices.",
            "blocked (unsafe intent)"
        )

    # Safe → AI response
    ai_response = generate_ai_response(prompt)
    log_event(prompt, "allowed")
    return f"✅ Safe Query\n\n🤖 AI Response: {ai_response}", "allowed"