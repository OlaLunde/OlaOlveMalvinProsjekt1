import requests as req

URL = "https://rasmusweb.no/spm.php"
GameID = "mastermind4"

def getResults():
    try:
        resultat = req.get(f"{URL}?id={GameID}")  # Legg til skjema og ID
        resultat.raise_for_status()  # Sjekk om forespørselen lykkes
        data = resultat.json()  # Konverter til JSON
        return data
    except Exception as e:
        print("Feil ved henting av resultater:", e)
        return []
    

def postResult(result):
    try:
        data = {"id": GameID, "svar": result}
        resultat = req.post(URL, json=data)
        resultat.raise_for_status()  # Sjekk om forespørselen lykkes
        try:
            return resultat.json()  # Hvis serveren returnerer JSON
        except ValueError:
            print("Serveren returnerte ikke gyldig JSON:", resultat.text)
            return None
    except Exception as e:
        print("Feil ved lagring av resultat:", e)
        return None



# Testing:
# postResult()
