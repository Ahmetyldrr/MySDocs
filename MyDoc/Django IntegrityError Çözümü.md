***Soru:*** import os
import django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'Home.settings')
django.setup()
os.environ["DJANGO_ALLOW_ASYNC_UNSAFE"] = "true"
from tournaments.models import Tournament, Season, Team,Match
from tournaments.models import FikstureModelData
from datetime import datetime, timedelta

class SofascoreAPI:
    def __init__(self):
        pass

    def fetch_data(self):
        data = FikstureModelData.objects.all().values()
        data_list = list(data)
        df = pd.DataFrame(data_list)
        df_exploded = df.explode('data')
        expanded_data = pd.json_normalize(df_exploded['data'])
        expanded_data['tarih'] = list(df_exploded['tarih'])
        veri = expanded_data.copy()
        veri.columns = [item.replace(".", "_") for item in veri.columns]
        return veri

    def tournament_data(self):
        verim = self.fetch_data()
        if verim is None:
            raise ValueError("Veri işlenmedi. Önce 'process_data()' metodunu çalıştırın.")
        
        # Aynı uniqueTournament_id'ye sahip olanları tekrar kontrol et
        verim = verim.drop_duplicates("tournament_uniqueTournament_id")
        
        cols = [
            "tournament_uniqueTournament_id", "tournament_name", "tournament_slug", "tournament_category_name",
            "tournament_category_slug", "tournament_uniqueTournament_category_id", 
            "tournament_uniqueTournament_hasEventPlayerStatistics", "tournament_id", "tournament_isGroup", 
            "tournament_uniqueTournament_hasPerformanceGraphFeature"
        ]
        
        for col in cols:
            if col not in verim.columns:
                verim.loc[:, col] = 0

        verim = verim[cols]

        for _, row in verim.iterrows():
            tournament_id = row['tournament_uniqueTournament_id']
            
            if pd.isna(tournament_id):
                print(f"Geçersiz tournament_uniqueTournament_id: {tournament_id}, atlanıyor.")
                continue
        
            if not Tournament.objects.filter(tournament_id=tournament_id).exists():
                Tournament.objects.create(
                    tournament_id=row['tournament_uniqueTournament_id'],
                    tournament_name=row['tournament_name'],
                    tournament_slug=row['tournament_slug'],
                    tournament_category_name=row['tournament_category_name'],
                    tournament_category_slug=row['tournament_category_slug'],
                    tournament_uniqueTournament_category_id=row['tournament_uniqueTournament_category_id'],
                    tournament_model_id=row['tournament_id'],
                    tournament_isGroup=row['tournament_isGroup'] if pd.notna(row['tournament_isGroup']) else False,
                    tournament_uniqueTournament_hasPerformanceGraphFeature=row['tournament_uniqueTournament_hasPerformanceGraphFeature'] if pd.notna(row['tournament_uniqueTournament_hasPerformanceGraphFeature']) else False
                )
                print(f"Tournament ID {tournament_id} başarıyla eklendi.")
            else:
                print(f"Tournament ID {tournament_id} zaten mevcut, eklenmedi.")

    def season_data(self):
        verim = self.fetch_data()
        if verim is None:
            raise ValueError("Veri işlenmedi. Önce 'process_data()' metodunu çalıştırın.")
        
        verim = verim.drop_duplicates("season_id")
        
        season_cols = ["season_id", "season_name", "season_year","tournament_uniqueTournament_id"]

        for col in season_cols:
            if col not in verim.columns:
                verim.loc[:, col] = 0

        verim = verim[season_cols]

        for _, row in verim.iterrows():
            season_id = row['season_id']
            tournament_id = row.get('tournament_uniqueTournament_id')
    
            if pd.isna(season_id) or pd.isna(tournament_id):
                print(f"Geçersiz season_id veya tournament_id: Season ID={season_id}, Tournament ID={tournament_id}. Atlanıyor.")
                continue
    
            if not Season.objects.filter(season_id=season_id).exists():
                tournament_instance = Tournament.objects.filter(tournament_id=tournament_id).first()
                
                if tournament_instance:
                    Season.objects.create(
                        season_id=row['season_id'],
                        season_name=row['season_name'],
                        season_year=row['season_year'],
                        tournament=tournament_instance  # Doğru sütun adı burada kullanılıyor
                    )
                    print(f"Season ID {season_id} başarıyla eklendi.")
                else:
                    print(f"Tournament ID {tournament_id} bulunamadı, Season ID {season_id} eklenemedi.")
            else:
                print(f"Season ID {season_id} zaten mevcut, eklenmedi.")
    
   
    def team_data(self):

        data = self.fetch_data()
        homecols = [
                    "homeTeam_id", "homeTeam_name", "homeTeam_slug", "homeTeam_shortName",
                    "homeTeam_nameCode", "homeTeam_national", "tournament_uniqueTournament_id", "season_id"
                ]
        
        awaycols = [
                    "awayTeam_id", "awayTeam_name", "awayTeam_slug", "awayTeam_shortName",
                    "awayTeam_nameCode", "awayTeam_national", "tournament_uniqueTournament_id", "season_id"
                ]
        
        # Home takımı için veri seçimi ve kolon isimlerinin ayarlanması
        homedata = data[homecols]
        homedata.columns = ["team_id", "team_name", "team_slug", "team_shortName",
                                       "team_nameCode", "team_national", "tournament_id", "season_id"]
        
        # Away takımı için veri seçimi ve kolon isimlerinin ayarlanması
        awaydata = data[awaycols]
        awaydata.columns  = ["team_id", "team_name", "team_slug", "team_shortName",
                                       "team_nameCode", "team_national", "tournament_id", "season_id"]
        
        # Home ve Away takımları birleştirme
        teamdata = pd.concat([homedata, awaydata])
        teamdata = teamdata.drop_duplicates(subset=["team_id", "tournament_id", "season_id"])
       
        for _, row in teamdata.iterrows():
            team_id = row['team_id']
            tournament_id = row['tournament_id']
            season_id = row['season_id']
            
            # Geçersiz veya eksik id'leri atla
            if pd.isna(team_id) or pd.isna(tournament_id) or pd.isna(season_id):
                print(f"Geçersiz değer: Team ID={team_id}, Tournament ID={tournament_id}, Season ID={season_id}. Atlanıyor.")
                continue

            # İlgili tournament ve season nesnelerini getir
            tournament_instance = Tournament.objects.filter(tournament_id=tournament_id).first()
            season_instance = Season.objects.filter(season_id=season_id).first()

            if tournament_instance and season_instance:
                # Takımın veritabanında var olup olmadığını kontrol et, yoksa oluştur
                if not Team.objects.filter(team_id=team_id, tournament=tournament_instance, season=season_instance).exists():
                    Team.objects.create(
                        team_id=team_id,
                        team_name=row['team_name'],
                        team_slug=row['team_slug'],
                        team_shortName=row['team_shortName'],
                        team_nameCode=row['team_nameCode'],
                        team_national=row['team_national'],
                        tournament=tournament_instance,  # ForeignKey olan alanlar
                        season=season_instance           # ForeignKey olan alanlar
                    )
                    print(f"Team ID {team_id} başarıyla eklendi.")
                else:
                    print(f"Team ID {team_id} zaten mevcut, eklenmedi.")
            else:
                print(f"Tournament ID {tournament_id} veya Season ID {season_id} bulunamadı.")

    def match_data(self):
        # Fetch data from the API or existing model
        verim = self.fetch_data()
        if verim is None:
            raise ValueError("Veri işlenmedi. Lütfen önce 'process_data()' metodunu çalıştırın.")
        
     
     
        new_cols = ['id', 'startTimestamp', 'slug', 'tournament_uniqueTournament_id', 'season_id',
                    'roundInfo_round', 'status_type', 'homeTeam_id', 'awayTeam_id',
                    'homeScore_current', 'homeScore_period1', 'homeScore_period2', 'homeScore_normaltime',
                    'awayScore_current', 'awayScore_period1', 'awayScore_period2', 'awayScore_normaltime']
        
        df1 = verim[new_cols] 
        df1['date'] = pd.to_datetime(df1['startTimestamp'], unit='s') + timedelta(hours=3)
        df2 = df1.drop("startTimestamp", axis=1)
        df3 = df2.fillna(0)
        for _, row in df3.iterrows():
            match_id = row['id']
            tournament_id = row['tournament_uniqueTournament_id']
            season_id = row['season_id']
            home_team_id = row['homeTeam_id']
            away_team_id = row['awayTeam_id']
            
            # Geçersiz veya eksik id'leri atla
            if pd.isna(match_id) or pd.isna(tournament_id) or pd.isna(season_id) or pd.isna(home_team_id) or pd.isna(away_team_id):
                print(f"Geçersiz değer: Match ID={match_id}, Tournament ID={tournament_id}, Season ID={season_id}, Home Team ID={home_team_id}, Away Team ID={away_team_id}. Atlanıyor.")
                continue

            # İlgili foreign key nesnelerini getir
            tournament_instance = Tournament.objects.filter(tournament_id=tournament_id).first()
            season_instance = Season.objects.filter(season_id=season_id).first()
            home_team_instance = Team.objects.filter(team_id=home_team_id).first()
            away_team_instance = Team.objects.filter(team_id=away_team_id).first()

            if tournament_instance and season_instance and home_team_instance and away_team_instance:
                # Match'in veritabanında olup olmadığını kontrol et, yoksa oluştur
                if not Match.objects.filter(id=match_id).exists():
                    Match.objects.create(
                        id=match_id,
                        startTimestamp=row['date'],  # DateTimeField olarak datetime verisi
                        slug=row['slug'],
                        tournament=tournament_instance,
                        season=season_instance,
                        homeTeam=home_team_instance,
                        awayTeam=away_team_instance,
                        roundInfo_round=row['roundInfo_round'],
                        homeScore_current=row['homeScore_current'],
                        homeScore_period1=row['homeScore_period1'],
                        homeScore_period2=row['homeScore_period2'],
                        homeScore_normaltime=row['homeScore_normaltime'],
                        awayScore_current=row['awayScore_current'],
                        awayScore_period1=row['awayScore_period1'],
                        awayScore_period2=row['awayScore_period2'],
                        awayScore_normaltime=row['awayScore_normaltime'],
                        status_type = row['status_type']
                    )
                    print(f"Match ID {match_id} başarıyla eklendi.")
                else:
                    print(f"Match ID {match_id} zaten mevcut, eklenmedi.")
            else:
                print(f"Tournament ID {tournament_id}, Season ID {season_id}, Home Team ID {home_team_id}, Away Team ID {away_team_id} bulunamadı.")





# SofascoreAPI sınıfını kullanarak team_data'yı veritabanına kaydetmek için:
api = SofascoreAPI()
teamdata = api.fetch_data()  # Veriyi getirin (API'den ya da dosyadan)
api.tournament_data()
api.season_data()
api.team_data()
api.match_data()
print("İşlemler bitti")  bu kodları çalıştırdğımdan bir hata ile karşılatırm  File ~/Masaüstü/myenv/lib/python3.12/site-packages/django/db/backends/sqlite3/base.py:354, in SQLiteCursorWrapper.execute(self, query, params)
    352 param_names = list(params) if isinstance(params, Mapping) else None
    353 query = self.convert_query(query, param_names=param_names)
--> 354 return super().execute(query, params)

IntegrityError: UNIQUE constraint failed: tournaments_team.team_id   istersen model ve admin verilerimi paylaşırım nmeden oldu

**Cevap:** Bu hatanın kaynağı, aynı `team_id` değerine sahip bir kaydın veritabanına yeniden eklenmeye çalışılmasıdır. Bu, veritabanında `UNIQUE` kısıtlamasına sahip olan `team_id` alanı nedeniyle `IntegrityError` hatasına yol açar. Kodunuza göre, `team_id`, `tournament` ve `season` bilgilerine göre benzersiz bir kayıt yaratılması bekleniyor, ancak bu üçlüden biri eksikse veya zaten veritabanında mevcutsa hata alırsınız. Ayrıca, `Team` modelinizin yapısını ve benzersiz alanlarını incelemek bu sorunu çözmekte yardımcı olabilir.

Bu hatayı gidermek için aşağıdaki adımları takip edebilirsiniz:

1. **Kodunuzu İnceleyin:** `Team` modeline yeni bir kayıt eklenmeden önce aynı `team_id`, `tournament`, ve `season` bilgilerine sahip kaydın var olup olmadığını kontrol ediyorsunuz. Bu kontrolü `team_id` ile sınırlamak yerine, `tournament` ve `season` ile birlikte tüm kombinasyonu kontrol ettiğinizden emin olun.

2. **Veritabanını Temizleyin (Geçici Çözüm):** Veritabanınızda halihazırda var olan eski `team_id` kayıtlarını silmek isteyebilirsiniz, ancak bu, dikkatlice yapılması gereken bir adımdır. Komut olarak çalıştırabilirsiniz:
   
   ```python
   Team.objects.all().delete()  # Tüm Team kayıtlarını siler. Dikkatli kullanın!
   ```

3. **Güncellenmiş Kod:** `team_id`, `tournament` ve `season` kombinasyonunu kullanarak eşsiz kontrolünü daha sağlam bir hale getirebiliriz. Kodunuzu, aynı `team_id`, `tournament` ve `season` kombinasyonunun mevcut olup olmadığını kontrol edecek şekilde güncelleyebiliriz:

   ```python
   if not Team.objects.filter(team_id=team_id, tournament=tournament_instance, season=season_instance).exists():
       Team.objects.create(
           team_id=team_id,
           team_name=row['team_name'],
           team_slug=row['team_slug'],
           team_shortName=row['team_shortName'],
           team_nameCode=row['team_nameCode'],
           team_national=row['team_national'],
           tournament=tournament_instance,
           season=season_instance
       )
       print(f"Team ID {team_id} başarıyla eklendi.")
   else:
       print(f"Team ID {team_id} zaten mevcut, eklenmedi.")
   ```

Bu yöntemle hatayı çözemezsek, model ve admin yapılandırmalarını da paylaşman faydalı olur.

***Soru:*** şimdi kodlarımda böyle bir hata çıkmaması için şöyle yap eski team sil yeni tem verisi ekle

