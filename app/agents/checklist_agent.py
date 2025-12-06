from openai import AsyncOpenAI
from settings import settings
import json
from app.tools.utils.handle_tools import handle_tools

client = AsyncOpenAI(
    base_url="https://openrouter.ai/api/v1",
    api_key=settings.OPEN_ROUTER_API_KEY,
)

async def checklist_agent(prompt: str):
    system_promt = """
    You are a helpful guide. You create complete checklists for any project, task, event, journey, or activity.

    IMPORTANT: You MUST respond with ONLY a JSON object.  
    No explanations, no extra text, no markdown, no commentary — ONLY the JSON object.

    MUST follow this exact structure:
    {
        "checklists": [
            {
                "heading": "<Heading 1>",
                "items": [
                    "<Item 1>",
                    "<Item 2>",
                    "<Item 3>",
                    "<Item N>"
                ]
            },
            {
                "heading": "<Heading 2>",
                "items": [
                    "<Item 1>",
                    "<Item 2>",
                    "<Item 3>",
                    "<Item N>"
                ]
            },
            {
                "heading": "<Heading 3>",
                "items": [
                    "<Item 1>",
                    "<Item 2>",
                    "<Item 3>",
                    "<Item N>"
                ]
            }
        ]
    }

    Rules:
    - You MUST use only: "checklists" (array), "heading" and "items" keys.
    - You MUST be accurate, concise, and exhaustive.
    - You MUST include all relevant and all possible checklist items.
    - You MUST try not to miss out any relevant checklist items.
    - You MUST output a valid JSON object.
    - split the checklist into multiple headings, if possible.
    """

    messages=[
        {"role": "system", "content": system_promt},
        {"role": "assistant", "content": "What are you looking to create a checklist for?"},
        {"role": "user", "content": prompt}
    ]

    try:
        response = await client.chat.completions.create(
            model="openai/gpt-oss-20b:free",
            # model="openai/gpt-3.5-turbo",
            messages=messages,
            response_format={"type": "json_object"}
        )
    except Exception as e:
        print(f"OpenRouter API error: {e}")
        print(f"Error type: {type(e)}")
        return []

    # Parse the response
    # The API returns a JSON object with the checklist array
    # We need to parse it and extract the checklist data
    if response.choices[0].finish_reason == "tool_calls":
        messages.append(response.choices[0].message)
        response = handle_tools(response.choices[0].message.tool_calls[0])
        messages.append(response)
    else:
        content = response.choices[0].message.content
        parsed_data = json.loads(content)

        return parsed_data
    
    return []