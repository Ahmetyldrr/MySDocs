from django.contrib import admin
from .models import Tournament
from .models import Season
from .models import Team

@admin.register(Tournament)
class TournamentAdmin(admin.ModelAdmin):
    # Listede gösterilecek sütunlar (ülke bilgisini de ekliyoruz)
    list_display = ['tournament_uniqueTournament_id', 'tournament_name', 'tournament_slug', 'tournament_category_name']
    
    # Arama yapılacak alanlar
    search_fields = ['tournament_name', 'tournament_slug']
    
    # Ülkeye göre filtreleme
    list_filter = ['tournament_category_name']  # Burada turnuva kategorisini (ülke) filtreliyoruz
    

@admin.register(Season)
class SeasonAdmin(admin.ModelAdmin):
    list_display = ['season_id','season_name', 'season_year', 'tournament']  # Turnuvayı da gösteriyoruz
    search_fields = ['season_name', 'season_year']
    list_filter = ['tournament']  # Sezonları turnuvaya göre filtreleyebiliriz
    
    
@admin.register(Team)
class TeamAdmin(admin.ModelAdmin):
    # Admin sayfasında gösterilecek alanlar
    list_display = ('team_id', 'team_name', 'team_shortName', 'tournament', 'season')
    
    # Admin sayfasında kullanılacak filtreler
    list_filter = ('team_name', 'tournament', 'season')

    # Arama alanı eklemek isterseniz
    search_fields = ('team_name', 'team_shortName', 'team_nameCode')