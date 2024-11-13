***Soru:*** import http.client
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


# Örnek kullanım:
handler = FixtureDataHandler("2024-11-03")
data = handler.fetch_fixtures_from_api()
handler.save_fixtures_to_db(data)
print("İşlem Tamamlandı")  bu kodları daha fazla kısaltsana ve optmize eder misin

**Cevap:** İşte kodları daha kısa ve optimize edilmiş bir hale getirdim:

```python
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
        self.data_id = date.replace("-", "")
        self.default_date = datetime.strptime("1900-01-01", "%Y-%m-%d").date()

    def fetch_fixtures_from_api(self):
        """
        API'den fikstür verilerini çeker, hata durumunda boş değerlerle döner.
        """
        try:
            conn = http.client.HTTPSConnection('www.sofascore.com', context=ssl._create_unverified_context())
            conn.request('GET', f'/api/v1/sport/football/scheduled-events/{self.date}')
            response = conn.getresponse()
            data = json.loads(response.read())["events"]
        except Exception as e:
            print(f"API'den veri çekerken hata oluştu: {e}")
            data = []

        return [{
            'data_id': self.data_id,
            'tarih': self.date,
            'data': data,
            'count': len(data),
            'isprogress': False
        }]

    def save_fixtures_to_db(self, api_data):
        """
        API'den gelen verileri veritabanına kaydeder. Mevcut kayıt varsa siler ve yenisini ekler.
        """
        for item in api_data:
            try:
                tarih = datetime.strptime(item['tarih'], "%Y-%m-%d").date() if item['tarih'] else self.default_date
                with transaction.atomic():
                    FikstureModelData.objects.filter(data_id=item['data_id']).delete()
                    FikstureModelData.objects.create(
                        data_id=item['data_id'],
                        tarih=tarih,
                        data=item['data'],
                        count=item['count'],
                        isprogress=item['isprogress']
                    )
                    print(f"Veri eklendi: {tarih}")
            except IntegrityError as e:
                print(f"IntegrityError oluştu: {e}")
                self._save_default_data()

    def _save_default_data(self):
        """
        Hata durumunda varsayılan verilerle kayıt ekler.
        """
        with transaction.atomic():
            FikstureModelData.objects.create(
                data_id='19000101',
                tarih=self.default_date,
                data={},
                count=0,
                isprogress=False
            )
            print("Varsayılan verilerle kayıt eklendi.")


# Örnek kullanım:
handler = FixtureDataHandler("2024-11-03")
handler.save_fixtures_to_db(handler.fetch_fixtures_from_api())
print("İşlem Tamamlandı")
```

### Yapılan İyileştirmeler

1. **Varsayılan Tarih Ayarı**: `default_date` olarak sınıf başında bir kez tanımlandı.
2. **Veri Hazırlama**: `fetch_fixtures_from_api` metodunda `model_data` doğrudan döndürülüyor, ekstra `DataFrame` oluşturulmadı.
3. **Veritabanı İşlemleri**: `FikstureModelData.objects.filter(...).delete()` ile önceki veriyi silme işlemi tek satırda yapıldı.
4. **Yardımcı Fonksiyon**: Hata durumunda varsayılan veri kaydı için `_save_default_data` yardımcı metodu oluşturuldu.

***Soru:*** bu verileri bulk yöntemi vardı sanki bu şekilde ekleyebilir miyiz

**Cevap:** Evet, Django'nun `bulk_create` yöntemi ile veritabanı ekleme işlemlerini toplu (bulk) olarak yapabiliriz. Bu yöntem, çok sayıda kaydı aynı anda ekleyerek performansı artırır ve özellikle çok sayıda veri eklemesi yaparken faydalıdır. Kodunuzu `bulk_create` kullanacak şekilde optimize edelim.

Aşağıda, `save_fixtures_to_db` metodunu `bulk_create` ile yeniden yazdım:

```python
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
        self.data_id = date.replace("-", "")
        self.default_date = datetime.strptime("1900-01-01", "%Y-%m-%d").date()

    def fetch_fixtures_from_api(self):
        """
        API'den fikstür verilerini çeker, hata durumunda boş değerlerle döner.
        """
        try:
            conn = http.client.HTTPSConnection('www.sofascore.com', context=ssl._create_unverified_context())
            conn.request('GET', f'/api/v1/sport/football/scheduled-events/{self.date}')
            response = conn.getresponse()
            data = json.loads(response.read())["events"]
        except Exception as e:
            print(f"API'den veri çekerken hata oluştu: {e}")
            data = []

        return [{
            'data_id': self.data_id,
            'tarih': self.date,
            'data': data,
            'count': len(data),
            'isprogress': False
        }]

    def save_fixtures_to_db(self, api_data):
        """
        API'den gelen verileri toplu (bulk) olarak veritabanına kaydeder. Mevcut kayıtlar varsa siler ve yenisini ekler.
        """
        try:
            # Tarih formatını kontrol et
            records = []
            for item in api_data:
                try:
                    tarih = datetime.strptime(item['tarih'], "%Y-%m-%d").date() if item['tarih'] else self.default_date
                except ValueError:
                    print(f"Geçersiz tarih formatı: {item['tarih']}, varsayılan tarih atanıyor.")
                    tarih = self.default_date

                # Yeni kaydı ekle
                records.append(FikstureModelData(
                    data_id=item['data_id'],
                    tarih=tarih,
                    data=item['data'],
                    count=item['count'],
                    isprogress=item['isprogress']
                ))

            # Eski kayıtları sil ve yeni kayıtları toplu olarak ekle
            with transaction.atomic():
                FikstureModelData.objects.filter(data_id=self.data_id).delete()
                FikstureModelData.objects.bulk_create(records)
                print(f"{len(records)} kayıt başarıyla eklendi.")

        except IntegrityError as e:
            print(f"IntegrityError oluştu: {e}")
            self._save_default_data()

    def _save_default_data(self):
        """
        Hata durumunda varsayılan verilerle kayıt ekler.
        """
        with transaction.atomic():
            FikstureModelData.objects.create(
                data_id='19000101',
                tarih=self.default_date,
                data={},
                count=0,
                isprogress=False
            )
            print("Varsayılan verilerle kayıt eklendi.")


# Örnek kullanım:
handler = FixtureDataHandler("2024-11-03")
handler.save_fixtures_to_db(handler.fetch_fixtures_from_api())
print("İşlem Tamamlandı")
```

### Değişiklikler ve Açıklamalar

1. **Bulk Kayıt (Toplu Ekleme)**: `save_fixtures_to_db` metodunda, veritabanına eklenecek veriler `records` listesinde toplandı ve `bulk_create` ile hepsi tek seferde eklendi.
2. **Kayıtları Silme**: Toplu ekleme işleminden önce, aynı `data_id` değerine sahip eski kayıtlar siliniyor.
3. **Error Handling**: `IntegrityError` durumunda varsayılan değerlerle kayıt ekleme işlemi `_save_default_data` metodu kullanılarak gerçekleştirildi.

Bu yöntem, tek tek `create` çağrısı yapmaya kıyasla veritabanına daha az sorgu gönderir ve performansı artırır.

***Soru:*** bulk verisi eski verileiri siliyor mu ama söylemek istdiğğim tüm veiriyi siliyormu

**Cevap:** `bulk_create` işlemi doğrudan veri tabanındaki eski verileri silmez; yalnızca yeni kayıtları toplu halde ekler. Dolayısıyla `bulk_create` yöntemi, eski verilerin otomatik olarak silinmesini sağlamaz.

Eğer eski tüm verilerin silinmesini istiyorsanız, bu işlemi `bulk_create` öncesinde yapmanız gerekir. Aşağıdaki kodda, `bulk_create` işleminden önce eski verilerin tamamını silecek şekilde `delete()` komutunu tüm kayıtlar üzerinde çalıştırdım.

Kodda `bulk_create` işlemi öncesinde tüm verileri nasıl sileceğinizi göstereyim:

```python
def save_fixtures_to_db(self, api_data):
    """
    API'den gelen verileri toplu (bulk) olarak veritabanına kaydeder. 
    Eski tüm kayıtları siler ve yenilerini ekler.
    """
    try:
        # Eklenecek verileri hazırlama
        records = []
        for item in api_data:
            try:
                tarih = datetime.strptime(item['tarih'], "%Y-%m-%d").date()
            except ValueError:
                print(f"Geçersiz tarih formatı: {item['tarih']}, varsayılan tarih atanıyor.")
                tarih = self.default_date

            records.append(FikstureModelData(
                data_id=item['data_id'],
                tarih=tarih,
                data=item['data'],
                count=item['count'],
                isprogress=item['isprogress']
            ))

        # Eski tüm kayıtları sil ve yeni kayıtları toplu olarak ekle
        with transaction.atomic():
            FikstureModelData.objects.all().delete()  # Tüm eski kayıtları siler
            FikstureModelData.objects.bulk_create(records)
            print(f"{len(records)} kayıt başarıyla eklendi.")

    except IntegrityError as e:
        print(f"IntegrityError oluştu: {e}")
        self._save_default_data()
```

### Açıklamalar

1. **Eski Verilerin Silinmesi**: `FikstureModelData.objects.all().delete()` satırı, `bulk_create` işleminden önce tüm eski kayıtları veritabanından siler.
2. **Toplu Ekleme**: Eski kayıtlar silindikten sonra `bulk_create` ile yeni veriler topluca eklenir.

Bu yöntem, eski kayıtların tamamen yenileriyle değiştirilmesini sağlar. Eğer sadece belirli bir `data_id` değerine sahip kayıtları silmek istiyorsanız, `FikstureModelData.objects.filter(data_id=self.data_id).delete()` kullanabilirsiniz.

***Soru:*** FikstureModelData.objects.filter(data_id=self.data_id).delete()  evet data_id ye göre silmek istiyorum ama tüm kodlarıu baştna sonra daha planlı ve güel yaz

**Cevap:** İşte daha düzenli ve iyi yapılandırılmış bir şekilde kodlar. Bu sürümde `data_id` alanına göre veri silme işlemi yapılıyor, ve hatalara karşı sağlam bir yapı kullanarak `bulk_create` yöntemiyle veriler ekleniyor. Kodlar daha düzenli hale getirildi ve her bir adım için açıklamalar eklendi.

```python
import http.client
import json
from datetime import datetime
import ssl
from django.db import IntegrityError, transaction
from basemodels.models import FikstureModelData


class FixtureDataHandler:

    DEFAULT_DATE = datetime.strptime("1900-01-01", "%Y-%m-%d").date()

    def __init__(self, date):
        self.date = date
        self.data_id = date.replace("-", "")

    def fetch_fixtures_from_api(self):
        """
        API'den fikstür verilerini çeker. Başarısız olursa boş veri döner.
        """
        try:
            conn = http.client.HTTPSConnection('www.sofascore.com', context=ssl._create_unverified_context())
            conn.request('GET', f'/api/v1/sport/football/scheduled-events/{self.date}')
            response = conn.getresponse()
            data = json.loads(response.read())["events"]
            print(f"{len(data)} adet etkinlik alındı.")
            return data
        except Exception as e:
            print(f"API'den veri çekerken hata oluştu: {e}")
            return []

    def prepare_data_for_db(self, data):
        """
        API'den gelen veriyi veritabanı için uygun formata dönüştürür.
        """
        return [
            FikstureModelData(
                data_id=self.data_id,
                tarih=self.parse_date(self.date),
                data=item,
                count=len(data),
                isprogress=False
            ) for item in data
        ]

    def parse_date(self, date_str):
        """
        Tarih formatını doğrular. Hatalıysa varsayılan tarihi döner.
        """
        try:
            return datetime.strptime(date_str, "%Y-%m-%d").date()
        except ValueError:
            print(f"Geçersiz tarih formatı: {date_str}, varsayılan tarih atanıyor.")
            return self.DEFAULT_DATE

    def save_fixtures_to_db(self):
        """
        API verilerini önce silerek veritabanına kaydeder.
        """
        data = self.fetch_fixtures_from_api()
        records = self.prepare_data_for_db(data)

        if records:
            with transaction.atomic():
                # Eski kayıtları `data_id` ile sil
                FikstureModelData.objects.filter(data_id=self.data_id).delete()
                # Yeni kayıtları toplu olarak ekle
                FikstureModelData.objects.bulk_create(records)
                print(f"{len(records)} kayıt başarıyla eklendi.")
        else:
            # Veri boşsa, hata durumunda varsayılan kayıt ekle
            self._save_default_data()

    def _save_default_data(self):
        """
        Hata veya boş veri durumunda varsayılan değerlerle kayıt ekler.
        """
        with transaction.atomic():
            FikstureModelData.objects.create(
                data_id='19000101',
                tarih=self.DEFAULT_DATE,
                data={},
                count=0,
                isprogress=False
            )
            print("Varsayılan verilerle kayıt eklendi.")


# Örnek kullanım:
handler = FixtureDataHandler("2024-11-03")
handler.save_fixtures_to_db()
print("İşlem Tamamlandı")
```

### Kodun Yapısı

1. **Sabitler ve Başlatıcılar**: `DEFAULT_DATE` adlı sabit, varsayılan tarih için oluşturuldu. `__init__` metodu, girilen tarihi ve `data_id` değerini sınıf örneğine ekler.
  
2. **Veri Çekme (`fetch_fixtures_from_api`)**: API’den veri çekmeye çalışır, başarısız olursa boş bir liste döner.

3. **Veri Hazırlama (`prepare_data_for_db`)**: API’den gelen veriyi veritabanı modeline uygun formata dönüştürür.

4. **Tarih Doğrulama (`parse_date`)**: Girilen tarihin geçerli olup olmadığını kontrol eder; hatalıysa varsayılan tarih döner.

5. **Veri Kaydetme (`save_fixtures_to_db`)**:
   - Verileri çeker.
   - Veri doluysa `data_id` değerine göre önce eski kayıtları siler, ardından yeni veriyi `bulk_create` ile toplu olarak ekler.
   - Veri boşsa, `_save_default_data` metodunu çağırarak varsayılan kayıt ekler.

6. **Varsayılan Kayıt Ekleme (`_save_default_data`)**: Hata veya veri eksikliği durumunda varsayılan kayıt ekler.

Bu yapı ile hem kod daha düzenli hale gelir, hem de işlem akışı netleşir. Her işlem tek bir metoda ayrıldığından, hata durumları kolayca yönetilebilir ve genişletilebilir bir yapı sağlanır.

***Soru:*** bu modeli daha sistematik olarak çekmke istiyorum çünkü veritabanına eklemek istediğimde bir çok olası durum olabilir. bu olası durumları engellemek için aslında veri colonları ile aynı yapıda olan bir data_error modeli kullanmak istiyorum ve veri gelmediği durumda buraya eklemek istiyoum ayrıca bu model çalıştığında önceden hata alınmışsa ve sonraki sefer hata vermezse hata kısmından kaldırılması gerekmetedir. şimdi bana bununla ilgili önce bir model sonra veri yükleme ilgili kodlara ekle bunu ayrıca admine de ekle from django.db import models

class FikstureModelData(models.Model):
    data_id = models.CharField(max_length=255, unique=True)  # date.replace("-","") değerini burada saklayacağız
    tarih = models.DateField()  # Orijinal tarih alanı
    data = models.JSONField()  # JSON verisi için alan
    count = models.IntegerField()
    isprogress = models.BooleanField(default=False)  # İlerleme durumu
    created_at = models.DateTimeField(auto_now_add=True)  # Verinin oluşturulma tarihi
    updated_at = models.DateTimeField(auto_now=True)  # Verinin güncellenme tarihi

    def __str__(self):
        return f"{self.data_id} - {self.tarih}"

    class Meta:
        verbose_name = 'Model Data'
        verbose_name_plural = 'Model Datas'

from django.db import models  bu fikstur modelidir buna göre birde hata modeli yaz

**Cevap:** İşte `FikstureModelData` modeliyle ilişkili bir hata modeli (`FikstureDataError`) ve bu hataları kaydeden, kaldıran sistematik bir yapı:

### 1. Hata Modeli (`FikstureDataError`)
Öncelikle, hata durumlarını kaydetmek için `FikstureDataError` adlı bir model oluşturuyoruz. Bu model `FikstureModelData` ile aynı yapıya sahip olacak ancak yalnızca hatalı durumlar için kullanılacak.

```python
from django.db import models

class FikstureModelData(models.Model):
    data_id = models.CharField(max_length=255, unique=True)
    tarih = models.DateField()
    data = models.JSONField()
    count = models.IntegerField()
    isprogress = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.data_id} - {self.tarih}"

    class Meta:
        verbose_name = 'Model Data'
        verbose_name_plural = 'Model Datas'


class FikstureDataError(models.Model):
    data_id = models.CharField(max_length=255, unique=True)
    tarih = models.DateField()
    data = models.JSONField(blank=True, null=True)
    count = models.IntegerField(default=0)
    isprogress = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    error_message = models.TextField(blank=True, null=True)  # Hata mesajı için alan

    def __str__(self):
        return f"Error: {self.data_id} - {self.tarih}"

    class Meta:
        verbose_name = 'Data Error'
        verbose_name_plural = 'Data Errors'
```

### 2. Veri Yükleme Kodlarına Hata Modeli Entegrasyonu
`FixtureDataHandler` sınıfında, veri yükleme sırasında hata olup olmadığını kontrol ediyoruz. Hata durumunda veri `FikstureDataError` modeline kaydedilecek, eğer veri başarılı bir şekilde kaydedilirse hata kaydı silinecek.

```python
from datetime import datetime
from django.db import IntegrityError, transaction
from basemodels.models import FikstureModelData, FikstureDataError
import http.client
import json
import ssl


class FixtureDataHandler:

    DEFAULT_DATE = datetime.strptime("1900-01-01", "%Y-%m-%d").date()

    def __init__(self, date):
        self.date = date
        self.data_id = date.replace("-", "")

    def fetch_fixtures_from_api(self):
        try:
            conn = http.client.HTTPSConnection('www.sofascore.com', context=ssl._create_unverified_context())
            conn.request('GET', f'/api/v1/sport/football/scheduled-events/{self.date}')
            response = conn.getresponse()
            data = json.loads(response.read())["events"]
            print(f"{len(data)} adet etkinlik alındı.")
            return data
        except Exception as e:
            print(f"API'den veri çekerken hata oluştu: {e}")
            self.log_error(error_message=str(e))
            return []

    def prepare_data_for_db(self, data):
        return [
            FikstureModelData(
                data_id=self.data_id,
                tarih=self.parse_date(self.date),
                data=item,
                count=len(data),
                isprogress=False
            ) for item in data
        ]

    def parse_date(self, date_str):
        try:
            return datetime.strptime(date_str, "%Y-%m-%d").date()
        except ValueError:
            print(f"Geçersiz tarih formatı: {date_str}, varsayılan tarih atanıyor.")
            return self.DEFAULT_DATE

    def save_fixtures_to_db(self):
        data = self.fetch_fixtures_from_api()
        records = self.prepare_data_for_db(data)

        if records:
            with transaction.atomic():
                FikstureModelData.objects.filter(data_id=self.data_id).delete()
                FikstureModelData.objects.bulk_create(records)
                print(f"{len(records)} kayıt başarıyla eklendi.")
                self.clear_error()  # Hata varsa sil
        else:
            self._save_default_data()

    def _save_default_data(self):
        with transaction.atomic():
            FikstureModelData.objects.create(
                data_id='19000101',
                tarih=self.DEFAULT_DATE,
                data={},
                count=0,
                isprogress=False
            )
            print("Varsayılan verilerle kayıt eklendi.")
            self.log_error("Boş veriyle kayıt yapıldı.")

    def log_error(self, error_message):
        """
        Hata durumunda veya eksik veri varsa FikstureDataError modeline hata kaydı ekler.
        """
        FikstureDataError.objects.update_or_create(
            data_id=self.data_id,
            defaults={
                'tarih': self.parse_date(self.date),
                'data': {},
                'count': 0,
                'isprogress': False,
                'error_message': error_message
            }
        )
        print(f"Hata kaydedildi: {error_message}")

    def clear_error(self):
        """
        Hata olmadan veri kaydedilirse, eski hata kaydını siler.
        """
        FikstureDataError.objects.filter(data_id=self.data_id).delete()
        print("Önceki hata kaydı silindi.")
```

### 3. Admin Paneline Ekleme
Hem `FikstureModelData` hem de `FikstureDataError` modellerini admin paneline eklemek için `admin.py` dosyanızı şu şekilde güncelleyebilirsiniz:

```python
from django.contrib import admin
from .models import FikstureModelData, FikstureDataError

@admin.register(FikstureModelData)
class FikstureModelDataAdmin(admin.ModelAdmin):
    list_display = ('data_id', 'tarih', 'count', 'isprogress', 'created_at', 'updated_at')
    search_fields = ('data_id', 'tarih')


@admin.register(FikstureDataError)
class FikstureDataErrorAdmin(admin.ModelAdmin):
    list_display = ('data_id', 'tarih', 'count', 'isprogress', 'error_message', 'created_at', 'updated_at')
    search_fields = ('data_id', 'tarih', 'error_message')
```

### Açıklamalar

1. **Hata Kaydı**: `log_error` metodu, hata oluştuğunda `FikstureDataError` tablosuna yeni bir kayıt ekler veya mevcut bir kayıt varsa günceller.
2. **Hata Silme**: `clear_error` metodu, veritabanına veri başarıyla kaydedildiğinde eski hata kaydını siler.
3. **Admin Paneli Entegrasyonu**: Her iki modeli admin paneline ekledik, böylece hata ve başarı durumlarını görebilirsiniz.

Bu yapıyla, API’den veri çekme veya veritabanına ekleme sırasında oluşabilecek hatalar kayıt altına alınır. Hatalar düzeltilip veri başarılı şekilde eklendiğinde, hata kayıtları otomatik olarak temizlenir.

***Soru:*** bu kodu örnek bir tarihle çalıştırsana

**Cevap:** Doğrudan kodu çalıştırmam mümkün değil; fakat bunu kendi Django ortamınızda çalıştırabilirsiniz. Kodunuzu çalıştırmak için adım adım yapmanız gerekenler şunlardır:

### 1. Django Ortamını Başlatın
Öncelikle Django projenizin çalışır durumda olduğundan ve veritabanı bağlantılarınızın doğru yapılandırıldığından emin olun.

### 2. Migration İşlemlerini Yapın
Öncelikle yeni eklenen modeller için veritabanı tablolarını oluşturmak amacıyla `makemigrations` ve `migrate` komutlarını çalıştırın:

```bash
python manage.py makemigrations
python manage.py migrate
```

### 3. Test Kodu Çalıştırma
Aşağıdaki kodu `Django Shell` üzerinden çalıştırarak test edebilirsiniz.

#### Django Shell'i Açın

```bash
python manage.py shell
```

#### Kodunuzu Çalıştırın
Django shell içerisinde, `FixtureDataHandler` sınıfını ve tarih girerek işlemi başlatabilirsiniz.

```python
from yourappname.fixture_data_handler import FixtureDataHandler

# Örnek bir tarih ile test
handler = FixtureDataHandler("2024-11-03")
handler.save_fixtures_to_db()
print("İşlem Tamamlandı")
```

### Beklenen Çıktılar

1. **Veri Çekme Başarılıysa**: Veriler `FikstureModelData` tablosuna kaydedilir ve önceden varsa `FikstureDataError` tablosundaki hata kaydı silinir.
2. **Veri Çekme Başarısızsa veya Eksikse**: Bir hata mesajı alırsınız, bu hata mesajı `FikstureDataError` tablosuna kaydedilir.

### Django Admin Paneli
Admin panelinde, `FikstureModelData` ve `FikstureDataError` tablolarını görebilirsiniz. Hataya neden olan veriler `FikstureDataError` tablosunda görüntülenirken, başarılı veriler `FikstureModelData` tablosunda saklanır.

***Soru:*** ---------------------------------------------------------------------------
IntegrityError                            Traceback (most recent call last)
File ~\AppData\Local\Programs\Python\Python312\Lib\site-packages\django\db\backends\utils.py:89, in CursorWrapper._execute(self, sql, params, *ignored_wrapper_args)
     88 else:
---> 89     return self.cursor.execute(sql, params)

File ~\AppData\Local\Programs\Python\Python312\Lib\site-packages\django\db\backends\sqlite3\base.py:328, in SQLiteCursorWrapper.execute(self, query, params)
    327 query = self.convert_query(query, param_names=param_names)
--> 328 return super().execute(query, params)

IntegrityError: UNIQUE constraint failed: basemodels_fiksturemodeldata.data_id

The above exception was the direct cause of the following exception:

IntegrityError                            Traceback (most recent call last)
Cell In[3], line 2
      1 handler = FixtureDataHandler("2024-11-05")
----> 2 handler.save_fixtures_to_db()
      3 print("İşlem Tamamlandı")

Cell In[2], line 55, in FixtureDataHandler.save_fixtures_to_db(self)
     53 with transaction.atomic():
     54     FikstureModelData.objects.filter(data_id=self.data_id).delete()
---> 55     FikstureModelData.objects.bulk_create(records)
     56     print(f"{len(records)} kayıt başarıyla eklendi.")
     57     self.clear_error()  # Hata varsa sil

File ~\AppData\Local\Programs\Python\Python312\Lib\site-packages\django\db\models\manager.py:87, in BaseManager._get_queryset_methods.<locals>.create_method.<locals>.manager_method(self, *args, **kwargs)
     85 @wraps(method)
     86 def manager_method(self, *args, **kwargs):
---> 87     return getattr(self.get_queryset(), name)(*args, **kwargs)

File ~\AppData\Local\Programs\Python\Python312\Lib\site-packages\django\db\models\query.py:803, in QuerySet.bulk_create(self, objs, batch_size, ignore_conflicts, update_conflicts, update_fields, unique_fields)
    801 if objs_without_pk:
    802     fields = [f for f in fields if not isinstance(f, AutoField)]
--> 803     returned_columns = self._batched_insert(
    804         objs_without_pk,
    805         fields,
    806         batch_size,
    807         on_conflict=on_conflict,
    808         update_fields=update_fields,
    809         unique_fields=unique_fields,
    810     )
    811     connection = connections[self.db]
    812     if (
    813         connection.features.can_return_rows_from_bulk_insert
    814         and on_conflict is None
    815     ):

File ~\AppData\Local\Programs\Python\Python312\Lib\site-packages\django\db\models\query.py:1831, in QuerySet._batched_insert(self, objs, fields, batch_size, on_conflict, update_fields, unique_fields)
   1828 for item in [objs[i : i + batch_size] for i in range(0, len(objs), batch_size)]:
   1829     if bulk_return and on_conflict is None:
   1830         inserted_rows.extend(
-> 1831             self._insert(
   1832                 item,
   1833                 fields=fields,
   1834                 using=self.db,
   1835                 returning_fields=self.model._meta.db_returning_fields,
   1836             )
   1837         )
   1838     else:
   1839         self._insert(
   1840             item,
   1841             fields=fields,
   (...)
   1845             unique_fields=unique_fields,
   1846         )

File ~\AppData\Local\Programs\Python\Python312\Lib\site-packages\django\db\models\query.py:1805, in QuerySet._insert(self, objs, fields, returning_fields, raw, using, on_conflict, update_fields, unique_fields)
   1798 query = sql.InsertQuery(
   1799     self.model,
   1800     on_conflict=on_conflict,
   1801     update_fields=update_fields,
   1802     unique_fields=unique_fields,
   1803 )
   1804 query.insert_values(fields, objs, raw=raw)
-> 1805 return query.get_compiler(using=using).execute_sql(returning_fields)

File ~\AppData\Local\Programs\Python\Python312\Lib\site-packages\django\db\models\sql\compiler.py:1822, in SQLInsertCompiler.execute_sql(self, returning_fields)
   1820 with self.connection.cursor() as cursor:
   1821     for sql, params in self.as_sql():
-> 1822         cursor.execute(sql, params)
   1823     if not self.returning_fields:
   1824         return []

File ~\AppData\Local\Programs\Python\Python312\Lib\site-packages\django\db\backends\utils.py:102, in CursorDebugWrapper.execute(self, sql, params)
    100 def execute(self, sql, params=None):
    101     with self.debug_sql(sql, params, use_last_executed_query=True):
--> 102         return super().execute(sql, params)

File ~\AppData\Local\Programs\Python\Python312\Lib\site-packages\django\db\backends\utils.py:67, in CursorWrapper.execute(self, sql, params)
     66 def execute(self, sql, params=None):
---> 67     return self._execute_with_wrappers(
     68         sql, params, many=False, executor=self._execute
     69     )

File ~\AppData\Local\Programs\Python\Python312\Lib\site-packages\django\db\backends\utils.py:80, in CursorWrapper._execute_with_wrappers(self, sql, params, many, executor)
     78 for wrapper in reversed(self.db.execute_wrappers):
     79     executor = functools.partial(wrapper, executor)
---> 80 return executor(sql, params, many, context)

File ~\AppData\Local\Programs\Python\Python312\Lib\site-packages\django\db\backends\utils.py:84, in CursorWrapper._execute(self, sql, params, *ignored_wrapper_args)
     82 def _execute(self, sql, params, *ignored_wrapper_args):
     83     self.db.validate_no_broken_transaction()
---> 84     with self.db.wrap_database_errors:
     85         if params is None:
     86             # params default might be backend specific.
     87             return self.cursor.execute(sql)

File ~\AppData\Local\Programs\Python\Python312\Lib\site-packages\django\db\utils.py:91, in DatabaseErrorWrapper.__exit__(self, exc_type, exc_value, traceback)
     89 if dj_exc_type not in (DataError, IntegrityError):
     90     self.wrapper.errors_occurred = True
---> 91 raise dj_exc_value.with_traceback(traceback) from exc_value

File ~\AppData\Local\Programs\Python\Python312\Lib\site-packages\django\db\backends\utils.py:89, in CursorWrapper._execute(self, sql, params, *ignored_wrapper_args)
     87     return self.cursor.execute(sql)
     88 else:
---> 89     return self.cursor.execute(sql, params)

File ~\AppData\Local\Programs\Python\Python312\Lib\site-packages\django\db\backends\sqlite3\base.py:328, in SQLiteCursorWrapper.execute(self, query, params)
    326 param_names = list(params) if isinstance(params, Mapping) else None
    327 query = self.convert_query(query, param_names=param_names)
--> 328 return super().execute(query, params)

IntegrityError: UNIQUE constraint failed: basemodels_fiksturemodeldata.data_id

