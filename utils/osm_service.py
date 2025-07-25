import requests
from Levenshtein import ratio
from apps.general.models import CachedLocation
from utils.address_normalizer import AddressNormalizer

class OSMService:
    NOMINATIM_URL = "https://nominatim.openstreetmap.org/search"
    OSRM_URL = "http://router.project-osrm.org/route/v1/driving"    
    
    
    def geocode(self, query):
        # Normalizar dirección primero
        normalized_query = AddressNormalizer.normalize(query)
        #print(f"Normalized address: {normalized_query}")  # Para depuración
        
        # Buscar en caché usando la versión normalizada
        cached = self._get_cached_location(normalized_query)
        if cached:
            return cached

        # Llamar a Nominatim con la dirección NORMALIZADA
        params = {
            'q': normalized_query,
            'format': 'json',
            'limit': 1,
            'addressdetails': 1,
            'countrycodes': 'us'
        }
        headers = {'User-Agent': 'MiamiDistanceApp/1.0'}

        try:
            response = requests.get(self.NOMINATIM_URL, params=params, headers=headers)
            if response.status_code == 200 and response.json():
                data = response.json()[0]
                result = {
                    'latitude': float(data['lat']),
                    'longitude': float(data['lon']),
                    'display_name': data['display_name']
                }
                self._save_to_cache(query, result)
                return result
        except Exception as e:
            print(f"Geocoding error: {e}")
        return None

    def calculate_distance(self, origin, destination, route_type='driving'):
        MIN_DISTANCE_THRESHOLD = 0.01  # 0.01 millas (~16 metros)
        
        origin_coords = self.geocode(origin)
        dest_coords = self.geocode(destination)

        if not origin_coords or not dest_coords:
            return None

        # Verificar si son la misma ubicación (o muy cercanas)
        if self._are_coordinates_equal(origin_coords, dest_coords):
            return 0.0

        # Construir URL para OSRM
        coords_str = f"{origin_coords['longitude']},{origin_coords['latitude']};{dest_coords['longitude']},{dest_coords['latitude']}"
        url = f"{self.OSRM_URL}/{coords_str}?overview=false"

        try:
            response = requests.get(url, timeout=10)
            response.raise_for_status()
            data = response.json()
            
            if data.get('routes'):
                distance_meters = data['routes'][0]['distance']
                distance_miles = distance_meters * 0.000621371
                
                # Validar distancia mínima
                if distance_miles < MIN_DISTANCE_THRESHOLD:
                    return 0.0
                    
                return round(distance_miles, 2)
                
            # Si no hay rutas pero las coordenadas son diferentes
            # Calcular distancia haversine como fallback
            return self._haversine_distance(origin_coords, dest_coords)
            
        except Exception as e:
            print(f"Routing error: {e}")
            # Fallback a cálculo de distancia directa
            return self._haversine_distance(origin_coords, dest_coords)

    def _are_coordinates_equal(self, coords1, coords2, threshold=0.0001):
        """Compara si dos conjuntos de coordenadas son casi iguales"""
        lat_diff = abs(float(coords1['latitude']) - float(coords2['latitude']))
        lon_diff = abs(float(coords1['longitude']) - float(coords2['longitude']))
        return lat_diff < threshold and lon_diff < threshold

    def _haversine_distance(self, coords1, coords2):
        """Calcula distancia en millas entre dos coordenadas (fórmula haversine)"""
        from math import radians, sin, cos, sqrt, atan2
        
        # Radio de la Tierra en millas
        R = 3958.8
        
        lat1 = radians(float(coords1['latitude']))
        lon1 = radians(float(coords1['longitude']))
        lat2 = radians(float(coords2['latitude']))
        lon2 = radians(float(coords2['longitude']))
        
        dlon = lon2 - lon1
        dlat = lat2 - lat1
        
        a = sin(dlat / 2)**2 + cos(lat1) * cos(lat2) * sin(dlon / 2)**2
        c = 2 * atan2(sqrt(a), sqrt(1 - a))
        
        distance = R * c
        return round(distance, 2)
    
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