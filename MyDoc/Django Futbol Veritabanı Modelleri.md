***Soru:*** şimdi ben bir futbol maçları için bir django site oluşturmak istiyorum bunun içinde önce bir ilişkisel veritabanı olulturmak istiyorum sana göndereeğim örnek verileri biten maçlarla ilgili tüm verileri bu verilerden şöyle bir modeller oluşturmak istiyorum öncelikle ülke modeli daha sonra ülkeye bağlı turnuva modeli daha sonra turnuvaya bağlı sezon daha sonra buradaki ev ve takım bilgilerini ekleyeceğim bir tane team modeli oluşturmak istiyorum bu modelleri bana django ORM ye göre oluştur ve hangisinin hangisine bağlı olduğunu belirt

**Cevap:** İstediğin futbol veritabanı yapısını oluşturabilmek için Django ORM yapısına uygun bir şekilde modelleri düzenleyelim. Bu yapıda önce en büyük model olan `Country` (Ülke), ardından `Tournament` (Turnuva), `Season` (Sezon), `Team` (Takım), ve bunlara bağlı diğer ilişkileri tanımlayacağız.

Verdiğin bilgilere göre, model yapısı şu şekilde olabilir:

### 1. Ülke Modeli (Country)
Her turnuva bir ülkeye bağlı olacak. İlk modelimiz ülke olacak.

```python
from django.db import models

class Country(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name
```

### 2. Turnuva Modeli (Tournament)
Her turnuva bir ülkeye bağlı olmalı, bu yüzden `Country` ile `ForeignKey` ilişkisi kuracağız.

```python
class Tournament(models.Model):
    name = models.CharField(max_length=100)
    country = models.ForeignKey(Country, on_delete=models.CASCADE, related_name='tournaments')

    def __str__(self):
        return f"{self.name} - {self.country.name}"
```

### 3. Sezon Modeli (Season)
Her turnuva farklı sezonlara sahip olabilir. Bu yüzden `Season` modelini `Tournament` ile ilişkilendireceğiz.

```python
class Season(models.Model):
    name = models.CharField(max_length=50)  # Örn: 2023/2024
    tournament = models.ForeignKey(Tournament, on_delete=models.CASCADE, related_name='seasons')

    def __str__(self):
        return f"{self.name} - {self.tournament.name}"
```

### 4. Takım Modeli (Team)
Her takım bir sezonda oynar. Ancak bir takım farklı sezonlarda da olabilir. Takımları burada tanımlayıp daha sonra maç modelinde iki takım olarak kullanacağız.

```python
class Team(models.Model):
    name = models.CharField(max_length=100)
    country = models.ForeignKey(Country, on_delete=models.CASCADE, related_name='teams')

    def __str__(self):
        return self.name
```

### 5. Maç Modeli (Match)
Bir maç, ev sahibi ve deplasman takımları, sezon ve diğer detayları içerecek. Takımların `Team` modeline bağlı olduğunu göz önünde bulundurarak, bir maçta iki takımın (ev sahibi ve deplasman) yer alacağını belirtiyoruz.

```python
class Match(models.Model):
    home_team = models.ForeignKey(Team, on_delete=models.CASCADE, related_name='home_matches')
    away_team = models.ForeignKey(Team, on_delete=models.CASCADE, related_name='away_matches')
    season = models.ForeignKey(Season, on_delete=models.CASCADE, related_name='matches')
    date = models.DateField()
    home_score = models.IntegerField()
    away_score = models.IntegerField()

    def __str__(self):
        return f"{self.home_team.name} vs {self.away_team.name} - {self.season.name}"
```

### Model İlişkileri
- `Country`: Her ülkenin birden fazla turnuvası olabilir (`1:N` ilişkisi).
- `Tournament`: Her turnuva bir ülkeye bağlıdır ve bir turnuvanın birçok sezonu olabilir (`1:N` ilişkisi).
- `Season`: Her sezon bir turnuvaya bağlıdır ve o sezon içinde birçok maç oynanabilir (`1:N` ilişkisi).
- `Team`: Her takım bir ülkeye bağlı olabilir, ancak bir maçta hem ev sahibi hem deplasman takımı olarak iki takım yer alacak (`1:N` ilişkisi).
- `Match`: Her maçta iki takım (ev ve deplasman) yer alır, bir sezona aittir ve belirli bir tarihte oynanır.

