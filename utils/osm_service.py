import requests
import re
from Levenshtein import ratio
from apps.general.models import CachedLocation
from utils.address_normalizer import AddressNormalizer
from typing import Optional, Dict
from urllib.parse import quote


class OSMService:
    """Servicio mejorado para geocodificación y cálculo de distancias con OSM"""
    
    NOMINATIM_URL = "https://nominatim.openstreetmap.org/search"
    OSRM_URL = "http://router.project-osrm.org/route/v1/driving"
    MIN_DISTANCE_THRESHOLD = 0.01  # ~16 metros
    
    def __init__(self):
        self.normalizer = AddressNormalizer()

    def geocode(self, query: str) -> Optional[Dict]:
        """Geocodifica una dirección normalizada"""
        normalized = self._prepare_query(query)
        
        # Buscar en caché primero
        cached = self._get_cached_location(normalized)
        if cached:
            return cached

        # Intentar geocodificación con OSM
        result = self._geocode_with_osm(normalized)
        if result:
            self._save_to_cache(query, result)
            return result
        
        # Fallback: intentar con componentes principales
        return self._try_fallback_geocoding(normalized)

    def calculate_distance(self, origin: str, destination: str) -> Optional[float]:
        """Calcula distancia entre dos direcciones en millas"""
        origin_coords = self.geocode(origin)
        dest_coords = self.geocode(destination)

        if not origin_coords or not dest_coords:
            return None

        # Verificar si son la misma ubicación
        if self._are_coordinates_equal(origin_coords, dest_coords):
            return 0.0

        # Calcular ruta con OSRM
        distance = self._calculate_osrm_distance(origin_coords, dest_coords)
        if distance is not None:
            return distance

        # Fallback a distancia haversine
        return self._haversine_distance(origin_coords, dest_coords)

    def _prepare_query(self, query: str) -> str:
        """Prepara la consulta para OSM"""
        normalized = self.normalizer.normalize(query)
        
        # Asegurar formato "Número Calle, Ciudad, Estado ZIP"
        parts = [p.strip() for p in normalized.split(',')]
        if len(parts) >= 3 and re.search(r'\b[A-Z]{2}\b', parts[-2]):
            # Formato: Calle, Ciudad, Estado ZIP
            street = parts[0]
            city = parts[-2]
            state_zip = parts[-1]
            return f"{street}, {city}, {state_zip}"
        
        return normalized

    def _geocode_with_osm(self, query: str) -> Optional[Dict]:
        """Geocodificación usando Nominatim"""
        params = {
            'q': query,
            'format': 'json',
            'limit': 1,
            'addressdetails': 1,
            'countrycodes': 'us',
            'dedupe': 1  # Eliminar duplicados
        }
        
        try:
            response = requests.get(
                self.NOMINATIM_URL,
                params=params,
                headers={'User-Agent': 'YourApp/1.0'},
                timeout=10
            )
            if response.status_code == 200:
                data = response.json()
                if data:
                    return {
                        'latitude': float(data[0]['lat']),
                        'longitude': float(data[0]['lon']),
                        'display_name': data[0]['display_name']
                    }
        except Exception as e:
            print(f"Geocoding error: {e}")
        return None

    def _try_fallback_geocoding(self, query: str) -> Optional[Dict]:
        """Intenta geocodificación con componentes simplificados"""
        # Intentar con solo calle y ciudad
        simplified = ','.join(query.split(',')[:2])
        if result := self._geocode_with_osm(f"{simplified}, US"):
            return result
        
        # Intentar con solo código postal
        if zip_match := re.search(r'\b\d{5}\b', query):
            if result := self._geocode_with_osm(f"{zip_match.group()}, US"):
                return result
        
        return None

    def _calculate_osrm_distance(self, origin: Dict, destination: Dict) -> Optional[float]:
        """Calcula distancia usando OSRM"""
        coords = f"{origin['longitude']},{origin['latitude']};{destination['longitude']},{destination['latitude']}"
        url = f"{self.OSRM_URL}/{coords}?overview=false"
        
        try:
            response = requests.get(url, timeout=10)
            if response.status_code == 200:
                data = response.json()
                if data.get('routes'):
                    distance_meters = data['routes'][0]['distance']
                    distance_miles = distance_meters * 0.000621371
                    return round(distance_miles, 2)
        except Exception as e:
            print(f"OSRM error: {e}")
        return None

    def _haversine_distance(self, coords1: Dict, coords2: Dict) -> float:
        """Calcula distancia haversine entre coordenadas"""
        from math import radians, sin, cos, sqrt, atan2
        
        lat1 = radians(coords1['latitude'])
        lon1 = radians(coords1['longitude'])
        lat2 = radians(coords2['latitude'])
        lon2 = radians(coords2['longitude'])
        
        dlat = lat2 - lat1
        dlon = lon2 - lon1
        
        a = sin(dlat/2)**2 + cos(lat1) * cos(lat2) * sin(dlon/2)**2
        c = 2 * atan2(sqrt(a), sqrt(1-a))
        
        return round(3958.8 * c, 2)  # Radio de la Tierra en millas

    def _are_coordinates_equal(self, coords1: Dict, coords2: Dict, threshold: float = 0.0001) -> bool:
        """Compara si dos coordenadas son casi iguales"""
        lat_diff = abs(coords1['latitude'] - coords2['latitude'])
        lon_diff = abs(coords1['longitude'] - coords2['longitude'])
        return lat_diff < threshold and lon_diff < threshold
    
    def _get_cached_location(self, query):
        # Búsqueda exacta
        exact_match = CachedLocation.objects.filter(query__iexact=query).first()
        if exact_match:
            return {
                'latitude': exact_match.latitude,
                'longitude': exact_match.longitude,
                'display_name': exact_match.display_name
            }

        # Búsqueda aproximada
        all_locations = CachedLocation.objects.all()
        best_match = None
        best_ratio = 0

        for loc in all_locations:
            current_ratio = ratio(query.lower(), loc.query.lower())
            if current_ratio > best_ratio:
                best_ratio = current_ratio
                best_match = loc

        if best_ratio > 0.7:  # Umbral de similitud
            return {
                'latitude': best_match.latitude,
                'longitude': best_match.longitude,
                'display_name': best_match.display_name
            }
        return None

    def _save_to_cache(self, query, data):
        try:
            CachedLocation.objects.create(
                query=query,
                latitude=data['latitude'],
                longitude=data['longitude'],
                display_name=data['display_name']
            )
        except Exception as e:
            print(f"Cache save error: {e}")