import json
import os
import hashlib
import requests
import time
from dotenv import load_dotenv

load_dotenv()

class ShopeeAPIClient:
    def __init__(self):
        self.base_url = os.getenv("SHOPEE_API_URL")
        self.app_id = os.getenv("SHOPEE_APP_ID")
        self.secret_key = os.getenv("SHOPEE_SECRET_KEY")
        if not all([self.base_url, self.app_id, self.secret_key]):
            raise ValueError("API credentials or URL not configured in .env.")

    def _generate_signature(self, payload, timestamp):
        payload_str = json.dumps(payload)
        factor = f"{self.app_id}{timestamp}{str(payload_str)}{self.secret_key}"
        return hashlib.sha256(factor.encode()).hexdigest()
    
    def fetch_offers(self):
        query = """
            {
                productOfferV2(listType: 0, sortType: 5) {
                    nodes {
                        productName
                        commissionRate
                        commission
                        price
                        productLink
                        offerLink
                    }
                }
            }
        """
        payload = {"query": query}
        timestamp = str(int(time.time()))
        signature = self._generate_signature(payload, timestamp)
        
        headers = {
            "Content-Type": "application/json",
            "Authorization": f"SHA256 Credential={self.app_id},Timestamp={timestamp},Signature={signature}"
        }
        
        try:
            response = requests.post(self.base_url, json=payload, headers=headers)
            response.raise_for_status()
            data = response.json()
            if "errors" in data:
                raise Exception(f"API Error: {data['errors']}")
            return data.get("data", {}).get("productOfferV2", {}).get("nodes", [])
        except requests.RequestException as e:
            print(f"HTTP Request failed: {e}")
            return []
        
# Example usage:
if __name__ == "__main__":
    client = ShopeeAPIClient()
    offers = client.fetch_offers()
    for offer in offers:
        print(offer)