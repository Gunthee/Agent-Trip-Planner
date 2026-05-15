from typing import Optional

HOTELS: dict = {
    "japan": [
        {"name": "Tokyo Shibuya Hotel",       "location": "Shibuya, Tokyo",      "price": 80,  "rating": 4.2, "amenities": ["WiFi", "Breakfast", "AC"]},
        {"name": "Shinjuku Grand Hotel",       "location": "Shinjuku, Tokyo",     "price": 120, "rating": 4.5, "amenities": ["WiFi", "Pool", "Restaurant", "Gym"]},
        {"name": "Kyoto Gion Inn",             "location": "Gion, Kyoto",         "price": 95,  "rating": 4.7, "amenities": ["WiFi", "Breakfast", "Traditional Room"]},
        {"name": "Osaka Budget Stay",          "location": "Namba, Osaka",        "price": 45,  "rating": 3.8, "amenities": ["WiFi", "AC"]},
        {"name": "Akihabara Tech Hotel",       "location": "Akihabara, Tokyo",    "price": 75,  "rating": 4.0, "amenities": ["WiFi", "AC", "Gaming Lounge"]},
    ],
    "korea": [
        {"name": "Myeongdong Tourist Hotel",   "location": "Myeongdong, Seoul",   "price": 70,  "rating": 4.1, "amenities": ["WiFi", "Breakfast"]},
        {"name": "Gangnam Luxury Hotel",       "location": "Gangnam, Seoul",      "price": 150, "rating": 4.8, "amenities": ["WiFi", "Pool", "Spa", "Restaurant"]},
        {"name": "Hongdae Hostel",             "location": "Hongdae, Seoul",      "price": 30,  "rating": 3.9, "amenities": ["WiFi", "Shared Kitchen"]},
        {"name": "Jeju Ocean View Resort",     "location": "Jeju Island",         "price": 110, "rating": 4.6, "amenities": ["WiFi", "Pool", "Ocean View"]},
    ],
    "paris": [
        {"name": "Montmartre Boutique Hotel",  "location": "Montmartre, Paris",   "price": 130, "rating": 4.3, "amenities": ["WiFi", "Breakfast", "City View"]},
        {"name": "Le Marais Hotel",            "location": "Le Marais, Paris",    "price": 180, "rating": 4.6, "amenities": ["WiFi", "Restaurant", "Bar"]},
        {"name": "Paris Budget Inn",           "location": "Near Eiffel Tower",   "price": 55,  "rating": 3.6, "amenities": ["WiFi", "Shared Bathroom"]},
    ],
    "singapore": [
        {"name": "Marina Bay Budget Inn",      "location": "Marina Bay",          "price": 90,  "rating": 4.0, "amenities": ["WiFi", "AC"]},
        {"name": "Sentosa Island Resort",      "location": "Sentosa Island",      "price": 220, "rating": 4.9, "amenities": ["WiFi", "Pool", "Beach", "Spa"]},
        {"name": "Chinatown Heritage Hotel",   "location": "Chinatown",           "price": 75,  "rating": 4.2, "amenities": ["WiFi", "Breakfast"]},
    ],
    "italy": [
        {"name": "Rome Centro Storico Hotel",  "location": "Centro Storico, Rome","price": 100, "rating": 4.4, "amenities": ["WiFi", "Breakfast"]},
        {"name": "Venice Canal View Hotel",    "location": "Grand Canal, Venice", "price": 200, "rating": 4.7, "amenities": ["WiFi", "Canal View", "Restaurant"]},
        {"name": "Florence Art Hotel",         "location": "Near Uffizi, Florence","price": 115,"rating": 4.5, "amenities": ["WiFi", "Breakfast", "Art Tours"]},
    ],
    "france": [  # alias
        {"name": "Montmartre Boutique Hotel",  "location": "Montmartre, Paris",   "price": 130, "rating": 4.3, "amenities": ["WiFi", "Breakfast", "City View"]},
        {"name": "Le Marais Hotel",            "location": "Le Marais, Paris",    "price": 180, "rating": 4.6, "amenities": ["WiFi", "Restaurant", "Bar"]},
    ],
    "tokyo": [
        {"name": "Tokyo Shibuya Hotel",        "location": "Shibuya, Tokyo",      "price": 80,  "rating": 4.2, "amenities": ["WiFi", "Breakfast", "AC"]},
        {"name": "Shinjuku Grand Hotel",       "location": "Shinjuku, Tokyo",     "price": 120, "rating": 4.5, "amenities": ["WiFi", "Pool", "Restaurant"]},
    ],
    "seoul": [
        {"name": "Myeongdong Tourist Hotel",   "location": "Myeongdong, Seoul",   "price": 70,  "rating": 4.1, "amenities": ["WiFi", "Breakfast"]},
        {"name": "Gangnam Luxury Hotel",       "location": "Gangnam, Seoul",      "price": 150, "rating": 4.8, "amenities": ["WiFi", "Pool", "Spa"]},
    ],
}


def search_hotels(
    destination: str,
    max_price_per_night: Optional[float] = None,
    min_rating: Optional[float] = None,
) -> str:
    """Search hotels in a destination with optional price/rating filters. Price is USD/night."""
    key = destination.lower().strip()
    hotels = None
    for k, v in HOTELS.items():
        if k in key or key in k:
            hotels = v
            break

    if hotels is None:
        available = ", ".join(sorted(set(HOTELS.keys())))
        return f"No hotel data for '{destination}'. Available: {available}"

    filtered = [
        h for h in hotels
        if (max_price_per_night is None or h["price"] <= max_price_per_night)
        and (min_rating is None or h["rating"] >= min_rating)
    ]

    if not filtered:
        return f"No hotels in {destination} match your filters (max ${max_price_per_night}/night, min rating {min_rating})."

    lines = [f"Hotels in {destination.title()} ({len(filtered)} results, price in USD/night):\n"]
    for h in sorted(filtered, key=lambda x: x["rating"], reverse=True):
        lines.append(
            f"  {h['name']}\n"
            f"    Location : {h['location']}\n"
            f"    Price    : ${h['price']}/night\n"
            f"    Rating   : {h['rating']}/5.0\n"
            f"    Amenities: {', '.join(h['amenities'])}\n"
        )
    return "\n".join(lines)
