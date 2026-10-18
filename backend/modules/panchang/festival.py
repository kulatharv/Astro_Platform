"""Live Hindu Festival Engine computed from Swiss Ephemeris lunar & solar data with astronomical precision."""

from datetime import datetime, timedelta
from typing import Any, Dict, List, Optional
import swisseph as swe

MONTH_NAMES = [
    "", "Chaitra", "Vaisakha", "Jyeshtha", "Ashadha", "Shravana",
    "Bhadrapada", "Ashwina", "Kartika", "Margashirsha", "Pausha", "Magha", "Phalguna"
]

NAKSHATRA_NAMES = [
    "Ashwini", "Bharani", "Krittika", "Rohini", "Mrigashira", "Ardra", "Punarvasu",
    "Pushya", "Ashlesha", "Magha", "Purva Phalguni", "Uttara Phalguni", "Hasta",
    "Chitra", "Swati", "Vishakha", "Anuradha", "Jyeshtha", "Mula", "Purva Ashadha",
    "Uttara Ashadha", "Shravana", "Dhanishta", "Shatabhisha", "Purva Bhadrapada",
    "Uttara Bhadrapada", "Revati"
]

TITHI_NAMES = [
    "Pratipada", "Dwitiya", "Tritiya", "Chaturthi", "Panchami", "Shashthi",
    "Saptami", "Ashtami", "Navami", "Dashami", "Ekadashi", "Dwadashi",
    "Trayodashi", "Chaturdashi", "Purnima",
    "Pratipada", "Dwitiya", "Tritiya", "Chaturthi", "Panchami", "Shashthi",
    "Saptami", "Ashtami", "Navami", "Dashami", "Ekadashi", "Dwadashi",
    "Trayodashi", "Chaturdashi", "Amavasya"
]

