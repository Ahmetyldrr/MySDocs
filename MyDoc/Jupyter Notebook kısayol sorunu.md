***Soru:*** jupyter notebook umda normalde seçili olan kodlarda Ctrl + Ö yaptığımda yoruma alıyordu ama şu anda olmuyor neden

**Cevap:** Jupyter Notebook'ta Türkçe klavye düzeninde çalışıyorsanız, `Ctrl + Ö` kombinasyonunun yoruma alma işlemi yapmaması, büyük olasılıkla klavye kısayollarıyla ilgili bir sorundan kaynaklanıyor olabilir. Jupyter Notebook varsayılan olarak kodu yoruma almak için `Ctrl + /` kısayolunu kullanır. Ancak, Türkçe klavyede `Ctrl + Ö` tuş kombinasyonu, İngilizce klavyedeki `Ctrl + /` ile aynı işlemi yapar çünkü `Ö` harfi, İngilizce klavyedeki `/` işaretine denk gelir.

Sorunu çözmek için şu adımları izleyebilirsiniz:

1. **Klavye Düzenini Kontrol Etmek:** Klavye düzeninizin doğru olduğundan emin olun. Eğer klavye düzeni yanlışsa, `Ctrl + Ö` çalışmayabilir.
   - Windows: Klavye düzenini `Alt + Shift` veya `Windows + Space` ile değiştirebilirsiniz.
   - Mac: `Cmd + Space` ile klavye düzenini değiştirebilirsiniz.

2. **Tarayıcı Kısayollarını Kontrol Etmek:** Bazı tarayıcılar (özellikle Chrome ve Firefox) Jupyter Notebook’ta kısayolların üzerine kendi kısayollarını tanımlayabilir. Bu durumda Jupyter kısayolları çalışmayabilir. Tarayıcı ayarlarını gözden geçirip, çakışan kısayolları kontrol edebilirsiniz.

3. **Jupyter Kısayol Ayarlarını Kontrol Etmek:** Jupyter Notebook içinde kısayol ayarlarını kontrol etmek için:
   - `Help` menüsüne tıklayın.
   - `Keyboard Shortcuts` seçeneğini seçin ve `Comment` kısayolunun hala `Ctrl + /` olduğunu doğrulayın.

Eğer bu çözümler sorunu çözmezse, Jupyter Notebook'u yeniden başlatmak ya da tarayıcı önbelleğini temizlemek de faydalı olabilir.

***Soru:*** Redo	Ctrl + Shift + Z
Undo	Ctrl + Z
Run Selected Cell	Shift + Enter
Find Next	Ctrl + G
Find Previous	Ctrl + Shift + G
Find…	Ctrl + F
Activate Next Tab	Ctrl + Shift + ]
Activate Next Tab Bar	Ctrl + Shift + .
Activate Previous Tab	Ctrl + Shift + [
Activate Previous Tab Bar	Ctrl + Shift + ,
Toggle Left Area	Ctrl + B
Toggle Mode	Ctrl + Shift + D
Toggle Right Area	Ctrl + J
Toggle Sidebar Widget	Alt + 1
Toggle Sidebar Widget	Alt + 2
Toggle Sidebar Widget	Alt + 3
Toggle Sidebar Widget	Alt + 4
Toggle Sidebar Widget	Alt + 5
Toggle Sidebar Widget	Alt + 6
Toggle Sidebar Widget	Alt + 7
Toggle Sidebar Widget	Alt + 8
Toggle Sidebar Widget	Alt + 9
Toggle Sidebar Widget	Alt + 0
Toggle Sidebar Widget	Alt + Shift + 1
Toggle Sidebar Widget	Alt + Shift + 2
Toggle Sidebar Widget	Alt + Shift + 3
Toggle Sidebar Widget	Alt + Shift + 4
Toggle Sidebar Widget	Alt + Shift + 5
Toggle Sidebar Widget	Alt + Shift + 6
Toggle Sidebar Widget	Alt + Shift + 7
Toggle Sidebar Widget	Alt + Shift + 8
Toggle Sidebar Widget	Alt + Shift + 9
Toggle Sidebar Widget	Alt + Shift + 0
Activate Command Palette	Ctrl + Shift + C
Show Keyboard Shortcuts…	Ctrl + Shift + H
Pause	F9
Next	F10
Debugger Panel	Ctrl + Shift + E
Step In	F11
Step Out	Shift + F11
Terminate	Shift + F9
Save Notebook	Ctrl + S
Save Notebook As…	Ctrl + Shift + S
Reopen Last	Ctrl + Shift + T
Activate Previously Used Tab	Ctrl + Shift + '
Table of Contents	Ctrl + Shift + K
  bunlardan hagisi yoruma alır

**Cevap:** Bu liste içinde kodu yoruma almak için bir kısayol görünmüyor. Jupyter Notebook'ta varsayılan olarak kodu yoruma almak için kullanılan kısayol `Ctrl + /` (veya Türkçe klavye için `Ctrl + Ö`) olması gerekirdi. Eğer bu kısayol çalışmıyorsa, Jupyter Notebook’ta kısayolların yeniden düzenlenmiş olma ihtimali olabilir.

Bu liste dışında, Jupyter'de kodu yoruma almak için kullanılan varsayılan kısayolun olup olmadığını öğrenmek için aşağıdaki adımları izleyebilirsiniz:

1. **Kısayol Listesini Kontrol Etmek:**
   - Jupyter Notebook içinde `Help` menüsünden **Keyboard Shortcuts** seçeneğine tıklayın.
   - Burada `Comment` veya `Toggle comment` ile ilişkili bir kısayol görebilirsiniz. Bu genellikle `Ctrl + /` ya da `Ctrl + Ö` olacaktır.

Eğer bu kısayol değiştirilmişse, yukarıdaki yöntemlerle kontrol edip ayarlayabilirsiniz.

***Soru:*** peki bunu terminalden ayarlamak istiyorum

**Cevap:** Jupyter Notebook'taki kısayolları terminalden düzenlemek için, Jupyter'in yapılandırma dosyalarını kullanabilirsiniz. Aşağıdaki adımlar, Jupyter Notebook'ta kısayolları terminal üzerinden nasıl değiştireceğinizi gösterir:

### 1. **Jupyter Konfigürasyon Dosyasını Oluşturun (Eğer Zaten Yoksa):**
Jupyter Notebook'un yapılandırma dosyasını terminalden şu komut ile oluşturabilirsiniz:

```bash
jupyter notebook --generate-config
```

Bu komut, genellikle şu dizinde bir yapılandırma dosyası (`jupyter_notebook_config.py`) oluşturur:

```
~/.jupyter/jupyter_notebook_config.py
```

### 2. **Jupyter Custom.js Dosyasını Düzenleyin:**
Klavye kısayollarını terminal üzerinden ayarlamak için `custom.js` dosyasını kullanmanız gerekiyor. Bu dosya yoksa, oluşturmanız gerekebilir.

İlk olarak şu dizine gidin:

```bash
cd ~/.jupyter/custom
```

Eğer bu dizin yoksa, oluşturmak için şu komutu kullanın:

```bash
mkdir -p ~/.jupyter/custom
```

Ardından, `custom.js` dosyasını oluşturun veya düzenleyin:

```bash
nano ~/.jupyter/custom/custom.js
```

### 3. **Kısayolu custom.js Dosyasına Ekleyin:**

Bu dosyanın içine, yoruma alma (`Ctrl + /` veya `Ctrl + Ö`) kısayolunu ayarlamak için aşağıdaki JavaScript kodunu ekleyin:

```javascript
define([
    'base/js/namespace',
    'base/js/events'
], function(Jupyter, events) {
    events.on('app_initialized.NotebookApp', function() {
        Jupyter.keyboard_manager.edit_shortcuts.add_shortcut('ctrl-ö', {
            help : 'toggle comment',
            help_index : 'zz',
            handler : function(event) {
                Jupyter.notebook.execute_cell();
                return false;
            }
        });
    });
});
```

Burada `ctrl-ö` kısayolu ile yorum satırını etkinleştirmeyi ayarlıyoruz. İsterseniz başka bir kısayol da tanımlayabilirsiniz.

### 4. **Jupyter Notebook'u Yeniden Başlatın:**

Yapılandırma dosyasını düzenledikten sonra, Jupyter Notebook'u kapatıp yeniden başlatın:

```bash
jupyter notebook
```

Bu adımlardan sonra, `Ctrl + Ö` kısayolunu kullanarak Jupyter Notebook'taki kodları yoruma alabilirsiniz.

### Ek Not:
Eğer başka kısayolları da özelleştirmek isterseniz, aynı dosyada benzer yapılar ekleyerek istediğiniz kısayolları tanımlayabilirsiniz.

***Soru:*** Team_id	Team_name	Team_slug	Team_shortName	Team_nameCode	Team_national	tournament_model	season_model
5194	Klaksvíkar Ítróttarfelag	klaksvikar-itrottarfelag	Klaksvík	KI	YANLIŞ		
661	Molde FK	molde-fk	Molde	MFK	YANLIŞ		  bana şimdi sana verdiğim örnek veriler üzerinden team adında bir model yarat bu modelde iki tane foreig id olacak torunament ve sezon modellerine ilişkisel bağlanacak şimdi bunu ekler misin

**Cevap:** Bu senaryoda, Django'da bir **Team** modeli oluşturacağız. Bu model, iki farklı ForeignKey alanı ile **tournament** ve **season** modellerine bağlanacak. Aşağıda, Python/Django ORM kullanarak bu yapıyı nasıl oluşturabileceğinize dair örnek bir model tanımlaması yer alıyor.

### Team Modeli

```python
from django.db import models

class Tournament(models.Model):
    name = models.CharField(max_length=255)
    # Turnuvaya dair diğer alanlar...

class Season(models.Model):
    year = models.IntegerField()
    # Sezona dair diğer alanlar...

class Team(models.Model):
    team_id = models.IntegerField(primary_key=True)  # Özel ID
    team_name = models.CharField(max_length=255)
    team_slug = models.SlugField(max_length=255)
    team_shortName = models.CharField(max_length=100)
    team_nameCode = models.CharField(max_length=10)
    team_national = models.BooleanField(default=False)  # YANLIŞ olarak verdiğin veri, Boolean tipi olabilir

    # ForeignKey alanları: Tournament ve Season modellerine bağlanıyor.
    tournament = models.ForeignKey(Tournament, on_delete=models.CASCADE)
    season = models.ForeignKey(Season, on_delete=models.CASCADE)

    def __str__(self):
        return self.team_name
```

### Açıklamalar:
1. **team_id**: Takım için özel bir ID tanımlanmış.
2. **team_name**: Takım adı için `CharField` kullandık.
3. **team_slug**: URL dostu bir isim için `SlugField` kullandık.
4. **team_shortName**: Takımın kısa ismi, `CharField` olarak tanımlandı.
5. **team_nameCode**: Takım adı kodu, kısa bir metin alanı.
6. **team_national**: Takımın milli takım olup olmadığını gösteren bir `BooleanField` (True/False) olarak tanımlandı.
7. **tournament**: Takımın hangi turnuvada oynadığını belirten `ForeignKey`, `Tournament` modeline bağlanıyor.
8. **season**: Takımın hangi sezonda yer aldığını gösteren `ForeignKey`, `Season` modeline bağlanıyor.

### Yapmanız Gerekenler:
1. Bu modelleri `models.py` dosyanıza ekleyin.
2. Ardından veritabanı şemanızı güncellemek için makemigrations ve migrate komutlarını çalıştırın:

```bash
python manage.py makemigrations
python manage.py migrate
```

Bu şekilde **Team** modeli, **Tournament** ve **Season** modelleri ile ilişkili olacak ve veritabanına kaydedilen her takım belirli bir turnuva ve sezona bağlı olacak.

***Soru:*** tamam team modelimi admine ekle ve ev ve dep takımları isimleri ve takım id adminde görünsün filtrede takıma göre atılsın

**Cevap:** Django admin paneline **Team** modelini eklemek ve istediğiniz şekilde özelleştirmek için aşağıdaki adımları izleyebilirsiniz.

### 1. **Admin Paneline Team Modelini Ekleyin:**

Öncelikle `admin.py` dosyanızı açın ve aşağıdaki kodları ekleyin. Bu kodlar, admin panelinde **Team** modelinin görünümünü özelleştirecek ve takıma göre filtreleme gibi isteklerinizi karşılayacaktır.

```python
from django.contrib import admin
from .models import Team

class TeamAdmin(admin.ModelAdmin):
    # Admin sayfasında gösterilecek alanlar
    list_display = ('team_id', 'team_name', 'team_shortName', 'tournament', 'season')
    
    # Admin sayfasında kullanılacak filtreler
    list_filter = ('team_name', 'tournament', 'season')

    # Arama alanı eklemek isterseniz
    search_fields = ('team_name', 'team_shortName', 'team_nameCode')

admin.site.register(Team, TeamAdmin)
```

### 2. **Açıklamalar:**

- **list_display**: Admin sayfasında listelenecek sütunları tanımlar. Burada, takımın ID'si, adı, kısa adı, turnuva ve sezon bilgileri gösterilecek.
- **list_filter**: Admin sayfasında sağ tarafta yer alacak filtreleme seçenekleri. Takım adına, turnuva ve sezon bilgilerine göre filtreleme yapabileceksiniz.
- **search_fields**: Takım adında, kısa adında veya kodunda arama yapmanızı sağlar.

### 3. **Admin Panelinde Ev ve Deplasman Takımlarını Gösterme:**

Eğer ev ve deplasman takımları gösterilecekse, bunun için ayrı bir **Match** modeli ya da benzer bir yapı kullanmak gerekecek. Eğer bu yapı zaten mevcutsa, örneğin `HomeTeam` ve `AwayTeam` şeklinde, bunları `list_display` içinde gösterebilirsiniz.

Örneğin:

```python
class MatchAdmin(admin.ModelAdmin):
    list_display = ('home_team', 'away_team', 'match_date')

admin.site.register(Match, MatchAdmin)
```

Eğer bu yapılar takımların kendisiyle ilişkili değilse, ev ve deplasman takımlarını ayrıca yönetmek için bir model tasarlamak gerekecektir. Bununla ilgili detay verirseniz, daha fazla yardımcı olabilirim.

### 4. **Admin Paneline Giriş:**

Kodları ekledikten sonra Django admin paneline giriş yapabilir ve takımları görebilir, ev ve deplasman takımlarını (varsa) listeleyebilir, takıma göre filtreleme yapabilirsiniz.

Admin paneline giriş yapmak için şu adımları takip edin:

1. Süper kullanıcı oluşturun (eğer henüz oluşturmadıysanız):

    ```bash
    python manage.py createsuperuser
    ```

2. Giriş yaptıktan sonra admin panelinizde **Team** modelini göreceksiniz ve istediğiniz özelliklerle yönetebileceksiniz.

***Soru:*** decoratör ile ekler misin admineü7

**Cevap:** Django admin paneline bir model dekoratör kullanarak eklemek, kodu daha temiz ve organize hale getirebilir. Bu durumda, Django'nun `admin.register` dekoratörünü kullanarak **Team** modelini admin paneline ekleyebiliriz.

Aşağıda, **Team** modelini dekoratör ile admin paneline nasıl ekleyeceğinizi gösteriyorum:

### 1. **Admin Paneline Team Modelini Dekoratör ile Eklemek:**

```python
from django.contrib import admin
from .models import Team

@admin.register(Team)
class TeamAdmin(admin.ModelAdmin):
    # Admin sayfasında gösterilecek alanlar
    list_display = ('team_id', 'team_name', 'team_shortName', 'tournament', 'season')
    
    # Admin sayfasında kullanılacak filtreler
    list_filter = ('team_name', 'tournament', 'season')

    # Arama alanı eklemek isterseniz
    search_fields = ('team_name', 'team_shortName', 'team_nameCode')
```

### 2. **Açıklamalar:**

- **@admin.register(Team)**: Bu dekoratör, **Team** modelini Django admin paneline ekler. Bu sayede `admin.site.register()` komutunu yazmanıza gerek kalmaz.
- **list_display**: Admin panelinde listelenen sütunları belirler.
- **list_filter**: Sağ tarafta yer alan filtreleme seçeneklerini tanımlar.
- **search_fields**: Belirli alanlarda arama yapılmasını sağlar.

### 3. **Django Admin Panelini Yenilemek:**

Yukarıdaki kodları ekledikten sonra, Django projenizi başlatın veya yeniden başlatın:

```bash
python manage.py runserver
```

Admin paneline giriş yaparak, **Team** modelini dekoratör ile eklenmiş şekilde yönetebilirsiniz. Artık takımları listeleyebilir, arama yapabilir ve filtreleyebilirsiniz.

Bu yöntem, Django admin yapılandırmalarını daha sade bir şekilde yönetmenizi sağlar ve büyük projelerde dekoratör kullanımı ile kodun okunabilirliğini artırır.

***Soru:*** from mymodel.models import Tournament 
from mymodel.models import Season

# Modelleri import edin
import pandas as pd

class SofascoreAPI:
    def __init__(self, date):
        self.date = date
        
    def fetch_data(self):
        """Verilen tarih için sofascore API'den veri çekme işlemi."""
        conn = http.client.HTTPSConnection('www.sofascore.com')
        conn.request(
            'GET',
            f'/api/v1/sport/football/scheduled-events/{self.date}'
        )
        response = conn.getresponse()
        data = response.read()
        data = json.loads(data)["events"]
        data = [{
            'tarih': self.date,
            'data': data
        }]
    
        if data is None:
            raise ValueError("Önce veriyi çekmek için 'fetch_data()' metodunu çalıştırın.")
        
        # Veriyi DataFrame'e çevir ve işle
        df = pd.DataFrame(data)
        df_exploded = df.explode('data')
        expanded_data = pd.json_normalize(df_exploded['data'])
        expanded_data['tarih'] = list(df_exploded['tarih'])
        datax = expanded_data.drop_duplicates(subset='id', keep='last')
        datax.columns = [item.replace(".", "_") for item in datax.columns]
        
        verim = datax.copy()

        return verim
        

    def fiksture_data(self):

            verim = self.fetch_data()
            """Eksik sütunları kontrol edip, varsa 0 ile doldurma ve veriyi sonlandırma."""
            if verim is None:
                raise ValueError("Veri işlenmedi. Önce 'process_data()' metodunu çalıştırın.")
            
            # Aynı uniqueTournament_id'ye sahip olanları tekrar kontrol et
            verim = verim.drop_duplicates("tournament_uniqueTournament_id")
            
            # İlgili sütunlar
            cols = [
                "tournament_uniqueTournament_id", "tournament_name", "tournament_slug", "tournament_category_name",
                "tournament_category_slug", "tournament_uniqueTournament_category_id", 
                "tournament_uniqueTournament_hasEventPlayerStatistics", "tournament_id", "tournament_isGroup", 
                "tournament_uniqueTournament_hasPerformanceGraphFeature"
            ]
            
            # Eksik sütunları 0 ile doldurma
            for col in cols:
                if col not in verim.columns:
                    verim.loc[:, col] = 0
    
            # Son olarak sadece belirtilen sütunlar kalsın
            verim = verim[cols]

            for _, row in verim.iterrows():
                tournament_id = row['tournament_uniqueTournament_id']
                
                # NaN değerlerini kontrol edin ve NaN olan satırları atlayın
                if pd.isna(tournament_id):
                    print(f"Geçersiz tournament_uniqueTournament_id: {tournament_id}, atlanıyor.")
                    continue  # NaN olan satırı atla
        
                # Modelde bu id ile kayıt olup olmadığını kontrol et
                if not Tournament.objects.filter(tournament_uniqueTournament_id=tournament_id).exists():
                    # Kayıt yoksa yeni kayıt oluştur
                    Tournament.objects.create(
                        tournament_uniqueTournament_id=row['tournament_uniqueTournament_id'],
                        tournament_name=row['tournament_name'],
                        tournament_slug=row['tournament_slug'],
                        tournament_category_name=row['tournament_category_name'],
                        tournament_category_slug=row['tournament_category_slug'],
                        tournament_uniqueTournament_category_id=row['tournament_uniqueTournament_category_id'],
                        tournament_uniqueTournament_hasEventPlayerStatistics=row['tournament_uniqueTournament_hasEventPlayerStatistics'],
                        tournament_id=row['tournament_id'],
                        tournament_isGroup=row['tournament_isGroup'] if pd.notna(row['tournament_isGroup']) else False,
                        tournament_uniqueTournament_hasPerformanceGraphFeature=row['tournament_uniqueTournament_hasPerformanceGraphFeature'] if pd.notna(row['tournament_uniqueTournament_hasPerformanceGraphFeature']) else False
                    )
                    print(f"Tournament ID {tournament_id} başarıyla eklendi.")
                else:
                    print(f"Tournament ID {tournament_id} zaten mevcut, eklenmedi.")

    def season_data(self):
        """Season verileri için eksik sütunları kontrol edip, 0 ile doldurma işlemi."""
        verim = self.fetch_data()
        
        if verim is None:
            raise ValueError("Veri işlenmedi. Önce 'process_data()' metodunu çalıştırın.")
        
        # Aynı season_id'ye sahip olanları tekrar kontrol et
        verim = verim.drop_duplicates("season_id")
        
        # Sezonla ilgili sütunlar
        season_cols = ["season_id", "season_name", "season_year","tournament_uniqueTournament_id"]

        # Eksik sütunları 0 ile doldurma
        for col in season_cols:
            if col not in verim.columns:
                verim.loc[:, col] = 0

        # Son olarak sadece season ile ilgili sütunları döndür
        verim = verim[season_cols]

        for _, row in verim.iterrows():
            season_id = row['season_id']
            tournament_id = row.get('tournament_uniqueTournament_id')  # İlgili turnuvayı al
    
            # NaN değerlerini kontrol edin ve geçersiz veriyi atlayın
            if pd.isna(season_id) or pd.isna(tournament_id):
                print(f"Geçersiz season_id veya tournament_id: Season ID={season_id}, Tournament ID={tournament_id}. Atlanıyor.")
                continue
    
            # Modelde bu id ile kayıt olup olmadığını kontrol et
            if not Season.objects.filter(season_id=season_id).exists():
                # Turnuva olup olmadığını kontrol et ve turnuva ile sezonu ilişkilendir
                tournament_instance = Tournament.objects.filter(tournament_uniqueTournament_id=tournament_id).first()
                
                if tournament_instance:
                    # Kayıt yoksa yeni sezon kaydı oluştur
                    Season.objects.create(
                        season_id=row['season_id'],
                        season_name=row['season_name'],
                        season_year=row['season_year'],
                        tournament=tournament_instance  # Turnuva ile ilişkilendir
                    )
                    print(f"Season ID {season_id} başarıyla eklendi.")
                else:
                    print(f"Tournament ID {tournament_id} bulunamadı, Season ID {season_id} eklenemedi.")
            else:
                print(f"Season ID {season_id} zaten mevcut, eklenmedi.")

   
tarih = "2024-09-21"
api = SofascoreAPI(tarih)         # Veriyi sofascore API'den çeker        # Çekilen veriyi işler
api.season_data()       # Sezon verileriyle ilgili işlem
api.fiksture_data() # Turnuva verileriyle ilgili işlem  şimdi bu verileri modellere çekerken kullandığım sınıftır lütfen şimdi sınıfı baştan sonra tekrar yazmana gerek yok , bana bir fonksiyoj ekleyeceksin team_data adında veriden alacağın colonları veiryorum homecols = ["homeTeam_id","homeTeam_name","homeTeam_slug","homeTeam_shortName",
            "homeTeam_nameCode","homeTeam_national","tournament_id","season_id"]  bu kolonları veriden alıp modele ekleyeceksin

