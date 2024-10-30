from django.db import models

class Tournament(models.Model):
    tournament_uniqueTournament_id = models.IntegerField()
    tournament_name = models.CharField(max_length=255)
    tournament_slug = models.CharField(max_length=255)
    tournament_category_name = models.CharField(max_length=255)
    tournament_category_slug = models.CharField(max_length=255)
    tournament_uniqueTournament_category_id = models.IntegerField()
    tournament_uniqueTournament_hasEventPlayerStatistics = models.BooleanField(default=False)
    tournament_id = models.IntegerField()
    
    # Bu iki alan True, False, Boş (None) ve 0 olabilir
    tournament_isGroup = models.BooleanField(null=True, blank=True, default=False)
    tournament_uniqueTournament_hasPerformanceGraphFeature = models.BooleanField(null=True, blank=True, default=False)

    def __str__(self):
        return self.tournament_name

    class Meta:
        verbose_name = 'Tournament'
        verbose_name_plural = 'Tournaments'




class Season(models.Model):
    season_id = models.IntegerField()  # Sezon için birincil anahtar
    season_name = models.CharField(max_length=255)
    season_year = models.CharField(max_length=9)  # Yıl bilgisini string olarak saklıyoruz (2024/2025 gibi)
    tournament = models.ForeignKey(Tournament, on_delete=models.CASCADE, related_name='seasons')

    def __str__(self):
        return f"{self.season_name} ({self.season_year})"
    
    
class Team(models.Model):
    team_id = models.IntegerField() 
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