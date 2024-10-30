import os
import sys
import django

# Proje kök dizinine gitmek için sys.path'e ekleme yap
# Projenin kök dizinini buraya ekle (manage.py'nin bulunduğu dizin)
sys.path.append("C:/Users/ahmet.yildirir/Desktop/DjangoTestler/FxS")

# Django ayarlarını doğru şekilde işaretle (settings.py dosyası Home içinde)
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'Home.settings')

# Asenkron işlemler için güvenlik uyarısını devre dışı bırakmak isterseniz:
os.environ["DJANGO_ALLOW_ASYNC_UNSAFE"] = "true"

# Django ortamını başlat
django.setup()


import http.client
import pandas as pd
import json
from datetime import datetime
import ssl
from django.db import IntegrityError, transaction
from basemodels.models import FikstureModelData


class FixtureDataHandler:

    def __init__(self, date):
        self.date = date

    def fetch_fixtures_from_api(self):
        """
        API'den fikstür verilerini çeker, hata durumunda boş değerlerle döner.
        """
        try:
            context = ssl._create_unverified_context()
            conn = http.client.HTTPSConnection('www.sofascore.com', context=context)
            conn.request('GET', f'/api/v1/sport/football/scheduled-events/{self.date}')
            response = conn.getresponse()
            data = json.loads(response.read())["events"]
            df = pd.DataFrame(data)
            model_data = [{
                'data_id': self.date.replace("-", ""),
                'tarih': self.date,
                'data': data,
                'count': len(df),
                'isprogress': False
            }]
        except Exception as e:
            print(f"API'den veri çekerken hata oluştu: {e}")
            model_data = [{
                'data_id': self.date.replace("-", ""),
                'tarih': self.date,
                'data': {},
                'count': 0,
                'isprogress': False
            }]
        
        return model_data

    def save_fixtures_to_db(self, api_data):
        """
        API'den gelen verileri veritabanına kaydeder. Mevcut kayıt varsa siler ve yenisini ekler.
        """
        
        for item in api_data:
            try:
                # Tarih formatını kontrol et ve hatalıysa varsayılan değeri kullan
                try:
                    tarih = datetime.strptime(item['tarih'], "%Y-%m-%d").date()
                except ValueError:
                    print(f"Geçersiz tarih formatı: {item['tarih']}, varsayılan tarih atanıyor.")
                    tarih = datetime.strptime("1900-01-01", "%Y-%m-%d").date()

                # Veritabanı işlemlerini atomik olarak başlat
                with transaction.atomic():
                    existing_entry = FikstureModelData.objects.filter(data_id=item['data_id']).first()

                    if existing_entry:
                        # Eğer veri mevcutsa, kaydı sil
                        existing_entry.delete()
                        print(f"Eski veri silindi: {item['data_id']}")

                    # Yeni kayıt ekle
                    FikstureModelData.objects.create(
                        data_id=item['data_id'],
                        tarih=tarih,  # Doğrulanmış tarih
                        data=item['data'],
                        count=item['count'],
                        isprogress=item['isprogress']
                    )
                    print(f"Yeni veri eklendi: {tarih}")

            except IntegrityError as e:
                print(f"IntegrityError oluştu: {e}")

                # Hata durumunda varsayılan değerlerle kayıt ekle
                with transaction.atomic():
                    FikstureModelData.objects.create(
                        data_id='19000101',  # Varsayılan data_id
                        tarih=datetime.strptime("1900-01-01", "%Y-%m-%d").date(),  # Varsayılan tarih
                        data={},  # Boş dictionary
                        count=0,  # Varsayılan 0
                        isprogress=False  # Varsayılan False
                    )
                    print(f"Boş değerlerle veri eklendi.")





from datetime import datetime, timedelta

# İki tarih arasında tüm tarihleri almak için fonksiyon
def get_dates_between(start_date, end_date):
    # Tarih formatı kontrolü (YYYY-MM-DD)
    start = datetime.strptime(start_date, "%Y-%m-%d")
    end = datetime.strptime(end_date, "%Y-%m-%d")

    # Başlangıç ve bitiş tarihleri arasında gün gün tarih oluştur
    date_list = [(start + timedelta(days=x)).strftime("%Y-%m-%d") for x in range(0, (end - start).days + 1)]
    return date_list

# Kullanıcıdan tarih aralığını al
start_date = input("Başlangıç tarihi girin (YYYY-MM-DD formatında): ")
end_date = input("Bitiş tarihi girin (YYYY-MM-DD formatında): ")

# İki tarih arasındaki tüm tarihleri al
date_range = get_dates_between(start_date, end_date)

# Her tarih için FixtureDataHandler class'ını çalıştır
for date in date_range:
    handler = FixtureDataHandler(date)  # Her tarih için yeni handler
    data = handler.fetch_fixtures_from_api()   # Veriyi API'den çek
    handler.save_fixtures_to_db(data)       # Veriyi veritabanına kaydet
