from openai import OpenAI
from settings import settings
import json

client = OpenAI(
    base_url="https://openrouter.ai/api/v1",
    api_key=settings.OPEN_ROUTER_API_KEY,
)

def launch_checklist_assistant(prompt: str):
    
    system_promt = """
    You are a helpful guide. You help the user to create checklists for their project/task/event/journey/etc, so that the user won't forget anything.
    
    IMPORTANT: You MUST respond with ONLY a JSON array following this EXACT structure. Do not include any other fields or commentary.
    Required JSON Schema:
    [
        {
            "heading": "Documents",
            "items": [
            "Flight tickets",
            "Valid ID (Passport/Driver's License)",
            "Travel insurance policy",
            "Accommodation reservation confirmation",
            "Vehicle rental agreement or ride‑share app details",
            "COVID‑19 requirements (if any)",
            "Emergency contacts"
            ]
        },
        {
            "heading": "Flights",
            "items": [
            "Flight booking reference",
            "Check‑in online confirmation"
            ]
        },
        {
            "heading": "Accommodation",
            "items": [
            "Hotel/guesthouse confirmation",
            "Check‑in time",
            "Address and contact number"
            ]
        },
        {
            "heading": "Transportation",
            "items": [
            "Airport transfer info",
            "Local ride‑share app account set up",
            "Public transport passes"
            ]
        },
        {
            "heading": "Expenses",
            "items": [
            "Travel budget",
            "Credit/debit cards",
            "Cash in local currency",
            "Travel app for currency exchange"
            ]
        }
    ]
    
    Rules:
    - Always be accurate and concise
    - Do not add unwanted items in the checklist
    - Provide all possible items in the checklist
    - MUST use only "heading", "checklist", and "items" fields
    - Response must be a valid JSON array
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

    # Parse the response
    content = json.loads(response.choices[0].message.content)
    
    # If the response is already an array, return it
    if isinstance(content, list):
        return content
    
    # If it's an object with a 'checklist' key, extract that
    if isinstance(content, dict) and 'checklist' in content:
        return content['checklist']
    
    # Otherwise, wrap it in an array
    return [content]