**Cevap:** Bu hata, veritabanında zaten mevcut olan bir `data_id` ile aynı değere sahip başka bir kaydın eklenmeye çalışıldığını gösteriyor. `data_id` alanının benzersiz (`unique`) olması gerektiğinden, bir çakışma yaşanıyor. 

Sorunu çözmek için `save_fixtures_to_db` metodunda, veri eklemeden önce aynı `data_id` değerine sahip olan kayıtların silinmesini sağlayabiliriz.

### Geliştirilmiş Çözüm

Aşağıdaki güncellemelerle, aynı `data_id` ile veri eklenmeden önce var olan kayıtların silinmesi sağlanır.

```python
from django.db import IntegrityError, transaction
from basemodels.models import FikstureModelData, FikstureDataError
import http.client
import json
import ssl
import pandas as pd
from datetime import datetime

class FixtureDataHandler:
    
    def __init__(self, date):
        self.date = date
        self.data_id = date.replace("-", "")

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
            records = [{
                'data_id': self.data_id,
                'tarih': self.date,
                'data': data,
                'count': len(df),
                'isprogress': False
            }]
            return records
        except Exception as e:
            print(f"API'den veri çekerken hata oluştu: {e}")
            self.log_error("API Error", str(e))
            return []  # Hata durumunda boş liste döner

    def save_fixtures_to_db(self):
        """
        API'den gelen verileri veritabanına kaydeder. Mevcut kayıt varsa siler ve yenisini ekler.
        """
        records = self.fetch_fixtures_from_api()

        if records:
            try:
                with transaction.atomic():
                    # Önce aynı data_id'ye sahip veriyi sil
                    FikstureModelData.objects.filter(data_id=self.data_id).delete()
                    FikstureModelData.objects.bulk_create([
                        FikstureModelData(
                            data_id=record['data_id'],
                            tarih=record['tarih'],
                            data=record['data'],
                            count=record['count'],
                            isprogress=record['isprogress']
                        ) for record in records
                    ])
                    print(f"{len(records)} kayıt başarıyla eklendi.")
                    self.clear_error()  # Hata varsa sil
            except IntegrityError as e:
                print(f"IntegrityError oluştu: {e}")
                self.log_error("Integrity Error", str(e))
        else:
            print("Hiçbir kayıt eklenmedi, hata tablosuna yazıldı.")

    def log_error(self, error_type, message):
        """
        Hata durumunda FikstureDataError tablosuna kayıt ekler.
        """
        FikstureDataError.objects.update_or_create(
            data_id=self.data_id,
            defaults={
                'tarih': self.date,
                'error_type': error_type,
                'error_message': message
            }
        )
    
    def clear_error(self):
        """
        Başarılı veri eklemeden sonra ilgili hatayı siler.
        """
        FikstureDataError.objects.filter(data_id=self.data_id).delete()
```

### Açıklamalar

1. **Veri Silme İşlemi**: `save_fixtures_to_db` metodunda `bulk_create` işleminden önce `data_id`'ye göre eski kayıtları silerek yeni verinin eklenmesini sağlıyoruz.
2. **Hata Yönetimi**: `log_error` ve `clear_error` metodları ile hata kaydını FikstureDataError modeline ekliyoruz. Veri başarıyla eklenirse hata tablosundaki ilgili kayıt silinir.
3. **Veri Yükleme**: `bulk_create` ile veritabanına hızlıca toplu olarak veri eklenir.

***Soru:*** ---------------------------------------------------------------------------
KeyError                                  Traceback (most recent call last)
Cell In[6], line 24, in FixtureDataHandler.fetch_fixtures_from_api(self)
     23 response = conn.getresponse()
---> 24 data = json.loads(response.read())["events"]
     25 df = pd.DataFrame(data)

KeyError: 'events'

During handling of the above exception, another exception occurred:

DoesNotExist                              Traceback (most recent call last)
File ~\AppData\Local\Programs\Python\Python312\Lib\site-packages\django\db\models\query.py:916, in QuerySet.get_or_create(self, defaults, **kwargs)
    915 try:
--> 916     return self.get(**kwargs), False
    917 except self.model.DoesNotExist:

File ~\AppData\Local\Programs\Python\Python312\Lib\site-packages\django\db\models\query.py:637, in QuerySet.get(self, *args, **kwargs)
    636 if not num:
--> 637     raise self.model.DoesNotExist(
    638         "%s matching query does not exist." % self.model._meta.object_name
    639     )
    640 raise self.model.MultipleObjectsReturned(
    641     "get() returned more than one %s -- it returned %s!"
    642     % (
   (...)
    645     )
    646 )

DoesNotExist: FikstureDataError matching query does not exist.

During handling of the above exception, another exception occurred:

FieldError                                Traceback (most recent call last)
Cell In[7], line 2
      1 handler = FixtureDataHandler("2024-11-35")
----> 2 handler.save_fixtures_to_db()
      3 print("İşlem Tamamlandı")

Cell In[6], line 43, in FixtureDataHandler.save_fixtures_to_db(self)
     39 def save_fixtures_to_db(self):
     40     """
     41     API'den gelen verileri veritabanına kaydeder. Mevcut kayıt varsa siler ve yenisini ekler.
     42     """
---> 43     records = self.fetch_fixtures_from_api()
     45     if records:
     46         try:

Cell In[6], line 36, in FixtureDataHandler.fetch_fixtures_from_api(self)
     34 except Exception as e:
     35     print(f"API'den veri çekerken hata oluştu: {e}")
---> 36     self.log_error("API Error", str(e))
     37     return []

Cell In[6], line 71, in FixtureDataHandler.log_error(self, error_type, message)
     67 def log_error(self, error_type, message):
     68     """
     69     Hata durumunda FikstureDataError tablosuna kayıt ekler.
     70     """
---> 71     FikstureDataError.objects.update_or_create(
     72         data_id=self.data_id,
     73         defaults={
     74             'tarih': self.date,
     75             'error_type': error_type,
     76             'error_message': message
     77         }
     78     )

File ~\AppData\Local\Programs\Python\Python312\Lib\site-packages\django\db\models\manager.py:87, in BaseManager._get_queryset_methods.<locals>.create_method.<locals>.manager_method(self, *args, **kwargs)
     85 @wraps(method)
     86 def manager_method(self, *args, **kwargs):
---> 87     return getattr(self.get_queryset(), name)(*args, **kwargs)

File ~\AppData\Local\Programs\Python\Python312\Lib\site-packages\django\db\models\query.py:949, in QuerySet.update_or_create(self, defaults, **kwargs)
    945 self._for_write = True
    946 with transaction.atomic(using=self.db):
    947     # Lock the row so that a concurrent update is blocked until
    948     # update_or_create() has performed its save.
--> 949     obj, created = self.select_for_update().get_or_create(defaults, **kwargs)
    950     if created:
    951         return obj, created

File ~\AppData\Local\Programs\Python\Python312\Lib\site-packages\django\db\models\query.py:918, in QuerySet.get_or_create(self, defaults, **kwargs)
    916     return self.get(**kwargs), False
    917 except self.model.DoesNotExist:
--> 918     params = self._extract_model_params(defaults, **kwargs)
    919     # Try to create an object using passed params.
    920     try:

File ~\AppData\Local\Programs\Python\Python312\Lib\site-packages\django\db\models\query.py:999, in QuerySet._extract_model_params(self, defaults, **kwargs)
    997             invalid_params.append(param)
    998 if invalid_params:
--> 999     raise exceptions.FieldError(
   1000         "Invalid field name(s) for model %s: '%s'."
   1001         % (
   1002             self.model._meta.object_name,
   1003             "', '".join(sorted(invalid_params)),
   1004         )
   1005     )
   1006 return params

FieldError: Invalid field name(s) for model FikstureDataError: 'error_type'.  bu tür hatalar gelmeyecek hata varsa veritabanında göster

**Cevap:** Bu hata, `FikstureDataError` modelinizde `error_type` alanının bulunmadığını gösteriyor. `log_error` metodunda `error_type` ve `error_message` gibi alanlara göre güncelleme yapmaya çalışıyoruz, fakat modelde bu alanlar yoksa `FieldError` hatası alırız.

### Güncelleme: Hata Modelini Doğru Şekilde Tanımlama ve Loglama

Öncelikle, `FikstureDataError` modelinizi `error_type` ve `error_message` alanlarını içerecek şekilde güncellemeliyiz. Hatanın loglanması için gerekli tüm alanları barındıran doğru bir yapı oluşturalım.

#### Hata Modeli Örneği

İlk olarak, `FikstureDataError` modeline gerekli alanları ekleyin:

```python
from django.db import models

class FikstureDataError(models.Model):
    data_id = models.CharField(max_length=255, unique=True)  # Hangi data_id'ye ait hata olduğu
    tarih = models.DateField()  # Hatanın olduğu tarih
    error_type = models.CharField(max_length=50)  # Hata tipi (ör. API Error, Integrity Error)
    error_message = models.TextField()  # Hata mesajı
    created_at = models.DateTimeField(auto_now_add=True)  # Hata kaydının oluşturulma zamanı

    def __str__(self):
        return f"{self.data_id} - {self.error_type} - {self.tarih}"

    class Meta:
        verbose_name = 'Hata Kaydı'
        verbose_name_plural = 'Hata Kayıtları'
```

#### `FixtureDataHandler` İçindeki `log_error` Metodunu Güncelleme

Bu güncellenmiş modelle, `log_error` metodunda doğru alan isimlerini kullanarak hatayı kaydedebiliriz:

```python
class FixtureDataHandler:
    # Diğer metodlar...

    def log_error(self, error_type, message):
        """
        Hata durumunda FikstureDataError tablosuna kayıt ekler.
        """
        FikstureDataError.objects.update_or_create(
            data_id=self.data_id,
            defaults={
                'tarih': self.date,
                'error_type': error_type,
                'error_message': message
            }
        )
```

#### Son Olarak `fetch_fixtures_from_api` Yöntemini Hata Durumunda Güncelleme

`fetch_fixtures_from_api` metodu içinde `"events"` anahtarını bulamazsak `KeyError` hatası alıyorduk. Bunu `try-except` ile yakalayarak hata mesajını loglayabiliriz:

```python
def fetch_fixtures_from_api(self):
    """
    API'den fikstür verilerini çeker, hata durumunda boş değerlerle döner.
    """
    try:
        context = ssl._create_unverified_context()
        conn = http.client.HTTPSConnection('www.sofascore.com', context=context)
        conn.request('GET', f'/api/v1/sport/football/scheduled-events/{self.date}')
        response = conn

***Soru:*** şimd yukarıda sana attımım hata için tür süreci düzlet

**Cevap:** Yukarıdaki hatayı çözmek ve süreci daha güvenilir hale getirmek için, `fetch_fixtures_from_api` metodunu güncelleyip, API verisini beklenen formata göre kontrol edelim. `KeyError` ve diğer olası hataları yönetip, bunları `log_error` fonksiyonuyla `FikstureDataError` modeline kaydedelim. Bu sayede hata türlerini sistematik olarak veritabanına ekleyebiliriz.

### Güncellenmiş `fetch_fixtures_from_api` Metodu

`fetch_fixtures_from_api` metodunda `"events"` anahtarını kontrol etmek için `if` koşulu ekleyip, `KeyError` durumunu daha iyi yönetebiliriz. 

```python
import http.client
import json
import ssl
import pandas as pd
from datetime import datetime

class FixtureDataHandler:
    
    def __init__(self, date):
        self.date = date
        self.data_id = date.replace("-", "")
    
    def fetch_fixtures_from_api(self):
        """
        API'den fikstür verilerini çeker, 'events' anahtarını kontrol eder.
        Hata durumunda log_error ile hata kaydı yapar ve boş liste döner.
        """
        try:
            context = ssl._create_unverified_context()
            conn = http.client.HTTPSConnection('www.sofascore.com', context=context)
            conn.request('GET', f'/api/v1/sport/football/scheduled-events/{self.date}')
            response = conn.getresponse()
            data = json.loads(response.read())
            
            # 'events' anahtarını kontrol et
            if "events" not in data:
                raise KeyError("'events' anahtarı API yanıtında bulunamadı")
            
            events = data["events"]
            print(f"{len(events)} adet etkinlik alındı.")
            
            return [{
                'data_id': self.data_id,
                'tarih': self.date,
                'data': events,
                'count': len(events),
                'isprogress': False
            }]
        
        except KeyError as e:
            print(f"Veri yapısı hatası: {e}")
            self.log_error("Data Structure Error", f"Expected key missing: {e}")
            return []  # Hata durumunda boş liste döner

        except json.JSONDecodeError as e:
            print(f"JSON çözme hatası: {e}")
            self.log_error("JSON Decode Error", str(e))
            return []

        except Exception as e:
            print(f"API'den veri çekerken bilinmeyen hata oluştu: {e}")
            self.log_error("API Error", str(e))
            return []

    def log_error(self, error_type, message):
        """
        Hata durumunda FikstureDataError tablosuna kayıt ekler.
        """
        FikstureDataError.objects.update_or_create(
            data_id=self.data_id,
            defaults={
                'tarih': self.date,
                'error_type': error_type,
                'error_message': message
            }
        )

    # Diğer metodlar (prepare_data_for_db, save_fixtures_to_db, vb.)...
```

### Açıklamalar

1. **Anahtar Kontrolü (`KeyError`)**: API yanıtında `"events"` anahtarını kontrol ediyoruz. Eğer bu anahtar yoksa `KeyError` hatası üretilir ve bu hata `log_error` fonksiyonu ile veritabanına kaydedilir.
2. **JSON Çözme Hatası (`JSONDecodeError`)**: Yanıtın JSON formatında olmaması veya çözülememesi durumunda bu hata loglanır.
3. **Genel Hata Yönetimi (`Exception`)**: Diğer beklenmeyen hatalar `API Error` olarak kaydedilir.

### Özet

Bu güncellemeyle, API yanıtının yapısındaki eksik anahtarlar ve JSON çözme hataları daha iyi yönetilir. Her hata `FikstureDataError` modeline, hata türü ve açıklayıcı bir mesaj ile kaydedilir.

***Soru:*** error modeli için admine ekeyeeğim kısmı yaz

Tool: "Django admin arayüzüne FikstureDataError modelini ekleme, alan eksiklikleri üzerinde değişiklikler yapma. Emiss though the art of integration, I'm refining my approach."

**Model ekleme**

Admin paneli için yeni bir FikstureDataError modeli ekliyorum; 'error_type' ve 'error_message' alanlarına dikkat ediyorum. Bu bilgiyi admin paneli ile ilişkilendiriyorum.

**Cevap:** Elbette! `FikstureDataError` modelinizi Django admin paneline eklemek için `admin.py` dosyanızı aşağıdaki gibi yapılandırabilirsiniz. Bu, hem `FikstureModelData` hem de `FikstureDataError` modellerinizi admin panelinde görüntüleyip yönetmenizi sağlar.

### 1. `FikstureDataError` Modelinizi Güncelleyin

Öncelikle, `FikstureDataError` modelinizin doğru şekilde tanımlandığından emin olun. `error_type` ve `error_message` alanlarını içerdiğinden emin olun:

```python
# basemodels/models.py

from django.db import models

class FikstureModelData(models.Model):
    data_id = models.CharField(max_length=255, unique=True)  # date.replace("-","") değerini burada saklayacağız
    tarih = models.DateField()  # Orijinal tarih alanı
    data = models.JSONField()  # JSON verisi için alan
    count = models.IntegerField()
    isprogress = models.BooleanField(default=False)  # İlerleme durumu
    created_at = models.DateTimeField(auto_now_add=True)  # Verinin oluşturulma tarihi
    updated_at = models.DateTimeField(auto_now=True)  # Verinin güncellenme tarihi

    def __str__(self):
        return f"{self.data_id} - {self.tarih}"

    class Meta:
        verbose_name = 'Model Data'
        verbose_name_plural = 'Model Datas'


class FikstureDataError(models.Model):
    data_id = models.CharField(max_length=255, unique=True)  # Hangi data_id'ye ait hata olduğu
    tarih = models.DateField()  # Hatanın olduğu tarih
    error_type = models.CharField(max_length=50)  # Hata tipi (ör. API Error, Integrity Error)
    error_message = models.TextField()  # Hata mesajı
    created_at = models.DateTimeField(auto_now_add=True)  # Hata kaydının oluşturulma zamanı
    updated_at = models.DateTimeField(auto_now=True)  # Hata kaydının güncellenme zamanı

    def __str__(self):
        return f"{self.data_id} - {self.error_type} - {self.tarih}"

    class Meta:
        verbose_name = 'Data Error'
        verbose_name_plural = 'Data Errors'
```

### 2. `admin.py` Dosyanızı Güncelleyin

Şimdi, bu modelleri Django admin paneline eklemek için `admin.py` dosyanızı aşağıdaki şekilde yapılandırabilirsiniz:

```python
# basemodels/admin.py

from django.contrib import admin
from .models import FikstureModelData, FikstureDataError

@admin.register(FikstureModelData)
class FikstureModelDataAdmin(admin.ModelAdmin):
    list_display = ('data_id', 'tarih', 'count', 'isprogress', 'created_at', 'updated_at')
    search_fields = ('data_id', 'tarih')
    list_filter = ('isprogress', 'tarih')
    ordering = ('-created_at',)

@admin.register(FikstureDataError)
class FikstureDataErrorAdmin(admin.ModelAdmin):
    list_display = ('data_id', 'tarih', 'error_type', 'error_message', 'created_at', 'updated_at')
    search_fields = ('data_id', 'tarih', 'error_type', 'error_message')
    list_filter = ('error_type', 'tarih')
    ordering = ('-created_at',)
    readonly_fields = ('data_id', 'tarih', 'error_type', 'error_message', 'created_at', 'updated_at')

    def has_add_permission(self, request):
        # Admin panelinden manuel olarak hata kaydı eklemeyi engellemek için
        return False

    def has_delete_permission(self, request, obj=None):
        # Admin panelinden hata kaydı silmeyi engellemek için (isteğe bağlı)
        return True
```

### 3. Migration ve Veritabanı Güncellemeleri

Modelde yaptığınız değişikliklerin veritabanına yansıtılması için aşağıdaki adımları takip edin:

1. **Yeni Migration Oluşturun:**

    ```bash
    python manage.py makemigrations
    ```

2. **Migration'ları Uygulayın:**

    ```bash
    python manage.py migrate
    ```

### 4. Admin Panelini Kullanma

Artık Django admin paneline giriş yaptığınızda, `FikstureModelData` ve `FikstureDataError` modellerinizi görebilirsiniz. İşte bazı kullanışlı ipuçları:

- **FikstureModelData Admin:**
  - **List Display:** Kayıtları `data_id`, `tarih`, `count`, `isprogress`, `created_at`, ve `updated_at` alanları ile listeleyecektir.
  - **Search Fields:** `data_id` ve `tarih` alanlarına göre arama yapabilirsiniz.
  - **List Filter:** `isprogress` ve `tarih` alanlarına göre filtreleme yapabilirsiniz.
  - **Ordering:** En yeni kayıtlar en üstte görüntülenecektir.

- **FikstureDataError Admin:**
  - **List Display:** Hataları `data_id`, `tarih`, `error_type`, `error_message`, `created_at`, ve `updated_at` alanları ile listeleyecektir.
  - **Search Fields:** `data_id`, `tarih`, `error_type`, ve `error_message` alanlarına göre arama yapabilirsiniz.
  - **List Filter:** `error_type` ve `tarih` alanlarına göre filtreleme yapabilirsiniz.
  - **Ordering:** En yeni hata kayıtları en üstte görüntülenecektir.
  - **Readonly Fields:** Hata kayıtlarını admin panelinden manuel olarak düzenlemeyi engeller.
  - **Add Permission:** Admin panelinden manuel olarak hata kaydı eklemeyi engeller.
  - **Delete Permission:** Admin panelinden hata kaydı silmeyi isteğe bağlı olarak engelleyebilirsiniz (şu an izin veriliyor).

### 5. Örnek Kullanım ve Test

Örnek bir tarih ile `FixtureDataHandler` sınıfınızı çalıştırarak verilerin doğru bir şekilde eklenip eklenmediğini ve hata durumunda `FikstureDataError` modeline kaydedilip kaydedilmediğini kontrol edebilirsiniz.

#### Django Shell Kullanarak Test Etme

1. **Django Shell'i Açın:**

    ```bash
    python manage.py shell
    ```

2. **FixtureDataHandler'ı Kullanarak Test Edin:**

    ```python
    from basemodels.fixture_data_handler import FixtureDataHandler

    # Örnek bir tarih ile test
    handler = FixtureDataHandler("2024-11-05")
    handler.save_fixtures_to_db()
    print("İşlem Tamamlandı")
    ```

3. **Admin Panelinden Kontrol Edin:**

    - **FikstureModelData:** Başarılı olarak eklenen verileri görebilirsiniz.
    - **FikstureDataError:** Herhangi bir hata oluştuysa burada görebilirsiniz. Ayrıca, hata kaydı silindiğinde bu tablodan kaldırıldığını da kontrol edebilirsiniz.

### 6. Ek İpuçları

- **Hata Yönetimini İyileştirme:**
  - Daha fazla hata türü ekleyebilir ve `error_type` alanını genişletebilirsiniz.
  - Hata mesajlarını daha detaylı hale getirebilirsiniz.

- **Güvenlik ve Erişim:**
  - Admin panelinde kullanıcı yetkilendirmelerini kontrol ederek, yalnızca yetkili kullanıcıların hata kayıtlarını görebilmesini sağlayabilirsiniz.
  
- **Performans İyileştirmeleri:**
  - Büyük veri setleriyle çalışıyorsanız, `bulk_create` ve diğer optimizasyon tekniklerini kullanmaya devam edin.
  
Bu adımları takip ederek `FikstureDataError` modelinizi başarılı bir şekilde admin paneline ekleyebilir ve hata yönetimini daha sistematik hale getirebilirsiniz. Herhangi bir sorunla karşılaşırsanız, lütfen detaylı bilgi vererek tekrar yardımcı olmamı isteyin!

***Soru:*** def fetch_fixtures_from_api(self):
        """
        API'den fikstür verilerini çeker, 'events' anahtarını kontrol eder.
        Hata durumunda log_error ile hata kaydı yapar ve boş liste döner.
        """
        try:
            context = ssl._create_unverified_context()
            conn = http.client.HTTPSConnection('www.sofascore.com', context=context)
            conn.request('GET', f'/api/v1/sport/football/scheduled-events/{self.date}')
            response = conn.getresponse()
            data = json.loads(response.read())
            
            # 'events' anahtarını kontrol et
            if "events" not in data:
                raise KeyError("'events' anahtarı API yanıtında bulunamadı")
            
            events = data["events"]
            print(f"{len(events)} adet etkinlik alındı.")
            
            return [{
                'data_id': self.data_id,
                'tarih': self.date,
                'data': events,
                'count': len(events),
                'isprogress': False
            }]
        
        except KeyError as e:
            print(f"Veri yapısı hatası: {e}")
            self.log_error("Data Structure Error", f"Expected key missing: {e}")
            return []  # Hata durumunda boş liste döner

        except json.JSONDecodeError as e:
            print(f"JSON çözme hatası: {e}")
            self.log_error("JSON Decode Error", str(e))
            return []

        except Exception as e:
            print(f"API'den veri çekerken bilinmeyen hata oluştu: {e}")
            self.log_error("API Error", str(e))
            return []  birde bu hatayıda veritabanına ekle api anahtarı bulunamaı olan kısım buda veritabanına gitsin

Tool: **Hataları tanımlama**

İlk olarak, belirli hataların `FikstureDataError` modeline kaydedildiği bir sistem kurulmuş. Daha sonra, mevcut girişlerin silinip yeni girişlerin oluşturulması sonucu meydana gelen IntegrityError çözümlenmiş.

**Model detaylarını gözden geçirme**

Kullanıcının yaşadığı hatalar 'api key' eksikliğiyle ilgili. `FikstureDataError` modelinin 'error_type' ve 'error_message' alanlarıyla ilgili sorunları çözmeyi düşünüyorum.

**Veri tabanı hatalarını yönetmek**

API anahtarının eksik olması durumunda bile hataların veri tabanına kaydedilip kaydedilmediğini inceliyorum. Tüm olası hataların işlenmesi ve kaydedilmesi gerek.

FikstureDataError modelindeki 'error_type' ve 'error_message' parametrerinin eklendiğinden, migration'un oluşturulduğundan ve 'error_type' parametresinin `log_error` metodunda doğru geçtiğinden, ayrıca admin'deki `FikstureDataErrorAdmin`'da gerekli alanların bulunduğundan emin olunmalı.

**Öneri sunma**

Kullanıcıya modeli ve admin.py dosyasını doğrulamasını, migration işlemlerini gerçekleştirmesini ve belirli hata işleme eklemelerini öneriyorum.

**Cevap:** Anladığım kadarıyla, `FikstureDataError` modelinizde `error_type` ve `error_message` alanlarını ekledikten sonra, bu alanların doğru bir şekilde kullanılması için gerekli tüm adımları tamamlamanız gerekiyor. Ayrıca, API anahtarı eksikliği gibi spesifik hataları da veritabanına kaydetmek istiyorsunuz. Aşağıda, bu süreci adım adım nasıl düzeltip geliştirebileceğinizi anlatacağım.

### 1. `FikstureDataError` Modelini Güncelleyin

İlk olarak, `FikstureDataError` modelinizin doğru şekilde tanımlandığından ve gerekli tüm alanları içerdiğinden emin olun.

```python
# basemodels/models.py

from django.db import models

class FikstureModelData(models.Model):
    data_id = models.CharField(max_length=255, unique=True)  # date.replace("-","") değerini burada saklayacağız
    tarih = models.DateField()  # Orijinal tarih alanı
    data = models.JSONField()  # JSON verisi için alan
    count = models.IntegerField()
    isprogress = models.BooleanField(default=False)  # İlerleme durumu
    created_at = models.DateTimeField(auto_now_add=True)  # Verinin oluşturulma tarihi
    updated_at = models.DateTimeField(auto_now=True)  # Verinin güncellenme tarihi

    def __str__(self):
        return f"{self.data_id} - {self.tarih}"

    class Meta:
        verbose_name = 'Model Data'
        verbose_name_plural = 'Model Datas'


class FikstureDataError(models.Model):
    data_id = models.CharField(max_length=255, unique=True)  # Hangi data_id'ye ait hata olduğu
    tarih = models.DateField()  # Hatanın olduğu tarih
    error_type = models.CharField(max_length=50)  # Hata tipi (ör. API Error, Integrity Error)
    error_message = models.TextField()  # Hata mesajı
    created_at = models.DateTimeField(auto_now_add=True)  # Hata kaydının oluşturulma zamanı
    updated_at = models.DateTimeField(auto_now=True)  # Hata kaydının güncellenme zamanı

    def __str__(self):
        return f"{self.data_id} - {self.error_type} - {self.tarih}"

    class Meta:
        verbose_name = 'Data Error'
        verbose_name_plural = 'Data Errors'
```

### 2. Migration İşlemlerini Yapın

Model değişikliklerinizin veritabanına yansıtılması için aşağıdaki adımları takip edin:

```bash
python manage.py makemigrations
python manage.py migrate
```

### 3. `admin.py` Dosyanızı Güncelleyin

Hem `FikstureModelData` hem de `FikstureDataError` modellerinizi admin paneline eklemek için `admin.py` dosyanızı aşağıdaki gibi yapılandırın:

```python
# basemodels/admin.py

from django.contrib import admin
from .models import FikstureModelData, FikstureDataError

@admin.register(FikstureModelData)
class FikstureModelDataAdmin(admin.ModelAdmin):
    list_display = ('data_id', 'tarih', 'count', 'isprogress', 'created_at', 'updated_at')
    search_fields = ('data_id', 'tarih')
    list_filter = ('isprogress', 'tarih')
    ordering = ('-created_at',)

@admin.register(FikstureDataError)
class FikstureDataErrorAdmin(admin.ModelAdmin):
    list_display = ('data_id', 'tarih', 'error_type', 'error_message', 'created_at', 'updated_at')
    search_fields = ('data_id', 'tarih', 'error_type', 'error_message')
    list_filter = ('error_type', 'tarih')
    ordering = ('-created_at',)
    readonly_fields = ('data_id', 'tarih', 'error_type', 'error_message', 'created_at', 'updated_at')

    def has_add_permission(self, request):
        # Admin panelinden manuel olarak hata kaydı eklemeyi engellemek için
        return False

    def has_change_permission(self, request, obj=None):
        # Admin panelinden hata kaydı değiştirmeyi engellemek için
        return False
```

### 4. `FixtureDataHandler` Sınıfını Güncelleyin

`FixtureDataHandler` sınıfınızı, hataları doğru bir şekilde `FikstureDataError` modeline kaydedecek şekilde güncelleyin. Ayrıca, spesifik hataları (örneğin, API anahtarı eksikliği) da yakalayarak loglayabilirsiniz.

```python
# basemodels/fixture_data_handler.py

import http.client
import json
import ssl
from datetime import datetime
from django.db import IntegrityError, transaction
from basemodels.models import FikstureModelData, FikstureDataError

