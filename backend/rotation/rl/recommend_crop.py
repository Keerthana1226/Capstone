import pickle
import json
import os
import sys
from collections import defaultdict

# Paths
BASE_DIR = os.path.dirname(__file__)
DATA_PATH = os.path.join(BASE_DIR, 'crop_data.json')
QTABLE_PATH = os.path.join(BASE_DIR, 'output', 'trained_q_table.pkl')

# Load crop data
with open(DATA_PATH, 'r') as f:
    crop_data = json.load(f)

# Dynamic crop name mappings
crop_names = list(crop_data.keys())
crop_to_index = {name: idx for idx, name in enumerate(crop_names)}
index_to_crop = {idx: name for name, idx in crop_to_index.items()}

seasons = ["Spring", "Summer", "Fall", "Winter"]
season_to_index = {season: idx for idx, season in enumerate(seasons)}
month_to_season = {
    1: "Winter", 2: "Winter", 3: "Spring", 4: "Spring", 5: "Spring", 6: "Summer",
    7: "Summer", 8: "Summer", 9: "Fall", 10: "Fall", 11: "Fall", 12: "Winter"
}
season_to_month = { "Spring": 4, "Summer": 7, "Fall": 10, "Winter": 1 }

# Load Q-table
try:
    with open(QTABLE_PATH, 'rb') as f:
        q_table = pickle.load(f)
except FileNotFoundError:
    q_table = {}

def find_closest_month(target_month, available_months):
    if not available_months:
        return None
    return min(available_months, key=lambda m: min(abs(m - target_month), 12 - abs(m - target_month)))

def extract_available_months(q_table):
    return sorted(set(s[0] for (s, _), _ in q_table.items() if isinstance(s, tuple) and len(s) >= 1 and 1 <= s[0] <= 12))

def get_recommendations(last_crop_name, season_name=None, month=None, max_recommendations=3, min_q_value=0):
    last_crop_name = last_crop_name.strip().title()
    if last_crop_name not in crop_to_index:
        close_matches = [name for name in crop_names if last_crop_name.lower() in name.lower()]
        if close_matches:
            return None, f"Invalid crop name: '{last_crop_name}'. Did you mean: {', '.join(close_matches)}"
        return None, f"Invalid crop name: '{last_crop_name}'."

    if month is None and season_name:
        season_name = season_name.strip().title()
        if season_name not in season_to_month:
            return None, f"Invalid season: '{season_name}'."
        month = season_to_month[season_name]

    if season_name is None and month is not None:
        try:
            month = int(month)
            if month < 1 or month > 12:
                return None, f"Invalid month: {month}."
            season_name = month_to_season[month]
        except:
            return None, f"Invalid month: {month}."
    elif season_name is None and month is None:
        return None, "Please provide a season or month."

    crop_index = crop_to_index[last_crop_name]
    original_state = (month, crop_index)

    state_actions = {}
    for (s, a), q in q_table.items():
        if s == original_state:
            state_actions[a] = q

    if not state_actions:
        closest_month = find_closest_month(month, extract_available_months(q_table))
        alt_state = (closest_month, crop_index)
        for (s, a), q in q_table.items():
            if s == alt_state:
                state_actions[a] = q

    if not state_actions:
        alt_state = (crop_index, season_to_index.get(season_name, 0))
        for (s, a), q in q_table.items():
            if s == alt_state:
                state_actions[a] = q

    if not state_actions:
        crop_actions = defaultdict(list)
        for (s, a), q in q_table.items():
            if isinstance(s, tuple) and len(s) >= 2 and s[1] == crop_index:
                crop_actions[a].append(q)
        for action, values in crop_actions.items():
            state_actions[action] = sum(values) / len(values)

    if not state_actions:
        return None, f"No recommendations found for '{last_crop_name}' in {season_name}."

    allowed_successors = crop_data.get(last_crop_name, {}).get("successor_crops", [])
    allowed_indices = [crop_to_index[c] for c in allowed_successors if c in crop_to_index]

    penalized_actions = []
    for a, q in state_actions.items():
        adjusted_q = q if a in allowed_indices else q - 5
        penalized_actions.append((a, adjusted_q))

    sorted_actions = sorted(penalized_actions, key=lambda x: x[1], reverse=True)

    recommendations = []
    for a, q in sorted_actions:
        if q < min_q_value or a not in index_to_crop:
            continue
        name = index_to_crop[a]
        data = crop_data.get(name, {})
        recommendations.append({
            "crop": name,
            "confidence": round(q, 2),
            "image_url": data.get("image_url", ""),
            "family": data.get("family", "Unknown"),
            "planting_months": data.get("planting_months", []),
            "grow_duration": data.get("grow_duration", "Unknown"),
            "successor_crops": data.get("successor_crops", [])
        })
        if len(recommendations) >= max_recommendations:
            break

    if not recommendations:
        return None, f"No suitable recommendations found for '{last_crop_name}' in {season_name}."

    return recommendations, None

def main():
    if '--json' in sys.argv:
        # API mode
        try:
            last_crop = input().strip()
            month_or_season = input().strip()
            try:
                month = int(month_or_season)
                season = None
            except:
                month = None
                season = month_or_season.strip().title()
            results, error = get_recommendations(last_crop, season_name=season, month=month)
            if error:
                print(json.dumps({"error": error}))
            else:
                print(json.dumps({"recommendations": results}, indent=2))
        except Exception as e:
            print(json.dumps({"error": f"Unexpected error: {str(e)}"}))
    else:
        # CLI mode
        print("Smart Crop Rotation Assistant (Interactive Mode)")
        last_crop = input("Enter last crop: ").strip()
        season_or_month = input("Enter current season or month: ").strip()
        try:
            month = int(season_or_month)
            season = None
        except:
            month = None
            season = season_or_month
        results, error = get_recommendations(last_crop, season_name=season, month=month)
        if error:
            print("❌", error)
        else:
            print("\n✅ Recommended Crops:")
            for i, rec in enumerate(results, 1):
                print(f"{i}. {rec['crop']} (Confidence: {rec['confidence']})")
                print(f"   Family: {rec['family']}")
                print(f"   Grow Duration: {rec['grow_duration']}")
                print(f"   Planting Months: {', '.join(map(str, rec['planting_months']))}")
                print(f"   Successor Crops: {', '.join(rec['successor_crops'])}")
                print()

if __name__ == '__main__':
    main()