**Cevap:** Mevcut `team_id`, `tournament`, ve `season` kombinasyonuna sahip bir kaydın olup olmadığını kontrol edip varsa silerek ardından yeni veriyi eklemek için kodunuzu aşağıdaki gibi güncelleyebiliriz:

```python
for _, row in teamdata.iterrows():
    team_id = row['team_id']
    tournament_id = row['tournament_id']
    season_id = row['season_id']
    
    # Geçersiz veya eksik id'leri atla
    if pd.isna(team_id) or pd.isna(tournament_id) or pd.isna(season_id):
        print(f"Geçersiz değer: Team ID={team_id}, Tournament ID={tournament_id}, Season ID={season_id}. Atlanıyor.")
        continue

    # İlgili tournament ve season nesnelerini getir
    tournament_instance = Tournament.objects.filter(tournament_id=tournament_id).first()
    season_instance = Season.objects.filter(season_id=season_id).first()

    if tournament_instance and season_instance:
        # Aynı team_id, tournament ve season kombinasyonuna sahip eski kaydı sil
        Team.objects.filter(team_id=team_id, tournament=tournament_instance, season=season_instance).delete()
        
        # Yeni kaydı oluştur
        Team.objects.create(
            team_id=team_id,
            team_name=row['team_name'],
            team_slug=row['team_slug'],
            team_shortName=row['team_shortName'],
            team_nameCode=row['team_nameCode'],
            team_national=row['team_national'],
            tournament=tournament_instance,
            season=season_instance
        )
        print(f"Team ID {team_id} güncellenerek eklendi.")
    else:
        print(f"Tournament ID {tournament_id} veya Season ID {season_id} bulunamadı.")
```

### Açıklama

1. **Kayıtları Silme:** `Team.objects.filter(...).delete()` satırı, belirttiğiniz kombinasyona sahip mevcut kayıtları veritabanından siler.
2. **Yeni Kayıt Eklemek:** Eski kayıt silindikten sonra yeni kayıt `Team.objects.create(...)` ile oluşturulur. 

Bu yöntem, aynı `team_id`, `tournament`, ve `season` kombinasyonuna sahip eski kaydı silip yenisini ekleyerek `IntegrityError` hatasını önler.

***Soru:*** s)
    103     return self.cursor.execute(sql)
    104 else:
--> 105     return self.cursor.execute(sql, params)

File ~/Masaüstü/myenv/lib/python3.12/site-packages/django/db/backends/sqlite3/base.py:354, in SQLiteCursorWrapper.execute(self, query, params)
    352 param_names = list(params) if isinstance(params, Mapping) else None
    353 query = self.convert_query(query, param_names=param_names)
--> 354 return super().execute(query, params)

IntegrityError: UNIQUE constraint failed: tournaments_team.team_id  hata geldi

**Cevap:** Bu hata, `team_id` alanı üzerinde `UNIQUE` kısıtlaması olduğundan, aynı `team_id` değerine sahip bir kayıt eklemeye çalıştığınızda oluşuyor. `delete` komutunun bu kaydı temizleyip ardından yeni kaydı eklemesi gerekirken yine de aynı hatayı alıyorsanız, bazı durumlarda Django’nun işlemi tam olarak sırasıyla yapmadığını gözlemleyebiliriz.

Bunun çözümü için `update_or_create` yöntemini kullanarak aynı `team_id`, `tournament` ve `season` değerine sahip bir kayıt varsa güncelleyecek, yoksa yeni bir kayıt ekleyecek şekilde değiştirebiliriz.

Kodunuzu aşağıdaki gibi düzenleyin:

```python
for _, row in teamdata.iterrows():
    team_id = row['team_id']
    tournament_id = row['tournament_id']
    season_id = row['season_id']
    
    # Geçersiz veya eksik id'leri atla
    if pd.isna(team_id) or pd.isna(tournament_id) or pd.isna(season_id):
        print(f"Geçersiz değer: Team ID={team_id}, Tournament ID={tournament_id}, Season ID={season_id}. Atlanıyor.")
        continue

    # İlgili tournament ve season nesnelerini getir
    tournament_instance = Tournament.objects.filter(tournament_id=tournament_id).first()
    season_instance = Season.objects.filter(season_id=season_id).first()

    if tournament_instance and season_instance:
        # Mevcut kayıt varsa güncelle, yoksa yeni kayıt oluştur
        team, created = Team.objects.update_or_create(
            team_id=team_id,
            tournament=tournament_instance,
            season=season_instance,
            defaults={
                'team_name': row['team_name'],
                'team_slug': row['team_slug'],
                'team_shortName': row['team_shortName'],
                'team_nameCode': row['team_nameCode'],
                'team_national': row['team_national'],
            }
        )
        if created:
            print(f"Team ID {team_id} başarıyla eklendi.")
        else:
            print(f"Team ID {team_id} güncellenerek kaydedildi.")
    else:
        print(f"Tournament ID {tournament_id} veya Season ID {season_id} bulunamadı.")
```

### Açıklama

- `update_or_create` yöntemi, belirtilen `team_id`, `tournament`, ve `season` kombinasyonunu kullanarak önce mevcut bir kayıt olup olmadığını kontrol eder. 
  - Varsa, `defaults` içinde sağlanan değerlerle günceller.
  - Yoksa yeni bir kayıt oluşturur.
  
Bu, UNIQUE constraint hatasını çözmeli ve gereksiz `delete` işlemlerini önlemelidir.

***Soru:*** File ~/Masaüstü/myenv/lib/python3.12/site-packages/django/db/backends/sqlite3/base.py:354, in SQLiteCursorWrapper.execute(self, query, params)
    352 param_names = list(params) if isinstance(params, Mapping) else None
    353 query = self.convert_query(query, param_names=param_names)
--> 354 return super().execute(query, params)

IntegrityError: UNIQUE constraint failed: tournaments_team.team_id  lütfen bu hatayı d

**Cevap:** Bu hata, `Team` modelinizdeki `team_id` alanının UNIQUE constraint ile tanımlı olmasından kaynaklanıyor. Yani aynı `team_id` değerine sahip birden fazla kayıt veritabanında bulunamıyor. Bu durumu çözmek için iki farklı yaklaşımdan yararlanabiliriz:

### 1. UNIQUE Kısıtını Diğer Alanlarla Genişletmek
Eğer `team_id` alanında UNIQUE kısıtı `tournament` ve `season` ile birlikte çalışacak şekilde genişletilebilirse, aynı `team_id` farklı turnuva ve sezon kombinasyonlarıyla kaydedilebilir. Bu durumda `Team` modelinizi güncelleyerek `team_id`, `tournament` ve `season` alanlarını birlikte UNIQUE yapabilirsiniz.

Örneğin:

```python
class Team(models.Model):
    team_id = models.IntegerField()
    tournament = models.ForeignKey(Tournament, on_delete=models.CASCADE)
    season = models.ForeignKey(Season, on_delete=models.CASCADE)
    # Diğer alanlar...

    class Meta:
        unique_together = ('team_id', 'tournament', 'season')  # UNIQUE kısıtı tanımlandı
```

Bu, `team_id` alanının yalnızca belirli bir `tournament` ve `season` kombinasyonunda benzersiz olmasını sağlar. Böylece aynı `team_id` farklı turnuva veya sezonlarla birden fazla kaydedilebilir.

> **Not:** Bu değişiklik sonrası `makemigrations` ve `migrate` komutlarını çalıştırarak veritabanı şemanızı güncelleyebilirsiniz.

### 2. Mevcut Kayıtları Silerek Eklemek (UNIQUE Kısıtını Güncellemeden)
Eğer UNIQUE kısıtını değiştiremiyorsanız, mevcut `team_id` değerine sahip olan kayıtları eklemeden önce silmeyi düşünebiliriz. Aşağıdaki kod, aynı `team_id` değerine sahip eski kayıtları silerek yenisini ekler:

```python
for _, row in teamdata.iterrows():
    team_id = row['team_id']
    tournament_id = row['tournament_id']
    season_id = row['season_id']
    
    # Geçersiz veya eksik id'leri atla
    if pd.isna(team_id) or pd.isna(tournament_id) or pd.isna(season_id):
        print(f"Geçersiz değer: Team ID={team_id}, Tournament ID={tournament_id}, Season ID={season_id}. Atlanıyor.")
        continue

    # İlgili tournament ve season nesnelerini getir
    tournament_instance = Tournament.objects.filter(tournament_id=tournament_id).first()
    season_instance = Season.objects.filter(season_id=season_id).first()

    if tournament_instance and season_instance:
        # Eski kaydı sil
        Team.objects.filter(team_id=team_id).delete()
        
        # Yeni kaydı oluştur
        Team.objects.create(
            team_id=team_id,
            team_name=row['team_name'],
            team_slug=row['team_slug'],
            team_shortName=row['team_shortName'],
            team_nameCode=row['team_nameCode'],
            team_national=row['team_national'],
            tournament=tournament_instance,
            season=season_instance
        )
        print(f"Team ID {team_id} güncellenerek eklendi.")
    else:
        print(f"Tournament ID {tournament_id} veya Season ID {season_id} bulunamadı.")
```

### Açıklama
Bu iki çözüm, aynı `team_id` alanına sahip kayıtların UNIQUE constraint hatasına neden olmadan veritabanına kaydedilmesini sağlamalıdır. İlk çözüm, kalıcı bir yapısal değişiklik sağlarken, ikinci çözümde her ekleme sırasında eski kayıt silinip yeni kayıt eklenir.

***Soru:*** class Team(models.Model):
    team_id = models.IntegerField(primary_key=True)  # Artık benzersiz değil, bir takım farklı turnuvalarda yer alabilir
    team_name = models.CharField(max_length=255)
    team_slug = models.SlugField(max_length=255)
    team_shortName = models.CharField(max_length=100)
    team_nameCode = models.CharField(max_length=10)
    team_national = models.BooleanField(default=False)

    # Bir takım birden fazla turnuvada oynayabilir
    tournament = models.ForeignKey(Tournament, on_delete=models.CASCADE, db_column='tournament_id', related_name='teams')

    # Bir takım birden fazla sezonda oynayabilir
    season = models.ForeignKey(Season, on_delete=models.CASCADE, db_column='season_id', related_name='teams2')

    def __str__(self):
        return f"{self.team_name} ({self.tournament.tournament_name} - {self.season.season_name})"

    class Meta:
        unique_together = ('team_id', 'tournament', 'season')  # Aynı takım, aynı turnuvada, aynı sezonda yalnızca bir kez yer alabilir  team model zaten böyle

**Cevap:** Model yapınızda `unique_together = ('team_id', 'tournament', 'season')` ayarı olduğu için, aynı `team_id` ile aynı `tournament` ve `season` kombinasyonuna sahip birden fazla kayıt eklenememesi gerekiyor. Ancak hala `IntegrityError: UNIQUE constraint failed: tournaments_team.team_id` hatası alıyorsanız, bunun birkaç nedeni olabilir:

1. **primary_key=True ile team_id Tanımlanması:**
   - `team_id` alanını `primary_key=True` olarak tanımlamışsınız. Bu durumda Django, `team_id` alanını UNIQUE yapar ve `unique_together` kısıtını dikkate almaz. Yani, aynı `team_id` değerine sahip birden fazla kayıt ekleyemezsiniz.
   - Çözüm olarak, `team_id` alanını `primary_key=True` olmadan tanımlayın. Eğer `primary_key=True` kullanmanız gerekmiyorsa, onu kaldırın ve `id` alanını Django’nun varsayılan birincil anahtar alanı olarak kullanın.

   ```python
   class Team(models.Model):
       team_id = models.IntegerField()  # primary_key=True kaldırıldı
       team_name = models.CharField(max_length=255)
       team_slug = models.SlugField(max_length=255)
       team_shortName = models.CharField(max_length=100)
       team_nameCode = models.CharField(max_length=10)
       team_national = models.BooleanField(default=False)

       tournament = models.ForeignKey(Tournament, on_delete=models.CASCADE, db_column='tournament_id', related_name='teams')
       season = models.ForeignKey(Season, on_delete=models.CASCADE, db_column='season_id', related_name='teams2')

       def __str__(self):
           return f"{self.team_name} ({self.tournament.tournament_name} - {self.season.season_name})"

       class Meta:
           unique_together = ('team_id', 'tournament', 'season')
   ```

2. **Veritabanı Şemasını Güncelleyin:**
   - Bu değişiklikten sonra, veritabanı şemasını güncellemek için aşağıdaki komutları çalıştırarak migrasyon yapın:
   
     ```bash
     python manage.py makemigrations
     python manage.py migrate
     ```

3. **Eski Kayıtları Temizleyin:**
   - Veritabanında mevcut aynı `team_id` değerine sahip kayıtlar varsa, `unique_together` kısıtına uymayanları temizlemeniz gerekebilir. Örneğin:

     ```python
     Team.objects.filter(team_id=duplike_olan_id).delete()
     ```

Bu adımlarla birlikte, `team_id` alanı artık yalnızca `tournament` ve `season` ile kombinlenerek benzersiz olacak ve `UNIQUE constraint` hatası çözülmelidir.

***Soru:*** ---------------------------------------------------------------------------
OperationalError                          Traceback (most recent call last)
File ~/Masaüstü/myenv/lib/python3.12/site-packages/django/db/backends/utils.py:105, in CursorWrapper._execute(self, sql, params, *ignored_wrapper_args)
    104 else:
--> 105     return self.cursor.execute(sql, params)

File ~/Masaüstü/myenv/lib/python3.12/site-packages/django/db/backends/sqlite3/base.py:354, in SQLiteCursorWrapper.execute(self, query, params)
    353 query = self.convert_query(query, param_names=param_names)
--> 354 return super().execute(query, params)

OperationalError: no such column: tournaments_team.id

The above exception was the direct cause of the following exception:

OperationalError                          Traceback (most recent call last)
Cell In[5], line 243
    241 api.tournament_data()
    242 api.season_data()
--> 243 api.team_data()
    244 api.match_data()
    245 print("İşlemler bitti")

Cell In[5], line 152, in SofascoreAPI.team_data(self)
    148 season_instance = Season.objects.filter(season_id=season_id).first()
    150 if tournament_instance and season_instance:
    151     # Mevcut kayıt varsa güncelle, yoksa yeni kayıt oluştur
