# address_normalizer.py
import re
from typing import Dict, Optional

class AddressNormalizer:
    """Normaliza direcciones de EE.UU. a formato compatible con OSM"""
    
    DIRECTIONAL_MAP = {
        'n': 'North', 'n.': 'North', 'north': 'North',
        's': 'South', 's.': 'South', 'south': 'South',
        'e': 'East', 'e.': 'East', 'east': 'East',
        'w': 'West', 'w.': 'West', 'west': 'West',
        'ne': 'Northeast', 'n.e.': 'Northeast', 'northeast': 'Northeast',
        'nw': 'Northwest', 'n.w.': 'Northwest', 'northwest': 'Northwest',
        'se': 'Southeast', 's.e.': 'Southeast', 'southeast': 'Southeast',
        'sw': 'Southwest', 's.w.': 'Southwest', 'southwest': 'Southwest'
    }
    
    STREET_TYPES = {
        'ave': 'Avenue', 'av': 'Avenue', 'avenue': 'Avenue', 'av.': 'Avenue',
        'st': 'Street', 'street': 'Street', 'st.': 'Street',
        'dr': 'Drive', 'drive': 'Drive', 'dr.': 'Drive',
        'blvd': 'Boulevard', 'boulevard': 'Boulevard', 'blvd.': 'Boulevard',
        'rd': 'Road', 'road': 'Road', 'rd.': 'Road',
        'ln': 'Lane', 'lane': 'Lane', 'ln.': 'Lane',
        'pl': 'Place', 'place': 'Place', 'pl.': 'Place',
        'trl': 'Trail', 'trail': 'Trail', 'trl.': 'Trail',
        'hw': 'Highway', 'highway': 'Highway', 'hwy': 'Highway', 'hwy.': 'Highway'
    }

    STATE_MAP = {
        state.lower(): abbr for abbr, state in {
            'AL': 'Alabama',
            'AK': 'Alaska',
            'AZ': 'Arizona',
            'AR': 'Arkansas',
            'CA': 'California',
            'CO': 'Colorado',
            'CT': 'Connecticut',
            'DE': 'Delaware',
            'FL': 'Florida',
            'GA': 'Georgia',
            'HI': 'Hawaii',
            'ID': 'Idaho',
            'IL': 'Illinois',
            'IN': 'Indiana',
            'IA': 'Iowa',
            'KS': 'Kansas',
            'KY': 'Kentucky',
            'LA': 'Louisiana',
            'ME': 'Maine',
            'MD': 'Maryland',
            'MA': 'Massachusetts',
            'MI': 'Michigan',
            'MN': 'Minnesota',
            'MS': 'Mississippi',
            'MO': 'Missouri',
            'MT': 'Montana',
            'NE': 'Nebraska',
            'NV': 'Nevada',
            'NH': 'New Hampshire',
            'NJ': 'New Jersey',
            'NM': 'New Mexico',
            'NY': 'New York',
            'NC': 'North Carolina',
            'ND': 'North Dakota',
            'OH': 'Ohio',
            'OK': 'Oklahoma',
            'OR': 'Oregon',
            'PA': 'Pennsylvania',
            'RI': 'Rhode Island',
            'SC': 'South Carolina',
            'SD': 'South Dakota',
            'TN': 'Tennessee',
            'TX': 'Texas',
            'UT': 'Utah',
            'VT': 'Vermont',
            'VA': 'Virginia',
            'WA': 'Washington',
            'WV': 'West Virginia',
            'WI': 'Wisconsin',
            'WY': 'Wyoming',
            # Territorios y áreas especiales
            'DC': 'District of Columbia',
            'PR': 'Puerto Rico',
            'GU': 'Guam',
            'VI': 'Virgin Islands',
            'AS': 'American Samoa',
            'MP': 'Northern Mariana Islands'
        }.items()
    }

    @classmethod
    def normalize(cls, address: str) -> str:
        """Normaliza una dirección a formato OSM compatible"""
        if not address:
            return address

        # Paso 1: Limpieza básica
        normalized = ' '.join(address.lower().strip().split())
        
        # Paso 2: Extraer y normalizar componentes
        normalized = cls._normalize_components(normalized)
        
        # Paso 3: Formateo final
        normalized = normalized.title()
        normalized = re.sub(r'\s+', ' ', normalized).strip()
        
        return normalized

    @classmethod
    def _normalize_components(cls, address: str) -> str:
        """Normaliza cada componente de la dirección"""
        # Normalizar rangos (123-125 Main St -> 123 Main St)
        address = cls._normalize_ranges(address)
        
        # Normalizar números ordinales (1st -> 1)
        address = cls._normalize_ordinals(address)
        
        # Normalizar direcciones direccionales (n -> North)
        address = cls._normalize_directions(address)
        
        # Normalizar tipos de calle (ave -> Avenue)
        address = cls._normalize_street_types(address)
        
        # Normalizar estados (california -> CA)
        address = cls._normalize_states(address)
        
        # Normalizar códigos postales
        address = cls._normalize_zip_codes(address)
        
        return address

    @classmethod
    def _normalize_ranges(cls, address: str) -> str:
        """Normaliza rangos de direcciones (123-125 Main St -> 123 Main St)"""
        return re.sub(
            r'(\d+)\s*-\s*(\d+)\s+([a-zA-Z]+(?:\s+[a-zA-Z]+)*)',
            lambda m: f"{m.group(1)} {m.group(3)}",
            address
        )

    @classmethod
    def _normalize_ordinals(cls, address: str) -> str:
        """Normaliza números ordinales (1st -> 1)"""
        return re.sub(r'(\d+)(?:st|nd|rd|th)\b', r'\1', address)

    @classmethod
    def _normalize_directions(cls, address: str) -> str:
        """Normaliza direcciones cardinales"""
        for abbr, full in cls.DIRECTIONAL_MAP.items():
            address = re.sub(
                rf'(^|\s){abbr}(\s|$|\W)',
                lambda m: f"{m.group(1)}{full.lower()}{m.group(2)}",
                address
            )
        return address

    @classmethod
    def _normalize_street_types(cls, address: str) -> str:
        """Normaliza tipos de calle"""
        for abbr, full in cls.STREET_TYPES.items():
            address = re.sub(
                rf'\b{abbr}\b',
                full.lower(),
                address
            )
        return address

    @classmethod
    def _normalize_states(cls, address: str) -> str:
        """Normaliza nombres de estados"""
        for state, abbr in cls.STATE_MAP.items():
            address = re.sub(
                rf'\b{state}\b',
                abbr,
                address
            )
        return address

    @classmethod
    def _normalize_zip_codes(cls, address: str) -> str:
        """Asegura formato correcto de códigos postales"""
        # Busca ZIP+4 (12345-6789) o ZIP básico (12345)
        if not re.search(r'\b\d{5}(?:-\d{4})?\b', address):
            # Si no encuentra ZIP, intenta extraerlo
            zip_match = re.search(r'\b(\d{5})\b', address)
            if zip_match:
                address = f"{address} {zip_match.group(1)}"
        return address