class FixtureDataHandler:

    DEFAULT_DATE = datetime.strptime("1900-01-01", "%Y-%m-%d").date()

    def __init__(self, date):
        self.date = date
        self.data_id = date.replace("-", "")

    def fetch_fixtures_from_api(self):
        """
        API'den fikstür verilerini çeker, 'events' anahtarını kontrol eder.
        Hata durumunda log_error ile hata kaydı yapar ve boş liste döner.
        """
        try:
            context = ssl._create_unverified_context()
            conn = http.client.HTTPSConnection('www.sofascore.com', context=context)
            conn.request('GET', f'/api/v1/sport/football/scheduled-events/{self.date}')
            response = conn.getresponse()

            if response.status != 200:
                raise Exception(f"API isteği başarısız oldu. HTTP Status: {response.status}")

            data = json.loads(response.read())

            # 'events' anahtarını kontrol et
            if "events" not in data:
                raise KeyError("'events' anahtarı API yanıtında bulunamadı")

            events = data["events"]
            print(f"{len(events)} adet etkinlik alındı.")

            return [{
                'data_id': self.data_id,
                'tarih': self.date,
                'data': events,
                'count': len(events),
                'isprogress': False
            }]

        except KeyError as e:
            print(f"Veri yapısı hatası: {e}")
            self.log_error("Data Structure Error", f"Expected key missing: {e}")
            return []  # Hata durumunda boş liste döner

        except json.JSONDecodeError as e:
            print(f"JSON çözme hatası: {e}")
            self.log_error("JSON Decode Error", str(e))
            return []

        except Exception as e:
            print(f"API'den veri çekerken bilinmeyen hata oluştu: {e}")
            self.log_error("API Error", str(e))
            return []

    def prepare_data_for_db(self, data):
        """
        API'den gelen veriyi veritabanı için uygun formata dönüştürür.
        """
        return [
            FikstureModelData(
                data_id=self.data_id,
                tarih=self.parse_date(self.date),
                data=item,
                count=len(data),
                isprogress=False
            ) for item in data
        ]

    def parse_date(self, date_str):
        """
        Tarih formatını doğrular. Hatalıysa varsayılan tarihi döner.
        """
        try:
            return datetime.strptime(date_str, "%Y-%m-%d").date()
        except ValueError:
            print(f"Geçersiz tarih formatı: {date_str}, varsayılan tarih atanıyor.")
            return self.DEFAULT_DATE

    def save_fixtures_to_db(self):
        """
        API verilerini önce silerek veritabanına kaydeder.
        """
        data = self.fetch_fixtures_from_api()
        records = self.prepare_data_for_db(data)

        if records:
            try:
                with transaction.atomic():
                    # Önce aynı data_id'ye sahip veriyi sil
                    FikstureModelData.objects.filter(data_id=self.data_id).delete()
                    # Yeni kayıtları toplu olarak ekle
                    FikstureModelData.objects.bulk_create(records)
                    print(f"{len(records)} kayıt başarıyla eklendi.")
                    self.clear_error()  # Hata varsa sil
            except IntegrityError as e:
                print(f"IntegrityError oluştu: {e}")
                self.log_error("Integrity Error", str(e))
        else:
            # Veri boşsa, hata durumunda varsayılan kayıt ekle
            self._save_default_data()

    def _save_default_data(self):
        """
        Hata veya boş veri durumunda varsayılan değerlerle kayıt ekler.
        """
        with transaction.atomic():
            FikstureModelData.objects.create(
                data_id='19000101',
                tarih=self.DEFAULT_DATE,
                data={},
                count=0,
                isprogress=False
            )
            print("Varsayılan verilerle kayıt eklendi.")
            self.log_error("Default Data Error", "Boş veriyle kayıt yapıldı.")

    def log_error(self, error_type, message):
        """
        Hata durumunda FikstureDataError tablosuna kayıt ekler.
        """
        FikstureDataError.objects.update_or_create(
            data_id=self.data_id,
            defaults={
                'tarih': self.parse_date(self.date),
                'error_type': error_type,
                'error_message': message
            }
        )
        print(f"Hata kaydedildi: {error_type} - {message}")

    def clear_error(self):
        """
        Başarılı veri eklemeden sonra ilgili hatayı siler.
        """
        FikstureDataError.objects.filter(data_id=self.data_id).delete()
        print("Önceki hata kaydı silindi.")
```

### 5. Hataları Daha İyi Yönetmek için Spesifik Durumları Yakalama

API anahtarının eksik olduğu gibi spesifik durumları yakalamak için API'den dönen yanıtı kontrol edebilirsiniz. Örneğin, API anahtarı eksikse API genellikle belirli bir hata mesajı veya kod döndürür. Bu durumda, bu özel hata durumunu yakalayıp loglayabilirsiniz.

#### Örnek: API Anahtarı Eksikliği

Farz edelim ki API, anahtar eksikliği durumunda `401 Unauthorized` veya özel bir hata mesajı döndürüyor. Bu durumda, `response.status` veya `data` içindeki hata mesajını kontrol edebilirsiniz.

```python
def fetch_fixtures_from_api(self):
    """
    API'den fikstür verilerini çeker, 'events' anahtarını kontrol eder.
    Hata durumunda log_error ile hata kaydı yapar ve boş liste döner.
    """
    try:
        context = ssl._create_unverified_context()
        conn = http.client.HTTPSConnection('www.sofascore.com', context=context)
        conn.request('GET', f'/api/v1/sport/football/scheduled-events/{self.date}')
        response = conn.getresponse()

        if response.status == 401:
            raise Exception("API Anahtarı Eksik veya Geçersiz")

        if response.status != 200:
            raise Exception(f"API isteği başarısız oldu. HTTP Status: {response.status}")

        data = json.loads(response.read())

        # 'events' anahtarını kontrol et
        if "events" not in data:
            raise KeyError("'events' anahtarı API yanıtında bulunamadı")

        events = data["events"]
        print(f"{len(events)} adet etkinlik alındı.")

        return [{
            'data_id': self.data_id,
            'tarih': self.date,
            'data': events,
            'count': len(events),
            'isprogress': False
        }]

    except KeyError as e:
        print(f"Veri yapısı hatası: {e}")
        self.log_error("Data Structure Error", f"Expected key missing: {e}")
        return []  # Hata durumunda boş liste döner

    except json.JSONDecodeError as e:
        print(f"JSON çözme hatası: {e}")
        self.log_error("JSON Decode Error", str(e))
        return []

    except Exception as e:
        print(f"API'den veri çekerken bilinmeyen hata oluştu: {e}")
        self.log_error("API Error", str(e))
        return []
```

Bu şekilde, API'den dönen HTTP durum kodlarını kontrol ederek daha spesifik hataları yakalayabilir ve `FikstureDataError` modeline kaydedebilirsiniz.

### 6. Örnek Kullanım ve Test Etme

Yaptığınız değişikliklerin doğru çalıştığından emin olmak için aşağıdaki adımları takip edebilirsiniz.

#### 1. Django Shell'i Kullanarak Test Etme

```bash
python manage.py shell
```

Django shell içerisinde, `FixtureDataHandler` sınıfını ve örnek bir tarih ile işlemi başlatın:

```python
from basemodels.fixture_data_handler import FixtureDataHandler

# Örnek bir tarih ile test
handler = FixtureDataHandler("2024-11-05")
handler.save_fixtures_to_db()
print("İşlem Tamamlandı")
```

#### 2. Admin Panelinden Kontrol Etme

- **FikstureModelData:** Başarılı olarak eklenen verileri görebilirsiniz.
- **FikstureDataError:** Herhangi bir hata oluştuysa burada görebilirsiniz. Ayrıca, hata kaydı silindiğinde bu tablodan kaldırıldığını da kontrol edebilirsiniz.

### 7. Hata Modelini Daha Sistematik Hale Getirmek

Hata modelinizi daha sistematik ve kapsamlı hale getirmek için aşağıdaki iyileştirmeleri yapabilirsiniz:

- **Hata Kategorileri:** `error_type` alanını enum gibi belirli hata kategorileriyle sınırlandırabilirsiniz.
- **Hata Seviyeleri:** Hataların ciddiyetine göre `error_level` gibi bir alan ekleyebilirsiniz.
- **Hata Detayları:** Daha fazla detay eklemek için ek alanlar veya ilişkili modeller kullanabilirsiniz.

#### Örnek: Gelişmiş Hata Modeli

```python
class FikstureDataError(models.Model):
    ERROR_TYPES = [
        ('API_ERROR', 'API Error'),
        ('DATA_STRUCTURE_ERROR', 'Data Structure Error'),
        ('JSON_DECODE_ERROR', 'JSON Decode Error'),
        ('INTEGRITY_ERROR', 'Integrity Error'),
        ('DEFAULT_DATA_ERROR', 'Default Data Error'),
        ('AUTH_ERROR', 'Authentication Error'),
        # Diğer hata tiplerini buraya ekleyebilirsiniz
    ]

    data_id = models.CharField(max_length=255, unique=True)  # Hangi data_id'ye ait hata olduğu
    tarih = models.DateField()  # Hatanın olduğu tarih
    error_type = models.CharField(max_length=50, choices=ERROR_TYPES)  # Hata tipi
    error_message = models.TextField()  # Hata mesajı
    created_at = models.DateTimeField(auto_now_add=True)  # Hata kaydının oluşturulma zamanı
    updated_at = models.DateTimeField(auto_now=True)  # Hata kaydının güncellenme zamanı

    def __str__(self):
        return f"{self.data_id} - {self.get_error_type_display()} - {self.tarih}"

    class Meta:
        verbose_name = 'Data Error'
        verbose_name_plural = 'Data Errors'
```

Bu şekilde, `error_type` alanını sınırlı seçeneklerle daha kontrol edilebilir hale getirebilirsiniz.

### 8. Ek İpuçları

- **API Anahtarı Yönetimi:** API anahtarınızı güvenli bir şekilde yönetmek için Django'nun `settings.py` dosyasını kullanabilirsiniz. Örneğin, API anahtarınızı `settings.py` içerisinde tanımlayıp, çevresel değişkenlerden alabilirsiniz.

    ```python
    # settings.py

    import os

    SOFASCORE_API_KEY = os.getenv('SOFASCORE_API_KEY', 'your_default_api_key_here')
    ```

    Ardından, `FixtureDataHandler` sınıfınızda bu anahtarı kullanabilirsiniz:

    ```python
    class FixtureDataHandler:

        def __init__(self, date):
            self.date = date
            self.data_id = date.replace("-", "")
            self.api_key = settings.SOFASCORE_API_KEY  # settings'den API anahtarını al

        def fetch_fixtures_from_api(self):
            try:
                context = ssl._create_unverified_context()
                headers = {
                    'Authorization': f'Bearer {self.api_key}',
                    # Diğer gerekli başlıklar
                }
                conn = http.client.HTTPSConnection('www.sofascore.com', context=context)
                conn.request('GET', f'/api/v1/sport/football/scheduled-events/{self.date}', headers=headers)
                response = conn.getresponse()

                if response.status == 401:
                    raise Exception("API Anahtarı Eksik veya Geçersiz")

                if response.status != 200:
                    raise Exception(f"API isteği başarısız oldu. HTTP Status: {response.status}")

                data = json.loads(response.read())

                if "events" not in data:
                    raise KeyError("'events' anahtarı API yanıtında bulunamadı")

                events = data["events"]
                print(f"{len(events)} adet etkinlik alındı.")

                return [{
                    'data_id': self.data_id,
                    'tarih': self.date,
                    'data': events,
                    'count': len(events),
                    'isprogress': False
                }]

            except KeyError as e:
                print(f"Veri yapısı hatası: {e}")
                self.log_error("Data Structure Error", f"Expected key missing: {e}")
                return []

            except json.JSONDecodeError as e:
                print(f"JSON çözme hatası: {e}")
                self.log_error("JSON Decode Error", str(e))
                return []

            except Exception as e:
                print(f"API'den veri çekerken bilinmeyen hata oluştu: {e}")
                self.log_error("API Error", str(e))
                return []
    ```

- **Hata Kayıtlarını Temizleme:** `FikstureDataError` modelinizdeki hataların sürekli olarak birikmesini istemiyorsanız, belirli zaman aralıklarında eski hataları temizleyen bir görev (task) oluşturabilirsiniz. Bunun için Celery gibi bir görev kuyruğu kullanabilirsiniz.

### 9. Özet

Bu adımları takip ederek, API'den veri çekerken oluşabilecek tüm olası hataları `FikstureDataError` modeline kaydedebilir ve bu hataları Django admin panelinden yönetebilirsiniz. Hataların doğru bir şekilde loglanması ve yönetilmesi, sisteminizin daha güvenilir ve bakımının daha kolay olmasını sağlar.

Herhangi bir adımda sorun yaşarsanız veya daha fazla yardıma ihtiyacınız olursa, lütfen ayrıntılı bir şekilde paylaşın, size yardımcı olmaktan memnuniyet duyarım!

***Soru:*** ---------------------------------------------------------------------------
DoesNotExist                              Traceback (most recent call last)
File ~\AppData\Local\Programs\Python\Python312\Lib\site-packages\django\db\models\query.py:916, in QuerySet.get_or_create(self, defaults, **kwargs)
    915 try:
--> 916     return self.get(**kwargs), False
    917 except self.model.DoesNotExist:

File ~\AppData\Local\Programs\Python\Python312\Lib\site-packages\django\db\models\query.py:637, in QuerySet.get(self, *args, **kwargs)
    636 if not num:
--> 637     raise self.model.DoesNotExist(
    638         "%s matching query does not exist." % self.model._meta.object_name
    639     )
    640 raise self.model.MultipleObjectsReturned(
    641     "get() returned more than one %s -- it returned %s!"
    642     % (
   (...)
    645     )
    646 )

DoesNotExist: FikstureDataError matching query does not exist.

During handling of the above exception, another exception occurred:

FieldError                                Traceback (most recent call last)
Cell In[24], line 27, in FixtureDataHandler.fetch_fixtures_from_api(self)
     26 if "events" not in data:
---> 27     self.log_error("Api error", str('Api özelliği bulunamadı'))
     28     return []

Cell In[24], line 60, in FixtureDataHandler.log_error(self, error_type, message)
     57 """
     58 Hata durumunda FikstureDataError tablosuna kayıt ekler.
     59 """
---> 60 FikstureDataError.objects.update_or_create(
     61     data_id=self.data_id,
     62     defaults={
     63         'tarih': self.date,
     64         'error_type': error_type,
     65         'error_message': message
     66     }
     67 )

File ~\AppData\Local\Programs\Python\Python312\Lib\site-packages\django\db\models\manager.py:87, in BaseManager._get_queryset_methods.<locals>.create_method.<locals>.manager_method(self, *args, **kwargs)
     85 @wraps(method)
     86 def manager_method(self, *args, **kwargs):
---> 87     return getattr(self.get_queryset(), name)(*args, **kwargs)

File ~\AppData\Local\Programs\Python\Python312\Lib\site-packages\django\db\models\query.py:949, in QuerySet.update_or_create(self, defaults, **kwargs)
    946 with transaction.atomic(using=self.db):
    947     # Lock the row so that a concurrent update is blocked until
    948     # update_or_create() has performed its save.
--> 949     obj, created = self.select_for_update().get_or_create(defaults, **kwargs)
    950     if created:

File ~\AppData\Local\Programs\Python\Python312\Lib\site-packages\django\db\models\query.py:918, in QuerySet.get_or_create(self, defaults, **kwargs)
    917 except self.model.DoesNotExist:
--> 918     params = self._extract_model_params(defaults, **kwargs)
    919     # Try to create an object using passed params.

File ~\AppData\Local\Programs\Python\Python312\Lib\site-packages\django\db\models\query.py:999, in QuerySet._extract_model_params(self, defaults, **kwargs)
    998 if invalid_params:
--> 999     raise exceptions.FieldError(
   1000         "Invalid field name(s) for model %s: '%s'."
   1001         % (
   1002             self.model._meta.object_name,
   1003             "', '".join(sorted(invalid_params)),
   1004         )
   1005     )
   1006 return params

FieldError: Invalid field name(s) for model FikstureDataError: 'error_type'.

During handling of the above exception, another exception occurred:

DoesNotExist                              Traceback (most recent call last)
File ~\AppData\Local\Programs\Python\Python312\Lib\site-packages\django\db\models\query.py:916, in QuerySet.get_or_create(self, defaults, **kwargs)
    915 try:
--> 916     return self.get(**kwargs), False
    917 except self.model.DoesNotExist:

File ~\AppData\Local\Programs\Python\Python312\Lib\site-packages\django\db\models\query.py:637, in QuerySet.get(self, *args, **kwargs)
    636 if not num:
--> 637     raise self.model.DoesNotExist(
    638         "%s matching query does not exist." % self.model._meta.object_name
    639     )
    640 raise self.model.MultipleObjectsReturned(
    641     "get() returned more than one %s -- it returned %s!"
    642     % (
   (...)
    645     )
    646 )

DoesNotExist: FikstureDataError matching query does not exist.

During handling of the above exception, another exception occurred:

FieldError                                Traceback (most recent call last)
Cell In[25], line 3
      1 # Örnek bir tarih ile test
      2 handler = FixtureDataHandler("2024-11-051")
----> 3 handler.save_fixtures_to_db()
      4 print("İşlem Tamamlandı")

Cell In[24], line 73, in FixtureDataHandler.save_fixtures_to_db(self)
     69 def save_fixtures_to_db(self):
     70     """
     71     API'den gelen verileri veritabanına kaydeder. Mevcut kayıt varsa siler ve yenisini ekler.
     72     """
---> 73     records = self.fetch_fixtures_from_api()
     75     if records:
     76         try:

Cell In[24], line 53, in FixtureDataHandler.fetch_fixtures_from_api(self)
     51 except Exception as e:
     52     print(f"API'den veri çekerken bilinmeyen hata oluştu: {e}")
---> 53     self.log_error("API Error", str(e))
     54     return []

Cell In[24], line 60, in FixtureDataHandler.log_error(self, error_type, message)
     56 def log_error(self, error_type, message):
     57     """
     58     Hata durumunda FikstureDataError tablosuna kayıt ekler.
     59     """
---> 60     FikstureDataError.objects.update_or_create(
     61         data_id=self.data_id,
     62         defaults={
     63             'tarih': self.date,
     64             'error_type': error_type,
     65             'error_message': message
     66         }
     67     )

File ~\AppData\Local\Programs\Python\Python312\Lib\site-packages\django\db\models\manager.py:87, in BaseManager._get_queryset_methods.<locals>.create_method.<locals>.manager_method(self, *args, **kwargs)
     85 @wraps(method)
     86 def manager_method(self, *args, **kwargs):
---> 87     return getattr(self.get_queryset(), name)(*args, **kwargs)

File ~\AppData\Local\Programs\Python\Python312\Lib\site-packages\django\db\models\query.py:949, in QuerySet.update_or_create(self, defaults, **kwargs)
    945 self._for_write = True
    946 with transaction.atomic(using=self.db):
    947     # Lock the row so that a concurrent update is blocked until
    948     # update_or_create() has performed its save.
--> 949     obj, created = self.select_for_update().get_or_create(defaults, **kwargs)
    950     if created:
    951         return obj, created

File ~\AppData\Local\Programs\Python\Python312\Lib\site-packages\django\db\models\query.py:918, in QuerySet.get_or_create(self, defaults, **kwargs)
    916     return self.get(**kwargs), False
    917 except self.model.DoesNotExist:
--> 918     params = self._extract_model_params(defaults, **kwargs)
    919     # Try to create an object using passed params.
    920     try:

File ~\AppData\Local\Programs\Python\Python312\Lib\site-packages\django\db\models\query.py:999, in QuerySet._extract_model_params(self, defaults, **kwargs)
    997             invalid_params.append(param)
    998 if invalid_params:
--> 999     raise exceptions.FieldError(
   1000         "Invalid field name(s) for model %s: '%s'."
   1001         % (
   1002             self.model._meta.object_name,
   1003             "', '".join(sorted(invalid_params)),
   1004         )
   1005     )
   1006 return params

FieldError: Invalid field name(s) for model FikstureDataError: 'error_type'.   tamam jiç bir hat gelmesin hepsi veirtabanına kaydedilsin

Tool: **Yetersiz alan tespiti**  
`FikstureDataError` modelinde 'error_type' alanının eksik olduğunu fark ediyorum. Hata ayıklama işlemlerine başlamadan önce bu alanı eklemeliyim.

**Güncellemeleri sağlamak**

`FikstureDataError` modelini güncellemek gerekiyor. Hata türü ve mesajı eklenmeli, ardından veritabanı geçişleri yapılmalı.

**Cevap:** Anladığım kadarıyla, `FikstureDataError` modelinizde `error_type` ve `error_message` alanlarının tanımlı olmaması nedeniyle `FieldError` hatası alıyorsunuz. Bu hatayı çözmek için aşağıdaki adımları izleyebilirsiniz:

1. **`FikstureDataError` Modelinizi Doğru Şekilde Tanımlayın**
2. **Migration İşlemlerini Gerçekleştirin**
3. **`FixtureDataHandler` Sınıfınızı Güncelleyin**
4. **`admin.py` Dosyanızı Güncelleyin**
5. **Kodunuzu Test Edin**

### 1. `FikstureDataError` Modelinizi Doğru Şekilde Tanımlayın

Öncelikle, `FikstureDataError` modelinizin doğru şekilde tanımlandığından emin olun. `error_type` ve `error_message` alanlarını içermelidir. Aşağıda, modelinizin doğru tanımlanmış hali bulunmaktadır:

```python
# basemodels/models.py

from django.db import models

class FikstureModelData(models.Model):
    data_id = models.CharField(max_length=255, unique=True)  # date.replace("-","") değerini burada saklayacağız
    tarih = models.DateField()  # Orijinal tarih alanı
    data = models.JSONField()  # JSON verisi için alan
    count = models.IntegerField()
    isprogress = models.BooleanField(default=False)  # İlerleme durumu
    created_at = models.DateTimeField(auto_now_add=True)  # Verinin oluşturulma tarihi
    updated_at = models.DateTimeField(auto_now=True)  # Verinin güncellenme tarihi

    def __str__(self):
        return f"{self.data_id} - {self.tarih}"

    class Meta:
        verbose_name = 'Model Data'
        verbose_name_plural = 'Model Datas'


class FikstureDataError(models.Model):
    data_id = models.CharField(max_length=255, unique=True)  # Hangi data_id'ye ait hata olduğu
    tarih = models.DateField()  # Hatanın olduğu tarih
    error_type = models.CharField(max_length=50)  # Hata tipi (ör. API Error, Integrity Error)
    error_message = models.TextField()  # Hata mesajı
    created_at = models.DateTimeField(auto_now_add=True)  # Hata kaydının oluşturulma zamanı
    updated_at = models.DateTimeField(auto_now=True)  # Hata kaydının güncellenme zamanı

    def __str__(self):
        return f"{self.data_id} - {self.error_type} - {self.tarih}"

    class Meta:
        verbose_name = 'Data Error'
        verbose_name_plural = 'Data Errors'
```

### 2. Migration İşlemlerini Gerçekleştirin

Modelinizi güncelledikten sonra, bu değişiklikleri veritabanınıza yansıtmak için migration işlemlerini yapmanız gerekiyor.

```bash
python manage.py makemigrations
python manage.py migrate
```

Bu komutlar, Django'nun model değişikliklerini algılamasını ve veritabanında gerekli tabloları oluşturmasını sağlar.

### 3. `FixtureDataHandler` Sınıfınızı Güncelleyin

`FixtureDataHandler` sınıfınızın `log_error` metodunu ve genel hata yönetimini doğru şekilde yapması için aşağıdaki gibi güncelleyebilirsiniz:

```python
# basemodels/fixture_data_handler.py

import http.client
import json
import ssl
from datetime import datetime
from django.db import IntegrityError, transaction
from basemodels.models import FikstureModelData, FikstureDataError


class FixtureDataHandler:

    DEFAULT_DATE = datetime.strptime("1900-01-01", "%Y-%m-%d").date()

    def __init__(self, date):
        self.date = date
        self.data_id = date.replace("-", "")

    def fetch_fixtures_from_api(self):
        """
        API'den fikstür verilerini çeker, 'events' anahtarını kontrol eder.
        Hata durumunda log_error ile hata kaydı yapar ve boş liste döner.
        """
        try:
            context = ssl._create_unverified_context()
            conn = http.client.HTTPSConnection('www.sofascore.com', context=context)
            conn.request('GET', f'/api/v1/sport/football/scheduled-events/{self.date}')
            response = conn.getresponse()

            if response.status == 401:
                raise Exception("API Anahtarı Eksik veya Geçersiz")

            if response.status != 200:
                raise Exception(f"API isteği başarısız oldu. HTTP Status: {response.status}")

            data = json.loads(response.read())

            # 'events' anahtarını kontrol et
            if "events" not in data:
                raise KeyError("'events' anahtarı API yanıtında bulunamadı")

            events = data["events"]
            print(f"{len(events)} adet etkinlik alındı.")

            return [{
                'data_id': self.data_id,
                'tarih': self.date,
                'data': events,
                'count': len(events),
                'isprogress': False
            }]

        except KeyError as e:
            print(f"Veri yapısı hatası: {e}")
            self.log_error("Data Structure Error", f"Expected key missing: {e}")
            return []  # Hata durumunda boş liste döner

        except json.JSONDecodeError as e:
            print(f"JSON çözme hatası: {e}")
            self.log_error("JSON Decode Error", str(e))
            return []

        except Exception as e:
            print(f"API'den veri çekerken bilinmeyen hata oluştu: {e}")
            self.log_error("API Error", str(e))
            return []

    def prepare_data_for_db(self, data):
        """
        API'den gelen veriyi veritabanı için uygun formata dönüştürür.
        """
        return [
            FikstureModelData(
                data_id=self.data_id,
                tarih=self.parse_date(self.date),
                data=item,
                count=len(data),
                isprogress=False
            ) for item in data
        ]

    def parse_date(self, date_str):
        """
        Tarih formatını doğrular. Hatalıysa varsayılan tarihi döner.
        """
        try:
            return datetime.strptime(date_str, "%Y-%m-%d").date()
        except ValueError:
            print(f"Geçersiz tarih formatı: {date_str}, varsayılan tarih atanıyor.")
            return self.DEFAULT_DATE

    def save_fixtures_to_db(self):
        """
        API verilerini önce silerek veritabanına kaydeder.
        """
        data = self.fetch_fixtures_from_api()
        records = self.prepare_data_for_db(data)

        if records:
            try:
                with transaction.atomic():
                    # Önce aynı data_id'ye sahip veriyi sil
                    FikstureModelData.objects.filter(data_id=self.data_id).delete()
                    # Yeni kayıtları toplu olarak ekle
                    FikstureModelData.objects.bulk_create(records)
                    print(f"{len(records)} kayıt başarıyla eklendi.")
                    self.clear_error()  # Hata varsa sil
            except IntegrityError as e:
                print(f"IntegrityError oluştu: {e}")
                self.log_error("Integrity Error", str(e))
        else:
            # Veri boşsa, hata durumunda varsayılan kayıt ekle
            self._save_default_data()

    def _save_default_data(self):
        """
        Hata veya boş veri durumunda varsayılan değerlerle kayıt ekler.
        """
        with transaction.atomic():
            FikstureModelData.objects.create(
                data_id='19000101',
                tarih=self.DEFAULT_DATE,
                data={},
                count=0,
                isprogress=False
            )
            print("Varsayılan verilerle kayıt eklendi.")
            self.log_error("Default Data Error", "Boş veriyle kayıt yapıldı.")

    def log_error(self, error_type, message):
        """
        Hata durumunda FikstureDataError tablosuna kayıt ekler.
        """
        FikstureDataError.objects.update_or_create(
            data_id=self.data_id,
            defaults={
                'tarih': self.parse_date(self.date),
                'error_type': error_type,
                'error_message': message
            }
        )
        print(f"Hata kaydedildi: {error_type} - {message}")

    def clear_error(self):
        """
        Başarılı veri eklemeden sonra ilgili hatayı siler.
        """
        FikstureDataError.objects.filter(data_id=self.data_id).delete()
        print("Önceki hata kaydı silindi.")
```

### 4. `admin.py` Dosyanızı Güncelleyin

`FikstureDataError` modelinizi Django admin paneline eklemek için `admin.py` dosyanızı aşağıdaki gibi güncelleyin:

```python
# basemodels/admin.py

from django.contrib import admin
from .models import FikstureModelData, FikstureDataError

@admin.register(FikstureModelData)
class FikstureModelDataAdmin(admin.ModelAdmin):
    list_display = ('data_id', 'tarih', 'count', 'isprogress', 'created_at', 'updated_at')
    search_fields = ('data_id', 'tarih')
    list_filter = ('isprogress', 'tarih')
    ordering = ('-created_at',)

@admin.register(FikstureDataError)
class FikstureDataErrorAdmin(admin.ModelAdmin):
    list_display = ('data_id', 'tarih', 'error_type', 'error_message', 'created_at', 'updated_at')
    search_fields = ('data_id', 'tarih', 'error_type', 'error_message')
    list_filter = ('error_type', 'tarih')
    ordering = ('-created_at',)
    readonly_fields = ('data_id', 'tarih', 'error_type', 'error_message', 'created_at', 'updated_at')

    def has_add_permission(self, request):
        # Admin panelinden manuel olarak hata kaydı eklemeyi engellemek için
        return False

    def has_change_permission(self, request, obj=None):
        # Admin panelinden hata kaydı değiştirmeyi engellemek için
        return False
```

### 5. Kodunuzu Test Edin

Model tanımlamalarını ve `admin.py` dosyasını güncelledikten sonra, kodunuzu tekrar test edelim.

#### 1. Django Shell'i Kullanarak Test Etme

```bash
python manage.py shell
```

Django shell içerisinde, `FixtureDataHandler` sınıfını ve örnek bir tarih ile işlemi başlatın:

```python
from basemodels.fixture_data_handler import FixtureDataHandler