--> 152     team, created = Team.objects.update_or_create(
    153         team_id=team_id,
    154         tournament=tournament_instance,
    155         season=season_instance,
    156         defaults={
    157             'team_name': row['team_name'],
    158             'team_slug': row['team_slug'],
    159             'team_shortName': row['team_shortName'],
    160             'team_nameCode': row['team_nameCode'],
    161             'team_national': row['team_national'],
    162         }
    163     )
    164     if created:
    165         print(f"Team ID {team_id} başarıyla eklendi.")

File ~/Masaüstü/myenv/lib/python3.12/site-packages/django/db/models/manager.py:87, in BaseManager._get_queryset_methods.<locals>.create_method.<locals>.manager_method(self, *args, **kwargs)
     85 @wraps(method)
     86 def manager_method(self, *args, **kwargs):
---> 87     return getattr(self.get_queryset(), name)(*args, **kwargs)

File ~/Masaüstü/myenv/lib/python3.12/site-packages/django/db/models/query.py:986, in QuerySet.update_or_create(self, defaults, create_defaults, **kwargs)
    982 self._for_write = True
    983 with transaction.atomic(using=self.db):
    984     # Lock the row so that a concurrent update is blocked until
    985     # update_or_create() has performed its save.
--> 986     obj, created = self.select_for_update().get_or_create(
    987         create_defaults, **kwargs
    988     )
    989     if created:
    990         return obj, created

File ~/Masaüstü/myenv/lib/python3.12/site-packages/django/db/models/query.py:948, in QuerySet.get_or_create(self, defaults, **kwargs)
    946 self._for_write = True
    947 try:
--> 948     return self.get(**kwargs), False
    949 except self.model.DoesNotExist:
    950     params = self._extract_model_params(defaults, **kwargs)

File ~/Masaüstü/myenv/lib/python3.12/site-packages/django/db/models/query.py:645, in QuerySet.get(self, *args, **kwargs)
    643     limit = MAX_GET_RESULTS
    644     clone.query.set_limits(high=limit)
--> 645 num = len(clone)
    646 if num == 1:
    647     return clone._result_cache[0]

File ~/Masaüstü/myenv/lib/python3.12/site-packages/django/db/models/query.py:382, in QuerySet.__len__(self)
    381 def __len__(self):
--> 382     self._fetch_all()
    383     return len(self._result_cache)

File ~/Masaüstü/myenv/lib/python3.12/site-packages/django/db/models/query.py:1928, in QuerySet._fetch_all(self)
   1926 def _fetch_all(self):
   1927     if self._result_cache is None:
-> 1928         self._result_cache = list(self._iterable_class(self))
   1929     if self._prefetch_related_lookups and not self._prefetch_done:
   1930         self._prefetch_related_objects()

File ~/Masaüstü/myenv/lib/python3.12/site-packages/django/db/models/query.py:91, in ModelIterable.__iter__(self)
     88 compiler = queryset.query.get_compiler(using=db)
     89 # Execute the query. This will also fill compiler.select, klass_info,
     90 # and annotations.
---> 91 results = compiler.execute_sql(
     92     chunked_fetch=self.chunked_fetch, chunk_size=self.chunk_size
     93 )
     94 select, klass_info, annotation_col_map = (
     95     compiler.select,
     96     compiler.klass_info,
     97     compiler.annotation_col_map,
     98 )
     99 model_cls = klass_info["model"]

File ~/Masaüstü/myenv/lib/python3.12/site-packages/django/db/models/sql/compiler.py:1574, in SQLCompiler.execute_sql(self, result_type, chunked_fetch, chunk_size)
   1572     cursor = self.connection.cursor()
   1573 try:
-> 1574     cursor.execute(sql, params)
   1575 except Exception:
   1576     # Might fail for server-side cursors (e.g. connection closed)
   1577     cursor.close()

File ~/Masaüstü/myenv/lib/python3.12/site-packages/django/db/backends/utils.py:122, in CursorDebugWrapper.execute(self, sql, params)
    120 def execute(self, sql, params=None):
    121     with self.debug_sql(sql, params, use_last_executed_query=True):
--> 122         return super().execute(sql, params)

File ~/Masaüstü/myenv/lib/python3.12/site-packages/django/db/backends/utils.py:79, in CursorWrapper.execute(self, sql, params)
     78 def execute(self, sql, params=None):
---> 79     return self._execute_with_wrappers(
     80         sql, params, many=False, executor=self._execute
     81     )

File ~/Masaüstü/myenv/lib/python3.12/site-packages/django/db/backends/utils.py:92, in CursorWrapper._execute_with_wrappers(self, sql, params, many, executor)
     90 for wrapper in reversed(self.db.execute_wrappers):
     91     executor = functools.partial(wrapper, executor)
---> 92 return executor(sql, params, many, context)

File ~/Masaüstü/myenv/lib/python3.12/site-packages/django/db/backends/utils.py:100, in CursorWrapper._execute(self, sql, params, *ignored_wrapper_args)
     98     warnings.warn(self.APPS_NOT_READY_WARNING_MSG, category=RuntimeWarning)
     99 self.db.validate_no_broken_transaction()
--> 100 with self.db.wrap_database_errors:
    101     if params is None:
    102         # params default might be backend specific.
    103         return self.cursor.execute(sql)

File ~/Masaüstü/myenv/lib/python3.12/site-packages/django/db/utils.py:91, in DatabaseErrorWrapper.__exit__(self, exc_type, exc_value, traceback)
     89 if dj_exc_type not in (DataError, IntegrityError):
     90     self.wrapper.errors_occurred = True
---> 91 raise dj_exc_value.with_traceback(traceback) from exc_value

File ~/Masaüstü/myenv/lib/python3.12/site-packages/django/db/backends/utils.py:105, in CursorWrapper._execute(self, sql, params, *ignored_wrapper_args)
    103     return self.cursor.execute(sql)
    104 else:
--> 105     return self.cursor.execute(sql, params)

File ~/Masaüstü/myenv/lib/python3.12/site-packages/django/db/backends/sqlite3/base.py:354, in SQLiteCursorWrapper.execute(self, query, params)
    352 param_names = list(params) if isinstance(params, Mapping) else None
    353 query = self.convert_query(query, param_names=param_names)
--> 354 return super().execute(query, params)

OperationalError: no such column: tournaments_team.id

**Cevap:** Bu hata, `Team` modelinizde birincil anahtar alanı (`id`) eksik olduğunda oluşur. Django, her model için varsayılan olarak bir `id` alanı oluşturur, ancak `team_id` alanını `primary_key=True` olarak belirttiğimizde, Django artık `id` sütununu oluşturmaz.

Eğer `team_id`'i `primary_key=True` olarak kullanmak istemiyorsanız, `id` alanını Django'nun varsayılan birincil anahtar alanı olarak bırakmanız gerekir. Bu şekilde `Team` modeli, otomatik olarak bir `id` sütununa sahip olur.

### Çözüm

1. **`primary_key=True` Özelliğini Kaldırın:**

   `team_id` alanındaki `primary_key=True` ifadesini kaldırarak Django'nun `id` sütununu otomatik olarak oluşturmasına izin verin.

   ```python
   class Team(models.Model):
       team_id = models.IntegerField()  # primary_key=True kaldırıldı
       team_name = models.CharField(max_length=255)
       team_slug = models.SlugField(max_length=255)
       team_shortName = models.CharField(max_length=100)
       team_nameCode = models.CharField(max_length=10)
       team_national = models.BooleanField(default=False)
       
       tournament = models.ForeignKey(Tournament, on_delete=models.CASCADE, db_column='tournament_id', related_name='teams')
       season = models.ForeignKey(Season, on_delete=models.CASCADE, db_column='season_id', related_name='teams2')

       def __str__(self):
           return f"{self.team_name} ({self.tournament.tournament_name} - {self.season.season_name})"

       class Meta:
           unique_together = ('team_id', 'tournament', 'season')
   ```

2. **Migrate İşlemlerini Çalıştırın:**

   Bu değişiklikten sonra, veritabanınızdaki şemayı güncellemek için şu komutları çalıştırın:

   ```bash
   python manage.py makemigrations
   python manage.py migrate
   ```

Bu değişikliklerle birlikte Django artık `id` sütununu otomatik olarak ekleyecek ve `OperationalError: no such column: tournaments_team.id` hatası ortadan kalkacaktır.

***Soru:*** OperationalError at /admin/tournaments/team/
no such column: tournaments_team.id
Request Method:	GET
Request URL:	http://127.0.0.1:8000/admin/tournaments/team/
Django Version:	5.1.1
Exception Type:	OperationalError
Exception Value:	
no such column: tournaments_team.id
Exception Location:	/home/ahmety/Masaüstü/myenv/lib/python3.12/site-packages/django/db/backends/sqlite3/base.py, line 354, in execute
Raised during:	django.contrib.admin.options.changelist_view
Python Executable:	/home/ahmety/Masaüstü/myenv/bin/python
Python Version:	3.12.3
Python Path:	
['/home/ahmety/Masaüstü/FxN',
 '/usr/lib/python312.zip',
 '/usr/lib/python3.12',
 '/usr/lib/python3.12/lib-dynload',
 '/home/ahmety/Masaüstü/myenv/lib/python3.12/site-packages']
Server time:	Mon, 28 Oct 2024 16:11:43 +0300

**Cevap:** Bu hata, veritabanınızın mevcut şemasında `id` sütununun eksik olmasından kaynaklanıyor. Daha önce `primary_key=True` kullanarak `id` sütununu kaldırdıysanız, yapılan değişiklikleri uygulamak için aşağıdaki adımları izleyebilirsiniz.

### Çözüm Adımları

1. **Veritabanını Silin ve Yeniden Oluşturun (Geliştirme Ortamı için):**
   Eğer bu veritabanını bir üretim ortamında kullanmıyorsanız, en hızlı çözüm veritabanını silip baştan oluşturmaktır. Bu, özellikle yapısal değişiklikler sonrası veritabanını tamamen sıfırlamak için en etkili yöntemdir.

   Aşağıdaki adımları izleyin:

   - `db.sqlite3` dosyasını silin (veya başka bir veritabanı kullanıyorsanız o veritabanını temizleyin).
   - Ardından, tüm migrasyonları tekrar uygulayın:

     ```bash
     python manage.py makemigrations
     python manage.py migrate
     ```

   Bu işlem, Django’nun tüm modelleri doğru şekilde yeniden oluşturmasına izin verecektir.

2. **Veritabanını Silmeden Çözüm Bulmak:**
   Eğer veritabanını silmek istemiyorsanız, modelde `primary_key=True` ifadesini kaldırdıktan sonra sırasıyla aşağıdaki işlemleri yapabilirsiniz:

   - Yeni migrasyon dosyasını oluşturmak için:

     ```bash
     python manage.py makemigrations
     ```

   - Django’nun yeni bir `id` sütunu eklemesini sağlamak için migrasyon işlemini çalıştırın:

     ```bash
     python manage.py migrate
     ```

   Ancak, veritabanı şemasında önceki `primary_key=True` kısıtlamasından dolayı bazı sütunlar karışabilir; bu durumda veritabanını sıfırlamak daha güvenilir bir yol olabilir.

### Not

Bu işlemlerden sonra tekrar `python manage.py runserver` komutunu çalıştırarak uygulamanızı yeniden başlatın. Admin paneline girdiğinizde artık `id` sütununa erişim hatası ile karşılaşmamanız gerekir.

***Soru:*** --------------------------------------------------------------------------
DoesNotExist                              Traceback (most recent call last)
File ~/Masaüstü/myenv/lib/python3.12/site-packages/django/db/models/query.py:948, in QuerySet.get_or_create(self, defaults, **kwargs)
    947 try:
--> 948     return self.get(**kwargs), False
    949 except self.model.DoesNotExist:

File ~/Masaüstü/myenv/lib/python3.12/site-packages/django/db/models/query.py:649, in QuerySet.get(self, *args, **kwargs)
    648 if not num:
--> 649     raise self.model.DoesNotExist(
    650         "%s matching query does not exist." % self.model._meta.object_name
    651     )
    652 raise self.model.MultipleObjectsReturned(
    653     "get() returned more than one %s -- it returned %s!"
    654     % (
   (...)
    657     )
    658 )

DoesNotExist: Team matching query does not exist.

During handling of the above exception, another exception occurred:

IntegrityError                            Traceback (most recent call last)
File ~/Masaüstü/myenv/lib/python3.12/site-packages/django/db/backends/utils.py:105, in CursorWrapper._execute(self, sql, params, *ignored_wrapper_args)
    104 else:
--> 105     return self.cursor.execute(sql, params)

File ~/Masaüstü/myenv/lib/python3.12/site-packages/django/db/backends/sqlite3/base.py:354, in SQLiteCursorWrapper.execute(self, query, params)
    353 query = self.convert_query(query, param_names=param_names)
--> 354 return super().execute(query, params)

IntegrityError: UNIQUE constraint failed: tournaments_team.team_id

The above exception was the direct cause of the following exception:

IntegrityError                            Traceback (most recent call last)
Cell In[6], line 243
    241 api.tournament_data()
    242 api.season_data()
--> 243 api.team_data()
    244 api.match_data()
    245 print("İşlemler bitti")

Cell In[6], line 152, in SofascoreAPI.team_data(self)
    148 season_instance = Season.objects.filter(season_id=season_id).first()
    150 if tournament_instance and season_instance:
    151     # Mevcut kayıt varsa güncelle, yoksa yeni kayıt oluştur
--> 152     team, created = Team.objects.update_or_create(
    153         team_id=team_id,
    154         tournament=tournament_instance,
    155         season=season_instance,
    156         defaults={
    157             'team_name': row['team_name'],
    158             'team_slug': row['team_slug'],
    159             'team_shortName': row['team_shortName'],
    160             'team_nameCode': row['team_nameCode'],
    161             'team_national': row['team_national'],
    162         }
    163     )
    164     if created:
    165         print(f"Team ID {team_id} başarıyla eklendi.")

File ~/Masaüstü/myenv/lib/python3.12/site-packages/django/db/models/manager.py:87, in BaseManager._get_queryset_methods.<locals>.create_method.<locals>.manager_method(self, *args, **kwargs)
     85 @wraps(method)
     86 def manager_method(self, *args, **kwargs):
