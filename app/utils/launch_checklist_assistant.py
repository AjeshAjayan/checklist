from openai import OpenAI
from settings import settings

client = OpenAI(
    base_url="https://openrouter.ai/api/v1",
    api_key=settings.OPEN_ROUTER_API_KEY,
)

def launch_checklist_assistant(prompt: str):
    
    system_promt = """
    You are a helpful guide. You help the user to create checklists for their project/task/event/journey/etc, so that the user won't forget anything.
    Respond in JSON format.
    <example>
    [
        {
            "heading": "Pre-Travel Essentials",
            "checklist": [
                {
                    "heading": "Documents",
                    "items": [
                        "Flight tickets (to Kochi + connecting transport to Lakshadweep)",
                        "Valid Government ID (Aadhaar/Passport/Driving License)",
                        "Lakshadweep Entry Permit (mandatory — apply via SPORTS website)",
                        "Hotel/Resort booking confirmation",
                        "Cruise/Helicopter booking confirmation (if applicable)",
                        "Emergency contacts"
                    ]
                }
            ]
        },
        {
            "heading": "Health & Safety",
            "checklist": [
                {
                    "heading": "Medical",
                    "items": [
                        "Prescription medications",
                        "Over-the-counter medications",
                        "Any other medical requirements"
                    ]
                },
                {
                    "heading": "Safety",
                    "items": [
                        "First-aid kit",
                        "Emergency contact information",
                        "Safety instructions"
                    ]
                }
            ]
        },
        {
            "heading": "Personal Items",
            "checklist": [
                {
                    "heading": "Personal Care",
                    "items": [
                        "Personal care items (toothbrush, toothpaste, etc.)",
                        "Shaving kit",
                        "Shampoo/Conditioner",
                        "Hairbrush/Comb",
                        "Hairdryer/Curling iron",
                        "Hair ties/bobby pins",
                        "Hair gel/spray",
                        "Sunscreen",
                        "Lip balm",
                        "Face mask",
                        "Face wipes",
                    ]
                }
            ]
        }
    ]
    <example>

    Always be accurate and concise. Do not add unwanted items in the checklist. Provide all 
    possible items in the checklist.
    """
    messages=[
        {"role": "system", "content": system_promt},
        {"role": "assistant", "content": "What are you looking to create a checklist for?"},
        {"role": "user", "content": prompt}
    ]

    response = client.chat.completions.create(
        model="openai/gpt-oss-20b:free",
        messages=messages,
        response_format={"type": "json_object"},
        reasoning_effort="minimal"
    )

    res = []
    for i in response.choices:
        res.append(i.message.content)

    return res
