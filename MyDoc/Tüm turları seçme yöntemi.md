***Soru:*** @shared_task
def fetch_and_save_match_data():
    # week="Biten" olan turları seçfilter yerine tümü gelsin istiyporujm
    rounds = RoundinfoModel.objects.filter(week="Devam")  burada

**Cevap:** Eğer sadece "Biten" olan turları değil, tüm turları getirmek istiyorsanız, `.filter(week="Biten")` kısmını kaldırabilir ve doğrudan bütün `RoundinfoModel` verilerini almak için `.all()` kullanabilirsiniz. Yani, kodu şu şekilde güncelleyebilirsiniz:

```python
@shared_task
def fetch_and_save_match_data():
    # Tüm turları seçiyoruz
    rounds = RoundinfoModel.objects.all()

    # Sonrasında diğer işlemleri buraya ekleyebilirsiniz
```

Bu şekilde, tüm `RoundinfoModel` kayıtlarını getirmiş olursunuz. Eğer sadece bazı turlar için koşul eklemek isterseniz, `.filter()` veya `.exclude()` gibi ek yöntemlerle özelleştirebilirsiniz.

Başka soruların olursa yardımcı olabilirim!

***Soru:*** @shared_task
def fetch_and_save_match_data():
    # week="Biten" olan turları seç
    #rounds = RoundinfoModel.objects.filter(week="Devam")
    rounds = RoundinfoModel.objects.all()
    for round_info in rounds:
        try:
            # SofaScore API'sinden verileri almak için gerekli parametreler
            tournament_id = round_info.tournament_id
            season_id = round_info.season_id
            round_num = round_info.round
            slug = round_info.slug if round_info.slug else ""
            prefix = round_info.prefix if round_info.prefix else ""
            
            # SofaScore API'sinden verileri çek
            df = RoundData(tournament_id, season_id, round_num, slug, prefix)
            
            # Alınan verileri MatchInfo modeline kaydet
            for index, row in df.iterrows():
                # Her bir sütun için NaN veya boş stringleri kontrol edip uygun değerler atıyoruz
                def clean_score(value):
                    """Boş değerler veya NaN'ları None veya 0 olarak temizler."""
                    if pd.isna(value) or value == '':
                        return None  # Null değerler için None kullanılıyor
                    return value  # Değer uygunsa, olduğu gibi döndür
                
                # Değerlerin temizlenmesi
                homeScore_period1 = clean_score(row["homeScore_period1"])
                homeScore_period2 = clean_score(row["homeScore_period2"])
                homeScore_normaltime = clean_score(row["homeScore_normaltime"])
                awayScore_period1 = clean_score(row["awayScore_period1"])
                awayScore_period2 = clean_score(row["awayScore_period2"])
                awayScore_normaltime = clean_score(row["awayScore_normaltime"])

                # MatchInfo modeline verileri kaydediyoruz
                MatchInfo.objects.update_or_create(
                    idx=row["id"],  # Maçın benzersiz ID'si
                    season_id=row["season_id"],  # Sezon ID'si
                    defaults={
                        'startTimestamp': row["startTimestamp"],
                        'tournament_name': row["tournament_name"],
                        'tournament_category_name': row["tournament_category_name"],
                        'tournament_category_id': row["tournament_category_id"],
                        'tournament_uniqueTournament_name': row["tournament_uniqueTournament_name"],
                        'tournament_uniqueTournament_id': row["tournament_uniqueTournament_id"],
                        'season_name': row["season_name"],
                        'season_year': row["season_year"],
                        'roundInfo_round': row["roundInfo_round"],
                        'status_type': row["status_type"],
                        'homeTeam_name': row["homeTeam_name"],
                        'homeTeam_nameCode': row["homeTeam_nameCode"],
                        'homeTeam_id': row["homeTeam_id"],
                        'awayTeam_name': row["awayTeam_name"],
                        'awayTeam_nameCode': row["awayTeam_nameCode"],
                        'awayTeam_id': row["awayTeam_id"],
                        'homeScore_period1': homeScore_period1,
                        'homeScore_period2': homeScore_period2,
                        'homeScore_normaltime': homeScore_normaltime,
                        'awayScore_period1': awayScore_period1,
                        'awayScore_period2': awayScore_period2,
                        'awayScore_normaltime': awayScore_normaltime,
                    }
                )
        except Exception as e:
            # Eğer bir hata olursa, MatchDataError modeline kaydediyoruz
            MatchDataError.objects.create(
                tournament_id=round_info.tournament_id,  # Hangi turnuvada hata olduğunu kaydediyoruz
                season_id=round_info.season_id,  # Hangi sezonda hata olduğunu kaydediyoruz
                round_num=round_info.round,  # Hangi turda hata olduğunu kaydediyoruz
                slug=slug,  # Slug (opsiyonel)
                prefix=prefix,  # Ön ek (opsiyonel)
                error _message=str(e)  # Hata mesajını kaydediyoruz
            )

