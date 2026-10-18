"""
Config-driven Deterministic Vedic Rules for Daily Actions and Muhurtas.
Based on classical texts (Muhurta Chintamani, Brihat Samhita, Kalaprakasika).
"""

# Categorized action mappings for Tithis
TITHI_RULES = {
    "Purnima": {
        "recommended": [
            {"category": "Spiritual", "action": "Satyanarayan Puja, fasting & philanthropic donations", "reason": "Full Moon auspicious spiritual energy"},
            {"category": "Health", "action": "Meditation, yoga & mental rejuvenation", "reason": "High lunar vitality"}
        ],
        "avoid": [
            {"category": "Health", "action": "High-intensity physical exertion or overexertion", "reason": "Full Moon peak lunar energy is traditionally reserved for spiritual reflection and rest"}
        ],
        "weight": 1.2
    },
    "Amavasya": {
        "recommended": [
            {"category": "Spiritual", "action": "Pitru Tarpan, ancestral remembrance & charity", "reason": "Sacred day for honoring ancestors"}
        ],
        "avoid": [
            {"category": "Business", "action": "Signing major long-term financial deals or inaugurations", "reason": "Dark Moon period with minimal lunar vitality"},
            {"category": "Travel", "action": "Starting long exploratory journeys", "reason": "Low lunar guidance"}
        ],
        "weight": -0.8
    },
    "Ekadashi": {
        "recommended": [
            {"category": "Spiritual", "action": "Vrat (fasting), Vishnu puja, prayer & reading scriptures", "reason": "Sacred Ekadashi day for mental clarity and detox"},
            {"category": "Health", "action": "Sattvic diet, fasting & digital detox", "reason": "Optimal biophysical detoxification cycle"}
        ],
        "avoid": [
            {"category": "Lifestyle", "action": "Heavy grain consumption or non-sattvic food", "reason": "Traditional Ekadashi fasting discipline"}
        ],
        "weight": 1.5
    },
    "Chaturthi": {
        "recommended": [
            {"category": "Spiritual", "action": "Ganesha Puja, removing obstacles & strategic planning", "reason": "Ganesha's sacred Tithi"}
        ],
        "avoid": [
            {"category": "Business", "action": "Initiating peaceful alliance contracts", "reason": "Rikta Tithi suitable primarily for aggressive/protective actions"}
        ],
        "weight": 0.0
    },
    "Navami": {
        "recommended": [
            {"category": "Defense", "action": "Physical training, sports, surgical interventions & debate", "reason": "Rikta Tithi associated with fierce and competitive energy"}
        ],
        "avoid": [
            {"category": "Finance", "action": "Lending money or inaugurating luxury assets", "reason": "Rikta Tithi energy unsuitable for peace/growth preservation"}
        ],
        "weight": -0.3
    },
    "Chaturdashi": {
        "recommended": [
            {"category": "Spiritual", "action": "Shiva worship, clearing debt & ending toxic habits", "reason": "Shiva's sacred transformation Tithi"}
        ],
        "avoid": [
            {"category": "Real Estate", "action": "Griha Pravesh (Housewarming) or wedding celebrations", "reason": "Rikta Tithi with volatile energies"}
        ],
        "weight": -0.5
    }
}

