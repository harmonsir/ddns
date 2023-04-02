import requests


def list_dns_records(api_key, zone_id):
    url = f"https://api.cloudflare.com/client/v4/zones/{zone_id}/dns_records"
    headers = {
        "Content-Type": "application/json",
        # "X-Auth-Key": f"{api_key}",
        "Authorization": f"Bearer {api_key}",
    }

    response = requests.get(url, headers=headers)
    # print(response.json())
    return response.json().get("result", [])


def update_dns_record(api_key, zone_id, domain, ip_address, **options):
    headers = {
        "Content-Type": "application/json",
        # "X-Auth-Key": f"{api_key}",
        "Authorization": f"Bearer {api_key}",
    }

    payload = {
        "content": ip_address,
        "name": domain,
        "type": options.get("type", "A"),
        "proxied": options.get("proxied", True),
        "ttl": options.get("ttl", 1),
        # "tags": ["owner:dns-team"],
    }

    id_ = None
    records = list_dns_records(api_key, zone_id)
    for c in records:
        if c["name"] == domain:
            if c["content"] == ip_address:
                print("No Change!")
                return
            id_ = c["id"]
            break
    if not id_:
        raise ValueError("Not found id_")

    url = f"https://api.cloudflare.com/client/v4/zones/{zone_id}/dns_records/{id_}"
    response = requests.put(url, headers=headers, json=payload)

    if response.status_code != 200:
        raise Exception(f'Failed to update DNS record: {response.text}')
    print(response.json())
