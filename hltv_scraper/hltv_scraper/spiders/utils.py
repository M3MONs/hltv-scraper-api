import json, os

def update_json_data(filename: str, data: dict):
    data_dir = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(__file__)))), "data")
    os.makedirs(data_dir, exist_ok=True)
    
    file = os.path.join(data_dir, f"{filename}.json")
    existing_data = {}

    try:
        if os.path.exists(file):
            with open(file, "r", encoding="utf-8") as f:
                existing_data = json.load(f)

        existing_data.update(data)

        with open(file, "w", encoding="utf-8") as f:
            json.dump(existing_data, f, indent=4)

    except Exception as e:
        print(f"An error occurred while updating JSON data: {e}")


def is_team_in_upcoming_match(match):
    return match.css("div.team1 .matchTeamName::text").get() is not None