# Nakshatra specific favorable actions
NAKSHATRA_RULES = {
    "Pushya": {
        "recommended": [
            {"category": "Wealth", "action": "Buying gold, real estate, jewelry or high-value investments", "reason": "Pushya is the most nourishing King of Nakshatras"},
            {"category": "Career", "action": "Launching new business ventures & signing employment contracts", "reason": "Highest sustained success potential"}
        ],
        "avoid": [
            {"category": "Relationship", "action": "Marriage ceremonies (traditional exception for Pushya)", "reason": "Pushya carries an ancient astrological constraint for Vivaha"}
        ],
        "weight": 2.0
    },
    "Rohini": {
        "recommended": [
            {"category": "Growth", "action": "Planting crops, construction, inaugurations & romantic unions", "reason": "Fixed (Dhruva) Nakshatra ruled by Brahma"}
        ],
        "avoid": [],
        "weight": 1.5
    },
    "Ashwini": {
        "recommended": [
            {"category": "Health", "action": "Starting medical treatments, surgeries, sports & fast travel", "reason": "Swift (Kshipra) Nakshatra ruled by Ashwini Kumaras (Divine Healers)"}
        ],
        "avoid": [],
        "weight": 1.2
    },
    "Krittika": {
        "recommended": [
            {"category": "Actions", "action": "Discarding clutter, negotiations requiring assertiveness & cooking", "reason": "Fiery (Ugra) Nakshatra ruled by Agni"}
        ],
        "avoid": [
            {"category": "Relationship", "action": "Delicate diplomatic compromises or long-term alliances", "reason": "Fiery cutting nature"}
        ],
        "weight": 0.2
    },
    "Swati": {
        "recommended": [
            {"category": "Vehicles", "action": "Buying automobiles, machinery, travel & learning music", "reason": "Movable (Chara) Nakshatra ruled by Vayu"}
        ],
        "avoid": [],
        "weight": 1.0
    },
    "Revati": {
        "recommended": [
            {"category": "Creative", "action": "Artistic projects, music recording, spiritual initiation & pet adoption", "reason": "Gentle (Mridu) Nakshatra ruled by Pushan"}
        ],
        "avoid": [],
        "weight": 1.1
    }
}

# Choghadiya Quality & Actions
CHOGHADIYA_RULES = {
    "Amrit": {
        "is_auspicious": True,
        "recommended": [
            {"category": "General", "action": "All auspicious starts, spiritual ceremonies, study & health", "reason": "Amrit Choghadiya (Nectar) yields long-lasting blessings"}
        ],
        "avoid": [],
        "score": 2.0
    },
    "Shubh": {
        "is_auspicious": True,
        "recommended": [
            {"category": "Finance", "action": "Financial transactions, contracts, weddings & religious events", "reason": "Shubh Choghadiya ruled by Jupiter generates auspicious growth"}
        ],
        "avoid": [],
        "score": 1.8
    },
    "Labh": {
        "is_auspicious": True,
        "recommended": [
            {"category": "Business", "action": "Commercial trade, sales campaigns, entering jobs & profit-making", "reason": "Labh Choghadiya ruled by Mercury maximizes commercial gains"}
        ],
        "avoid": [],
        "score": 1.5
    },
    "Char": {
        "is_auspicious": True,
        "recommended": [
            {"category": "Travel", "action": "Travel, logistics, movement, vehicle purchase & dynamic activities", "reason": "Char Choghadiya ruled by Venus favors motion & travel"}
        ],
        "avoid": [
            {"category": "Real Estate", "action": "Laying permanent foundation stones", "reason": "Char is mobile in nature"}
        ],
        "score": 0.8
    },
    "Rog": {
        "is_auspicious": False,
        "recommended": [
            {"category": "Debate", "action": "Competitive defense, medical diagnosis & confronting challenges", "reason": "Rog Choghadiya ruled by Mars favors assertive conflict resolution"}
        ],
        "avoid": [
            {"category": "General", "action": "Starting new business projects, partnerships or major journeys", "reason": "Rog Choghadiya creates friction & obstacles"}
        ],
        "score": -1.5
    },
    "Kaal": {
        "is_auspicious": False,
        "recommended": [
            {"category": "Labor", "action": "Deep cleaning, scrap clearing, hard physical labor & discipline", "reason": "Kaal Choghadiya ruled by Saturn"}
        ],
        "avoid": [
            {"category": "General", "action": "Auspicious ceremonies, investing savings or celebration launches", "reason": "Kaal (Time/Loss) causes delays and setbacks"}
        ],
        "score": -2.0
    },
    "Udveg": {
        "is_auspicious": False,
        "recommended": [
            {"category": "Government", "action": "Government filings, taxation paperwork & dealing with authority", "reason": "Udveg Choghadiya ruled by Sun"}
        ],
        "avoid": [
            {"category": "Mind", "action": "Delicate negotiations, sensitive family discussions or lending", "reason": "Udveg induces anxiety and restlessness"}
        ],
        "score": -1.2
    }
}