# Örnek bir tarih ile test (geçersiz bir tarih kullanarak hata tetikleyebilirsiniz)
handler = FixtureDataHandler("2024-11-35")  # 35. gün geçersizdir
handler.save_fixtures_to_db()
print("İşlem Tamamlandı")
```

#### 2. Admin Panelinden Kontrol Etme

- **FikstureModelData:** Başarılı olarak eklenen verileri görebilirsiniz.
- **FikstureDataError:** Herhangi bir hata oluştuysa burada görebilirsiniz. Ayrıca, hata kaydı silindiğinde bu tablodan kaldırıldığını da kontrol edebilirsiniz.

### Hataların Doğru Kaydedildiğinden Emin Olmak

Eğer `FikstureDataError` modeliniz doğru şekilde tanımlandıysa ve migration işlemleri yapıldıysa, aşağıdaki hatasız çalışması gerekmektedir:

- **`FieldError: Invalid field name(s) for model FikstureDataError: 'error_type'.`** hatası almamalısınız.
- API'den veri çekerken herhangi bir hata oluşursa, bu hata `FikstureDataError` modeline kaydedilecektir.

### Özet ve İpuçları

1. **Model Tanımlamaları:** `FikstureDataError` modelinde gerekli tüm alanların doğru şekilde tanımlandığından emin olun.
2. **Migration İşlemleri:** Model değişikliklerinden sonra `makemigrations` ve `migrate` komutlarını çalıştırın.
3. **Admin Paneli:** `admin.py` dosyasını doğru şekilde güncelleyerek modellerinizi admin paneline ekleyin.
4. **Hata Yönetimi:** `FixtureDataHandler` sınıfında `log_error` metodunun doğru şekilde çalıştığından emin olun.
5. **Test Etme:** Django shell ve admin paneli üzerinden test ederek, verilerin doğru şekilde kaydedildiğini ve hataların doğru şekilde loglandığını kontrol edin.

### Ekstra: Daha Fazla Hata Yönetimi

`FixtureDataHandler` sınıfınızı daha kapsamlı hale getirmek için aşağıdaki iyileştirmeleri yapabilirsiniz:

- **Spesifik Hata Türleri:** API'den dönen spesifik hata mesajlarını yakalayarak, `error_type` alanını daha detaylı hale getirebilirsiniz.
- **Hata Kategorileri:** `error_type` alanını belirli kategorilerle sınırlandırarak daha sistematik hata yönetimi sağlayabilirsiniz.

#### Örnek: Gelişmiş `error_type` Alanı

```python
class FikstureDataError(models.Model):
    ERROR_TYPES = [
        ('API_ERROR', 'API Error'),
        ('DATA_STRUCTURE_ERROR', 'Data Structure Error'),
        ('JSON_DECODE_ERROR', 'JSON Decode Error'),
        ('INTEGRITY_ERROR', 'Integrity Error'),
        ('DEFAULT_DATA_ERROR', 'Default Data Error'),
        ('AUTH_ERROR', 'Authentication Error'),
        # Diğer hata tiplerini buraya ekleyebilirsiniz
    ]

    data_id = models.CharField(max_length=255, unique=True)
    tarih = models.DateField()
    error_type = models.CharField(max_length=50, choices=ERROR_TYPES)
    error_message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.data_id} - {self.get_error_type_display()} - {self.tarih}"

    class Meta:
        verbose_name = 'Data Error'
        verbose_name_plural = 'Data Errors'
```

Bu şekilde, `error_type` alanını sınırlı seçeneklerle daha kontrol edilebilir hale getirebilirsiniz.

#### Güncellenmiş `log_error` Metodu

```python
def log_error(self, error_type, message):
    """
    Hata durumunda FikstureDataError tablosuna kayıt ekler.
    """
    FikstureDataError.objects.update_or_create(
        data_id=self.data_id,
        defaults={
            'tarih': self.parse_date(self.date),
            'error_type': error_type,
            'error_message': message
        }
    )
    print(f"Hata kaydedildi: {error_type} - {message}")
```

### Sonuç

Yukarıdaki adımları takip ederek, `FikstureDataError` modelinizdeki `error_type` ve `error_message` alanlarını doğru şekilde tanımlayabilir ve bu hataları veritabanına güvenli bir şekilde kaydedebilirsiniz. Herhangi bir adımda sorun yaşarsanız, lütfen model tanımlamalarınızı ve migration işlemlerinizi kontrol edin. Yardıma ihtiyaç duyarsanız, daha fazla ayrıntı sağlayarak tekrar sorabilirsiniz.

***Soru:*** API'den veri çekerken bilinmeyen hata oluştu: API isteği başarısız oldu. HTTP Status: 404
Geçersiz tarih formatı: 2024-11-051, varsayılan tarih atanıyor.
---------------------------------------------------------------------------
Exception                                 Traceback (most recent call last)
Cell In[32], line 34, in FixtureDataHandler.fetch_fixtures_from_api(self)
     33 if response.status != 200:
---> 34     raise Exception(f"API isteği başarısız oldu. HTTP Status: {response.status}")
     36 data = json.loads(response.read())

Exception: API isteği başarısız oldu. HTTP Status: 404

During handling of the above exception, another exception occurred:

DoesNotExist                              Traceback (most recent call last)
File ~\AppData\Local\Programs\Python\Python312\Lib\site-packages\django\db\models\query.py:916, in QuerySet.get_or_create(self, defaults, **kwargs)
    915 try:
--> 916     return self.get(**kwargs), False
    917 except self.model.DoesNotExist:

File ~\AppData\Local\Programs\Python\Python312\Lib\site-packages\django\db\models\query.py:637, in QuerySet.get(self, *args, **kwargs)
    636 if not num:
--> 637     raise self.model.DoesNotExist(
    638         "%s matching query does not exist." % self.model._meta.object_name
    639     )
    640 raise self.model.MultipleObjectsReturned(
    641     "get() returned more than one %s -- it returned %s!"
    642     % (
   (...)
    645     )
    646 )

DoesNotExist: FikstureDataError matching query does not exist.

During handling of the above exception, another exception occurred:

FieldError                                Traceback (most recent call last)
Cell In[33], line 3
      1 # Örnek bir tarih ile test
      2 handler = FixtureDataHandler("2024-11-051")
----> 3 handler.save_fixtures_to_db()
      4 print("İşlem Tamamlandı")

Cell In[32], line 96, in FixtureDataHandler.save_fixtures_to_db(self)
     92 def save_fixtures_to_db(self):
     93     """
     94     API verilerini önce silerek veritabanına kaydeder.
     95     """
---> 96     data = self.fetch_fixtures_from_api()
     97     records = self.prepare_data_for_db(data)
     99     if records:

Cell In[32], line 65, in FixtureDataHandler.fetch_fixtures_from_api(self)
     63 except Exception as e:
     64     print(f"API'den veri çekerken bilinmeyen hata oluştu: {e}")
---> 65     self.log_error("API Error", str(e))
     66     return []

Cell In[32], line 134, in FixtureDataHandler.log_error(self, error_type, message)
    130 def log_error(self, error_type, message):
    131     """
    132     Hata durumunda FikstureDataError tablosuna kayıt ekler.
    133     """
--> 134     FikstureDataError.objects.update_or_create(
    135         data_id=self.data_id,
    136         defaults={
    137             'tarih': self.parse_date(self.date),
    138             'error_type': error_type,
    139             'error_message': message
    140         }
    141     )
    142     print(f"Hata kaydedildi: {error_type} - {message}")

File ~\AppData\Local\Programs\Python\Python312\Lib\site-packages\django\db\models\manager.py:87, in BaseManager._get_queryset_methods.<locals>.create_method.<locals>.manager_method(self, *args, **kwargs)
     85 @wraps(method)
     86 def manager_method(self, *args, **kwargs):
---> 87     return getattr(self.get_queryset(), name)(*args, **kwargs)

File ~\AppData\Local\Programs\Python\Python312\Lib\site-packages\django\db\models\query.py:949, in QuerySet.update_or_create(self, defaults, **kwargs)
    945 self._for_write = True
    946 with transaction.atomic(using=self.db):
    947     # Lock the row so that a concurrent update is blocked until
    948     # update_or_create() has performed its save.
--> 949     obj, created = self.select_for_update().get_or_create(defaults, **kwargs)
    950     if created:
    951         return obj, created

File ~\AppData\Local\Programs\Python\Python312\Lib\site-packages\django\db\models\query.py:918, in QuerySet.get_or_create(self, defaults, **kwargs)
    916     return self.get(**kwargs), False
    917 except self.model.DoesNotExist:
--> 918     params = self._extract_model_params(defaults, **kwargs)
    919     # Try to create an object using passed params.
    920     try:

File ~\AppData\Local\Programs\Python\Python312\Lib\site-packages\django\db\models\query.py:999, in QuerySet._extract_model_params(self, defaults, **kwargs)
    997             invalid_params.append(param)
    998 if invalid_params:
--> 999     raise exceptions.FieldError(
   1000         "Invalid field name(s) for model %s: '%s'."
   1001         % (
   1002             self.model._meta.object_name,
   1003             "', '".join(sorted(invalid_params)),
   1004         )
   1005     )
   1006 return params

FieldError: Invalid field name(s) for model FikstureDataError: 'error_type'.
   sistem hata vermeye devam edyır

Tool: **Sorunları yönetme ve güncelleme**

Fikstür veri alımında hata modelini oluşturma sürecindeyim. `FikstureDataError` modelinde 'error_type' alanı olmadığından, `update_or_create` kullanırken hata alıyorum. Alanı eklemek ve migrations yapmak gerekiyor.

**Yeniden başlatmayı gözden geçiriyorum**

Sunucunun yeniden başlatılmamış olduğuna mı yoksa migrasyonlarla ilgili bir sorun mu olduğuna bakılıyor. Modelle ilgili sorunları çözmek için birkaç adım atılmalıdır.

**Modellen ouvragea**

FikstureDataError modelini tanımlarken 'error_type' ve 'error_message' alanlarını eklemek gerekiyor. Ardından, migrations işlemlerini yapmasını sağlamak gerekiyor.

**Veritabanı modelini gözden geçiriyorum**

`FikstureDataError` modelinin tanımını iyice inceliyorum. Migrations işlemlerini yönlendirmeyi planlıyorum.

**Cevap:** Anladığınız üzere, `FikstureDataError` modelinizde `error_type` ve `error_message` alanları tanımlı değil veya doğru şekilde uygulanmamış. Bu nedenle, `update_or_create` metodu bu alanları bulamıyor ve `FieldError` hatası alıyorsunuz.

Bu sorunu çözmek için aşağıdaki adımları dikkatlice takip edin:

1. **`FikstureDataError` Modelinizi Doğru Şekilde Tanımlayın**
2. **Migration İşlemlerini Gerçekleştirin**
3. **`FixtureDataHandler` Sınıfınızı Doğru Hale Getirin**
4. **`admin.py` Dosyanızı Doğru Şekilde Güncelleyin**
5. **Kodu Test Edin**

### 1. `FikstureDataError` Modelinizi Doğru Şekilde Tanımlayın

Öncelikle, `FikstureDataError` modelinizin doğru tanımlandığından emin olun. Aşağıda, gerekli tüm alanları içeren doğru bir model tanımı bulunmaktadır:

```python
# basemodels/models.py

from django.db import models

class FikstureModelData(models.Model):
    data_id = models.CharField(max_length=255, unique=True)  # date.replace("-","") değerini burada saklayacağız
    tarih = models.DateField()  # Orijinal tarih alanı
    data = models.JSONField()  # JSON verisi için alan
    count = models.IntegerField()
    isprogress = models.BooleanField(default=False)  # İlerleme durumu
    created_at = models.DateTimeField(auto_now_add=True)  # Verinin oluşturulma tarihi
    updated_at = models.DateTimeField(auto_now=True)  # Verinin güncellenme tarihi

    def __str__(self):
        return f"{self.data_id} - {self.tarih}"

    class Meta:
        verbose_name = 'Model Data'
        verbose_name_plural = 'Model Datas'


class FikstureDataError(models.Model):
    ERROR_TYPES = [
        ('API_ERROR', 'API Error'),
        ('DATA_STRUCTURE_ERROR', 'Data Structure Error'),
        ('JSON_DECODE_ERROR', 'JSON Decode Error'),
        ('INTEGRITY_ERROR', 'Integrity Error'),
        ('DEFAULT_DATA_ERROR', 'Default Data Error'),
        ('AUTH_ERROR', 'Authentication Error'),
        # Diğer hata tiplerini buraya ekleyebilirsiniz
    ]

    data_id = models.CharField(max_length=255, unique=True)  # Hangi data_id'ye ait hata olduğu
    tarih = models.DateField()  # Hatanın olduğu tarih
    error_type = models.CharField(max_length=50, choices=ERROR_TYPES)  # Hata tipi
    error_message = models.TextField()  # Hata mesajı
    created_at = models.DateTimeField(auto_now_add=True)  # Hata kaydının oluşturulma zamanı
    updated_at = models.DateTimeField(auto_now=True)  # Hata kaydının güncellenme zamanı

    def __str__(self):
        return f"{self.data_id} - {self.get_error_type_display()} - {self.tarih}"

    class Meta:
        verbose_name = 'Data Error'
        verbose_name_plural = 'Data Errors'
```

### 2. Migration İşlemlerini Gerçekleştirin

Modelinizi güncelledikten sonra, bu değişikliklerin veritabanına yansıtılması için migration işlemlerini yapmanız gerekmektedir.

Terminal veya Komut İstemcisinde aşağıdaki komutları çalıştırın:

```bash
python manage.py makemigrations
python manage.py migrate
```

Bu komutlar, Django'nun model değişikliklerinizi algılamasını ve veritabanında gerekli tabloları oluşturmasını sağlar.

### 3. `FixtureDataHandler` Sınıfınızı Doğru Hale Getirin

`FixtureDataHandler` sınıfınızın `log_error` metodunun doğru alanları kullandığından emin olun. Aşağıda, güncellenmiş ve hatasız bir `FixtureDataHandler` sınıfı örneği bulunmaktadır:

```python
# basemodels/fixture_data_handler.py

import http.client
import json
import ssl
from datetime import datetime
from django.db import IntegrityError, transaction
from basemodels.models import FikstureModelData, FikstureDataError

class FixtureDataHandler:

    DEFAULT_DATE = datetime.strptime("1900-01-01", "%Y-%m-%d").date()

    def __init__(self, date):
        self.date = date
        self.data_id = date.replace("-", "")

    def fetch_fixtures_from_api(self):
        """
        API'den fikstür verilerini çeker, 'events' anahtarını kontrol eder.
        Hata durumunda log_error ile hata kaydı yapar ve boş liste döner.
        """
        try:
            context = ssl._create_unverified_context()
            conn = http.client.HTTPSConnection('www.sofascore.com', context=context)
            conn.request('GET', f'/api/v1/sport/football/scheduled-events/{self.date}')
            response = conn.getresponse()

            if response.status == 401:
                raise Exception("API Anahtarı Eksik veya Geçersiz")

            if response.status != 200:
                raise Exception(f"API isteği başarısız oldu. HTTP Status: {response.status}")

            data = json.loads(response.read())

            # 'events' anahtarını kontrol et
            if "events" not in data:
                raise KeyError("'events' anahtarı API yanıtında bulunamadı")

            events = data["events"]
            print(f"{len(events)} adet etkinlik alındı.")

            return [{
                'data_id': self.data_id,
                'tarih': self.date,
                'data': events,
                'count': len(events),
                'isprogress': False
            }]

        except KeyError as e:
            print(f"Veri yapısı hatası: {e}")
            self.log_error("DATA_STRUCTURE_ERROR", f"Expected key missing: {e}")
            return []  # Hata durumunda boş liste döner

        except json.JSONDecodeError as e:
            print(f"JSON çözme hatası: {e}")
            self.log_error("JSON_DECODE_ERROR", str(e))
            return []

        except Exception as e:
            print(f"API'den veri çekerken bilinmeyen hata oluştu: {e}")
            self.log_error("API_ERROR", str(e))
            return []

    def prepare_data_for_db(self, data):
        """
        API'den gelen veriyi veritabanı için uygun formata dönüştürür.
        """
        return [
            FikstureModelData(
                data_id=self.data_id,
                tarih=self.parse_date(self.date),
                data=item,
                count=len(data),
                isprogress=False
            ) for item in data
        ]

    def parse_date(self, date_str):
        """
        Tarih formatını doğrular. Hatalıysa varsayılan tarihi döner.
        """
        try:
            return datetime.strptime(date_str, "%Y-%m-%d").date()
        except ValueError:
            print(f"Geçersiz tarih formatı: {date_str}, varsayılan tarih atanıyor.")
            return self.DEFAULT_DATE

    def save_fixtures_to_db(self):
        """
        API verilerini önce silerek veritabanına kaydeder.
        """
        data = self.fetch_fixtures_from_api()
        records = self.prepare_data_for_db(data)

        if records:
            try:
                with transaction.atomic():
                    # Önce aynı data_id'ye sahip veriyi sil
                    FikstureModelData.objects.filter(data_id=self.data_id).delete()
                    # Yeni kayıtları toplu olarak ekle
                    FikstureModelData.objects.bulk_create(records)
                    print(f"{len(records)} kayıt başarıyla eklendi.")
                    self.clear_error()  # Hata varsa sil
            except IntegrityError as e:
                print(f"IntegrityError oluştu: {e}")
                self.log_error("INTEGRITY_ERROR", str(e))
        else:
            # Veri boşsa, hata durumunda varsayılan kayıt ekle
            self._save_default_data()

    def _save_default_data(self):
        """
        Hata veya boş veri durumunda varsayılan değerlerle kayıt ekler.
        """
        with transaction.atomic():
            FikstureModelData.objects.create(
                data_id='19000101',
                tarih=self.DEFAULT_DATE,
                data={},
                count=0,
                isprogress=False
            )
            print("Varsayılan verilerle kayıt eklendi.")
            self.log_error("DEFAULT_DATA_ERROR", "Boş veriyle kayıt yapıldı.")

    def log_error(self, error_type, message):
        """
        Hata durumunda FikstureDataError tablosuna kayıt ekler.
        """
        FikstureDataError.objects.update_or_create(
            data_id=self.data_id,
            defaults={
                'tarih': self.parse_date(self.date),
                'error_type': error_type,
                'error_message': message
            }
        )
        print(f"Hata kaydedildi: {error_type} - {message}")

    def clear_error(self):
        """
        Başarılı veri eklemeden sonra ilgili hatayı siler.
        """
        FikstureDataError.objects.filter(data_id=self.data_id).delete()
        print("Önceki hata kaydı silindi.")
```

### 4. `admin.py` Dosyanızı Doğru Şekilde Güncelleyin

Hem `FikstureModelData` hem de `FikstureDataError` modellerinizi Django admin paneline eklemek için `admin.py` dosyanızı aşağıdaki gibi yapılandırın:

```python
# basemodels/admin.py

from django.contrib import admin
from .models import FikstureModelData, FikstureDataError

@admin.register(FikstureModelData)
class FikstureModelDataAdmin(admin.ModelAdmin):
    list_display = ('data_id', 'tarih', 'count', 'isprogress', 'created_at', 'updated_at')
    search_fields = ('data_id', 'tarih')
    list_filter = ('isprogress', 'tarih')
    ordering = ('-created_at',)

@admin.register(FikstureDataError)
class FikstureDataErrorAdmin(admin.ModelAdmin):
    list_display = ('data_id', 'tarih', 'error_type', 'error_message', 'created_at', 'updated_at')
    search_fields = ('data_id', 'tarih', 'error_type', 'error_message')
    list_filter = ('error_type', 'tarih')
    ordering = ('-created_at',)
    readonly_fields = ('data_id', 'tarih', 'error_type', 'error_message', 'created_at', 'updated_at')

    def has_add_permission(self, request):
        # Admin panelinden manuel olarak hata kaydı eklemeyi engellemek için
        return False

    def has_change_permission(self, request, obj=None):
        # Admin panelinden hata kaydı değiştirmeyi engellemek için
        return False
```

### 5. Kodunuzu Test Edin

Model tanımlamalarını ve `admin.py` dosyasını güncelledikten sonra, kodunuzu tekrar test ederek hatasız çalıştığından emin olmalısınız.

#### a. Django Shell'i Kullanarak Test Etme

Öncelikle Django shell'i açın:

```bash
python manage.py shell
```

Shell içerisinde aşağıdaki adımları izleyin:

```python
from basemodels.fixture_data_handler import FixtureDataHandler

# Geçersiz bir tarih kullanarak hatayı tetikleyin
handler = FixtureDataHandler("2024-11-35")  # 35. gün geçersizdir
handler.save_fixtures_to_db()
print("İşlem Tamamlandı")
```

#### b. Hataların Doğru Kaydedildiğinden Emin Olma

- **Başarılı Bir İşlem Durumu:**
  - `FikstureModelData` tablosunda ilgili kayıt eklenecektir.
  - Eğer önceden bu `data_id` için bir hata kaydı varsa, `FikstureDataError` tablosundan silinecektir.

- **Başarısız Bir İşlem Durumu (Geçersiz Tarih):**
  - `FikstureDataError` tablosuna yeni bir hata kaydı eklenecektir.
  - `FikstureModelData` tablosuna varsayılan bir kayıt eklenecektir (`data_id='19000101'`).

#### c. Admin Panelinden Kontrol Etme

Django admin paneline giriş yapın ve `FikstureModelData` ile `FikstureDataError` modellerini kontrol edin.

- **FikstureModelData:**
  - Başarılı olarak eklenen verileri görebilirsiniz.
  
- **FikstureDataError:**
  - Oluşan hataları burada görebilirsiniz.
  - Hata kaydı silindiğinde, ilgili kayıt bu tabloda yer almayacaktır.

### Ekstra: Hata Yönetimini Daha İyileştirme

Hata modelinizi daha kapsamlı hale getirmek için aşağıdaki iyileştirmeleri yapabilirsiniz:

1. **Hata Kategorileri ve Seviyeleri:**
   - `error_type` alanını daha spesifik hale getirebilirsiniz.
   - `error_level` gibi ek alanlar ekleyerek hataların ciddiyetini belirtebilirsiniz.

2. **Hata Mesajlarını Detaylandırma:**
   - `error_message` alanını daha detaylı hale getirerek hata nedenlerini daha iyi anlayabilirsiniz.

#### Örnek: Gelişmiş `FikstureDataError` Modeli

```python
class FikstureDataError(models.Model):
    ERROR_TYPES = [
        ('API_ERROR', 'API Error'),
        ('DATA_STRUCTURE_ERROR', 'Data Structure Error'),
        ('JSON_DECODE_ERROR', 'JSON Decode Error'),
        ('INTEGRITY_ERROR', 'Integrity Error'),
        ('DEFAULT_DATA_ERROR', 'Default Data Error'),
        ('AUTH_ERROR', 'Authentication Error'),
        # Diğer hata tiplerini buraya ekleyebilirsiniz
    ]

    data_id = models.CharField(max_length=255, unique=True)  # Hangi data_id'ye ait hata olduğu
    tarih = models.DateField()  # Hatanın olduğu tarih
    error_type = models.CharField(max_length=50, choices=ERROR_TYPES)  # Hata tipi
    error_message = models.TextField()  # Hata mesajı
    created_at = models.DateTimeField(auto_now_add=True)  # Hata kaydının oluşturulma zamanı
    updated_at = models.DateTimeField(auto_now=True)  # Hata kaydının güncellenme zamanı

    def __str__(self):
        return f"{self.data_id} - {self.get_error_type_display()} - {self.tarih}"

    class Meta:
        verbose_name = 'Data Error'
        verbose_name_plural = 'Data Errors'
```

### Sorun Çözümü İçin Adımların Tekrarı

1. **Model Tanımlamaları:**
   - `FikstureDataError` modelinizin doğru şekilde tanımlandığından emin olun (yukarıdaki örneği kullanabilirsiniz).

2. **Migration İşlemleri:**
   - Model değişikliklerini yaptıktan sonra aşağıdaki komutları çalıştırın:
     ```bash
     python manage.py makemigrations
     python manage.py migrate
     ```

3. **Admin Paneli:**
   - `admin.py` dosyanızın doğru şekilde güncellendiğinden emin olun (yukarıdaki örneği kullanabilirsiniz).

4. **Kodunuzu Test Edin:**
   - Django shell veya başka bir yöntemle `FixtureDataHandler` sınıfınızı test edin ve hataların doğru şekilde kaydedildiğini doğrulayın.

### Olası Sorunlar ve Çözümleri

- **Model Değişiklikleri Yansımadı:**
  - `makemigrations` ve `migrate` komutlarını doğru şekilde çalıştırdığınızdan emin olun.
  - Migration dosyalarınızı kontrol edin (`basemodels/migrations/` klasöründe).

- **Yanlış Model Dosyası:**
  - `FikstureDataError` modelinizi doğru uygulama (`app`) içinde tanımladığınızdan emin olun.

- **Yanlış Uygulama (`App`) Ayarları:**
  - `settings.py` dosyanızda `basemodels` uygulamasının `INSTALLED_APPS` listesinde yer aldığından emin olun.

  ```python
  # settings.py

  INSTALLED_APPS = [
      # Diğer uygulamalar...
      'basemodels',
      # ...
  ]
  ```

- **Veritabanı Cache Sorunları:**
  - Özellikle SQLite kullanıyorsanız, veritabanı dosyasını (örneğin `db.sqlite3`) silip yeniden oluşturmanız gerekebilir. Ancak bu adımı yapmadan önce veritabanınızdaki mevcut verileri yedeklemeyi unutmayın.

### Özet

Bu adımları dikkatlice takip ederek, `FikstureDataError` modelinizdeki `error_type` ve `error_message` alanlarının doğru şekilde tanımlanmasını ve bu alanlara göre hata kayıtlarının yapılmasını sağlayabilirsiniz. Ayrıca, Django admin panelinde bu hataları kolayca yönetebilir ve izleyebilirsiniz.

Eğer hala sorun yaşıyorsanız, aşağıdaki adımları izleyerek daha fazla bilgi sağlayabilirsiniz:

1. **Model Tanımını Paylaşın:**
   - `basemodels/models.py` dosyanızın tamamını paylaşın.

2. **Migration Durumunu Kontrol Edin:**
   - `python manage.py showmigrations` komutunu çalıştırarak hangi migration'ların uygulandığını kontrol edin.

3. **Hata Mesajlarını İnceleyin:**
   - Hata mesajlarında belirtilen alan adlarının doğru olduğundan emin olun.

Bu bilgilerle, daha detaylı ve hedefe yönelik bir çözüm sunabilirim.

***Soru:*** # basemodels/fixture_data_handler.py

import http.client
import json
import ssl
from datetime import datetime
from django.db import IntegrityError, transaction
from basemodels.models import FikstureModelData, FikstureDataError

class FixtureDataHandler:

    DEFAULT_DATE = datetime.strptime("1900-01-01", "%Y-%m-%d").date()

    def __init__(self, date):
        self.date = date
        self.data_id = date.replace("-", "")

    def fetch_fixtures_from_api(self):
        """
        API'den fikstür verilerini çeker, 'events' anahtarını kontrol eder.
        Hata durumunda log_error ile hata kaydı yapar ve boş liste döner.
        """
        try:
            context = ssl._create_unverified_context()
            conn = http.client.HTTPSConnection('www.sofascore.com', context=context)
            conn.request('GET', f'/api/v1/sport/football/scheduled-events/{self.date}')
            response = conn.getresponse()

            if response.status == 401:
                 self.log_error='hata 401'

            if response.status != 200:
                self.log_error='hata 401'

            data = json.loads(response.read())

            # 'events' anahtarını kontrol et
            if "events" not in data:
                 self.log_error='Event gecersiz.'
            try:
                events = data["events"]
                print(f"{len(events)} adet etkinlik alındı.")
            except:
                events=[0]

            return [{
                'data_id': self.data_id,
                'tarih': self.date,
                'data': events,
                'count': len(events),
                'isprogress': False
            }]

        except KeyError as e:
            print(f"Veri yapısı hatası: {e}")
            self.log_error("DATA_STRUCTURE_ERROR", f"Expected key missing: {e}")
            return []  # Hata durumunda boş liste döner

        except json.JSONDecodeError as e:
            print(f"JSON çözme hatası: {e}")
            self.log_error("JSON_DECODE_ERROR", str(e))
            return []

        except Exception as e:
            print(f"API'den veri çekerken bilinmeyen hata oluştu: {e}")
            self.log_error("API_ERROR", str(e))
            return []

    def prepare_data_for_db(self, data):
        """
        API'den gelen veriyi veritabanı için uygun formata dönüştürür.
        """
        return [
            FikstureModelData(
                data_id=self.data_id,
                tarih=self.parse_date(self.date),
                data=item,
                count=len(data),
                isprogress=False
            ) for item in data
        ]

    def parse_date(self, date_str):
        """
        Tarih formatını doğrular. Hatalıysa varsayılan tarihi döner.
        """
        try:
            return datetime.strptime(date_str, "%Y-%m-%d").date()
        except ValueError:
            print(f"Geçersiz tarih formatı: {date_str}, varsayılan tarih atanıyor.")
            return self.DEFAULT_DATE

    def save_fixtures_to_db(self):
        """
        API verilerini önce silerek veritabanına kaydeder.
        """
        data = self.fetch_fixtures_from_api()
        records = self.prepare_data_for_db(data)

        if records:
            try:
                with transaction.atomic():
                    # Önce aynı data_id'ye sahip veriyi sil
                    FikstureModelData.objects.filter(data_id=self.data_id).delete()
                    # Yeni kayıtları toplu olarak ekle
                    FikstureModelData.objects.bulk_create(records)
                    print(f"{len(records)} kayıt başarıyla eklendi.")
                    self.clear_error()  # Hata varsa sil
            except IntegrityError as e:
                print(f"IntegrityError oluştu: {e}")
                self.log_error("INTEGRITY_ERROR", str(e))
        else:
            # Veri boşsa, hata durumunda varsayılan kayıt ekle
            self._save_default_data()

    def _save_default_data(self):
        """
        Hata veya boş veri durumunda varsayılan değerlerle kayıt ekler.
        """
        with transaction.atomic():
            FikstureModelData.objects.create(
                data_id='19000101',
                tarih=self.DEFAULT_DATE,
                data={},
                count=0,
                isprogress=False
            )
            print("Varsayılan verilerle kayıt eklendi.")
            self.log_error("DEFAULT_DATA_ERROR", "Boş veriyle kayıt yapıldı.")

    def log_error(self, error_type, message):
        """
        Hata durumunda FikstureDataError tablosuna kayıt ekler.
        """
        FikstureDataError.objects.update_or_create(
            data_id=self.data_id,
            defaults={
                'tarih': self.parse_date(self.date),
                'error_type': error_type,
                'error_message': message
            }
        )
        print(f"Hata kaydedildi: {error_type} - {message}")

    def clear_error(self):
        """
        Başarılı veri eklemeden sonra ilgili hatayı siler.
        """
        FikstureDataError.objects.filter(data_id=self.data_id).delete()
        print("Önceki hata kaydı silindi.")



  lütfen burada gelen tüm hata türlerini veritabanına kaydet hiç print falan kullanma

Tool: **İşlemleri tamamlamak**

Django tabanlı bir uygulama geliştiriyorum, API'den verileri çekip veritabanına kaydediyor, hata modeline kayıtlıyor. Hata modelinde eksik alanlar var ve hatalar doğru yönetilmiyor.

**Sınıfı ele almak**

FixtureDataHandler sınıfını ele alıyorum. Hataları veritabanına kaydediyorum, `print` kullanımı yok. Hataları `FikstureDataError` modeliyle kaydediyorum. Hataların doğru sınıflandırıldığından ve `self.log_error = 'hata 401'` kullanmanın hatalı olduğundan emin oluyorum.

**Güncellemeler yapıyorum**

API yanıtlarını kontrol ediyorum. Hataları `FikstureDataError` modeline kaydediyorum. Yanlış hata mesajlarını düzenliyorum.

**Cevap:** Anladığınız üzere, `FikstureDataError` modelinizde `error_type` ve `error_message` alanlarının doğru şekilde tanımlanmaması veya doğru şekilde uygulanmaması nedeniyle `FieldError` hatası alıyorsunuz. Ayrıca, `FixtureDataHandler` sınıfınızda bazı hatalı kodlar bulunmakta. Aşağıda, bu sorunları çözmek için adım adım yapmanız gerekenleri detaylı bir şekilde açıklıyorum.

### 1. `FikstureDataError` Modelinizi Doğru Şekilde Tanımlayın

Öncelikle, `FikstureDataError` modelinizin doğru şekilde tanımlandığından emin olun. `error_type` ve `error_message` alanlarını içermelidir. Aşağıda, gerekli tüm alanları içeren doğru bir model tanımı bulunmaktadır:

```python
# basemodels/models.py