---> 87     return getattr(self.get_queryset(), name)(*args, **kwargs)

File ~/Masaüstü/myenv/lib/python3.12/site-packages/django/db/models/query.py:986, in QuerySet.update_or_create(self, defaults, create_defaults, **kwargs)
    982 self._for_write = True
    983 with transaction.atomic(using=self.db):
    984     # Lock the row so that a concurrent update is blocked until
    985     # update_or_create() has performed its save.
--> 986     obj, created = self.select_for_update().get_or_create(
    987         create_defaults, **kwargs
    988     )
    989     if created:
    990         return obj, created

File ~/Masaüstü/myenv/lib/python3.12/site-packages/django/db/models/query.py:955, in QuerySet.get_or_create(self, defaults, **kwargs)
    953     with transaction.atomic(using=self.db):
    954         params = dict(resolve_callables(params))
--> 955         return self.create(**params), True
    956 except IntegrityError:
    957     try:

File ~/Masaüstü/myenv/lib/python3.12/site-packages/django/db/models/query.py:679, in QuerySet.create(self, **kwargs)
    677 obj = self.model(**kwargs)
    678 self._for_write = True
--> 679 obj.save(force_insert=True, using=self.db)
    680 return obj

File ~/Masaüstü/myenv/lib/python3.12/site-packages/django/db/models/base.py:891, in Model.save(self, force_insert, force_update, using, update_fields, *args)
    888     if loaded_fields:
    889         update_fields = frozenset(loaded_fields)
--> 891 self.save_base(
    892     using=using,
    893     force_insert=force_insert,
    894     force_update=force_update,
    895     update_fields=update_fields,
    896 )

File ~/Masaüstü/myenv/lib/python3.12/site-packages/django/db/models/base.py:997, in Model.save_base(self, raw, force_insert, force_update, using, update_fields)
    993         force_insert = self._validate_force_insert(force_insert)
    994         parent_inserted = self._save_parents(
    995             cls, using, update_fields, force_insert
    996         )
--> 997     updated = self._save_table(
    998         raw,
    999         cls,
   1000         force_insert or parent_inserted,
   1001         force_update,
   1002         using,
   1003         update_fields,
   1004     )
   1005 # Store the database on which the object was saved
   1006 self._state.db = using

File ~/Masaüstü/myenv/lib/python3.12/site-packages/django/db/models/base.py:1160, in Model._save_table(self, raw, cls, force_insert, force_update, using, update_fields)
   1154 fields = [
   1155     f
   1156     for f in meta.local_concrete_fields
   1157     if not f.generated and (pk_set or f is not meta.auto_field)
   1158 ]
   1159 returning_fields = meta.db_returning_fields
-> 1160 results = self._do_insert(
   1161     cls._base_manager, using, fields, returning_fields, raw
   1162 )
   1163 if results:
   1164     for value, field in zip(results[0], returning_fields):

File ~/Masaüstü/myenv/lib/python3.12/site-packages/django/db/models/base.py:1201, in Model._do_insert(self, manager, using, fields, returning_fields, raw)
   1196 def _do_insert(self, manager, using, fields, returning_fields, raw):
   1197     """
   1198     Do an INSERT. If returning_fields is defined then this method should
   1199     return the newly created data for the model.
   1200     """
-> 1201     return manager._insert(
   1202         [self],
   1203         fields=fields,
   1204         returning_fields=returning_fields,
   1205         using=using,
   1206         raw=raw,
   1207     )

File ~/Masaüstü/myenv/lib/python3.12/site-packages/django/db/models/manager.py:87, in BaseManager._get_queryset_methods.<locals>.create_method.<locals>.manager_method(self, *args, **kwargs)
     85 @wraps(method)
     86 def manager_method(self, *args, **kwargs):
---> 87     return getattr(self.get_queryset(), name)(*args, **kwargs)

File ~/Masaüstü/myenv/lib/python3.12/site-packages/django/db/models/query.py:1847, in QuerySet._insert(self, objs, fields, returning_fields, raw, using, on_conflict, update_fields, unique_fields)
   1840 query = sql.InsertQuery(
   1841     self.model,
   1842     on_conflict=on_conflict,
   1843     update_fields=update_fields,
   1844     unique_fields=unique_fields,
   1845 )
   1846 query.insert_values(fields, objs, raw=raw)
-> 1847 return query.get_compiler(using=using).execute_sql(returning_fields)

File ~/Masaüstü/myenv/lib/python3.12/site-packages/django/db/models/sql/compiler.py:1836, in SQLInsertCompiler.execute_sql(self, returning_fields)
   1834 with self.connection.cursor() as cursor:
   1835     for sql, params in self.as_sql():
-> 1836         cursor.execute(sql, params)
   1837     if not self.returning_fields:
   1838         return []

File ~/Masaüstü/myenv/lib/python3.12/site-packages/django/db/backends/utils.py:122, in CursorDebugWrapper.execute(self, sql, params)
    120 def execute(self, sql, params=None):
    121     with self.debug_sql(sql, params, use_last_executed_query=True):
--> 122         return super().execute(sql, params)

File ~/Masaüstü/myenv/lib/python3.12/site-packages/django/db/backends/utils.py:79, in CursorWrapper.execute(self, sql, params)
     78 def execute(self, sql, params=None):
---> 79     return self._execute_with_wrappers(
     80         sql, params, many=False, executor=self._execute
     81     )

File ~/Masaüstü/myenv/lib/python3.12/site-packages/django/db/backends/utils.py:92, in CursorWrapper._execute_with_wrappers(self, sql, params, many, executor)
     90 for wrapper in reversed(self.db.execute_wrappers):
     91     executor = functools.partial(wrapper, executor)
---> 92 return executor(sql, params, many, context)

File ~/Masaüstü/myenv/lib/python3.12/site-packages/django/db/backends/utils.py:100, in CursorWrapper._execute(self, sql, params, *ignored_wrapper_args)
     98     warnings.warn(self.APPS_NOT_READY_WARNING_MSG, category=RuntimeWarning)
     99 self.db.validate_no_broken_transaction()
--> 100 with self.db.wrap_database_errors:
    101     if params is None:
    102         # params default might be backend specific.
    103         return self.cursor.execute(sql)

File ~/Masaüstü/myenv/lib/python3.12/site-packages/django/db/utils.py:91, in DatabaseErrorWrapper.__exit__(self, exc_type, exc_value, traceback)
     89 if dj_exc_type not in (DataError, IntegrityError):
     90     self.wrapper.errors_occurred = True
---> 91 raise dj_exc_value.with_traceback(traceback) from exc_value

File ~/Masaüstü/myenv/lib/python3.12/site-packages/django/db/backends/utils.py:105, in CursorWrapper._execute(self, sql, params, *ignored_wrapper_args)
    103     return self.cursor.execute(sql)
    104 else:
--> 105     return self.cursor.execute(sql, params)

File ~/Masaüstü/myenv/lib/python3.12/site-packages/django/db/backends/sqlite3/base.py:354, in SQLiteCursorWrapper.execute(self, query, params)
    352 param_names = list(params) if isinstance(params, Mapping) else None
    353 query = self.convert_query(query, param_names=param_names)
--> 354 return super().execute(query, params)

IntegrityError: UNIQUE constraint failed: tournaments_team.team_id  bu hatanın hiç oluşmamasını istiyorum 
import os
import django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'Home.settings')
django.setup()
os.environ["DJANGO_ALLOW_ASYNC_UNSAFE"] = "true"
from tournaments.models import Tournament, Season, Team,Match
from tournaments.models import FikstureModelData
from datetime import datetime, timedelta

class SofascoreAPI:
    def __init__(self):
        pass

    def fetch_data(self):
        data = FikstureModelData.objects.all().values()
        data_list = list(data)
        df = pd.DataFrame(data_list)
        df_exploded = df.explode('data')
        expanded_data = pd.json_normalize(df_exploded['data'])
        expanded_data['tarih'] = list(df_exploded['tarih'])
        veri = expanded_data.copy()
        veri.columns = [item.replace(".", "_") for item in veri.columns]
        return veri

    def tournament_data(self):
        verim = self.fetch_data()
        if verim is None:
            raise ValueError("Veri işlenmedi. Önce 'process_data()' metodunu çalıştırın.")
        
        # Aynı uniqueTournament_id'ye sahip olanları tekrar kontrol et
        verim = verim.drop_duplicates("tournament_uniqueTournament_id")
        
        cols = [
            "tournament_uniqueTournament_id", "tournament_name", "tournament_slug", "tournament_category_name",
            "tournament_category_slug", "tournament_uniqueTournament_category_id", 
            "tournament_uniqueTournament_hasEventPlayerStatistics", "tournament_id", "tournament_isGroup", 
            "tournament_uniqueTournament_hasPerformanceGraphFeature"
        ]
        
        for col in cols:
            if col not in verim.columns:
                verim.loc[:, col] = 0

        verim = verim[cols]

        for _, row in verim.iterrows():
            tournament_id = row['tournament_uniqueTournament_id']
            
            if pd.isna(tournament_id):
                print(f"Geçersiz tournament_uniqueTournament_id: {tournament_id}, atlanıyor.")
                continue
        
            if not Tournament.objects.filter(tournament_id=tournament_id).exists():
                Tournament.objects.create(
                    tournament_id=row['tournament_uniqueTournament_id'],
                    tournament_name=row['tournament_name'],
                    tournament_slug=row['tournament_slug'],
                    tournament_category_name=row['tournament_category_name'],
                    tournament_category_slug=row['tournament_category_slug'],
                    tournament_uniqueTournament_category_id=row['tournament_uniqueTournament_category_id'],
                    tournament_model_id=row['tournament_id'],
                    tournament_isGroup=row['tournament_isGroup'] if pd.notna(row['tournament_isGroup']) else False,
                    tournament_uniqueTournament_hasPerformanceGraphFeature=row['tournament_uniqueTournament_hasPerformanceGraphFeature'] if pd.notna(row['tournament_uniqueTournament_hasPerformanceGraphFeature']) else False
                )
                print(f"Tournament ID {tournament_id} başarıyla eklendi.")
            else:
                print(f"Tournament ID {tournament_id} zaten mevcut, eklenmedi.")

    def season_data(self):
        verim = self.fetch_data()
        if verim is None:
            raise ValueError("Veri işlenmedi. Önce 'process_data()' metodunu çalıştırın.")
        
        verim = verim.drop_duplicates("season_id")
        
        season_cols = ["season_id", "season_name", "season_year","tournament_uniqueTournament_id"]

        for col in season_cols:
            if col not in verim.columns:
                verim.loc[:, col] = 0

        verim = verim[season_cols]

        for _, row in verim.iterrows():
            season_id = row['season_id']
            tournament_id = row.get('tournament_uniqueTournament_id')
    
            if pd.isna(season_id) or pd.isna(tournament_id):
                print(f"Geçersiz season_id veya tournament_id: Season ID={season_id}, Tournament ID={tournament_id}. Atlanıyor.")
                continue
    
            if not Season.objects.filter(season_id=season_id).exists():
                tournament_instance = Tournament.objects.filter(tournament_id=tournament_id).first()
                
                if tournament_instance:
                    Season.objects.create(
                        season_id=row['season_id'],
                        season_name=row['season_name'],
                        season_year=row['season_year'],
                        tournament=tournament_instance  # Doğru sütun adı burada kullanılıyor
                    )
                    print(f"Season ID {season_id} başarıyla eklendi.")
                else:
                    print(f"Tournament ID {tournament_id} bulunamadı, Season ID {season_id} eklenemedi.")
            else:
                print(f"Season ID {season_id} zaten mevcut, eklenmedi.")
    
   
    def team_data(self):

        data = self.fetch_data()
        homecols = [
                    "homeTeam_id", "homeTeam_name", "homeTeam_slug", "homeTeam_shortName",
                    "homeTeam_nameCode", "homeTeam_national", "tournament_uniqueTournament_id", "season_id"
                ]
        
        awaycols = [
                    "awayTeam_id", "awayTeam_name", "awayTeam_slug", "awayTeam_shortName",
                    "awayTeam_nameCode", "awayTeam_national", "tournament_uniqueTournament_id", "season_id"
                ]
        
        # Home takımı için veri seçimi ve kolon isimlerinin ayarlanması
        homedata = data[homecols]
        homedata.columns = ["team_id", "team_name", "team_slug", "team_shortName",
                                       "team_nameCode", "team_national", "tournament_id", "season_id"]
        
        # Away takımı için veri seçimi ve kolon isimlerinin ayarlanması
        awaydata = data[awaycols]
        awaydata.columns  = ["team_id", "team_name", "team_slug", "team_shortName",
                                       "team_nameCode", "team_national", "tournament_id", "season_id"]
        
        # Home ve Away takımları birleştirme
        teamdata = pd.concat([homedata, awaydata])
        teamdata = teamdata.drop_duplicates(subset=["team_id", "tournament_id", "season_id"])
       
        for _, row in teamdata.iterrows():
            team_id = row['team_id']
            tournament_id = row['tournament_id']
            season_id = row['season_id']
            
            # Geçersiz veya eksik id'leri atla
            if pd.isna(team_id) or pd.isna(tournament_id) or pd.isna(season_id):
                print(f"Geçersiz değer: Team ID={team_id}, Tournament ID={tournament_id}, Season ID={season_id}. Atlanıyor.")
                continue
        
            # İlgili tournament ve season nesnelerini getir
            tournament_instance = Tournament.objects.filter(tournament_id=tournament_id).first()
            season_instance = Season.objects.filter(season_id=season_id).first()
        
            if tournament_instance and season_instance:
                # Mevcut kayıt varsa güncelle, yoksa yeni kayıt oluştur
                team, created = Team.objects.update_or_create(
                    team_id=team_id,
                    tournament=tournament_instance,
                    season=season_instance,
                    defaults={
                        'team_name': row['team_name'],
                        'team_slug': row['team_slug'],
                        'team_shortName': row['team_shortName'],
                        'team_nameCode': row['team_nameCode'],
                        'team_national': row['team_national'],
                    }
                )
                if created:
                    print(f"Team ID {team_id} başarıyla eklendi.")
                else:
                    print(f"Team ID {team_id} güncellenerek kaydedildi.")
            else:
                print(f"Tournament ID {tournament_id} veya Season ID {season_id} bulunamadı.")

    def match_data(self):
        # Fetch data from the API or existing model
        verim = self.fetch_data()
        if verim is None:
            raise ValueError("Veri işlenmedi. Lütfen önce 'process_data()' metodunu çalıştırın.")
        
     
     
        new_cols = ['id', 'startTimestamp', 'slug', 'tournament_uniqueTournament_id', 'season_id',
                    'roundInfo_round', 'status_type', 'homeTeam_id', 'awayTeam_id',
                    'homeScore_current', 'homeScore_period1', 'homeScore_period2', 'homeScore_normaltime',
                    'awayScore_current', 'awayScore_period1', 'awayScore_period2', 'awayScore_normaltime']
        
        df1 = verim[new_cols] 
        df1['date'] = pd.to_datetime(df1['startTimestamp'], unit='s') + timedelta(hours=3)
        df2 = df1.drop("startTimestamp", axis=1)
        df3 = df2.fillna(0)
        for _, row in df3.iterrows():
            match_id = row['id']
            tournament_id = row['tournament_uniqueTournament_id']
            season_id = row['season_id']
            home_team_id = row['homeTeam_id']
            away_team_id = row['awayTeam_id']
            
            # Geçersiz veya eksik id'leri atla
            if pd.isna(match_id) or pd.isna(tournament_id) or pd.isna(season_id) or pd.isna(home_team_id) or pd.isna(away_team_id):
                print(f"Geçersiz değer: Match ID={match_id}, Tournament ID={tournament_id}, Season ID={season_id}, Home Team ID={home_team_id}, Away Team ID={away_team_id}. Atlanıyor.")
                continue

            # İlgili foreign key nesnelerini getir
            tournament_instance = Tournament.objects.filter(tournament_id=tournament_id).first()
            season_instance = Season.objects.filter(season_id=season_id).first()
            home_team_instance = Team.objects.filter(team_id=home_team_id).first()
            away_team_instance = Team.objects.filter(team_id=away_team_id).first()

            if tournament_instance and season_instance and home_team_instance and away_team_instance:
                # Match'in veritabanında olup olmadığını kontrol et, yoksa oluştur
                if not Match.objects.filter(id=match_id).exists():
                    Match.objects.create(
                        id=match_id,
                        startTimestamp=row['date'],  # DateTimeField olarak datetime verisi
                        slug=row['slug'],
                        tournament=tournament_instance,
                        season=season_instance,
                        homeTeam=home_team_instance,
                        awayTeam=away_team_instance,
                        roundInfo_round=row['roundInfo_round'],
                        homeScore_current=row['homeScore_current'],
                        homeScore_period1=row['homeScore_period1'],
                        homeScore_period2=row['homeScore_period2'],
                        homeScore_normaltime=row['homeScore_normaltime'],
                        awayScore_current=row['awayScore_current'],
                        awayScore_period1=row['awayScore_period1'],
                        awayScore_period2=row['awayScore_period2'],
                        awayScore_normaltime=row['awayScore_normaltime'],
                        status_type = row['status_type']
                    )
                    print(f"Match ID {match_id} başarıyla eklendi.")
                else:
                    print(f"Match ID {match_id} zaten mevcut, eklenmedi.")
            else:
                print(f"Tournament ID {tournament_id}, Season ID {season_id}, Home Team ID {home_team_id}, Away Team ID {away_team_id} bulunamadı.")





