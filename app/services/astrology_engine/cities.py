"""Comprehensive city database and coordinates resolver for Indian and international cities."""

import requests

CITIES = {
    # ── Maharashtra ──
    "Pune": {"lat": 18.5204, "lon": 73.8567, "timezone": 5.5},
    "Mumbai": {"lat": 19.0760, "lon": 72.8777, "timezone": 5.5},
    "Nagpur": {"lat": 21.1458, "lon": 79.0882, "timezone": 5.5},
    "Nashik": {"lat": 20.0059, "lon": 73.7897, "timezone": 5.5},
    "Aurangabad": {"lat": 19.8762, "lon": 75.3433, "timezone": 5.5},
    "Chhatrapati Sambhajinagar": {"lat": 19.8762, "lon": 75.3433, "timezone": 5.5},
    "Solapur": {"lat": 17.6868, "lon": 75.9064, "timezone": 5.5},
    "Kolhapur": {"lat": 16.7050, "lon": 74.2433, "timezone": 5.5},
    "Amravati": {"lat": 20.9374, "lon": 77.7796, "timezone": 5.5},
    "Nanded": {"lat": 19.1383, "lon": 77.3210, "timezone": 5.5},
    "Thane": {"lat": 19.2183, "lon": 72.9781, "timezone": 5.5},
    "Navi Mumbai": {"lat": 19.0330, "lon": 73.0297, "timezone": 5.5},

    # ── Delhi / NCR ──
    "Delhi": {"lat": 28.6139, "lon": 77.2090, "timezone": 5.5},
    "New Delhi": {"lat": 28.6139, "lon": 77.2090, "timezone": 5.5},
    "Noida": {"lat": 28.5355, "lon": 77.3910, "timezone": 5.5},
    "Gurgaon": {"lat": 28.4595, "lon": 77.0266, "timezone": 5.5},
    "Gurugram": {"lat": 28.4595, "lon": 77.0266, "timezone": 5.5},
    "Faridabad": {"lat": 28.4089, "lon": 77.3178, "timezone": 5.5},
    "Ghaziabad": {"lat": 28.6692, "lon": 77.4538, "timezone": 5.5},

    # ── Karnataka ──
    "Bangalore": {"lat": 12.9716, "lon": 77.5946, "timezone": 5.5},
    "Bengaluru": {"lat": 12.9716, "lon": 77.5946, "timezone": 5.5},
    "Mysore": {"lat": 12.2958, "lon": 76.6394, "timezone": 5.5},
    "Mysuru": {"lat": 12.2958, "lon": 76.6394, "timezone": 5.5},
    "Hubli": {"lat": 15.3647, "lon": 75.1240, "timezone": 5.5},
    "Mangalore": {"lat": 12.9141, "lon": 74.8560, "timezone": 5.5},
    "Belgaum": {"lat": 15.8497, "lon": 74.4977, "timezone": 5.5},
    "Gulbarga": {"lat": 17.3297, "lon": 76.8343, "timezone": 5.5},

    # ── Tamil Nadu ──
    "Chennai": {"lat": 13.0827, "lon": 80.2707, "timezone": 5.5},
    "Madras": {"lat": 13.0827, "lon": 80.2707, "timezone": 5.5},
    "Coimbatore": {"lat": 11.0168, "lon": 76.9558, "timezone": 5.5},
    "Madurai": {"lat": 9.9252, "lon": 78.1198, "timezone": 5.5},
    "Salem": {"lat": 11.6643, "lon": 78.1460, "timezone": 5.5},
    "Trichy": {"lat": 10.7905, "lon": 78.7047, "timezone": 5.5},
    "Tirunelveli": {"lat": 8.7139, "lon": 77.7567, "timezone": 5.5},
    "Vellore": {"lat": 12.9165, "lon": 79.1325, "timezone": 5.5},

    # ── Andhra Pradesh / Telangana ──
    "Hyderabad": {"lat": 17.3850, "lon": 78.4867, "timezone": 5.5},
    "Secunderabad": {"lat": 17.4399, "lon": 78.4983, "timezone": 5.5},
    "Visakhapatnam": {"lat": 17.6868, "lon": 83.2185, "timezone": 5.5},
    "Vijayawada": {"lat": 16.5062, "lon": 80.6480, "timezone": 5.5},
    "Tirupati": {"lat": 13.6288, "lon": 79.4192, "timezone": 5.5},
    "Warangal": {"lat": 17.9784, "lon": 79.5941, "timezone": 5.5},
    "Guntur": {"lat": 16.3067, "lon": 80.4365, "timezone": 5.5},
    "Nellore": {"lat": 14.4426, "lon": 79.9865, "timezone": 5.5},

    # ── Gujarat ──
    "Ahmedabad": {"lat": 23.0225, "lon": 72.5714, "timezone": 5.5},
    "Surat": {"lat": 21.1702, "lon": 72.8311, "timezone": 5.5},
    "Vadodara": {"lat": 22.3072, "lon": 73.1812, "timezone": 5.5},
    "Rajkot": {"lat": 22.3039, "lon": 70.8022, "timezone": 5.5},
    "Bhavnagar": {"lat": 21.7645, "lon": 72.1519, "timezone": 5.5},
    "Jamnagar": {"lat": 22.4707, "lon": 70.0577, "timezone": 5.5},
    "Gandhinagar": {"lat": 23.2156, "lon": 72.6369, "timezone": 5.5},

    # ── Rajasthan ──
    "Jaipur": {"lat": 26.9124, "lon": 75.7873, "timezone": 5.5},
    "Jodhpur": {"lat": 26.2389, "lon": 73.0243, "timezone": 5.5},
    "Udaipur": {"lat": 24.5854, "lon": 73.7125, "timezone": 5.5},
    "Kota": {"lat": 25.2138, "lon": 75.8648, "timezone": 5.5},
    "Ajmer": {"lat": 26.4499, "lon": 74.6399, "timezone": 5.5},
    "Bikaner": {"lat": 28.0229, "lon": 73.3119, "timezone": 5.5},

    # ── Uttar Pradesh / Uttarakhand ──
    "Lucknow": {"lat": 26.8467, "lon": 80.9462, "timezone": 5.5},
    "Varanasi": {"lat": 25.3176, "lon": 82.9739, "timezone": 5.5},
    "Kanpur": {"lat": 26.4499, "lon": 80.3319, "timezone": 5.5},
    "Agra": {"lat": 27.1767, "lon": 78.0081, "timezone": 5.5},
    "Prayagraj": {"lat": 25.4358, "lon": 81.8463, "timezone": 5.5},
    "Allahabad": {"lat": 25.4358, "lon": 81.8463, "timezone": 5.5},
    "Meerut": {"lat": 28.9845, "lon": 77.7064, "timezone": 5.5},
    "Ayodhya": {"lat": 26.7922, "lon": 82.1998, "timezone": 5.5},
    "Haridwar": {"lat": 29.9457, "lon": 78.1642, "timezone": 5.5},
    "Dehradun": {"lat": 30.3165, "lon": 78.0322, "timezone": 5.5},
    "Rishikesh": {"lat": 30.0869, "lon": 78.2676, "timezone": 5.5},

    # ── Madhya Pradesh ──
    "Bhopal": {"lat": 23.2599, "lon": 77.4126, "timezone": 5.5},
    "Indore": {"lat": 22.7196, "lon": 75.8577, "timezone": 5.5},
    "Gwalior": {"lat": 26.2183, "lon": 78.1828, "timezone": 5.5},
    "Jabalpur": {"lat": 23.1815, "lon": 79.9864, "timezone": 5.5},
    "Ujjain": {"lat": 23.1765, "lon": 75.7885, "timezone": 5.5},

    # ── West Bengal / East ──
    "Kolkata": {"lat": 22.5726, "lon": 88.3639, "timezone": 5.5},
    "Calcutta": {"lat": 22.5726, "lon": 88.3639, "timezone": 5.5},
    "Patna": {"lat": 25.5941, "lon": 85.1376, "timezone": 5.5},
    "Bhubaneswar": {"lat": 20.2961, "lon": 85.8245, "timezone": 5.5},
    "Cuttack": {"lat": 20.4625, "lon": 85.8830, "timezone": 5.5},
    "Ranchi": {"lat": 23.3441, "lon": 85.3096, "timezone": 5.5},
    "Guwahati": {"lat": 26.1445, "lon": 91.7362, "timezone": 5.5},

    # ── Punjab / Haryana / North ──
    "Chandigarh": {"lat": 30.7333, "lon": 76.7794, "timezone": 5.5},
    "Amritsar": {"lat": 31.6340, "lon": 74.8723, "timezone": 5.5},
    "Ludhiana": {"lat": 30.9010, "lon": 75.8573, "timezone": 5.5},
    "Jalandhar": {"lat": 31.3260, "lon": 75.5762, "timezone": 5.5},
    "Shimla": {"lat": 31.1048, "lon": 77.1734, "timezone": 5.5},
    "Srinagar": {"lat": 34.0837, "lon": 74.7973, "timezone": 5.5},
    "Jammu": {"lat": 32.7266, "lon": 74.8570, "timezone": 5.5},

    # ── Kerala / Goa ──
    "Kochi": {"lat": 9.9312, "lon": 76.2673, "timezone": 5.5},
    "Cochin": {"lat": 9.9312, "lon": 76.2673, "timezone": 5.5},
    "Thiruvananthapuram": {"lat": 8.5241, "lon": 76.9366, "timezone": 5.5},
    "Trivandrum": {"lat": 8.5241, "lon": 76.9366, "timezone": 5.5},
    "Kozhikode": {"lat": 11.2588, "lon": 75.7804, "timezone": 5.5},
    "Panaji": {"lat": 15.4909, "lon": 73.8278, "timezone": 5.5},
    "Goa": {"lat": 15.2993, "lon": 74.1240, "timezone": 5.5},

    # ── International Capitals & Hubs ──
    "London": {"lat": 51.5074, "lon": -0.1278, "timezone": 0.0},
    "New York": {"lat": 40.7128, "lon": -74.0060, "timezone": -5.0},
    "San Francisco": {"lat": 37.7749, "lon": -122.4194, "timezone": -8.0},
    "Dubai": {"lat": 25.2048, "lon": 55.2708, "timezone": 4.0},
    "Singapore": {"lat": 1.3521, "lon": 103.8198, "timezone": 8.0},
    "Toronto": {"lat": 43.6532, "lon": -79.3832, "timezone": -5.0},
    "Sydney": {"lat": -33.8688, "lon": 151.2093, "timezone": 10.0},
}

CITY_CACHE: dict[str, dict] = {}


def get_city(name: str) -> tuple[float, float, float] | None:
    """
    Look up coordinates and timezone for a city name.
    Returns: (latitude, longitude, timezone_offset_hours) or None.
    """
    if not name:
        return None

    clean_name = name.strip()

    # 1. Exact match
    if clean_name in CITIES:
        c = CITIES[clean_name]
        return c["lat"], c["lon"], c["timezone"]

    # 2. Case-insensitive match
    lower_name = clean_name.lower()
    for key, c in CITIES.items():
        if key.lower() == lower_name:
            return c["lat"], c["lon"], c["timezone"]

    # 3. Dynamic cache lookup
    if clean_name in CITY_CACHE:
        c = CITY_CACHE[clean_name]
        return c["lat"], c["lon"], c["timezone"]

    # 4. Fallback: Default to Pune / IST if unknown
    return None


def get_city_names() -> list[str]:
    """Return sorted list of all built-in city names."""
    return sorted(CITIES.keys())