ANNUAL_FESTIVALS: List[Dict[str, Any]] = [
    {"month_lunar": 1, "paksha": "Shukla", "tithi_in_paksha": 1, "name": "Gudi Padwa / Ugadi / Chaitra Navratri Begins", "tag": "major", "icon": "🚩", "desc": "Vedic New Year and invocation of Divine Mother Durga.", "remedies": "Erect Gudi / Neem-Jaggery prasad, invoke blessings of Maa Durga."},
    {"month_lunar": 1, "paksha": "Shukla", "tithi_in_paksha": 9, "name": "Rama Navami", "tag": "major", "icon": "🏹", "desc": "Divine birth celebration of Maryada Purushottam Lord Rama.", "remedies": "Chant Shri Rama Raksha Stotra, perform Rama Archana at midday."},
    {"month_lunar": 1, "paksha": "Shukla", "tithi_in_paksha": 11, "name": "Kamada Ekadashi", "tag": "ekadashi", "icon": "🌿", "desc": "Sacred Ekadashi for fulfillment of righteous desires.", "remedies": "Observe Ekadashi fast, offer Tulsi leaves to Lord Vishnu."},
    {"month_lunar": 1, "paksha": "Shukla", "tithi_in_paksha": 15, "name": "Hanuman Jayanti (Chaitra Purnima)", "tag": "major", "icon": "🐒", "desc": "Birth of Lord Hanuman, embodiment of courage, strength, and devotion.", "remedies": "Recite Hanuman Chalisa 7 times and offer sindoor with jasmine oil."},
    {"month_lunar": 1, "paksha": "Krishna", "tithi_in_paksha": 11, "name": "Varuthini Ekadashi", "tag": "ekadashi", "icon": "🌿", "desc": "Virtuous Ekadashi removing past negative karmas.", "remedies": "Fast dedicated to Lord Vamana avatar."},
    {"month_lunar": 2, "paksha": "Shukla", "tithi_in_paksha": 3, "name": "Akshaya Tritiya (Parashurama Jayanti)", "tag": "major", "icon": "✨", "desc": "Day of eternal auspiciousness, unending prosperity, and noble charity.", "remedies": "Gold/silver purchase, donation of water and food grains."},
    {"month_lunar": 2, "paksha": "Shukla", "tithi_in_paksha": 11, "name": "Mohini Ekadashi", "tag": "ekadashi", "icon": "🌿", "desc": "Ekadashi commemorating Lord Vishnu enchantress Mohini form.", "remedies": "Fast for purification of consciousness."},
    {"month_lunar": 2, "paksha": "Shukla", "tithi_in_paksha": 14, "name": "Narasimha Jayanti", "tag": "vrat", "icon": "🦁", "desc": "Sunset advent of Lord Narasimha protecting devotee Prahlada.", "remedies": "Sunset meditation and prayer for fearlessness."},
    {"month_lunar": 2, "paksha": "Shukla", "tithi_in_paksha": 15, "name": "Buddha Purnima (Vaisakha Purnima)", "tag": "purnima", "icon": "🌕", "desc": "Celebration of Lord Buddha enlightenment and compassion.", "remedies": "Satyanarayan puja and distribution of food to the needy."},
    {"month_lunar": 2, "paksha": "Krishna", "tithi_in_paksha": 11, "name": "Apara Ekadashi", "tag": "ekadashi", "icon": "🌿", "desc": "Ekadashi granting boundless spiritual merit.", "remedies": "Vishnu worship with sacred yellow flowers."},
    {"month_lunar": 3, "paksha": "Shukla", "tithi_in_paksha": 10, "name": "Ganga Dussehra", "tag": "vrat", "icon": "🌊", "desc": "Descent of holy river Ganga upon Earth.", "remedies": "Holy dip in holy rivers or offer Ganga jal at home."},
    {"month_lunar": 3, "paksha": "Shukla", "tithi_in_paksha": 11, "name": "Nirjala Ekadashi", "tag": "major", "icon": "💧", "desc": "Most sacred Ekadashi observed with waterless fast.", "remedies": "Donate water pitchers, hand fans, and summer fruits."},
    {"month_lunar": 3, "paksha": "Shukla", "tithi_in_paksha": 15, "name": "Vat Purnima (Jyeshtha Purnima)", "tag": "vrat", "icon": "🌳", "desc": "Worship of sacred Banyan tree for spouse longevity and family harmony.", "remedies": "Tie sacred white/yellow thread around Banyan tree."},
    {"month_lunar": 3, "paksha": "Krishna", "tithi_in_paksha": 11, "name": "Yogini Ekadashi", "tag": "ekadashi", "icon": "🌿", "desc": "Fast for physical well-being and purification.", "remedies": "Fast dedicated to Lord Narayana."},
    {"month_lunar": 3, "paksha": "Krishna", "tithi_in_paksha": 15, "name": "Vat Savitri Vrat (Amavasya) / Shani Jayanti", "tag": "amavasya", "icon": "🌑", "desc": "Devotion of Devi Savitri and birth of Lord Shani Dev.", "remedies": "Offer mustard oil and black sesame to Shani Dev."},
    {"month_lunar": 4, "paksha": "Shukla", "tithi_in_paksha": 2, "name": "Jagannath Ratha Yatra", "tag": "major", "icon": "🛕", "desc": "Grand Chariot procession of Lord Jagannath, Balabhadra, and Subhadra.", "remedies": "Sing Jagannath Ashtakam and Mahamantra."},
    {"month_lunar": 4, "paksha": "Shukla", "tithi_in_paksha": 11, "name": "Devshayani Ekadashi (Ashadhi Ekadashi)", "tag": "major", "icon": "🌿", "desc": "Beginning of the 4-month sacred Chaturmas period.", "remedies": "Begin sacred sankalpa, observe fast, recite Vishnu Sahasranama."},
    {"month_lunar": 4, "paksha": "Shukla", "tithi_in_paksha": 15, "name": "Guru Purnima (Vyasa Puja)", "tag": "major", "icon": "🧘", "desc": "Veneration of spiritual teachers, mentors, and Sage Veda Vyasa.", "remedies": "Express gratitude to Guru and parents; chant Guru Paduka Stotram."},
    {"month_lunar": 4, "paksha": "Krishna", "tithi_in_paksha": 11, "name": "Kamika Ekadashi", "tag": "ekadashi", "icon": "🌿", "desc": "Ekadashi for spiritual purification during early Chaturmas.", "remedies": "Offer Tulsi leaves to Lord Krishna."},
    {"month_lunar": 5, "paksha": "Shukla", "tithi_in_paksha": 3, "name": "Hariyali Teej", "tag": "vrat", "icon": "🌸", "desc": "Celebration of the divine reunion of Shiva and Parvati.", "remedies": "Shiva-Parvati worship for happy married life."},
    {"month_lunar": 5, "paksha": "Shukla", "tithi_in_paksha": 5, "name": "Nag Panchami", "tag": "vrat", "icon": "🐍", "desc": "Sacred worship of Serpent deities for nature harmony and Rahu remedies.", "remedies": "Offer milk and kheer to snake deities for Rahu-Ketu dosha shanti."},
    {"month_lunar": 5, "paksha": "Shukla", "tithi_in_paksha": 11, "name": "Shravana Putrada Ekadashi", "tag": "ekadashi", "icon": "🌿", "desc": "Ekadashi fast for progeny protection and spiritual prosperity.", "remedies": "Fast dedicated to Lord Vishnu."},
    {"month_lunar": 5, "paksha": "Shukla", "tithi_in_paksha": 15, "name": "Raksha Bandhan (Shravani Purnima / Upakarma)", "tag": "major", "icon": "🧵", "desc": "Sacred thread ritual of brother-sister bond and Vedic Upakarma.", "remedies": "Tie Rakhi, exchange auspicious blessings and sweets."},
    {"month_lunar": 5, "paksha": "Krishna", "tithi_in_paksha": 8, "name": "Krishna Janmashtami (Gokulashtami)", "tag": "major", "icon": "🦚", "desc": "Divine birth celebration of Lord Krishna in midnight Rohini Nakshatra.", "remedies": "Midnight Puja, offer Makhan-Mishri bhog and cradle infant Krishna."},
    {"month_lunar": 5, "paksha": "Krishna", "tithi_in_paksha": 11, "name": "Aja Ekadashi", "tag": "ekadashi", "icon": "🌿", "desc": "Ekadashi for cleansing past negativities and gaining clarity.", "remedies": "Worship Lord Hrishikesha with heartfelt prayer."},
    {"month_lunar": 6, "paksha": "Shukla", "tithi_in_paksha": 3, "name": "Hartalika Teej", "tag": "vrat", "icon": "🌺", "desc": "Vow of Devi Parvati for obtaining Lord Shiva as consort.", "remedies": "Observe Nirjala fast and worship handmade Shiva-Parvati idols."},
    {"month_lunar": 6, "paksha": "Shukla", "tithi_in_paksha": 4, "name": "Ganesh Chaturthi (Vinayaka Chavithi)", "tag": "major", "icon": "🐘", "desc": "Grand 10-day celebration of Lord Ganesha, remover of all obstacles.", "remedies": "Install Ganesha idol; offer 21 Durva blades, red flowers, and Modaks."},
    {"month_lunar": 6, "paksha": "Shukla", "tithi_in_paksha": 5, "name": "Rishi Panchami", "tag": "vrat", "icon": "📜", "desc": "Sacred veneration of Sapta Rishis for purification from mistakes.", "remedies": "Pray to ancient Rishis for spiritual clarity."},
    {"month_lunar": 6, "paksha": "Shukla", "tithi_in_paksha": 8, "name": "Radha Ashtami", "tag": "vrat", "icon": "🌸", "desc": "Divine advent of Shri Radharani at noon.", "remedies": "Midday worship of Radha-Krishna with fragrant flowers."},
    {"month_lunar": 6, "paksha": "Shukla", "tithi_in_paksha": 11, "name": "Parsva Ekadashi (Parivartini Ekadashi)", "tag": "ekadashi", "icon": "🌿", "desc": "Lord Vishnu shifts posture during cosmic sleep; powerful fast.", "remedies": "Fast and light ghee lamps for Vishnu."},
    {"month_lunar": 6, "paksha": "Shukla", "tithi_in_paksha": 14, "name": "Anant Chaturdashi (Ganesh Visarjan)", "tag": "major", "icon": "🔱", "desc": "Culmination of Ganeshotsav and sacred 14-knot Ananta ritual.", "remedies": "Tie sacred Anant thread and perform Ganesha visarjan with chanting."},
    {"month_lunar": 6, "paksha": "Shukla", "tithi_in_paksha": 15, "name": "Bhadrapada Purnima / Pitru Paksha Shraddha Begins", "tag": "purnima", "icon": "🌕", "desc": "Commencement of the solemn fortnight dedicated to ancestors (Pitrus).", "remedies": "Perform Tarpan and feed cows, crows, and seekers."},
    {"month_lunar": 6, "paksha": "Krishna", "tithi_in_paksha": 11, "name": "Indira Ekadashi", "tag": "ekadashi", "icon": "🌿", "desc": "Ekadashi dedicated to ancestral liberation and family lineage peace.", "remedies": "Offer Ekadashi fast merit for the peace of ancestors."},
    {"month_lunar": 6, "paksha": "Krishna", "tithi_in_paksha": 15, "name": "Sarva Pitru Amavasya (Mahalaya Amavasya)", "tag": "major", "icon": "🌑", "desc": "Grand culmination of Pitru Paksha; all ancestors are venerated.", "remedies": "Perform Shraddha with black sesame, kheer, and water for all departed souls."},
    {"month_lunar": 7, "paksha": "Shukla", "tithi_in_paksha": 1, "name": "Sharad Navratri Begins (Ghatasthapana)", "tag": "major", "icon": "🪔", "desc": "Nine sacred nights invoking Divine Mother Durga.", "remedies": "Perform Kalash Sthapana; light Akhand Jyoti; recite Argala Stotram."},
    {"month_lunar": 7, "paksha": "Shukla", "tithi_in_paksha": 8, "name": "Maha Ashtami (Durga Ashtami)", "tag": "major", "icon": "⚔️", "desc": "Worship of Maa Mahagauri and grand Sandhi Puja celebration.", "remedies": "Perform Kanya Pujan (worship of 9 girls) and offer Puri-Chana-Halwa."},
    {"month_lunar": 7, "paksha": "Shukla", "tithi_in_paksha": 9, "name": "Maha Navami / Ayudha Puja", "tag": "major", "icon": "🌸", "desc": "Worship of Maa Siddhidatri, tools of craft, books, and vehicles.", "remedies": "Blessing of work tools, vehicles, and books with turmeric & flowers."},
    {"month_lunar": 7, "paksha": "Shukla", "tithi_in_paksha": 10, "name": "Dussehra (Vijayadashami)", "tag": "major", "icon": "🏹", "desc": "Triumph of Lord Rama over Ravana and Maa Durga over Mahishasura.", "remedies": "Exchange auspicious Shami leaves and initiate new studies or ventures."},
    {"month_lunar": 7, "paksha": "Shukla", "tithi_in_paksha": 11, "name": "Papankusha Ekadashi", "tag": "ekadashi", "icon": "🌿", "desc": "Ekadashi fast freeing the mind from attachment and remorse.", "remedies": "Fast with meditation and prayer to Lord Padmanabha."},
    {"month_lunar": 7, "paksha": "Shukla", "tithi_in_paksha": 15, "name": "Sharad Purnima (Kojagiri Lakshmi Puja)", "tag": "major", "icon": "🌕", "desc": "Night of divine nectar showers and arrival of Goddess Lakshmi.", "remedies": "Place sweet rice kheer under moonlight; worship Lakshmi at midnight."},
    {"month_lunar": 7, "paksha": "Krishna", "tithi_in_paksha": 4, "name": "Karwa Chauth (Sankashti Vrat)", "tag": "major", "icon": "🌙", "desc": "Sacred fast by married women for partner longevity and health.", "remedies": "Observe Nirjala fast until moonrise; offer Arghya to Chandra Dev."},
    {"month_lunar": 7, "paksha": "Krishna", "tithi_in_paksha": 8, "name": "Ahoi Ashtami", "tag": "vrat", "icon": "⭐", "desc": "Maternal fast for children happiness, health, and longevity.", "remedies": "Worship Ahoi Mata in evening after sighting evening stars."},
    {"month_lunar": 7, "paksha": "Krishna", "tithi_in_paksha": 11, "name": "Rama Ekadashi", "tag": "ekadashi", "icon": "🌿", "desc": "Pre-Diwali Ekadashi fast dedicated to Lord Vishnu and Devi Lakshmi.", "remedies": "Recite Vishnu Sahasranama and light evening lamps."},
    {"month_lunar": 7, "paksha": "Krishna", "tithi_in_paksha": 13, "name": "Dhanteras (Dhanvantari Jayanti)", "tag": "major", "icon": "🪙", "desc": "Advent of Lord Dhanvantari (God of Ayurveda) & wealth invocation.", "remedies": "Buy copper/silver/brass items; light 13 Yamadeepam diyas outside home."},
    {"month_lunar": 7, "paksha": "Krishna", "tithi_in_paksha": 14, "name": "Naraka Chaturdashi (Kali Chaudas / Choti Diwali)", "tag": "major", "icon": "🪔", "desc": "Elimination of Narakasura and cleansing of bodily impurities.", "remedies": "Pre-dawn Abhyanga Snan (oil bath) with sesame paste; light 14 lamps."},
    {"month_lunar": 7, "paksha": "Krishna", "tithi_in_paksha": 15, "name": "Diwali (Maha Lakshmi Puja)", "tag": "major", "icon": "✨", "desc": "Grand Festival of Lights! Invocation of Goddess Lakshmi, Ganesha & Kuber.", "remedies": "Perform Lakshmi Puja in Pradosh/Sthir Lagna; illuminate entire home with clay lamps."},
    {"month_lunar": 8, "paksha": "Shukla", "tithi_in_paksha": 1, "name": "Govardhan Puja / Annakut / Gujarati New Year", "tag": "major", "icon": "🌄", "desc": "Lifting of Govardhan Hill by Lord Krishna & culinary gratitude feast.", "remedies": "Prepare Annakut (56 delicacies); perform Gau Puja (cow worship)."},
    {"month_lunar": 8, "paksha": "Shukla", "tithi_in_paksha": 2, "name": "Bhai Dooj (Yama Dwitiya)", "tag": "major", "icon": "👫", "desc": "Sacred sibling festival celebrating love, protection, and longevity.", "remedies": "Sisters apply vermilion tilak to brothers; mutual gifts and feast."},
    {"month_lunar": 8, "paksha": "Shukla", "tithi_in_paksha": 6, "name": "Chhath Puja (Surya Shashthi)", "tag": "major", "icon": "☀️", "desc": "Auspicious sun-worship festival in running waters for health and vitality.", "remedies": "Offer Sandhya and Usha Arghya to Surya Dev with Thekua prasad."},
    {"month_lunar": 8, "paksha": "Shukla", "tithi_in_paksha": 8, "name": "Gopashtami", "tag": "vrat", "icon": "🐄", "desc": "Veneration of cows and calves nurtured by Lord Krishna.", "remedies": "Feed green grass, jaggery, and rotis to mother cows."},
    {"month_lunar": 8, "paksha": "Shukla", "tithi_in_paksha": 11, "name": "Devutthana Ekadashi (Tulsi Vivah Begins)", "tag": "major", "icon": "🌿", "desc": "Lord Vishnu awakens from Yogic slumber; holy wedding season opens.", "remedies": "Perform wedding of sacred Tulsi plant with Shaligram/Vishnu."},
    {"month_lunar": 8, "paksha": "Shukla", "tithi_in_paksha": 15, "name": "Dev Deepawali (Kartik Purnima)", "tag": "major", "icon": "🪔", "desc": "Festival of lights celebrated by the Gods in Kashi (Varanasi).", "remedies": "Light lamps near water bodies/temples; recite Shiva Mahimna Stotra."},
    {"month_lunar": 8, "paksha": "Krishna", "tithi_in_paksha": 11, "name": "Utpanna Ekadashi", "tag": "ekadashi", "icon": "🌿", "desc": "Manifestation of Goddess Ekadashi for protection of righteous devotees.", "remedies": "Fast dedicated to Lord Narayana."},
    {"month_lunar": 9, "paksha": "Shukla", "tithi_in_paksha": 11, "name": "Gita Jayanti (Mokshada Ekadashi)", "tag": "major", "icon": "📖", "desc": "Deliverance of the holy Srimad Bhagavad Gita by Lord Krishna on Kurukshetra.", "remedies": "Recite Gita chapters, donate copies of Bhagavad Gita, Vishnu Puja."},
    {"month_lunar": 9, "paksha": "Shukla", "tithi_in_paksha": 15, "name": "Dattatreya Jayanti (Margashirsha Purnima)", "tag": "major", "icon": "🕉️", "desc": "Birth of Lord Dattatreya, supreme synthesis of Brahma, Vishnu & Shiva.", "remedies": "Chant Datta Bavani and meditate on the universal Guru."},
    {"month_lunar": 9, "paksha": "Krishna", "tithi_in_paksha": 11, "name": "Saphala Ekadashi", "tag": "ekadashi", "icon": "🌿", "desc": "Ekadashi turning earnest spiritual efforts into fruitful reality.", "remedies": "Fast with prayer to Lord Achyuta."},
    {"month_lunar": 10, "paksha": "Shukla", "tithi_in_paksha": 11, "name": "Pausha Putrada Ekadashi", "tag": "ekadashi", "icon": "🌿", "desc": "Ekadashi fast for progeny protection and prosperity.", "remedies": "Offer fragrant flowers and white sweets to Lord Vishnu."},
    {"month_lunar": 10, "paksha": "Shukla", "tithi_in_paksha": 15, "name": "Pausha Purnima (Shakambhari Purnima)", "tag": "purnima", "icon": "🌕", "desc": "Start of Magha holy snan month; devotion to Mother Nature Shakambhari.", "remedies": "Donate vegetables, grains, and warm blankets to the poor."},
    {"month_lunar": 10, "paksha": "Krishna", "tithi_in_paksha": 11, "name": "Shattila Ekadashi", "tag": "ekadashi", "icon": "🌿", "desc": "Ekadashi utilizing sacred sesame in 6 sanctifying rituals.", "remedies": "Sesame bath, sesame donation, sesame havan, and sesame food."},
    {"month_lunar": 11, "paksha": "Shukla", "tithi_in_paksha": 5, "name": "Vasant Panchami (Saraswati Puja)", "tag": "major", "icon": "🌸", "desc": "Advent of Spring and veneration of Goddess Saraswati, patron of wisdom.", "remedies": "Wear yellow attire; worship books, musical instruments, and Saraswati with yellow flowers."},
    {"month_lunar": 11, "paksha": "Shukla", "tithi_in_paksha": 7, "name": "Ratha Saptami (Surya Jayanti)", "tag": "major", "icon": "☀️", "desc": "Birth of Sun God turning his cosmic chariot towards North-East.", "remedies": "Morning bath with 7 Ark leaves on head; offer milk boiled in clay pot to Surya."},
    {"month_lunar": 11, "paksha": "Shukla", "tithi_in_paksha": 11, "name": "Jaya Ekadashi", "tag": "ekadashi", "icon": "🌿", "desc": "Ekadashi granting victory over inner doubts and spiritual hurdles.", "remedies": "Observe fast dedicated to Lord Madhava."},
    {"month_lunar": 11, "paksha": "Shukla", "tithi_in_paksha": 15, "name": "Magha Purnima (Maha Maghi Snan)", "tag": "purnima", "icon": "🌕", "desc": "Culmination of month-long Magha snan; divine bathing in holy rivers.", "remedies": "Holy river bath, donation of food and clothes to spiritual seekers."},
    {"month_lunar": 11, "paksha": "Krishna", "tithi_in_paksha": 11, "name": "Vijaya Ekadashi", "tag": "ekadashi", "icon": "🌿", "desc": "Ekadashi observed by Lord Rama prior to crossing the ocean to Lanka.", "remedies": "Fast for overcoming major undertakings and trials."},
    {"month_lunar": 11, "paksha": "Krishna", "tithi_in_paksha": 14, "name": "Maha Shivaratri", "tag": "major", "icon": "🔱", "desc": "The Great Night of Shiva! Grand wedding of Shiva-Parvati & Jyotirlinga manifestation.", "remedies": "Night-long Shiva Abhishek with Belpatra, milk, gangajal, honey; chant Om Namah Shivaya."},
    {"month_lunar": 12, "paksha": "Shukla", "tithi_in_paksha": 11, "name": "Amalaki Ekadashi", "tag": "ekadashi", "icon": "🍈", "desc": "Sacred Ekadashi worshipping the life-giving Amla tree and Lord Vishnu.", "remedies": "Offer water and incense to Amla tree; distribute Amla prasad."},
    {"month_lunar": 12, "paksha": "Shukla", "tithi_in_paksha": 14, "name": "Holika Dahan (Choti Holi)", "tag": "major", "icon": "🔥", "desc": "Victory of devotee Prahlada over Holika; burning of negativity in sacred fire.", "remedies": "Circumambulate Holika bonfire; offer green wheat earheads, coconut, and sweets."},
    {"month_lunar": 12, "paksha": "Shukla", "tithi_in_paksha": 15, "name": "Holi (Rangwali Holi / Dhulivandan)", "tag": "major", "icon": "🎨", "desc": "Grand Festival of Colors celebrating spring, divine love, and harmonious union.", "remedies": "Apply natural herbal gulal, embrace loved ones, seek forgiveness and start anew."},
    {"month_lunar": 12, "paksha": "Krishna", "tithi_in_paksha": 11, "name": "Papmochani Ekadashi", "tag": "ekadashi", "icon": "🌿", "desc": "Final Ekadashi of the Vedic year clearing all past remorse and negativity.", "remedies": "Fast dedicated to Lord Vishnu in preparation for Vedic New Year."},
]


