from django.contrib import admin

from .models import FikstureModelData
from .models import Tournament
from .models import Season

@admin.register(FikstureModelData)
class ModelDataAdmin(admin.ModelAdmin):
    list_display = ('data_id', 'tarih', 'count' ,'isprogress', 'created_at', 'updated_at')  # Tüm alanlar gösteriliyor
    list_filter = ('tarih', 'isprogress')  # Tarih ve ilerleme durumu filtrelenebilir
    search_fields = ('data_id', 'data')  # data_id ve data alanlarında arama yapılabilir


@admin.register(Tournament)
class TournamentAdmin(admin.ModelAdmin):
    # Listede gösterilecek sütunlar (ülke bilgisini de ekliyoruz)
    list_display = ['tournament_id', 'tournament_name', 'tournament_slug', 'tournament_category_name']
    
    # Arama yapılacak alanlar
    search_fields = ['tournament_name', 'tournament_slug']
    
    # Ülkeye göre filtreleme
    list_filter = ['tournament_category_name']  # Burada turnuva kategorisini (ülke) filtreliyoruz
    
    
    
@admin.register(Season)
class SeasonAdmin(admin.ModelAdmin):
    list_display = ['season_id','season_name', 'season_year', 'tournament']  # Turnuvayı da gösteriyoruz
    search_fields = ['season_name', 'season_year']
    list_filter = ['tournament']  # Sezonları turnuvaya göre filtreleyebiliriz
    
    
    

from .models import Team

# Team modelini admin paneline ekliyoruz
@admin.register(Team)
class TeamAdmin(admin.ModelAdmin):
    # Görüntülemek istediğiniz alanlar
    list_display = ('team_name', 'team_shortName', 'team_nameCode', 'team_national', 'tournament', 'season')
    
    # Arama yapılacak alanlar
    search_fields = ('team_name', 'team_shortName', 'team_nameCode')

    # Filtreleme alanları (sağ tarafta)
    list_filter = ('tournament', 'season', 'team_national')
    
    # Varsayılan sıralama
    ordering = ('season',)


from .models import Match

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