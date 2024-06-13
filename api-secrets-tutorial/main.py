from pyscript import fetch

response = await fetch(
    "https://examples.pyscriptapps.com/secrets/api/proxies/list-secrets",
    method="GET"
).json()


print(response)


