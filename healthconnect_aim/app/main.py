import os
from web3 import Web3, EthereumTesterProvider
from eth_account.messages import encode_defunct

from pyhypercycle_aim import SimpleQueue, JSONResponseCORS, aim_uri

PORT = os.environ.get('PORT', 4000)

storage = dict()

class ValidDoctorAim(SimpleQueue):
    manifest = {
        "name": "A doctor validation service",
        "short_name": "aim_greeting",
        "version": "0.1.0",
        "license": "Open",
        "terms-of-service": "https://hypercycle.ai/tos",
        "author": "Hypercycle"
    }
    def __init__(self):
       pass

    @aim_uri(
        uri="/register_doctor",
        methods=["POST"],
        endpoint_manifest={
            "input_query": "",
            "input_headers": {},
            "input_body": {"inputs": "<Text>"},
            "output": "<JSON>",
            "documentation": "",
            "currency": "HYPC",
            "price_per_call": {"estimated_cost": 0, "min": 0, "max": 0.1},
            "price_per_mb": {"estimated_cost": 0, "min": 0, "max": 0.1},
            "example_calls": [{
                "body": "",
                "method": "POST",
                "query": "",
                "headers": "",
                "output": {"text": "Hello World!"}
            }]

    })
    async def register(self, request):
        costs = []
        costs.append({"estimated_cost": 1, "min": 1, "max": 1,
                      "currency": "StorageUnits"})
        if request.headers.get("cost_only"):
            return JSONResponseCORS({"costs": costs})
        license = request.query_params.get("license", "")
        pubkey = request.query_params.get("public_key", "")

        storage[pubkey] = license
        return JSONResponseCORS({"status": "ok"},
                                headers={"used": "1", "currency": "ProcessingUnits"})
    @aim_uri(
        uri="/check_doctor",
        methods=["GET"],
        endpoint_manifest={
            "input_query": "",
            "input_headers": {},
            "input_body": {"inputs": "<Text>"},
            "output": "<JSON>",
            "documentation": "",
            "currency": "HYPC",
            "price_per_call": {"estimated_cost": 0, "min": 0, "max": 0.1},
            "price_per_mb": {"estimated_cost": 0, "min": 0, "max": 0.1},
            "example_calls": [{
                "body": "",
                "method": "POST",
                "query": "",
                "headers": "",
                "output": {"text": "Hello World!"}
            }]

    })
    async def check_doctor(self, request):
        costs = []
        costs.append({"estimated_cost": 1, "min": 1, "max": 1,
                      "currency": "BandwidthUnits"})
        if request.headers.get("cost_only"):
            return JSONResponseCORS({"costs": costs})
        pubkey = request.query_params.get("public_key", "")
        license = request.query_params.get("license", "")
        message = request.query_params.get("message", "")
        signature = request.query_params.get("signature", "")
        #look at: https://web3py.readthedocs.io/en/stable/web3.eth.account.html

        encmessage = encode_defunct(text=message)
        w3.eth.account.recover_message(encmessage, signature=ed_message.signature)

        data = storage.get(pubkey, "")
        if data == license:
            return_val = {"status": "valid"}
        else:
            return_val = {"status": "invalid"}

        return JSONResponseCORS(return_val,
                                headers={"used": "1", "currency": "BandwidthUnits"})




def main():
  app = ValidDoctorAim()
  app.run(uvicorn_kwargs={"port": PORT, "host": "0.0.0.0"})

if __name__ == "__main__":
    main()