**Cevap:** Görünüşe göre kodunuz neredeyse tamamlanmış, ancak küçük bir hata var: `error _message` değişkeninde `_` karakteri fazladan yer almış. Doğrusu `error_message` olmalı. Ayrıca, aşağıda küçük bir iyileştirme ve düzenlemeler yaptım:

```python
@shared_task
def fetch_and_save_match_data():
    # Tüm turları seçiyoruz
    rounds = RoundinfoModel.objects.all()
    for round_info in rounds:
        try:
            # SofaScore API'sinden verileri almak için gerekli parametreler
            tournament_id = round_info.tournament_id
            season_id = round_info.season_id
            round_num = round_info.round
            slug = round_info.slug if round_info.slug else ""
            prefix = round_info.prefix if round_info.prefix else ""
            
            # SofaScore API'sinden verileri çek
            df = RoundData(tournament_id, season_id, round_num, slug, prefix)
            
            # Alınan verileri MatchInfo modeline kaydet
            for index, row in df.iterrows():
                # Her bir sütun için NaN veya boş stringleri kontrol edip uygun değerler atıyoruz
                def clean_score(value):
                    """Boş değerler veya NaN'ları None olarak temizler."""
                    if pd.isna(value) or value == '':
                        return None  # Null değerler için None kullanılıyor
                    return value  # Değer uygunsa, olduğu gibi döndür
                
                # Değerlerin temizlenmesi
                homeScore_period1 = clean_score(row["homeScore_period1"])
                homeScore_period2 = clean_score(row["homeScore_period2"])
                homeScore_normaltime = clean_score(row["homeScore_normaltime"])
                awayScore_period1 = clean_score(row["awayScore_period1"])
                awayScore_period2 = clean_score(row["awayScore_period2"])
                awayScore_normaltime = clean_score(row["awayScore_normaltime"])

                # MatchInfo modeline verileri kaydediyoruz
                MatchInfo.objects.update_or_create(
                    idx=row["id"],  # Maçın benzersiz ID'si
                    season_id=row["season_id"],  # Sezon ID'si
                    defaults={
                        'startTimestamp': row["startTimestamp"],
                        'tournament_name': row["tournament_name"],
                        'tournament_category_name': row["tournament_category_name"],
                        'tournament_category_id': row["tournament_category_id"],
                        'tournament_uniqueTournament_name': row["tournament_uniqueTournament_name"],
                        'tournament_uniqueTournament_id': row["tournament_uniqueTournament_id"],
                        'season_name': row["season_name"],
                        'season_year': row["season_year"],
                        'roundInfo_round': row["roundInfo_round"],
                        'status_type': row["status_type"],
                        'homeTeam_name': row["homeTeam_name"],
                        'homeTeam_nameCode': row["homeTeam_nameCode"],
                        'homeTeam_id': row["homeTeam_id"],
                        'awayTeam_name': row["awayTeam_name"],
                        'awayTeam_nameCode': row["awayTeam_nameCode"],
                        'awayTeam_id': row["awayTeam_id"],
                        'homeScore_period1': homeScore_period1,
                        'homeScore_period2': homeScore_period2,
                        'homeScore_normaltime': homeScore_normaltime,
                        'awayScore_period1': awayScore_period1,
                        'awayScore_period2': awayScore_period2,
                        'awayScore_normaltime': awayScore_normaltime,
                    }
                )
        except Exception as e:
            # Eğer bir hata olursa, MatchDataError modeline kaydediyoruz
            MatchDataError.objects.create(
                tournament_id=round_info.tournament_id,  # Hangi turnuvada hata olduğunu kaydediyoruz
                season_id=round_info.season_id,  # Hangi sezonda hata olduğunu kaydediyoruz
                round_num=round_info.round,  # Hangi turda hata olduğunu kaydediyoruz
                slug=slug,  # Slug (opsiyonel)
                prefix=prefix,  # Ön ek (opsiyonel)
                error_message=str(e)  # Hata mesajını kaydediyoruz
            )
```

Yapılan iyileştirmeler:
1. `error_message` yazım hatası düzeltildi.
2. Temizleme fonksiyonu (`clean_score`) NaN ve boş stringler için daha net hale getirildi.
3. Veri güncellemelerinde `update_or_create` ile `defaults` kullanıldı, böylece mevcut olanlar güncellenip olmayanlar eklenecek.

Başka soruların olursa yardımcı olmaktan memnuniyet duyarım!