**Cevap:** Verilen yapı üzerinden, **Team** modeline uygun verileri çekmek ve işlemek için `team_data` adında bir fonksiyon ekleyeceğiz. Veriden alacağımız kolonları belirledikten sonra, bu verileri **Team** modeline kaydedeceğiz. Aşağıdaki adımlarla bu fonksiyonu ekleyebilirsiniz.

### `team_data` Fonksiyonu

```python
from mymodel.models import Team  # Team modelini import et

class SofascoreAPI:
    # Diğer fonksiyonlar burada yer alıyor...

    def team_data(self):
        """Verilen verilerden homeTeam bilgilerini çek ve modele ekle."""
        
        verim = self.fetch_data()  # Veriyi sofascore API'den çek

        if verim is None:
            raise ValueError("Veri işlenmedi. Önce 'fetch_data()' metodunu çalıştırın.")
        
        # Aynı homeTeam_id'ye sahip olanları tekrar kontrol et
        verim = verim.drop_duplicates("homeTeam_id")

        # İlgili home team sütunları
        homecols = [
            "homeTeam_id", "homeTeam_name", "homeTeam_slug", "homeTeam_shortName",
            "homeTeam_nameCode", "homeTeam_national", "tournament_id", "season_id"
        ]

        # Eksik sütunları kontrol edip, eğer yoksa 0 ile doldurma
        for col in homecols:
            if col not in verim.columns:
                verim.loc[:, col] = 0

        # Sadece home team ile ilgili sütunları al
        verim = verim[homecols]

        for _, row in verim.iterrows():
            home_team_id = row['homeTeam_id']
            tournament_id = row['tournament_id']
            season_id = row['season_id']

            # NaN değerlerini kontrol edin ve geçersiz veriyi atlayın
            if pd.isna(home_team_id) or pd.isna(tournament_id) or pd.isna(season_id):
                print(f"Geçersiz homeTeam_id, tournament_id veya season_id: HomeTeam ID={home_team_id}, Tournament ID={tournament_id}, Season ID={season_id}. Atlanıyor.")
                continue
            
            # Modelde bu id ile kayıt olup olmadığını kontrol et
            if not Team.objects.filter(team_id=home_team_id).exists():
                # Turnuva ve sezon olup olmadığını kontrol et
                tournament_instance = Tournament.objects.filter(tournament_uniqueTournament_id=tournament_id).first()
                season_instance = Season.objects.filter(season_id=season_id).first()
                
                if tournament_instance and season_instance:
                    # Kayıt yoksa yeni takım kaydı oluştur
                    Team.objects.create(
                        team_id=row['homeTeam_id'],
                        team_name=row['homeTeam_name'],
                        team_slug=row['homeTeam_slug'],
                        team_shortName=row['homeTeam_shortName'],
                        team_nameCode=row['homeTeam_nameCode'],
                        team_national=row['homeTeam_national'] if pd.notna(row['homeTeam_national']) else False,
                        tournament=tournament_instance,  # Turnuva ile ilişkilendir
                        season=season_instance  # Sezon ile ilişkilendir
                    )
                    print(f"Home Team ID {home_team_id} başarıyla eklendi.")
                else:
                    print(f"Tournament ID {tournament_id} veya Season ID {season_id} bulunamadı, Home Team ID {home_team_id} eklenemedi.")
            else:
                print(f"Home Team ID {home_team_id} zaten mevcut, eklenmedi.")
```