Bu yapıyla temel bir futbol veritabanı kurmuş olduk. Eğer ekleyeceğin başka veri tipleri ya da ek bilgiler varsa, onları da bu yapıya ekleyebiliriz.

**Cevap:** Gönderdiğin verileri görselle inceledim. Veriler içerisinde birçok önemli alan var ve bunları modellerimizle ilişkilendireceğiz. Daha önce oluşturduğumuz modelleri geliştireceğiz, böylece daha somut bir yapıya sahip olacaksın.

Aşağıda her modelde yer alması gereken yeni alanları ekleyerek, id'ler ve diğer verileri de göz önünde bulundurduk.

### 1. Ülke Modeli (Country)

```python
class Country(models.Model):
    alpha2 = models.CharField(max_length=2)  # Örn: "HR"
    alpha3 = models.CharField(max_length=3)  # Örn: "HRV"
    name = models.CharField(max_length=100)  # Örn: "Croatia"
    slug = models.SlugField(max_length=100)  # URL'de kullanılacak, örn: "croatia"

    def __str__(self):
        return self.name
```

### 2. Turnuva Modeli (Tournament)

```python
class Tournament(models.Model):
    name = models.CharField(max_length=100)  # Örn: "UEFA Nations League"
    slug = models.SlugField(max_length=100)  # URL'de kullanılacak, örn: "uefa-nations-league"
    unique_tournament_name = models.CharField(max_length=100)  # Örn: "UEFA Nations League"
    country = models.ForeignKey(Country, on_delete=models.CASCADE, related_name='tournaments')
    category_name = models.CharField(max_length=100)  # Örn: "Europe"
    category_slug = models.SlugField(max_length=100)  # URL'de kullanılacak, örn: "europe"
    sport_name = models.CharField(max_length=50)  # Örn: "Football"
    sport_slug = models.SlugField(max_length=50)  # URL'de kullanılacak, örn: "football"

    def __str__(self):
        return f"{self.name} - {self.country.name}"
```

### 3. Sezon Modeli (Season)

```python
class Season(models.Model):
    name = models.CharField(max_length=50)  # Örn: "2024/2025"
    year = models.IntegerField()  # Sezon yılı, Örn: 2024
    tournament = models.ForeignKey(Tournament, on_delete=models.CASCADE, related_name='seasons')

    def __str__(self):
        return f"{self.name} - {self.tournament.name}"
```

### 4. Takım Modeli (Team)

```python
class Team(models.Model):
    name = models.CharField(max_length=100)  # Örn: "Croatia"
    slug = models.SlugField(max_length=100)  # URL'de kullanılacak, örn: "croatia"
    short_name = models.CharField(max_length=50)  # Kısa adı, Örn: "CRO"
    country = models.ForeignKey(Country, on_delete=models.CASCADE, related_name='teams')
    primary_color = models.CharField(max_length=7)  # Örn: "#374df5"
    secondary_color = models.CharField(max_length=7)  # Örn: "#ffffff"
    sport_name = models.CharField(max_length=50)  # Örn: "Football"
    disabled = models.BooleanField(default=False)  # Takım aktif mi
    national = models.BooleanField(default=True)  # Milli takım mı?

    def __str__(self):
        return self.name
```

### 5. Maç Modeli (Match)

```python
class Match(models.Model):
    home_team = models.ForeignKey(Team, on_delete=models.CASCADE, related_name='home_matches')
    away_team = models.ForeignKey(Team, on_delete=models.CASCADE, related_name='away_matches')
    season = models.ForeignKey(Season, on_delete=models.CASCADE, related_name='matches')
    date = models.DateField()
    home_score = models.IntegerField()
    away_score = models.IntegerField()
    status_code = models.CharField(max_length=50)  # Örn: "100"
    status_description = models.CharField(max_length=100)  # Örn: "Finished"
    final_result_only = models.BooleanField(default=False)  # Sadece final sonuçları mı?
    injury_time1 = models.IntegerField(null=True, blank=True)  # 1. yarı sakatlık süresi
    injury_time2 = models.IntegerField(null=True, blank=True)  # 2. yarı sakatlık süresi

    def __str__(self):
        return f"{self.home_team.name} vs {self.away_team.name} - {self.season.name}"
```