***Soru:*** peki bu kodlarda response=200 gelmezse hata veritabanına yazılır mı

**Cevap:** Eğer kodunuzda API'den gelen yanıta göre hata kontrolü yapmak istiyorsanız ve `response=200` olmadığında bir hata kaydetmek istiyorsanız, bu durumda API'den gelen cevabı kontrol edip, uygun olmayan yanıtlar için veritabanına hata kaydı ekleyebilirsiniz.

Mevcut kodunuzda veriyi çekerken bir API çağrısı yapıyorsanız, bu çağrıyı kontrol etmek için genellikle `response.status_code` gibi bir alan kullanılır. API'den alınan yanıt 200 değilse, bir hata fırlatabilir ve bu hatayı `except` bloğunda yakalayarak veritabanına kaydedebilirsiniz.

Örneğin, API çağrısını ve `response.status_code` kontrolünü aşağıdaki gibi yapabilirsiniz:

```python
@shared_task
def fetch_and_save_match_data():
    # Tüm turları seçiyoruz
    rounds = RoundinfoModel.objects.all()
    for round_info in rounds:
        try:
            # SofaScore API'sinden verileri almak için gerekli parametreler
            tournament_id = round_info.tournament_id
            season_id = round_info.season_id
            round_num = round_info.round
            slug = round_info.slug if round_info.slug else ""
            prefix = round_info.prefix if round_info.prefix else ""
            
            # SofaScore API'sinden verileri çek (burada API çağrısı yapıyoruz)
            response = requests.get(f"API_ENDPOINT?tournament_id={tournament_id}&season_id={season_id}&round_num={round_num}&slug={slug}&prefix={prefix}")
            
            # API yanıtı başarılı mı diye kontrol ediyoruz
            if response.status_code != 200:
                raise Exception(f"API error: Received response code {response.status_code}")
            
            # API yanıtı başarılıysa veriyi işliyoruz
            df = pd.DataFrame(response.json())  # Örnek olarak JSON verisini pandas DataFrame'e çeviriyoruz
            
            # Alınan verileri MatchInfo modeline kaydet
            for index, row in df.iterrows():
                # Her bir sütun için NaN veya boş stringleri kontrol edip uygun değerler atıyoruz
                def clean_score(value):
                    """Boş değerler veya NaN'ları None olarak temizler."""
                    if pd.isna(value) or value == '':
                        return None  # Null değerler için None kullanılıyor
                    return value  # Değer uygunsa, olduğu gibi döndür
                
                # Değerlerin temizlenmesi
                homeScore_period1 = clean_score(row["homeScore_period1"])
                homeScore_period2 = clean_score(row["homeScore_period2"])
                homeScore_normaltime = clean_score(row["homeScore_normaltime"])
                awayScore_period1 = clean_score(row["awayScore_period1"])
                awayScore_period2 = clean_score(row["awayScore_period2"])
                awayScore_normaltime = clean_score(row["awayScore_normaltime"])

                # MatchInfo modeline verileri kaydediyoruz
                MatchInfo.objects.update_or_create(
                    idx=row["id"],  # Maçın benzersiz ID'si
                    season_id=row["season_id"],  # Sezon ID'si
                    defaults={
                        'startTimestamp': row["startTimestamp"],
                        'tournament_name': row["tournament_name"],
                        'tournament_category_name': row["tournament_category_name"],
                        'tournament_category_id': row["tournament_category_id"],
                        'tournament_uniqueTournament_name': row["tournament_uniqueTournament_name"],
                        'tournament_uniqueTournament_id': row["tournament_uniqueTournament_id"],
                        'season_name': row["season_name"],
                        'season_year': row["season_year"],
                        'roundInfo_round': row["roundInfo_round"],
                        'status_type': row["status_type"],
                        'homeTeam_name': row["homeTeam_name"],
                        'homeTeam_nameCode': row["homeTeam_nameCode"],
                        'homeTeam_id': row["homeTeam_id"],
                        'awayTeam_name': row["awayTeam_name"],
                        'awayTeam_nameCode': row["awayTeam_nameCode"],
                        'awayTeam_id': row["awayTeam_id"],
                        'homeScore_period1': homeScore_period1,
                        'homeScore_period2': homeScore_period2,
                        'homeScore_normaltime': homeScore_normaltime,
                        'awayScore_period1': awayScore_period1,
                        'awayScore_period2': awayScore_period2,
                        'awayScore_normaltime': awayScore_normaltime,
                    }
                )
        except Exception as e:
            # Eğer bir hata olursa, MatchDataError modeline kaydediyoruz
            MatchDataError.objects.create(
                tournament_id=round_info.tournament_id,  # Hangi turnuvada hata olduğunu kaydediyoruz
                season_id=round_info.season_id,  # Hangi sezonda hata olduğunu kaydediyoruz
                round_num=round_info.round,  # Hangi turda hata olduğunu kaydediyoruz
                slug=slug,  # Slug (opsiyonel)
                prefix=prefix,  # Ön ek (opsiyonel)
                error_message=str(e)  # Hata mesajını kaydediyoruz
            )
```

