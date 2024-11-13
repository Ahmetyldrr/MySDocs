***Soru:*** @admin.register(Match)
class MatchAdmin(admin.ModelAdmin):
    list_display = ('id', 'homeTeam', 'awayTeam', 'season', 'tournament', 'status_type', 'startTimestamp')
    list_filter = ('season', 'tournament', 'status_type')
    search_fields = ('homeTeam__team_name', 'awayTeam__team_name', 'slug')

    # Admin panelinde gözüken ev sahibi ve deplasman takım isimlerini düzenleme
    def home_team_name(self, obj):
        return obj.homeTeam.team_name
    home_team_name.short_description = 'Home Team'

    def away_team_name(self, obj):
        return obj.awayTeam.team_name
    away_team_name.short_description = 'Away Team'  bu model ile adminde şöyle bir şey var takımların hometeam ve awaytem Wolverhampton (Premier League - Premier League 24/25)	Manchester City (Premier League - Premier League 24/25)  bu şekilde yazııyor neden bu böylee adminde

**Cevap:** Admin panelindeki takım isimlerinin yanında parantez içinde sezona ve turnuvaya dair bilgilerin çıkması, muhtemelen takımın `__str__()` veya `__repr__()` metotlarında bu bilgilere yer verilmesinden kaynaklanıyor. Django admin, varsayılan olarak `ForeignKey` alanlarına bağlanmış modellerin `__str__()` metodunu kullanarak bu nesneleri görüntüler. Yani, `homeTeam` ve `awayTeam` ilişkili olduğu modelde tanımlı olan `__str__()` metodu nedeniyle böyle bir görüntü oluşuyor olabilir.

Bunu düzeltmek için `Team` modelinin `__str__()` metodunu kontrol edip, sadece takım ismini döndürecek şekilde güncelleyebilirsin. Şu adımları izleyebilirsin:

1. **`Team` Modelini Kontrol Et:**
   `Team` modelindeki `__str__()` metodunu kontrol et. Şu anki hali muhtemelen takım adının yanı sıra turnuva ve sezon bilgilerini de döndürüyor.

   Eğer şu anki `__str__()` metodu bu tarzdaysa:

   ```python
   def __str__(self):
       return f"{self.team_name} ({self.tournament} - {self.season})"
   ```

   Bunu sadece takım ismini döndürecek şekilde değiştir:

   ```python
   def __str__(self):
       return self.team_name
   ```

2. **Admin Panelindeki Değişiklikler:**
   Eğer takım ismini bu şekilde ayarladıktan sonra hala admin panelinde istenmeyen bilgiler gözüküyorsa, admin panelinde özel olarak `home_team_name` ve `away_team_name` metotlarını kullanarak gösterebilirsin, bu zaten yapmış olduğun bir işlem. Bu haliyle `list_display`'i şu şekilde düzenleyebilirsin:

   ```python
   @admin.register(Match)
   class MatchAdmin(admin.ModelAdmin):
       list_display = ('id', 'home_team_name', 'away_team_name', 'season', 'tournament', 'status_type', 'startTimestamp')
       list_filter = ('season', 'tournament', 'status_type')
       search_fields = ('homeTeam__team_name', 'awayTeam__team_name', 'slug')
       
       def home_team_name(self, obj):
           return obj.homeTeam.team_name
       home_team_name.short_description = 'Home Team'
   
       def away_team_name(self, obj):
           return obj.awayTeam.team_name
       away_team_name.short_description = 'Away Team'
   ```

Bu iki adım sorununu çözecektir. Takım ismi artık parantez içinde ek bilgiler olmadan görünecektir.

