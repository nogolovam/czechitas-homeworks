import requests
import json

# Část 1 – IČO
def search_by_ico():
    ico = input("Zadejte IČO subjektu: ").strip()
    url = f"https://ares.gov.cz/ekonomicke-subjekty-v-be/rest/ekonomicke-subjekty/{ico}"
    res = requests.get(url)
    json_data = res.json()
    obchodni_jmeno = json_data.get("obchodniJmeno", "Neznámé jméno")
    adresa = json_data.get("sidlo", {}).get("textovaAdresa", "Neznámá adresa")
    print(f"{obchodni_jmeno}, {adresa}")

# Funkce pro nalezení názvu právní formy podle kódu
def find_legal_form(kod, polozky):
    for polozka in polozky:
        if polozka.get("kod") == kod:
            nazvy = polozka.get("nazev", [])
            for zaznam in nazvy:
                if zaznam.get("kodJazyka") == "cs":
                    return zaznam.get("nazev", "Neznámá forma")
    return "Neznámá forma"

# Načtení číselníku
def get_legal_forms():
    url = "https://ares.gov.cz/ekonomicke-subjekty-v-be/rest/ciselniky-nazevniky/vyhledat"
    headers = {
        "accept": "application/json",
        "Content-Type": "application/json",
    }
    data = '{"kodCiselniku": "PravniForma", "zdrojCiselniku": "res"}'
    res = requests.post(url, headers=headers, data=data)
    json_data = res.json()
    ciselnik = json_data.get("ciselniky", [{}])[0]
    return ciselnik.get("polozkyCiselniku", [])

# Část 2 – hledání podle názvu
def search_by_name():
    polozky_ciselniku = get_legal_forms()
    nazev = input("Zadejte název subjektu pro vyhledání: ").strip()
    url = "https://ares.gov.cz/ekonomicke-subjekty-v-be/rest/ekonomicke-subjekty/vyhledat"
    headers = {
        "accept": "application/json",
        "Content-Type": "application/json",
    }
    data = json.dumps({"obchodniJmeno": nazev})
    data = data.encode("utf-8")
    res = requests.post(url, headers=headers, data=data)
    json_data = res.json()
    subjekty = json_data.get("ekonomickeSubjekty", [])
    print(f"Nalezeno subjektů: {json_data.get('pocetCelkem', 0)}")
    for subjekt in subjekty:
        jmeno = subjekt.get("obchodniJmeno", "Neznámé jméno")
        ico = subjekt.get("ico", "Neznámé IČO")
        pravni_forma_kod = subjekt.get("pravniForma", "")
        pravni_forma_nazev = find_legal_form(pravni_forma_kod, polozky_ciselniku)
        print(f"{jmeno}, {ico}, {pravni_forma_nazev}")


print("1 – Hledání podle IČO")
print("2 – Hledání podle názvu")
volba = input("Zadejte číslo volby (1 nebo 2): ").strip()

if volba == "1":
    search_by_ico()
elif volba == "2":
    search_by_name()
else:
    print("Neplatná volba.")