def _get_lunar_day_details(dt: datetime) -> Dict[str, Any]:
    """Calculate comprehensive Vedic lunar state for a given date."""
    swe.set_sid_mode(swe.SIDM_LAHIRI)
    flags = swe.FLG_SWIEPH | swe.FLG_SIDEREAL

    jd = swe.julday(dt.year, dt.month, dt.day, 6.0)
    sun_lon = swe.calc_ut(jd, swe.SUN, flags)[0][0] % 360.0
    moon_lon = swe.calc_ut(jd, swe.MOON, flags)[0][0] % 360.0

    diff = (moon_lon - sun_lon) % 360.0
    tithi_idx = int(diff / 12.0)  # 0 to 29
    paksha = "Shukla" if tithi_idx < 15 else "Krishna"
    tithi_in_paksha = (tithi_idx % 15) + 1  # 1 to 15

    nak_idx = int(moon_lon / (360.0 / 27.0)) % 27
    nakshatra = NAKSHATRA_NAMES[nak_idx]
    tithi_name = TITHI_NAMES[tithi_idx]

    # Calculate Chandramana Amanta Lunar Month (Masa)
    days_back = diff / 12.190749
    jd_nm = jd - days_back
    for _ in range(3):
        s = swe.calc_ut(jd_nm, swe.SUN, flags)[0][0] % 360.0
        m = swe.calc_ut(jd_nm, swe.MOON, flags)[0][0] % 360.0
        d = (m - s) % 360.0
        if d > 180.0:
            d -= 360.0
        jd_nm -= d / 12.190749

    s_nm = swe.calc_ut(jd_nm, swe.SUN, flags)[0][0] % 360.0
    nm_sign = int(s_nm / 30.0) % 12
    month_lunar = ((nm_sign + 1) % 12) + 1
    month_name = MONTH_NAMES[month_lunar]

    return {
        "jd": jd,
        "sun_lon": sun_lon,
        "moon_lon": moon_lon,
        "tithi_idx": tithi_idx,
        "paksha": paksha,
        "tithi_in_paksha": tithi_in_paksha,
        "tithi_name": tithi_name,
        "nakshatra": nakshatra,
        "month_lunar": month_lunar,
        "month_name": month_name,
    }


