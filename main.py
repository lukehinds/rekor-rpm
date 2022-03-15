import base64
import requests
import json

REKOR_URL = "http://127.0.0.1:9000/api/v1/log/entries"

REKOR_API_HEADERS = {
    'Content-Type': 'application/json',
    'Accept': 'application/json'
}

def post_rekor_api(rpm_b64, rpm_pub_key_b64):
    payload_json = {
        "apiVersion": "0.0.1",
        "kind": "rpm",
        "spec": {
            "package": {
                "content": rpm_b64
            },
            "publicKey": {
                "content": rpm_pub_key_b64
            }
        }
    }
    payload = json.dumps(payload_json)
    r = requests.post(REKOR_URL, data=payload, headers=REKOR_API_HEADERS)
    print("Status code: {}".format(r.status_code))
    return r

def main():
    rpm = "NetworkManager-1.36.0-0.10.el9.x86_64.rpm"
    with open(rpm, "rb") as f:
        rpm_bytes = f.read()
        rpm_b64 = base64.b64encode(rpm_bytes).decode('utf-8')

    public_key = "rh_pub.gpg"
    with open(public_key, "rb") as f:
        public_key_bytes = f.read()
        rpm_pub_key_b64 = base64.b64encode(public_key_bytes).decode('utf-8')

    r = post_rekor_api(rpm_b64, rpm_pub_key_b64)
    print(r.text)

if __name__ == "__main__":
    main()