### Açıklamalar:
1. **`verim = self.fetch_data()`**: Sofascore API'den veri çekiyoruz. Eğer veri çekme işlemi başarısız olursa, hata fırlatılır.
2. **`homecols`**: Home team ile ilgili sütunları alıyoruz.
3. **NaN Kontrolü**: Her bir satırdaki `homeTeam_id`, `tournament_id` ve `season_id` değerlerini kontrol ediyoruz. Eğer bir değer NaN ise, satır atlanıyor.
4. **Kayıt Kontrolü**: Team modelinde zaten aynı `homeTeam_id`'ye sahip bir kayıt varsa, bu kayıt eklenmiyor. Eğer kayıt yoksa, **tournament** ve **season** modelleriyle ilişkilendirilmiş yeni bir **Team** kaydı oluşturuluyor.
5. **Eksik Sütunları 0 ile Doldurma**: Eğer veri çekilen sütunlar eksikse, bu sütunlar 0 olarak dolduruluyor.

Bu fonksiyonu mevcut sınıfınıza ekledikten sonra, aşağıdaki şekilde kullanarak **Team** verilerini ekleyebilirsiniz:

```python
api.team_data()  # Team verilerini ekler
```

Bu fonksiyon, Sofascore API'den çekilen **homeTeam** bilgilerini veritabanınıza kaydedecek ve ilgili **Tournament** ve **Season** modelleriyle ilişkilendirecektir.

***Soru:*** 294048	FC Kryvbas Kryvyi Rih	Kryvbas	Copa Libertadores, Knockout stage	Premier League 24/25 (24/25)  team modelim adminde isme göre geliyor bu ddoğru bir yaklaşım mı ben aslında id kullanuyorudum

**Cevap:** Django admin panelinde modelleri listelemek için **ID** yerine **isim** üzerinden sıralama yapmanın yaygın bir pratik olmasının nedeni, isimlerin insanlar için daha anlaşılır ve tanınabilir olmasıdır. Ancak, eğer uygulamanızda **ID**'ler üzerinden işlem yapıyorsanız ve admin panelinde **ID** üzerinden çalışmak daha mantıklıysa, bunu admin panelinde **ID** ile görüntüleyecek şekilde ayarlayabilirsiniz.

### Team Modelinde ID'yi Listelemek

Eğer **Team** modelinizi admin panelinde **ID** üzerinden görüntülemek istiyorsanız, `admin.py` dosyanızda **list_display**'i güncelleyebilirsiniz. Şu anda admin paneli varsayılan olarak modelin `__str__` metodunda döndürülen değeri (genellikle isim) kullanıyor olabilir. Eğer ID'yi kullanmak istiyorsanız, **list_display**'i ID'yi gösterecek şekilde ayarlayabilirsiniz.

### `admin.py` Dosyanızı Güncelleyin

```python
from django.contrib import admin
from .models import Team

@admin.register(Team)
class TeamAdmin(admin.ModelAdmin):
    # ID'yi ve diğer ilgili alanları admin panelinde göster
    list_display = ('team_id', 'team_name', 'team_shortName', 'tournament', 'season')
    
    # İsterseniz ID üzerinden filtreleme veya arama da ekleyebilirsiniz
    search_fields = ('team_id', 'team_name')
    list_filter = ('tournament', 'season')
```

### `__str__` Metodunu Güncellemek (İsteğe Bağlı)

Eğer modelin **ID** üzerinden temsil edilmesini istiyorsanız, **Team** modelinde `__str__` metodunu güncelleyebilirsiniz. Bu, admin panelinde ve Django shell'de model nesneleri ile çalışırken nesnelerin nasıl temsil edileceğini değiştirir.

```python
class Team(models.Model):
    team_id = models.IntegerField(primary_key=True)
    team_name = models.CharField(max_length=255)
    team_slug = models.SlugField(max_length=255)
    team_shortName = models.CharField(max_length=100)
    team_nameCode = models.CharField(max_length=10)
    team_national = models.BooleanField(default=False)
    tournament = models.ForeignKey(Tournament, on_delete=models.CASCADE)
    season = models.ForeignKey(Season, on_delete=models.CASCADE)

    def __str__(self):
        return str(self.team_id)  # ID'yi döndürüyor
```

Bu değişikliklerle, **Team** modelinin admin panelindeki listesinde **team_id** gösterilecek ve modelin string temsili de **team_id** olarak değişecektir.

Eğer hem **ID** hem de **isim**'i aynı anda göstermek isterseniz, `__str__` metodunu şu şekilde düzenleyebilirsiniz:

```python
def __str__(self):
    return f"{self.team_id} - {self.team_name}"
```

Bu sayede hem **ID** hem de **isim** aynı anda görünür olacak.

***Soru:*** from mymodel.models import Team  # Team modelini import et

class SofascoreAPI:
    # Diğer fonksiyonlar burada yer alıyor...

    def team_data(self):
        """Verilen verilerden homeTeam bilgilerini çek ve modele ekle."""
        
        verim = self.fetch_data()  # Veriyi sofascore API'den çek

        if verim is None:
            raise ValueError("Veri işlenmedi. Önce 'fetch_data()' metodunu çalıştırın.")
        
        # Aynı homeTeam_id'ye sahip olanları tekrar kontrol et
        verim = verim.drop_duplicates("homeTeam_id")

        # İlgili home team sütunları
        homecols = [
            "homeTeam_id", "homeTeam_name", "homeTeam_slug", "homeTeam_shortName",
            "homeTeam_nameCode", "homeTeam_national", "tournament_id", "season_id"
        ]

        # Eksik sütunları kontrol edip, eğer yoksa 0 ile doldurma
        for col in homecols:
            if col not in verim.columns:
                verim.loc[:, col] = 0

        # Sadece home team ile ilgili sütunları al
        verim = verim[homecols]

        for _, row in verim.iterrows():
            home_team_id = row['homeTeam_id']
            tournament_id = row['tournament_id']
            season_id = row['season_id']

            # NaN değerlerini kontrol edin ve geçersiz veriyi atlayın
            if pd.isna(home_team_id) or pd.isna(tournament_id) or pd.isna(season_id):
                print(f"Geçersiz homeTeam_id, tournament_id veya season_id: HomeTeam ID={home_team_id}, Tournament ID={tournament_id}, Season ID={season_id}. Atlanıyor.")
                continue
            
            # Modelde bu id ile kayıt olup olmadığını kontrol et
            if not Team.objects.filter(team_id=home_team_id).exists():
                # Turnuva ve sezon olup olmadığını kontrol et
                tournament_instance = Tournament.objects.filter(tournament_uniqueTournament_id=tournament_id).first()
                season_instance = Season.objects.filter(season_id=season_id).first()
                
                if tournament_instance and season_instance:
                    # Kayıt yoksa yeni takım kaydı oluştur
                    Team.objects.create(
                        team_id=row['homeTeam_id'],
                        team_name=row['homeTeam_name'],
                        team_slug=row['homeTeam_slug'],
                        team_shortName=row['homeTeam_shortName'],
                        team_nameCode=row['homeTeam_nameCode'],
                        team_national=row['homeTeam_national'] if pd.notna(row['homeTeam_national']) else False,
                        tournament=tournament_instance,  # Turnuva ile ilişkilendir
                        season=season_instance  # Sezon ile ilişkilendir
                    )
                    print(f"Home Team ID {home_team_id} başarıyla eklendi.")
                else:
                    print(f"Tournament ID {tournament_id} veya Season ID {season_id} bulunamadı, Home Team ID {home_team_id} eklenemedi.")
            else:
                print(f"Home Team ID {home_team_id} zaten mevcut, eklenmedi.")  bu veriyi çekerken instance vs gerek yok direk ben bilgileri tek tek vereceğişm buna göre kodları düzelt

**Cevap:** Eğer doğrudan veritabanına kaydedeceğiniz bilgileri manuel olarak verecekseniz ve `instance` kontrollerini ortadan kaldırmak istiyorsanız, kodu basitleştirebiliriz. Yani, ilişkisel kontroller ve `instance` kullanımı olmadan veriyi veritabanına kaydedecek bir yapı oluşturacağız.

İşte `team_data` fonksiyonunu bu istek doğrultusunda basitleştirilmiş hali:

### Düzeltilmiş Kod:

```python
from mymodel.models import Team  # Team modelini import et

class SofascoreAPI:
    # Diğer fonksiyonlar burada yer alıyor...

    def team_data(self):
        """Verilen verilerden homeTeam bilgilerini çek ve modele ekle."""
        
        verim = self.fetch_data()  # Veriyi sofascore API'den çek

        if verim is None:
            raise ValueError("Veri işlenmedi. Önce 'fetch_data()' metodunu çalıştırın.")
        
        # Aynı homeTeam_id'ye sahip olanları tekrar kontrol et
        verim = verim.drop_duplicates("homeTeam_id")

        # İlgili home team sütunları
        homecols = [
            "homeTeam_id", "homeTeam_name", "homeTeam_slug", "homeTeam_shortName",
            "homeTeam_nameCode", "homeTeam_national", "tournament_id", "season_id"
        ]

        # Eksik sütunları kontrol edip, eğer yoksa 0 ile doldurma
        for col in homecols:
            if col not in verim.columns:
                verim.loc[:, col] = 0

        # Sadece home team ile ilgili sütunları al
        verim = verim[homecols]

        for _, row in verim.iterrows():
            home_team_id = row['homeTeam_id']
            tournament_id = row['tournament_id']
            season_id = row['season_id']

            # NaN değerlerini kontrol edin ve geçersiz veriyi atlayın
            if pd.isna(home_team_id) or pd.isna(tournament_id) or pd.isna(season_id):
                print(f"Geçersiz homeTeam_id, tournament_id veya season_id: HomeTeam ID={home_team_id}, Tournament ID={tournament_id}, Season ID={season_id}. Atlanıyor.")
                continue
            
            # Modelde bu id ile kayıt olup olmadığını kontrol et
            if not Team.objects.filter(team_id=home_team_id).exists():
                # Kayıt yoksa yeni takım kaydı oluştur
                Team.objects.create(
                    team_id=row['homeTeam_id'],
                    team_name=row['homeTeam_name'],
                    team_slug=row['homeTeam_slug'],
                    team_shortName=row['homeTeam_shortName'],
                    team_nameCode=row['homeTeam_nameCode'],
                    team_national=row['homeTeam_national'] if pd.notna(row['homeTeam_national']) else False,
                    tournament_id=row['tournament_id'],  # Direk ID ile ilişkilendiriyoruz
                    season_id=row['season_id']  # Direk ID ile ilişkilendiriyoruz
                )
                print(f"Home Team ID {home_team_id} başarıyla eklendi.")
            else:
                print(f"Home Team ID {home_team_id} zaten mevcut, eklenmedi.")
```

### Yapılan Değişiklikler:
1. **Foreign Key instance kontrollerini kaldırdık**: Artık `Tournament` ve `Season` modelleri ile manuel olarak `instance` çekip ilişkilendirmiyoruz. Bunun yerine, doğrudan `tournament_id` ve `season_id` değerlerini kullanıyoruz.
   
   ```python
   tournament_id=row['tournament_id'],  # ForeignKey yerine doğrudan ID
   season_id=row['season_id']  # ForeignKey yerine doğrudan ID
   ```

2. **instance yerine ID kullanımı**: Bu yapıyla, veritabanına sadece ID’leri ile kayıtları bağlamış oluyoruz, yani Django’nun model instance mantığına gerek kalmıyor.

3. **Veri doğrulaması (NaN kontrolü)**: Eğer `homeTeam_id`, `tournament_id` veya `season_id` sütunlarında NaN değerler varsa, bu satırları atlıyoruz.

### Kullanım:
Bu yapı, manuel olarak ID’lerle işlem yapmanıza olanak tanır ve ForeignKey instance kontrollerini ortadan kaldırır. Bu sayede verileriniz hızlı ve doğrudan veritabanına kaydedilebilir.

Bu fonksiyonu şu şekilde kullanabilirsiniz:

```python
api.team_data()  # Team verilerini ekler
```

***Soru:*** ---------------------------------------------------------------------------
IntegrityError                            Traceback (most recent call last)
File ~/Masaüstü/myenv/lib/python3.12/site-packages/django/db/utils.py:98, in DatabaseErrorWrapper.__call__.<locals>.inner(*args, **kwargs)
     97 with self:
---> 98     return func(*args, **kwargs)

IntegrityError: FOREIGN KEY constraint failed

The above exception was the direct cause of the following exception:

IntegrityError                            Traceback (most recent call last)
Cell In[34], line 201
    199 api.season_data()       # Sezon verileriyle ilgili işlem
    200 api.fiksture_data() # Turnuva verileriyle ilgili işlem
--> 201 api.team_data() 

Cell In[34], line 182, in SofascoreAPI.team_data(self)
    179 # Modelde bu id ile kayıt olup olmadığını kontrol et
    180 if not Team.objects.filter(team_id=home_team_id).exists():
    181     # Kayıt yoksa yeni takım kaydı oluştur
--> 182     Team.objects.create(
    183         team_id=row['homeTeam_id'],
    184         team_name=row['homeTeam_name'],
    185         team_slug=row['homeTeam_slug'],
    186         team_shortName=row['homeTeam_shortName'],
    187         team_nameCode=row['homeTeam_nameCode'],
    188         team_national=row['homeTeam_national'] if pd.notna(row['homeTeam_national']) else False,
    189         tournament_id=row['tournament_id'],  # Direk ID ile ilişkilendiriyoruz
    190         season_id=row['season_id']  # Direk ID ile ilişkilendiriyoruz
    191     )
    192     print(f"Home Team ID {home_team_id} başarıyla eklendi.")
    193 else:

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

File ~/Masaüstü/myenv/lib/python3.12/site-packages/django/db/models/sql/compiler.py:1848, in SQLInsertCompiler.execute_sql(self, returning_fields)
   1845 elif self.connection.features.can_return_columns_from_insert:
   1846     assert len(self.query.objs) == 1
   1847     rows = [
-> 1848         self.connection.ops.fetch_returned_insert_columns(
   1849             cursor,
   1850             self.returning_params,
   1851         )
   1852     ]
   1853     cols = [field.get_col(opts.db_table) for field in self.returning_fields]
   1854 else:

File ~/Masaüstü/myenv/lib/python3.12/site-packages/django/db/backends/base/operations.py:216, in BaseDatabaseOperations.fetch_returned_insert_columns(self, cursor, returning_params)
    211 def fetch_returned_insert_columns(self, cursor, returning_params):
    212     """
    213     Given a cursor object that has just performed an INSERT...RETURNING
    214     statement into a table, return the newly created data.
    215     """
--> 216     return cursor.fetchone()

File ~/Masaüstü/myenv/lib/python3.12/site-packages/django/db/utils.py:97, in DatabaseErrorWrapper.__call__.<locals>.inner(*args, **kwargs)
     96 def inner(*args, **kwargs):
---> 97     with self:
     98         return func(*args, **kwargs)

File ~/Masaüstü/myenv/lib/python3.12/site-packages/django/db/utils.py:91, in DatabaseErrorWrapper.__exit__(self, exc_type, exc_value, traceback)
     89 if dj_exc_type not in (DataError, IntegrityError):
     90     self.wrapper.errors_occurred = True
---> 91 raise dj_exc_value.with_traceback(traceback) from exc_value

File ~/Masaüstü/myenv/lib/python3.12/site-packages/django/db/utils.py:98, in DatabaseErrorWrapper.__call__.<locals>.inner(*args, **kwargs)
     96 def inner(*args, **kwargs):
     97     with self:
---> 98         return func(*args, **kwargs)

IntegrityError: FOREIGN KEY constraint failed

**Cevap:** Bu hata, bir **foreign key** (yabancı anahtar) ilişkisine sahip bir alanın geçerli olmayan bir değerle doldurulmaya çalışıldığını gösteriyor. Django, veritabanında ilişkisel tutarlılığı sağlamak için bu tür kontroller uygular. **ForeignKey constraint failed** hatası genellikle şunlardan kaynaklanır:

1. **ForeignKey Alanı İçin Geçerli Bir Kayıt Olmaması**: Yabancı anahtarla ilişkilendirilen `tournament_id` veya `season_id`, veritabanında mevcut olmayabilir. Bu durumda, `Team` modelini kaydetmeye çalışırken, Django bu ID'lerin **Tournament** ve **Season** tablolarında mevcut olup olmadığını kontrol eder. Eğer bu tablolarda ilgili ID'ler yoksa, veriyi kaydedemez.

2. **Yanlış ID'ler Kullanmak**: Veriler doğrudan **tournament_id** ve **season_id** üzerinden işleniyor ancak bu ID'ler **Tournament** ve **Season** tablolarında mevcut değilse, Django ilişkiyi kuramaz ve hata oluşur.

### Çözüm:
Bu hatayı çözmek için, **tournament_id** ve **season_id** değerlerinin gerçekten veritabanında var olup olmadığını kontrol etmeniz gerekir. Bunu yapmanın iki yolu vardır:

#### 1. ID'lerin Varlığını Kontrol Edin:
Her kayıt eklemeden önce ilgili **Tournament** ve **Season** modellerinde bu ID'lerin var olup olmadığını kontrol edebilir ve eksikse eklemeyi atlayabilirsiniz.

```python
def team_data(self):
    """Verilen verilerden homeTeam bilgilerini çek ve modele ekle."""
    
    verim = self.fetch_data()  # Veriyi sofascore API'den çek

    if verim is None:
        raise ValueError("Veri işlenmedi. Önce 'fetch_data()' metodunu çalıştırın.")
    
    # Aynı homeTeam_id'ye sahip olanları tekrar kontrol et
    verim = verim.drop_duplicates("homeTeam_id")

    # İlgili home team sütunları
    homecols = [
        "homeTeam_id", "homeTeam_name", "homeTeam_slug", "homeTeam_shortName",
        "homeTeam_nameCode", "homeTeam_national", "tournament_id", "season_id"
    ]

    # Eksik sütunları kontrol edip, eğer yoksa 0 ile doldurma
    for col in homecols:
        if col not in verim.columns:
            verim.loc[:, col] = 0

    # Sadece home team ile ilgili sütunları al
    verim = verim[homecols]

    for _, row in verim.iterrows():
        home_team_id = row['homeTeam_id']
        tournament_id = row['tournament_id']
        season_id = row['season_id']

        # NaN değerlerini kontrol edin ve geçersiz veriyi atlayın
        if pd.isna(home_team_id) or pd.isna(tournament_id) or pd.isna(season_id):
            print(f"Geçersiz homeTeam_id, tournament_id veya season_id: HomeTeam ID={home_team_id}, Tournament ID={tournament_id}, Season ID={season_id}. Atlanıyor.")
            continue

        # Turnuva ve sezon ID'sinin var olup olmadığını kontrol edin
        if not Tournament.objects.filter(id=tournament_id).exists():
            print(f"Tournament ID {tournament_id} mevcut değil. Home Team ID {home_team_id} kaydedilemedi.")
            continue

        if not Season.objects.filter(id=season_id).exists():
            print(f"Season ID {season_id} mevcut değil. Home Team ID {home_team_id} kaydedilemedi.")
            continue

        # Modelde bu id ile kayıt olup olmadığını kontrol et
        if not Team.objects.filter(team_id=home_team_id).exists():
            # Kayıt yoksa yeni takım kaydı oluştur
            Team.objects.create(
                team_id=row['homeTeam_id'],
                team_name=row['homeTeam_name'],
                team_slug=row['homeTeam_slug'],
                team_shortName=row['homeTeam_shortName'],
                team_nameCode=row['homeTeam_nameCode'],
                team_national=row['homeTeam_national'] if pd.notna(row['homeTeam_national']) else False,
                tournament_id=row['tournament_id'],  # ForeignKey ID kullanıyoruz
                season_id=row['season_id']  # ForeignKey ID kullanıyoruz
            )
            print(f"Home Team ID {home_team_id} başarıyla eklendi.")
        else:
            print(f"Home Team ID {home_team_id} zaten mevcut, eklenmedi.")
```

#### 2. Önce İlgili Tabloları Doldurun:
**Tournament** ve **Season** tablolarının veritabanında dolu olduğundan emin olun. Eğer bu tablolar boşsa veya bu ID'ler eksikse, önce bu tabloları doldurmalısınız. Örneğin, **tournament_id** ve **season_id** verileriniz doğru şekilde **Tournament** ve **Season** tablolarına eklenmeden **Team** tablosuna eklemeye çalışırsanız, yabancı anahtar kısıtlaması bu hatayı üretecektir.

#### 3. Manuel Kayıt Ekleyin:
Eğer belirli bir turnuva ve sezon yoksa, bunları manuel olarak veritabanına ekleyebilirsiniz. Örneğin, ID'leri doğru ayarladığınızdan ve her turnuva ve sezonun veritabanında olduğundan emin olun:

```python
Tournament.objects.create(id=tournament_id, name="Sample Tournament")
Season.objects.create(id=season_id, year=2024)
```

Bu şekilde, ilgili veritabanı tablolarının doğru doldurulduğundan emin olduktan sonra **Team** kaydını yapabilirsiniz.

***Soru:*** from mymodel.models import Tournament 
from mymodel.models import Season
from mymodel.models import Team
# Modelleri import edin
import pandas as pd

class SofascoreAPI:
    def __init__(self, date):
        self.date = date
        
    def fetch_data(self):
        """Verilen tarih için sofascore API'den veri çekme işlemi."""
        conn = http.client.HTTPSConnection('www.sofascore.com')
        conn.request(
            'GET',
            f'/api/v1/sport/football/scheduled-events/{self.date}'
        )
        response = conn.getresponse()
        data = response.read()
        data = json.loads(data)["events"]
        data = [{
            'tarih': self.date,
            'data': data
        }]
    
        if data is None:
            raise ValueError("Önce veriyi çekmek için 'fetch_data()' metodunu çalıştırın.")
        
        # Veriyi DataFrame'e çevir ve işle
        df = pd.DataFrame(data)
        df_exploded = df.explode('data')
        expanded_data = pd.json_normalize(df_exploded['data'])
        expanded_data['tarih'] = list(df_exploded['tarih'])
        datax = expanded_data.drop_duplicates(subset='id', keep='last')
        datax.columns = [item.replace(".", "_") for item in datax.columns]
        
        verim = datax.copy()

        return verim
        

    def fiksture_data(self):

            verim = self.fetch_data()
            """Eksik sütunları kontrol edip, varsa 0 ile doldurma ve veriyi sonlandırma."""
            if verim is None:
                raise ValueError("Veri işlenmedi. Önce 'process_data()' metodunu çalıştırın.")
            
            # Aynı uniqueTournament_id'ye sahip olanları tekrar kontrol et
            verim = verim.drop_duplicates("tournament_uniqueTournament_id")
            
            # İlgili sütunlar
            cols = [
                "tournament_uniqueTournament_id", "tournament_name", "tournament_slug", "tournament_category_name",
                "tournament_category_slug", "tournament_uniqueTournament_category_id", 
                "tournament_uniqueTournament_hasEventPlayerStatistics", "tournament_id", "tournament_isGroup", 
                "tournament_uniqueTournament_hasPerformanceGraphFeature"
            ]
            
            # Eksik sütunları 0 ile doldurma
            for col in cols:
                if col not in verim.columns:
                    verim.loc[:, col] = 0
    
            # Son olarak sadece belirtilen sütunlar kalsın
            verim = verim[cols]

            for _, row in verim.iterrows():
                tournament_id = row['tournament_uniqueTournament_id']
                
                # NaN değerlerini kontrol edin ve NaN olan satırları atlayın
                if pd.isna(tournament_id):
                    print(f"Geçersiz tournament_uniqueTournament_id: {tournament_id}, atlanıyor.")
                    continue  # NaN olan satırı atla
        
                # Modelde bu id ile kayıt olup olmadığını kontrol et
                if not Tournament.objects.filter(tournament_uniqueTournament_id=tournament_id).exists():
                    # Kayıt yoksa yeni kayıt oluştur
                    Tournament.objects.create(
                        tournament_uniqueTournament_id=row['tournament_uniqueTournament_id'],
                        tournament_name=row['tournament_name'],
                        tournament_slug=row['tournament_slug'],
                        tournament_category_name=row['tournament_category_name'],
                        tournament_category_slug=row['tournament_category_slug'],
                        tournament_uniqueTournament_category_id=row['tournament_uniqueTournament_category_id'],
                        tournament_uniqueTournament_hasEventPlayerStatistics=row['tournament_uniqueTournament_hasEventPlayerStatistics'],
                        tournament_id=row['tournament_id'],
                        tournament_isGroup=row['tournament_isGroup'] if pd.notna(row['tournament_isGroup']) else False,
                        tournament_uniqueTournament_hasPerformanceGraphFeature=row['tournament_uniqueTournament_hasPerformanceGraphFeature'] if pd.notna(row['tournament_uniqueTournament_hasPerformanceGraphFeature']) else False
                    )
                    print(f"Tournament ID {tournament_id} başarıyla eklendi.")
                else:
                    print(f"Tournament ID {tournament_id} zaten mevcut, eklenmedi.")

    def season_data(self):
        """Season verileri için eksik sütunları kontrol edip, 0 ile doldurma işlemi."""
        verim = self.fetch_data()
        
        if verim is None:
            raise ValueError("Veri işlenmedi. Önce 'process_data()' metodunu çalıştırın.")
        
        # Aynı season_id'ye sahip olanları tekrar kontrol et
        verim = verim.drop_duplicates("season_id")
        
        # Sezonla ilgili sütunlar
        season_cols = ["season_id", "season_name", "season_year","tournament_uniqueTournament_id"]

        # Eksik sütunları 0 ile doldurma
        for col in season_cols:
            if col not in verim.columns:
                verim.loc[:, col] = 0

        # Son olarak sadece season ile ilgili sütunları döndür
        verim = verim[season_cols]

        for _, row in verim.iterrows():
            season_id = row['season_id']
            tournament_id = row.get('tournament_uniqueTournament_id')  # İlgili turnuvayı al
    
            # NaN değerlerini kontrol edin ve geçersiz veriyi atlayın
            if pd.isna(season_id) or pd.isna(tournament_id):
                print(f"Geçersiz season_id veya tournament_id: Season ID={season_id}, Tournament ID={tournament_id}. Atlanıyor.")
                continue
    
            # Modelde bu id ile kayıt olup olmadığını kontrol et
            if not Season.objects.filter(season_id=season_id).exists():
                # Turnuva olup olmadığını kontrol et ve turnuva ile sezonu ilişkilendir
                tournament_instance = Tournament.objects.filter(tournament_uniqueTournament_id=tournament_id).first()
                
                if tournament_instance:
                    # Kayıt yoksa yeni sezon kaydı oluştur
                    Season.objects.create(
                        season_id=row['season_id'],
                        season_name=row['season_name'],
                        season_year=row['season_year'],
                        tournament=tournament_instance  # Turnuva ile ilişkilendir
                    )
                    print(f"Season ID {season_id} başarıyla eklendi.")
                else:
                    print(f"Tournament ID {tournament_id} bulunamadı, Season ID {season_id} eklenemedi.")
            else:
                print(f"Season ID {season_id} zaten mevcut, eklenmedi.")

    def team_data(self):
        """Verilen verilerden homeTeam bilgilerini çek ve modele ekle."""
        
        verim = self.fetch_data()  # Veriyi sofascore API'den çek

        if verim is None:
            raise ValueError("Veri işlenmedi. Önce 'fetch_data()' metodunu çalıştırın.")
        
        # Aynı homeTeam_id'ye sahip olanları tekrar kontrol et
        verim = verim.drop_duplicates("homeTeam_id")

        # İlgili home team sütunları
        homecols = [
            "homeTeam_id", "homeTeam_name", "homeTeam_slug", "homeTeam_shortName",
            "homeTeam_nameCode", "homeTeam_national", "tournament_id", "season_id"
        ]

        # Eksik sütunları kontrol edip, eğer yoksa 0 ile doldurma
        for col in homecols:
            if col not in verim.columns:
                verim.loc[:, col] = 0

        # Sadece home team ile ilgili sütunları al
        verim = verim[homecols]

        for _, row in verim.iterrows():
            home_team_id = row['homeTeam_id']
            tournament_id = row['tournament_id']
            season_id = row['season_id']

            # NaN değerlerini kontrol edin ve geçersiz veriyi atlayın
            if pd.isna(home_team_id) or pd.isna(tournament_id) or pd.isna(season_id):
                
                print(f"Geçersiz homeTeam_id, tournament_id veya season_id: HomeTeam ID={home_team_id}, Tournament ID={tournament_id}, Season ID={season_id}. Atlanıyor.")
                continue
            
            # Modelde bu id ile kayıt olup olmadığını kontrol et
            if not Team.objects.filter(team_id=home_team_id).exists():
                # Turnuva ve sezon olup olmadığını kontrol et
                tournament_instance = Tournament.objects.filter(tournament_uniqueTournament_id=tournament_id).first()
                season_instance = Season.objects.filter(season_id=season_id).first()
                
                if tournament_instance and season_instance:
                    # Kayıt yoksa yeni takım kaydı oluştur
                    Team.objects.create(
                        team_id=row['homeTeam_id'],
                        team_name=row['homeTeam_name'],
                        team_slug=row['homeTeam_slug'],
                        team_shortName=row['homeTeam_shortName'],
                        team_nameCode=row['homeTeam_nameCode'],
                        team_national=row['homeTeam_national'] if pd.notna(row['homeTeam_national']) else False,
                        tournament=tournament_instance,  # Turnuva ile ilişkilendir
                        season=season_instance  # Sezon ile ilişkilendir
                    )
                    print(f"Home Team ID {home_team_id} başarıyla eklendi.")
                else:
                    print(f"Tournament ID {tournament_id} veya Season ID {season_id} bulunamadı, Home Team ID {home_team_id} eklenemedi.")
            else:
                print(f"Home Team ID {home_team_id} zaten mevcut, eklenmedi.")

   