# SofascoreAPI sınıfını kullanarak team_data'yı veritabanına kaydetmek için:
api = SofascoreAPI()
teamdata = api.fetch_data()  # Veriyi getirin (API'den ya da dosyadan)
api.tournament_data()
api.season_data()
api.team_data()
api.match_data()
print("İşlemler bitti")

**Cevap:** Bu hatayı önlemek için `update_or_create` işleminden önce eski kayıtları silerek benzersiz (UNIQUE) kısıt hatalarını engelleyebiliriz. `team_id`, `tournament`, ve `season` alanları ile benzersiz bir kombinasyon yaratmamız gerektiğinden, önce aynı `team_id`, `tournament`, ve `season` kombinasyonuna sahip kayıt varsa onu silebiliriz.

### Güncellenmiş `team_data` Yöntemi

Aşağıda, eski kaydı silen ve ardından yeni kaydı oluşturan güncellenmiş bir `team_data` yöntemi bulabilirsiniz:

```python
def team_data(self):
    data = self.fetch_data()
    homecols = [
                "homeTeam_id", "homeTeam_name", "homeTeam_slug", "homeTeam_shortName",
                "homeTeam_nameCode", "homeTeam_national", "tournament_uniqueTournament_id", "season_id"
            ]
    
    awaycols = [
                "awayTeam_id", "awayTeam_name", "awayTeam_slug", "awayTeam_shortName",
                "awayTeam_nameCode", "awayTeam_national", "tournament_uniqueTournament_id", "season_id"
            ]
    
    # Home takımı için veri seçimi ve kolon isimlerinin ayarlanması
    homedata = data[homecols]
    homedata.columns = ["team_id", "team_name", "team_slug", "team_shortName",
                                   "team_nameCode", "team_national", "tournament_id", "season_id"]
    
    # Away takımı için veri seçimi ve kolon isimlerinin ayarlanması
    awaydata = data[awaycols]
    awaydata.columns  = ["team_id", "team_name", "team_slug", "team_shortName",
                                   "team_nameCode", "team_national", "tournament_id", "season_id"]
    
    # Home ve Away takımları birleştirme
    teamdata = pd.concat([homedata, awaydata])
    teamdata = teamdata.drop_duplicates(subset=["team_id", "tournament_id", "season_id"])
   
    for _, row in teamdata.iterrows():
        team_id = row['team_id']
        tournament_id = row['tournament_id']
        season_id = row['season_id']
        
        # Geçersiz veya eksik id'leri atla
        if pd.isna(team_id) or pd.isna(tournament_id) or pd.isna(season_id):
            print(f"Geçersiz değer: Team ID={team_id}, Tournament ID={tournament_id}, Season ID={season_id}. Atlanıyor.")
            continue
    
        # İlgili tournament ve season nesnelerini getir
        tournament_instance = Tournament.objects.filter(tournament_id=tournament_id).first()
        season_instance = Season.objects.filter(season_id=season_id).first()
    
        if tournament_instance and season_instance:
            # Eski kaydı sil
            Team.objects.filter(team_id=team_id, tournament=tournament_instance, season=season_instance).delete()
            
            # Yeni kaydı oluştur
            team = Team.objects.create(
                team_id=team_id,
                team_name=row['team_name'],
                team_slug=row['team_slug'],
                team_shortName=row['team_shortName'],
                team_nameCode=row['team_nameCode'],
                team_national=row['team_national'],
                tournament=tournament_instance,
                season=season_instance
            )
            print(f"Team ID {team_id} başarıyla güncellenerek eklendi.")
        else:
            print(f"Tournament ID {tournament_id} veya Season ID {season_id} bulunamadı.")
```

### Açıklama

1. **Eski Kayıtların Silinmesi:** `Team.objects.filter(...).delete()` komutu, aynı `team_id`, `tournament`, ve `season` kombinasyonuna sahip eski kaydı siler. Böylece UNIQUE constraint hatasını önleriz.
2. **Yeni Kaydın Eklenmesi:** Eski kayıt silindikten sonra yeni kaydı güvenle oluştururuz.

Bu yöntem, aynı takımın aynı turnuva ve sezon için yalnızca bir kez kaydedilmesini garanti ederek UNIQUE kısıtını ihlal etmeden yeni veriyi eklemenizi sağlar.

***Soru:*** --------------------------------------------------------------------------
IntegrityError                            Traceback (most recent call last)
File ~/Masaüstü/myenv/lib/python3.12/site-packages/django/db/backends/utils.py:105, in CursorWrapper._execute(self, sql, params, *ignored_wrapper_args)
    104 else:
--> 105     return self.cursor.execute(sql, params)

File ~/Masaüstü/myenv/lib/python3.12/site-packages/django/db/backends/sqlite3/base.py:354, in SQLiteCursorWrapper.execute(self, query, params)
    353 query = self.convert_query(query, param_names=param_names)
--> 354 return super().execute(query, params)

IntegrityError: UNIQUE constraint failed: tournaments_team.team_id

The above exception was the direct cause of the following exception:

IntegrityError                            Traceback (most recent call last)
Cell In[5], line 240
    238 api.tournament_data()
    239 api.season_data()
--> 240 api.team_data()
    241 api.match_data()
    242 print("İşlemler bitti")

Cell In[5], line 154, in SofascoreAPI.team_data(self)
    151     Team.objects.filter(team_id=team_id, tournament=tournament_instance, season=season_instance).delete()
    153     # Yeni kaydı oluştur
--> 154     team = Team.objects.create(
    155         team_id=team_id,
    156         team_name=row['team_name'],
    157         team_slug=row['team_slug'],
    158         team_shortName=row['team_shortName'],
    159         team_nameCode=row['team_nameCode'],
    160         team_national=row['team_national'],
    161         tournament=tournament_instance,
    162         season=season_instance
    163     )
    164     print(f"Team ID {team_id} başarıyla güncellenerek eklendi.")
    165 else:

File ~/Masaüstü/myenv/lib/python3.12/site-packages/django/db/models/manager.py:87, in BaseManager._get_queryset_methods.<locals>.create_method.<locals>.manager_method(self, *args, **kwargs)
     85 @wraps(method)
     86 def manager_method(self, *args, **kwargs):
---> 87     return getattr(self.get_queryset(), name)(*args, **kwargs)

File ~/Masaüstü/myenv/lib/python3.12/site-packages/django/db/models/query.py:679, in QuerySet.create(self, **kwargs)
    677 obj = self.model(**kwargs)
    678 self._for_write = True
--> 679 obj.save(force_insert=True, using=self.db)
    680 return obj

File ~/Masaüstü/myenv/lib/python3.12/site-packages/django/db/models/base.py:891, in Model.save(self, force_insert, force_update, using, update_fields, *args)
    888     if loaded_fields:
    889         update_fields = frozenset(loaded_fields)
--> 891 self.save_base(
    892     using=using,
    893     force_insert=force_insert,
    894     force_update=force_update,
    895     update_fields=update_fields,
    896 )

File ~/Masaüstü/myenv/lib/python3.12/site-packages/django/db/models/base.py:997, in Model.save_base(self, raw, force_insert, force_update, using, update_fields)
    993         force_insert = self._validate_force_insert(force_insert)
    994         parent_inserted = self._save_parents(
    995             cls, using, update_fields, force_insert
    996         )
--> 997     updated = self._save_table(
    998         raw,
    999         cls,
   1000         force_insert or parent_inserted,
   1001         force_update,
   1002         using,
   1003         update_fields,
   1004     )
   1005 # Store the database on which the object was saved
   1006 self._state.db = using

File ~/Masaüstü/myenv/lib/python3.12/site-packages/django/db/models/base.py:1160, in Model._save_table(self, raw, cls, force_insert, force_update, using, update_fields)
   1154 fields = [
   1155     f
   1156     for f in meta.local_concrete_fields
   1157     if not f.generated and (pk_set or f is not meta.auto_field)
   1158 ]
   1159 returning_fields = meta.db_returning_fields
-> 1160 results = self._do_insert(
   1161     cls._base_manager, using, fields, returning_fields, raw
   1162 )
   1163 if results:
   1164     for value, field in zip(results[0], returning_fields):

File ~/Masaüstü/myenv/lib/python3.12/site-packages/django/db/models/base.py:1201, in Model._do_insert(self, manager, using, fields, returning_fields, raw)
   1196 def _do_insert(self, manager, using, fields, returning_fields, raw):
   1197     """
   1198     Do an INSERT. If returning_fields is defined then this method should
   1199     return the newly created data for the model.
   1200     """
-> 1201     return manager._insert(
   1202         [self],
   1203         fields=fields,
   1204         returning_fields=returning_fields,
   1205         using=using,
   1206         raw=raw,
   1207     )

File ~/Masaüstü/myenv/lib/python3.12/site-packages/django/db/models/manager.py:87, in BaseManager._get_queryset_methods.<locals>.create_method.<locals>.manager_method(self, *args, **kwargs)
     85 @wraps(method)
     86 def manager_method(self, *args, **kwargs):
---> 87     return getattr(self.get_queryset(), name)(*args, **kwargs)

File ~/Masaüstü/myenv/lib/python3.12/site-packages/django/db/models/query.py:1847, in QuerySet._insert(self, objs, fields, returning_fields, raw, using, on_conflict, update_fields, unique_fields)
   1840 query = sql.InsertQuery(
   1841     self.model,
   1842     on_conflict=on_conflict,
   1843     update_fields=update_fields,
   1844     unique_fields=unique_fields,
   1845 )
   1846 query.insert_values(fields, objs, raw=raw)
-> 1847 return query.get_compiler(using=using).execute_sql(returning_fields)

File ~/Masaüstü/myenv/lib/python3.12/site-packages/django/db/models/sql/compiler.py:1836, in SQLInsertCompiler.execute_sql(self, returning_fields)
   1834 with self.connection.cursor() as cursor:
   1835     for sql, params in self.as_sql():
-> 1836         cursor.execute(sql, params)
   1837     if not self.returning_fields:
   1838         return []

File ~/Masaüstü/myenv/lib/python3.12/site-packages/django/db/backends/utils.py:122, in CursorDebugWrapper.execute(self, sql, params)
    120 def execute(self, sql, params=None):
    121     with self.debug_sql(sql, params, use_last_executed_query=True):
--> 122         return super().execute(sql, params)

File ~/Masaüstü/myenv/lib/python3.12/site-packages/django/db/backends/utils.py:79, in CursorWrapper.execute(self, sql, params)
     78 def execute(self, sql, params=None):
---> 79     return self._execute_with_wrappers(
     80         sql, params, many=False, executor=self._execute
     81     )

File ~/Masaüstü/myenv/lib/python3.12/site-packages/django/db/backends/utils.py:92, in CursorWrapper._execute_with_wrappers(self, sql, params, many, executor)
     90 for wrapper in reversed(self.db.execute_wrappers):
     91     executor = functools.partial(wrapper, executor)
