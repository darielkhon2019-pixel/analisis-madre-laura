import os
import requests
from pathlib import Path
import time

# Configuración
COOKIE = os.environ.get("COOKIE_MADRE_LAURA")
if not COOKIE:
    raise Exception("No se encontró la cookie. Configúrala en los Secrets de GitHub.")

GRUPOS_MAP = {
    "601": 666, "602": 667, "603": 668,
    "701": 669, "702": 670, "703": 671,
    "801": 673, "802": 674, "803": 675,
    "901": 676, "902": 677, "903": 678,
    "1001": 679, "1002": 680,
    "1101": 681, "1102": 682
}

# Períodos a descargar (1 al 4)
PERIODOS = [1, 2, 3, 4]

HEADERS = {
    "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8",
    "accept-language": "es-419,es;q=0.9,en;q=0.8",
    "cookie": COOKIE,
    "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/134.0.0.0 Safari/537.36"
}

def descargar():
    base_dir = Path("data/raw")
    base_dir.mkdir(parents=True, exist_ok=True)
    
    session = requests.Session()
    session.headers.update(HEADERS)
    
    for grupo, idg in GRUPOS_MAP.items():
        for periodo in PERIODOS:
            url = f"https://madre-laura.edu.co/sges/index.php?reporte=1&idg={idg}&grupo={grupo}&per={periodo}"
            filename = base_dir / f"Notas_grupo_{grupo}_per{periodo}.xlsx"
            
            # YA NO HAY 'if filename.exists(): continue' — Siempre descargamos
            print(f"📥 Descargando/Actualizando: {grupo} - P{periodo}...")
            try:
                res = session.get(url, timeout=30)
                
                # Verificar si es un Excel válido (empieza con PK)
                if res.status_code == 200 and res.content[:2] == b'PK':
                    with open(filename, "wb") as f:
                        f.write(res.content)
                    print(f"✅ Guardado/Actualizado: {filename.name}")
                else:
                    print(f"⚠️ No es un Excel válido (posiblemente sin notas o cookie expirada). Status: {res.status_code}")
            except Exception as e:
                print(f"❌ Error en {grupo} P{periodo}: {e}")
            
            # Pequeña pausa para no saturar el servidor del colegio
            time.sleep(1)

if __name__ == "__main__":
    descargar()
