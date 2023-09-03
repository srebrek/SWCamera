import json
import time
from requests import get, post
import image_to_text_resources.azure_keys as azure_keys
from Models.Model import data_extraction as de

# Endpoint URL
endpoint = azure_keys.endpoint
apim_key = azure_keys.key1
post_url = endpoint + "/formrecognizer/v2.1/prebuilt/receipt/analyze"
source = r"image_to_text_resources/test_foto2.jpg"

headers = {
    # Request headers
    'Content-Type': 'image/jpg',
    'Ocp-Apim-Subscription-Key': apim_key,
}

params = {
    "includeTextDetails": True,
    "locale": "en-US"
}

with open(source, "rb") as f:
    data_bytes = f.read()

try:
    resp = post(url=post_url, data=data_bytes, headers=headers, params=params)
    if resp.status_code != 202:
        print("POST analyze failed:\n%s" % resp.text)
        quit()
    else:
        print("POST analyze succeeded:\n%s" % resp.headers)
        get_url = resp.headers["operation-location"]
except Exception as e:
    print("POST analyze failed:\n%s" % str(e))
    quit()

n_tries = 10
n_try = 0
wait_sec = 6
while n_try < n_tries:
    try:
        resp = get(url = get_url, headers = {"Ocp-Apim-Subscription-Key": apim_key})
        resp_json = json.loads(resp.text)
        if resp.status_code != 200:
            print("GET Receipt results failed:\n%s" % resp_json)
            quit()
        status = resp_json["status"]
        if status == "succeeded":
            print("Receipt Analysis succeeded:\n%s" % json.dumps(resp_json, indent=2, sort_keys=True))
            processed_data = de.DataProcessor(resp_json)
            receipt = de.Receipt()
            for item in processed_data.item_list:
                receipt.add_item(item)
            receipt.set_total_price(processed_data.total_price)
            print(receipt)
            quit()
        if status == "failed":
            print("Analysis failed:\n%s" % resp_json)
            quit()
        # Analysis still running. Wait and retry.
        time.sleep(wait_sec)
        n_try += 1
    except Exception as e:
        msg = "GET analyze results failed:\n%s" % str(e)
        print(msg)
        quit()
