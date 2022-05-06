import json
from pprint import pprint
import requests
from ratelimiter import RateLimiter

API_KEY = ''

eligibleAddresses = open("eligibleAddresses.txt")
eligibleAddresses = eligibleAddresses.read()
eligibleAddresses = eligibleAddresses.splitlines()

results = []
eligibleAddressesLen = len(eligibleAddresses)


def getTxData(i):
    response = requests.get("https://api.etherscan.io/api?module=account"
                            "&action=txlist"
                            f'&address={eligibleAddresses[i]}'
                            "&startblock=0"
                            "&endblock=99999999"
                            "&offset=10"
                            "&sort=asc"
                            f"&apikey={API_KEY}")

    print(f'Getting {eligibleAddresses[i]} || {i} / {eligibleAddressesLen}')
    fromsTx = []
    tosTx = []
    try:
        for result in response.json()["result"]:
            if result["from"] not in fromsTx:
                fromsTx.append(result["from"])
            if result["to"] not in tosTx:
                tosTx.append(result["to"])
        result = {
            "address": eligibleAddresses[1],
            "froms": fromsTx,
            "tos": tosTx,
            "txCount": len(response.json()["result"]),
        }
        results.append(result)
    except:
        print("error")


if __name__ == "__main__":
    rate_limiter = RateLimiter(max_calls=5, period=1)
    for i in range(eligibleAddressesLen):
        with rate_limiter:
            getTxData(i)
    with open('json_data_ethereum.json', 'w') as outfile:
        json.dump(results, outfile)
