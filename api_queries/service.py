import requests


from api_queries.queries1_repo import regions_with_severity, max_difference_between_consecutive_years_with_percentage

OPENCAGE_API_KEY = "bfa11842d84d477ebc17255c97c2cc3a"
def get_location(name):
    url = f"https://api.opencagedata.com/geocode/v1/json?q={name}&key={OPENCAGE_API_KEY}"

    response = requests.get(url)

    if response.status_code == 200:
        data = response.json()

        if data["results"]:
            location = data["results"][0]["geometry"]
            lon = location["lng"]
            lat = location["lat"]
            return {"lon": lon, "lat": lat}
        else:
            print(f"No geolocation data found for {name}.")
            return {"lon": 0.0, "lat": 0.0}
    else:
        print(f"Error fetching geolocation data: {response.status_code}")
        return {"lon": 0.0, "lat": 0.0}

def get_marker_color(avg_sev):
    if avg_sev > 75:
        return "red"
    elif avg_sev > 50:
        return "orange"
    elif avg_sev > 25:
        return "yellow"
    else:
        return "green"

def regions_severity_locations(limit=5):
    regions = regions_with_severity(limit)
    new_regions = []
    for region in regions:
        location = get_location(region[0])
        if location:
            try:
                avg_sev = float(region[1])
                new_regions.append({
                    "region_name": region[0],
                    "lat": location["lat"],
                    "lon": location["lon"],
                    "avg_sev": avg_sev,
                })
            except Exception as e:
                print(f"Error processing region {region[0]}: {e}")

    return new_regions

def regions_max_diff():
    regions = max_difference_between_consecutive_years_with_percentage()
    for region in regions:
        location = get_location(region["region_name"])
        if location:
            try:
                region["percentage_change"] = round(region["percentage_change"], 2)
                region["lat"] = location["lat"]
                region["lon"] = location["lon"]
            except Exception as e:
                print(f"Error processing region {region['region_name']}: {e}")
    return regions