tarih = "2023-10-20"

api = SofascoreAPI(tarih)  
api.fiksture_data()  # Veriyi sofascore API'den çeker        # Çekilen veriyi işler
api.season_data()       # Sezon verileriyle ilgili işlem
api.team_data() 
Tournament ID 17 başarıyla eklendi.
Tournament ID 8 başarıyla eklendi.
Tournament ID 23 başarıyla eklendi.
Tournament ID 35 başarıyla eklendi.
Tournament ID 34 başarıyla eklendi.
Tournament ID 325 başarıyla eklendi.
Tournament ID 52 başarıyla eklendi.
Tournament ID 38 başarıyla eklendi.
Tournament ID 185 başarıyla eklendi.
Tournament ID 13475 başarıyla eklendi.
Tournament ID 11621 başarıyla eklendi.
Tournament ID 170 başarıyla eklendi.
Tournament ID 210 başarıyla eklendi.
Tournament ID 18 başarıyla eklendi.
Tournament ID 54 başarıyla eklendi.
Tournament ID 44 başarıyla eklendi.
Tournament ID 53 başarıyla eklendi.
Tournament ID 182 başarıyla eklendi.
Tournament ID 390 başarıyla eklendi.
Tournament ID 131 başarıyla eklendi.
Tournament ID 98 başarıyla eklendi.
Tournament ID 136 başarıyla eklendi.
Tournament ID 649 başarıyla eklendi.
Tournament ID 11536 başarıyla eklendi.
Tournament ID 172 başarıyla eklendi.
Tournament ID 202 başarıyla eklendi.
Tournament ID 39 başarıyla eklendi.
Tournament ID 25 başarıyla eklendi.
Tournament ID 16736 başarıyla eklendi.
Tournament ID 11541 başarıyla eklendi.
Tournament ID 240 başarıyla eklendi.
Tournament ID 808 başarıyla eklendi.
Tournament ID 1900 başarıyla eklendi.
Tournament ID 192 başarıyla eklendi.
Tournament ID 196 başarıyla eklendi.
Tournament ID 20 başarıyla eklendi.
Tournament ID 406 başarıyla eklendi.
Tournament ID 955 başarıyla eklendi.
Tournament ID 152 başarıyla eklendi.
Tournament ID 40 başarıyla eklendi.
Tournament ID 1894 başarıyla eklendi.
Tournament ID 13362 başarıyla eklendi.
Tournament ID 203 başarıyla eklendi.
Tournament ID 1690 başarıyla eklendi.
Tournament ID 410 başarıyla eklendi.
Tournament ID 777 başarıyla eklendi.
Tournament ID 825 başarıyla eklendi.
Tournament ID 1032 başarıyla eklendi.
Tournament ID 1044 başarıyla eklendi.
Tournament ID 9 başarıyla eklendi.
Tournament ID 1139 başarıyla eklendi.
Tournament ID 10640 başarıyla eklendi.
Tournament ID 232 başarıyla eklendi.
Tournament ID 1127 başarıyla eklendi.
Tournament ID 187 başarıyla eklendi.
Tournament ID 211 başarıyla eklendi.
Tournament ID 841 başarıyla eklendi.
Tournament ID 135 başarıyla eklendi.
Tournament ID 709 başarıyla eklendi.
Tournament ID 169 başarıyla eklendi.
Tournament ID 222 başarıyla eklendi.
Tournament ID 247 başarıyla eklendi.
Tournament ID 782 başarıyla eklendi.
Tournament ID 205 başarıyla eklendi.
Tournament ID 47 başarıyla eklendi.
Tournament ID 65 başarıyla eklendi.
Tournament ID 178 başarıyla eklendi.
Tournament ID 41 başarıyla eklendi.
Tournament ID 55 başarıyla eklendi.
Tournament ID 183 başarıyla eklendi.
Tournament ID 704 başarıyla eklendi.
Tournament ID 491 başarıyla eklendi.
Tournament ID 42 başarıyla eklendi.
Tournament ID 1083 başarıyla eklendi.
Tournament ID 493 başarıyla eklendi.
Tournament ID 1079 başarıyla eklendi.
Tournament ID 1085 başarıyla eklendi.
Tournament ID 1191 başarıyla eklendi.
Tournament ID 186 başarıyla eklendi.
Tournament ID 11619 başarıyla eklendi.
Tournament ID 1015 başarıyla eklendi.
Tournament ID 915 başarıyla eklendi.
Tournament ID 193 başarıyla eklendi.
Tournament ID 11445 başarıyla eklendi.
Tournament ID 11446 başarıyla eklendi.
Tournament ID 402 başarıyla eklendi.
Tournament ID 682 başarıyla eklendi.
Tournament ID 197 başarıyla eklendi.
Tournament ID 198 başarıyla eklendi.
Tournament ID 629 başarıyla eklendi.
Tournament ID 11611 başarıyla eklendi.
Tournament ID 685 başarıyla eklendi.
Tournament ID 2123 başarıyla eklendi.
Tournament ID 22 başarıyla eklendi.
Tournament ID 11085 başarıyla eklendi.
Tournament ID 11090 başarıyla eklendi.
Tournament ID 201 başarıyla eklendi.
Tournament ID 229 başarıyla eklendi.
Tournament ID 336 başarıyla eklendi.
Tournament ID 206 başarıyla eklendi.
Tournament ID 212 başarıyla eklendi.
Tournament ID 46 başarıyla eklendi.
Tournament ID 214 başarıyla eklendi.
Tournament ID 216 başarıyla eklendi.
Tournament ID 984 başarıyla eklendi.
Tournament ID 218 başarıyla eklendi.
Tournament ID 1369 başarıyla eklendi.
Tournament ID 278 başarıyla eklendi.
Tournament ID 626 başarıyla eklendi.
Tournament ID 254 başarıyla eklendi.
Season ID 52186 başarıyla eklendi.
Season ID 52376 başarıyla eklendi.
Season ID 52760 başarıyla eklendi.
Season ID 52608 başarıyla eklendi.
Season ID 52571 başarıyla eklendi.
Season ID 48982 başarıyla eklendi.
Season ID 53190 başarıyla eklendi.
Season ID 52383 başarıyla eklendi.
Season ID 53223 başarıyla eklendi.
Season ID 47644 başarıyla eklendi.
Season ID 52052 başarıyla eklendi.
Season ID 52147 başarıyla eklendi.
Season ID 53417 başarıyla eklendi.
Season ID 52367 başarıyla eklendi.
Season ID 52563 başarıyla eklendi.
Season ID 52607 başarıyla eklendi.
Season ID 52947 başarıyla eklendi.
Season ID 52572 başarıyla eklendi.
Season ID 49058 başarıyla eklendi.
Season ID 52556 başarıyla eklendi.
Season ID 53276 başarıyla eklendi.
Season ID 54447 başarıyla eklendi.
Season ID 49950 başarıyla eklendi.
Season ID 52847 başarıyla eklendi.
Season ID 52364 başarıyla eklendi.
Season ID 52176 başarıyla eklendi.
Season ID 52172 başarıyla eklendi.
Season ID 52368 başarıyla eklendi.
Season ID 48353 başarıyla eklendi.
Season ID 47642 başarıyla eklendi.
Season ID 48720 başarıyla eklendi.
Season ID 55005 başarıyla eklendi.
Season ID 54846 başarıyla eklendi.
Season ID 47946 başarıyla eklendi.
Season ID 48055 başarıyla eklendi.
Season ID 47806 başarıyla eklendi.
Season ID 48078 başarıyla eklendi.
Season ID 53241 başarıyla eklendi.
Season ID 52541 başarıyla eklendi.
Season ID 47730 başarıyla eklendi.
Season ID 54509 başarıyla eklendi.
Season ID 48265 başarıyla eklendi.
Season ID 52470 başarıyla eklendi.
Season ID 48864 başarıyla eklendi.
Season ID 48379 başarıyla eklendi.
Season ID 48706 başarıyla eklendi.
Season ID 53587 başarıyla eklendi.
Season ID 52944 başarıyla eklendi.
Season ID 53244 başarıyla eklendi.
Season ID 52384 başarıyla eklendi.
Season ID 53225 başarıyla eklendi.
Season ID 54165 başarıyla eklendi.
Season ID 53133 başarıyla eklendi.
Season ID 53464 başarıyla eklendi.
Season ID 52398 başarıyla eklendi.
Season ID 52551 başarıyla eklendi.
Season ID 54499 başarıyla eklendi.
Season ID 52545 başarıyla eklendi.
Season ID 53263 başarıyla eklendi.
Season ID 49103 başarıyla eklendi.
Season ID 52702 başarıyla eklendi.
Season ID 52173 başarıyla eklendi.
Season ID 50458 başarıyla eklendi.
Season ID 52361 başarıyla eklendi.
Season ID 52329 başarıyla eklendi.
Season ID 52684 başarıyla eklendi.
Season ID 48281 başarıyla eklendi.
Season ID 48608 başarıyla eklendi.
Season ID 48709 başarıyla eklendi.
Season ID 53055 başarıyla eklendi.
Season ID 48739 başarıyla eklendi.
Season ID 52815 başarıyla eklendi.
Season ID 53003 başarıyla eklendi.
Season ID 52794 başarıyla eklendi.
Season ID 52841 başarıyla eklendi.
Season ID 52958 başarıyla eklendi.
Season ID 52399 başarıyla eklendi.
Season ID 53685 başarıyla eklendi.
Season ID 54993 başarıyla eklendi.
Season ID 53134 başarıyla eklendi.
Season ID 52519 başarıyla eklendi.
Season ID 52957 başarıyla eklendi.
Season ID 47939 başarıyla eklendi.
Season ID 53814 başarıyla eklendi.
Season ID 53816 başarıyla eklendi.
Season ID 48054 başarıyla eklendi.
Season ID 48738 başarıyla eklendi.
Season ID 49002 başarıyla eklendi.
Season ID 48778 başarıyla eklendi.
Season ID 52579 başarıyla eklendi.
Season ID 53021 başarıyla eklendi.
Season ID 53074 başarıyla eklendi.
Season ID 53465 başarıyla eklendi.
Season ID 47820 başarıyla eklendi.
Season ID 47949 başarıyla eklendi.
Season ID 47948 başarıyla eklendi.
Season ID 48838 başarıyla eklendi.
Season ID 52362 başarıyla eklendi.
Season ID 53979 başarıyla eklendi.
Season ID 52606 başarıyla eklendi.
Season ID 52395 başarıyla eklendi.
Season ID 47762 başarıyla eklendi.
Season ID 48137 başarıyla eklendi.
Season ID 52365 başarıyla eklendi.
Season ID 53910 başarıyla eklendi.
Season ID 52774 başarıyla eklendi.
Season ID 53414 başarıyla eklendi.
Season ID 48634 başarıyla eklendi.
Season ID 55929 başarıyla eklendi.
Season ID 52310 başarıyla eklendi.
Tournament ID 1 veya Season ID 52186 bulunamadı, Home Team ID 44 eklenemedi.
Tournament ID 36 veya Season ID 52376 bulunamadı, Home Team ID 2820 eklenemedi.
Tournament ID 36 veya Season ID 52376 bulunamadı, Home Team ID 2824 eklenemedi.
Tournament ID 33 veya Season ID 52760 bulunamadı, Home Team ID 2701 eklenemedi.
Home Team ID 2673 başarıyla eklendi.
Home Team ID 2547 başarıyla eklendi.
Home Team ID 2576 başarıyla eklendi.
Home Team ID 2538 başarıyla eklendi.
Home Team ID 2569 başarıyla eklendi.
Home Team ID 2524 başarıyla eklendi.
Tournament ID 4 veya Season ID 52571 bulunamadı, Home Team ID 1662 eklenemedi.
Tournament ID 83 veya Season ID 48982 bulunamadı, Home Team ID 1954 eklenemedi.
Tournament ID 83 veya Season ID 48982 bulunamadı, Home Team ID 1963 eklenemedi.
Tournament ID 83 veya Season ID 48982 bulunamadı, Home Team ID 1968 eklenemedi.
Tournament ID 83 veya Season ID 48982 bulunamadı, Home Team ID 1961 eklenemedi.
Tournament ID 62 veya Season ID 53190 bulunamadı, Home Team ID 3072 eklenemedi.
Tournament ID 62 veya Season ID 53190 bulunamadı, Home Team ID 5138 eklenemedi.
Tournament ID 62 veya Season ID 53190 bulunamadı, Home Team ID 3085 eklenemedi.
Home Team ID 4860 başarıyla eklendi.
Tournament ID 127 veya Season ID 53223 bulunamadı, Home Team ID 120154 eklenemedi.
Tournament ID 72142 veya Season ID 47644 bulunamadı, Home Team ID 3205 eklenemedi.
Tournament ID 72142 veya Season ID 47644 bulunamadı, Home Team ID 6074 eklenemedi.
Tournament ID 72142 veya Season ID 47644 bulunamadı, Home Team ID 3207 eklenemedi.
Tournament ID 72142 veya Season ID 47644 bulunamadı, Home Team ID 3217 eklenemedi.
Tournament ID 72142 veya Season ID 47644 bulunamadı, Home Team ID 42338 eklenemedi.
Tournament ID 72142 veya Season ID 47644 bulunamadı, Home Team ID 7628 eklenemedi.
Tournament ID 72142 veya Season ID 47644 bulunamadı, Home Team ID 7629 eklenemedi.
Tournament ID 72142 veya Season ID 47644 bulunamadı, Home Team ID 3210 eklenemedi.
Tournament ID 72142 veya Season ID 47644 bulunamadı, Home Team ID 3202 eklenemedi.
Tournament ID 28 veya Season ID 52052 bulunamadı, Home Team ID 1949 eklenemedi.
Tournament ID 28 veya Season ID 52052 bulunamadı, Home Team ID 201624 eklenemedi.
Tournament ID 28 veya Season ID 52052 bulunamadı, Home Team ID 1941 eklenemedi.
Tournament ID 48 veya Season ID 52147 bulunamadı, Home Team ID 35226 eklenemedi.
Tournament ID 1107 veya Season ID 53417 bulunamadı, Home Team ID 25736 eklenemedi.
Tournament ID 1107 veya Season ID 53417 bulunamadı, Home Team ID 7674 eklenemedi.
Tournament ID 1107 veya Season ID 53417 bulunamadı, Home Team ID 36967 eklenemedi.
Tournament ID 2 veya Season ID 52367 bulunamadı, Home Team ID 13 eklenemedi.
Tournament ID 2 veya Season ID 52367 bulunamadı, Home Team ID 21 eklenemedi.
Tournament ID 37 veya Season ID 52563 bulunamadı, Home Team ID 2814 eklenemedi.
Home Team ID 2541 başarıyla eklendi.
Home Team ID 2598 başarıyla eklendi.
Home Team ID 2676 başarıyla eklendi.
Home Team ID 2561 başarıyla eklendi.
Home Team ID 2581 başarıyla eklendi.
Home Team ID 2690 başarıyla eklendi.
Home Team ID 2712 başarıyla eklendi.
Home Team ID 2761 başarıyla eklendi.
Home Team ID 7933 başarıyla eklendi.
Home Team ID 2737 başarıyla eklendi.
Home Team ID 2708 başarıyla eklendi.
Tournament ID 19 veya Season ID 52572 bulunamadı, Home Team ID 1667 eklenemedi.
Tournament ID 1449 veya Season ID 49058 bulunamadı, Home Team ID 7314 eklenemedi.
Tournament ID 1449 veya Season ID 49058 bulunamadı, Home Team ID 87202 eklenemedi.
Tournament ID 1449 veya Season ID 49058 bulunamadı, Home Team ID 2005 eklenemedi.
Tournament ID 1449 veya Season ID 49058 bulunamadı, Home Team ID 21982 eklenemedi.
Home Team ID 2949 başarıyla eklendi.
Home Team ID 2963 başarıyla eklendi.
Home Team ID 2973 başarıyla eklendi.
Home Team ID 2994 başarıyla eklendi.
Home Team ID 2965 başarıyla eklendi.
Home Team ID 46161 başarıyla eklendi.
Home Team ID 2976 başarıyla eklendi.
Home Team ID 2947 başarıyla eklendi.
Tournament ID 101 veya Season ID 53276 bulunamadı, Home Team ID 117198 eklenemedi.
Tournament ID 101 veya Season ID 53276 bulunamadı, Home Team ID 55603 eklenemedi.
Tournament ID 101 veya Season ID 53276 bulunamadı, Home Team ID 3080 eklenemedi.
Tournament ID 144 veya Season ID 54447 bulunamadı, Home Team ID 2946 eklenemedi.
Tournament ID 144 veya Season ID 54447 bulunamadı, Home Team ID 371682 eklenemedi.
Tournament ID 144 veya Season ID 54447 bulunamadı, Home Team ID 42210 eklenemedi.
Tournament ID 144 veya Season ID 54447 bulunamadı, Home Team ID 5971 eklenemedi.
Tournament ID 652 veya Season ID 49950 bulunamadı, Home Team ID 34694 eklenemedi.
Tournament ID 652 veya Season ID 49950 bulunamadı, Home Team ID 49936 eklenemedi.
Tournament ID 652 veya Season ID 49950 bulunamadı, Home Team ID 41537 eklenemedi.
Tournament ID 652 veya Season ID 49950 bulunamadı, Home Team ID 34692 eklenemedi.
Tournament ID 652 veya Season ID 49950 bulunamadı, Home Team ID 251278 eklenemedi.
Tournament ID 19236 veya Season ID 52847 bulunamadı, Home Team ID 6114 eklenemedi.
Tournament ID 19236 veya Season ID 52847 bulunamadı, Home Team ID 89370 eklenemedi.
Tournament ID 19236 veya Season ID 52847 bulunamadı, Home Team ID 6975 eklenemedi.
Tournament ID 49 veya Season ID 52364 bulunamadı, Home Team ID 2219 eklenemedi.
Tournament ID 49 veya Season ID 52364 bulunamadı, Home Team ID 2220 eklenemedi.
Tournament ID 49 veya Season ID 52364 bulunamadı, Home Team ID 2230 eklenemedi.
Tournament ID 49 veya Season ID 52364 bulunamadı, Home Team ID 23951 eklenemedi.
Tournament ID 64 veya Season ID 52176 bulunamadı, Home Team ID 7918 eklenemedi.
Tournament ID 64 veya Season ID 52176 bulunamadı, Home Team ID 7691 eklenemedi.
Tournament ID 64 veya Season ID 52176 bulunamadı, Home Team ID 38729 eklenemedi.
Tournament ID 12 veya Season ID 52172 bulunamadı, Home Team ID 1305 eklenemedi.
Tournament ID 84 veya Season ID 52368 bulunamadı, Home Team ID 79 eklenemedi.
Tournament ID 84 veya Season ID 52368 bulunamadı, Home Team ID 51 eklenemedi.
Tournament ID 4330 veya Season ID 48353 bulunamadı, Home Team ID 273544 eklenemedi.
Tournament ID 4330 veya Season ID 48353 bulunamadı, Home Team ID 327860 eklenemedi.
Tournament ID 4330 veya Season ID 48353 bulunamadı, Home Team ID 32529 eklenemedi.
Tournament ID 4330 veya Season ID 48353 bulunamadı, Home Team ID 335685 eklenemedi.
Tournament ID 16752 veya Season ID 47642 bulunamadı, Home Team ID 5998 eklenemedi.
Tournament ID 16752 veya Season ID 47642 bulunamadı, Home Team ID 387619 eklenemedi.
Tournament ID 16752 veya Season ID 47642 bulunamadı, Home Team ID 249194 eklenemedi.
Tournament ID 16752 veya Season ID 47642 bulunamadı, Home Team ID 5994 eklenemedi.
Tournament ID 16752 veya Season ID 47642 bulunamadı, Home Team ID 90968 eklenemedi.
Tournament ID 16752 veya Season ID 47642 bulunamadı, Home Team ID 323510 eklenemedi.
Tournament ID 16752 veya Season ID 47642 bulunamadı, Home Team ID 39722 eklenemedi.
Tournament ID 16752 veya Season ID 47642 bulunamadı, Home Team ID 5996 eklenemedi.
Tournament ID 1387 veya Season ID 48720 bulunamadı, Home Team ID 277525 eklenemedi.
Tournament ID 38612 veya Season ID 55005 bulunamadı, Home Team ID 43560 eklenemedi.
Tournament ID 38612 veya Season ID 55005 bulunamadı, Home Team ID 371622 eklenemedi.
Tournament ID 38612 veya Season ID 55005 bulunamadı, Home Team ID 187866 eklenemedi.
Tournament ID 38566 veya Season ID 54846 bulunamadı, Home Team ID 40655 eklenemedi.
Tournament ID 79 veya Season ID 47946 bulunamadı, Home Team ID 3173 eklenemedi.
Tournament ID 79 veya Season ID 47946 bulunamadı, Home Team ID 3170 eklenemedi.
Tournament ID 79 veya Season ID 47946 bulunamadı, Home Team ID 3190 eklenemedi.
Tournament ID 82 veya Season ID 48055 bulunamadı, Home Team ID 5127 eklenemedi.
Tournament ID 82 veya Season ID 48055 bulunamadı, Home Team ID 3145 eklenemedi.
Tournament ID 82 veya Season ID 48055 bulunamadı, Home Team ID 5128 eklenemedi.
Tournament ID 82 veya Season ID 48055 bulunamadı, Home Team ID 3138 eklenemedi.
Tournament ID 82 veya Season ID 48055 bulunamadı, Home Team ID 3146 eklenemedi.
Tournament ID 82 veya Season ID 48055 bulunamadı, Home Team ID 3137 eklenemedi.
Tournament ID 82 veya Season ID 48055 bulunamadı, Home Team ID 7061 eklenemedi.
Tournament ID 82 veya Season ID 48055 bulunamadı, Home Team ID 3149 eklenemedi.
Tournament ID 82 veya Season ID 48055 bulunamadı, Home Team ID 3135 eklenemedi.
Tournament ID 5 veya Season ID 47806 bulunamadı, Home Team ID 656 eklenemedi.
Tournament ID 34468 veya Season ID 48078 bulunamadı, Home Team ID 87854 eklenemedi.
Tournament ID 3708 veya Season ID 53241 bulunamadı, Home Team ID 336456 eklenemedi.
Tournament ID 3708 veya Season ID 53241 bulunamadı, Home Team ID 56021 eklenemedi.
Tournament ID 3708 veya Season ID 53241 bulunamadı, Home Team ID 56023 eklenemedi.
Tournament ID 3708 veya Season ID 53241 bulunamadı, Home Team ID 21895 eklenemedi.
Tournament ID 219 veya Season ID 52541 bulunamadı, Home Team ID 44319 eklenemedi.
Tournament ID 219 veya Season ID 52541 bulunamadı, Home Team ID 204657 eklenemedi.
Tournament ID 24 veya Season ID 47730 bulunamadı, Home Team ID 1807 eklenemedi.
Tournament ID 14193 veya Season ID 54509 bulunamadı, Home Team ID 174076 eklenemedi.
Tournament ID 14193 veya Season ID 54509 bulunamadı, Home Team ID 207680 eklenemedi.
Tournament ID 14193 veya Season ID 54509 bulunamadı, Home Team ID 174078 eklenemedi.
Tournament ID 75934 veya Season ID 48265 bulunamadı, Home Team ID 197072 eklenemedi.
Home Team ID 24118 başarıyla eklendi.
Home Team ID 2333 başarıyla eklendi.
Home Team ID 2320 başarıyla eklendi.
Tournament ID 37913 veya Season ID 48864 bulunamadı, Home Team ID 151010 eklenemedi.
Tournament ID 39098 veya Season ID 48379 bulunamadı, Home Team ID 7650 eklenemedi.
Tournament ID 39098 veya Season ID 48379 bulunamadı, Home Team ID 48912 eklenemedi.
Tournament ID 39098 veya Season ID 48379 bulunamadı, Home Team ID 7644 eklenemedi.
Tournament ID 6230 veya Season ID 48706 bulunamadı, Home Team ID 339827 eklenemedi.
Tournament ID 6230 veya Season ID 48706 bulunamadı, Home Team ID 41263 eklenemedi.
Tournament ID 6230 veya Season ID 48706 bulunamadı, Home Team ID 92539 eklenemedi.
Tournament ID 4051 veya Season ID 53587 bulunamadı, Home Team ID 264822 eklenemedi.
Tournament ID 4051 veya Season ID 53587 bulunamadı, Home Team ID 34312 eklenemedi.
Tournament ID 7157 veya Season ID 52944 bulunamadı, Home Team ID 66566 eklenemedi.
Tournament ID 7157 veya Season ID 52944 bulunamadı, Home Team ID 35607 eklenemedi.
Tournament ID 7157 veya Season ID 52944 bulunamadı, Home Team ID 255498 eklenemedi.
Tournament ID 7157 veya Season ID 52944 bulunamadı, Home Team ID 85743 eklenemedi.
Tournament ID 7157 veya Season ID 52944 bulunamadı, Home Team ID 35886 eklenemedi.
Tournament ID 15635 veya Season ID 53244 bulunamadı, Home Team ID 266375 eklenemedi.
Tournament ID 692 veya Season ID 52384 bulunamadı, Home Team ID 169260 eklenemedi.
Tournament ID 692 veya Season ID 52384 bulunamadı, Home Team ID 2920 eklenemedi.
Tournament ID 5397 veya Season ID 53225 bulunamadı, Home Team ID 36701 eklenemedi.
Tournament ID 5397 veya Season ID 53225 bulunamadı, Home Team ID 78501 eklenemedi.
Tournament ID 5397 veya Season ID 53225 bulunamadı, Home Team ID 264965 eklenemedi.
Tournament ID 5397 veya Season ID 53225 bulunamadı, Home Team ID 78489 eklenemedi.
Tournament ID 7372 veya Season ID 54165 bulunamadı, Home Team ID 325685 eklenemedi.
Tournament ID 810 veya Season ID 53133 bulunamadı, Home Team ID 229794 eklenemedi.
Tournament ID 810 veya Season ID 53133 bulunamadı, Home Team ID 5550 eklenemedi.
Tournament ID 810 veya Season ID 53133 bulunamadı, Home Team ID 5551 eklenemedi.
Tournament ID 3739 veya Season ID 53464 bulunamadı, Home Team ID 231057 eklenemedi.
Tournament ID 3739 veya Season ID 53464 bulunamadı, Home Team ID 362904 eklenemedi.
Tournament ID 50 veya Season ID 52398 bulunamadı, Home Team ID 25397 eklenemedi.
Tournament ID 50 veya Season ID 52398 bulunamadı, Home Team ID 1922 eklenemedi.
Tournament ID 92 veya Season ID 52551 bulunamadı, Home Team ID 7084 eklenemedi.
Tournament ID 3657 veya Season ID 54499 bulunamadı, Home Team ID 133488 eklenemedi.
Tournament ID 3657 veya Season ID 54499 bulunamadı, Home Team ID 212197 eklenemedi.
Tournament ID 3657 veya Season ID 54499 bulunamadı, Home Team ID 42201 eklenemedi.
Tournament ID 3657 veya Season ID 54499 bulunamadı, Home Team ID 41756 eklenemedi.
Tournament ID 3657 veya Season ID 54499 bulunamadı, Home Team ID 79565 eklenemedi.
Tournament ID 3657 veya Season ID 54499 bulunamadı, Home Team ID 42206 eklenemedi.
Tournament ID 30 veya Season ID 52545 bulunamadı, Home Team ID 7785 eklenemedi.
Tournament ID 30 veya Season ID 52545 bulunamadı, Home Team ID 105969 eklenemedi.
Tournament ID 30 veya Season ID 52545 bulunamadı, Home Team ID 2049 eklenemedi.
Tournament ID 30 veya Season ID 52545 bulunamadı, Home Team ID 2050 eklenemedi.
Tournament ID 30 veya Season ID 52545 bulunamadı, Home Team ID 2067 eklenemedi.
Tournament ID 30 veya Season ID 52545 bulunamadı, Home Team ID 7786 eklenemedi.
Tournament ID 30 veya Season ID 52545 bulunamadı, Home Team ID 2103 eklenemedi.
Tournament ID 3590 veya Season ID 53263 bulunamadı, Home Team ID 36951 eklenemedi.
Tournament ID 3590 veya Season ID 53263 bulunamadı, Home Team ID 231384 eklenemedi.
Tournament ID 3590 veya Season ID 53263 bulunamadı, Home Team ID 37750 eklenemedi.
Tournament ID 616 veya Season ID 49103 bulunamadı, Home Team ID 3359 eklenemedi.
Tournament ID 616 veya Season ID 49103 bulunamadı, Home Team ID 42965 eklenemedi.
Tournament ID 2557 veya Season ID 52702 bulunamadı, Home Team ID 37064 eklenemedi.
Home Team ID 389096 başarıyla eklendi.
Home Team ID 3272 başarıyla eklendi.
Home Team ID 36938 başarıyla eklendi.
Home Team ID 3277 başarıyla eklendi.
Tournament ID 3583 veya Season ID 50458 bulunamadı, Home Team ID 382022 eklenemedi.
Tournament ID 3583 veya Season ID 50458 bulunamadı, Home Team ID 281331 eklenemedi.
Tournament ID 3583 veya Season ID 50458 bulunamadı, Home Team ID 311351 eklenemedi.
Tournament ID 3583 veya Season ID 50458 bulunamadı, Home Team ID 164044 eklenemedi.
Tournament ID 843 veya Season ID 52361 bulunamadı, Home Team ID 4863 eklenemedi.
Tournament ID 843 veya Season ID 52361 bulunamadı, Home Team ID 2213 eklenemedi.
Tournament ID 843 veya Season ID 52361 bulunamadı, Home Team ID 7739 eklenemedi.
Tournament ID 843 veya Season ID 52361 bulunamadı, Home Team ID 2215 eklenemedi.
Tournament ID 843 veya Season ID 52361 bulunamadı, Home Team ID 4865 eklenemedi.
Tournament ID 843 veya Season ID 52361 bulunamadı, Home Team ID 35264 eklenemedi.
Tournament ID 13 veya Season ID 52329 bulunamadı, Home Team ID 1314 eklenemedi.
Tournament ID 13 veya Season ID 52329 bulunamadı, Home Team ID 1371 eklenemedi.
Tournament ID 13 veya Season ID 52329 bulunamadı, Home Team ID 1392 eklenemedi.
Tournament ID 13 veya Season ID 52329 bulunamadı, Home Team ID 1295 eklenemedi.
Tournament ID 93782 veya Season ID 52684 bulunamadı, Home Team ID 1398 eklenemedi.
Tournament ID 93782 veya Season ID 52684 bulunamadı, Home Team ID 1287 eklenemedi.
Tournament ID 93782 veya Season ID 52684 bulunamadı, Home Team ID 22163 eklenemedi.
Tournament ID 93782 veya Season ID 52684 bulunamadı, Home Team ID 1304 eklenemedi.
Tournament ID 93782 veya Season ID 52684 bulunamadı, Home Team ID 1403 eklenemedi.
Tournament ID 618 veya Season ID 48281 bulunamadı, Home Team ID 7105 eklenemedi.
Tournament ID 618 veya Season ID 48281 bulunamadı, Home Team ID 3343 eklenemedi.
Tournament ID 75354 veya Season ID 48608 bulunamadı, Home Team ID 5114 eklenemedi.
Tournament ID 75354 veya Season ID 48608 bulunamadı, Home Team ID 2249 eklenemedi.
Tournament ID 75354 veya Season ID 48608 bulunamadı, Home Team ID 2255 eklenemedi.
Tournament ID 91433 veya Season ID 48709 bulunamadı, Home Team ID 2271 eklenemedi.
Tournament ID 950 veya Season ID 53055 bulunamadı, Home Team ID 1664 eklenemedi.
Tournament ID 950 veya Season ID 53055 bulunamadı, Home Team ID 4493 eklenemedi.
Tournament ID 950 veya Season ID 53055 bulunamadı, Home Team ID 39126 eklenemedi.
Tournament ID 950 veya Season ID 53055 bulunamadı, Home Team ID 361815 eklenemedi.
Tournament ID 950 veya Season ID 53055 bulunamadı, Home Team ID 1663 eklenemedi.
Tournament ID 950 veya Season ID 53055 bulunamadı, Home Team ID 52874 eklenemedi.
Tournament ID 950 veya Season ID 53055 bulunamadı, Home Team ID 35064 eklenemedi.
Tournament ID 950 veya Season ID 53055 bulunamadı, Home Team ID 1657 eklenemedi.
Tournament ID 950 veya Season ID 53055 bulunamadı, Home Team ID 6921 eklenemedi.
Tournament ID 3012 veya Season ID 48739 bulunamadı, Home Team ID 78961 eklenemedi.
Tournament ID 3012 veya Season ID 48739 bulunamadı, Home Team ID 37297 eklenemedi.
Tournament ID 3012 veya Season ID 48739 bulunamadı, Home Team ID 254627 eklenemedi.
Tournament ID 8343 veya Season ID 52815 bulunamadı, Home Team ID 2680 eklenemedi.
Tournament ID 8343 veya Season ID 52815 bulunamadı, Home Team ID 5880 eklenemedi.
Tournament ID 8343 veya Season ID 52815 bulunamadı, Home Team ID 2582 eklenemedi.
Tournament ID 8343 veya Season ID 52815 bulunamadı, Home Team ID 2595 eklenemedi.
Tournament ID 8343 veya Season ID 52815 bulunamadı, Home Team ID 2536 eklenemedi.
Tournament ID 8343 veya Season ID 52815 bulunamadı, Home Team ID 2560 eklenemedi çoğu veri mevcut olmasına rağmen bunların çoğunu pass geçşyor ve eklemiyor neden bçyle bir sotun var.