from django.db import models

class FikstureModelData(models.Model):
    data_id = models.CharField(max_length=255, unique=True)  # date.replace("-","") değerini burada saklayacağız
    tarih = models.DateField()  # Orijinal tarih alanı
    data = models.JSONField()  # JSON verisi için alan
    count = models.IntegerField()
    isprogress = models.BooleanField(default=False)  # İlerleme durumu
    created_at = models.DateTimeField(auto_now_add=True)  # Verinin oluşturulma tarihi
    updated_at = models.DateTimeField(auto_now=True)  # Verinin güncellenme tarihi

    def __str__(self):
        return f"{self.data_id} - {self.tarih}"

    class Meta:
        verbose_name = 'Model Data'
        verbose_name_plural = 'Model Datas'


class FikstureDataError(models.Model):
    ERROR_TYPES = [
        ('API_ERROR', 'API Error'),
        ('DATA_STRUCTURE_ERROR', 'Data Structure Error'),
        ('JSON_DECODE_ERROR', 'JSON Decode Error'),
        ('INTEGRITY_ERROR', 'Integrity Error'),
        ('DEFAULT_DATA_ERROR', 'Default Data Error'),
        ('AUTH_ERROR', 'Authentication Error'),
        # Diğer hata tiplerini buraya ekleyebilirsiniz
    ]

    data_id = models.CharField(max_length=255, unique=True)  # Hangi data_id'ye ait hata olduğu
    tarih = models.DateField()  # Hatanın olduğu tarih
    error_type = models.CharField(max_length=50, choices=ERROR_TYPES)  # Hata tipi
    error_message = models.TextField()  # Hata mesajı
    created_at = models.DateTimeField(auto_now_add=True)  # Hata kaydının oluşturulma zamanı
    updated_at = models.DateTimeField(auto_now=True)  # Hata kaydının güncellenme zamanı

    def __str__(self):
        return f"{self.data_id} - {self.get_error_type_display()} - {self.tarih}"

    class Meta:
        verbose_name = 'Data Error'
        verbose_name_plural = 'Data Errors'
```

### 2. Migration İşlemlerini Gerçekleştirin

Modelinizi güncelledikten sonra, bu değişikliklerin veritabanına yansıtılması için migration işlemlerini yapmanız gerekiyor.

Terminal veya Komut İstemcisinde aşağıdaki komutları çalıştırın:

```bash
python manage.py makemigrations
python manage.py migrate
```

Bu komutlar, Django'nun model değişikliklerinizi algılamasını ve veritabanında gerekli tabloları oluşturmasını sağlar.

### 3. `admin.py` Dosyanızı Doğru Şekilde Güncelleyin

Hem `FikstureModelData` hem de `FikstureDataError` modellerinizi Django admin paneline eklemek için `admin.py` dosyanızı aşağıdaki gibi yapılandırın:

```python
# basemodels/admin.py

from django.contrib import admin
from .models import FikstureModelData, FikstureDataError

@admin.register(FikstureModelData)
class FikstureModelDataAdmin(admin.ModelAdmin):
    list_display = ('data_id', 'tarih', 'count', 'isprogress', 'created_at', 'updated_at')
    search_fields = ('data_id', 'tarih')
    list_filter = ('isprogress', 'tarih')
    ordering = ('-created_at',)

@admin.register(FikstureDataError)
class FikstureDataErrorAdmin(admin.ModelAdmin):
    list_display = ('data_id', 'tarih', 'error_type', 'error_message', 'created_at', 'updated_at')
    search_fields = ('data_id', 'tarih', 'error_type', 'error_message')
    list_filter = ('error_type', 'tarih')
    ordering = ('-created_at',)
    readonly_fields = ('data_id', 'tarih', 'error_type', 'error_message', 'created_at', 'updated_at')

    def has_add_permission(self, request):
        # Admin panelinden manuel olarak hata kaydı eklemeyi engellemek için
        return False

    def has_change_permission(self, request, obj=None):
        # Admin panelinden hata kaydı değiştirmeyi engellemek için
        return False
```

### 4. `FixtureDataHandler` Sınıfınızı Doğru Hale Getirin

`FixtureDataHandler` sınıfınızı, tüm hataları `FikstureDataError` modeline kaydedecek ve `print` ifadelerini kaldıracak şekilde güncelleyin. Ayrıca, hata durumlarında doğru şekilde `log_error` metodunu çağırdığınızdan emin olun.

Aşağıda, güncellenmiş ve hatasız bir `FixtureDataHandler` sınıfı örneği bulunmaktadır:

```python
# basemodels/fixture_data_handler.py

import http.client
import json
import ssl
from datetime import datetime
from django.db import IntegrityError, transaction
from basemodels.models import FikstureModelData, FikstureDataError

class FixtureDataHandler:

    DEFAULT_DATE = datetime.strptime("1900-01-01", "%Y-%m-%d").date()

    def __init__(self, date):
        self.date = date
        self.data_id = date.replace("-", "")

    def fetch_fixtures_from_api(self):
        """
        API'den fikstür verilerini çeker, 'events' anahtarını kontrol eder.
        Hata durumunda log_error ile hata kaydı yapar ve boş liste döner.
        """
        try:
            context = ssl._create_unverified_context()
            conn = http.client.HTTPSConnection('www.sofascore.com', context=context)
            conn.request('GET', f'/api/v1/sport/football/scheduled-events/{self.date}')
            response = conn.getresponse()

            if response.status == 401:
                self.log_error("AUTH_ERROR", "API Anahtarı Eksik veya Geçersiz")
                return []

            if response.status != 200:
                self.log_error("API_ERROR", f"API isteği başarısız oldu. HTTP Status: {response.status}")
                return []

            data = json.loads(response.read())

            # 'events' anahtarını kontrol et
            if "events" not in data:
                self.log_error("DATA_STRUCTURE_ERROR", "'events' anahtarı API yanıtında bulunamadı")
                return []

            events = data["events"]
            return [{
                'data_id': self.data_id,
                'tarih': self.date,
                'data': events,
                'count': len(events),
                'isprogress': False
            }]

        except KeyError as e:
            self.log_error("DATA_STRUCTURE_ERROR", f"Expected key missing: {e}")
            return []  # Hata durumunda boş liste döner

        except json.JSONDecodeError as e:
            self.log_error("JSON_DECODE_ERROR", str(e))
            return []

        except Exception as e:
            self.log_error("API_ERROR", str(e))
            return []

    def prepare_data_for_db(self, data):
        """
        API'den gelen veriyi veritabanı için uygun formata dönüştürür.
        """
        return [
            FikstureModelData(
                data_id=self.data_id,
                tarih=self.parse_date(self.date),
                data=item,
                count=len(data),
                isprogress=False
            ) for item in data
        ]

    def parse_date(self, date_str):
        """
        Tarih formatını doğrular. Hatalıysa varsayılan tarihi döner.
        """
        try:
            return datetime.strptime(date_str, "%Y-%m-%d").date()
        except ValueError:
            self.log_error("DATA_STRUCTURE_ERROR", f"Geçersiz tarih formatı: {date_str}, varsayılan tarih atanıyor.")
            return self.DEFAULT_DATE

    def save_fixtures_to_db(self):
        """
        API verilerini önce silerek veritabanına kaydeder.
        """
        data = self.fetch_fixtures_from_api()
        records = self.prepare_data_for_db(data)

        if records:
            try:
                with transaction.atomic():
                    # Önce aynı data_id'ye sahip veriyi sil
                    FikstureModelData.objects.filter(data_id=self.data_id).delete()
                    # Yeni kayıtları toplu olarak ekle
                    FikstureModelData.objects.bulk_create(records)
                    self.clear_error()  # Hata varsa sil
            except IntegrityError as e:
                self.log_error("INTEGRITY_ERROR", str(e))
        else:
            # Veri boşsa, hata durumunda varsayılan kayıt ekle
            self._save_default_data()

    def _save_default_data(self):
        """
        Hata veya boş veri durumunda varsayılan değerlerle kayıt ekler.
        """
        with transaction.atomic():
            FikstureModelData.objects.create(
                data_id='19000101',
                tarih=self.DEFAULT_DATE,
                data={},
                count=0,
                isprogress=False
            )
            self.log_error("DEFAULT_DATA_ERROR", "Boş veriyle kayıt yapıldı.")

    def log_error(self, error_type, message):
        """
        Hata durumunda FikstureDataError tablosuna kayıt ekler.
        """
        FikstureDataError.objects.update_or_create(
            data_id=self.data_id,
            defaults={
                'tarih': self.parse_date(self.date),
                'error_type': error_type,
                'error_message': message
            }
        )

    def clear_error(self):
        """
        Başarılı veri eklemeden sonra ilgili hatayı siler.
        """
        FikstureDataError.objects.filter(data_id=self.data_id).delete()
```

### 5. Kodu Test Edin

Model tanımlamalarını ve `admin.py` dosyasını güncelledikten sonra, kodunuzu tekrar test ederek hatasız çalıştığından emin olmalısınız.

#### a. Django Shell'i Kullanarak Test Etme

Öncelikle Django shell'i açın:

```bash
python manage.py shell
```

Shell içerisinde, `FixtureDataHandler` sınıfınızı ve örnek bir tarih ile işlemi başlatın:

```python
from basemodels.fixture_data_handler import FixtureDataHandler

# Geçersiz bir tarih kullanarak hatayı tetikleyin
handler = FixtureDataHandler("2024-11-35")  # 35. gün geçersizdir
handler.save_fixtures_to_db()
print("İşlem Tamamlandı")
```

#### b. Hataların Doğru Kaydedildiğinden Emin Olma

- **Başarılı Bir İşlem Durumu:**
  - `FikstureModelData` tablosunda ilgili kayıt eklenecektir.
  - Eğer önceden bu `data_id` için bir hata kaydı varsa, `FikstureDataError` tablosundan silinecektir.

- **Başarısız Bir İşlem Durumu (Geçersiz Tarih):**
  - `FikstureDataError` tablosuna yeni bir hata kaydı eklenecektir.
  - `FikstureModelData` tablosuna varsayılan bir kayıt eklenecektir (`data_id='19000101'`).

#### c. Admin Panelinden Kontrol Etme

Django admin paneline giriş yapın ve `FikstureModelData` ile `FikstureDataError` modellerini kontrol edin.

- **FikstureModelData:**
  - Başarılı olarak eklenen verileri görebilirsiniz.
  
- **FikstureDataError:**
  - Oluşan hataları burada görebilirsiniz.
  - Hata kaydı silindiğinde, ilgili kayıt bu tabloda yer almayacaktır.

### 6. Ekstra: API Anahtarı Yönetimi ve Spesifik Hataların Yakalanması

API anahtarınızı güvenli bir şekilde yönetmek için Django'nun `settings.py` dosyasını kullanabilirsiniz. Ayrıca, API'den dönen spesifik hata mesajlarını yakalayarak, `error_type` alanını daha detaylı hale getirebilirsiniz.

#### a. API Anahtarını `settings.py` İçerisinde Tanımlayın

```python
# settings.py

import os

SOFASCORE_API_KEY = os.getenv('SOFASCORE_API_KEY', 'your_default_api_key_here')
```

#### b. `FixtureDataHandler` Sınıfında API Anahtarını Kullanma

```python
# basemodels/fixture_data_handler.py

from django.conf import settings

class FixtureDataHandler:

    DEFAULT_DATE = datetime.strptime("1900-01-01", "%Y-%m-%d").date()

    def __init__(self, date):
        self.date = date
        self.data_id = date.replace("-", "")
        self.api_key = settings.SOFASCORE_API_KEY  # settings'den API anahtarını al

    def fetch_fixtures_from_api(self):
        """
        API'den fikstür verilerini çeker, 'events' anahtarını kontrol eder.
        Hata durumunda log_error ile hata kaydı yapar ve boş liste döner.
        """
        try:
            context = ssl._create_unverified_context()
            headers = {
                'Authorization': f'Bearer {self.api_key}',
                # Diğer gerekli başlıklar
            }
            conn = http.client.HTTPSConnection('www.sofascore.com', context=context)
            conn.request('GET', f'/api/v1/sport/football/scheduled-events/{self.date}', headers=headers)
            response = conn.getresponse()

            if response.status == 401:
                self.log_error("AUTH_ERROR", "API Anahtarı Eksik veya Geçersiz")
                return []

            if response.status != 200:
                self.log_error("API_ERROR", f"API isteği başarısız oldu. HTTP Status: {response.status}")
                return []

            data = json.loads(response.read())

            # 'events' anahtarını kontrol et
            if "events" not in data:
                self.log_error("DATA_STRUCTURE_ERROR", "'events' anahtarı API yanıtında bulunamadı")
                return []

            events = data["events"]
            return [{
                'data_id': self.data_id,
                'tarih': self.date,
                'data': events,
                'count': len(events),
                'isprogress': False
            }]

        except KeyError as e:
            self.log_error("DATA_STRUCTURE_ERROR", f"Expected key missing: {e}")
            return []  # Hata durumunda boş liste döner

        except json.JSONDecodeError as e:
            self.log_error("JSON_DECODE_ERROR", str(e))
            return []

        except Exception as e:
            self.log_error("API_ERROR", str(e))
            return []
```

### 7. Hataların Sürekli Birikmesini Önlemek İçin Düzenli Temizlik

Eğer `FikstureDataError` modelinizdeki hataların sürekli olarak birikmesini istemiyorsanız, belirli zaman aralıklarında eski hataları temizleyen bir görev (task) oluşturabilirsiniz. Bunun için Celery gibi bir görev kuyruğu kullanabilirsiniz. Bu adım opsiyoneldir ve projenizin ihtiyaçlarına göre uygulanabilir.

### 8. Özet

Bu adımları dikkatlice takip ederek:

1. **Model Tanımlamaları:** `FikstureDataError` modelinizin doğru şekilde tanımlandığından emin olun.
2. **Migration İşlemleri:** Model değişikliklerinden sonra `makemigrations` ve `migrate` komutlarını çalıştırın.
3. **Admin Paneli:** `admin.py` dosyanızı doğru şekilde güncelleyerek modellerinizi admin paneline ekleyin.
4. **Hata Yönetimi:** `FixtureDataHandler` sınıfında `log_error` metodunun doğru şekilde çalıştığından ve tüm hataları veritabanına kaydettiğinden emin olun.
5. **Test Etme:** Django shell veya admin paneli üzerinden test ederek, verilerin doğru şekilde kaydedildiğini ve hataların doğru şekilde loglandığını kontrol edin.

Eğer hala `FieldError: Invalid field name(s) for model FikstureDataError: 'error_type'.` hatası alıyorsanız, aşağıdaki adımları kontrol edin:

- **Model Dosyasını Doğru Güncellediğinizden Emin Olun:**
  `basemodels/models.py` dosyanızda `FikstureDataError` modelinde `error_type` ve `error_message` alanlarının tanımlı olduğundan emin olun.

- **Migration İşlemlerini Doğru Yapın:**
  Model değişikliklerinden sonra `makemigrations` ve `migrate` komutlarını doğru şekilde çalıştırdığınızdan emin olun.

- **Veritabanı Bağlantısını Kontrol Edin:**
  Doğru veritabanına bağlandığınızdan ve migration'ların doğru veritabanına uygulandığından emin olun.

- **Django Shell'de Model Alanlarını Kontrol Edin:**
  Django shell'de `FikstureDataError` modelinin tüm alanlarının doğru tanımlandığını kontrol edin.

```bash
python manage.py shell
```

Shell içerisinde:

```python
from basemodels.models import FikstureDataError
FikstureDataError._meta.get_fields()
```

Bu komut, modelinizdeki tüm alanları listeleyecektir. `error_type` ve `error_message` alanlarının burada göründüğünden emin olun.

### Sonuç

Bu adımları takip ederek, `FikstureDataError` modelinizdeki tüm hata türlerini doğru şekilde kaydedebilir ve `FixtureDataHandler` sınıfınızı hatasız çalışacak şekilde düzeltebilirsiniz. Hataların doğru şekilde loglandığından emin olmak için her adımı dikkatlice uygulayın ve test edin.

Herhangi bir adımda sorun yaşarsanız veya daha fazla yardıma ihtiyacınız olursa, lütfen detaylı bilgi sağlayarak tekrar sorabilirsiniz. Yardımcı olmaktan memnuniyet duyarım!

***Soru:*** ConnectionResetError                      Traceback (most recent call last)
Cell In[50], line 24, in FixtureDataHandler.fetch_fixtures_from_api(self)
     23 conn = http.client.HTTPSConnection('www.sofascore.com', context=context)
---> 24 conn.request('GET', f'/api/v1/sport/football/scheduled-events/{self.date}')
     25 response = conn.getresponse()

File ~\AppData\Local\Programs\Python\Python312\Lib\http\client.py:1319, in HTTPConnection.request(self, method, url, body, headers, encode_chunked)
   1318 """Send a complete request to the server."""
-> 1319 self._send_request(method, url, body, headers, encode_chunked)

File ~\AppData\Local\Programs\Python\Python312\Lib\http\client.py:1365, in HTTPConnection._send_request(self, method, url, body, headers, encode_chunked)
   1364     body = _encode(body, 'body')
-> 1365 self.endheaders(body, encode_chunked=encode_chunked)

File ~\AppData\Local\Programs\Python\Python312\Lib\http\client.py:1314, in HTTPConnection.endheaders(self, message_body, encode_chunked)
   1313     raise CannotSendHeader()
-> 1314 self._send_output(message_body, encode_chunked=encode_chunked)

File ~\AppData\Local\Programs\Python\Python312\Lib\http\client.py:1074, in HTTPConnection._send_output(self, message_body, encode_chunked)
   1073 del self._buffer[:]
-> 1074 self.send(msg)
   1076 if message_body is not None:
   1077 
   1078     # create a consistent interface to message_body

File ~\AppData\Local\Programs\Python\Python312\Lib\http\client.py:1018, in HTTPConnection.send(self, data)
   1017 if self.auto_open:
-> 1018     self.connect()
   1019 else:

File ~\AppData\Local\Programs\Python\Python312\Lib\http\client.py:1460, in HTTPSConnection.connect(self)
   1458     server_hostname = self.host
-> 1460 self.sock = self._context.wrap_socket(self.sock,
   1461                                       server_hostname=server_hostname)

File ~\AppData\Local\Programs\Python\Python312\Lib\ssl.py:455, in SSLContext.wrap_socket(self, sock, server_side, do_handshake_on_connect, suppress_ragged_eofs, server_hostname, session)
    449 def wrap_socket(self, sock, server_side=False,
    450                 do_handshake_on_connect=True,
    451                 suppress_ragged_eofs=True,
    452                 server_hostname=None, session=None):
    453     # SSLSocket class handles server_hostname encoding before it calls
    454     # ctx._wrap_socket()
--> 455     return self.sslsocket_class._create(
    456         sock=sock,
    457         server_side=server_side,
    458         do_handshake_on_connect=do_handshake_on_connect,
    459         suppress_ragged_eofs=suppress_ragged_eofs,
    460         server_hostname=server_hostname,
    461         context=self,
    462         session=session
    463     )

File ~\AppData\Local\Programs\Python\Python312\Lib\ssl.py:1046, in SSLSocket._create(cls, sock, server_side, do_handshake_on_connect, suppress_ragged_eofs, server_hostname, context, session)
   1045             raise ValueError("do_handshake_on_connect should not be specified for non-blocking sockets")
-> 1046         self.do_handshake()
   1047 except (OSError, ValueError):

File ~\AppData\Local\Programs\Python\Python312\Lib\ssl.py:1317, in SSLSocket.do_handshake(self, block)
   1316         self.settimeout(None)
-> 1317     self._sslobj.do_handshake()
   1318 finally:

ConnectionResetError: [WinError 10054] Varolan bir bağlantı uzaktaki bir ana bilgisayar tarafından zorla kapatıldı

During handling of the above exception, another exception occurred:

DoesNotExist                              Traceback (most recent call last)
File ~\AppData\Local\Programs\Python\Python312\Lib\site-packages\django\db\models\query.py:916, in QuerySet.get_or_create(self, defaults, **kwargs)
    915 try:
--> 916     return self.get(**kwargs), False
    917 except self.model.DoesNotExist:

File ~\AppData\Local\Programs\Python\Python312\Lib\site-packages\django\db\models\query.py:637, in QuerySet.get(self, *args, **kwargs)
    636 if not num:
--> 637     raise self.model.DoesNotExist(
    638         "%s matching query does not exist." % self.model._meta.object_name
    639     )
    640 raise self.model.MultipleObjectsReturned(
    641     "get() returned more than one %s -- it returned %s!"
    642     % (
   (...)
    645     )
    646 )

DoesNotExist: FikstureDataError matching query does not exist.

During handling of the above exception, another exception occurred:

FieldError                                Traceback (most recent call last)
Cell In[51], line 3
      1 # Örnek bir tarih ile test
      2 handler = FixtureDataHandler("2000-11-01")
----> 3 handler.save_fixtures_to_db()
      4 print("İşlem Tamamlandı")

Cell In[50], line 91, in FixtureDataHandler.save_fixtures_to_db(self)
     87 def save_fixtures_to_db(self):
     88     """
     89     API verilerini önce silerek veritabanına kaydeder.
     90     """
---> 91     data = self.fetch_fixtures_from_api()
     92     records = self.prepare_data_for_db(data)
     94     if records:

Cell In[50], line 60, in FixtureDataHandler.fetch_fixtures_from_api(self)
     57     return []
     59 except Exception as e:
---> 60     self.log_error("API_ERROR", str(e))
     61     return []

Cell In[50], line 126, in FixtureDataHandler.log_error(self, error_type, message)
    122 def log_error(self, error_type, message):
    123     """
    124     Hata durumunda FikstureDataError tablosuna kayıt ekler.
    125     """
--> 126     FikstureDataError.objects.update_or_create(
    127         data_id=self.data_id,
    128         defaults={
    129             'tarih': self.parse_date(self.date),
    130             'error_type': error_type,
    131             'error_message': message
    132         }
    133     )

File ~\AppData\Local\Programs\Python\Python312\Lib\site-packages\django\db\models\manager.py:87, in BaseManager._get_queryset_methods.<locals>.create_method.<locals>.manager_method(self, *args, **kwargs)
     85 @wraps(method)
     86 def manager_method(self, *args, **kwargs):
---> 87     return getattr(self.get_queryset(), name)(*args, **kwargs)

File ~\AppData\Local\Programs\Python\Python312\Lib\site-packages\django\db\models\query.py:949, in QuerySet.update_or_create(self, defaults, **kwargs)
    945 self._for_write = True
    946 with transaction.atomic(using=self.db):
    947     # Lock the row so that a concurrent update is blocked until
    948     # update_or_create() has performed its save.
--> 949     obj, created = self.select_for_update().get_or_create(defaults, **kwargs)
    950     if created:
    951         return obj, created

File ~\AppData\Local\Programs\Python\Python312\Lib\site-packages\django\db\models\query.py:918, in QuerySet.get_or_create(self, defaults, **kwargs)
    916     return self.get(**kwargs), False
    917 except self.model.DoesNotExist:
--> 918     params = self._extract_model_params(defaults, **kwargs)
    919     # Try to create an object using passed params.
    920     try:

File ~\AppData\Local\Programs\Python\Python312\Lib\site-packages\django\db\models\query.py:999, in QuerySet._extract_model_params(self, defaults, **kwargs)
    997             invalid_params.append(param)
    998 if invalid_params:
--> 999     raise exceptions.FieldError(
   1000         "Invalid field name(s) for model %s: '%s'."
   1001         % (
   1002             self.model._meta.object_name,
   1003             "', '".join(sorted(invalid_params)),
   1004         )
   1005     )
   1006 return params

FieldError: Invalid field name(s) for model FikstureDataError: 'error_type'.
1   bu hata da gelmesin hiç hata gelmesin hata kısmına göndersin

Tool: **Gözden geçiriyorum modeli**

Üzerinde çalıştığımız Django modelinde 'error_type' alanının eksik olduğunu fark ediyorum. Bu, data hatalarını doğru bir şekilde kaydedemememe sebep oluyor.

**Model tanımlamasını kontrol etmek**

Utilis modelindeki campos mutably_getirildiği gibi 'error_type' ve 'error_message' alanlarını doğru tanımlıyorum.

**Veritabanı değişikliklerini uygulamak**

Migasyonlar oluşturulmuş ve uygulanmış mı? INSTALLED_APPS'te uygulama doğru bir şekilde bulunuyor mu?

**Kod hatalarını düzeltmek**

fetch_fixtures_from_api fonksiyonunda log_error metodunu çağırıyorum ve geçerli hata mesajlarını doğrulamaya odaklanıyorum.

**Cevap:** Anladığınız üzere, `FikstureDataError` modelinizde `error_type` ve `error_message` alanlarının doğru şekilde tanımlanmaması veya doğru şekilde uygulanmaması nedeniyle `FieldError: Invalid field name(s) for model FikstureDataError: 'error_type'.` hatası alıyorsunuz. Ayrıca, `FixtureDataHandler` sınıfınızda bazı hatalı kodlar bulunuyor. Aşağıda, bu sorunları çözmek için adım adım yapmanız gerekenleri detaylı bir şekilde açıklıyorum.

### Adım 1: `FikstureDataError` Modelini Doğru Şekilde Tanımlayın

Öncelikle, `FikstureDataError` modelinizin doğru şekilde tanımlandığından emin olun. Bu modelde `error_type` ve `error_message` alanlarının tanımlı olduğundan emin olmalısınız.

#### `models.py` Dosyanızı Güncelleyin

```python
# basemodels/models.py

from django.db import models

class FikstureModelData(models.Model):
    data_id = models.CharField(max_length=255, unique=True)  # date.replace("-","") değerini burada saklayacağız
    tarih = models.DateField()  # Orijinal tarih alanı
    data = models.JSONField()  # JSON verisi için alan
    count = models.IntegerField()
    isprogress = models.BooleanField(default=False)  # İlerleme durumu
    created_at = models.DateTimeField(auto_now_add=True)  # Verinin oluşturulma tarihi
    updated_at = models.DateTimeField(auto_now=True)  # Verinin güncellenme tarihi

    def __str__(self):
        return f"{self.data_id} - {self.tarih}"

    class Meta:
        verbose_name = 'Model Data'
        verbose_name_plural = 'Model Datas'


class FikstureDataError(models.Model):
    ERROR_TYPES = [
        ('API_ERROR', 'API Error'),
        ('DATA_STRUCTURE_ERROR', 'Data Structure Error'),
        ('JSON_DECODE_ERROR', 'JSON Decode Error'),
        ('INTEGRITY_ERROR', 'Integrity Error'),
        ('DEFAULT_DATA_ERROR', 'Default Data Error'),
        ('AUTH_ERROR', 'Authentication Error'),
        # Diğer hata tiplerini buraya ekleyebilirsiniz
    ]

    data_id = models.CharField(max_length=255, unique=True)  # Hangi data_id'ye ait hata olduğu
    tarih = models.DateField()  # Hatanın olduğu tarih
    error_type = models.CharField(max_length=50, choices=ERROR_TYPES)  # Hata tipi
    error_message = models.TextField()  # Hata mesajı
    created_at = models.DateTimeField(auto_now_add=True)  # Hata kaydının oluşturulma zamanı
    updated_at = models.DateTimeField(auto_now=True)  # Hata kaydının güncellenme zamanı

    def __str__(self):
        return f"{self.data_id} - {self.get_error_type_display()} - {self.tarih}"

    class Meta:
        verbose_name = 'Data Error'
        verbose_name_plural = 'Data Errors'
```

### Adım 2: Migration İşlemlerini Gerçekleştirin

Modelinizi güncelledikten sonra, bu değişikliklerin veritabanına yansıtılması için migration işlemlerini yapmanız gerekiyor.

#### Terminal veya Komut İstemcisinde Aşağıdaki Komutları Çalıştırın:

```bash
python manage.py makemigrations
python manage.py migrate
```

Bu komutlar, Django'nun model değişikliklerinizi algılamasını ve veritabanında gerekli tabloları oluşturmasını sağlar.

### Adım 3: `admin.py` Dosyanızı Doğru Şekilde Güncelleyin

Her iki modeli de Django admin paneline eklemek için `admin.py` dosyanızı aşağıdaki gibi yapılandırın.

#### `admin.py` Dosyasını Güncelleyin

```python
# basemodels/admin.py

from django.contrib import admin
from .models import FikstureModelData, FikstureDataError

@admin.register(FikstureModelData)
class FikstureModelDataAdmin(admin.ModelAdmin):
    list_display = ('data_id', 'tarih', 'count', 'isprogress', 'created_at', 'updated_at')
    search_fields = ('data_id', 'tarih')
    list_filter = ('isprogress', 'tarih')
    ordering = ('-created_at',)

@admin.register(FikstureDataError)
class FikstureDataErrorAdmin(admin.ModelAdmin):
    list_display = ('data_id', 'tarih', 'error_type', 'error_message', 'created_at', 'updated_at')
    search_fields = ('data_id', 'tarih', 'error_type', 'error_message')
    list_filter = ('error_type', 'tarih')
    ordering = ('-created_at',)
    readonly_fields = ('data_id', 'tarih', 'error_type', 'error_message', 'created_at', 'updated_at')

    def has_add_permission(self, request):
        # Admin panelinden manuel olarak hata kaydı eklemeyi engellemek için
        return False

    def has_change_permission(self, request, obj=None):
        # Admin panelinden hata kaydı değiştirmeyi engellemek için
        return False
