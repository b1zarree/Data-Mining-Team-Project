import requests
import logging
from typing import Dict, Any, Optional

# Loglama ayarları
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

class WeatherAPIClient:
    """Open-Meteo üzerinden tarihsel hava durumu verilerini çeken istemci sınıfı."""
    
    BASE_URL = "https://archive-api.open-meteo.com/v1/archive"
    
    # Karşılaştırmalı analiz için hedef şehirler ve koordinatları
    CITIES = {
        "Kraków": {"latitude": 50.0614, "longitude": 19.9366},
        "İstanbul": {"latitude": 41.0082, "longitude": 28.9784},
        "Ankara": {"latitude": 39.9199, "longitude": 32.8543},
        "Çanakkale": {"latitude": 40.1553, "longitude": 26.4142}
    }

    def __init__(self):
        # Bağlantı havuzunu (connection pooling) kullanarak performansı artırmak için Session kullanımı
        self.session = requests.Session()

    def fetch_historical_data(self, city: str, start_date: str, end_date: str) -> Optional[Dict[str, Any]]:
        """
        Belirtilen şehir ve tarih aralığı için günlük maksimum sıcaklık ve toplam yağış verilerini çeker.
        Tarih formatı: 'YYYY-MM-DD'
        """
        if city not in self.CITIES:
            logging.error(f"'{city}' tanımlı şehirler listesinde bulunamadı.")
            return None

        coords = self.CITIES[city]
        params = {
            "latitude": coords["latitude"],
            "longitude": coords["longitude"],
            "start_date": start_date,
            "end_date": end_date,
            "daily": ["temperature_2m_max", "precipitation_sum"],
            "timezone": "auto"
        }

        try:
            response = self.session.get(self.BASE_URL, params=params)
            response.raise_for_status()
            logging.info(f"{city} için hava durumu verileri başarıyla çekildi.")
            return response.json()
        except requests.exceptions.RequestException as e:
            logging.error(f"{city} verisi çekilirken hata oluştu: {e}")
            return None