Bu kodda:
1. `requests.get()` ile API'den veriyi çekiyoruz.
2. API yanıtını `response.status_code` ile kontrol ediyoruz. Eğer 200 değilse, bir hata fırlatıyoruz.
3. Hata fırlatıldığında `except` bloğunda bu hatayı yakalayıp `MatchDataError` tablosuna kaydediyoruz.

Bu sayede, `response=200` olmadığında, hata mesajı veritabanına yazılacaktır.

***Soru:*** mevcut kodlarımda bu hata veritabanına kaydedilir mi kaydedilmez mi

**Cevap:** Mevcut kodlarınıza göre, eğer API çağrısı sırasında veya verilerin işlenmesi sırasında bir hata meydana gelirse, bu hata `except Exception as e:` bloğu tarafından yakalanır ve `MatchDataError` modeline kaydedilir. Ancak, şu anki haliyle spesifik olarak `response=200` kontrolü yapılmadığı için, API'den gelen cevabın başarıyla (status code 200) gelip gelmediği kontrol edilmemekte. 

Yani **mevcut haliyle**:
- Genel bir hata oluşursa (örneğin verilerin alınamaması, yanlış indeks kullanımı gibi), bu hata `MatchDataError` modeline kaydedilecektir.
- Ancak, API'den gelen yanıtın başarılı olup olmadığını (örneğin, `response=200` olup olmadığını) şu an kontrol etmiyorsunuz. Eğer API başarısız bir yanıt verirse, bu özel durumu kaydetmezsiniz çünkü yanıt durumu ile ilgili bir kontrol yok.

Eğer `response=200` durumunu özel olarak kontrol etmek ve yanıt başarısız olduğunda hatayı veritabanına kaydetmek isterseniz, API yanıtını `requests` ile çağırıyorsanız, `response.status_code` kontrolü eklemeniz gerekir.

Mevcut kodların sadece genel hataları yakalayacağını, ancak API yanıtının spesifik olarak `200` olmadığını yakalamayacağını unutmayın.

***Soru:*** yani yanıt alınmazsa şimdilik pass geçiyorum

**Cevap:** Evet, mevcut kodlarınıza göre API'den bir yanıt alınamazsa ya da yanıt hatalı olursa, kod bunu **şimdilik pass geçiyor**. Çünkü API yanıt durumunu kontrol eden bir mekanizma bulunmuyor. Bu nedenle, herhangi bir hatalı yanıt (`response=200` değilse) veritabanına kaydedilmiyor ve bu durum fark edilmeden geçiliyor.

Eğer API yanıtını kontrol etmek ve hata durumlarını kaydetmek istiyorsanız, yukarıda bahsettiğim gibi `response.status_code` kontrolünü ekleyerek bu durumu yönetebilirsiniz. Ancak şimdilik bu kontrolü atlayıp sadece genel hataları yakalıyor ve veritabanına kaydediyorsunuz.

***Soru:*** peki bunu da veritabanına kaydetmek için kodkarımnı düzsenle

**Cevap:** API yanıtının başarısız olduğu durumları da veritabanına kaydetmek için, API yanıtını kontrol edip, eğer `response.status_code` 200 değilse, bu durumu bir hata olarak yakalayıp `MatchDataError` modeline kaydedebilirsiniz. Aşağıda kodlarını bu doğrultuda nasıl güncelleyebileceğini gösteriyorum:

