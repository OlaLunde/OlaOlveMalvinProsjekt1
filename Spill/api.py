import requests as req

URL = "https://rasmusweb.no/spm.php"
GameID = "mastermind4"

def getResults():
    resultat = req.get(URL + "?id=" + GameID)  # , requestOptions)
    data = resultat.json()
    return data

def postResult(result):
    data = {"id": GameID , "svar": result}
    resultat = req.post(URL, json=data)
    return resultat
<<<<<<< HEAD
=======


# Testing:
postResult()
