import re
from typing import Dict, Optional

class AddressNormalizer:
    """Normaliza direcciones a un formato estándar para mejor reconocimiento"""
    
    # Mapeo de abreviaciones y términos comunes
    DIRECTIONAL_MAP = {
        'n': 'North', 's': 'South', 'e': 'East', 'w': 'West',
        'ne': 'Northeast', 'nw': 'Northwest',
        'se': 'Southeast', 'sw': 'Southwest'
    }
    
    STREET_TYPES = {
        'ave': 'Avenue', 'av': 'Avenue', 'avenue': 'Avenue',
        'st': 'Street', 'street': 'Street',
        'dr': 'Drive', 'drive': 'Drive',
        'blvd': 'Boulevard', 'boulevard': 'Boulevard',
        'rd': 'Road', 'road': 'Road',
        'ln': 'Lane', 'lane': 'Lane',
        'pl': 'Place', 'place': 'Place',
        'ter': 'Terrace', 'terrace': 'Terrace',
        'trl': 'Trail', 'trail': 'Trail'
    }
    
    STATE_MAP = {
        'fl': 'FL', 'florida': 'FL',
        'ca': 'CA', 'california': 'CA'
        # Agregar más estados según necesidad
    }

    @classmethod
    def normalize(cls, address: str) -> str:
        """Normaliza una dirección a formato estándar"""
        if not address:
            return address
        
        # Paso 0: Manejar rangos de direcciones (ej. 4398-4000)
        address = cls._normalize_address_ranges(address)
        
        # Paso 1: Convertir a minúsculas y quitar espacios extras
        normalized = ' '.join(address.lower().strip().split())
        
        # Paso 2: Normalizar números ordinales (1st, 2nd, 3rd, 4th, etc.)
        normalized = cls._normalize_ordinal_numbers(normalized)
        
        # Paso 3: Normalizar direcciones direccionales (N, S, E, W)
        normalized = cls._normalize_directions(normalized)
        
        # Paso 4: Normalizar tipos de calle (Ave, St, etc.)
        normalized = cls._normalize_street_types(normalized)
        
        # Paso 5: Normalizar estados
        normalized = cls._normalize_states(normalized)
        
        # Paso 6: Asegurar formato de código postal
        normalized = cls._normalize_zip_code(normalized)
        
        # Paso 7: Capitalizar palabras y limpiar
        normalized = normalized.title()
        normalized = re.sub(r'\s+', ' ', normalized).strip()
        
        # Paso 8: Asegurar país si no está presente
        # if not any(x in normalized for x in ['EE. UU.', 'USA', 'US']):
        #     normalized += ', EE. UU.'
            
        return normalized

    @classmethod
    def _normalize_address_ranges(cls, address: str) -> str:
        """Convierte rangos de direcciones a un formato manejable"""
        # Patrón para rangos como 4398-4000 o 4101-4311
        range_pattern = r'(\d+)\s*-\s*(\d+)\s+([a-zA-Z]+)'
        
        # Reemplazar con el primer número del rango
        normalized = re.sub(
            range_pattern,
            lambda m: f"{m.group(1)} {m.group(3)}",  # Toma el primer número y el nombre de la calle
            address
        )
        return normalized
    
    @classmethod
    def _normalize_ordinal_numbers(cls, address: str) -> str:
        """Convierte 66th a 66, 1st a 1, etc."""
        return re.sub(
            r'(\d+)(st|nd|rd|th)\b',
            lambda m: m.group(1),
            address
        )

    @classmethod
    def _normalize_directions(cls, address: str) -> str:
        """Normaliza direcciones cardinales"""
        for abbr, full in cls.DIRECTIONAL_MAP.items():
            address = re.sub(
                rf'\b{abbr}\b',
                full.lower(),
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
        for abbr, full in cls.STATE_MAP.items():
            address = re.sub(
                rf'\b{abbr}\b',
                full,
                address
            )
        return address

    @classmethod
    def _normalize_zip_code(cls, address: str) -> str:
        """Asegura formato de código postal (5 o 5-4 dígitos)"""
        # Busca patrones como 33024 o 33024-1234
        if not re.search(r'\b\d{5}(-\d{4})?\b', address):
            # Si no encuentra código postal, intenta extraer de la dirección
            zip_match = re.search(r'\b(\d{5})\b', address)
            if zip_match:
                address = address.replace(zip_match.group(1), f"FL {zip_match.group(1)}")
        return address