### Model İlişkileri ve Verilerin Kullanımı
- **Country**: Takımların ve turnuvaların bağlı olduğu ülkeleri temsil ediyor.
- **Tournament**: Turnuvalar hem ülke hem de spor kategorisine göre organize ediliyor.
- **Season**: Her turnuvanın farklı sezonları var ve bu sezonlar `Match` modeliyle ilişkilendirilecek.
- **Team**: Her takım, ülkeye bağlı olarak tanımlanacak. Ek renk bilgileri ve kısa adlar eklendi.
- **Match**: Maçlar iki takımı, sezonu ve skoru içeriyor. Ayrıca maçın durumu ve uzatma süreleri gibi detaylar da eklenmiş durumda.

Bu modellerle, sana gönderdiğin verilerin temelini oluşturan bir futbol veritabanı yapısı sunuyoruz. Herhangi bir ekleme veya düzeltme yapmamı istersen, haber verebilirsin!

***Soru:*** tamam bu modellere id lerle ilgili bağlantılar kur ve sana gönderdiğim sutun bilgileri kullan ki buna göre işlemleri yapayım daha fazla bilgi olmasını istiyorum her modele id eklemeni istiyorum

**Cevap:** Tamam, her modelde ID’lerle ilgili bağlantıları ve diğer sütun bilgilerini kullanarak detaylı bir yapı oluşturacağız. Django’da otomatik olarak her modelde `id` alanı zaten mevcut, ancak senin istediğin özel ID’ler ve diğer sütun bilgilerine göre her modeli güncelleyeceğiz.

İlk olarak ID’leri manuel olarak ekleyelim ve modellerde sütunlara uygun yeni alanları da tanımlayalım. Gönderdiğin verilerdeki alanları en uygun modellere ekleyeceğim. Ayrıca, veritabanı ilişkilerini ID’lerle kurarak daha net bir yapıya ulaşacağız.

### 1. Ülke Modeli (Country)

```python
class Country(models.Model):
    id = models.CharField(max_length=10, primary_key=True)  # Özel ID alanı
    alpha2 = models.CharField(max_length=2)  # Örn: "HR"
    alpha3 = models.CharField(max_length=3)  # Örn: "HRV"
    name = models.CharField(max_length=100)  # Örn: "Croatia"
    slug = models.SlugField(max_length=100)  # URL'de kullanılacak, örn: "croatia"
    
    def __str__(self):
        return self.name
```

Burada manuel `id` alanını tanımladık ve ülke kodlarını `alpha2` ve `alpha3` olarak kaydettik. 

### 2. Turnuva Modeli (Tournament)

```python
class Tournament(models.Model):
    id = models.IntegerField(primary_key=True)  # Özel turnuva ID'si
    name = models.CharField(max_length=100)  # Örn: "UEFA Nations League"
    slug = models.SlugField(max_length=100)  # URL'de kullanılacak, örn: "uefa-nations-league"
    unique_tournament_name = models.CharField(max_length=100)  # Örn: "UEFA Nations League"
    country = models.ForeignKey(Country, on_delete=models.CASCADE, related_name='tournaments')
    category_name = models.CharField(max_length=100)  # Örn: "Europe"
    category_slug = models.SlugField(max_length=100)  # URL'de kullanılacak, örn: "europe"
    sport_name = models.CharField(max_length=50)  # Örn: "Football"
    sport_slug = models.SlugField(max_length=50)  # URL'de kullanılacak, örn: "football"
    has_event_player_statistics = models.BooleanField(default=False)  # Oyuncu istatistikleri var mı?

    def __str__(self):
        return f"{self.name} - {self.country.name}"
```

Bu turnuva modeli, her turnuvaya özel bir `id` alanı içeriyor. Ayrıca oyuncu istatistikleri ve spor bilgileri gibi alanları da ekledik.

### 3. Sezon Modeli (Season)

```python
class Season(models.Model):
    id = models.IntegerField(primary_key=True)  # Sezon ID'si
    name = models.CharField(max_length=50)  # Örn: "2024/2025"
    year = models.IntegerField()  # Sezon yılı, Örn: 2024
    tournament = models.ForeignKey(Tournament, on_delete=models.CASCADE, related_name='seasons')

    def __str__(self):
        return f"{self.name} - {self.tournament.name}"
```

Sezon modeli, her sezon için özel bir `id` alanı ve turnuvaya olan ilişkisini içeriyor.

