from config.Security import Security
from config.Resource import Resource 
import json
from fastapi.security import OAuth2PasswordBearer

SECRET_KEY = "d9e61be3d4cc6c9a5f6d3c2360f37ce3fdd1c0247adc0068d45be18811772a9e"
ALGORITHM = "HS256"
TOKEN_EXPIRATION_DAYS = 1

SHOW_ADMIN_ROUTES = True

with open('./config/connections.json', 'r') as archivo:
    master_data = json.load(archivo)
    securitySesion = Security(master_data["Master"], SECRET_KEY, ALGORITHM, TOKEN_EXPIRATION_DAYS)

with open('./config/connections.json', 'r') as archivo:
    master_data = json.load(archivo)
    dataSourceSesion = Resource(master_data["Master"])

authScheme = OAuth2PasswordBearer(tokenUrl="token")