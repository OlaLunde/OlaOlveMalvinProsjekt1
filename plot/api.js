const URL = "https://rasmusweb.no/spm.php"
const spmID = "forEU"

async function getRequest() {
    const htmlObj = document.getElementById("get")
    htmlObj.innerHTML = "Waiting for response"

    const apiCallPromise = await fetch(URL + "?id=" + spmID, {
        method: "GET",
        headers: {
            Accept: "application/json",
        },
    })

    htmlObj.innerHTML = ""
    appendPElm(htmlObj, "StatusCodeOK: " + apiCallPromise.ok)

    // Getting the json entries from the response:
    const entries = await apiCallPromise.json()
    console.log(entries)

    for (const entry of entries) {
        console.log(entry)
        appendPElm(htmlObj, "Entry: " + JSON.stringify(entry))
    }
}

// Poster et svar til php backend
async function postRequest(svar) {
    const htmlObj = document.getElementById("post")
    htmlObj.innerHTML = "Waiting for response"

    postBody = {}
    postBody.id = spmID
    postBody.svar = svar

    const apiCallPromise = await fetch(URL, {
        method: "POST",
        headers: {
            Accept: "application/json",
        },
        body: JSON.stringify(postBody),
    })

    htmlObj.innerHTML = ""
    appendPElm(htmlObj, "StatusCodeOK: " + apiCallPromise.ok)

    // Getting the json from the response:
    const responseJson = await apiCallPromise.json()
    console.log(responseJson)

    appendPElm(htmlObj, "Response: " + responseJson)
}

function appendPElm(htmlObj, text) {
    const p = document.createElement("p")
    p.textContent = text
    htmlObj.appendChild(p)
}
