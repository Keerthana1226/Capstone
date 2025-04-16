import requests
import json
import time

def get_wikimedia_image_url(name):
    search_url = "https://en.wikipedia.org/w/api.php"
    params = {
        "action": "query",
        "format": "json",
        "prop": "pageimages",
        "titles": name,
        "pithumbsize": 500,
        "redirects": 1
    }
    try:
        response = requests.get(search_url, params=params)
        data = response.json()
        pages = data.get("query", {}).get("pages", {})
        for page_id, page_data in pages.items():
            if "thumbnail" in page_data:
                return page_data["thumbnail"]["source"]
    except Exception as e:
        print(f"Error fetching image for {name}: {e}")
    return None

with open("indian_crop_dataset.json", "r") as f:
    crop_data = json.load(f)

for crop, details in crop_data.items():
    print(f"Fetching image for crop: {crop}")
    crop_data[crop]["image_url"] = get_wikimedia_image_url(crop) or "Image not found"
    time.sleep(0.5)

    updated_successors = {}
    for successor in details.get("successor_crops", []):
        print(f"   ↪ Fetching image for successor: {successor}")
        img = get_wikimedia_image_url(successor) or "Image not found"
        updated_successors[successor] = {"image_url": img}
        time.sleep(0.5)

    crop_data[crop]["successors"] = updated_successors

# Save the final dataset
with open("crops_with_successor_images.json", "w") as f:
    json.dump(crop_data, f, indent=4)

print("✅ All images (main + successor crops) fetched and saved.")