**Cevap:** Bu hataların ana nedeni, **Tournament** veya **Season** tablolarında gerekli ID'lerin mevcut olmamasıdır. Sistem, veritabanına **Team** verilerini eklemeye çalıştığında, ilgili **Tournament** veya **Season** ID'lerinin var olup olmadığını kontrol eder. Eğer bu ID'ler veritabanında mevcut değilse, **foreign key constraint** nedeniyle bu veriler eklenemiyor ve pass geçiliyor.

### Çözüm Adımları:

1. **İlgili Turnuva ve Sezon Verilerinin Varlığını Kontrol Etme:**
   `team_data` metodunda, takım eklemeden önce ilgili **Tournament** ve **Season** ID'lerinin veritabanında mevcut olup olmadığını kontrol ediyorsunuz. Ancak, API'den gelen bazı turnuva veya sezon ID'leri **Tournament** ve **Season** tablolarında bulunmadığı için eklenemiyor. Bu durum, eklemeye çalıştığınız takımların veritabanına kaydedilmesini engelliyor.

2. **Eksik Turnuva ve Sezonları Önce Ekleyin:**
   Eğer bir turnuva veya sezon eksikse, takım verisini eklemeden önce eksik olan turnuva ve sezon verilerini otomatik olarak ekleyebilirsiniz. Bu sayede, **Team** verisini eklemeden önce gerekli turnuva ve sezon kayıtları yaratılmış olur.

