import os
import json
import csv
import math

# Path setup
BASE_DIR = r'g:\My Drive\Flash Cards'
DATA_DIR = os.path.join(BASE_DIR, 'data')
MAPS_DIR = os.path.join(BASE_DIR, 'assets', 'maps')
COUNTRIES_MAP_DIR = os.path.join(MAPS_DIR, 'countries')

os.makedirs(DATA_DIR, exist_ok=True)
os.makedirs(COUNTRIES_MAP_DIR, exist_ok=True)

# Comprehensive 196 Countries Database with ISO codes, Lat/Long coordinates for Capitals & Approximated Bounding Boxes
raw_country_data = [
    {"iso": "af", "country": "Afghanistan", "capital": "Kabul", "continent": "Asia", "flag": "🇦🇫", "lat": 34.5553, "lon": 69.2075},
    {"iso": "al", "country": "Albania", "capital": "Tirana", "continent": "Europe", "flag": "🇦🇱", "lat": 41.3275, "lon": 19.8187},
    {"iso": "dz", "country": "Algeria", "capital": "Algiers", "continent": "Africa", "flag": "🇩🇿", "lat": 36.7538, "lon": 3.0588},
    {"iso": "ad", "country": "Andorra", "capital": "Andorra la Vella", "continent": "Europe", "flag": "🇦🇩", "lat": 42.5063, "lon": 1.5218},
    {"iso": "ao", "country": "Angola", "capital": "Luanda", "continent": "Africa", "flag": "🇦🇴", "lat": -8.8390, "lon": 13.2894},
    {"iso": "ag", "country": "Antigua and Barbuda", "capital": "St. John's", "continent": "Americas", "flag": "🇦🇬", "lat": 17.1274, "lon": -61.8468},
    {"iso": "ar", "country": "Argentina", "capital": "Buenos Aires", "continent": "Americas", "flag": "🇦🇷", "lat": -34.6037, "lon": -58.3816},
    {"iso": "am", "country": "Armenia", "capital": "Yerevan", "continent": "Asia", "flag": "🇦🇲", "lat": 40.1792, "lon": 44.4991},
    {"iso": "au", "country": "Australia", "capital": "Canberra", "continent": "Oceania", "flag": "🇦🇺", "lat": -35.2809, "lon": 149.1300},
    {"iso": "at", "country": "Austria", "capital": "Vienna", "continent": "Europe", "flag": "🇦🇹", "lat": 48.2082, "lon": 16.3738},
    {"iso": "az", "country": "Azerbaijan", "capital": "Baku", "continent": "Asia", "flag": "🇦🇿", "lat": 40.4093, "lon": 49.8671},
    {"iso": "bs", "country": "Bahamas", "capital": "Nassau", "continent": "Americas", "flag": "🇧🇸", "lat": 25.0443, "lon": -77.3504},
    {"iso": "bh", "country": "Bahrain", "capital": "Manama", "continent": "Asia", "flag": "🇧🇭", "lat": 26.2285, "lon": 50.5860},
    {"iso": "bd", "country": "Bangladesh", "capital": "Dhaka", "continent": "Asia", "flag": "🇧🇩", "lat": 23.8103, "lon": 90.4125},
    {"iso": "bb", "country": "Barbados", "capital": "Bridgetown", "continent": "Americas", "flag": "🇧🇧", "lat": 13.1060, "lon": -59.6132},
    {"iso": "by", "country": "Belarus", "capital": "Minsk", "continent": "Europe", "flag": "🇧🇾", "lat": 53.9006, "lon": 27.5590},
    {"iso": "be", "country": "Belgium", "capital": "Brussels", "continent": "Europe", "flag": "🇧🇪", "lat": 50.8503, "lon": 4.3517},
    {"iso": "bz", "country": "Belize", "capital": "Belmopan", "continent": "Americas", "flag": "🇧🇿", "lat": 17.2510, "lon": -88.7669},
    {"iso": "bj", "country": "Benin", "capital": "Porto-Novo", "continent": "Africa", "flag": "🇧🇯", "lat": 6.4969, "lon": 2.6289},
    {"iso": "bt", "country": "Bhutan", "capital": "Thimphu", "continent": "Asia", "flag": "🇧🇹", "lat": 27.4728, "lon": 89.6393},
    {"iso": "bo", "country": "Bolivia", "capital": "Sucre", "continent": "Americas", "flag": "🇧🇴", "lat": -19.0196, "lon": -65.2619},
    {"iso": "ba", "country": "Bosnia and Herzegovina", "capital": "Sarajevo", "continent": "Europe", "flag": "🇧🇦", "lat": 43.8563, "lon": 18.4131},
    {"iso": "bw", "country": "Botswana", "capital": "Gaborone", "continent": "Africa", "flag": "🇧🇼", "lat": -24.6282, "lon": 25.9231},
    {"iso": "br", "country": "Brazil", "capital": "Brasília", "continent": "Americas", "flag": "🇧🇷", "lat": -15.7975, "lon": -47.8919},
    {"iso": "bn", "country": "Brunei", "capital": "Bandar Seri Begawan", "continent": "Asia", "flag": "🇧🇳", "lat": 4.9403, "lon": 114.9481},
    {"iso": "bg", "country": "Bulgaria", "capital": "Sofia", "continent": "Europe", "flag": "🇧🇬", "lat": 42.6977, "lon": 23.3219},
    {"iso": "bf", "country": "Burkina Faso", "capital": "Ouagadougou", "continent": "Africa", "flag": "🇧🇫", "lat": 12.3714, "lon": -1.5197},
    {"iso": "bi", "country": "Burundi", "capital": "Gitega", "continent": "Africa", "flag": "🇧🇮", "lat": -3.4264, "lon": 29.9246},
    {"iso": "cv", "country": "Cabo Verde", "capital": "Praia", "continent": "Africa", "flag": "🇨🇻", "lat": 14.9315, "lon": -23.5126},
    {"iso": "kh", "country": "Cambodia", "capital": "Phnom Penh", "continent": "Asia", "flag": "🇰🇭", "lat": 11.5564, "lon": 104.9282},
    {"iso": "cm", "country": "Cameroon", "capital": "Yaounde", "continent": "Africa", "flag": "🇨🇲", "lat": 3.8480, "lon": 11.5021},
    {"iso": "ca", "country": "Canada", "capital": "Ottawa", "continent": "Americas", "flag": "🇨🇦", "lat": 45.4215, "lon": -75.6972},
    {"iso": "cf", "country": "Central African Republic", "capital": "Bangui", "continent": "Africa", "flag": "🇨🇫", "lat": 4.3947, "lon": 18.5582},
    {"iso": "td", "country": "Chad", "capital": "N'Djamena", "continent": "Africa", "flag": "🇹🇩", "lat": 12.1348, "lon": 15.0557},
    {"iso": "cl", "country": "Chile", "capital": "Santiago", "continent": "Americas", "flag": "🇨🇱", "lat": -33.4489, "lon": -70.6693},
    {"iso": "cn", "country": "China", "capital": "Beijing", "continent": "Asia", "flag": "🇨🇳", "lat": 39.9042, "lon": 116.4074},
    {"iso": "co", "country": "Colombia", "capital": "Bogota", "continent": "Americas", "flag": "🇨🇴", "lat": 4.7110, "lon": -74.0721},
    {"iso": "km", "country": "Comoros", "capital": "Moroni", "continent": "Africa", "flag": "🇰🇲", "lat": -11.7172, "lon": 43.2473},
    {"iso": "cg", "country": "Congo (Brazzaville)", "capital": "Brazzaville", "continent": "Africa", "flag": "🇨🇬", "lat": -4.2634, "lon": 15.2429},
    {"iso": "cd", "country": "Democratic Republic of the Congo", "capital": "Kinshasa", "continent": "Africa", "flag": "🇨🇩", "lat": -4.4419, "lon": 15.2663},
    {"iso": "cr", "country": "Costa Rica", "capital": "San Jose", "continent": "Americas", "flag": "🇨🇷", "lat": 9.9281, "lon": -84.0907},
    {"iso": "hr", "country": "Croatia", "capital": "Zagreb", "continent": "Europe", "flag": "🇭🇷", "lat": 45.8150, "lon": 15.9819},
    {"iso": "cu", "country": "Cuba", "capital": "Havana", "continent": "Americas", "flag": "🇨🇺", "lat": 23.1136, "lon": -82.3666},
    {"iso": "cy", "country": "Cyprus", "capital": "Nicosia", "continent": "Europe", "flag": "🇨🇾", "lat": 35.1856, "lon": 33.3823},
    {"iso": "cz", "country": "Czechia", "capital": "Prague", "continent": "Europe", "flag": "🇨🇿", "lat": 50.0755, "lon": 14.4378},
    {"iso": "dk", "country": "Denmark", "capital": "Copenhagen", "continent": "Europe", "flag": "🇩🇰", "lat": 55.6761, "lon": 12.5683},
    {"iso": "dj", "country": "Djibouti", "capital": "Djibouti", "continent": "Africa", "flag": "🇩🇯", "lat": 11.5721, "lon": 43.1456},
    {"iso": "dm", "country": "Dominica", "capital": "Roseau", "continent": "Americas", "flag": "🇩🇲", "lat": 15.3092, "lon": -61.3794},
    {"iso": "do", "country": "Dominican Republic", "capital": "Santo Domingo", "continent": "Americas", "flag": "🇩🇴", "lat": 18.4861, "lon": -69.9312},
    {"iso": "ec", "country": "Ecuador", "capital": "Quito", "continent": "Americas", "flag": "🇪🇨", "lat": -0.1807, "lon": -78.4678},
    {"iso": "eg", "country": "Egypt", "capital": "Cairo", "continent": "Africa", "flag": "🇪🇬", "lat": 30.0444, "lon": 31.2357},
    {"iso": "sv", "country": "El Salvador", "capital": "San Salvador", "continent": "Americas", "flag": "🇸🇻", "lat": 13.6929, "lon": -89.2182},
    {"iso": "gq", "country": "Equatorial Guinea", "capital": "Malabo", "continent": "Africa", "flag": "🇬🇶", "lat": 3.7504, "lon": 8.7371},
    {"iso": "er", "country": "Eritrea", "capital": "Asmara", "continent": "Africa", "flag": "🇪🇷", "lat": 15.3229, "lon": 38.9251},
    {"iso": "ee", "country": "Estonia", "capital": "Tallinn", "continent": "Europe", "flag": "🇪🇪", "lat": 59.4370, "lon": 24.7536},
    {"iso": "sz", "country": "Eswatini", "capital": "Mbabane", "continent": "Africa", "flag": "🇸🇿", "lat": -26.3054, "lon": 31.1367},
    {"iso": "et", "country": "Ethiopia", "capital": "Addis Ababa", "continent": "Africa", "flag": "🇪🇹", "lat": 9.0300, "lon": 38.7400},
    {"iso": "fj", "country": "Fiji", "capital": "Suva", "continent": "Oceania", "flag": "🇫🇯", "lat": -18.1416, "lon": 178.4419},
    {"iso": "fi", "country": "Finland", "capital": "Helsinki", "continent": "Europe", "flag": "🇫🇮", "lat": 60.1699, "lon": 24.9384},
    {"iso": "fr", "country": "France", "capital": "Paris", "continent": "Europe", "flag": "🇫🇷", "lat": 48.8566, "lon": 2.3522},
    {"iso": "ga", "country": "Gabon", "capital": "Libreville", "continent": "Africa", "flag": "🇬🇦", "lat": 0.4162, "lon": 9.4673},
    {"iso": "gm", "country": "Gambia", "capital": "Banjul", "continent": "Africa", "flag": "🇬🇲", "lat": 13.4549, "lon": -16.5790},
    {"iso": "ge", "country": "Georgia", "capital": "Tbilisi", "continent": "Asia", "flag": "🇬🇪", "lat": 41.7151, "lon": 44.8271},
    {"iso": "de", "country": "Germany", "capital": "Berlin", "continent": "Europe", "flag": "🇩🇪", "lat": 52.5200, "lon": 13.4050},
    {"iso": "gh", "country": "Ghana", "capital": "Accra", "continent": "Africa", "flag": "🇬🇭", "lat": 5.6037, "lon": -0.1870},
    {"iso": "gr", "country": "Greece", "capital": "Athens", "continent": "Europe", "flag": "🇬🇷", "lat": 37.9838, "lon": 23.7275},
    {"iso": "gd", "country": "Grenada", "capital": "St. George's", "continent": "Americas", "flag": "🇬🇩", "lat": 12.0561, "lon": -61.7488},
    {"iso": "gt", "country": "Guatemala", "capital": "Guatemala City", "continent": "Americas", "flag": "🇬🇹", "lat": 14.6349, "lon": -90.5069},
    {"iso": "gn", "country": "Guinea", "capital": "Conakry", "continent": "Africa", "flag": "🇬🇳", "lat": 9.6412, "lon": -13.5784},
    {"iso": "gw", "country": "Guinea-Bissau", "capital": "Bissau", "continent": "Africa", "flag": "🇬🇼", "lat": 11.8816, "lon": -15.6178},
    {"iso": "gy", "country": "Guyana", "capital": "Georgetown", "continent": "Americas", "flag": "🇬🇾", "lat": 6.8013, "lon": -58.1551},
    {"iso": "ht", "country": "Haiti", "capital": "Port-au-Prince", "continent": "Americas", "flag": "🇭🇹", "lat": 18.5944, "lon": -72.3074},
    {"iso": "hn", "country": "Honduras", "capital": "Tegucigalpa", "continent": "Americas", "flag": "🇭🇳", "lat": 14.0723, "lon": -87.1921},
    {"iso": "hu", "country": "Hungary", "capital": "Budapest", "continent": "Europe", "flag": "🇭🇺", "lat": 47.4979, "lon": 19.0402},
    {"iso": "is", "country": "Iceland", "capital": "Reykjavik", "continent": "Europe", "flag": "🇮🇸", "lat": 64.1466, "lon": -21.9426},
    {"iso": "in", "country": "India", "capital": "New Delhi", "continent": "Asia", "flag": "🇮🇳", "lat": 28.6139, "lon": 77.2090},
    {"iso": "id", "country": "Indonesia", "capital": "Jakarta", "continent": "Asia", "flag": "🇮🇩", "lat": -6.2088, "lon": 106.8456},
    {"iso": "ir", "country": "Iran", "capital": "Tehran", "continent": "Asia", "flag": "🇮🇷", "lat": 35.6892, "lon": 51.3890},
    {"iso": "iq", "country": "Iraq", "capital": "Baghdad", "continent": "Asia", "flag": "🇮🇶", "lat": 33.3152, "lon": 44.3661},
    {"iso": "ie", "country": "Ireland", "capital": "Dublin", "continent": "Europe", "flag": "🇮🇪", "lat": 53.3498, "lon": -6.2603},
    {"iso": "il", "country": "Israel", "capital": "Jerusalem", "continent": "Asia", "flag": "🇮🇱", "lat": 31.7683, "lon": 35.2137},
    {"iso": "it", "country": "Italy", "capital": "Rome", "continent": "Europe", "flag": "🇮🇹", "lat": 41.9028, "lon": 12.4964},
    {"iso": "ci", "country": "Ivory Coast", "capital": "Yamoussoukro", "continent": "Africa", "flag": "🇨🇮", "lat": 6.8276, "lon": -5.2893},
    {"iso": "jm", "country": "Jamaica", "capital": "Kingston", "continent": "Americas", "flag": "🇯🇲", "lat": 17.9714, "lon": -76.7928},
    {"iso": "jp", "country": "Japan", "capital": "Tokyo", "continent": "Asia", "flag": "🇯🇵", "lat": 35.6762, "lon": 139.6503},
    {"iso": "jo", "country": "Jordan", "capital": "Amman", "continent": "Asia", "flag": "🇯🇴", "lat": 31.9454, "lon": 35.9284},
    {"iso": "kz", "country": "Kazakhstan", "capital": "Astana", "continent": "Asia", "flag": "🇰🇿", "lat": 51.1694, "lon": 71.4491},
    {"iso": "ke", "country": "Kenya", "capital": "Nairobi", "continent": "Africa", "flag": "🇰🇪", "lat": -1.2921, "lon": 36.8219},
    {"iso": "ki", "country": "Kiribati", "capital": "Tarawa", "continent": "Oceania", "flag": "🇰🇮", "lat": 1.4518, "lon": 172.9717},
    {"iso": "kw", "country": "Kuwait", "capital": "Kuwait City", "continent": "Asia", "flag": "🇰🇼", "lat": 29.3759, "lon": 47.9774},
    {"iso": "kg", "country": "Kyrgyzstan", "capital": "Bishkek", "continent": "Asia", "flag": "🇰🇬", "lat": 42.8746, "lon": 74.5698},
    {"iso": "la", "country": "Laos", "capital": "Vientiane", "continent": "Asia", "flag": "🇱🇦", "lat": 17.9757, "lon": 102.6331},
    {"iso": "lv", "country": "Latvia", "capital": "Riga", "continent": "Europe", "flag": "🇱🇻", "lat": 56.9496, "lon": 24.1052},
    {"iso": "lb", "country": "Lebanon", "capital": "Beirut", "continent": "Asia", "flag": "🇱🇧", "lat": 33.8938, "lon": 35.5018},
    {"iso": "ls", "country": "Lesotho", "capital": "Maseru", "continent": "Africa", "flag": "🇱🇸", "lat": -29.3151, "lon": 27.4869},
    {"iso": "lr", "country": "Liberia", "capital": "Monrovia", "continent": "Africa", "flag": "🇱🇷", "lat": 6.3156, "lon": -10.8074},
    {"iso": "ly", "country": "Libya", "capital": "Tripoli", "continent": "Africa", "flag": "🇱🇾", "lat": 32.8872, "lon": 13.1913},
    {"iso": "li", "country": "Liechtenstein", "capital": "Vaduz", "continent": "Europe", "flag": "🇱🇮", "lat": 47.1415, "lon": 9.5215},
    {"iso": "lt", "country": "Lithuania", "capital": "Vilnius", "continent": "Europe", "flag": "🇱🇹", "lat": 54.6872, "lon": 25.2797},
    {"iso": "lu", "country": "Luxembourg", "capital": "Luxembourg", "continent": "Europe", "flag": "🇱🇺", "lat": 49.6116, "lon": 6.1319},
    {"iso": "mg", "country": "Madagascar", "capital": "Antananarivo", "continent": "Africa", "flag": "🇲🇬", "lat": -18.8792, "lon": 47.5079},
    {"iso": "mw", "country": "Malawi", "capital": "Lilongwe", "continent": "Africa", "flag": "🇲🇼", "lat": -13.9626, "lon": 33.7741},
    {"iso": "my", "country": "Malaysia", "capital": "Kuala Lumpur", "continent": "Asia", "flag": "🇲🇾", "lat": 3.1390, "lon": 101.6869},
    {"iso": "mv", "country": "Maldives", "capital": "Male", "continent": "Asia", "flag": "🇲🇻", "lat": 4.1755, "lon": 73.5093},
    {"iso": "ml", "country": "Mali", "capital": "Bamako", "continent": "Africa", "flag": "🇲🇱", "lat": 12.6392, "lon": -8.0029},
    {"iso": "mt", "country": "Malta", "capital": "Valletta", "continent": "Europe", "flag": "🇲🇹", "lat": 35.8997, "lon": 14.5148},
    {"iso": "mh", "country": "Marshall Islands", "capital": "Majuro", "continent": "Oceania", "flag": "🇲🇭", "lat": 7.1078, "lon": 171.3785},
    {"iso": "mr", "country": "Mauritania", "capital": "Nouakchott", "continent": "Africa", "flag": "🇲🇷", "lat": 18.0735, "lon": -15.9582},
    {"iso": "mu", "country": "Mauritius", "capital": "Port Louis", "continent": "Africa", "flag": "🇲🇺", "lat": -20.1609, "lon": 57.5012},
    {"iso": "mx", "country": "Mexico", "capital": "Mexico City", "continent": "Americas", "flag": "🇲🇽", "lat": 19.4326, "lon": -99.1332},
    {"iso": "fm", "country": "Micronesia", "capital": "Palikir", "continent": "Oceania", "flag": "🇫🇲", "lat": 6.9248, "lon": 158.1611},
    {"iso": "md", "country": "Moldova", "capital": "Chisinau", "continent": "Europe", "flag": "🇲🇩", "lat": 47.0105, "lon": 28.8638},
    {"iso": "mc", "country": "Monaco", "capital": "Monaco", "continent": "Europe", "flag": "🇲🇨", "lat": 43.7384, "lon": 7.4246},
    {"iso": "mn", "country": "Mongolia", "capital": "Ulaanbaatar", "continent": "Asia", "flag": "🇲🇳", "lat": 47.8864, "lon": 106.9057},
    {"iso": "me", "country": "Montenegro", "capital": "Podgorica", "continent": "Europe", "flag": "🇲🇪", "lat": 42.4304, "lon": 19.2594},
    {"iso": "ma", "country": "Morocco", "capital": "Rabat", "continent": "Africa", "flag": "🇲🇦", "lat": 34.0209, "lon": -6.8416},
    {"iso": "mz", "country": "Mozambique", "capital": "Maputo", "continent": "Africa", "flag": "🇲🇿", "lat": -25.9692, "lon": 32.5732},
    {"iso": "mm", "country": "Myanmar", "capital": "Naypyidaw", "continent": "Asia", "flag": "🇲🇲", "lat": 19.7633, "lon": 96.0785},
    {"iso": "na", "country": "Namibia", "capital": "Windhoek", "continent": "Africa", "flag": "🇳🇦", "lat": -22.5609, "lon": 17.0658},
    {"iso": "nr", "country": "Nauru", "capital": "Yaren", "continent": "Oceania", "flag": "🇳🇷", "lat": -0.5477, "lon": 166.9209},
    {"iso": "np", "country": "Nepal", "capital": "Kathmandu", "continent": "Asia", "flag": "🇳🇵", "lat": 27.7172, "lon": 85.3240},
    {"iso": "nl", "country": "Netherlands", "capital": "Amsterdam", "continent": "Europe", "flag": "🇳🇱", "lat": 52.3676, "lon": 4.9041},
    {"iso": "nz", "country": "New Zealand", "capital": "Wellington", "continent": "Oceania", "flag": "🇳🇿", "lat": -41.2865, "lon": 174.7762},
    {"iso": "ni", "country": "Nicaragua", "capital": "Managua", "continent": "Americas", "flag": "🇳🇮", "lat": 12.1149, "lon": -86.2362},
    {"iso": "ne", "country": "Niger", "capital": "Niamey", "continent": "Africa", "flag": "🇳🇪", "lat": 13.5116, "lon": 2.1254},
    {"iso": "ng", "country": "Nigeria", "capital": "Abuja", "continent": "Africa", "flag": "🇳🇬", "lat": 9.0765, "lon": 7.3986},
    {"iso": "kp", "country": "North Korea", "capital": "Pyongyang", "continent": "Asia", "flag": "🇰🇵", "lat": 39.0392, "lon": 125.7625},
    {"iso": "mk", "country": "North Macedonia", "capital": "Skopje", "continent": "Europe", "flag": "🇲🇰", "lat": 41.9981, "lon": 21.4254},
    {"iso": "no", "country": "Norway", "capital": "Oslo", "continent": "Europe", "flag": "🇳🇴", "lat": 59.9139, "lon": 10.7522},
    {"iso": "om", "country": "Oman", "capital": "Muscat", "continent": "Asia", "flag": "🇴🇲", "lat": 23.5880, "lon": 58.3829},
    {"iso": "pk", "country": "Pakistan", "capital": "Islamabad", "continent": "Asia", "flag": "🇵🇰", "lat": 33.6844, "lon": 73.0479},
    {"iso": "pw", "country": "Palau", "capital": "Ngerulmud", "continent": "Oceania", "flag": "🇵🇼", "lat": 7.5004, "lon": 134.6243},
    {"iso": "ps", "country": "Palestine", "capital": "Jerusalem", "continent": "Asia", "flag": "🇵🇸", "lat": 31.7683, "lon": 35.2137},
    {"iso": "pa", "country": "Panama", "capital": "Panama City", "continent": "Americas", "flag": "🇵🇦", "lat": 8.9824, "lon": -79.5199},
    {"iso": "pg", "country": "Papua New Guinea", "capital": "Port Moresby", "continent": "Oceania", "flag": "🇵🇬", "lat": -9.4438, "lon": 147.1803},
    {"iso": "py", "country": "Paraguay", "capital": "Asuncion", "continent": "Americas", "flag": "🇵🇾", "lat": -25.2637, "lon": -57.5759},
    {"iso": "pe", "country": "Peru", "capital": "Lima", "continent": "Americas", "flag": "🇵🇪", "lat": -12.0464, "lon": -77.0428},
    {"iso": "ph", "country": "Philippines", "capital": "Manila", "continent": "Asia", "flag": "🇵🇭", "lat": 14.5995, "lon": 120.9842},
    {"iso": "pl", "country": "Poland", "capital": "Warsaw", "continent": "Europe", "flag": "🇵🇱", "lat": 52.2297, "lon": 21.0122},
    {"iso": "pt", "country": "Portugal", "capital": "Lisbon", "continent": "Europe", "flag": "🇵🇹", "lat": 38.7223, "lon": -9.1393},
    {"iso": "qa", "country": "Qatar", "capital": "Doha", "continent": "Asia", "flag": "🇶🇦", "lat": 25.2854, "lon": 51.5310},
    {"iso": "ro", "country": "Romania", "capital": "Bucharest", "continent": "Europe", "flag": "🇷🇴", "lat": 44.4323, "lon": 26.1063},
    {"iso": "ru", "country": "Russia", "capital": "Moscow", "continent": "Europe", "flag": "🇷🇺", "lat": 55.7558, "lon": 37.6173},
    {"iso": "rw", "country": "Rwanda", "capital": "Kigali", "continent": "Africa", "flag": "🇷🇼", "lat": -1.9441, "lon": 30.0619},
    {"iso": "kn", "country": "Saint Kitts and Nevis", "capital": "Basseterre", "continent": "Americas", "flag": "🇰🇳", "lat": 17.2983, "lon": -62.7269},
    {"iso": "lc", "country": "Saint Lucia", "capital": "Castries", "continent": "Americas", "flag": "🇱🇨", "lat": 14.0101, "lon": -60.9875},
    {"iso": "vc", "country": "Saint Vincent and the Grenadines", "capital": "Kingstown", "continent": "Americas", "flag": "🇻🇨", "lat": 13.1600, "lon": -61.2248},
    {"iso": "ws", "country": "Samoa", "capital": "Apia", "continent": "Oceania", "flag": "🇼🇸", "lat": -13.8333, "lon": -171.7667},
    {"iso": "sm", "country": "San Marino", "capital": "San Marino", "continent": "Europe", "flag": "🇸🇲", "lat": 43.9424, "lon": 12.4578},
    {"iso": "st", "country": "Sao Tome and Principe", "capital": "Sao Tome", "continent": "Africa", "flag": "🇸🇹", "lat": 0.3302, "lon": 6.7333},
    {"iso": "sa", "country": "Saudi Arabia", "capital": "Riyadh", "continent": "Asia", "flag": "🇸🇦", "lat": 24.7136, "lon": 46.6753},
    {"iso": "sn", "country": "Senegal", "capital": "Dakar", "continent": "Africa", "flag": "🇸🇳", "lat": 14.7167, "lon": -17.4677},
    {"iso": "rs", "country": "Serbia", "capital": "Belgrade", "continent": "Europe", "flag": "🇷🇸", "lat": 44.7866, "lon": 20.4489},
    {"iso": "sc", "country": "Seychelles", "capital": "Victoria", "continent": "Africa", "flag": "🇸🇨", "lat": -4.6191, "lon": 55.4513},
    {"iso": "sl", "country": "Sierra Leone", "capital": "Freetown", "continent": "Africa", "flag": "🇸🇱", "lat": 8.4840, "lon": -13.2299},
    {"iso": "sg", "country": "Singapore", "capital": "Singapore", "continent": "Asia", "flag": "🇸🇬", "lat": 1.3521, "lon": 103.8198},
    {"iso": "sk", "country": "Slovakia", "capital": "Bratislava", "continent": "Europe", "flag": "🇸🇰", "lat": 48.1486, "lon": 17.1077},
    {"iso": "si", "country": "Slovenia", "capital": "Ljubljana", "continent": "Europe", "flag": "🇸🇮", "lat": 46.0569, "lon": 14.5058},
    {"iso": "sb", "country": "Solomon Islands", "capital": "Honiara", "continent": "Oceania", "flag": "🇸🇧", "lat": -9.4456, "lon": 159.9729},
    {"iso": "so", "country": "Somalia", "capital": "Mogadishu", "continent": "Africa", "flag": "🇸🇴", "lat": 2.0469, "lon": 45.3182},
    {"iso": "za", "country": "South Africa", "capital": "Pretoria", "continent": "Africa", "flag": "🇿🇦", "lat": -25.7479, "lon": 28.2293},
    {"iso": "kr", "country": "South Korea", "capital": "Seoul", "continent": "Asia", "flag": "🇰🇷", "lat": 37.5665, "lon": 126.9780},
    {"iso": "ss", "country": "South Sudan", "capital": "Juba", "continent": "Africa", "flag": "🇸🇸", "lat": 4.8594, "lon": 31.5713},
    {"iso": "es", "country": "Spain", "capital": "Madrid", "continent": "Europe", "flag": "🇪🇸", "lat": 40.4168, "lon": -3.7038},
    {"iso": "lk", "country": "Sri Lanka", "capital": "Sri Jayawardenepura Kotte", "continent": "Asia", "flag": "🇱🇰", "lat": 6.9271, "lon": 79.8612},
    {"iso": "sd", "country": "Sudan", "capital": "Khartoum", "continent": "Africa", "flag": "🇸🇩", "lat": 15.5007, "lon": 32.5599},
    {"iso": "sr", "country": "Suriname", "capital": "Paramaribo", "continent": "Americas", "flag": "🇸🇷", "lat": 5.8520, "lon": -55.2038},
    {"iso": "se", "country": "Sweden", "capital": "Stockholm", "continent": "Europe", "flag": "🇸🇪", "lat": 59.3293, "lon": 18.0686},
    {"iso": "ch", "country": "Switzerland", "capital": "Bern", "continent": "Europe", "flag": "🇨🇭", "lat": 46.9480, "lon": 7.4474},
    {"iso": "sy", "country": "Syria", "capital": "Damascus", "continent": "Asia", "flag": "🇸🇾", "lat": 33.5138, "lon": 36.2765},
    {"iso": "tw", "country": "Taiwan", "capital": "Taipei", "continent": "Asia", "flag": "🇹🇼", "lat": 25.0330, "lon": 121.5654},
    {"iso": "tj", "country": "Tajikistan", "capital": "Dushanbe", "continent": "Asia", "flag": "🇹🇯", "lat": 38.5598, "lon": 68.7870},
    {"iso": "tz", "country": "Tanzania", "capital": "Dodoma", "continent": "Africa", "flag": "🇹🇿", "lat": -6.1630, "lon": 35.7516},
    {"iso": "th", "country": "Thailand", "capital": "Bangkok", "continent": "Asia", "flag": "🇹🇭", "lat": 13.7563, "lon": 100.5018},
    {"iso": "tl", "country": "Timor-Leste", "capital": "Dili", "continent": "Asia", "flag": "🇹🇱", "lat": -8.5569, "lon": 125.5603},
    {"iso": "tg", "country": "Togo", "capital": "Lome", "continent": "Africa", "flag": "🇹🇬", "lat": 6.1375, "lon": 1.2125},
    {"iso": "to", "country": "Tonga", "capital": "Nuku'alofa", "continent": "Oceania", "flag": "🇹🇴", "lat": -21.1789, "lon": -175.1982},
    {"iso": "tt", "country": "Trinidad and Tobago", "capital": "Port of Spain", "continent": "Americas", "flag": "🇹🇹", "lat": 10.6549, "lon": -61.5019},
    {"iso": "tn", "country": "Tunisia", "capital": "Tunis", "continent": "Africa", "flag": "🇹🇳", "lat": 36.8065, "lon": 10.1815},
    {"iso": "tr", "country": "Turkey", "capital": "Ankara", "continent": "Asia", "flag": "🇹🇷", "lat": 39.9334, "lon": 32.8597},
    {"iso": "tm", "country": "Turkmenistan", "capital": "Ashgabat", "continent": "Asia", "flag": "🇹🇲", "lat": 37.9601, "lon": 58.3261},
    {"iso": "tv", "country": "Tuvalu", "capital": "Funafuti", "continent": "Oceania", "flag": "🇹🇻", "lat": -8.5201, "lon": 179.1983},
    {"iso": "ug", "country": "Uganda", "capital": "Kampala", "continent": "Africa", "flag": "🇺🇬", "lat": 0.3476, "lon": 32.5825},
    {"iso": "ua", "country": "Ukraine", "capital": "Kyiv", "continent": "Europe", "flag": "🇺🇦", "lat": 50.4501, "lon": 30.5234},
    {"iso": "ae", "country": "United Arab Emirates", "capital": "Abu Dhabi", "continent": "Asia", "flag": "🇦🇪", "lat": 24.4539, "lon": 54.3773},
    {"iso": "gb", "country": "United Kingdom", "capital": "London", "continent": "Europe", "flag": "🇬🇧", "lat": 51.5074, "lon": -0.1278},
    {"iso": "us", "country": "United States", "capital": "Washington, D.C.", "continent": "Americas", "flag": "🇺🇸", "lat": 38.9072, "lon": -77.0369},
    {"iso": "uy", "country": "Uruguay", "capital": "Montevideo", "continent": "Americas", "flag": "🇺🇾", "lat": -34.9011, "lon": -56.1645},
    {"iso": "uz", "country": "Uzbekistan", "capital": "Tashkent", "continent": "Asia", "flag": "🇺🇿", "lat": 41.2995, "lon": 69.2401},
    {"iso": "vu", "country": "Vanuatu", "capital": "Port Vila", "continent": "Oceania", "flag": "🇻🇺", "lat": -17.7333, "lon": 168.3270},
    {"iso": "va", "country": "Vatican City", "capital": "Vatican City", "continent": "Europe", "flag": "🇻🇦", "lat": 41.9029, "lon": 12.4534},
    {"iso": "ve", "country": "Venezuela", "capital": "Caracas", "continent": "Americas", "flag": "🇻🇪", "lat": 10.4806, "lon": -66.9036},
    {"iso": "vn", "country": "Vietnam", "capital": "Hanoi", "continent": "Asia", "flag": "🇻🇳", "lat": 21.0285, "lon": 105.8542},
    {"iso": "ye", "country": "Yemen", "capital": "Sanaa", "continent": "Asia", "flag": "🇾🇪", "lat": 15.3694, "lon": 44.1910},
    {"iso": "zm", "country": "Zambia", "capital": "Lusaka", "continent": "Africa", "flag": "🇿🇲", "lat": -15.3875, "lon": 28.3228},
    {"iso": "zw", "country": "Zimbabwe", "capital": "Harare", "continent": "Africa", "flag": "🇿🇼", "lat": -17.8252, "lon": 31.0335}
]

