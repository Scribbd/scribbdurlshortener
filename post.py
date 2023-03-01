import base64
import json
import os
from pathlib import Path

import gnupg
import requests

ENDPOINT = os.getenv("ENDPOINT")
KEYID = os.getenv("KEYID")
gnu_home = Path("~/.gnupg/")

gpg = gnupg.GPG(gnupghome=gnu_home.expanduser().resolve())

test_payload = {
  "target": "https://example.com"
}
encode_payload = json.dumps(test_payload, indent=2).encode("utf-8")

authorization_header: gnupg.Sign = gpg.sign(encode_payload, keyid=KEYID)
print(authorization_header)
encoded_header = base64.b64encode(authorization_header.data)
print(encoded_header)

response = requests.post(url=f"{ENDPOINT}/test",headers={"Authorization": encoded_header},json=test_payload)

print(response.status_code, response.reason)
print(response.text)