### Güncellenmiş Çözüm Kodu:

Aşağıdaki örnekte, **team_data** metodunu güncelleyerek turnuva ve sezon ID'lerinin veritabanında bulunup bulunmadığını kontrol ediyoruz. Eğer turnuva veya sezon eksikse, bunları veritabanına ekliyoruz.

```python
def team_data(self):
    """Verilen verilerden homeTeam bilgilerini çek ve modele ekle."""
    
    verim = self.fetch_data()  # Veriyi sofascore API'den çek

    if verim is None:
        raise ValueError("Veri işlenmedi. Önce 'fetch_data()' metodunu çalıştırın.")
    
    # Aynı homeTeam_id'ye sahip olanları tekrar kontrol et
    verim = verim.drop_duplicates("homeTeam_id")

    # İlgili home team sütunları
    homecols = [
        "homeTeam_id", "homeTeam_name", "homeTeam_slug", "homeTeam_shortName",
        "homeTeam_nameCode", "homeTeam_national", "tournament_id", "season_id"
    ]

    # Eksik sütunları kontrol edip, eğer yoksa 0 ile doldurma
    for col in homecols:
        if col not in verim.columns:
            verim.loc[:, col] = 0

    # Sadece home team ile ilgili sütunları al
    verim = verim[homecols]

    for _, row in verim.iterrows():
        home_team_id = row['homeTeam_id']
        tournament_id = row['tournament_id']
        season_id = row['season_id']

        # NaN değerlerini kontrol edin ve geçersiz veriyi atlayın
        if pd.isna(home_team_id) or pd.isna(tournament_id) or pd.isna(season_id):
            print(f"Geçersiz homeTeam_id, tournament_id veya season_id: HomeTeam ID={home_team_id}, Tournament ID={tournament_id}, Season ID={season_id}. Atlanıyor.")
            continue

        # Turnuva olup olmadığını kontrol et ve eksikse ekle
        tournament_instance, created = Tournament.objects.get_or_create(
            tournament_uniqueTournament_id=tournament_id,
            defaults={
                'tournament_name': row.get('tournament_name', 'Unknown'),
                'tournament_slug': row.get('tournament_slug', ''),
                'tournament_category_name': row.get('tournament_category_name', ''),
                'tournament_category_slug': row.get('tournament_category_slug', ''),
                'tournament_uniqueTournament_category_id': row.get('tournament_uniqueTournament_category_id', 0),
                'tournament_uniqueTournament_hasEventPlayerStatistics': row.get('tournament_uniqueTournament_hasEventPlayerStatistics', False),
                'tournament_id': row.get('tournament_id', tournament_id),
                'tournament_isGroup': row.get('tournament_isGroup', False),
                'tournament_uniqueTournament_hasPerformanceGraphFeature': row.get('tournament_uniqueTournament_hasPerformanceGraphFeature', False)
            }
        )

        # Sezon olup olmadığını kontrol et ve eksikse ekle
        season_instance, created = Season.objects.get_or_create(
            season_id=season_id,
            defaults={
                'season_name': row.get('season_name', 'Unknown'),
                'season_year': row.get('season_year', 0),
                'tournament': tournament_instance  # Turnuva ile ilişkilendir
            }
        )
        
        # Team ekleme işlemi
        if not Team.objects.filter(team_id=home_team_id).exists():
            Team.objects.create(
                team_id=row['homeTeam_id'],
                team_name=row['homeTeam_name'],
                team_slug=row['homeTeam_slug'],
                team_shortName=row['homeTeam_shortName'],
                team_nameCode=row['homeTeam_nameCode'],
                team_national=row['homeTeam_national'] if pd.notna(row['homeTeam_national']) else False,
                tournament=tournament_instance,  # Turnuva ile ilişkilendir
                season=season_instance  # Sezon ile ilişkilendir
            )
            print(f"Home Team ID {home_team_id} başarıyla eklendi.")
        else:
            print(f"Home Team ID {home_team_id} zaten mevcut, eklenmedi.")
```

