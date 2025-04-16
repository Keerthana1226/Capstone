import json

def generate_crop_rotation_plan(dataset_path, start_crop, start_month=1, max_months=12):
    with open(dataset_path, 'r') as f:
        crops = json.load(f)

    crop_plan = []
    current_month = start_month
    current_crop = start_crop
    months_used = 0

    while months_used < max_months:
        crop_info = crops.get(current_crop)
        if not crop_info:
            break

        growth = crop_info['grow_duration']
        planting_months = crop_info['planting_months']

        if current_month not in planting_months:
            found = False
            for shift in range(1, 13):
                try_month = (current_month + shift - 1) % 12 + 1
                if try_month in planting_months:
                    current_month = try_month
                    months_used += shift
                    found = True
                    break
            if not found or months_used >= max_months:
                break

        # Now plant crop
        end_month = ((current_month + growth - 1) - 1) % 12 + 1

        crop_plan.append({
            "Crop": current_crop,
            "Start Month": current_month,
            "End Month": end_month
        })

        months_used += growth
        current_month = ((current_month + growth - 1) % 12) + 1

        # Look for valid successors
        valid_successors = []
        for next_crop in crop_info['successor_crops']:
            next_info = crops.get(next_crop)
            if next_info:
                if current_month in next_info['planting_months']:
                    valid_successors.append(next_crop)

        if valid_successors:
            current_crop = valid_successors[0]
        else:
            found = False
            for shift in range(1, 13):
                try_month = (current_month + shift - 1) % 12 + 1
                for crop_name, crop_data in crops.items():
                    if try_month in crop_data['planting_months']:
                        current_crop = crop_name
                        current_month = try_month
                        months_used += shift
                        found = True
                        break
                if found:
                    break
            if not found:
                break

    return crop_plan
