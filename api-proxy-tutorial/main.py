from pyscript import fetch

response = await fetch(
    "https://examples.pyscriptapps.com/api-proxy-tutorial/api/proxies/status-check", 
    method="GET"
).json()

print(response)