---> 92 return executor(sql, params, many, context)

File ~/Masaüstü/myenv/lib/python3.12/site-packages/django/db/backends/utils.py:100, in CursorWrapper._execute(self, sql, params, *ignored_wrapper_args)
     98     warnings.warn(self.APPS_NOT_READY_WARNING_MSG, category=RuntimeWarning)
     99 self.db.validate_no_broken_transaction()
--> 100 with self.db.wrap_database_errors:
    101     if params is None:
    102         # params default might be backend specific.
    103         return self.cursor.execute(sql)

File ~/Masaüstü/myenv/lib/python3.12/site-packages/django/db/utils.py:91, in DatabaseErrorWrapper.__exit__(self, exc_type, exc_value, traceback)
     89 if dj_exc_type not in (DataError, IntegrityError):
     90     self.wrapper.errors_occurred = True
---> 91 raise dj_exc_value.with_traceback(traceback) from exc_value

File ~/Masaüstü/myenv/lib/python3.12/site-packages/django/db/backends/utils.py:105, in CursorWrapper._execute(self, sql, params, *ignored_wrapper_args)
    103     return self.cursor.execute(sql)
    104 else:
--> 105     return self.cursor.execute(sql, params)

File ~/Masaüstü/myenv/lib/python3.12/site-packages/django/db/backends/sqlite3/base.py:354, in SQLiteCursorWrapper.execute(self, query, params)
    352 param_names = list(params) if isinstance(params, Mapping) else None
    353 query = self.convert_query(query, param_names=param_names)
--> 354 return super().execute(query, params)

IntegrityError: UNIQUE constraint failed: tournaments_team.team_id

**Cevap:** Bu hata, `Team` modelinizdeki `team_id` alanının benzersiz (UNIQUE) kısıtlaması nedeniyle aynı `team_id` değerine sahip birden fazla kayıt eklenmeye çalışıldığında oluşur. Bu durumda, `team_id`, `tournament`, ve `season` kombinasyonunu UNIQUE yapmamıza rağmen, SQLite veritabanında benzersiz olmayan bir `team_id` hatasına yol açabilir.

### Alternatif Çözüm: `update_or_create` ile Benzersizlik Sağlama

Aşağıda, `update_or_create` yöntemi ile aynı `team_id`, `tournament`, ve `season` kombinasyonuna sahip kaydın güncellenmesini ve benzersiz kısıtlamayı sağlamayı deneyebiliriz.

```python
def team_data(self):
    data = self.fetch_data()
    homecols = [
                "homeTeam_id", "homeTeam_name", "homeTeam_slug", "homeTeam_shortName",
                "homeTeam_nameCode", "homeTeam_national", "tournament_uniqueTournament_id", "season_id"
            ]
    
    awaycols = [
                "awayTeam_id", "awayTeam_name", "awayTeam_slug", "awayTeam_shortName",
                "awayTeam_nameCode", "awayTeam_national", "tournament_uniqueTournament_id", "season_id"
            ]
    
    # Home ve Away takım verilerini hazırlama
    homedata = data[homecols]
    homedata.columns = ["team_id", "team_name", "team_slug", "team_shortName",
                                   "team_nameCode", "team_national", "tournament_id", "season_id"]
    
    awaydata = data[awaycols]
    awaydata.columns = ["team_id", "team_name", "team_slug", "team_shortName",
                                   "team_nameCode", "team_national", "tournament_id", "season_id"]
    
    # Takımları birleştirip benzersiz kayıtları seçme
    teamdata = pd.concat([homedata, awaydata]).drop_duplicates(subset=["team_id", "tournament_id", "season_id"])
   
    for _, row in teamdata.iter

***Soru:*** burata lütfen try excpect ekleyerek bu işlemi geçer misin

**Cevap:** Tabii, `try-except` bloğu ekleyerek UNIQUE kısıtını ihlal eden durumlarda hatayı yakalayabilir ve programın kesintiye uğramadan devam etmesini sağlayabiliriz. İşte `team_data` metodunuzun güncellenmiş hâli:

```python
def team_data(self):
    data = self.fetch_data()
    homecols = [
                "homeTeam_id", "homeTeam_name", "homeTeam_slug", "homeTeam_shortName",
                "homeTeam_nameCode", "homeTeam_national", "tournament_uniqueTournament_id", "season_id"
            ]
    
    awaycols = [
                "awayTeam_id", "awayTeam_name", "awayTeam_slug", "awayTeam_shortName",
                "awayTeam_nameCode", "awayTeam_national", "tournament_uniqueTournament_id", "season_id"
            ]
    
    # Home ve Away takımları için veri hazırlama
    homedata = data[homecols]
    homedata.columns = ["team_id", "team_name", "team_slug", "team_shortName",
                        "team_nameCode", "team_national", "tournament_id", "season_id"]
    
    awaydata = data[awaycols]
    awaydata.columns = ["team_id", "team_name", "team_slug", "team_shortName",
                        "team_nameCode", "team_national", "tournament_id", "season_id"]
    
    # Home ve Away takımları birleştirme ve benzersiz kayıtları seçme
    teamdata = pd.concat([homedata, awaydata]).drop_duplicates(subset=["team_id", "tournament_id", "season_id"])
   
    for _, row in teamdata.iterrows():
        team_id = row['team_id']
        tournament_id = row['tournament_id']
        season_id = row['season_id']
        
        # Geçersiz veya eksik id'leri atla
        if pd.isna(team_id) or pd.isna(tournament_id) or pd.isna(season_id):
            print(f"Geçersiz değer: Team ID={team_id}, Tournament ID={tournament_id}, Season ID={season_id}. Atlanıyor.")
            continue
    
        # İlgili tournament ve season nesnelerini getir
        tournament_instance = Tournament.objects.filter(tournament_id=tournament_id).first()
        season_instance = Season.objects.filter(season_id=season_id).first()
    
        if tournament_instance and season_instance:
            try:
                # UNIQUE constraint hatası durumunda except'e düşer
                team, created = Team.objects.update_or_create(
                    team_id=team_id,
                    tournament=tournament_instance,
                    season=season_instance,
                    defaults={
                        'team_name': row['team_name'],
                        'team_slug': row['team_slug'],
                        'team_shortName': row['team_shortName'],
                        'team_nameCode': row['team_nameCode'],
                        'team_national': row['team_national'],
                    }
                )
                if created:
                    print(f"Team ID {team_id} başarıyla eklendi.")
                else:
                    print(f"Team ID {team_id} güncellenerek kaydedildi.")
            except IntegrityError:
                print(f"UNIQUE constraint ihlali nedeniyle Team ID {team_id} eklenemedi.")
        else:
            print(f"Tournament ID {tournament_id} veya Season ID {season_id} bulunamadı.")
```

### Açıklama
- `try-except` bloğu içinde `update_or_create` işlemi yapılır.
- Eğer `IntegrityError` hatası oluşursa, bu durum `except` bloğu tarafından yakalanır ve kullanıcıya bir bilgilendirme mesajı yazdırılır.
  
Bu yapı ile her UNIQUE constraint ihlalinde hata mesajı alarak kodunuzu kesintisiz çalıştırabilirsiniz.

***Soru:*** # Örnek kullanım:
handler = FixtureDataHandler("2024-10-09")
data = handler.fetch_fixtures_from_api()
handler.save_fixtures_to_db(data)  bu kodlarda çektiğim veriler için şunu yap 2024.01.01 den başla ve for i ile uygun trih formatı için bir fonksiyon oluştur ver veri çekecek fonskiyon

**Cevap:** Belirttiğiniz başlangıç tarihinden itibaren for döngüsü kullanarak her gün için veri çekebilecek bir fonksiyon oluşturabiliriz. `2024-01-01` tarihinden başlayarak istenilen formatta tarih oluşturacak ve her tarih için veri çekmeye çalışacak bir yapı aşağıda verilmiştir:

```python
from datetime import datetime, timedelta

class FixtureDataHandler:
    def __init__(self, start_date):
        self.start_date = datetime.strptime(start_date, "%Y-%m-%d")  # Başlangıç tarihini datetime formatına çevir
        self.date_format = "%Y-%m-%d"  # API'nin kabul ettiği tarih formatı

    def fetch_fixtures_from_api(self, date):
        # Burada API'den veri çekme işlemini yapın
        # Örneğin, bu fonksiyon API'den belirtilen tarihteki maç verilerini çekebilir
        print(f"Veri çekiliyor: {date}")  # Test için tarih çıktısını ver
        # Gerekli işlemler (örneğin, requests modülüyle API çağrısı)
        # Örnek: response = requests.get(f"https://api.example.com/fixtures?date={date}")
        # return response.json()  # Dönen veriyi işleyin

    def save_fixtures_to_db(self, data):
        # Çekilen veriyi veritabanına kaydetme işlemi
        print("Veri veritabanına kaydediliyor...")  # Test çıktısı
        # Örnek: FixtureModel.objects.create(**data)

    def fetch_data_for_date_range(self, end_date):
        end_date = datetime.strptime(end_date, "%Y-%m-%d")
        current_date = self.start_date

        while current_date <= end_date:
            date_str = current_date.strftime(self.date_format)
            data = self.fetch_fixtures_from_api(date_str)  # Her tarih için veri çekme
            self.save_fixtures_to_db(data)  # Çekilen veriyi kaydet
            current_date += timedelta(days=1)  # Sonraki güne geç

# Örnek kullanım
handler = FixtureDataHandler("2024-01-01")
handler.fetch_data_for_date_range("2024-01-10")  # Belirtilen tarih aralığı için veri çeker
```

### Açıklama

1. **`__init__`**: Başlangıç tarihini (`start_date`) alır ve uygun formata çevirir.
2. **`fetch_fixtures_from_api`**: API'den belirli bir tarihte veri çeker (örneğin, tarih `2024-01-01` formatında).
3. **`save_fixtures_to_db`**: Çekilen veriyi veritabanına kaydeder.
4. **`fetch_data_for_date_range`**: Belirtilen tarih aralığında (`end_date`'ye kadar) her gün için veri çekip veritabanına kaydeder. `while` döngüsü ile her gün için `fetch_fixtures_from_api` çağrısı yapılır ve ardından `save_fixtures_to_db` ile veritabanına kaydedilir.

**Cevap:** Bu örnekte, başlangıç tarihi olan `"2024-01-01"` tarihinden itibaren `for` döngüsü ile belirli bir zaman aralığında veri çekecek bir fonksiyon oluşturacağız. İstenen tarih formatına göre her tarihte `fetch_fixtures_from_api` ve `save_fixtures_to_db` işlemlerini çağıracağız.

### Tarihleri İşleyen Fonksiyonun Kodları

İlk olarak, başlangıç tarihi `"2024-01-01"` olacak şekilde bir döngü kuruyoruz. Ardından her tarihte API'den veri çekip kaydediyoruz.

```python
from datetime import datetime, timedelta

class FixtureDataHandler:
    def __init__(self, date_str):
        self.date = datetime.strptime(date_str, "%Y-%m-%d")

    def fetch_fixtures_from_api(self):
        # API'den veri çekme işlemlerini burada yapın
        # Örnek veri
        return [{"match": "Team A vs Team B", "date": self.date.strftime("%Y-%m-%d")}]

    def save_fixtures_to_db(self, data):
        # Çekilen veriyi veritabanına kaydetme işlemleri
        print(f"Veri kaydedildi: {data}")

    def fetch_and_save_for_date_range(self, start_date, end_date):
        current_date = datetime.strptime(start_date, "%Y-%m-%d")
        end_date = datetime.strptime(end_date, "%Y-%m-%d")
        
        while current_date <= end_date:
            self.date = current_date
            data = self.fetch_fixtures_from_api()
            self.save_fixtures_to_db(data)
            current_date += timedelta(days=1)  # Bir gün ileriye git
            print(f"{self.date.strftime('%Y-%m-%d')} tarihi için veri işlendi.")

# Örnek kullanım
handler = FixtureDataHandler("2024-01-01")
handler.fetch_and_save_for_date_range("2024-01-01", "2024-01-10")
```

### Açıklama

- `fetch_and_save_for_date_range` fonksiyonu, belirtilen `start_date` ve `end_date` tarih aralığında her gün için `fetch_fixtures_from_api` ve `save_fixtures_to_db` fonksiyonlarını çağırır.
- `timedelta(days=1)` ile döngü, her iterasyonda bir gün ileri giderek belirtilen aralık boyunca tüm günlerin verisini işler.
- `print` ifadesi, her gün için işlem durumunu belirtir.

Bu yapı, başlangıç tarihinden bitiş tarihine kadar her gün için veri çekip kaydetmenizi sağlar.

***Soru:*** bu şekilde değil istediğim başlangıç ve bitiş tarihlerini ben vereyim ve her seferinde # Örnek kullanım:
handler = FixtureDataHandler("2024-10-09")
data = handler.fetch_fixtures_from_api()
handler.save_fixtures_to_db(data)  burası çalışsın senden istediğim for tarih in tarihler: diyip allta bu fonksyionu çalıştırmak

**Cevap:** Anladım. Bu durumda, başlangıç ve bitiş tarihlerini kullanıcıdan alarak her tarih için `fetch_fixtures_from_api` ve `save_fixtures_to_db` fonksiyonlarını çalıştırmak üzere bir `for` döngüsü kuracağız.

Aşağıdaki kod, belirtilen tarih aralığındaki her gün için `FixtureDataHandler` sınıfını kullanarak veri çeker ve kaydeder.

```python
from datetime import datetime, timedelta

class FixtureDataHandler:
    def __init__(self, date_str):
        self.date = datetime.strptime(date_str, "%Y-%m-%d")

    def fetch_fixtures_from_api(self):
        # API'den veri çekme işlemlerini burada yapın
        return [{"match": "Team A vs Team B", "date": self.date.strftime("%Y-%m-%d")}]

    def save_fixtures_to_db(self, data):
        # Çekilen veriyi veritabanına kaydetme işlemleri
        print(f"Veri kaydedildi: {data}")

# Tarih aralığını alacak fonksiyon
def get_date_range(start_date, end_date):
    start = datetime.strptime(start_date, "%Y-%m-%d")
    end = datetime.strptime(end_date, "%Y-%m-%d")
    delta = timedelta(days=1)
    dates = []
    while start <= end:
        dates.append(start.strftime("%Y-%m-%d"))
        start += delta
    return dates