### 4. Takım Modeli (Team)

```python
class Team(models.Model):
    id = models.IntegerField(primary_key=True)  # Takım ID'si
    name = models.CharField(max_length=100)  # Örn: "Croatia"
    slug = models.SlugField(max_length=100)  # URL'de kullanılacak, örn: "croatia"
    short_name = models.CharField(max_length=50)  # Kısa adı, Örn: "CRO"
    country = models.ForeignKey(Country, on_delete=models.CASCADE, related_name='teams')
    primary_color = models.CharField(max_length=7)  # Örn: "#374df5"
    secondary_color = models.CharField(max_length=7)  # Örn: "#ffffff"
    sport_name = models.CharField(max_length=50)  # Örn: "Football"
    disabled = models.BooleanField(default=False)  # Takım aktif mi?
    national = models.BooleanField(default=True)  # Milli takım mı?

    def __str__(self):
        return self.name
```

Takım modeline `id` alanını ekledik ve renk bilgileri gibi ek bilgileri modele dâhil ettik.

### 5. Maç Modeli (Match)

```python
class Match(models.Model):
    id = models.IntegerField(primary_key=True)  # Maç ID'si
    home_team = models.ForeignKey(Team, on_delete=models.CASCADE, related_name='home_matches')
    away_team = models.ForeignKey(Team, on_delete=models.CASCADE, related_name='away_matches')
    season = models.ForeignKey(Season, on_delete=models.CASCADE, related_name='matches')
    date = models.DateField()
    home_score = models.IntegerField()
    away_score = models.IntegerField()
    status_code = models.CharField(max_length=50)  # Örn: "100"
    status_description = models.CharField(max_length=100)  # Örn: "Finished"
    final_result_only = models.BooleanField(default=False)  # Sadece final sonuçları mı?
    injury_time1 = models.IntegerField(null=True, blank=True)  # 1. yarı sakatlık süresi
    injury_time2 = models.IntegerField(null=True, blank=True)  # 2. yarı sakatlık süresi

    def __str__(self):
        return f"{self.home_team.name} vs {self.away_team.name} - {self.season.name}"
```

Maç modeli, hem takımların ilişkilerini hem de maç durumu gibi önemli bilgileri içeriyor. `id` alanı ekleyerek her maç için benzersiz bir tanımlayıcı sağladık.

### Model İlişkileri ve Ek Bilgiler
- **Country** modeline manuel bir `id` alanı ekledik.
- **Tournament** modelinde hem turnuva ID’si hem de oyuncu istatistikleri gibi ek alanlar eklendi.
- **Season** ve **Team** modellerine de özel `id` alanları ekledik ve ülke, turnuva gibi ilişkiler kuruldu.
- **Match** modelinde maçlara dair ekstra detaylar eklenerek ID bağlantıları oluşturuldu.

Bu şekilde her modele ek sütunlar ve ID'lerle birlikte tam olarak istediğin ilişkisel veritabanı yapısını oluşturdum. Şimdi bu modelleri kullanarak veritabanında gerekli işlemleri gerçekleştirebilirsin. Eğer başka bir geliştirme istersen, belirtmen yeterli!

***Soru:*** peki modellerimi sutunlarımala eşletir hangi model sutunu hangi verimle eşleşiyor bana bunları ekle

**Cevap:** Aşağıda, gönderdiğin veri yapısındaki sütunların hangi modele ve alanlara karşılık geldiğini gösteren bir eşleştirme yapıyorum. Bu şekilde her bir sütunun hangi model ve alanla eşleştiğini görebileceksin.

### Veriden Modeller ve Alanlar

#### **Country Modeli Eşleşmeleri:**
Verilerde ülkeye dair bilgiler:

| Veri Sütunu                     | Model          | Alan                     |
|----------------------------------|----------------|--------------------------|
| tournament.category.country.alpha2          | Country        | alpha2                   |
| tournament.category.country.alpha3          | Country        | alpha3                   |
| tournament.category.country.name            | Country        | name                     |
| tournament.category.country.slug            | Country        | slug                     |

#### **Tournament Modeli Eşleşmeleri:**
Verilerde turnuva ile ilgili bilgiler:

