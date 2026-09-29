import urllib.parse
import re
import pandas as pd

def extract_features_from_url(url: str) -> pd.DataFrame:
    """
    Dada una URL cruda, extrae las métricas léxicas y estructurales
    necesarias para igualar el formato de las 22 variables del dataset original.
    
    NOTA: Esta función base contiene los cálculos más comunes. 
    Se debe validar comparando los nombres y tipos de columnas resultantes 
    con las columnas de X_train del dataset.
    """
    parsed = urllib.parse.urlparse(url)
    
    url_length = len(url)
    domain_length = len(parsed.netloc)
    is_ip = 1 if re.match(r'^[0-9]+(?:\.[0-9]+){3}$', parsed.netloc) else 0
    is_https = 1 if parsed.scheme == 'https' else 0
    
    digits = sum(c.isdigit() for c in url)
    digit_ratio = digits / url_length if url_length > 0 else 0
    
    special_chars = sum(not c.isalnum() for c in url)
    special_char_count = special_chars
    
    # Este diccionario DEBE expandirse y ajustarse a los nombres exactos 
    # de las columnas que usa el modelo entrenado.
    features = {
        'url_length': [url_length],
        'domain_length': [domain_length],
        'is_ip': [is_ip],
        'is_https': [is_https],
        'digit_ratio': [digit_ratio],
        'special_char_count': [special_char_count]
    }
    
    return pd.DataFrame(features)

if __name__ == "__main__":
    # Prueba local
    test_url = "http://secure-update-banco.com/login?id=82349"
    print("URL de prueba:", test_url)
    print("Características extraídas:")
    print(extract_features_from_url(test_url).T)
