import httpx
from settings import settings


async def get_weather_by_place(place: str, country: str = "", state: str = "") -> dict:
    """
    Fetch weather data for a given place using OpenWeatherMap API.
    
    Args:
        place (str): The name of the city or location
        country (str): Country code (e.g., "US", "GB", "IN") - optional
        state (str): State or province name - optional
        
    Returns:
        dict: Weather data containing temperature, description, humidity, etc.
    """
    try:
        # Build the location query string
        # Format: "city,state,country" for more precise results
        location_parts = [place]
        if state:
            location_parts.append(state)
        if country:
            location_parts.append(country)
        location_query = ",".join(location_parts)
        
        async with httpx.AsyncClient(timeout=10.0) as client:
            # Step 1: Use Geocoding API to get detailed location information including state
            geocoding_url = "http://api.openweathermap.org/geo/1.0/direct"
            geocoding_params = {
                "q": location_query,
                "limit": 1,
                "appid": settings.OPEN_WEATHER_API_KEY
            }
            
            geocoding_response = await client.get(geocoding_url, params=geocoding_params)
            geocoding_response.raise_for_status()
            geocoding_data = geocoding_response.json()

            if not geocoding_data:
                return {
                    "error": f"Location '{location_query}' not found via geocoding.",
                    "status_code": 404
                }
            
            lat = geocoding_data[0]["lat"]
            lon = geocoding_data[0]["lon"]
            city_name = geocoding_data[0].get("name", place)
            country_code = geocoding_data[0].get("country", country)
            state_name = geocoding_data[0].get("state", state)

            # Step 2: Get weather data using coordinates
            weather_url = "https://api.openweathermap.org/data/2.5/weather"
            
            # Parameters for the API request
            weather_params = {
                "lat": lat,
                "lon": lon,
                "appid": settings.OPEN_WEATHER_API_KEY,
                "units": "metric"  # Use metric units (Celsius)
            }
            
            # Make the API request
            response = await client.get(weather_url, params=weather_params)
            response.raise_for_status()  # Raise an exception for bad status codes
            
            # Parse the JSON response
            data = response.json()
            
            # Extract relevant weather information
            weather_data = {
                "location": city_name,
                "state": state_name,
                "country": country_code,
                "latitude": lat,
                "longitude": lon,
                "temperature": data.get("main", {}).get("temp"),
                "feels_like": data.get("main", {}).get("feels_like"),
                "temp_min": data.get("main", {}).get("temp_min"),
                "temp_max": data.get("main", {}).get("temp_max"),
                "humidity": data.get("main", {}).get("humidity"),
                "pressure": data.get("main", {}).get("pressure"),
                "description": data.get("weather", [{}])[0].get("description", ""),
                "main": data.get("weather", [{}])[0].get("main", ""),
                "icon": data.get("weather", [{}])[0].get("icon", ""),
                "wind_speed": data.get("wind", {}).get("speed"),
                "wind_deg": data.get("wind", {}).get("deg"),
                "clouds": data.get("clouds", {}).get("all"),
                "visibility": data.get("visibility"),
                "sunrise": data.get("sys", {}).get("sunrise"),
                "sunset": data.get("sys", {}).get("sunset"),
            }
            
            return weather_data
        
    except httpx.HTTPStatusError as e:
        # Handle HTTP errors (e.g., 404 for city not found, 401 for invalid API key)
        if e.response.status_code == 404:
            return {
                "error": f"Location '{place}' not found",
                "status_code": 404
            }
        elif e.response.status_code == 401:
            return {
                "error": "Invalid API key",
                "status_code": 401
            }
        else:
            return {
                "error": f"HTTP error occurred: {str(e)}",
                "status_code": e.response.status_code
            }
    
    except httpx.TimeoutException:
        return {
            "error": "Request timed out. Please try again.",
            "status_code": 408
        }
    
    except httpx.RequestError as e:
        return {
            "error": f"Network error occurred: {str(e)}",
            "status_code": 500
        }
    
    except Exception as e:
        return {
            "error": f"An unexpected error occurred: {str(e)}",
            "status_code": 500
        }