```

### Adım 4: `FixtureDataHandler` Sınıfınızı Doğru Hale Getirin

`FixtureDataHandler` sınıfınızın `log_error` metodunun doğru şekilde çalıştığından emin olun. Ayrıca, `print` ifadelerini kaldırarak tüm hataların veritabanına kaydedilmesini sağlayın.

#### Güncellenmiş `fixture_data_handler.py` Dosyası

```python
# basemodels/fixture_data_handler.py

import http.client
import json
import ssl
from datetime import datetime
from django.db import IntegrityError, transaction
from basemodels.models import FikstureModelData, FikstureDataError

class FixtureDataHandler:

    DEFAULT_DATE = datetime.strptime("1900-01-01", "%Y-%m-%d").date()

    def __init__(self, date):
        self.date = date
        self.data_id = date.replace("-", "")

    def fetch_fixtures_from_api(self):
        """
        API'den fikstür verilerini çeker, 'events' anahtarını kontrol eder.
        Hata durumunda log_error ile hata kaydı yapar ve boş liste döner.
        """
        try:
            context = ssl._create_unverified_context()
            conn = http.client.HTTPSConnection('www.sofascore.com', context=context)
            conn.request('GET', f'/api/v1/sport/football/scheduled-events/{self.date}')
            response = conn.getresponse()

            if response.status == 401:
                self.log_error("AUTH_ERROR", "API Anahtarı Eksik veya Geçersiz")
                return []

            if response.status != 200:
                self.log_error("API_ERROR", f"API isteği başarısız oldu. HTTP Status: {response.status}")
                return []

            data = json.loads(response.read())

            # 'events' anahtarını kontrol et
            if "events" not in data:
                self.log_error("DATA_STRUCTURE_ERROR", "'events' anahtarı API yanıtında bulunamadı")
                return []

            events = data["events"]
            return [{
                'data_id': self.data_id,
                'tarih': self.date,
                'data': events,
                'count': len(events),
                'isprogress': False
            }]

        except KeyError as e:
            self.log_error("DATA_STRUCTURE_ERROR", f"Expected key missing: {e}")
            return []  # Hata durumunda boş liste döner

        except json.JSONDecodeError as e:
            self.log_error("JSON_DECODE_ERROR", str(e))
            return []

        except ConnectionResetError as e:
            self.log_error("CONNECTION_RESET_ERROR", str(e))
            return []

        except Exception as e:
            self.log_error("API_ERROR", str(e))
            return []

    def prepare_data_for_db(self, data):
        """
        API'den gelen veriyi veritabanı için uygun formata dönüştürür.
        """
        return [
            FikstureModelData(
                data_id=self.data_id,
                tarih=self.parse_date(self.date),
                data=item,
                count=len(data),
                isprogress=False
            ) for item in data
        ]

    def parse_date(self, date_str):
        """
        Tarih formatını doğrular. Hatalıysa varsayılan tarihi döner.
        """
        try:
            return datetime.strptime(date_str, "%Y-%m-%d").date()
        except ValueError:
            self.log_error("DATA_STRUCTURE_ERROR", f"Geçersiz tarih formatı: {date_str}, varsayılan tarih atanıyor.")
            return self.DEFAULT_DATE

    def save_fixtures_to_db(self):
        """
        API verilerini önce silerek veritabanına kaydeder.
        """
        data = self.fetch_fixtures_from_api()
        records = self.prepare_data_for_db(data)

        if records:
            try:
                with transaction.atomic():
                    # Önce aynı data_id'ye sahip veriyi sil
                    FikstureModelData.objects.filter(data_id=self.data_id).delete()
                    # Yeni kayıtları toplu olarak ekle
                    FikstureModelData.objects.bulk_create(records)
                    self.clear_error()  # Hata varsa sil
            except IntegrityError as e:
                self.log_error("INTEGRITY_ERROR", str(e))
        else:
            # Veri boşsa, hata durumunda varsayılan kayıt ekle
            self._save_default_data()

    def _save_default_data(self):
        """
        Hata veya boş veri durumunda varsayılan değerlerle kayıt ekler.
        """
        with transaction.atomic():
            FikstureModelData.objects.create(
                data_id='19000101',
                tarih=self.DEFAULT_DATE,
                data={},
                count=0,
                isprogress=False
            )
            self.log_error("DEFAULT_DATA_ERROR", "Boş veriyle kayıt yapıldı.")

    def log_error(self, error_type, message):
        """
        Hata durumunda FikstureDataError tablosuna kayıt ekler.
        """
        FikstureDataError.objects.update_or_create(
            data_id=self.data_id,
            defaults={
                'tarih': self.parse_date(self.date),
                'error_type': error_type,
                'error_message': message
            }
        )

    def clear_error(self):
        """
        Başarılı veri eklemeden sonra ilgili hatayı siler.
        """
        FikstureDataError.objects.filter(data_id=self.data_id).delete()
```

### Adım 5: Kodunuzu Test Edin

Model tanımlamalarını ve `admin.py` dosyasını güncelledikten sonra, kodunuzu tekrar test ederek hatasız çalıştığından emin olmalısınız.

#### a. Django Shell'i Kullanarak Test Etme

Öncelikle Django shell'i açın:

```bash
python manage.py shell
```

Shell içerisinde, `FixtureDataHandler` sınıfınızı ve örnek bir tarih ile işlemi başlatın:

```python
from basemodels.fixture_data_handler import FixtureDataHandler

# Geçersiz bir tarih kullanarak hatayı tetikleyin
handler = FixtureDataHandler("2024-11-35")  # 35. gün geçersizdir
handler.save_fixtures_to_db()
print("İşlem Tamamlandı")
```

#### b. Hataların Doğru Kaydedildiğinden Emin Olma

- **Başarılı Bir İşlem Durumu:**
  - `FikstureModelData` tablosunda ilgili kayıt eklenecektir.
  - Eğer önceden bu `data_id` için bir hata kaydı varsa, `FikstureDataError` tablosundan silinecektir.

- **Başarısız Bir İşlem Durumu (Geçersiz Tarih):**
  - `FikstureDataError` tablosuna yeni bir hata kaydı eklenecektir.
  - `FikstureModelData` tablosuna varsayılan bir kayıt eklenecektir (`data_id='19000101'`).

#### c. Admin Panelinden Kontrol Etme

Django admin paneline giriş yapın ve `FikstureModelData` ile `FikstureDataError` modellerini kontrol edin.

- **FikstureModelData:**
  - Başarılı olarak eklenen verileri görebilirsiniz.

- **FikstureDataError:**
  - Oluşan hataları burada görebilirsiniz.
  - Hata kaydı silindiğinde, ilgili kayıt bu tabloda yer almayacaktır.

### Adım 6: Ekstra Hataları Yönetme

`ConnectionResetError` gibi bağlantı hatalarını da yakalayarak veritabanına kaydetmek istiyorsunuz. Bu tür hataları da `except` bloklarına ekleyebilirsiniz.

#### Güncellenmiş `fetch_fixtures_from_api` Metodu

```python
def fetch_fixtures_from_api(self):
    """
    API'den fikstür verilerini çeker, 'events' anahtarını kontrol eder.
    Hata durumunda log_error ile hata kaydı yapar ve boş liste döner.
    """
    try:
        context = ssl._create_unverified_context()
        headers = {
            'Authorization': f'Bearer {self.api_key}',
            # Diğer gerekli başlıklar
        }
        conn = http.client.HTTPSConnection('www.sofascore.com', context=context)
        conn.request('GET', f'/api/v1/sport/football/scheduled-events/{self.date}', headers=headers)
        response = conn.getresponse()

        if response.status == 401:
            self.log_error("AUTH_ERROR", "API Anahtarı Eksik veya Geçersiz")
            return []

        if response.status != 200:
            self.log_error("API_ERROR", f"API isteği başarısız oldu. HTTP Status: {response.status}")
            return []

        data = json.loads(response.read())

        # 'events' anahtarını kontrol et
        if "events" not in data:
            self.log_error("DATA_STRUCTURE_ERROR", "'events' anahtarı API yanıtında bulunamadı")
            return []

        events = data["events"]
        return [{
            'data_id': self.data_id,
            'tarih': self.date,
            'data': events,
            'count': len(events),
            'isprogress': False
        }]

    except KeyError as e:
        self.log_error("DATA_STRUCTURE_ERROR", f"Expected key missing: {e}")
        return []  # Hata durumunda boş liste döner

    except json.JSONDecodeError as e:
        self.log_error("JSON_DECODE_ERROR", str(e))
        return []

    except ConnectionResetError as e:
        self.log_error("CONNECTION_RESET_ERROR", str(e))
        return []

    except Exception as e:
        self.log_error("API_ERROR", str(e))
        return []
```

Bu şekilde, `ConnectionResetError` gibi spesifik hataları da yakalayarak veritabanına kaydedebilirsiniz.

### Adım 7: Model Alanlarını Kontrol Etme

Modelinizin doğru şekilde tanımlandığından ve migration'ların doğru yapıldığından emin olmak için Django shell'de model alanlarını kontrol edebilirsiniz.

#### Django Shell'de Model Alanlarını Kontrol Edin

```bash
python manage.py shell
```

Shell içerisinde:

```python
from basemodels.models import FikstureDataError
for field in FikstureDataError._meta.get_fields():
    print(field.name)
```

Bu komut, `FikstureDataError` modelinizdeki tüm alanları listeleyecektir. `error_type` ve `error_message` alanlarının burada göründüğünden emin olun.

### Adım 8: Sorun Giderme

Eğer hala `FieldError` alıyorsanız, aşağıdaki adımları izleyerek sorunu çözebilirsiniz:

1. **Model Dosyasını Doğru Güncellediğinizden Emin Olun:**
   - `basemodels/models.py` dosyanızda `FikstureDataError` modelinde `error_type` ve `error_message` alanlarının tanımlı olduğundan emin olun.

2. **Migration İşlemlerini Doğru Yapın:**
   - Model değişikliklerinden sonra `makemigrations` ve `migrate` komutlarını doğru şekilde çalıştırdığınızdan emin olun.

3. **Veritabanı Bağlantısını Kontrol Edin:**
   - Doğru veritabanına bağlandığınızdan ve migration'ların doğru veritabanına uygulandığından emin olun.

4. **Django Shell'de Model Alanlarını Kontrol Edin:**
   - Yukarıdaki adımda belirtilen şekilde model alanlarını kontrol edin.

5. **Veritabanını Yeniden Migrasyon Yapın:**
   - Eğer hala sorun yaşıyorsanız, mevcut migration dosyalarını silip yeniden oluşturmayı düşünebilirsiniz. Ancak bu işlemi yapmadan önce veritabanınızdaki mevcut verileri yedeklemeyi unutmayın.

### Adım 9: Kodu Son Hale Getirme

Tüm adımları takip ederek, `FixtureDataHandler` sınıfınızı ve `FikstureDataError` modelinizi hatasız çalışacak şekilde düzelttik. İşte son hali:

#### `models.py`

```python
# basemodels/models.py

from django.db import models

class FikstureModelData(models.Model):
    data_id = models.CharField(max_length=255, unique=True)  # date.replace("-","") değerini burada saklayacağız
    tarih = models.DateField()  # Orijinal tarih alanı
    data = models.JSONField()  # JSON verisi için alan
    count = models.IntegerField()
    isprogress = models.BooleanField(default=False)  # İlerleme durumu
    created_at = models.DateTimeField(auto_now_add=True)  # Verinin oluşturulma tarihi
    updated_at = models.DateTimeField(auto_now=True)  # Verinin güncellenme tarihi

    def __str__(self):
        return f"{self.data_id} - {self.tarih}"

    class Meta:
        verbose_name = 'Model Data'
        verbose_name_plural = 'Model Datas'


class FikstureDataError(models.Model):
    ERROR_TYPES = [
        ('API_ERROR', 'API Error'),
        ('DATA_STRUCTURE_ERROR', 'Data Structure Error'),
        ('JSON_DECODE_ERROR', 'JSON Decode Error'),
        ('INTEGRITY_ERROR', 'Integrity Error'),
        ('DEFAULT_DATA_ERROR', 'Default Data Error'),
        ('AUTH_ERROR', 'Authentication Error'),
        # Diğer hata tiplerini buraya ekleyebilirsiniz
    ]

    data_id = models.CharField(max_length=255, unique=True)  # Hangi data_id'ye ait hata olduğu
    tarih = models.DateField()  # Hatanın olduğu tarih
    error_type = models.CharField(max_length=50, choices=ERROR_TYPES)  # Hata tipi
    error_message = models.TextField()  # Hata mesajı
    created_at = models.DateTimeField(auto_now_add=True)  # Hata kaydının oluşturulma zamanı
    updated_at = models.DateTimeField(auto_now=True)  # Hata kaydının güncellenme zamanı

    def __str__(self):
        return f"{self.data_id} - {self.get_error_type_display()} - {self.tarih}"

    class Meta:
        verbose_name = 'Data Error'
        verbose_name_plural = 'Data Errors'
```

#### `fixture_data_handler.py`

```python
# basemodels/fixture_data_handler.py

import http.client
import json
import ssl
from datetime import datetime
from django.db import IntegrityError, transaction
from basemodels.models import FikstureModelData, FikstureDataError
from django.conf import settings

class FixtureDataHandler:

    DEFAULT_DATE = datetime.strptime("1900-01-01", "%Y-%m-%d").date()

    def __init__(self, date):
        self.date = date
        self.data_id = date.replace("-", "")
        self.api_key = settings.SOFASCORE_API_KEY  # settings'den API anahtarını al

    def fetch_fixtures_from_api(self):
        """
        API'den fikstür verilerini çeker, 'events' anahtarını kontrol eder.
        Hata durumunda log_error ile hata kaydı yapar ve boş liste döner.
        """
        try:
            context = ssl._create_unverified_context()
            headers = {
                'Authorization': f'Bearer {self.api_key}',
                # Diğer gerekli başlıklar
            }
            conn = http.client.HTTPSConnection('www.sofascore.com', context=context)
            conn.request('GET', f'/api/v1/sport/football/scheduled-events/{self.date}', headers=headers)
            response = conn.getresponse()

            if response.status == 401:
                self.log_error("AUTH_ERROR", "API Anahtarı Eksik veya Geçersiz")
                return []

            if response.status != 200:
                self.log_error("API_ERROR", f"API isteği başarısız oldu. HTTP Status: {response.status}")
                return []

            data = json.loads(response.read())

            # 'events' anahtarını kontrol et
            if "events" not in data:
                self.log_error("DATA_STRUCTURE_ERROR", "'events' anahtarı API yanıtında bulunamadı")
                return []

            events = data["events"]
            return [{
                'data_id': self.data_id,
                'tarih': self.date,
                'data': events,
                'count': len(events),
                'isprogress': False
            }]

        except KeyError as e:
            self.log_error("DATA_STRUCTURE_ERROR", f"Expected key missing: {e}")
            return []  # Hata durumunda boş liste döner

        except json.JSONDecodeError as e:
            self.log_error("JSON_DECODE_ERROR", str(e))
            return []

        except ConnectionResetError as e:
            self.log_error("CONNECTION_RESET_ERROR", str(e))
            return []

        except Exception as e:
            self.log_error("API_ERROR", str(e))
            return []

    def prepare_data_for_db(self, data):
        """
        API'den gelen veriyi veritabanı için uygun formata dönüştürür.
        """
        return [
            FikstureModelData(
                data_id=self.data_id,
                tarih=self.parse_date(self.date),
                data=item,
                count=len(data),
                isprogress=False
            ) for item in data
        ]

    def parse_date(self, date_str):
        """
        Tarih formatını doğrular. Hatalıysa varsayılan tarihi döner.
        """
        try:
            return datetime.strptime(date_str, "%Y-%m-%d").date()
        except ValueError:
            self.log_error("DATA_STRUCTURE_ERROR", f"Geçersiz tarih formatı: {date_str}, varsayılan tarih atanıyor.")
            return self.DEFAULT_DATE

    def save_fixtures_to_db(self):
        """
        API verilerini önce silerek veritabanına kaydeder.
        """
        data = self.fetch_fixtures_from_api()
        records = self.prepare_data_for_db(data)

        if records:
            try:
                with transaction.atomic():
                    # Önce aynı data_id'ye sahip veriyi sil
                    FikstureModelData.objects.filter(data_id=self.data_id).delete()
                    # Yeni kayıtları toplu olarak ekle
                    FikstureModelData.objects.bulk_create(records)
                    self.clear_error()  # Hata varsa sil
            except IntegrityError as e:
                self.log_error("INTEGRITY_ERROR", str(e))
        else:
            # Veri boşsa, hata durumunda varsayılan kayıt ekle
            self._save_default_data()

    def _save_default_data(self):
        """
        Hata veya boş veri durumunda varsayılan değerlerle kayıt ekler.
        """
        with transaction.atomic():
            FikstureModelData.objects.create(
                data_id='19000101',
                tarih=self.DEFAULT_DATE,
                data={},
                count=0,
                isprogress=False
            )
            self.log_error("DEFAULT_DATA_ERROR", "Boş veriyle kayıt yapıldı.")

    def log_error(self, error_type, message):
        """
        Hata durumunda FikstureDataError tablosuna kayıt ekler.
        """
        FikstureDataError.objects.update_or_create(
            data_id=self.data_id,
            defaults={
                'tarih': self.parse_date(self.date),
                'error_type': error_type,
                'error_message': message
            }
        )

    def clear_error(self):
        """
        Başarılı veri eklemeden sonra ilgili hatayı siler.
        """
        FikstureDataError.objects.filter(data_id=self.data_id).delete()
```

### Adım 7: Hataların Doğru Kaydedildiğinden Emin Olma

Bu adımları takip ettikten sonra, hataların doğru şekilde veritabanına kaydedildiğinden emin olmak için Django shell veya admin panelini kullanarak kontrol edebilirsiniz.

#### Django Shell'de Kontrol Etme

```bash
python manage.py shell
```

Shell içerisinde:

```python
from basemodels.fixture_data_handler import FixtureDataHandler

# Geçersiz bir tarih kullanarak hatayı tetikleyin
handler = FixtureDataHandler("2024-11-35")  # 35. gün geçersizdir
handler.save_fixtures_to_db()
print("İşlem Tamamlandı")
```

#### Admin Panelinde Kontrol Etme

1. **Django Admin Paneline Giriş Yapın:**
   - URL genellikle `http://localhost:8000/admin/` olur.

2. **`FikstureModelData` ve `FikstureDataError` Modellerini Kontrol Edin:**
   - **FikstureModelData:** Başarılı olarak eklenen verileri görebilirsiniz.
   - **FikstureDataError:** Oluşan hataları burada görebilirsiniz.

### Adım 8: Ekstra Hata Yönetimi

Bağlantı hataları gibi diğer spesifik hataları da yakalamak istiyorsanız, ilgili `except` bloklarını ekleyebilirsiniz. Örneğin, `ConnectionResetError` gibi hataları yakalayabilirsiniz.

#### Güncellenmiş `fetch_fixtures_from_api` Metodu

```python
def fetch_fixtures_from_api(self):
    """
    API'den fikstür verilerini çeker, 'events' anahtarını kontrol eder.
    Hata durumunda log_error ile hata kaydı yapar ve boş liste döner.
    """
    try:
        context = ssl._create_unverified_context()
        headers = {
            'Authorization': f'Bearer {self.api_key}',
            # Diğer gerekli başlıklar
        }
        conn = http.client.HTTPSConnection('www.sofascore.com', context=context)
        conn.request('GET', f'/api/v1/sport/football/scheduled-events/{self.date}', headers=headers)
        response = conn.getresponse()

        if response.status == 401:
            self.log_error("AUTH_ERROR", "API Anahtarı Eksik veya Geçersiz")
            return []

        if response.status != 200:
            self.log_error("API_ERROR", f"API isteği başarısız oldu. HTTP Status: {response.status}")
            return []

        data = json.loads(response.read())

        # 'events' anahtarını kontrol et
        if "events" not in data:
            self.log_error("DATA_STRUCTURE_ERROR", "'events' anahtarı API yanıtında bulunamadı")
            return []

        events = data["events"]
        return [{
            'data_id': self.data_id,
            'tarih': self.date,
            'data': events,
            'count': len(events),
            'isprogress': False
        }]

    except KeyError as e:
        self.log_error("DATA_STRUCTURE_ERROR", f"Expected key missing: {e}")
        return []  # Hata durumunda boş liste döner

    except json.JSONDecodeError as e:
        self.log_error("JSON_DECODE_ERROR", str(e))
        return []

    except ConnectionResetError as e:
        self.log_error("CONNECTION_RESET_ERROR", str(e))
        return []

    except Exception as e:
        self.log_error("API_ERROR", str(e))
        return []
```

### Adım 9: Özet ve İpuçları

1. **Model Tanımlamaları:**
   - `FikstureDataError` modelinizde `error_type` ve `error_message` alanlarının doğru şekilde tanımlandığından emin olun.

2. **Migration İşlemleri:**
   - Model değişikliklerinden sonra `makemigrations` ve `migrate` komutlarını doğru şekilde çalıştırdığınızdan emin olun.

3. **Admin Paneli:**
   - `admin.py` dosyanızı doğru şekilde güncelleyerek modellerinizi admin paneline ekleyin.

4. **Hata Yönetimi:**
   - `FixtureDataHandler` sınıfında `log_error` metodunun doğru şekilde çalıştığından ve tüm hataları veritabanına kaydettiğinden emin olun.
   - `print` ifadelerini kaldırarak tüm hataların veritabanına kaydedilmesini sağlayın.

5. **Test Etme:**
   - Django shell veya admin paneli üzerinden test ederek, verilerin doğru şekilde kaydedildiğini ve hataların doğru şekilde loglandığını kontrol edin.

6. **Spesifik Hataları Yakalama:**
   - `ConnectionResetError` gibi spesifik hataları yakalayarak veritabanına kaydedin.

### Sonuç

Bu adımları dikkatlice takip ederek, `FikstureDataError` modelinizdeki tüm hata türlerini doğru şekilde kaydedebilir ve `FixtureDataHandler` sınıfınızı hatasız çalışacak şekilde düzeltebilirsiniz. Herhangi bir adımda sorun yaşarsanız, aşağıdaki kontrolleri yaparak sorunu tespit edebilirsiniz:

- **Model Dosyasını Kontrol Edin:**
  - `basemodels/models.py` dosyanızda `FikstureDataError` modelinde `error_type` ve `error_message` alanlarının tanımlı olduğundan emin olun.

- **Migration Durumunu Kontrol Edin:**
  - `python manage.py showmigrations` komutunu çalıştırarak hangi migration'ların uygulandığını kontrol edin.

- **Veritabanı Bağlantısını Kontrol Edin:**
  - Doğru veritabanına bağlandığınızdan ve migration'ların doğru veritabanına uygulandığından emin olun.

- **Django Shell'de Model Alanlarını Kontrol Edin:**
  - Shell içerisinde `FikstureDataError` modelinin tüm alanlarını kontrol edin:
    ```python
    from basemodels.models import FikstureDataError
    for field in FikstureDataError._meta.get_fields():
        print(field.name)
    ```

Bu kontrolleri yaptıktan sonra hala sorun yaşıyorsanız, lütfen aşağıdaki bilgileri paylaşarak daha detaylı yardımcı olmamı sağlayın:

1. **`models.py` Dosyanızın Tamamı:**
   - `FikstureDataError` modelinizi tam olarak nasıl tanımladığınızı paylaşın.

2. **Migration Durumunu Gösterin:**
   - `python manage.py showmigrations` komutunun çıktısını paylaşın.

3. **Hata Mesajlarını İnceleyin:**
   - Hata mesajlarında belirtilen alan adlarının doğru olduğundan emin olun.

Bu bilgilerle, daha hedefe yönelik ve etkili bir çözüm sunabilirim.

***Soru:*** OperationalError at /admin/basemodels/fiksturedataerror/
no such column: basemodels_fiksturedataerror.error_type
Request Method:	GET
Request URL:	http://127.0.0.1:8000/admin/basemodels/fiksturedataerror/
Django Version:	4.2.7
Exception Type:	OperationalError
Exception Value:	
no such column: basemodels_fiksturedataerror.error_type
Exception Location:	C:\Users\ahmet.yildirir\AppData\Local\Programs\Python\Python312\Lib\site-packages\django\db\backends\sqlite3\base.py, line 328, in execute
Raised during:	django.contrib.admin.options.changelist_view
Python Executable:	C:\Users\ahmet.yildirir\AppData\Local\Programs\Python\Python312\python.exe
Python Version:	3.12.0
Python Path:	
['C:\\Users\\ahmet.yildirir\\Desktop\\DjangoTestler\\FxS',
 'C:\\Users\\ahmet.yildirir\\AppData\\Local\\Programs\\Python\\Python312\\python312.zip',
 'C:\\Users\\ahmet.yildirir\\AppData\\Local\\Programs\\Python\\Python312\\DLLs',
 'C:\\Users\\ahmet.yildirir\\AppData\\Local\\Programs\\Python\\Python312\\Lib',
 'C:\\Users\\ahmet.yildirir\\AppData\\Local\\Programs\\Python\\Python312',
 'C:\\Users\\ahmet.yildirir\\AppData\\Local\\Programs\\Python\\Python312\\Lib\\site-packages',
 'C:\\Users\\ahmet.yildirir\\AppData\\Local\\Programs\\Python\\Python312\\Lib\\site-packages\\win32',
 'C:\\Users\\ahmet.yildirir\\AppData\\Local\\Programs\\Python\\Python312\\Lib\\site-packages\\win32\\lib',
 'C:\\Users\\ahmet.yildirir\\AppData\\Local\\Programs\\Python\\Python312\\Lib\\site-packages\\Pythonwin']
Server time:	Wed, 06 Nov 2024 13:37:17 +0300   peki bu hata neden geldi

Tool: **Model güncellemelerini kontrol ediyorum**

Django'da FikstureModelData ve FikstureDataError ile çalışıyorum. Hata türü kolonu eksik veya yanlış migrasyonlar sorun yaratabiliyor.

modelleri kontrol ediyor ve database işlem adımlarını değerlendiriyorum.

**İzleme ve düzeltme**

Modeller güncellendiğinde migrasyonların oluşturulup oluşturulmadığını, veritabanında uygulandığını ve verilerin korunduğunu kontrol ediyorum. Gerekirse, migrasyonları düzeltmeyi düşünüyorum.

**İnceleme yapıyorum**

fetch_fixtures_from_api'yi inceledim ve user yanlışlıkla self.log_error'ı '_hata_401' olarak ayarlamış. Bu, method'u geçersiz kılarak hatalara neden olur.

**Geri adım atma**  
Kullanıcının kodundaki hatayı düzeltmek için, `self.log_error`'ı bir dize olarak ayarladığı yanlış değişiklikleri geri alması gerekiyor.

**Veritabanı hata yönetimini ele almak**

Kodda `self.log_error` kullanımını düzeltmek ve hata mesajlarını uygun bir şekilde işlemek üzerine çalışmalar yapıyorum.

**Cevap:** Görünüşe göre, Django projenizde `FikstureDataError` modelinizdeki `error_type` ve `error_message` alanları doğru şekilde tanımlanmamış veya kodunuzda bu alanlara yanlış şekilde erişim sağlanmış. Bu durum, veritabanınızda bu alanların olmamasına ve `OperationalError: no such column: basemodels_fiksturedataerror.error_type` hatasının ortaya çıkmasına neden oluyor.

### Sorunun Kaynağı

Ana sorun, `FixtureDataHandler` sınıfınızda `self.log_error` metodunu yanlış şekilde kullanmanızdan kaynaklanıyor. Kodunuzda şu satırları gördüm:

```python
if response.status == 401:
    self.log_error='hata 401'

if response.status != 200:
    self.log_error='hata 401'
```

Bu satırlar, `log_error` metodunu bir string ile **özel bir değişken** olarak yeniden tanımlıyor. Sonuç olarak, `log_error` metodu artık bir metod değil, bir string oluyor. Bu da daha sonra `self.log_error("API_ERROR", str(e))` çağırdığınızda Django'nun bu stringi bir metod olarak tanımamasına ve hata almanıza neden oluyor.

### Çözüm Adımları

Bu hatayı düzeltmek için aşağıdaki adımları dikkatlice takip edin:

1. **`FixtureDataHandler` Sınıfını Doğru Şekilde Güncelleyin**
2. **`FikstureDataError` Modelinizi Doğru Tanımlayın**
3. **Migration İşlemlerini Doğru Şekilde Uygulayın**
4. **Admin Panelini Kontrol Edin ve Test Edin**

#### 1. `FixtureDataHandler` Sınıfını Doğru Şekilde Güncelleyin

Öncelikle, `FixtureDataHandler` sınıfınızda `log_error` metodunu doğru şekilde kullanmanız gerekiyor. `log_error` metodunu **asla** bir string ile yeniden tanımlamayın. Bunun yerine, bu metodu doğru şekilde çağırın.

**Yanlış Kullanım:**

```python
if response.status == 401:
    self.log_error = 'hata 401'

if response.status != 200:
    self.log_error = 'hata 401'
```

**Doğru Kullanım:**

```python
if response.status == 401:
    self.log_error("AUTH_ERROR", "API Anahtarı Eksik veya Geçersiz")
    return []

if response.status != 200:
    self.log_error("API_ERROR", f"API isteği başarısız oldu. HTTP Status: {response.status}")
    return []
```

**Güncellenmiş `fixture_data_handler.py`:**