def get_day_festivals(dt: datetime) -> List[Dict[str, Any]]:
    """Retrieve all astronomical festivals and observances for a single specific calendar date."""
    swe.set_sid_mode(swe.SIDM_LAHIRI)
    flags = swe.FLG_SWIEPH | swe.FLG_SIDEREAL

    details = _get_lunar_day_details(dt)
    month_lunar = details["month_lunar"]
    month_name = details["month_name"]
    paksha = details["paksha"]
    tithi_in_paksha = details["tithi_in_paksha"]
    tithi_name = details["tithi_name"]
    nakshatra = details["nakshatra"]
    sun_lon = details["sun_lon"]
    jd = details["jd"]

    results: List[Dict[str, Any]] = []

    # 1. Check Solar Ingress (Makar Sankranti)
    if 269.0 <= sun_lon <= 272.0:
        jd_prev = jd - 1.0
        s_prev = swe.calc_ut(jd_prev, swe.SUN, flags)[0][0] % 360.0
        if s_prev < 270.0 <= sun_lon:
            results.append({
                "name": "Makar Sankranti / Pongal / Uttarayana",
                "tag": "major",
                "icon": "☀️",
                "desc": "Sun enters Makara (Capricorn) marking the start of auspicious Uttarayana.",
                "remedies": "Holy bath, offer Arghya to Sun God, donate til-gul and warm clothes.",
            })

    # 2. Match Annual Festivals
    for fest in ANNUAL_FESTIVALS:
        if (
            fest["month_lunar"] == month_lunar
            and fest["paksha"] == paksha
            and fest["tithi_in_paksha"] == tithi_in_paksha
        ):
            results.append(fest)

    # 3. Monthly Recurring Vrats (Only if no major annual festival is assigned)
    if not results:
        if paksha == "Shukla" and tithi_in_paksha == 4:
            results.append({
                "name": "Vinayaka Chaturthi",
                "tag": "vrat",
                "icon": "🐘",
                "desc": "Monthly auspicious day for Lord Ganesha worship.",
                "remedies": "Offer Modak and Durva grass to Lord Ganesha.",
            })
        elif paksha == "Krishna" and tithi_in_paksha == 4:
            results.append({
                "name": "Sankashti Chaturthi",
                "tag": "vrat",
                "icon": "🌙",
                "desc": "Monthly fast for Lord Ganesha for removal of distress.",
                "remedies": "Fast until Moonrise; worship Ganesha with modak.",
            })
        elif tithi_in_paksha == 13:
            results.append({
                "name": f"{paksha} Pradosh Vrat",
                "tag": "vrat",
                "icon": "🔱",
                "desc": "Sacred twilight worship of Lord Shiva and Maa Parvati.",
                "remedies": "Perform evening Shiva Puja during Pradosh Kaal.",
            })
        elif paksha == "Shukla" and tithi_in_paksha == 15:
            results.append({
                "name": f"{month_name} Purnima / Satyanarayan Vrat",
                "tag": "purnima",
                "icon": "🌕",
                "desc": "Auspicious full moon day for Sri Satyanarayan Katha and charity.",
                "remedies": "Perform Satyanarayan Puja and donate food.",
            })
        elif paksha == "Krishna" and tithi_in_paksha == 15:
            results.append({
                "name": f"{month_name} Amavasya (Darsha Amavasya)",
                "tag": "amavasya",
                "icon": "🌑",
                "desc": "Auspicious new moon day for meditation and ancestor Tarpan.",
                "remedies": "Offer water and black sesame to ancestors; feed birds and cows.",
            })

    formatted: List[Dict[str, Any]] = []
    for r in results:
        formatted.append({
            "name": r["name"],
            "date": dt.strftime("%d %b %Y"),
            "iso_date": dt.strftime("%Y-%m-%d"),
            "desc": r["desc"],
            "description": r["desc"],
            "tithi": f"{paksha} {tithi_name}",
            "paksha": paksha,
            "nakshatra": nakshatra,
            "tag": r.get("tag", "festival"),
            "icon": r.get("icon", "🎉"),
            "remedies": r.get("remedies", ""),
            "month": month_name,
            "is_today": False,
        })

    return formatted


