import requests
import json
from web3.auto import w3
from eth_account.messages import encode_defunct

def get_raw_message():
    """
    Function to get message to sign from axie
    """
    # An exemple of a requestBody needed
    request_body = {"operationName":"CreateRandomMessage","variables":{},"query":"mutation CreateRandomMessage {\n  createRandomMessage\n}\n"}
    # Send the request
    r = requests.post('https://axieinfinity.com/graphql-server-v2/graphql', headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2228.0 Safari/537.36',}, data=request_body)
    # Load the data into json format
    json_data = json.loads(r.text)
    # Return the message to sign
    return json_data['data']['createRandomMessage']

def get_sign_message(raw_message, account_private_key):
    """
    Function to sign the message got from getRawMessage function
    """
    # Load the private key from the DataBase in Hex
    private_key = bytearray.fromhex(account_private_key)
    message = encode_defunct(text=raw_message)
    # Sign the message with the private key
    hex_signature = w3.eth.account.sign_message(message, private_key=private_key)
    # Return the signature
    return hex_signature

def submit_signature(signed_message, message, account_address):
    """
    Function to submit the signature and get authorization
    """
    # An example of a requestBody needed
    request_body = {"operationName":"CreateAccessTokenWithSignature","variables":{"input":{"mainnet":"ethereum","owner":"User's Eth Wallet Address","message":"User's Raw Message","signature":"User's Signed Message"}},"query":"mutation CreateAccessTokenWithSignature($input: SignatureInput!) {\n  createAccessTokenWithSignature(input: $input) {\n    newAccount\n    result\n    accessToken\n    __typename\n  }\n}\n"}
    # Remplace in that example to the actual signed message
    request_body['variables']['input']['signature'] = signed_message['signature'].hex()
    # Remplace in that example to the actual raw message
    request_body['variables']['input']['message'] = message
    # Remplace in that example to the actual account address
    request_body['variables']['input']['owner'] = account_address
    # Send the request
    r = requests.post('https://axieinfinity.com/graphql-server-v2/graphql', headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2228.0 Safari/537.36',}, json=request_body)
    # Load the data into json format
    json_data = json.loads(r.text)
    # Return the accessToken value$
    print(json_data)
    return json_data['data']['createAccessTokenWithSignature']['accessToken']
    return
