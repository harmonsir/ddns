import asyncio
import requests
import yaml

from core import cloudflare


def get_current_ip(ip_urls):
    for url in ip_urls:
        try:
            response = requests.get(url)
            if response.status_code == 200:
                return response.text.strip()
        except:
            pass
    return None


def update_dns(provider, domain, ip):
    # Code to update DNS record using the specified provider
    pass


async def update_domains(config):
    for domain_config in config['domains']:
        domain = domain_config['name']
        # interval = domain_config['interval']
        ip_type = domain_config['ip_type']
        ip_urls = domain_config['ip_urls']
        providers = domain_config['provider']
        current_ip = get_current_ip(ip_urls)
        if current_ip is not None:
            for provider in providers:
                provider_name = provider['name']
                api_key = provider['api_key']
                zone_id = provider['zone_id']
                # Authenticate with provider using api_key and zone_id
                # Update DNS record for domain using provider and current_ip
                cloudflare.update_dns_record(
                    api_key=api_key,
                    zone_id=zone_id,
                    domain=domain,
                    ip_address=current_ip,
                )


async def main():
    with open('config.yml', 'r') as f:
        config = yaml.safe_load(f)

    interval = config.get("globals", {}).get("interval", 300)
    while True:
        try:
            print("Starting update ddns !!")
            await update_domains(config)
            print("Done and sleep 300s !!")
            await asyncio.sleep(interval)
        except requests.exceptions.SSLError as e:
            print(e)
        except requests.exceptions.Timeout as e:
            print(f"err: {e} !!")
            await asyncio.sleep(15)
        except requests.exceptions.HTTPError as e:
            print(f"err: {e} !!")
            await asyncio.sleep(30)


if __name__ == '__main__':
    asyncio.run(main())