| Veri Sütunu                                      | Model          | Alan                           |
|--------------------------------------------------|----------------|--------------------------------|
| tournament.id                                    | Tournament      | id                             |
| tournament.name                                  | Tournament      | name                           |
| tournament.slug                                  | Tournament      | slug                           |
| tournament.category.name                         | Tournament      | category_name                  |
| tournament.category.slug                         | Tournament      | category_slug                  |
| tournament.category.sport.name                   | Tournament      | sport_name                     |
| tournament.category.sport.slug                   | Tournament      | sport_slug                     |
| tournament.uniqueTournament.name                 | Tournament      | unique_tournament_name          |
| tournament.uniqueTournament.slug                 | Tournament      | slug (aynı)                    |
| tournament.uniqueTournament.hasEventPlayerStatistics | Tournament  | has_event_player_statistics    |

#### **Season Modeli Eşleşmeleri:**
Sezon ile ilgili veriler:

| Veri Sütunu                  | Model   | Alan         |
|------------------------------|---------|--------------|
| season.id                    | Season  | id           |
| season.name                  | Season  | name         |
| season.year                  | Season  | year         |
| season.editor                | Season  | year (editor'dan ek bilgi yok) |

#### **Team Modeli Eşleşmeleri:**
Takım ile ilgili sütunlar:

| Veri Sütunu                                | Model   | Alan             |
|--------------------------------------------|---------|------------------|
| homeTeam.id / awayTeam.id                  | Team    | id               |
| homeTeam.name / awayTeam.name              | Team    | name             |
| homeTeam.slug / awayTeam.slug              | Team    | slug             |
| homeTeam.shortName / awayTeam.shortName    | Team    | short_name       |
| homeTeam.country.alpha2 / awayTeam.country.alpha2 | Team    | country.alpha2   |
| homeTeam.country.alpha3 / awayTeam.country.alpha3 | Team    | country.alpha3   |
| homeTeam.country.name / awayTeam.country.name | Team  | country.name     |
| homeTeam.teamColors.primary / awayTeam.teamColors.primary | Team | primary_color |
| homeTeam.teamColors.secondary / awayTeam.teamColors.secondary | Team | secondary_color |
| homeTeam.disabled / awayTeam.disabled      | Team    | disabled         |
| homeTeam.national / awayTeam.national      | Team    | national         |

#### **Match Modeli Eşleşmeleri:**
Maç bilgileri için veriler:

| Veri Sütunu                                | Model   | Alan               |
|--------------------------------------------|---------|--------------------|
| id                                         | Match   | id                 |
| startTimestamp                             | Match   | date               |
| homeTeam.id                                | Match   | home_team.id       |
| awayTeam.id                                | Match   | away_team.id       |
| homeScore.current                          | Match   | home_score         |
| awayScore.current                          | Match   | away_score         |
| status.code                                | Match   | status_code        |
| status.description                         | Match   | status_description |
| time.injuryTime1                           | Match   | injury_time1       |
| time.injuryTime2                           | Match   | injury_time2       |

### Eşleşme Tablosu

Bu tabloyla birlikte verilerindeki her sütunun hangi modele karşılık geldiğini ve modelde hangi alanla eşleştiğini gördün. Artık bu bilgileri kullanarak veritabanına uygun şekilde verileri işleyebilirsin. 

Başka bir ayrıntı veya ekleme ihtiyacı olursa bana sorabilirsin!

***Soru:*** tamam bu modelleri bir excel de bana göster bana ver

**Cevap:** Verilerdeki sütunların uzunlukları eşit olmadığı için hata alıyoruz. Bunu düzeltmek için, eksik sütunlara `None` ekleyerek hepsini eşit hale getireceğim. Hemen işlemi tekrar yaparak sana Excel dosyasını vereceğim.

**Cevap:** İstediğiniz modelleri ve sütun eşleştirmelerini içeren Excel dosyasını başarıyla oluşturdum. Aşağıdaki bağlantıdan dosyayı indirebilirsiniz:

[Excel dosyasını indir](sandbox:/mnt/data/model_sutun_eslesmesi.xlsx)

***Soru:*** ben şimdi fiksturden günlük olarak maçları eçkiyorum ve gelen dataframe üzerinden modellerime veri dağıtabilir miyim

**Cevap:** Evet, elindeki DataFrame'den verileri Django modellerine dağıtabilir ve veritabanına kaydedebilirsin. Bu işlem için aşağıdaki adımları izleyebilirsin:

### 1. Django Ortamını Hazırlama
Öncelikle Django projesinde gerekli modelleri oluşturduğundan emin olmalısın. Bu modelleri daha önce tartıştığımız şekilde oluşturdun varsayıyorum.

### 2. DataFrame Üzerinden Modellerle Eşleştirme
DataFrame'deki verileri Django modellerine dağıtmak için şu adımları izleyebilirsin:

- Her modeldeki veriyi, DataFrame'deki ilgili sütunlarla eşleştir.
- Veritabanında zaten var olan verileri güncellemek, yoksa yeni veri eklemek için Django'nun `get_or_create` veya `update_or_create` metotlarını kullanabilirsin.

### Örnek: Verileri Django'ya Ekleme

Aşağıda bir örnek senaryo sunuyorum. Bu senaryoda her maç için ülke, turnuva, sezon, takım ve maç bilgileri DataFrame’den alınıp veritabanına kaydediliyor.

#### Örnek: DataFrame'den Verileri Kaydetme

```python
import pandas as pd
from yourapp.models import Country, Tournament, Season, Team, Match

# Örnek bir DataFrame (bu, dışardan çekilen fikstür verilerin olabilir)
df = pd.DataFrame({
    'country_name': ['Croatia', 'Scotland'],
    'country_alpha2': ['HR', 'SC'],
    'tournament_name': ['UEFA Nations League', 'UEFA Nations League'],
    'season_year': [2024, 2024],
    'home_team': ['Croatia', 'Scotland'],
    'away_team': ['Scotland', 'Croatia'],
    'home_score': [2, 1],
    'away_score': [1, 2],
    'match_date': ['2024-10-12', '2024-10-13'],
    'status_code': [100, 100],
    'status_description': ['Finished', 'Finished']
})

# DataFrame üzerinde döngüyle her satırı işle ve modellere kaydet
for index, row in df.iterrows():
    # Ülke kaydetme veya güncelleme
    country, created = Country.objects.get_or_create(
        alpha2=row['country_alpha2'],
        defaults={'name': row['country_name']}
    )

    # Turnuva kaydetme veya güncelleme
    tournament, created = Tournament.objects.get_or_create(
        name=row['tournament_name'],
        defaults={'country': country}
    )

    # Sezon kaydetme veya güncelleme
    season, created = Season.objects.get_or_create(
        year=row['season_year'],
        tournament=tournament
    )

    # Takımlar kaydetme
    home_team, created = Team.objects.get_or_create(
        name=row['home_team'],
        defaults={'country': country}
    )

    away_team, created = Team.objects.get_or_create(
        name=row['away_team'],
        defaults={'country': country}
    )

    # Maçı kaydetme
    match, created = Match.objects.get_or_create(
        home_team=home_team,
        away_team=away_team,
        season=season,
        date=row['match_date'],
        defaults={
            'home_score': row['home_score'],
            'away_score': row['away_score'],
            'status_code': row['status_code'],
            'status_description': row['status_description']
        }
    )
```

### Açıklamalar:
- `get_or_create`: Veritabanında aynı kayda sahip bir veri olup olmadığını kontrol eder. Eğer yoksa yeni bir kayıt oluşturur, varsa mevcut olanı döner.
- `iterrows()`: DataFrame'deki her satırı döngüyle işler.
- Veriler: DataFrame'den gelen her satırdaki veriler ilgili modele kaydedilir.

### 3. Performansı Artırmak İçin
Bu işlemi her gün düzenli olarak yapıyorsan ve veritabanı performansını artırmak istiyorsan:
- **Bulk insert** işlemlerini tercih edebilirsin. Örneğin, önce tüm yeni takımları veya maçları topluca eklemek için `bulk_create` kullanabilirsin.
- Veritabanında **indexler** oluşturmak, büyük verilerde sorgu hızını artırabilir.

### 4. Hataları Yakalama
Bu işlemler sırasında veri tipine, boş değerlere veya mevcut olmayan ilişkilere dikkat etmelisin. `try-except` blokları kullanarak hataları yakalayabilir ve loglayabilirsin.

Bu yapıyla DataFrame üzerinden gelen verileri modellerine rahatça dağıtabilirsin. Eğer başka bir konuda yardıma ihtiyacın olursa, memnuniyetle yardımcı olurum!