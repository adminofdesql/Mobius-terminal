import requests
import re
from bs4 import BeautifulSoup

class DataMiner:
    def __init__(self):
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        }

    def clean_number(self, raw_text):
        """Removes symbols ($ , %) and converts to float."""
        clean = re.sub(r'[^\d.]', '', raw_text)
        try:
            return float(clean)
        except ValueError:
            return 0.0

    def scour(self, url, css_selector, name):
        """Fetches live data from a target URL."""
        print(f"[MINER] Connecting to source for '{name}'...")
        try:
            response = requests.get(url, headers=self.headers, timeout=5)
            if response.status_code == 200:
                soup = BeautifulSoup(response.content, 'html.parser')
                element = soup.select_one(css_selector)
                
                if element:
                    val = self.clean_number(element.get_text())
                    print(f"   -> Found Raw Data: {val}")
                    return val
                else:
                    print(f"   [ERROR] Selector not found: {css_selector}")
            else:
                print(f"   [ERROR] Connection failed: {response.status_code}")
        except Exception as e:
            print(f"   [ERROR] Scouring failed: {e}")
        
        return None