def get_today_festivals() -> List[Dict[str, Any]]:
    """Retrieve all festivals falling on today's date."""
    today = datetime.now()
    festivals = get_day_festivals(today)

    for f in festivals:
        f["date"] = today.strftime("%Y-%m-%d")
        f["is_today"] = True

    if not festivals:
        details = _get_lunar_day_details(today)
        festivals.append({
            "name": f"{details['paksha']} {details['tithi_name']} Nitya Puja",
            "date": today.strftime("%Y-%m-%d"),
            "desc": f"Auspicious day for personal meditation and mantra japa under {details['nakshatra']} Nakshatra.",
            "description": f"Auspicious day for personal meditation and mantra japa under {details['nakshatra']} Nakshatra.",
            "tithi": f"{details['paksha']} {details['tithi_name']}",
            "paksha": details["paksha"],
            "nakshatra": details["nakshatra"],
            "tag": "vrat",
            "icon": "🕉️",
            "remedies": "Chant Gayatri mantra or perform personal Ishta Devata worship.",
            "month": details["month_name"],
            "is_today": True,
        })

    return festivals


def get_upcoming_festivals(limit: int = 14) -> List[Dict[str, Any]]:
    """Calculate upcoming festivals for the next 60 days with clean deduplication."""
    upcoming: List[Dict[str, Any]] = []
    base_date = datetime.now()
    seen_festival_names = set()

    for day_offset in range(1, 65):
        dt = base_date + timedelta(days=day_offset)
        day_events = get_day_festivals(dt)

        for fest in day_events:
            key = (fest["name"], fest["month"])
            if key not in seen_festival_names:
                seen_festival_names.add(key)
                upcoming.append(fest)
                if len(upcoming) >= limit:
                    return upcoming

    return upcoming