# Planetary Hora Guidance
HORA_RULES = {
    "Sun": {
        "recommended": [{"category": "Authority", "action": "Meeting superiors, government paperwork & leadership tasks", "reason": "Sun Hora enhances executive power"}],
        "avoid": [{"category": "Marriage", "action": "Gentle romantic reconciliations", "reason": "Fiery ego nature"}]
    },
    "Moon": {
        "recommended": [{"category": "Commerce", "action": "Public relations, client meetings, creative writing & culinary arts", "reason": "Moon Hora enhances intuition & empathy"}],
        "avoid": [{"category": "Aggression", "action": "Fierce arguments or litigation filings", "reason": "Soft lunar nature"}]
    },
    "Mars": {
        "recommended": [{"category": "Action", "action": "Sports, gym workouts, buying land/machinery & surgical procedures", "reason": "Mars Hora boosts physical vitality"}],
        "avoid": [{"category": "Diplomacy", "action": "Signing peace accords or delicate negotiations", "reason": "High impulsiveness"}]
    },
    "Mercury": {
        "recommended": [{"category": "Finance", "action": "Trading, accounting, writing code, learning & signing business contracts", "reason": "Mercury Hora sharpens intellect & commerce"}],
        "avoid": [],
    },
    "Jupiter": {
        "recommended": [{"category": "Wealth", "action": "Major investments, consultations with mentors, education & temple visits", "reason": "Jupiter Hora is the supreme auspicious hour"}],
        "avoid": [],
    },
    "Venus": {
        "recommended": [{"category": "Luxury", "action": "Purchasing vehicles, clothes, art, dates & entertainment launches", "reason": "Venus Hora enhances beauty, arts & connection"}],
        "avoid": [{"category": "Hard Labor", "action": "Demolition or heavy harsh labor", "reason": "Refined aesthetic nature"}]
    },
    "Saturn": {
        "recommended": [{"category": "Foundations", "action": "Excavation, long-term investments, agriculture, oil/iron deals & meditation", "reason": "Saturn Hora favors patience & grounding"}],
        "avoid": [{"category": "Speed", "action": "Fast-turnaround speculative trades or fast trips", "reason": "Slowness and restriction"}]
    }
}

# Disha Shool (Prohibited Direction for travel on weekdays + Vedic Remedy)
DISHA_SHOOL = {
    0: {"direction": "West", "sanskrit": "Pashchim", "remedy": "Consume betel leaf (Paan) or ghee before departure", "avoid_msg": "Avoid long-distance travel towards West on Sunday"},
    1: {"direction": "East", "sanskrit": "Purva", "remedy": "Look into a mirror or drink a spoonful of milk before leaving", "avoid_msg": "Avoid long-distance travel towards East on Monday"},
    2: {"direction": "North", "sanskrit": "Uttara", "remedy": "Eat jaggery (Gud) or coriander seeds before departure", "avoid_msg": "Avoid long-distance travel towards North on Tuesday"},
    3: {"direction": "North", "sanskrit": "Uttara", "remedy": "Eat jaggery or curd with sugar before leaving", "avoid_msg": "Avoid long-distance travel towards North on Wednesday"},
    4: {"direction": "South", "sanskrit": "Dakshin", "remedy": "Consume yellow mustard seeds or curd before departure", "avoid_msg": "Avoid long-distance travel towards South on Thursday"},
    5: {"direction": "West", "sanskrit": "Pashchim", "remedy": "Eat barley (Jau) or curd before leaving", "avoid_msg": "Avoid long-distance travel towards West on Friday"},
    6: {"direction": "East", "sanskrit": "Purva", "remedy": "Consume ginger (Adrak) or black sesame before departure", "avoid_msg": "Avoid long-distance travel towards East on Saturday"}
}