***Soru:*** id	startTimestamp	slug	tournament_id	season_id	roundInfo_round	status_type	homeTeam_id	awayTeam_id	homeScore_current	homeScore_period1	homeScore_period2	homeScore_normaltime	awayScore_current	awayScore_period1	awayScore_period2	awayScore_normaltime
0	11907436	2024-10-21 12:00:00+00:00	djurgardens-if-hammarby-if	40	57284	27	finished	1758	1759	2	2	0	2	0	0	0	0
1	11907437	2024-10-21 17:10:00+00:00	aik-ifk-goteborg	40	57284	27	finished	1761	1764	1	0	1	1	2	1	1	2
2	11907438	2024-10-21 17:00:00+00:00	if-brommapojkarna-ifk-norrkoping	40	57284	27	finished	1769	1787	1	1	0	1	1	1	0	1
3	11907440	2024-10-20 14:30:00+00:00	ifk-varnamo-gais-goteborg	40	57284	27	finished	1786	1842	0	0	0	0	0	0	0	0
4	11907442	2024-10-20 12:00:00+00:00	kalmar-ff-mjallby-aif	40	57284	27	finished	1891	1783	0	0	0	0	3	2	1	3
...	...	...	...	...	...	...	...	...	...	...	...	...	...	...	...	...	...
477	12991468	2024-10-20 20:30:00+00:00	sol-de-america-cerro-porteno	11541	63769	16	finished	36439	5991	0	0	0	0	1	1	0	1
478	12991470	2024-10-20 23:00:00+00:00	olimpia-libertad	11541	63769	16	finished	5996	5997	0	0	0	0	1	0	1	1
479	12992167	2024-10-20 17:15:00+00:00	ksc-lokeren-temse-rfc-seraing	9	61412	8	finished	371484	204712	0	0	0	0	1	1	0	1
480	13008795	2024-10-22 23:30:00+00:00	atlanta-united-cf-montreal	242	57317	0	notstarted	22006	243211	0	0	0	0	0	0	0	0
481	13016256	2024-10-23 12:00:00+00:00	kapa-kpv	55	58125	29	notstarted	2256	2273	0	0	0	0	0	0	0	0  şimndi elimde modelimde şöyle bir veri var burada takım idlerine göre ve sezon bilgisine göre her ligin puan durum tablosunu nasıl oluşturabilrim

**Cevap:** Her ligin puan durumu tablosunu oluşturmak için belirli adımları izleyerek takım puanlarını hesaplayabiliriz. Bu süreçte, maç sonuçlarına dayanarak galibiyet, beraberlik, mağlubiyet, atılan goller, yenilen goller gibi bilgileri toplar ve bu verilere göre puan durumunu çıkarırız.

İzleyebileceğin adımlar şu şekilde:

### 1. Gerekli Verileri Seç:
Öncelikle, maç sonuçlarından takımların galibiyet, beraberlik, mağlubiyet, atılan/yenen gol sayıları gibi bilgileri toplayacağız. Modelde yer alan şu alanları kullanacağız:

- `homeScore_current`: Ev sahibi takımın attığı toplam gol.
- `awayScore_current`: Deplasman takımının attığı toplam gol.
- `homeTeam_id`: Ev sahibi takımın ID'si.
- `awayTeam_id`: Deplasman takımının ID'si.
- `status_type`: Maçın bitip bitmediğini kontrol etmek için (sadece `finished` olan maçlar değerlendirilecek).
- `season_id`: Sezon bilgisine göre filtreleme.
- `tournament_id`: Her turnuvaya (lig) özel puan durumu oluşturmak için.

### 2. Puan Durumu Hesaplama:
Her takım için şu istatistikleri toplayacağız:

- **Galibiyet (W)**: Ev sahibi veya deplasman takımının maçı kazandığı maçlar.
- **Beraberlik (D)**: Her iki takımın da eşit skorla bitirdiği maçlar.
- **Mağlubiyet (L)**: Ev sahibi veya deplasman takımının kaybettiği maçlar.
- **Atılan Goller (GF)**: Her takımın attığı toplam gol.
- **Yenilen Goller (GA)**: Her takımın yediği toplam gol.
- **Puan (Pts)**: Galibiyet için 3, beraberlik için 1 puan verilecek.

### 3. Puan Durumu İçin Python/Pandas Kodlaması:
Veriyi Pandas ile işleyerek ligin puan durumunu hesaplayabilirsin. Şu adımlarla ilerleyebilirsin:

```python
import pandas as pd

# Örnek verileri içe aktar (Senin mevcut verin burada bir DataFrame olmalı)
data = {
    'id': [11907436, 11907437, 11907438],
    'startTimestamp': ['2024-10-21 12:00:00', '2024-10-21 17:10:00', '2024-10-21 17:00:00'],
    'homeTeam_id': [1758, 1761, 1769],
    'awayTeam_id': [1759, 1764, 1787],
    'homeScore_current': [2, 1, 1],
    'awayScore_current': [0, 2, 1],
    'season_id': [57284, 57284, 57284],
    'tournament_id': [40, 40, 40],
    'status_type': ['finished', 'finished', 'finished']
}

df = pd.DataFrame(data)

# Puan durumu hesaplamaya başla
def puan_durumu(df, tournament_id, season_id):
    # İlgili sezon ve turnuvadaki maçları filtrele
    df = df[(df['tournament_id'] == tournament_id) & (df['season_id'] == season_id) & (df['status_type'] == 'finished')]

    # Tüm takımları bul
    teams = pd.concat([df['homeTeam_id'], df['awayTeam_id']]).unique()

    # Puan durumu için gerekli sütunları oluştur
    puan_durumu = pd.DataFrame(teams, columns=['team_id'])
    puan_durumu['W'] = 0  # Galibiyet
    puan_durumu['D'] = 0  # Beraberlik
    puan_durumu['L'] = 0  # Mağlubiyet
    puan_durumu['GF'] = 0  # Atılan Goller
    puan_durumu['GA'] = 0  # Yenen Goller
    puan_durumu['Pts'] = 0  # Puan

    # Her maç için takımların performansını güncelle
    for _, row in df.iterrows():
        home_team = row['homeTeam_id']
        away_team = row['awayTeam_id']
        home_score = row['homeScore_current']
        away_score = row['awayScore_current']

        # Atılan ve yenilen golleri güncelle
        puan_durumu.loc[puan_durumu['team_id'] == home_team, 'GF'] += home_score
        puan_durumu.loc[puan_durumu['team_id'] == home_team, 'GA'] += away_score
        puan_durumu.loc[puan_durumu['team_id'] == away_team, 'GF'] += away_score
        puan_durumu.loc[puan_durumu['team_id'] == away_team, 'GA'] += home_score

        # Maç sonucuna göre puan, galibiyet, beraberlik, mağlubiyet güncelle
        if home_score > away_score:
            # Ev sahibi kazandı
            puan_durumu.loc[puan_durumu['team_id'] == home_team, 'W'] += 1
            puan_durumu.loc[puan_durumu['team_id'] == home_team, 'Pts'] += 3
            puan_durumu.loc[puan_durumu['team_id'] == away_team, 'L'] += 1
        elif home_score < away_score:
            # Deplasman kazandı
            puan_durumu.loc[puan_durumu['team_id'] == away_team, 'W'] += 1
            puan_durumu.loc[puan_durumu['team_id'] == away_team, 'Pts'] += 3
            puan_durumu.loc[puan_durumu['team_id'] == home_team, 'L'] += 1
        else:
            # Beraberlik
            puan_durumu.loc[puan_durumu['team_id'] == home_team, 'D'] += 1
            puan_durumu.loc[puan_durumu['team_id'] == home_team, 'Pts'] += 1
            puan_durumu.loc[puan_durumu['team_id'] == away_team, 'D'] += 1
            puan_durumu.loc[puan_durumu['team_id'] == away_team, 'Pts'] += 1

    # Puan durumunu puanlara göre sıralama
    puan_durumu = puan_durumu.sort_values(by=['Pts', 'GF', 'GA'], ascending=[False, False, True])
    
    return puan_durumu

# Sezon ve turnuva için puan durumu
puan_tablosu = puan_durumu(df, tournament_id=40, season_id=57284)

import ace_tools as tools; tools.display_dataframe_to_user(name="Puan Durumu", dataframe=puan_tablosu)
```

### 4. Açıklama:
- `puan_durumu()` fonksiyonu, bir turnuva ve sezon için tüm takımların puan durumunu hesaplar.
- `homeTeam` ve `awayTeam` olarak oynayan her takımın gol istatistikleri güncellenir.
- Maç sonucuna göre galibiyet, beraberlik, mağlubiyet ve puanlar güncellenir.
- Son olarak, puan durumunu puan, atılan goller ve yenilen goller ile sıralar.

Bu kodu kendi verinle uygulayarak her ligin puan durumunu oluşturabilirsin.