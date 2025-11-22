# from serpapi import GoogleSearch
#
# def get_top_50_attractions(city, api_key="764f6562ac7a13291ac92c6a7759fe148a5063770000a6e20e36a6c4edee6368", tag="tourist attractions"):
#     """
#     Fetches top 5 popular attractions using SerpAPI Google Maps Engine.
#     """
#     if not api_key:
#         raise ValueError("API key is required")
#
#     tag = tag or "tourist attractions"
#
#     params = {
#         "engine": "google_maps",
#         "q": f"{tag} in {city}",
#         "type": "search",
#         "api_key": api_key
#     }
#
#     try:
#         search = GoogleSearch(params)
#         results = search.get_dict()
#     except Exception as e:
#         return [f"Error fetching data: {e}"]
#
#     places = []
#
#     local_results = results.get("local_results", [])
#     for place in local_results:
#         title = place.get("title")
#         if title:
#             places.append(title)
#         if len(places) == 50:
#             break
#
#     # Fill missing entries
#     while len(places) < 5:
#         places.append(f"More {tag} available in {city}")
#
#     return places


from serpapi import GoogleSearch
from functools import lru_cache

@lru_cache(maxsize=50)  # cache results for speed
def get_top_50_attractions(city, api_key, tag="tourist attractions"):
    """
    Fetches up to 50 popular attractions using SerpAPI Google Maps Engine.
    Optimized for speed on Render.
    """

    if not api_key:
        raise ValueError("API key is required")

    tag = tag or "tourist attractions"

    params = {
        "engine": "google_maps",
        "q": f"{tag} in {city}",
        "type": "search",
        "api_key": api_key
    }

    try:
        search = GoogleSearch(params)
        results = search.get_dict()
    except Exception as e:
        return [f"Error fetching data: {e}"]

    places = []
    local_results = results.get("local_results", [])

    # Limit processing for speed
    for place in local_results[:50]:
        title = place.get("title")
        if title:
            places.append(title)

    # Ensure minimum results
    if not places:
        return [f"No {tag} found for {city}"]

    return places
