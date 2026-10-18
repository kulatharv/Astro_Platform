"""Vedic Planetary Aspects (Drishti) Engine."""


def calculate_vedic_aspects(chart: dict) -> dict[str, list[int]]:
    """
    Calculate Vedic Drishti (aspects cast by planets onto other houses).
    Standard rule: All planets aspect the 7th house from their position.
    Special aspects:
      - Mars: 4th, 7th, 8th
      - Jupiter: 5th, 7th, 9th
      - Saturn: 3rd, 7th, 10th
      - Rahu/Ketu: 5th, 7th, 9th
    """
    aspects = {}
    planets_by_house = chart.get("planets_by_house", {})

    for house_str, planet_list in planets_by_house.items():
        try:
            h = int(house_str)
        except (ValueError, TypeError):
            continue

        for p in planet_list:
            name = p.get("planet")
            targeted_houses = []

            # 7th aspect for all
            targeted_houses.append(((h + 6 - 1) % 12) + 1)

            if name == "Mars":
                targeted_houses.append(((h + 4 - 1) % 12) + 1)
                targeted_houses.append(((h + 8 - 1) % 12) + 1)
            elif name in ("Jupiter", "Rahu", "Ketu"):
                targeted_houses.append(((h + 5 - 1) % 12) + 1)
                targeted_houses.append(((h + 9 - 1) % 12) + 1)
            elif name == "Saturn":
                targeted_houses.append(((h + 3 - 1) % 12) + 1)
                targeted_houses.append(((h + 10 - 1) % 12) + 1)

            aspects[name] = sorted(list(set(targeted_houses)))

    return aspects
