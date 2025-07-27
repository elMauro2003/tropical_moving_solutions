
from utils.osm_service import OSMService
service = OSMService()

# Normalización
normalized = service.normalizer.normalize("123-125 n main st, miami fl 33144")
# Resultado: "123 North Main Street, Miami, FL 33144"

# Cálculo de distancia
distance = service.calculate_distance(
    "7175 SW 8th St, Miami, FL 33144",
    "5798 SW 28th St, Miami, FL 33155"
)