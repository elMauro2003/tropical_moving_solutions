import requests
from Levenshtein import ratio
from apps.general.models import CachedLocation

class OSMService:
    NOMINATIM_URL = "https://nominatim.openstreetmap.org/search"
    OSRM_URL = "http://router.project-osrm.org/route/v1/driving"

    def geocode(self, query):
        # Verificar caché primero
        cached = self._get_cached_location(query)
        if cached:
            return cached

        # Llamar a Nominatim
        params = {
            'q': query,
            'format': 'json',
            'limit': 1,
            'addressdetails': 1,
            'countrycodes': 'us'  # Filtro para EE.UU.
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
        origin_coords = self.geocode(origin)
        dest_coords = self.geocode(destination)

        if not origin_coords or not dest_coords:
            return None

        # Construir URL para OSRM
        coords_str = f"{origin_coords['longitude']},{origin_coords['latitude']};{dest_coords['longitude']},{dest_coords['latitude']}"
        url = f"{self.OSRM_URL}/{coords_str}?overview=false"

        try:
            response = requests.get(url)
            if response.status_code == 200:
                data = response.json()
                if data.get('routes'):
                    distance_meters = data['routes'][0]['distance']
                    distance_miles = distance_meters * 0.000621371  # Conversión a millas
                    return round(distance_miles, 2)
        except Exception as e:
            print(f"Routing error: {e}")
        return None

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