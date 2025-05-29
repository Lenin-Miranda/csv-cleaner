def parse_address(text):
    import re

    sufijos_calle = r"(?:ST|AVE|BLVD|RD|DR|CT|LN|WAY|PL|TRL|PKWY|HWY|CIR|TER|LOOP|ALY|PLZ|WALK|ROW|SQ|BND|XING|PKY|MNR|PASS|RTE|PIKE|EXT|EXPY|FWY|STE)"
    unidades_solo = r"APT|STE|UNIT|FL|BLDG|RM|DEPT|SUITE|SPC|#"
    unidades = rf"(?:{unidades_solo})\s*[A-Z0-9]+|[A-Z0-9]+\s*(?:{unidades_solo})"


    # Normalizar
    texto = re.sub(r'\s+', ' ', text.strip().upper())
    texto = re.sub(rf"({sufijos_calle})\s+({unidades_solo})", r"\1 \2", texto)

    # Regexes
    patron_po_box = re.compile(
        r"^(PO BOX \d+)[,\s]+([A-Z\s]+?)[,\s]+([A-Z]{2})[,\s]+(\d{5}(?:-\d{4})?)$"
    )

    patron_direccion = re.compile(
    rf"^(\d+\s+(?:[A-Z0-9]+\s+)*{sufijos_calle}(?:\s+(?:N|S|E|W|NE|NW|SE|SW))?(?:\s+{unidades})?)\s+([A-Z]+(?:\s+[A-Z]+)*)\s+([A-Z]{{2}})\s+(\d{{5}}(?:-\d{{4}})?)$"

    )

    match_po = patron_po_box.match(texto)
    if match_po:
        return list(match_po.groups())

    match_dir = patron_direccion.match(texto)
    if match_dir:
        direccion, ciudad, estado, zip_code = match_dir.groups()
        
        # 🛠️ Post-procesamiento: si ciudad empieza con una letra suelta, pásala a la dirección
        ciudad_partes = ciudad.strip().split()
        if len(ciudad_partes) > 1 and len(ciudad_partes[0]) == 1:
            direccion += f" {ciudad_partes[0]}"
            ciudad = " ".join(ciudad_partes[1:])

        return [direccion, ciudad, estado, zip_code]

    print("No match found for:", texto)
    return ["", "", "", ""]
