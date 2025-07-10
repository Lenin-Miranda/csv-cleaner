import re

def parse_address(text):
    sufijos_calle = r"(?:ST|AVE|BLVD|RD|DR|CT|LN|WAY|PL|TRL|PKWY|HWY|CIR|TER|LOOP|ALY|PLZ|WALK|ROW|SQ|BND|XING|PKY|MNR|PASS|RTE|PIKE|EXT|EXPY|FWY|STE)"
    unidades_solo = r"APT|STE|UNIT|FL|BLDG|RM|DEPT|SUITE|SPC|LOT#"
    unidades = rf"(?:{unidades_solo})\s*[A-Z0-9\-]+|[A-Z0-9\-]+\s*(?:{unidades_solo})"
    cardinales = r"(?:N|S|E|W|NE|NW|SE|SW|South|West|East|North|)"
    
    texto = re.sub(r'\s+', ' ', text.strip().upper())
    texto = re.sub(rf"({sufijos_calle})\s+({unidades_solo})", r"\1 \2", texto)

    patron_po_box = re.compile(
        r"^(PO BOX \d+)[,\s]+([A-Za-z\s]+),?\s+([A-Za-z]{2})\s+(\d{5,9}(?:-\d{4})?)$"
    )
    patron_direccion = re.compile(
        rf"^(.*?)"  # Dirección flexible
        rf"[, ]+([A-Za-z\s\.'-]+?)"  # Ciudad (no greedy)
        rf"[, ]+([A-Za-z]{{2}})"  # Estado (exactamente dos letras)
        rf"[, ]+(\d{{5,9}}(?:-?\d{{4}})?)"  # Código postal
        rf"(?:[, ]+([A-Za-z\s]+))?"  # País opcional
        rf"$"
    )
    patron_dir_zip = re.compile(
        rf"^(.*?)[, ]+(\d{{5,9}}(?:-?\d{{4}})?)$"  # Dirección y código postal
    )

    match_po = patron_po_box.match(texto)
    if match_po:
        return list(match_po.groups())

    match_dir = patron_direccion.match(texto)
    if not match_dir:
        match_dir_zip = patron_dir_zip.match(texto)
        if match_dir_zip:
            direccion, zip_code = match_dir_zip.groups()
            # Intentar separar ciudad conocida de la dirección
            ciudades_conocidas = [
                "PHOENIX", "SCOTTSDALE", "TUCSON", "PARADISE VALLEY", "LITCHFIELD PK", "GLENDALE", "CAVE CREEK", "SEATTLE", "CHANDLER", "MESA", "TEMPE", "GILBERT", "PEORIA", "SUN CITY", "AVONDALE", "GOODYEAR", "SURPRISE", "BUCKEYE", "YUMA", "FLAGSTAFF", "PRESCOTT", "SIERRA VISTA", "KINGMAN", "BULLHEAD CITY", "LAKE HAVASU CITY", "SHOW LOW", "PAYSON", "EL MIRAGE", "SAFFORD", "DOUGLAS", "ELOY", "COTTONWOOD", "GLOBE", "SAN LUIS", "SAHUARITA", "ORO VALLEY", "MARICOPA", "QUEEN CREEK", "FOUNTAIN HILLS", "LAVEEN", "SUN LAKES", "GOODYEAR", "SURPRISE", "CHINO VALLEY", "YOUNGTOWN", "TOLLESON", "WICKENBURG", "LAVEEN", "APACHE JUNCTION"
            ]
            ciudad = ""
            direccion_limpia = direccion.strip()
            for c in ciudades_conocidas:
                if direccion_limpia.endswith(" " + c):
                    direccion = direccion_limpia[:-(len(c)+1)].strip()
                    ciudad = c
                    break
            return [direccion, ciudad, "", zip_code]
        return ["", "", "", ""]

    direccion, ciudad, estado, zip_code, pais = match_dir.groups()

    # Si el país es USA, lo eliminamos de la dirección y del zip
    if pais and pais.strip().upper() == "USA":
        direccion = direccion.strip()
        if zip_code:
            zip_code = zip_code.strip()
    elif pais:
        direccion = f"{direccion.strip()} {pais.strip()}"

    # Corrección para ciudades compuestas mal separadas
    ciudad_partes = ciudad.strip().split()
    direccion_partes = direccion.strip().split()

    palabras_ciudad_comunes = {"RIO", "SUN", "CAMP", "PHOENIX", "SCOTTSDALE", "LITCHFIELD", "SUNCITY", "WEST", "VERDE"}

    if len(ciudad_partes) == 1 and direccion_partes and direccion_partes[-1] in palabras_ciudad_comunes:
        ciudad = direccion_partes[-1] + " " + ciudad
        direccion = " ".join(direccion_partes[:-1])

    return [direccion, ciudad, estado if estado else "", zip_code if zip_code else ""]