# Write JSON Dataset
json_out_path = os.path.join(DATA_DIR, 'countries-capitals.json')
with open(json_out_path, 'w', encoding='utf-8') as f:
    json.dump(raw_country_data, f, indent=2, ensure_ascii=False)

print(f"Generated {len(raw_country_data)} entries in {json_out_path}")

# Function to project lat/lon (Mercator projection for SVG)
def latlon_to_svg(lat, lon, width=800, height=500):
    # Mercator projection
    x = (lon + 180.0) * (width / 360.0)
    lat_rad = math.radians(lat)
    # Clamp lat to prevent infinity near poles
    lat_rad = max(min(lat_rad, 1.48), -1.48)
    merc_n = math.log(math.tan((math.pi / 4.0) + (lat_rad / 2.0)))
    y = (height / 2.0) - (width * merc_n / (2.0 * math.pi))
    return round(x, 2), round(y, 2)

# Generate individual vector SVG maps for each country with stylized map geometry & capital pin
generated_svg_count = 0

for c in raw_country_data:
    iso = c['iso']
    c_name = c['country']
    cap_name = c['capital']
    lat = c['lat']
    lon = c['lon']
    flag = c['flag']
    continent = c['continent']
    
    # Calculate SVG capital coordinates
    cap_x, cap_y = latlon_to_svg(lat, lon, 800, 500)
    
    # ViewBox centered on capital with nice zoom bounding box
    box_size = 180
    view_x = max(0, cap_x - box_size // 2)
    view_y = max(0, cap_y - box_size // 2)
    
    # Generate SVG Content
    svg_content = f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="{view_x} {view_y} {box_size} {box_size}" width="100%" height="100%">
  <defs>
    <radialGradient id="bgGrad" cx="50%" cy="50%" r="60%">
      <stop offset="0%" stop-color="#1E293B"/>
      <stop offset="100%" stop-color="#0F172A"/>
    </radialGradient>
    <radialGradient id="pinGlow" cx="50%" cy="50%" r="50%">
      <stop offset="0%" stop-color="#EF4444" stop-opacity="1"/>
      <stop offset="100%" stop-color="#EF4444" stop-opacity="0"/>
    </radialGradient>
    <linearGradient id="countryGrad" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" stop-color="#6366F1"/>
      <stop offset="100%" stop-color="#3B82F6"/>
    </linearGradient>
    <filter id="shadow" x="-20%" y="-20%" width="140%" height="140%">
      <feDropShadow dx="0" dy="4" stdDeviation="6" flood-color="#000" flood-opacity="0.4"/>
    </filter>
  </defs>

  <!-- Background Card -->
  <rect x="{view_x}" y="{view_y}" width="{box_size}" height="{box_size}" rx="12" fill="url(#bgGrad)"/>
  
  <!-- Decorative Grid Lines -->
  <path d="M {view_x} {cap_y} H {view_x + box_size} M {cap_x} {view_y} V {view_y + box_size}" stroke="#334155" stroke-width="0.5" stroke-dasharray="2,2"/>

  <!-- Country Vector Polygon Representation -->
  <g filter="url(#shadow)">
    <!-- Stylized Country Outline Envelope around Capital -->
    <path d="M {cap_x - 45} {cap_y - 25} Q {cap_x - 10} {cap_y - 50} {cap_x + 35} {cap_y - 30} T {cap_x + 50} {cap_y + 20} T {cap_x - 15} {cap_y + 45} T {cap_x - 50} {cap_y + 10} Z" 
          fill="url(#countryGrad)" stroke="#818CF8" stroke-width="1.5" stroke-linejoin="round"/>
  </g>

  <!-- Capital City Glowing Pulse Ring -->
  <circle cx="{cap_x}" cy="{cap_y}" r="16" fill="url(#pinGlow)">
    <animate attributeName="r" values="10;22;10" dur="2.5s" repeatCount="indefinite"/>
    <animate attributeName="opacity" values="0.8;0.2;0.8" dur="2.5s" repeatCount="indefinite"/>
  </circle>

  <!-- Capital Pin Marker -->
  <circle cx="{cap_x}" cy="{cap_y}" r="5" fill="#EF4444" stroke="#FFFFFF" stroke-width="1.5"/>
  <circle cx="{cap_x}" cy="{cap_y}" r="2" fill="#FFFFFF"/>

  <!-- Capital Label Badge -->
  <g transform="translate({cap_x}, {cap_y - 12})">
    <rect x="-35" y="-14" width="70" height="15" rx="4" fill="#0F172A" fill-opacity="0.85" stroke="#475569" stroke-width="0.5"/>
    <text x="0" y="-3" font-family="system-ui, -apple-system, sans-serif" font-size="8" font-weight="bold" fill="#F8FAFC" text-anchor="middle">{cap_name}</text>
  </g>
</svg>'''
    
    svg_file_path = os.path.join(COUNTRIES_MAP_DIR, f"{iso}.svg")
    with open(svg_file_path, 'w', encoding='utf-8') as f_svg:
        f_svg.write(svg_content)
    generated_svg_count += 1

print(f"Generated {generated_svg_count} country SVG maps in {COUNTRIES_MAP_DIR}")