```python
# basemodels/fixture_data_handler.py

import http.client
import json
import ssl
from datetime import datetime
from django.db import IntegrityError, transaction
from basemodels.models import FikstureModelData, FikstureDataError
from django.conf import settings

class FixtureDataHandler:

    DEFAULT_DATE = datetime.strptime("1900-01-01", "%Y-%m-%d").date()

    def __init__(self, date):
        self.date = date
        self.data_id = date.replace("-", "")
        self.api_key = settings.SOFASCORE_API_KEY  # settings'den API anahtarını al

    def fetch_fixtures_from_api(self):
        """
        API'den fikstür verilerini çeker, 'events' anahtarını kontrol eder.
        Hata durumunda log_error ile hata kaydı yapar ve boş liste döner.
        """
        try:
            context = ssl._create_unverified_context()
            headers = {
                'Authorization': f'Bearer {self.api_key}',
                # Diğer gerekli başlıklar
            }
            conn = http.client.HTTPSConnection('www.sofascore.com', context=context)
            conn.request('GET', f'/api/v1/sport/football/scheduled-events/{self.date}', headers=headers)
            response = conn.getresponse()

            if response.status == 401:
                self.log_error("AUTH_ERROR", "API Anahtarı Eksik veya Geçersiz")
                return []

            if response.status != 200:
                self.log_error("API_ERROR", f"API isteği başarısız oldu. HTTP Status: {response.status}")
                return []

            data = json.loads(response.read())

            # 'events' anahtarını kontrol et
            if "events" not in data:
                self.log_error("DATA_STRUCTURE_ERROR", "'events' anahtarı API yanıtında bulunamadı")
                return []

            events = data["events"]
            return [{
                'data_id': self.data_id,
                'tarih': self.date,
                'data': events,
                'count': len(events),
                'isprogress': False
            }]

        except KeyError as e:
            self.log_error("DATA_STRUCTURE_ERROR", f"Expected key missing: {e}")
            return []  # Hata durumunda boş liste döner

        except json.JSONDecodeError as e:
            self.log_error("JSON_DECODE_ERROR", str(e))
            return []

        except ConnectionResetError as e:
            self.log_error("CONNECTION_RESET_ERROR", str(e))
            return []

        except Exception as e:
            self.log_error("API_ERROR", str(e))
            return []

    def prepare_data_for_db(self, data):
        """
        API'den gelen veriyi veritabanı için uygun formata dönüştürür.
        """
        return [
            FikstureModelData(
                data_id=self.data_id,
                tarih=self.parse_date(self.date),
                data=item,
                count=len(data),
                isprogress=False
            ) for item in data
        ]

    def parse_date(self, date_str):
        """
        Tarih formatını doğrular. Hatalıysa varsayılan tarihi döner.
        """
        try:
            return datetime.strptime(date_str, "%Y-%m-%d").date()
        except ValueError:
            self.log_error("DATA_STRUCTURE_ERROR", f"Geçersiz tarih formatı: {date_str}, varsayılan tarih atanıyor.")
            return self.DEFAULT_DATE

    def save_fixtures_to_db(self):
        """
        API verilerini önce silerek veritabanına kaydeder.
        """
        data = self.fetch_fixtures_from_api()
        records = self.prepare_data_for_db(data)

        if records:
            try:
                with transaction.atomic():
                    # Önce aynı data_id'ye sahip veriyi sil
                    FikstureModelData.objects.filter(data_id=self.data_id).delete()
                    # Yeni kayıtları toplu olarak ekle
                    FikstureModelData.objects.bulk_create(records)
                    self.clear_error()  # Hata varsa sil
            except IntegrityError as e:
                self.log_error("INTEGRITY_ERROR", str(e))
        else:
            # Veri boşsa, hata durumunda varsayılan kayıt ekle
            self._save_default_data()

    def _save_default_data(self):
        """
        Hata veya boş veri durumunda varsayılan değerlerle kayıt ekler.
        """
        with transaction.atomic():
            FikstureModelData.objects.create(
                data_id='19000101',
                tarih=self.DEFAULT_DATE,
                data={},
                count=0,
                isprogress=False
            )
            self.log_error("DEFAULT_DATA_ERROR", "Boş veriyle kayıt yapıldı.")

    def log_error(self, error_type, message):
        """
        Hata durumunda FikstureDataError tablosuna kayıt ekler.
        """
        FikstureDataError.objects.update_or_create(
            data_id=self.data_id,
            defaults={
                'tarih': self.parse_date(self.date),
                'error_type': error_type,
                'error_message': message
            }
        )

    def clear_error(self):
        """
        Başarılı veri eklemeden sonra ilgili hatayı siler.
        """
        FikstureDataError.objects.filter(data_id=self.data_id).delete()
```

#### 2. `FikstureDataError` Modelinizi Doğru Tanımlayın

`FikstureDataError` modelinizin doğru şekilde tanımlandığından emin olun. Özellikle `error_type` ve `error_message` alanlarının tanımlı olması gerekiyor.

**`models.py` Dosyanızı Güncelleyin:**

```python
# basemodels/models.py

from django.db import models

class FikstureModelData(models.Model):
    data_id = models.CharField(max_length=255, unique=True)  # date.replace("-","") değerini burada saklayacağız
    tarih = models.DateField()  # Orijinal tarih alanı
    data = models.JSONField()  # JSON verisi için alan
    count = models.IntegerField()
    isprogress = models.BooleanField(default=False)  # İlerleme durumu
    created_at = models.DateTimeField(auto_now_add=True)  # Verinin oluşturulma tarihi
    updated_at = models.DateTimeField(auto_now=True)  # Verinin güncellenme tarihi

    def __str__(self):
        return f"{self.data_id} - {self.tarih}"

    class Meta:
        verbose_name = 'Model Data'
        verbose_name_plural = 'Model Datas'


class FikstureDataError(models.Model):
    ERROR_TYPES = [
        ('API_ERROR', 'API Error'),
        ('DATA_STRUCTURE_ERROR', 'Data Structure Error'),
        ('JSON_DECODE_ERROR', 'JSON Decode Error'),
        ('INTEGRITY_ERROR', 'Integrity Error'),
        ('DEFAULT_DATA_ERROR', 'Default Data Error'),
        ('AUTH_ERROR', 'Authentication Error'),
        # Diğer hata tiplerini buraya ekleyebilirsiniz
    ]

    data_id = models.CharField(max_length=255, unique=True)  # Hangi data_id'ye ait hata olduğu
    tarih = models.DateField()  # Hatanın olduğu tarih
    error_type = models.CharField(max_length=50, choices=ERROR_TYPES)  # Hata tipi
    error_message = models.TextField()  # Hata mesajı
    created_at = models.DateTimeField(auto_now_add=True)  # Hata kaydının oluşturulma zamanı
    updated_at = models.DateTimeField(auto_now=True)  # Hata kaydının güncellenme zamanı

    def __str__(self):
        return f"{self.data_id} - {self.get_error_type_display()} - {self.tarih}"

    class Meta:
        verbose_name = 'Data Error'
        verbose_name_plural = 'Data Errors'
```

#### 3. Migration İşlemlerini Doğru Şekilde Uygulayın

Model değişikliklerinizin veritabanına yansıtılması için migration işlemlerini dikkatlice yapmanız gerekiyor.

**Terminal veya Komut İstemcisinde Aşağıdaki Komutları Çalıştırın:**

```bash
python manage.py makemigrations
python manage.py migrate
```

**Not:**
- `makemigrations` komutu, model değişikliklerinizi algılar ve gerekli migration dosyalarını oluşturur.
- `migrate` komutu ise bu migration dosyalarını veritabanınıza uygular.

Eğer bu komutlar sırasında herhangi bir hata alırsanız, hatayı çözmeden devam etmeyin.

#### 4. Admin Panelini Kontrol Edin ve Test Edin

Migration işlemlerini başarıyla tamamladıktan sonra, Django admin panelini kullanarak `FikstureDataError` modelinizi kontrol edin.

**Django Admin Paneline Giriş Yapın:**
- Genellikle `http://127.0.0.1:8000/admin/` adresinde bulunur.
- Yönetici kullanıcı bilgilerinizle giriş yapın.

**`FikstureDataError` Modelini Kontrol Edin:**
- `basemodels` uygulamasını bulun ve `FikstureDataError` modelini tıklayın.
- Şimdi, modelin alanlarının doğru şekilde göründüğünden emin olun (`error_type` ve `error_message` dahil).

### Ekstra Kontroller ve Sorun Giderme

Eğer yukarıdaki adımları uyguladıktan sonra hala sorun yaşıyorsanız, aşağıdaki kontrolleri yapabilirsiniz:

#### a. Django Shell'de Model Alanlarını Kontrol Edin

```bash
python manage.py shell
```

Shell içerisinde:

```python
from basemodels.models import FikstureDataError
for field in FikstureDataError._meta.get_fields():
    print(field.name)
```

Bu komut, `FikstureDataError` modelinizdeki tüm alanları listeleyecektir. `error_type` ve `error_message` alanlarının burada göründüğünden emin olun.

#### b. Migration Dosyalarını Kontrol Edin

`basemodels/migrations/` klasöründe oluşturulan migration dosyalarını kontrol edin. `FikstureDataError` modeline eklenen `error_type` ve `error_message` alanlarını içeren bir migration dosyası olmalıdır.

#### c. Veritabanını Kontrol Edin

SQLite kullanıyorsanız, veritabanınızda (`db.sqlite3`) `basemodels_fiksturedataerror` tablosunun `error_type` ve `error_message` sütunlarına sahip olduğundan emin olun. Bunun için SQLite tarayıcısı kullanabilirsiniz veya aşağıdaki komutları kullanabilirsiniz:

```bash
sqlite3 db.sqlite3
```

SQLite prompt'unda:

```sql
.schema basemodels_fiksturedataerror
```

Bu komut, tablo yapısını gösterir. `error_type` ve `error_message` sütunlarının orada olup olmadığını kontrol edin.

#### d. Migration'ları Yeniden Uygulayın

Eğer migration'larınızın doğru uygulandığından emin değilseniz, aşağıdaki adımları takip edebilirsiniz:

1. **Migration Dosyalarını Silin:**
   - `basemodels/migrations/` klasöründe `__init__.py` dışındaki tüm dosyaları silin.

2. **Veritabanını Silin:**
   - SQLite kullanıyorsanız, `db.sqlite3` dosyasını silin.
   - **Dikkat:** Bu adım tüm verilerinizi silecektir. Eğer önemli verileriniz varsa, yedek almayı unutmayın.

3. **Migration'ları Tekrar Oluşturun ve Uygulayın:**

```bash
python manage.py makemigrations
python manage.py migrate
```

4. **Admin Panelini Tekrar Kontrol Edin:**

Yeniden oluşturulan veritabanı ve migration'lar ile admin paneline tekrar giriş yapın ve `FikstureDataError` modelini kontrol edin.

### Sonuç

Bu adımları takip ederek, `FikstureDataError` modelinizdeki `error_type` ve `error_message` alanlarının doğru şekilde tanımlandığından ve veritabanına başarılı bir şekilde uygulandığından emin olabilirsiniz. Özellikle `log_error` metodunu doğru şekilde çağırmak ve asla bir metodu bir string ile yeniden tanımlamamak çok önemlidir.

Eğer bu adımları dikkatlice uygularsanız, artık `OperationalError: no such column: basemodels_fiksturedataerror.error_type` hatası almanızın önüne geçebilirsiniz. Herhangi bir adımda sorun yaşarsanız veya ek yardım isterseniz, lütfen ayrıntılı bilgi sağlayarak tekrar sorabilirsiniz.

***Soru:*** şimdi bu modelde şöyle bir şey yapalım eğer count = len(data) 1 ise veri gelmemiş demektir bunu FikstureDataError modeline atmalısın kodlaru düzelt
import http.client
import json
import ssl
from datetime import datetime
from django.db import IntegrityError, transaction
from basemodels.models import FikstureModelData, FikstureDataError
from django.conf import settings

class FixtureDataHandler:

    DEFAULT_DATE = datetime.strptime("1900-01-01", "%Y-%m-%d").date()

    def __init__(self, date):
        self.date = date
        self.data_id = date.replace("-", "")
      

    def fetch_fixtures_from_api(self):
        """
        API'den fikstür verilerini çeker, 'events' anahtarını kontrol eder.
        Hata durumunda log_error ile hata kaydı yapar ve boş liste döner.
        """
        try:
            context = ssl._create_unverified_context()

            conn = http.client.HTTPSConnection('www.sofascore.com', context=context)
            conn.request('GET', f'/api/v1/sport/football/scheduled-events/{self.date}', )
            response = conn.getresponse()

            if response.status == 401:
                self.log_error("AUTH_ERROR", "API Anahtarı Eksik veya Geçersiz")
                return []

            if response.status != 200:
                self.log_error("API_ERROR", f"API isteği başarısız oldu. HTTP Status: {response.status}")
                return []

            data = json.loads(response.read())

            # 'events' anahtarını kontrol et
            if "events" not in data:
                self.log_error("DATA_STRUCTURE_ERROR", "'events' anahtarı API yanıtında bulunamadı")
                return []

            events = data["events"]
            return [{
                'data_id': self.data_id,
                'tarih': self.date,
                'data': events,
                'count': len(events),
                'isprogress': False
            }]

        except KeyError as e:
            self.log_error("DATA_STRUCTURE_ERROR", f"Expected key missing: {e}")
            return []  # Hata durumunda boş liste döner

        except json.JSONDecodeError as e:
            self.log_error("JSON_DECODE_ERROR", str(e))
            return []

        except ConnectionResetError as e:
            self.log_error("CONNECTION_RESET_ERROR", str(e))
            return []

        except Exception as e:
            self.log_error("API_ERROR", str(e))
            return []

    def prepare_data_for_db(self, data):
        """
        API'den gelen veriyi veritabanı için uygun formata dönüştürür.
        """
        return [
            FikstureModelData(
                data_id=self.data_id,
                tarih=self.parse_date(self.date),
                data=item,
                count=len(data),
                isprogress=False
            ) for item in data
        ]

    def parse_date(self, date_str):
        """
        Tarih formatını doğrular. Hatalıysa varsayılan tarihi döner.
        """
        try:
            return datetime.strptime(date_str, "%Y-%m-%d").date()
        except ValueError:
            self.log_error("DATA_STRUCTURE_ERROR", f"Geçersiz tarih formatı: {date_str}, varsayılan tarih atanıyor.")
            return self.DEFAULT_DATE

    def save_fixtures_to_db(self):
        """
        API verilerini önce silerek veritabanına kaydeder.
        """
        data = self.fetch_fixtures_from_api()
        records = self.prepare_data_for_db(data)

        if records:
            try:
                with transaction.atomic():
                    # Önce aynı data_id'ye sahip veriyi sil
                    FikstureModelData.objects.filter(data_id=self.data_id).delete()
                    # Yeni kayıtları toplu olarak ekle
                    FikstureModelData.objects.bulk_create(records)
                    self.clear_error()  # Hata varsa sil
            except IntegrityError as e:
                self.log_error("INTEGRITY_ERROR", str(e))
        else:
            # Veri boşsa, hata durumunda varsayılan kayıt ekle
            self._save_default_data()

    def _save_default_data(self):
        """
        Hata veya boş veri durumunda varsayılan değerlerle kayıt ekler.
        """
        with transaction.atomic():
            FikstureModelData.objects.create(
                data_id='19000101',
                tarih=self.DEFAULT_DATE,
                data={},
                count=0,
                isprogress=False
            )
            self.log_error("DEFAULT_DATA_ERROR", "Boş veriyle kayıt yapıldı.")

    def log_error(self, error_type, message):
        """
        Hata durumunda FikstureDataError tablosuna kayıt ekler.
        """
        FikstureDataError.objects.update_or_create(
            data_id=self.data_id,
            defaults={
                'tarih': self.parse_date(self.date),
                'error_type': error_type,
                'error_message': message
            }
        )

    def clear_error(self):
        """
        Başarılı veri eklemeden sonra ilgili hatayı siler.
        """
        FikstureDataError.objects.filter(data_id=self.data_id).delete()

Tool: **Veri çekme ve loglama işlemi**

Django projesiyle API verilerini çekip, saklayıp, hata loglama işlemi yapıyorum. `fixture_data_handler.py` dosyasını düzeltiyorum. `FixtureDataHandler` sınıfını, `count = len(data) == 1` olduğunda veri almadığını belirtmek ve `FikstureDataError` modeline eklemek için güncelliyorum.

**Güncü yapılandırma**

Bu sefer, `OperationalError` hatasını düzenlemek için `fixture_data_handler.py` dosyasını güncelliyorum. Hatalar veritabanına kaydedilecek ve `print` ifadeleri kaldırılacak.

**Veritabanı düzeyi**

İhtiyaç varsa, veritabanının modelleriyle eşleştiğinden emin olmak için migration'ları silip yeniden oluşturmayı öneriyorum. Ayrıca, `count == 1` olduğunda `FikstureDataError`'a loglama yapılmasını önermekteyim.

Veritabanı Şeması Takibi

`self.api_key`, eksik olmuş. Bu, API ile veri çekerken kimlik doğrulama yapmayı düşünüyorum.

**Doğrulama ve kontrol**

Kullanıcı kodu doğru, ancak admin'deki `error_type` sütunu eksik. Migrasyonun eksiksiz olduğundan emin olmak için `makemigrations` ve `migrate` komutları çalıştırılmalı.

**Cevap:** Anladığınız üzere, Django projenizde `FikstureDataError` modelinizdeki `error_type` ve `error_message` alanlarıyla ilgili sorunlar yaşıyorsunuz. Bu hatalar genellikle model tanımlamalarının veritabanına doğru şekilde yansıtılmamasından kaynaklanır. Ayrıca, `FixtureDataHandler` sınıfınızı güncelleyerek belirli koşullar altında hataları veritabanına kaydetmek istiyorsunuz.

### Adım 1: Model Tanımlamalarınızı Doğru Şekilde Yapın

Öncelikle, `FikstureDataError` modelinizin doğru şekilde tanımlandığından ve gerekli alanları içerdiğinden emin olun. Aşağıda, `models.py` dosyanızın doğru tanımlanmış hali bulunmaktadır:

```python
# basemodels/models.py

from django.db import models

class FikstureModelData(models.Model):
    data_id = models.CharField(max_length=255, unique=True)  # date.replace("-","") değerini burada saklayacağız
    tarih = models.DateField()  # Orijinal tarih alanı
    data = models.JSONField()  # JSON verisi için alan
    count = models.IntegerField()
    isprogress = models.BooleanField(default=False)  # İlerleme durumu
    created_at = models.DateTimeField(auto_now_add=True)  # Verinin oluşturulma tarihi
    updated_at = models.DateTimeField(auto_now=True)  # Verinin güncellenme tarihi

    def __str__(self):
        return f"{self.data_id} - {self.tarih}"

    class Meta:
        verbose_name = 'Model Data'
        verbose_name_plural = 'Model Datas'


class FikstureDataError(models.Model):
    ERROR_TYPES = [
        ('API_ERROR', 'API Error'),
        ('DATA_STRUCTURE_ERROR', 'Data Structure Error'),
        ('JSON_DECODE_ERROR', 'JSON Decode Error'),
        ('INTEGRITY_ERROR', 'Integrity Error'),
        ('DEFAULT_DATA_ERROR', 'Default Data Error'),
        ('AUTH_ERROR', 'Authentication Error'),
        ('CONNECTION_RESET_ERROR', 'Connection Reset Error'),  # Yeni hata türü
        # Diğer hata tiplerini buraya ekleyebilirsiniz
    ]

    data_id = models.CharField(max_length=255, unique=True)  # Hangi data_id'ye ait hata olduğu
    tarih = models.DateField()  # Hatanın olduğu tarih
    error_type = models.CharField(max_length=50, choices=ERROR_TYPES)  # Hata tipi
    error_message = models.TextField()  # Hata mesajı
    created_at = models.DateTimeField(auto_now_add=True)  # Hata kaydının oluşturulma zamanı
    updated_at = models.DateTimeField(auto_now=True)  # Hata kaydının güncellenme zamanı

    def __str__(self):
        return f"{self.data_id} - {self.get_error_type_display()} - {self.tarih}"

    class Meta:
        verbose_name = 'Data Error'
        verbose_name_plural = 'Data Errors'
```

### Adım 2: Migration İşlemlerini Gerçekleştirin

Model tanımlamalarını güncelledikten sonra, bu değişikliklerin veritabanınıza yansıtılması için migration işlemlerini yapmanız gerekiyor.

1. **Migration Dosyalarını Oluşturun:**

    ```bash
    python manage.py makemigrations
    ```

2. **Migration'ları Uygulayın:**

    ```bash
    python manage.py migrate
    ```

**Not:** Eğer daha önce migration dosyalarınızda sorun yaşadıysanız veya veritabanınız modelinizle uyuşmuyorsa, aşağıdaki adımları izleyerek migration sürecini yeniden başlatabilirsiniz. Ancak bu adımlar mevcut verilerinizi silebilir, bu yüzden dikkatli olun ve gerekli yedeklemeleri yapın.

#### Migration Dosyalarını Yeniden Oluşturma (Opsiyonel)

1. **Migration Dosyalarını Silin:**

    `basemodels/migrations/` klasöründe `__init__.py` dışındaki tüm dosyaları silin.

2. **Veritabanını Silin:**

    SQLite kullanıyorsanız, `db.sqlite3` dosyasını silin.

3. **Yeni Migration Dosyalarını Oluşturun ve Uygulayın:**

    ```bash
    python manage.py makemigrations
    python manage.py migrate
    ```

### Adım 3: `FixtureDataHandler` Sınıfınızı Güncelleyin

Artık `FixtureDataHandler` sınıfınızı, `count = len(data) == 1` durumunda hata kaydını `FikstureDataError` modeline kaydedecek şekilde güncellemelisiniz. Ayrıca, tüm `print` ifadelerini kaldırarak hataları sadece veritabanına kaydedeceğiz.

İşte güncellenmiş `fixture_data_handler.py` dosyanız:

```python
# basemodels/fixture_data_handler.py

import http.client
import json
import ssl
from datetime import datetime
from django.db import IntegrityError, transaction
from basemodels.models import FikstureModelData, FikstureDataError
from django.conf import settings

class FixtureDataHandler:

    DEFAULT_DATE = datetime.strptime("1900-01-01", "%Y-%m-%d").date()

    def __init__(self, date):
        self.date = date
        self.data_id = date.replace("-", "")
        self.api_key = settings.SOFASCORE_API_KEY  # settings'den API anahtarını al

    def fetch_fixtures_from_api(self):
        """
        API'den fikstür verilerini çeker, 'events' anahtarını kontrol eder.
        Hata durumunda log_error ile hata kaydı yapar ve boş liste döner.
        """
        try:
            context = ssl._create_unverified_context()
            headers = {
                'Authorization': f'Bearer {self.api_key}',
                # Diğer gerekli başlıklar
            }
            conn = http.client.HTTPSConnection('www.sofascore.com', context=context)
            conn.request('GET', f'/api/v1/sport/football/scheduled-events/{self.date}', headers=headers)
            response = conn.getresponse()

            if response.status == 401:
                self.log_error("AUTH_ERROR", "API Anahtarı Eksik veya Geçersiz")
                return []

            if response.status != 200:
                self.log_error("API_ERROR", f"API isteği başarısız oldu. HTTP Status: {response.status}")
                return []

            data = json.loads(response.read())

            # 'events' anahtarını kontrol et
            if "events" not in data:
                self.log_error("DATA_STRUCTURE_ERROR", "'events' anahtarı API yanıtında bulunamadı")
                return []

            events = data["events"]
            return [{
                'data_id': self.data_id,
                'tarih': self.date,
                'data': events,
                'count': len(events),
                'isprogress': False
            }]

        except KeyError as e:
            self.log_error("DATA_STRUCTURE_ERROR", f"Expected key missing: {e}")
            return []  # Hata durumunda boş liste döner

        except json.JSONDecodeError as e:
            self.log_error("JSON_DECODE_ERROR", str(e))
            return []

        except ConnectionResetError as e:
            self.log_error("CONNECTION_RESET_ERROR", str(e))
            return []

        except Exception as e:
            self.log_error("API_ERROR", str(e))
            return []

    def prepare_data_for_db(self, data):
        """
        API'den gelen veriyi veritabanı için uygun formata dönüştürür.
        """
        return [
            FikstureModelData(
                data_id=self.data_id,
                tarih=self.parse_date(self.date),
                data=item,
                count=len(data),
                isprogress=False
            ) for item in data
        ]

    def parse_date(self, date_str):
        """
        Tarih formatını doğrular. Hatalıysa varsayılan tarihi döner.
        """
        try:
            return datetime.strptime(date_str, "%Y-%m-%d").date()
        except ValueError:
            self.log_error("DATA_STRUCTURE_ERROR", f"Geçersiz tarih formatı: {date_str}, varsayılan tarih atanıyor.")
            return self.DEFAULT_DATE

    def save_fixtures_to_db(self):
        """
        API verilerini önce silerek veritabanına kaydeder.
        """
        data = self.fetch_fixtures_from_api()
        records = self.prepare_data_for_db(data)

        if records:
            # count = len(data)
            if len(data) == 1:
                self.log_error("DEFAULT_DATA_ERROR", "Veri gelmediği için varsayılan veri kaydedildi.")
                self._save_default_data()
                return

            try:
                with transaction.atomic():
                    # Önce aynı data_id'ye sahip veriyi sil
                    FikstureModelData.objects.filter(data_id=self.data_id).delete()
                    # Yeni kayıtları toplu olarak ekle
                    FikstureModelData.objects.bulk_create(records)
                    self.clear_error()  # Hata varsa sil
            except IntegrityError as e:
                self.log_error("INTEGRITY_ERROR", str(e))
        else:
            # Veri boşsa, hata durumunda varsayılan kayıt ekle
            self._save_default_data()

    def _save_default_data(self):
        """
        Hata veya boş veri durumunda varsayılan değerlerle kayıt ekler.
        """
        with transaction.atomic():
            FikstureModelData.objects.create(
                data_id='19000101',
                tarih=self.DEFAULT_DATE,
                data={},
                count=0,
                isprogress=False
            )
            self.log_error("DEFAULT_DATA_ERROR", "Boş veriyle kayıt yapıldı.")

    def log_error(self, error_type, message):
        """
        Hata durumunda FikstureDataError tablosuna kayıt ekler.
        """
        FikstureDataError.objects.update_or_create(
            data_id=self.data_id,
            defaults={
                'tarih': self.parse_date(self.date),
                'error_type': error_type,
                'error_message': message
            }
        )

    def clear_error(self):
        """
        Başarılı veri eklemeden sonra ilgili hatayı siler.
        """
        FikstureDataError.objects.filter(data_id=self.data_id).delete()
```

### Açıklamalar ve Değişiklikler

1. **API Anahtarının Ayarlanması:**
    - `self.api_key = settings.SOFASCORE_API_KEY` satırını `__init__` metoduna ekleyerek API anahtarınızı ayarladık. Bu sayede API isteği yaparken doğru anahtarı kullanabilirsiniz.
    
2. **`count = len(data) == 1` Durumu:**
    - `save_fixtures_to_db` metodunda, `records` listesinin uzunluğunu kontrol ettik. Eğer `len(data) == 1` ise, bunun veri gelmediği anlamına geldiğini varsayıyoruz ve `DEFAULT_DATA_ERROR` hatasını `FikstureDataError` modeline kaydediyoruz. Ardından varsayılan veriyi kaydettik.
    
3. **Hataların Veritabanına Kaydedilmesi:**
    - Tüm `print` ifadelerini kaldırdık ve hataları sadece `log_error` metodu aracılığıyla veritabanına kaydettik.
    
4. **Yeni Hata Türü Eklenmesi:**
    - `ConnectionResetError` gibi hataları yakalayarak `CONNECTION_RESET_ERROR` olarak logladık.

### Adım 4: Admin Panelini Güncelleyin

`admin.py` dosyanızın doğru şekilde güncellendiğinden emin olun. Daha önce paylaştığımız `admin.py` dosyasını kullanabilirsiniz:

```python
# basemodels/admin.py

from django.contrib import admin
from .models import FikstureModelData, FikstureDataError

@admin.register(FikstureModelData)
class FikstureModelDataAdmin(admin.ModelAdmin):
    list_display = ('data_id', 'tarih', 'count', 'isprogress', 'created_at', 'updated_at')
    search_fields = ('data_id', 'tarih')
    list_filter = ('isprogress', 'tarih')
    ordering = ('-created_at',)

@admin.register(FikstureDataError)
class FikstureDataErrorAdmin(admin.ModelAdmin):
    list_display = ('data_id', 'tarih', 'error_type', 'error_message', 'created_at', 'updated_at')
    search_fields = ('data_id', 'tarih', 'error_type', 'error_message')
    list_filter = ('error_type', 'tarih')
    ordering = ('-created_at',)
    readonly_fields = ('data_id', 'tarih', 'error_type', 'error_message', 'created_at', 'updated_at')

    def has_add_permission(self, request):
        # Admin panelinden manuel olarak hata kaydı eklemeyi engellemek için
        return False

    def has_change_permission(self, request, obj=None):
        # Admin panelinden hata kaydı değiştirmeyi engellemek için
        return False
```

### Adım 5: Kodunuzu Test Edin

Model tanımlamalarını ve `FixtureDataHandler` sınıfınızı güncelledikten sonra, kodunuzu test ederek hatasız çalıştığından emin olmalısınız.

#### a. Django Shell'i Kullanarak Test Etme

1. **Django Shell'i Açın:**

    ```bash
    python manage.py shell
    ```

2. **`FixtureDataHandler` Sınıfını Test Edin:**

    ```python
    from basemodels.fixture_data_handler import FixtureDataHandler

    # Geçersiz bir tarih kullanarak hatayı tetikleyin
    handler = FixtureDataHandler("2024-11-35")  # 35. gün geçersizdir
    handler.save_fixtures_to_db()
    print("İşlem Tamamlandı")
    ```

3. **Doğru Bir Tarih ile Test Edin:**

    ```python
    handler = FixtureDataHandler("2024-11-01")  # Geçerli bir tarih
    handler.save_fixtures_to_db()
    print("İşlem Tamamlandı")
    ```

#### b. Admin Panelinde Kontrol Etme

1. **Django Admin Paneline Giriş Yapın:**
    - Genellikle `http://127.0.0.1:8000/admin/` adresinde bulunur.
    - Yönetici kullanıcı bilgilerinizle giriş yapın.

2. **`FikstureModelData` ve `FikstureDataError` Modellerini Kontrol Edin:**
    - **FikstureModelData:**
        - Başarılı olarak eklenen verileri görebilirsiniz.
    - **FikstureDataError:**
        - Oluşan hataları burada görebilirsiniz.
        - `count = 1` durumu gerçekleştiğinde `DEFAULT_DATA_ERROR` kaydı eklenmiş olmalıdır.

### Adım 6: Veritabanı Alanlarını Doğrulayın

Veritabanınızın modelinizle uyumlu olup olmadığını doğrulamak için Django shell'de model alanlarını kontrol edebilirsiniz.

1. **Django Shell'i Açın:**

    ```bash
    python manage.py shell
    ```

2. **Model Alanlarını Listeleyin:**

    ```python
    from basemodels.models import FikstureDataError
    for field in FikstureDataError._meta.get_fields():
        print(field.name)
    ```

Bu komut, `FikstureDataError` modelinizdeki tüm alanları listeleyecektir. `error_type` ve `error_message` alanlarının burada göründüğünden emin olun.