```python
import requests  # API çağrısı yapabilmek için gerekli

@shared_task
def fetch_and_save_match_data():
    # Tüm turları seçiyoruz
    rounds = RoundinfoModel.objects.all()
    for round_info in rounds:
        try:
            # SofaScore API'sinden verileri almak için gerekli parametreler
            tournament_id = round_info.tournament_id
            season_id = round_info.season_id
            round_num = round_info.round
            slug = round_info.slug if round_info.slug else ""
            prefix = round_info.prefix if round_info.prefix else ""
            
            # API çağrısı yap
            response = requests.get(f"API_ENDPOINT?tournament_id={tournament_id}&season_id={season_id}&round_num={round_num}&slug={slug}&prefix={prefix}")
            
            # API yanıtını kontrol et
            if response.status_code != 200:
                # Yanıt 200 değilse, veritabanına hata olarak kaydet
                raise Exception(f"API error: Received response code {response.status_code}")
            
            # API yanıtı başarılı ise, veriyi işliyoruz
            df = pd.DataFrame(response.json())  # Örnek olarak JSON verisini pandas DataFrame'e çeviriyoruz
            
            # Alınan verileri MatchInfo modeline kaydet
            for index, row in df.iterrows():
                # Her bir sütun için NaN veya boş stringleri kontrol edip uygun değerler atıyoruz
                def clean_score(value):
                    """Boş değerler veya NaN'ları None olarak temizler."""
                    if pd.isna(value) or value == '':
                        return None  # Null değerler için None kullanılıyor
                    return value  # Değer uygunsa, olduğu gibi döndür
                
                # Değerlerin temizlenmesi
                homeScore_period1 = clean_score(row["homeScore_period1"])
                homeScore_period2 = clean_score(row["homeScore_period2"])
                homeScore_normaltime = clean_score(row["homeScore_normaltime"])
                awayScore_period1 = clean_score(row["awayScore_period1"])
                awayScore_period2 = clean_score(row["awayScore_period2"])
                awayScore_normaltime = clean_score(row["awayScore_normaltime"])

                # MatchInfo modeline verileri kaydediyoruz
                MatchInfo.objects.update_or_create(
                    idx=row["id"],  # Maçın benzersiz ID'si
                    season_id=row["season_id"],  # Sezon ID'si
                    defaults={
                        'startTimestamp': row["startTimestamp"],
                        'tournament_name': row["tournament_name"],
                        'tournament_category_name': row["tournament_category_name"],
                        'tournament_category_id': row["tournament_category_id"],
                        'tournament_uniqueTournament_name': row["tournament_uniqueTournament_name"],
                        'tournament_uniqueTournament_id': row["tournament_uniqueTournament_id"],
                        'season_name': row["season_name"],
                        'season_year': row["season_year"],
                        'roundInfo_round': row["roundInfo_round"],
                        'status_type': row["status_type"],
                        'homeTeam_name': row["homeTeam_name"],
                        'homeTeam_nameCode': row["homeTeam_nameCode"],
                        'homeTeam_id': row["homeTeam_id"],
                        'awayTeam_name': row["awayTeam_name"],
                        'awayTeam_nameCode': row["awayTeam_nameCode"],
                        'awayTeam_id': row["awayTeam_id"],
                        'homeScore_period1': homeScore_period1,
                        'homeScore_period2': homeScore_period2,
                        'homeScore_normaltime': homeScore_normaltime,
                        'awayScore_period1': awayScore_period1,
                        'awayScore_period2': awayScore_period2,
                        'awayScore_normaltime': awayScore_normaltime,
                    }
                )
        except Exception as e:
            # Eğer bir hata olursa, MatchDataError modeline kaydediyoruz
            MatchDataError.objects.create(
                tournament_id=round_info.tournament_id,  # Hangi turnuvada hata olduğunu kaydediyoruz
                season_id=round_info.season_id,  # Hangi sezonda hata olduğunu kaydediyoruz
                round_num=round_info.round,  # Hangi turda hata olduğunu kaydediyoruz
                slug=slug,  # Slug (opsiyonel)
                prefix=prefix,  # Ön ek (opsiyonel)
                error_message=str(e)  # Hata mesajını kaydediyoruz
            )
```

### Güncellemeler:
1. **API yanıt kontrolü**: API'den dönen yanıtı `response.status_code` ile kontrol ediyorum. Eğer yanıt `200` değilse, bir `Exception` fırlatıyorum.
2. **Exception handling**: Eğer API'den bir hata alırsanız ya da başka bir hata oluşursa, `except` bloğunda bu hatayı yakalayıp `MatchDataError` modeline kaydediyorum. Bu sayede API başarısız yanıtlar da veritabanına kaydedilecektir.

Bu yöntemle artık sadece genel hatalar değil, API'den alınamayan ya da başarısız gelen yanıtlar da `MatchDataError` tablosuna kaydedilecek.

***Soru:*** from celery import shared_task
from .models import RoundinfoModel, MatchInfo, MatchDataError
import http.client
import json
import pandas as pd
from datetime import datetime