# Örnek kullanım
start_date = "2024-01-01"
end_date = "2024-01-10"
tarihler = get_date_range(start_date, end_date)

for tarih in tarihler:
    handler = FixtureDataHandler(tarih)
    data = handler.fetch_fixtures_from_api()
    handler.save_fixtures_to_db(data)
```

### Açıklama

1. **Tarih Aralığını Hesaplayan Fonksiyon**: `get_date_range` fonksiyonu, belirtilen başlangıç (`start_date`) ve bitiş (`end_date`) tarihleri arasında bir günlük artışla tüm tarihleri liste olarak döndürür.
   
2. **`for` Döngüsü ile Her Tarih İçin İşlem Yapma**: 
   - `tarihler` listesindeki her bir tarih için `FixtureDataHandler` nesnesi oluşturulup API’den veri çekilir ve kaydedilir.
   - `for` döngüsü, istenen tarih formatını kullanarak her gün için `fetch_fixtures_from_api` ve `save_fixtures_to_db` fonksiyonlarını çalıştırır.

***Soru:*** def match_data(self):
        # Fetch data from the API or existing model
        verim = self.fetch_data()
        if verim is None:
            raise ValueError("Veri işlenmedi. Lütfen önce 'process_data()' metodunu çalıştırın.")
        
     
     
        new_cols = ['id', 'startTimestamp', 'slug', 'tournament_uniqueTournament_id', 'season_id',
                    'roundInfo_round', 'status_type', 'homeTeam_id', 'awayTeam_id',
                    'homeScore_current', 'homeScore_period1', 'homeScore_period2', 'homeScore_normaltime',
                    'awayScore_current', 'awayScore_period1', 'awayScore_period2', 'awayScore_normaltime']
        
        df1 = verim[new_cols] 
        df1['date'] = pd.to_datetime(df1['startTimestamp'], unit='s') + timedelta(hours=3)
        df2 = df1.drop("startTimestamp", axis=1)
        df3 = df2.fillna(0)
        for _, row in df3.iterrows():
            match_id = row['id']
            tournament_id = row['tournament_uniqueTournament_id']
            season_id = row['season_id']
            home_team_id = row['homeTeam_id']
            away_team_id = row['awayTeam_id']
            
            # Geçersiz veya eksik id'leri atla
            if pd.isna(match_id) or pd.isna(tournament_id) or pd.isna(season_id) or pd.isna(home_team_id) or pd.isna(away_team_id):
                print(f"Geçersiz değer: Match ID={match_id}, Tournament ID={tournament_id}, Season ID={season_id}, Home Team ID={home_team_id}, Away Team ID={away_team_id}. Atlanıyor.")
                continue

            # İlgili foreign key nesnelerini getir
            tournament_instance = Tournament.objects.filter(tournament_id=tournament_id).first()
            season_instance = Season.objects.filter(season_id=season_id).first()
            home_team_instance = Team.objects.filter(team_id=home_team_id).first()
            away_team_instance = Team.objects.filter(team_id=away_team_id).first()

            if tournament_instance and season_instance and home_team_instance and away_team_instance:
                # Match'in veritabanında olup olmadığını kontrol et, yoksa oluştur
                if not Match.objects.filter(id=match_id).exists():
                    Match.objects.create(
                        id=match_id,
                        startTimestamp=row['date'],  # DateTimeField olarak datetime verisi
                        slug=row['slug'],
                        tournament=tournament_instance,
                        season=season_instance,
                        homeTeam=home_team_instance,
                        awayTeam=away_team_instance,
                        roundInfo_round=row['roundInfo_round'],
                        homeScore_current=row['homeScore_current'],
                        homeScore_period1=row['homeScore_period1'],
                        homeScore_period2=row['homeScore_period2'],
                        homeScore_normaltime=row['homeScore_normaltime'],
                        awayScore_current=row['awayScore_current'],
                        awayScore_period1=row['awayScore_period1'],
                        awayScore_period2=row['awayScore_period2'],
                        awayScore_normaltime=row['awayScore_normaltime'],
                        status_type = row['status_type']
                    )
                    print(f"Match ID {match_id} başarıyla eklendi.")
                else:
                    print(f"Match ID {match_id} zaten mevcut, eklenmedi.")
            else:
                print(f"Tournament ID {tournament_id}, Season ID {season_id}, Home Team ID {home_team_id}, Away Team ID {away_team_id} bulunamadı.")
  bu modelde de ünique bozulduğunda try except ekelme istiyorujmü

**Cevap:** Tabii, `try-except` bloğu ekleyerek UNIQUE kısıtına takılan durumlarda hatayı yakalayabilir ve işlemin kesintiye uğramasını engelleyebiliriz. Kodunuza `IntegrityError` hatasını yakalamak için `try-except` ekleyelim. Hata oluştuğunda, uygun bir mesaj görüntülenecek ve işlem devam edecek.

### Güncellenmiş `match_data` Fonksiyonu

```python
from django.db.utils import IntegrityError

def match_data(self):
    # Fetch data from the API or existing model
    verim = self.fetch_data()
    if verim is None:
        raise ValueError("Veri işlenmedi. Lütfen önce 'process_data()' metodunu çalıştırın.")

    new_cols = ['id', 'startTimestamp', 'slug', 'tournament_uniqueTournament_id', 'season_id',
                'roundInfo_round', 'status_type', 'homeTeam_id', 'awayTeam_id',
                'homeScore_current', 'homeScore_period1', 'homeScore_period2', 'homeScore_normaltime',
                'awayScore_current', 'awayScore_period1', 'awayScore_period2', 'awayScore_normaltime']
    
    df1 = verim[new_cols] 
    df1['date'] = pd.to_datetime(df1['startTimestamp'], unit='s') + timedelta(hours=3)
    df2 = df1.drop("startTimestamp", axis=1)
    df3 = df2.fillna(0)
    for _, row in df3.iterrows():
        match_id = row['id']
        tournament_id = row['tournament_uniqueTournament_id']
        season_id = row['season_id']
        home_team_id = row['home_team_id']
        away_team_id = row['away_team_id']

        # Geçersiz veya eksik id'leri atla
        if pd.isna(match_id) or pd.isna(tournament_id) or pd.isna(season_id) or pd.isna(home_team_id) or pd.isna(away_team_id):
            print(f"Geçersiz değer: Match ID={match_id}, Tournament ID={tournament_id}, Season ID={season_id}, Home Team ID={home_team_id}, Away Team ID={away_team_id}. Atlanıyor.")
            continue

        # İlgili foreign key nesnelerini getir
        tournament_instance = Tournament.objects.filter(tournament_id=tournament_id).first()
        season_instance = Season.objects.filter(season_id=season_id).first()
        home_team_instance = Team.objects.filter(team_id=home_team_id).first()
        away_team_instance = Team.objects.filter(team_id=away_team_id).first()

        if tournament_instance and season_instance and home_team_instance and away_team_instance:
            try:
                # Match'in veritabanında olup olmadığını kontrol et, yoksa oluştur
                if not Match.objects.filter(id=match_id).exists():
                    Match.objects.create(
                        id=match_id,
                        startTimestamp=row['date'],  # DateTimeField olarak datetime verisi
                        slug=row['slug'],
                        tournament=tournament_instance,
                        season=season_instance,
                        homeTeam=home_team_instance,
                        awayTeam=away_team_instance,
                        roundInfo_round=row['roundInfo_round'],
                        homeScore_current=row['homeScore_current'],
                        homeScore_period1=row['homeScore_period1'],
                        homeScore_period2=row['homeScore_period2'],
                        homeScore_normaltime=row['homeScore_normaltime'],
                        awayScore_current=row['awayScore_current'],
                        awayScore_period1=row['awayScore_period1'],
                        awayScore_period2=row['awayScore_period2'],
                        awayScore_normaltime=row['awayScore_normaltime'],
                        status_type=row['status_type']
                    )
                    print(f"Match ID {match_id} başarıyla eklendi.")
                else:
                    print(f"Match ID {match_id} zaten mevcut, eklenmedi.")
            except IntegrityError:
                print(f"UNIQUE constraint ihlali nedeniyle Match ID {match_id} eklenemedi.")
        else:
            print(f"Tournament ID {tournament_id}, Season ID {season_id}, Home Team ID {home_team_id}, Away Team ID {away_team_id} bulunamadı.")
```

### Açıklama

- **`try-except` bloğu**: `Match.objects.create(...)` işlemi sırasında bir `IntegrityError` oluşursa, hata `except` bloğu tarafından yakalanır ve `Match ID` zaten veritabanında mevcut olduğundan yeni kayıt eklenmez.
- **Hata Mesajı**: `IntegrityError` meydana geldiğinde, konsolda uygun bir hata mesajı görüntülenir, böylece hangi `match_id` değerinin UNIQUE kısıtını ihlal ettiği anlaşılır.

***Soru:*** home_team_id = row['homeTeam_id']  değerini ve aeay için yanlış eklemişsın bunşarı değiltirme lütfen

**Cevap:** Anladım, `home_team_id` ve `away_team_id` değerlerini değiştirmeden olduğu gibi bırakacağım. Aşağıda, bu alanları değiştirmeden `try-except` bloğunu ekleyerek güncellenmiş kodu paylaşıyorum.

### Güncellenmiş `match_data` Fonksiyonu

```python
from django.db.utils import IntegrityError

def match_data(self):
    # Fetch data from the API or existing model
    verim = self.fetch_data()
    if verim is None:
        raise ValueError("Veri işlenmedi. Lütfen önce 'process_data()' metodunu çalıştırın.")

    new_cols = ['id', 'startTimestamp', 'slug', 'tournament_uniqueTournament_id', 'season_id',
                'roundInfo_round', 'status_type', 'homeTeam_id', 'awayTeam_id',
                'homeScore_current', 'homeScore_period1', 'homeScore_period2', 'homeScore_normaltime',
                'awayScore_current', 'awayScore_period1', 'awayScore_period2', 'awayScore_normaltime']
    
    df1 = verim[new_cols] 
    df1['date'] = pd.to_datetime(df1['startTimestamp'], unit='s') + timedelta(hours=3)
    df2 = df1.drop("startTimestamp", axis=1)
    df3 = df2.fillna(0)
    for _, row in df3.iterrows():
        match_id = row['id']
        tournament_id = row['tournament_uniqueTournament_id']
        season_id = row['season_id']
        home_team_id = row['homeTeam_id']  # Orijinal isimler korundu
        away_team_id = row['awayTeam_id']  # Orijinal isimler korundu

        # Geçersiz veya eksik id'leri atla
        if pd.isna(match_id) or pd.isna(tournament_id) or pd.isna(season_id) or pd.isna(home_team_id) or pd.isna(away_team_id):
            print(f"Geçersiz değer: Match ID={match_id}, Tournament ID={tournament_id}, Season ID={season_id}, Home Team ID={home_team_id}, Away Team ID={away_team_id}. Atlanıyor.")
            continue

        # İlgili foreign key nesnelerini getir
        tournament_instance = Tournament.objects.filter(tournament_id=tournament_id).first()
        season_instance = Season.objects.filter(season_id=season_id).first()
        home_team_instance = Team.objects.filter(team_id=home_team_id).first()
        away_team_instance = Team.objects.filter(team_id=away_team_id).first()

        if tournament_instance and season_instance and home_team_instance and away_team_instance:
            try:
                # Match'in veritabanında olup olmadığını kontrol et, yoksa oluştur
                if not Match.objects.filter(id=match_id).exists():
                    Match.objects.create(
                        id=match_id,
                        startTimestamp=row['date'],  # DateTimeField olarak datetime verisi
                        slug=row['slug'],
                        tournament=tournament_instance,
                        season=season_instance,
                        homeTeam=home_team_instance,
                        awayTeam=away_team_instance,
                        roundInfo_round=row['roundInfo_round'],
                        homeScore_current=row['homeScore_current'],
                        homeScore_period1=row['homeScore_period1'],
                        homeScore_period2=row['homeScore_period2'],
                        homeScore_normaltime=row['homeScore_normaltime'],
                        awayScore_current=row['awayScore_current'],
                        awayScore_period1=row['awayScore_period1'],
                        awayScore_period2=row['awayScore_period2'],
                        awayScore_normaltime=row['awayScore_normaltime'],
                        status_type=row['status_type']
                    )
                    print(f"Match ID {match_id} başarıyla eklendi.")
                else:
                    print(f"Match ID {match_id} zaten mevcut, eklenmedi.")
            except IntegrityError:
                print(f"UNIQUE constraint ihlali nedeniyle Match ID {match_id} eklenemedi.")
        else:
            print(f"Tournament ID {tournament_id}, Season ID {season_id}, Home Team ID {home_team_id}, Away Team ID {away_team_id} bulunamadı.")
