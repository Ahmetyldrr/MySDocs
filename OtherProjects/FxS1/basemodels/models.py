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

from django.db import models

class Tournament(models.Model):
    tournament_id = models.IntegerField(primary_key=True)  # Bu alan anahtar olarak kullanılacak
    tournament_name = models.CharField(max_length=255)
    tournament_slug = models.CharField(max_length=255)
    tournament_category_name = models.CharField(max_length=255)
    tournament_category_slug = models.CharField(max_length=255)
    tournament_uniqueTournament_category_id = models.IntegerField()
    tournament_uniqueTournament_hasEventPlayerStatistics = models.BooleanField(default=False)
    tournament_model_id = models.IntegerField()

    # Bu iki alan True, False, Boş (None) ve 0 olabilir
    tournament_isGroup = models.BooleanField(null=True, blank=True, default=False)
    tournament_uniqueTournament_hasPerformanceGraphFeature = models.BooleanField(null=True, blank=True, default=False)

    def __str__(self):
        return self.tournament_name

    class Meta:
        verbose_name = 'Tournament'
        verbose_name_plural = 'Tournaments'


class Season(models.Model):
    season_id = models.IntegerField(primary_key=True)  # Sezon için birincil anahtar
    season_name = models.CharField(max_length=255)
    season_year = models.CharField(max_length=9)  # Yıl bilgisini string olarak saklıyoruz (2024/2025 gibi)
    
    # tournament_id yerine kendi tanımladığınız sütunu kullanın
    tournament = models.ForeignKey(Tournament, on_delete=models.CASCADE, db_column='tournament_id', related_name='seasons')

    def __str__(self):
        return f"{self.season_name} ({self.season_year})"


class Team(models.Model):
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
        unique_together = ('team_id', 'tournament', 'season')  # Aynı takım, aynı turnuvada, aynı sezonda yalnızca bir kez yer alabilir


from basemodels.models import Team, Tournament, Season

class Match(models.Model):
    id = models.IntegerField(primary_key=True)  # Manuel olarak ID ekleyeceğin için IntegerField kullandık
    startTimestamp = models.DateTimeField()  # Artık datetime olacak
    slug = models.SlugField(max_length=255)  # Maç slug'ı
    tournament = models.ForeignKey(Tournament, on_delete=models.CASCADE)  # Turnuva ile ilişki
    season = models.ForeignKey(Season, on_delete=models.CASCADE)  # Sezon ile ilişki
    roundInfo_round = models.IntegerField()  # Tur bilgisi
    status_type = models.CharField(max_length=50)  # Maç durumu (ör. finished)
    homeTeam = models.ForeignKey(Team, on_delete=models.CASCADE, related_name='home_matches')  # Ev sahibi takım
    awayTeam = models.ForeignKey(Team, on_delete=models.CASCADE, related_name='away_matches')  # Deplasman takımı
    homeScore_current = models.IntegerField()  # Ev sahibi skor (mevcut)
    homeScore_period1 = models.IntegerField()  # Ev sahibi 1. yarı skoru
    homeScore_period2 = models.IntegerField()  # Ev sahibi 2. yarı skoru
    homeScore_normaltime = models.IntegerField()  # Ev sahibi normal süre skoru
    awayScore_current = models.IntegerField()  # Deplasman skor (mevcut)
    awayScore_period1 = models.IntegerField()  # Deplasman 1. yarı skoru
    awayScore_period2 = models.IntegerField()  # Deplasman 2. yarı skoru
    awayScore_normaltime = models.IntegerField()  # Deplasman normal süre skoru

    def __str__(self):
        return f"{self.homeTeam.team_name} vs {self.awayTeam.team_name} ({self.slug})"

    class Meta:
        verbose_name = 'Match'
        verbose_name_plural = 'Matches'
        unique_together = ('homeTeam', 'awayTeam', 'season', 'tournament')