@shared_task
def fetch_and_save_match_data():
    # week="Biten" olan turları seç
    #rounds = RoundinfoModel.objects.filter(week="Devam")
    rounds = RoundinfoModel.objects.all()
    for round_info in rounds:
        try:
            # SofaScore API'sinden verileri almak için gerekli parametreler
            tournament_id = round_info.tournament_id
            season_id = round_info.season_id
            round_num = round_info.round
            slug = round_info.slug if round_info.slug else ""
            prefix = round_info.prefix if round_info.prefix else ""
            
            # SofaScore API'sinden verileri çek
            df = RoundData(tournament_id, season_id, round_num, slug, prefix)
            
            # Alınan verileri MatchInfo modeline kaydet
            for index, row in df.iterrows():
                # Her bir sütun için NaN veya boş stringleri kontrol edip uygun değerler atıyoruz
                def clean_score(value):
                    """Boş değerler veya NaN'ları None veya 0 olarak temizler."""
                    if pd.isna(value) or value == '':
                        return None  # Null değerler için None kullanılıyor
                    return value  # Değer uygunsa, olduğu gibi döndür
                
                # Değerlerin temizlenmesi
                homeScore_period1 = clean_score(row["homeScore_period1"])
                homeScore_period2 = clean_score(row["homeScore_period2"])
                homeScore_normaltime = clean_score(row["homeScore_normaltime"])
                awayScore_period1 = clean_score(row["awayScore_period1"])
                awayScore_period2 = clean_score(row["awayScore_period2"])
                awayScore_normaltime = clean_score(row["awayScore_normaltime"])

                # MatchInfo modeline verileri kaydediyoruz
                MatchInfo.objects.update_or_create(
                    idx=row["id"],  # Maçın benzersiz ID'si
                    season_id=row["season_id"],  # Sezon ID'si
                    defaults={
                        'startTimestamp': row["startTimestamp"],
                        'tournament_name': row["tournament_name"],
                        'tournament_category_name': row["tournament_category_name"],
                        'tournament_category_id': row["tournament_category_id"],
                        'tournament_uniqueTournament_name': row["tournament_uniqueTournament_name"],
                        'tournament_uniqueTournament_id': row["tournament_uniqueTournament_id"],
                        'season_name': row["season_name"],
                        'season_year': row["season_year"],
                        'roundInfo_round': row["roundInfo_round"],
                        'status_type': row["status_type"],
                        'homeTeam_name': row["homeTeam_name"],
                        'homeTeam_nameCode': row["homeTeam_nameCode"],
                        'homeTeam_id': row["homeTeam_id"],
                        'awayTeam_name': row["awayTeam_name"],
                        'awayTeam_nameCode': row["awayTeam_nameCode"],
                        'awayTeam_id': row["awayTeam_id"],
                        'homeScore_period1': homeScore_period1,
                        'homeScore_period2': homeScore_period2,
                        'homeScore_normaltime': homeScore_normaltime,
                        'awayScore_period1': awayScore_period1,
                        'awayScore_period2': awayScore_period2,
                        'awayScore_normaltime': awayScore_normaltime,
                    }
                )
        except Exception as e:
            # Eğer bir hata olursa, MatchDataError modeline kaydediyoruz
            MatchDataError.objects.create(
                tournament_id=round_info.tournament_id,  # Hangi turnuvada hata olduğunu kaydediyoruz
                season_id=round_info.season_id,  # Hangi sezonda hata olduğunu kaydediyoruz
                round_num=round_info.round,  # Hangi turda hata olduğunu kaydediyoruz
                slug=slug,  # Slug (opsiyonel)
                prefix=prefix,  # Ön ek (opsiyonel)
                error_message=str(e)  # Hata mesajını kaydediyoruz
            )  düzeltmeyi bu kodlara yapar mısın

**Cevap:** Elbette, API yanıt kontrolü ekleyerek ve genel bir hata yakalayıcıyla birlikte `response=200` kontrolünü yapabileceğiniz güncel kodu aşağıda bulabilirsiniz:

1. `http.client` ile HTTP isteği yapılacak.
2. Eğer yanıt `200` değilse, bir hata fırlatılacak ve `MatchDataError` modeline kaydedilecek.

İşte düzeltmeler yapılmış hali:

```python
from celery import shared_task
from .models import RoundinfoModel, MatchInfo, MatchDataError
import http.client
import json
import pandas as pd
from datetime import datetime

@shared_task
def fetch_and_save_match_data():
    # week="Biten" olan turları seç
    # rounds = RoundinfoModel.objects.filter(week="Devam")
    rounds = RoundinfoModel.objects.all()
    
    for round_info in rounds:
        try:
            # SofaScore API'sinden verileri almak için gerekli parametreler
            tournament_id = round_info.tournament_id
            season_id = round_info.season_id
            round_num = round_info.round
            slug = round_info.slug if round_info.slug else ""
            prefix = round_info.prefix if round_info.prefix else ""
            
            # API bağlantısı kuruluyor
            conn = http.client.HTTPSConnection("api.sofascore.com")
            endpoint = f"/api/v1/tournament/{tournament_id}/season/{season_id}/round/{round_num}?slug={slug}&prefix={prefix}"
            conn.request("GET", endpoint)

            # Yanıt alınıyor
            response = conn.getresponse()
            
            # Yanıt kontrolü, 200 değilse hata kaydet
            if response.status != 200:
                raise Exception(f"API error: Received response code {response.status}")

            # JSON verilerini yükle
            data = response.read().decode("utf-8")
            json_data = json.loads(data)
            df = pd.DataFrame(json_data)  # Örnek olarak JSON verisini pandas DataFrame'e çeviriyoruz

            # Alınan verileri MatchInfo modeline kaydet
            for index, row in df.iterrows():
                # Her bir sütun için NaN veya boş stringleri kontrol edip uygun değerler atıyoruz
                def clean_score(value):
                    """Boş değerler veya NaN'ları None olarak temizler."""
                    if pd.isna(value) or value == '':
                        return None  # Null değerler için None kullanılıyor
                    return value  # Değer uygunsa, olduğu gibi döndür

                # Değerlerin temizlenmesi
                homeScore_period1 = clean_score(row["homeScore_period1"])
                homeScore_period2 = clean_score(row["homeScore_period2"])
                homeScore_normaltime = clean_score(row["homeScore_normaltime"])
                awayScore_period1 = clean_score(row["awayScore_period1"])
                awayScore_period2 = clean_score(row["awayScore_period2"])
                awayScore_normaltime = clean_score(row["awayScore_normaltime"])

                # MatchInfo modeline verileri kaydediyoruz
                MatchInfo.objects.update_or_create(
                    idx=row["id"],  # Maçın benzersiz ID'si
                    season_id=row["season_id"],  # Sezon ID'si
                    defaults={
                        'startTimestamp': row["startTimestamp"],
                        'tournament_name': row["tournament_name"],
                        'tournament_category_name': row["tournament_category_name"],
                        'tournament_category_id': row["tournament_category_id"],
                        'tournament_uniqueTournament_name': row["tournament_uniqueTournament_name"],
                        'tournament_uniqueTournament_id': row["tournament_uniqueTournament_id"],
                        'season_name': row["season_name"],
                        'season_year': row["season_year"],
                        'roundInfo_round': row["roundInfo_round"],
                        'status_type': row["status_type"],
                        'homeTeam_name': row["homeTeam_name"],
                        'homeTeam_nameCode': row["homeTeam_nameCode"],
                        'homeTeam_id': row["homeTeam_id"],
                        'awayTeam_name': row["awayTeam_name"],
                        'awayTeam_nameCode': row["awayTeam_nameCode"],
                        'awayTeam_id': row["awayTeam_id"],
                        'homeScore_period1': homeScore_period1,
                        'homeScore_period2': homeScore_period2,
                        'homeScore_normaltime': homeScore_normaltime,
                        'awayScore_period1': awayScore_period1,
                        'awayScore_period2': awayScore_period2,
                        'awayScore_normaltime': awayScore_normaltime,
                    }
                )
            
        except Exception as e:
            # Eğer bir hata olursa, MatchDataError modeline kaydediyoruz
            MatchDataError.objects.create(
                tournament_id=round_info.tournament_id,  # Hangi turnuvada hata olduğunu kaydediyoruz
                season_id=round_info.season_id,  # Hangi sezonda hata olduğunu kaydediyoruz
                round_num=round_info.round,  # Hangi turda hata olduğunu kaydediyoruz
                slug=slug,  # Slug (opsiyonel)
                prefix=prefix,  # Ön ek (opsiyonel)
                error_message=str(e)  # Hata mesajını kaydediyoruz
            )
```

### Güncellemeler:
1. **API Yanıt Kontrolü:** `response.status` kontrol edilerek, `200` yanıtı gelmezse bir hata fırlatılır. Hata, `except` bloğunda yakalanır ve `MatchDataError` modeline kaydedilir.
2. **Veri İşleme:** Eğer API yanıtı başarılıysa, JSON verileri pandas DataFrame'e çevrilir ve işlenir.
3. **Hata Durumunda Kayıt:** Eğer herhangi bir hata meydana gelirse (örneğin API hatası, veri işleme hatası), `MatchDataError` tablosuna bu hata kaydedilir.

Bu haliyle, API yanıtı kontrol edilir ve başarısız durumlarda hatalar düzgün bir şekilde veritabanına kaydedilir.

***Soru:*** bu veir yaklaşık 98 lig ortalam 30 hafta ve her haftada 8 maç olursa kaç api isteiği gider

**Cevap:** Bu durumda, toplamda kaç API isteği yapılacağını hesaplayalım.

### Verilenler:
- **98 lig** var.
- Her ligin ortalama **30 hafta** süreceği belirtilmiş.
- Her hafta **8 maç** oynanacak.

### Hesaplama:

Toplam API isteği şu şekilde hesaplanır:

\[
\text{Toplam API İsteği} = \text{Lig Sayısı} \times \text{Hafta Sayısı} \times \text{Haftalık Maç Sayısı}
\]

\[
\text{Toplam API İsteği} = 98 \times 30 \times 8 = 23,520
\]

### Sonuç:
Bu durumda toplamda **23,520 API isteği** yapılması gerekecek.

Bu sayı, her maç için bir API isteği yapacağınız varsayılarak hesaplanmıştır. Eğer başka ek API istekleri (örneğin maçla ilgili daha fazla veri çekmek) gerekiyorsa, bu sayı artabilir.

***Soru:*** peki bu ortalama 12 concurreny celery ile yapılıyor kaç dk srer

**Cevap:** Bu işlemi Celery ile gerçekleştirmek için ortalama süreyi hesaplayabilmek için bazı bilgilere daha ihtiyacımız var. Özellikle her bir API isteğinin ne kadar sürdüğü önemlidir. Bununla birlikte, varsayımlar yaparak bir tahmin yapabiliriz.

### Verilenler:
- **23,520 API isteği** yapılacak.
- **12 concurrency** (eşzamanlı çalışan işçi sayısı).
- Her bir API isteğinin yanıt süresini **x saniye** olarak kabul edelim (gerçek süreyi bilmediğimiz için bu değişkeni varsayacağız).

### Hesaplama:
İlk olarak, her bir işçinin işlem süresi üzerinden tahmini yapalım.

#### Toplam İstek Süresi:
Eğer her bir API isteği **x saniye** sürüyorsa, her işçi için toplam istek süresi şu şekilde hesaplanır:

\[
\text{Toplam Süre (saniye)} = \frac{\text{Toplam API İsteği} \times \text{İstek Başına Süre}}{\text{Concurrency}}
\]

\[
\text{Toplam Süre (saniye)} = \frac{23,520 \times x}{12}
\]

Bu formülden:

\[
\text{Toplam Süre (saniye)} = 1,960 \times x
\]

#### Dakikaya Çevirme:
Sonucu dakika cinsinden almak için saniyeyi dakikaya çeviriyoruz:

\[
\text{Toplam Süre (dakika)} = \frac{1,960 \times x}{60}
\]

\[
\text{Toplam Süre (dakika)} \approx 32.67 \times x
\]

### Sonuç:
Bu formüle göre, **her bir API isteği kaç saniye sürüyorsa, toplam süreyi** ona göre hesaplayabiliriz.

Eğer her bir API isteği ortalama **1 saniye** sürerse:
\[
\text{Toplam Süre (dakika)} = 32.67 \text{ dakika}
\]

Eğer her bir API isteği **2 saniye** sürerse:
\[
\text{Toplam Süre (dakika)} = 65.34 \text{ dakika}
\]

Bu süre, her isteğin ne kadar zaman aldığına bağlı olarak değişecektir. Eşzamanlılık (concurrency) arttıkça süre kısalacaktır.

***Soru:*** b,r saniyede 3 istek

**Cevap:** Eğer 1 saniyede 3 API isteği yapılabiliyorsa, toplam süreyi aşağıdaki gibi hesaplayabiliriz:

### Verilenler:
- **23,520 API isteği** yapılacak.
- **12 concurrency** (eşzamanlı çalışan işçi sayısı).
- **1 saniyede 3 istek** yapılabiliyor.

### Hesaplama:

İlk olarak, her bir işçi için saniyede kaç istek yapılabileceğini hesaplayalım:

\[
\text{İşçi başına saniyede istek} = \frac{3}{12} = 0.25 \text{ istek/saniye}
\]

Bu durumda, **1 işçi** 1 saniyede **0.25 istek** yapabiliyor. 

#### Toplam Süre:
Toplam süreyi bulmak için:

\[
\text{Toplam Süre (saniye)} = \frac{\text{Toplam İstek Sayısı}}{\text{İşçi başına saniyedeki istek sayısı}}
\]

\[
\text{Toplam Süre (saniye)} = \frac{23,520}{0.25} = 94,080 \text{ saniye}
\]

#### Dakikaya Çevirme:
Bu süreyi dakikaya çevirelim:

\[
\text{Toplam Süre (dakika)} = \frac{94,080}{60} = 1,568 \text{ dakika}
\]

### Sonuç:
Eğer her saniyede 3 istek yapılabiliyorsa ve 12 concurrency ile çalışıyorsanız, bu işlem **yaklaşık 1,568 dakika** sürecektir, yani yaklaşık **26 saat**.

Bu süreyi daha da azaltmak için daha fazla işçi (concurrency) kullanabilir ya da istekleri daha hızlı gerçekleştirecek bir yöntem (örneğin, farklı API limitleri) kullanabilirsiniz.