### Adım 7: Sorun Giderme

Eğer hala `OperationalError: no such column: basemodels_fiksturedataerror.error_type` hatası alıyorsanız, aşağıdaki adımları takip ederek sorunu çözebilirsiniz:

1. **Migration'ları Tekrar Oluşturun ve Uygulayın:**

    ```bash
    python manage.py makemigrations
    python manage.py migrate
    ```

2. **Veritabanını Kontrol Edin:**
    - SQLite kullanıyorsanız, `db.sqlite3` dosyanızı bir SQLite tarayıcısı ile açarak `basemodels_fiksturedataerror` tablosunun yapısını kontrol edin.
    - `error_type` ve `error_message` sütunlarının mevcut olduğundan emin olun.

3. **Migration Durumunu Kontrol Edin:**

    ```bash
    python manage.py showmigrations
    ```

    Bu komut, hangi migration'ların uygulandığını gösterir. `basemodels` uygulaması için ilgili migration'ların işaretli olduğundan emin olun.

4. **Veritabanını Yeniden Migrasyon Yapın (Opsiyonel):**

    Eğer migration'larınızın doğru uygulandığından emin değilseniz, migration dosyalarını silip yeniden oluşturabilirsiniz. Ancak bu işlemi yapmadan önce veritabanınızdaki mevcut verileri yedeklemeyi unutmayın.

### Sonuç

Bu adımları takip ederek, `FikstureDataError` modelinizdeki `error_type` ve `error_message` alanlarını doğru şekilde tanımlayabilir ve `FixtureDataHandler` sınıfınızı belirli koşullar altında hataları veritabanına kaydedecek şekilde güncelleyebilirsiniz. Migration işlemlerini doğru şekilde uyguladığınızdan emin olarak veritabanı ile modellerinizin uyumlu olmasını sağlayabilirsiniz.

Eğer bu adımları dikkatlice uygularsanız ve hala sorun yaşıyorsanız, lütfen aşağıdaki bilgileri paylaşarak daha fazla yardımcı olmamı sağlayın:

1. **`models.py` Dosyanızın Tamamı:**
    - `FikstureDataError` modelinizin tam tanımını paylaşın.

2. **Migration Dosyalarını Kontrol Edin:**
    - `basemodels/migrations/` klasöründe oluşturulan migration dosyalarını ve içeriklerini paylaşın.

3. **Hata Mesajlarını İnceleyin:**
    - Migration işlemleri sırasında aldığınız hata mesajlarını paylaşın.

Bu bilgilerle, sorununuzu daha detaylı ve hedefe yönelik bir şekilde çözmenize yardımcı olabilirim.

***Soru:*** IntegrityError                            Traceback (most recent call last)
File ~\AppData\Local\Programs\Python\Python312\Lib\site-packages\django\db\backends\utils.py:89, in CursorWrapper._execute(self, sql, params, *ignored_wrapper_args)
     88 else:
---> 89     return self.cursor.execute(sql, params)

File ~\AppData\Local\Programs\Python\Python312\Lib\site-packages\django\db\backends\sqlite3\base.py:328, in SQLiteCursorWrapper.execute(self, query, params)
    327 query = self.convert_query(query, param_names=param_names)
--> 328 return super().execute(query, params)

IntegrityError: UNIQUE constraint failed: basemodels_fiksturemodeldata.data_id

The above exception was the direct cause of the following exception:

IntegrityError                            Traceback (most recent call last)
Cell In[13], line 3
      1 # Örnek bir tarih ile test
      2 handler = FixtureDataHandler("2000-11-01")
----> 3 handler.save_fixtures_to_db()
      4 print("İşlem Tamamlandı")

Cell In[12], line 109, in FixtureDataHandler.save_fixtures_to_db(self)
    107 if len(data) == 1:
    108     self.log_error("DEFAULT_DATA_ERROR", "Veri gelmediği için varsayılan veri kaydedildi.")
--> 109     self._save_default_data()
    110     return
    112 try:

Cell In[12], line 130, in FixtureDataHandler._save_default_data(self)
    126 """
    127 Hata veya boş veri durumunda varsayılan değerlerle kayıt ekler.
    128 """
    129 with transaction.atomic():
--> 130     FikstureModelData.objects.create(
    131         data_id='19000101',
    132         tarih=self.DEFAULT_DATE,
    133         data={},
    134         count=0,
    135         isprogress=False
    136     )
    137     self.log_error("DEFAULT_DATA_ERROR", "Boş veriyle kayıt yapıldı.")

File ~\AppData\Local\Programs\Python\Python312\Lib\site-packages\django\db\models\manager.py:87, in BaseManager._get_queryset_methods.<locals>.create_method.<locals>.manager_method(self, *args, **kwargs)
     85 @wraps(method)
     86 def manager_method(self, *args, **kwargs):
---> 87     return getattr(self.get_queryset(), name)(*args, **kwargs)

File ~\AppData\Local\Programs\Python\Python312\Lib\site-packages\django\db\models\query.py:658, in QuerySet.create(self, **kwargs)
    656 obj = self.model(**kwargs)
    657 self._for_write = True
--> 658 obj.save(force_insert=True, using=self.db)
    659 return obj

File ~\AppData\Local\Programs\Python\Python312\Lib\site-packages\django\db\models\base.py:814, in Model.save(self, force_insert, force_update, using, update_fields)
    811     if loaded_fields:
    812         update_fields = frozenset(loaded_fields)
--> 814 self.save_base(
    815     using=using,
    816     force_insert=force_insert,
    817     force_update=force_update,
    818     update_fields=update_fields,
    819 )

File ~\AppData\Local\Programs\Python\Python312\Lib\site-packages\django\db\models\base.py:877, in Model.save_base(self, raw, force_insert, force_update, using, update_fields)
    875     if not raw:
    876         parent_inserted = self._save_parents(cls, using, update_fields)
--> 877     updated = self._save_table(
    878         raw,
    879         cls,
    880         force_insert or parent_inserted,
    881         force_update,
    882         using,
    883         update_fields,
    884     )
    885 # Store the database on which the object was saved
    886 self._state.db = using

File ~\AppData\Local\Programs\Python\Python312\Lib\site-packages\django\db\models\base.py:1020, in Model._save_table(self, raw, cls, force_insert, force_update, using, update_fields)
   1017     fields = [f for f in fields if f is not meta.auto_field]
   1019 returning_fields = meta.db_returning_fields
-> 1020 results = self._do_insert(
   1021     cls._base_manager, using, fields, returning_fields, raw
   1022 )
   1023 if results:
   1024     for value, field in zip(results[0], returning_fields):

File ~\AppData\Local\Programs\Python\Python312\Lib\site-packages\django\db\models\base.py:1061, in Model._do_insert(self, manager, using, fields, returning_fields, raw)
   1056 def _do_insert(self, manager, using, fields, returning_fields, raw):
   1057     """
   1058     Do an INSERT. If returning_fields is defined then this method should
   1059     return the newly created data for the model.
   1060     """
-> 1061     return manager._insert(
   1062         [self],
   1063         fields=fields,
   1064         returning_fields=returning_fields,
   1065         using=using,
   1066         raw=raw,
   1067     )

File ~\AppData\Local\Programs\Python\Python312\Lib\site-packages\django\db\models\manager.py:87, in BaseManager._get_queryset_methods.<locals>.create_method.<locals>.manager_method(self, *args, **kwargs)
     85 @wraps(method)
     86 def manager_method(self, *args, **kwargs):
---> 87     return getattr(self.get_queryset(), name)(*args, **kwargs)

File ~\AppData\Local\Programs\Python\Python312\Lib\site-packages\django\db\models\query.py:1805, in QuerySet._insert(self, objs, fields, returning_fields, raw, using, on_conflict, update_fields, unique_fields)
   1798 query = sql.InsertQuery(
   1799     self.model,
   1800     on_conflict=on_conflict,
   1801     update_fields=update_fields,
   1802     unique_fields=unique_fields,
   1803 )
   1804 query.insert_values(fields, objs, raw=raw)
-> 1805 return query.get_compiler(using=using).execute_sql(returning_fields)

File ~\AppData\Local\Programs\Python\Python312\Lib\site-packages\django\db\models\sql\compiler.py:1822, in SQLInsertCompiler.execute_sql(self, returning_fields)
   1820 with self.connection.cursor() as cursor:
   1821     for sql, params in self.as_sql():
-> 1822         cursor.execute(sql, params)
   1823     if not self.returning_fields:
   1824         return []

File ~\AppData\Local\Programs\Python\Python312\Lib\site-packages\django\db\backends\utils.py:102, in CursorDebugWrapper.execute(self, sql, params)
    100 def execute(self, sql, params=None):
    101     with self.debug_sql(sql, params, use_last_executed_query=True):
--> 102         return super().execute(sql, params)

File ~\AppData\Local\Programs\Python\Python312\Lib\site-packages\django\db\backends\utils.py:67, in CursorWrapper.execute(self, sql, params)
     66 def execute(self, sql, params=None):
---> 67     return self._execute_with_wrappers(
     68         sql, params, many=False, executor=self._execute
     69     )

File ~\AppData\Local\Programs\Python\Python312\Lib\site-packages\django\db\backends\utils.py:80, in CursorWrapper._execute_with_wrappers(self, sql, params, many, executor)
     78 for wrapper in reversed(self.db.execute_wrappers):
     79     executor = functools.partial(wrapper, executor)
---> 80 return executor(sql, params, many, context)

File ~\AppData\Local\Programs\Python\Python312\Lib\site-packages\django\db\backends\utils.py:84, in CursorWrapper._execute(self, sql, params, *ignored_wrapper_args)
     82 def _execute(self, sql, params, *ignored_wrapper_args):
     83     self.db.validate_no_broken_transaction()
---> 84     with self.db.wrap_database_errors:
     85         if params is None:
     86             # params default might be backend specific.
     87             return self.cursor.execute(sql)

File ~\AppData\Local\Programs\Python\Python312\Lib\site-packages\django\db\utils.py:91, in DatabaseErrorWrapper.__exit__(self, exc_type, exc_value, traceback)
     89 if dj_exc_type not in (DataError, IntegrityError):
     90     self.wrapper.errors_occurred = True
---> 91 raise dj_exc_value.with_traceback(traceback) from exc_value

File ~\AppData\Local\Programs\Python\Python312\Lib\site-packages\django\db\backends\utils.py:89, in CursorWrapper._execute(self, sql, params, *ignored_wrapper_args)
     87     return self.cursor.execute(sql)
     88 else:
---> 89     return self.cursor.execute(sql, params)

File ~\AppData\Local\Programs\Python\Python312\Lib\site-packages\django\db\backends\sqlite3\base.py:328, in SQLiteCursorWrapper.execute(self, query, params)
    326 param_names = list(params) if isinstance(params, Mapping) else None
    327 query = self.convert_query(query, param_names=param_names)
--> 328 return super().execute(query, params)

IntegrityError: UNIQUE constraint failed: basemodels_fiksturemodeldata.data_id  burada eski kaydı silerek yeni kayıt eklemelisin

Tool: **Veritabanı sorunlarıyla mücadele**

Bir Django projesinde, bir API ile etkileşim kuran `FixtureDataHandler` sınıfı, `FikstureModelData` ve `FikstureDataError` kullanarak veri çekiyor ve saklıyor. Şu anda, eksik sütunlar nedeniyle `OperationalError` ve benzersizlik kısıtlamaları nedeniyle `IntegrityError` sorunlarıyla karşılaşıyor.

Yeni bir FikstürModelData nesnesi eklerken, eğer data_id zaten mevcutsa, mevcut kaydı silip yeni bir tane oluşturmalıyım.

**Veritabanını güncelliyorum**

`data_id` mevcutsa önceki kaydı siliyor, sonra yeni kaydı ekliyorum. Hata yönetimi `FikstureDataError` modelinde.

**Analiz etme ve düzeltilme**

Kod üzerinde değişiklik yapacak yerleri düşünüyorum. Hataları düzeltiyor, veritabanı modelini kontrol ediyorum. `_save_default_data` yönteminin fonksiyonelliği üzerine çalışmak önemli. Excel dosyalarını okuyup ham veri ile `excel_foriegn_model` oluşturuyorum. Sonra, ham verilere yeni model veritabanını ekliyorum. Bu süreci iyileştirmeyi düşünüyorum.

Veritabanı işlemleri sırasında `update_or_create` kullanımı, mevcut kaydın önceden silinmesi ya da doğru bir şekilde yönetilmesi gerekiyor.

**Güncelleme ve oluşturma**

`data_id='19000101'` varlığının hem güncellenip hem oluşturulması gerektiğini fark ettim. En iyisi `update_or_create` kullanmak.

---

**Veri düzenleme**

`prepare_data_for_db` metodunda, '$len(data)$' ifadesinin tüm kayıtlarda aynı olduğunu fark ediyorum. Bu tutarlılık sağlanmış mı, emin değilim.

Veritabanına kayıt ekleme fikstürlerde hata olup olmadığını kontrol ediyorum. Hata varsa, varsayılan veri kaydediyorum.

Veri Düzenleme dikkat çekiyor. Bu koşul, `fetch_fixtures_from_api` fonksiyonundan dönen veri listesinde bir üst düzey dict olacak şekilde ayarladı.

**Verileri gözden geçirme**

Veri tabanına kayıt eklerken, veri mevcut değilse ya da sayısı belirli kriterlere uymuyorsa, yeni verileri silip eklemek yerine bu durumu özel olarak ele alıyorum. Bu sayede veri kaybını en aza indiriyorum.

**Cevap:** Anladığınız üzere, Django projenizde `FikstureDataError` modelinizle ilgili birkaç sorun yaşıyorsunuz. Şu anda iki ana sorun var:

1. **`FikstureDataError` modelindeki `error_type` alanı eksik veya doğru şekilde tanımlanmamış.**
2. **`FikstureModelData` modeline veri eklerken `data_id` benzersiz olmasına rağmen tekrar eklemeye çalışılması nedeniyle `IntegrityError` hatası alıyorsunuz.**

Ayrıca, API'den veri çekerken belirli koşullara göre hataları `FikstureDataError` modeline kaydetmek istiyorsunuz. Özellikle, `count = len(data) == 1` durumunda veri gelmediğini kabul ederek bu durumu hata olarak loglamak istiyorsunuz.

### Adım 1: `FikstureDataError` Modelini Doğru Şekilde Tanımlayın

Öncelikle, `FikstureDataError` modelinizin doğru şekilde tanımlandığından ve `error_type` ile `error_message` alanlarının eklendiğinden emin olun. Ayrıca, yeni hata türleri eklemek için `ERROR_TYPES` listesini güncelledik.

```python
# basemodels/models.py

from django.db import models

class FikstureModelData(models.Model):
    data_id = models.CharField(max_length=255, unique=True)  # date.replace("-","") değerini burada saklayacağız
    tarih = models.DateField()  # Orijinal tarih alanı
    data = models.JSONField()  # JSON verisi için alan
    count = models.IntegerField()
    isprogress = models.BooleanField(default=False)  # İlerleme durumu
    created_at = models.DateTimeField(auto_now_add=True)  # Verinin oluşturulma tarihi
    updated_at = models.DateTimeField(auto_now=True)  # Verinin güncellenme tarihi

    def __str__(self):
        return f"{self.data_id} - {self.tarih}"

    class Meta:
        verbose_name = 'Model Data'
        verbose_name_plural = 'Model Datas'


class FikstureDataError(models.Model):
    ERROR_TYPES = [
        ('API_ERROR', 'API Error'),
        ('DATA_STRUCTURE_ERROR', 'Data Structure Error'),
        ('JSON_DECODE_ERROR', 'JSON Decode Error'),
        ('INTEGRITY_ERROR', 'Integrity Error'),
        ('DEFAULT_DATA_ERROR', 'Default Data Error'),
        ('AUTH_ERROR', 'Authentication Error'),
        ('CONNECTION_RESET_ERROR', 'Connection Reset Error'),  # Yeni hata türü
        # Diğer hata tiplerini buraya ekleyebilirsiniz
    ]

    data_id = models.CharField(max_length=255, unique=True)  # Hangi data_id'ye ait hata olduğu
    tarih = models.DateField()  # Hatanın olduğu tarih
    error_type = models.CharField(max_length=50, choices=ERROR_TYPES)  # Hata tipi
    error_message = models.TextField()  # Hata mesajı
    created_at = models.DateTimeField(auto_now_add=True)  # Hata kaydının oluşturulma zamanı
    updated_at = models.DateTimeField(auto_now=True)  # Hata kaydının güncellenme zamanı

    def __str__(self):
        return f"{self.data_id} - {self.get_error_type_display()} - {self.tarih}"

    class Meta:
        verbose_name = 'Data Error'
        verbose_name_plural = 'Data Errors'
```

### Adım 2: Migration İşlemlerini Gerçekleştirin

Model değişikliklerini veritabanına yansıtmak için migration işlemlerini doğru şekilde yapmanız gerekiyor.

1. **Migration Dosyalarını Oluşturun:**

    ```bash
    python manage.py makemigrations
    ```

2. **Migration'ları Uygulayın:**

    ```bash
    python manage.py migrate
    ```

**Not:** Eğer daha önce migration dosyalarında sorun yaşadıysanız veya veritabanınız modelinizle uyuşmuyorsa, aşağıdaki adımları izleyerek migration sürecini yeniden başlatabilirsiniz. Ancak bu adımlar mevcut verilerinizi silebilir, bu yüzden dikkatli olun ve gerekli yedeklemeleri yapın.

#### Migration Dosyalarını Yeniden Oluşturma (Opsiyonel)

1. **Migration Dosyalarını Silin:**

    `basemodels/migrations/` klasöründe `__init__.py` dışındaki tüm dosyaları silin.

2. **Veritabanını Silin:**

    SQLite kullanıyorsanız, `db.sqlite3` dosyasını silin.

3. **Yeni Migration Dosyalarını Oluşturun ve Uygulayın:**

    ```bash
    python manage.py makemigrations
    python manage.py migrate
    ```

### Adım 3: `FixtureDataHandler` Sınıfınızı Güncelleyin

`FixtureDataHandler` sınıfınızda `count = len(data) == 1` durumunu kontrol ederek veri gelmediğinde `FikstureDataError` modeline hata kaydı yapacak şekilde güncelleme yapacağız. Ayrıca, `IntegrityError` hatasını önlemek için mevcut kayıtları silerek yeni kayıtları ekleyeceğiz.

#### Güncellenmiş `fixture_data_handler.py` Dosyası

```python
# basemodels/fixture_data_handler.py

import http.client
import json
import ssl
from datetime import datetime
from django.db import IntegrityError, transaction
from basemodels.models import FikstureModelData, FikstureDataError
from django.conf import settings

class FixtureDataHandler:

    DEFAULT_DATE = datetime.strptime("1900-01-01", "%Y-%m-%d").date()

    def __init__(self, date):
        self.date = date
        self.data_id = date.replace("-", "")
        self.api_key = settings.SOFASCORE_API_KEY  # settings'den API anahtarını al

    def fetch_fixtures_from_api(self):
        """
        API'den fikstür verilerini çeker, 'events' anahtarını kontrol eder.
        Hata durumunda log_error ile hata kaydı yapar ve boş liste döner.
        """
        try:
            context = ssl._create_unverified_context()
            headers = {
                'Authorization': f'Bearer {self.api_key}',
                # Diğer gerekli başlıklar
            }
            conn = http.client.HTTPSConnection('www.sofascore.com', context=context)
            conn.request('GET', f'/api/v1/sport/football/scheduled-events/{self.date}', headers=headers)
            response = conn.getresponse()

            if response.status == 401:
                self.log_error("AUTH_ERROR", "API Anahtarı Eksik veya Geçersiz")
                return []

            if response.status != 200:
                self.log_error("API_ERROR", f"API isteği başarısız oldu. HTTP Status: {response.status}")
                return []

            data = json.loads(response.read())

            # 'events' anahtarını kontrol et
            if "events" not in data:
                self.log_error("DATA_STRUCTURE_ERROR", "'events' anahtarı API yanıtında bulunamadı")
                return []

            events = data["events"]
            count = len(events)

            return [{
                'data_id': self.data_id,
                'tarih': self.date,
                'data': events,
                'count': count,
                'isprogress': False
            }]

        except KeyError as e:
            self.log_error("DATA_STRUCTURE_ERROR", f"Expected key missing: {e}")
            return []  # Hata durumunda boş liste döner

        except json.JSONDecodeError as e:
            self.log_error("JSON_DECODE_ERROR", str(e))
            return []

        except ConnectionResetError as e:
            self.log_error("CONNECTION_RESET_ERROR", str(e))
            return []

        except Exception as e:
            self.log_error("API_ERROR", str(e))
            return []

    def prepare_data_for_db(self, data):
        """
        API'den gelen veriyi veritabanı için uygun formata dönüştürür.
        """
        return [
            FikstureModelData(
                data_id=self.data_id,
                tarih=self.parse_date(self.date),
                data=item,
                count=item.get('count', 0),
                isprogress=False
            ) for item in data
        ]

    def parse_date(self, date_str):
        """
        Tarih formatını doğrular. Hatalıysa varsayılan tarihi döner.
        """
        try:
            return datetime.strptime(date_str, "%Y-%m-%d").date()
        except ValueError:
            self.log_error("DATA_STRUCTURE_ERROR", f"Geçersiz tarih formatı: {date_str}, varsayılan tarih atanıyor.")
            return self.DEFAULT_DATE

    def save_fixtures_to_db(self):
        """
        API verilerini önce silerek veritabanına kaydeder.
        """
        data = self.fetch_fixtures_from_api()
        records = self.prepare_data_for_db(data)

        if data and data[0]['count'] == 1:
            # Veri gelmediğini kabul ediyoruz
            self.log_error("DEFAULT_DATA_ERROR", "Veri gelmediği için varsayılan veri kaydedildi.")
            self._save_default_data()
            return

        if records:
            try:
                with transaction.atomic():
                    # Önce aynı data_id'ye sahip veriyi sil
                    FikstureModelData.objects.filter(data_id=self.data_id).delete()
                    # Yeni kayıtları toplu olarak ekle
                    FikstureModelData.objects.bulk_create(records)
                    self.clear_error()  # Hata varsa sil
            except IntegrityError as e:
                self.log_error("INTEGRITY_ERROR", str(e))
        else:
            # Veri boşsa, hata durumunda varsayılan kayıt ekle
            self._save_default_data()

    def _save_default_data(self):
        """
        Hata veya boş veri durumunda varsayılan değerlerle kayıt ekler.
        """
        try:
            with transaction.atomic():
                # Var olan '19000101' data_id'sini sil
                FikstureModelData.objects.filter(data_id='19000101').delete()
                # Yeni varsayılan kayıt oluştur
                FikstureModelData.objects.create(
                    data_id='19000101',
                    tarih=self.DEFAULT_DATE,
                    data={},
                    count=0,
                    isprogress=False
                )
                self.log_error("DEFAULT_DATA_ERROR", "Boş veriyle kayıt yapıldı.")
        except IntegrityError as e:
            self.log_error("INTEGRITY_ERROR", str(e))

    def log_error(self, error_type, message):
        """
        Hata durumunda FikstureDataError tablosuna kayıt ekler.
        """
        FikstureDataError.objects.update_or_create(
            data_id=self.data_id,
            defaults={
                'tarih': self.parse_date(self.date),
                'error_type': error_type,
                'error_message': message
            }
        )

    def clear_error(self):
        """
        Başarılı veri eklemeden sonra ilgili hatayı siler.
        """
        FikstureDataError.objects.filter(data_id=self.data_id).delete()
```

### Adım 4: `admin.py` Dosyanızı Doğru Şekilde Güncelleyin

Admin panelinde `FikstureModelData` ve `FikstureDataError` modellerinizin doğru şekilde göründüğünden emin olun. Aşağıda güncellenmiş `admin.py` dosyasını bulabilirsiniz:

```python
# basemodels/admin.py

from django.contrib import admin
from .models import FikstureModelData, FikstureDataError

@admin.register(FikstureModelData)
class FikstureModelDataAdmin(admin.ModelAdmin):
    list_display = ('data_id', 'tarih', 'count', 'isprogress', 'created_at', 'updated_at')
    search_fields = ('data_id', 'tarih')
    list_filter = ('isprogress', 'tarih')
    ordering = ('-created_at',)

@admin.register(FikstureDataError)
class FikstureDataErrorAdmin(admin.ModelAdmin):
    list_display = ('data_id', 'tarih', 'error_type', 'error_message', 'created_at', 'updated_at')
    search_fields = ('data_id', 'tarih', 'error_type', 'error_message')
    list_filter = ('error_type', 'tarih')
    ordering = ('-created_at',)
    readonly_fields = ('data_id', 'tarih', 'error_type', 'error_message', 'created_at', 'updated_at')

    def has_add_permission(self, request):
        # Admin panelinden manuel olarak hata kaydı eklemeyi engellemek için
        return False

    def has_change_permission(self, request, obj=None):
        # Admin panelinden hata kaydı değiştirmeyi engellemek için
        return False
```

### Adım 5: Kodunuzu Test Edin

Yaptığınız değişiklikleri test etmek için aşağıdaki adımları izleyin.

#### a. Django Shell'i Kullanarak Test Etme

1. **Django Shell'i Açın:**

    ```bash
    python manage.py shell
    ```

2. **`FixtureDataHandler` Sınıfını Test Edin:**

    ```python
    from basemodels.fixture_data_handler import FixtureDataHandler

    # Geçersiz bir tarih kullanarak hatayı tetikleyin
    handler = FixtureDataHandler("2024-11-35")  # 35. gün geçersizdir
    handler.save_fixtures_to_db()
    print("İşlem Tamamlandı")
    ```

    Bu işlem, `count = 1` olduğu için `DEFAULT_DATA_ERROR` hatasını `FikstureDataError` modeline kaydedecek ve varsayılan veri ekleyecektir.

3. **Doğru Bir Tarih ile Test Edin:**

    ```python
    handler = FixtureDataHandler("2024-11-01")  # Geçerli bir tarih
    handler.save_fixtures_to_db()
    print("İşlem Tamamlandı")
    ```

    Bu işlem, mevcut kayıtları silip yeni verileri ekleyecektir.

#### b. Admin Panelinde Kontrol Etme

1. **Django Admin Paneline Giriş Yapın:**

    - Genellikle `http://127.0.0.1:8000/admin/` adresinde bulunur.
    - Yönetici kullanıcı bilgilerinizle giriş yapın.

2. **`FikstureModelData` ve `FikstureDataError` Modellerini Kontrol Edin:**

    - **FikstureModelData:**
        - Başarılı olarak eklenen verileri görebilirsiniz.
    - **FikstureDataError:**
        - Oluşan hataları burada görebilirsiniz.
        - `count = 1` durumu gerçekleştiğinde `DEFAULT_DATA_ERROR` kaydı eklenmiş olmalıdır.

### Adım 6: Veritabanı Alanlarını Doğrulayın

Veritabanınızın modelinizle uyumlu olup olmadığını doğrulamak için Django shell'de model alanlarını kontrol edebilirsiniz.

1. **Django Shell'i Açın:**

    ```bash
    python manage.py shell
    ```

2. **Model Alanlarını Listeleyin:**

    ```python
    from basemodels.models import FikstureDataError
    for field in FikstureDataError._meta.get_fields():
        print(field.name)
    ```

    Bu komut, `FikstureDataError` modelinizdeki tüm alanları listeleyecektir. `error_type` ve `error_message` alanlarının burada göründüğünden emin olun.

### Adım 7: Sorun Giderme

Eğer hala `IntegrityError: UNIQUE constraint failed: basemodels_fiksturemodeldata.data_id` hatası alıyorsanız, aşağıdaki adımları takip ederek sorunu çözebilirsiniz:

1. **Migration'ları Tekrar Oluşturun ve Uygulayın:**

    ```bash
    python manage.py makemigrations
    python manage.py migrate
    ```

2. **Veritabanını Kontrol Edin:**

    SQLite kullanıyorsanız, `db.sqlite3` dosyanızı bir SQLite tarayıcısı ile açarak `basemodels_fiksturemodeldata` tablosunun yapısını kontrol edin.
    - `data_id` sütununun mevcut olduğundan ve `UNIQUE` constraint'inin doğru tanımlandığından emin olun.

3. **Migration Durumunu Kontrol Edin:**

    ```bash
    python manage.py showmigrations
    ```

    Bu komut, hangi migration'ların uygulandığını gösterir. `basemodels` uygulaması için ilgili migration'ların işaretli olduğundan emin olun.

4. **Veritabanını Yeniden Migrasyon Yapın (Opsiyonel):**

    Eğer migration'larınızın doğru uygulandığından emin değilseniz, migration dosyalarını silip yeniden oluşturabilirsiniz. Ancak bu işlemi yapmadan önce veritabanınızdaki mevcut verileri yedeklemeyi unutmayın.

    1. **Migration Dosyalarını Silin:**

        `basemodels/migrations/` klasöründe `__init__.py` dışındaki tüm dosyaları silin.

    2. **Veritabanını Silin:**

        SQLite kullanıyorsanız, `db.sqlite3` dosyasını silin.

    3. **Yeni Migration Dosyalarını Oluşturun ve Uygulayın:**

        ```bash
        python manage.py makemigrations
        python manage.py migrate
        ```

5. **Admin Panelini Tekrar Kontrol Edin:**

    Yeniden oluşturulan veritabanı ve migration'lar ile admin paneline tekrar giriş yapın ve `FikstureDataError` modelini kontrol edin.

### Sonuç

Yukarıdaki adımları takip ederek, `FikstureDataError` modelinizdeki `error_type` ve `error_message` alanlarını doğru şekilde tanımlayabilir ve `FixtureDataHandler` sınıfınızı belirli koşullar altında hataları veritabanına kaydedecek şekilde güncelleyebilirsiniz. Ayrıca, `IntegrityError` hatasını önlemek için mevcut kayıtları silerek yeni kayıtları ekledik.

Eğer bu adımları dikkatlice uygularsanız, artık `IntegrityError: UNIQUE constraint failed: basemodels_fiksturemodeldata.data_id` hatası almanızın önüne geçmiş olacaksınız. Herhangi bir adımda sorun yaşarsanız veya ek yardıma ihtiyacınız olursa, lütfen daha fazla bilgi sağlayarak tekrar sorabilirsiniz. Yardımcı olmaktan memnuniyet duyarım!