```

### Açıklama

- `home_team_id` ve `away_team_id` değerlerini olduğu gibi koruduk.
- `try-except` bloğu `IntegrityError` hatalarını yakalayarak UNIQUE kısıtı ihlallerini işleyecek şekilde eklendi.
- Hata durumunda ilgili `match_id` için bir bilgilendirme mesajı gösterilir, böylece kod kesintisiz çalışır.

***Soru:*** ValueError: Excel does not support datetimes with timezones. Please ensure that datetimes are timezone unaware before writing to Excel.  id	startTimestamp	slug	tournament_id	season_id	roundInfo_round	status_type	homeTeam_id	awayTeam_id	homeScore_current	homeScore_period1	homeScore_period2	homeScore_normaltime	awayScore_current	awayScore_period1	awayScore_period2	awayScore_normaltime
0	11173503	2024-09-10 17:00:00+00:00	kosovo-u21-israel-u21

**Cevap:** Bu hata, `Excel`'in zaman dilimi bilgisine sahip datetime nesnelerini (`timezone-aware datetimes`) desteklememesi nedeniyle ortaya çıkıyor. Bu sorunu çözmek için zaman dilimi bilgilerini datetime nesnelerinden kaldırmamız gerekiyor. Python’da bunu `tz_localize(None)` veya `tz_convert(None)` yöntemlerini kullanarak yapabiliriz.

Aşağıda, `startTimestamp` alanını zaman diliminden arındırmak için kodunuzu güncelledim. Bu işlemi `Excel`’e yazma işlemi öncesinde veya veriyi düzenleme sırasında yapabilirsiniz.

### Güncellenmiş Kod

```python
def match_data(self):
    # Fetch data from the API or existing model
    verim = self.fetch_data()
    if verim is None:
        raise ValueError("Veri işlenmedi. Lütfen önce 'process_data()' metodunu çalıştırın.")

    new_cols = ['id', 'startTimestamp', 'slug', 'tournament_uniqueTournament_id', 'season_id',
                'roundInfo_round', 'status_type', 'homeTeam_id', 'awayTeam_id',
                'homeScore_current', 'homeScore_period1', 'homeScore_period2', 'homeScore_normaltime',
                'awayScore_current', 'awayScore_period1', 'awayScore_period2', 'awayScore_normaltime']
    
    df1 = verim[new_cols] 
    df1['startTimestamp'] = pd.to_datetime(df1['startTimestamp'], unit='s') + timedelta(hours=3)
    
    # Zaman dilimi bilgisini kaldır
    df1['startTimestamp'] = df1['startTimestamp'].dt.tz_localize(None)
    
    df2 = df1.fillna(0)
    
    # Veriyi Excel’e yazma işlemi
    try:
        df2.to_excel("match_data.xlsx", index=False)
        print("Veri başarıyla Excel'e kaydedildi.")
    except ValueError as e:
        print(f"Excel'e yazarken hata oluştu: {e}")
```

### Açıklama

- **Zaman Dilimi Bilgisini Kaldırma**: `df1['startTimestamp'].dt.tz_localize(None)` ifadesi, `startTimestamp` sütunundaki tüm datetime nesnelerinden zaman dilimi bilgisini kaldırır.
- **Excel'e Yazma**: Zaman diliminden arındırılan veriyi artık `to_excel` yöntemiyle `Excel`’e yazabiliriz. Bu işlem herhangi bir `ValueError` oluşturmadan çalışmalıdır.

Bu düzenleme, veriyi `Excel`'e yazarken `timezone` hatasını önleyecektir.

***Soru:*** def match_data(self):
        # Fetch data from the API or existing model
        verim = self.fetch_data()
        if verim is None:
            raise ValueError("Veri işlenmedi. Lütfen önce 'process_data()' metodunu çalıştırın.")
        
     
     
        new_cols = ['id', 'startTimestamp', 'slug', 'tournament_uniqueTournament_id', 'season_id',
                    'roundInfo_round', 'status_type', 'homeTeam_id', 'awayTeam_id',
                    'homeScore_current', 'homeScore_period1', 'homeScore_period2', 'homeScore_normaltime',
                    'awayScore_current', 'awayScore_period1', 'awayScore_period2', 'awayScore_normaltime']
        
        df1 = verim[new_cols] 
        df1['date'] = pd.to_datetime(df1['startTimestamp'], unit='s') + timedelta(hours=3)
        df2 = df1.drop("startTimestamp", axis=1)
        df3 = df2.fillna(0)
        for _, row in df3.iterrows():
            match_id = row['id']
            tournament_id = row['tournament_uniqueTournament_id']
            season_id = row['season_id']
            home_team_id = row['homeTeam_id']
            away_team_id = row['awayTeam_id']
            
            # Geçersiz veya eksik id'leri atla
            if pd.isna(match_id) or pd.isna(tournament_id) or pd.isna(season_id) or pd.isna(home_team_id) or pd.isna(away_team_id):
                print(f"Geçersiz değer: Match ID={match_id}, Tournament ID={tournament_id}, Season ID={season_id}, Home Team ID={home_team_id}, Away Team ID={away_team_id}. Atlanıyor.")
                continue

            # İlgili foreign key nesnelerini getir
            tournament_instance = Tournament.objects.filter(tournament_id=tournament_id).first()
            season_instance = Season.objects.filter(season_id=season_id).first()
            home_team_instance = Team.objects.filter(team_id=home_team_id).first()
            away_team_instance = Team.objects.filter(team_id=away_team_id).first()

            if tournament_instance and season_instance and home_team_instance and away_team_instance:
                try:
                    # Match'in veritabanında olup olmadığını kontrol et, yoksa oluştur
                    if not Match.objects.filter(id=match_id).exists():
                        Match.objects.create(
                            id=match_id,
                            startTimestamp=row['date'],  # DateTimeField olarak datetime verisi
                            slug=row['slug'],
                            tournament=tournament_instance,
                            season=season_instance,
                            homeTeam=home_team_instance,
                            awayTeam=away_team_instance,
                            roundInfo_round=row['roundInfo_round'],
                            homeScore_current=row['homeScore_current'],
                            homeScore_period1=row['homeScore_period1'],
                            homeScore_period2=row['homeScore_period2'],
                            homeScore_normaltime=row['homeScore_normaltime'],
                            awayScore_current=row['awayScore_current'],
                            awayScore_period1=row['awayScore_period1'],
                            awayScore_period2=row['awayScore_period2'],
                            awayScore_normaltime=row['awayScore_normaltime'],
                            status_type=row['status_type']
                        )
                        print(f"Match ID {match_id} başarıyla eklendi.")
                    else:
                        print(f"Match ID {match_id} zaten mevcut, eklenmedi.")
                except IntegrityError:
                    print(f"UNIQUE constraint ihlali nedeniyle Match ID {match_id} eklenemedi.")
            else:
                print(f"Tournament ID {tournament_id}, Season ID {season_id}, Home Team ID {home_team_id}, Away Team ID {away_team_id} bulunamadı.")



# SofascoreAPI sınıfını kullanarak team_data'yı veritabanına kaydetmek için:
api = SofascoreAPI()
teamdata = api.fetch_data()  # Veriyi getirin (API'den ya da dosyadan)
api.tournament_data()
api.season_data()
api.team_data()
api.match_data()

***Soru:*** def match_data(self):
        # Fetch data from the API or existing model
        verim = self.fetch_data()
        if verim is None:
            raise ValueError("Veri işlenmedi. Lütfen önce 'process_data()' metodunu çalıştırın.")
        
     
     
        new_cols = ['id', 'startTimestamp', 'slug', 'tournament_uniqueTournament_id', 'season_id',
                    'roundInfo_round', 'status_type', 'homeTeam_id', 'awayTeam_id',
                    'homeScore_current', 'homeScore_period1', 'homeScore_period2', 'homeScore_normaltime',
                    'awayScore_current', 'awayScore_period1', 'awayScore_period2', 'awayScore_normaltime']
        
        df1 = verim[new_cols] 
        df1['date'] = pd.to_datetime(df1['startTimestamp'], unit='s') + timedelta(hours=3)
        df2 = df1.drop("startTimestamp", axis=1)
        df3 = df2.fillna(0)
        for _, row in df3.iterrows():
            match_id = row['id']
            tournament_id = row['tournament_uniqueTournament_id']
            season_id = row['season_id']
            home_team_id = row['homeTeam_id']
            away_team_id = row['awayTeam_id']
            
            # Geçersiz veya eksik id'leri atla
            if pd.isna(match_id) or pd.isna(tournament_id) or pd.isna(season_id) or pd.isna(home_team_id) or pd.isna(away_team_id):
                print(f"Geçersiz değer: Match ID={match_id}, Tournament ID={tournament_id}, Season ID={season_id}, Home Team ID={home_team_id}, Away Team ID={away_team_id}. Atlanıyor.")
                continue

            # İlgili foreign key nesnelerini getir
            tournament_instance = Tournament.objects.filter(tournament_id=tournament_id).first()
            season_instance = Season.objects.filter(season_id=season_id).first()
            home_team_instance = Team.objects.filter(team_id=home_team_id).first()
            away_team_instance = Team.objects.filter(team_id=away_team_id).first()

            if tournament_instance and season_instance and home_team_instance and away_team_instance:
                try:
                    # Match'in veritabanında olup olmadığını kontrol et, yoksa oluştur
                    if not Match.objects.filter(id=match_id).exists():
                        Match.objects.create(
                            id=match_id,
                            startTimestamp=row['date'],  # DateTimeField olarak datetime verisi
                            slug=row['slug'],
                            tournament=tournament_instance,
                            season=season_instance,
                            homeTeam=home_team_instance,
                            awayTeam=away_team_instance,
                            roundInfo_round=row['roundInfo_round'],
                            homeScore_current=row['homeScore_current'],
                            homeScore_period1=row['homeScore_period1'],
                            homeScore_period2=row['homeScore_period2'],
                            homeScore_normaltime=row['homeScore_normaltime'],
                            awayScore_current=row['awayScore_current'],
                            awayScore_period1=row['awayScore_period1'],
                            awayScore_period2=row['awayScore_period2'],
                            awayScore_normaltime=row['awayScore_normaltime'],
                            status_type=row['status_type']
                        )
                        print(f"Match ID {match_id} başarıyla eklendi.")
                    else:
                        print(f"Match ID {match_id} zaten mevcut, eklenmedi.")
                except IntegrityError:
                    print(f"UNIQUE constraint ihlali nedeniyle Match ID {match_id} eklenemedi.")
            else:
                print(f"Tournament ID {tournament_id}, Season ID {season_id}, Home Team ID {home_team_id}, Away Team ID {away_team_id} bulunamadı.")



# SofascoreAPI sınıfını kullanarak team_data'yı veritabanına kaydetmek için:
api = SofascoreAPI()
teamdata = api.fetch_data()  # Veriyi getirin (API'den ya da dosyadan)
api.tournament_data()
api.season_data()
api.team_data()
api.match_data()
print("İşlemler bitti")   bu kodlarada  şöylşe olması lazım unique hatası vermeyecek aynı kriterlerde bir maç varsa silsib hiçbir zaman unique hatası olmayacak

**Cevap:** Bu durumda, `match_data` metodunda `Match` kaydı oluşturulmadan önce aynı `match_id` ile kayıtlı bir maç varsa onu silerek UNIQUE hatası riskini ortadan kaldırabiliriz. Kodda, aynı `match_id`'ye sahip kayıtları bulup silen bir işlem ekleyeceğiz.

### Güncellenmiş `match_data` Metodu

```python
from django.db.utils import IntegrityError

def match_data(self):
    # Fetch data from the API or existing model
    verim = self.fetch_data()
    if verim is None:
        raise ValueError("Veri işlenmedi. Lütfen önce 'process_data()' metodunu çalıştırın.")

    new_cols = ['id', 'startTimestamp', 'slug', 'tournament_uniqueTournament_id', 'season_id',
                'roundInfo_round', 'status_type', 'homeTeam_id', 'awayTeam_id',
                'homeScore_current', 'homeScore_period1', 'homeScore_period2', 'homeScore_normaltime',
                'awayScore_current', 'awayScore_period1', 'awayScore_period2', 'awayScore_normaltime']
    
    df1 = verim[new_cols] 
    df1['date'] = pd.to_datetime(df1['startTimestamp'], unit='s') + timedelta(hours=3)
    df2 = df1.drop("startTimestamp", axis=1)
    df3 = df2.fillna(0)
    
    for _, row in df3.iterrows():
        match_id = row['id']
        tournament_id = row['tournament_uniqueTournament_id']
        season_id = row['season_id']
        home_team_id = row['homeTeam_id']
        away_team_id = row['awayTeam_id']
        
        # Geçersiz veya eksik id'leri atla
        if pd.isna(match_id) or pd.isna(tournament_id) or pd.isna(season_id) or pd.isna(home_team_id) or pd.isna(away_team_id):
            print(f"Geçersiz değer: Match ID={match_id}, Tournament ID={tournament_id}, Season ID={season_id}, Home Team ID={home_team_id}, Away Team ID={away_team_id}. Atlanıyor.")
            continue

        # İlgili foreign key nesnelerini getir
        tournament_instance = Tournament.objects.filter(tournament_id=tournament_id).first()
        season_instance = Season.objects.filter(season_id=season_id).first()
        home_team_instance = Team.objects.filter(team_id=home_team_id).first()
        away_team_instance = Team.objects.filter(team_id=away_team_id).first()

        if tournament_instance and season_instance and home_team_instance and away_team_instance:
            try:
                # Aynı match_id ile daha önce eklenmiş maç varsa sil
                Match.objects.filter(id=match_id).delete()

                # Yeni maçı oluştur
                Match.objects.create(
                    id=match_id,
                    startTimestamp=row['date'],  # DateTimeField olarak datetime verisi
                    slug=row['slug'],
                    tournament=tournament_instance,
                    season=season_instance,
                    homeTeam=home_team_instance,
                    awayTeam=away_team_instance,
                    roundInfo_round=row['roundInfo_round'],
                    homeScore_current=row['homeScore_current'],
                    homeScore_period1=row['homeScore_period1'],
                    homeScore_period2=row['homeScore_period2'],
                    homeScore_normaltime=row['homeScore_normaltime'],
                    awayScore_current=row['awayScore_current'],
                    awayScore_period1=row['awayScore_period1'],
                    awayScore_period2=row['awayScore_period2'],
                    awayScore_normaltime=row['awayScore_normaltime'],
                    status_type=row['status_type']
                )
                print(f"Match ID {match_id} başarıyla eklendi.")
            except IntegrityError:
                print(f"UNIQUE constraint ihlali nedeniyle Match ID {match_id} eklenemedi.")
        else:
            print(f"Tournament ID {tournament_id}, Season ID {season_id}, Home Team ID={home_team_id}, Away Team ID={away_team_id} bulunamadı.")
```

### Açıklama

- **Kayıt Silme İşlemi**: `Match.objects.filter(id=match_id).delete()` ifadesi, aynı `match_id` değerine sahip daha önce eklenmiş olan herhangi bir kaydı siler. Böylece UNIQUE hatası oluşmadan yeni kaydı ekleyebiliriz.
- **Yeni Kayıt Oluşturma**: Eski kayıt silindikten sonra `Match.objects.create(...)` ifadesi ile yeni kayıt oluşturulur. Bu şekilde UNIQUE constraint ihlali oluşmaz.

Bu yöntem, veritabanında aynı `match_id` ile kaydedilmiş maçların tekrar eklenmesini engelleyerek hatasız bir işlem sağlar.