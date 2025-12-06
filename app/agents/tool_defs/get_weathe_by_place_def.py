get_weather_by_place_def = {
    "name": "get_weather_by_place",
    "description": "Get weather by place, country and state",
    "parameters": {
        "type": "object",
        "properties": {
            "place": {
                "type": "string",
                "description": "The name of the city or location"
            },
            "country": {
                "type": "string",
                "description": "Name of the country. Eg: India, China, USA"
            },
            "state": {
                "type": "string",
                "description": "Name of the state or province. Eg: Maharashtra, California"
            }
        },
        "required": ["place", "country", "state"],
        "additionalProperties": False
    }
}
