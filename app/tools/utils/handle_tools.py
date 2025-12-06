import json
from app.tools.get_weather_by_place import get_weather_by_place

def handle_tools(tool_call):
    if tool_call.function.name == "get_weather_by_place":
        args = json.loads(tool_call.function.arguments)
        weather = get_weather_by_place(args.get("place"), args.get("country"), args.get("state"))

        response = {
            "role": "tool",
            "content": weather,
            "tool_call_id": tool_call.id
        } 

        return response
