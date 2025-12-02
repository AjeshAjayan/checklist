from openai import OpenAI
from settings import settings
import json

client = OpenAI(
    base_url="https://openrouter.ai/api/v1",
    api_key=settings.OPEN_ROUTER_API_KEY,
)

def launch_checklist_assistant(prompt: str):
    
    system_promt = """
    You are a helpful guide. You create complete checklists for any project, task, event, journey, or activity.

    IMPORTANT: You MUST respond with ONLY a JSON array.  
    No explanations, no extra fields, no markdown, no commentary — ONLY the JSON array.

    MUST follow this exact structure:

    [
        {
            "heading": "<Heading 1>",
            "items": [
                "<Item 1>",
                "<Item 2>",
                "<Item 3>",
                ...
                "<Item N>"
            ]
        },
        {
            "heading": "<Heading 2>",
            "items": [
                "<Item 1>",
                "<Item 2>",
                "<Item 3>",
                ...
                "<Item N>"
            ]
        },
        {
            "heading": "<Heading 3>",
            "items": [
                "<Item 1>",
                "<Item 2>",
                "<Item 3>",
                ...
                "<Item N>"
            ]
        }
    ]

    Rules:
    - You MUST always provide **3 or more headings** — never only one.
    - MUST use only: "heading" and "items".
    - MUST be accurate, concise, and exhaustive.
    - MUST include all relevant checklist items.
    - MUST output a valid JSON array.
    """

    messages=[
        {"role": "system", "content": system_promt},
        {"role": "assistant", "content": "What are you looking to create a checklist for?"},
        {"role": "user", "content": prompt}
    ]

    response = client.chat.completions.create(
        # model="openai/gpt-oss-20b:free",
        model="openai/gpt-3.5-turbo",
        messages=messages,
        response_format={"type": "json_object"},
        reasoning_effort="minimal"
    )

    # Parse the response
    # The API returns a JSON object with the checklist array
    # We need to parse it and extract the checklist data
    
    if response.choices:
        content = response.choices[0].message.content
        print("Response:", response.model_dump_json(indent=2), "\n\n\n")
        print("Raw response:", content)
        
        try:
            # Parse the JSON string
            parsed_data = json.loads(content)
            
            # The API can return different formats:
            # 1. A single checklist object: {"heading": "...", "items": [...]}
            # 2. An array of checklist objects: [{"heading": "...", "items": [...]}, ...]
            # 3. A wrapper object: {"checklist": [...]}
            
            if isinstance(parsed_data, dict):
                # Check if it has "heading" and "items" - it's a single checklist
                if "heading" in parsed_data and "items" in parsed_data:
                    checklist = [parsed_data]  # Wrap in array
                # Check if it has a "checklist" key
                elif "checklist" in parsed_data:
                    checklist = parsed_data["checklist"]
                    # Ensure it's a list
                    if not isinstance(checklist, list):
                        checklist = [checklist]
                else:
                    # Try to extract the first value if it looks like a wrapper
                    first_value = list(parsed_data.values())[0] if parsed_data else []
                    checklist = first_value if isinstance(first_value, list) else [first_value]
            elif isinstance(parsed_data, list):
                # If it's already a list, use it directly
                checklist = parsed_data
            else:
                checklist = []
            
            print("Parsed checklist:", checklist)
            return checklist
        except json.JSONDecodeError as e:
            print(f"JSON parsing error: {e}")
            return []
    
    return []