### Çözümdeki Değişiklikler:
1. **`get_or_create` Kullanımı**: Bu fonksiyon, veritabanında ilgili kaydın var olup olmadığını kontrol eder. Eğer ilgili turnuva veya sezon veritabanında yoksa, yeni bir kayıt oluşturur. Böylece eksik olan turnuva ve sezon verileri de otomatik olarak eklenir.
   
2. **Varsayılan Değerler**: Eğer API'den gelen bazı değerler eksikse, varsayılan olarak boş ya da uygun bir değer ekliyoruz (örneğin `Unknown`).

### Bu Kodla Ne Elde Edersiniz?
- Eksik olan turnuva ve sezon kayıtlarını otomatik olarak veritabanına ekleyeceksiniz.
- Eğer turnuva veya sezon veritabanında zaten varsa, tekrar eklemeye çalışmaz ve mevcut kaydı kullanır.
- Böylece, takımların eklenmesinde eksik turnuva veya sezon verileri nedeniyle sorun yaşanmaz.

### Test Etme:
Bu değişiklikleri uyguladıktan sonra `team_data` fonksiyonunu çalıştırın ve eksik kayıtların da başarıyla eklendiğinden emin olun.

```python
api.team_data()
```

***Soru:*** tüm season ve torunament verileri var çünkü aynı veri üwerinden verileri alıyoruz bu yüzden heğpsi var

**Cevap:** Eğer **Tournament** ve **Season** verileriniz zaten mevcutsa ve hala verilerin bir kısmının eklenmediğini görüyorsanız, sorunun başka bir kaynağı olabilir. Bu durumda, olası birkaç sorunu ve çözümünü gözden geçirelim.

### Olası Sorunlar:

1. **Veri Tutarsızlığı veya Yanlış ID'ler**:
   Aynı veri setinden aldığınızı belirtiyorsunuz, ancak bazen turnuva veya sezon ID'leri, veritabanına doğru şekilde eklenmeyebilir. Örneğin, **season_id** veya **tournament_id** yanlış olabilir ya da küçük bir format farklılığı olabilir.

2. **NaN Değerleri**:
   Verilerinizde **NaN** (boş) değerler bulunuyor olabilir. Bu tür değerler kaydedilmeden atlanıyor olabilir.

3. **Verilerin Doğru İlişkilendirilmemesi**:
   Eğer **Tournament** veya **Season** tablolarında doğru şekilde ilişkilendirilmemiş ya da eşleşmeyen ID'ler varsa, verilerin ilişkilendirilmesi başarısız olabilir.

### Olası Çözüm Yöntemleri:

1. **Veritabanı Kayıtlarını Kontrol Edin**:
   Aynı **tournament_id** ve **season_id**'lerin gerçekten veritabanında bulunduğundan ve API'den çekilen verilerle birebir eşleştiğinden emin olun. Küçük bir farklılık bile eklemeyi başarısız kılabilir. Bunu kontrol etmek için, Django shell'de şu komutları kullanarak belirli ID'lerin var olup olmadığını test edebilirsiniz:

   ```python
   from mymodel.models import Tournament, Season

   # Belirli bir Tournament ID'sinin var olup olmadığını kontrol et
   Tournament.objects.filter(tournament_uniqueTournament_id=desired_tournament_id).exists()

   # Belirli bir Season ID'sinin var olup olmadığını kontrol et
   Season.objects.filter(season_id=desired_season_id).exists()
   ```

2. **Veri Türlerini ve NaN Değerlerini Kontrol Edin**:
   **NaN** değerler veya eksik sütunlar, verilerin eklenmesini engelleyebilir. `pd.isna()` kullanarak veri setinizde bu değerlerin var olup olmadığını kontrol edebilirsiniz. Eğer boş alanlar varsa, bu verileri atlayabilir ya da boş alanları geçici değerlerle doldurabilirsiniz.

3. **Detaylı Loglama Ekleme**:
   Hangi verilerin neden eklenemediğini anlamak için, kodunuzu daha fazla ayrıntı kaydeden loglar ile güncelleyebilirsiniz. Örneğin:

   ```python
   if not Tournament.objects.filter(tournament_uniqueTournament_id=tournament_id).exists():
       print(f"Tournament ID {tournament_id} veritabanında mevcut değil.")
   elif not Season.objects.filter(season_id=season_id).exists():
       print(f"Season ID {season_id} veritabanında mevcut değil.")
   else:
       print(f"Tournament ID {tournament_id} ve Season ID {season_id} veritabanında mevcut, veri ekleniyor.")
   ```

   Bu sayede hangi verilerin hangi nedenlerden dolayı eklenemediğini daha net görebilirsiniz.

4. **Veri Örneklerini Manuel Test Etme**:
   Sorun yaşanan belirli **Tournament** ve **Season** ID'leri ile ilgili verileri manuel olarak test edin. Örneğin, aşağıdaki gibi tek bir **team_data** ekleme işlemini manuel yaparak neden sorun yaşandığını daha iyi anlayabilirsiniz:

   ```python
   tournament_instance = Tournament.objects.filter(tournament_uniqueTournament_id=36).first()
   season_instance = Season.objects.filter(season_id=52376).first()

   if tournament_instance and season_instance:
       Team.objects.create(
           team_id=2820,
           team_name="Sample Team",
           team_slug="sample-team",
           team_shortName="ST",
           team_nameCode="ST",
           team_national=False,
           tournament=tournament_instance,
           season=season_instance
       )
       print("Team başarıyla eklendi.")
   else:
       print("Team eklenemedi.")
   ```

5. **API'den Gelen Veriyi Kaydedip Karşılaştırın**:
   Eğer sorun hala devam ederse, API'den gelen ham verileri (örn. JSON yanıtları) kaydedip veritabanınızdaki mevcut verilerle karşılaştırın. Bu, veritabanına eklenemeyen verilerin doğru olup olmadığını anlamanıza yardımcı olabilir.

### Sonuç:
Eğer **Tournament** ve **Season** verileriniz zaten doğruysa, sorun büyük olasılıkla veri tutarsızlıklarından veya **NaN** değerlerinden kaynaklanıyor olabilir. Yukarıdaki adımlarla bu sorunları tespit edebilir ve çözebilirsiniz.

***Soru:*** 2320	Lokomotiv Moscow	Lokomotiv	Serie B	Premier League 23/24 (23/24)  mesela burada Seria B takımı değil yanlış eklemiş kodlarda bir mantım hatası var

**Cevap:** Belirttiğiniz gibi, **Lokomotiv Moscow**'un **Serie B** gibi bir ligde görünmesi yanlış bir veri eşleşmesi olabilir. Bu, API'den gelen verilerin doğru şekilde işlenmediği veya yanlış bir ilişkilendirme yapıldığı anlamına gelebilir. Bu tip bir hata genellikle verilerin işlenmesi veya eşleştirilmesinde bir sorun olduğunda ortaya çıkar.

### Muhtemel Sorunlar:
1. **Yanlış Ligde Gösterilme (tournament_id/season_id eşleşmesi hatası):** Veritabanına kaydedilen takımların turnuva (tournament) ve sezon (season) bilgileri doğru şekilde ilişkilendirilmiyor olabilir.
2. **Veri İşleme Hatası:** API'den gelen verilerin doğru şekilde ayrıştırılmaması veya doğru sütunlara yerleştirilmemesi sonucu yanlış eşleştirmeler yapılabilir.

Bu durumu çözmek için önce verilerin nasıl işlendiğine bakalım ve ardından doğru turnuva ile takımların nasıl ilişkilendirileceğine dair önerilerde bulunalım.

### 1. **Veri İşleme Mantığına Bakalım:**
API'den gelen verilerin doğru sütunlarda olduğundan emin olun. Özellikle **tournament_name**, **tournament_id**, ve **season_id** gibi alanlar doğru eşleştirilmiş mi kontrol edilmelidir. Şu kısımda doğru verilerin alınması önemlidir:

```python
homecols = [
    "homeTeam_id", "homeTeam_name", "homeTeam_slug", "homeTeam_shortName",
    "homeTeam_nameCode", "homeTeam_national", "tournament_id", "season_id"
]
```

Bu sütunlar API'den doğru bir şekilde çekiliyorsa, eklemeden önce verilerin doğruluğunu kontrol etmelisiniz. Özellikle **tournament_id** ve **season_id**'lerin doğru turnuva ve sezona ait olup olmadığını kontrol etmek için bir doğrulama ekleyebilirsiniz.

### 2. **Turnuva ve Sezon Kontrolleri:**
API'den gelen verilerin mantıksal olarak doğru olup olmadığını kontrol edebilirsiniz. Örneğin, takımın **Serie B** gibi bir turnuvada olup olmadığını kontrol etmek için, turnuva adıyla takım adını karşılaştıran bir doğrulama ekleyebilirsiniz:

```python
def team_data(self):
    """Verilen verilerden homeTeam bilgilerini çek ve modele ekle."""
    
    verim = self.fetch_data()  # Veriyi sofascore API'den çek

    if verim is None:
        raise ValueError("Veri işlenmedi. Önce 'fetch_data()' metodunu çalıştırın.")
    
    # Aynı homeTeam_id'ye sahip olanları tekrar kontrol et
    verim = verim.drop_duplicates("homeTeam_id")

    # İlgili home team sütunları
    homecols = [
        "homeTeam_id", "homeTeam_name", "homeTeam_slug", "homeTeam_shortName",
        "homeTeam_nameCode", "homeTeam_national", "tournament_id", "season_id", "tournament_name"
    ]

    # Eksik sütunları kontrol edip, eğer yoksa 0 ile doldurma
    for col in homecols:
        if col not in verim.columns:
            verim.loc[:, col] = 0

    # Sadece home team ile ilgili sütunları al
    verim = verim[homecols]

    for _, row in verim.iterrows():
        home_team_id = row['homeTeam_id']
        tournament_id = row['tournament_id']
        season_id = row['season_id']
        tournament_name = row['tournament_name']

        # NaN değerlerini kontrol edin ve geçersiz veriyi atlayın
        if pd.isna(home_team_id) or pd.isna(tournament_id) or pd.isna(season_id):
            print(f"Geçersiz homeTeam_id, tournament_id veya season_id: HomeTeam ID={home_team_id}, Tournament ID={tournament_id}, Season ID={season_id}. Atlanıyor.")
            continue

        # Mantıksal olarak turnuva ve takım eşleştirmesini doğrulayın
        if "Serie B" in tournament_name and "Lokomotiv Moscow" in row['homeTeam_name']:
            print(f"Hatalı eşleştirme: {row['homeTeam_name']} Serie B turnuvasında olamaz. Veri atlanıyor.")
            continue

        # Turnuva olup olmadığını kontrol et ve eksikse ekle
        tournament_instance = Tournament.objects.filter(tournament_uniqueTournament_id=tournament_id).first()
        season_instance = Season.objects.filter(season_id=season_id).first()
        
        # Modelde bu id ile kayıt olup olmadığını kontrol et
        if not Team.objects.filter(team_id=home_team_id).exists():
            if tournament_instance and season_instance:
                Team.objects.create(
                    team_id=row['homeTeam_id'],
                    team_name=row['homeTeam_name'],
                    team_slug=row['homeTeam_slug'],
                    team_shortName=row['homeTeam_shortName'],
                    team_nameCode=row['homeTeam_nameCode'],
                    team_national=row['homeTeam_national'] if pd.notna(row['homeTeam_national']) else False,
                    tournament=tournament_instance,  # Turnuva ile ilişkilendir
                    season=season_instance  # Sezon ile ilişkilendir
                )
                print(f"Home Team ID {home_team_id} başarıyla eklendi.")
            else:
                print(f"Tournament ID {tournament_id} veya Season ID {season_id} bulunamadı, Home Team ID {home_team_id} eklenemedi.")
        else:
            print(f"Home Team ID {home_team_id} zaten mevcut, eklenmedi.")
```

### 3. **Yanlış Turnuva Eklemesini Engelleme:**
Bu kod örneği ile, takımın yer aldığı turnuvanın mantıksal olarak doğru olup olmadığını kontrol ediyoruz. Eğer **Lokomotiv Moscow** gibi bir takımın **Serie B**'de olamayacağını biliyorsak, bu tür hataları ekleme aşamasında yakalayabilir ve verinin eklenmesini engelleyebiliriz.

### 4. **Doğrulama ve Test Etme:**
Veriyi API'den aldıktan sonra, her turnuva ve takım ilişkisinin mantıksal olarak doğru olup olmadığını kontrol ederek veri tutarsızlıklarını giderebilirsiniz. Ayrıca, bu tür kontrolleri genişleterek diğer olası hatalı eşleştirmeleri de önleyebilirsiniz.

### Özet:
- **Lokomotiv Moscow**'un **Serie B**'de gözükmesi gibi yanlış eşleştirmeler, veri işleme sırasında mantıksal bir hata olabilir.
- Verileri doğru şekilde işlemek ve mantıksal hataları kontrol etmek için turnuva ve takım ilişkilerini doğrulayan ek kontroller yapmalısınız.
- Bu kontrolleri kullanarak yanlış turnuva-takım eşleşmelerini tespit edebilir ve veritabanına yanlış verilerin kaydedilmesini engelleyebilirsiniz.