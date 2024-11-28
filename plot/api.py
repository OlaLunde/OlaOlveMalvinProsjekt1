import requests as req

URL = "https://rasmusweb.no/spm.php"
GameID = "mastermind"

def getResults():
    resultat = req.get(URL + "?id=" + GameID)  # , requestOptions)
    print(f"Statuskode: {resultat.status_code}")
    data = resultat.json()
    print(data)

def postResult(result):
    data = {"id": GameID , "svar": result}
    resultat = req.post(URL, json=data)
    print(f"Statuskode: {resultat.status_code}")
    print(resultat.json())


postResult()
getResults()
