<<<<<<< HEAD
from django.contrib import admin

from django.contrib import admin
from .models import MatchStats

from django.contrib import admin
from .models import MatchStats
from django.contrib import admin
from django.utils.translation import gettext_lazy as _

class EmptyStatsFilter(admin.SimpleListFilter):
    title = _('Stats Durumu')
    parameter_name = 'stats_empty'

    def lookups(self, request, model_admin):
        return (
            ('empty', _('Veri yok')),
            ('not_empty', _('Veri var')),
        )

    def queryset(self, request, queryset):
        if self.value() == 'empty':
            return queryset.filter(stats__isnull=True) | queryset.filter(stats__exact='')
        if self.value() == 'not_empty':
            return queryset.exclude(stats__isnull=True).exclude(stats__exact='')

from django.contrib import admin
from django.utils.translation import gettext_lazy as _

class EmptyStatsFilter(admin.SimpleListFilter):
    title = _('Stats Durumu')
    parameter_name = 'stats_empty'

    def lookups(self, request, model_admin):
        return (
            ('empty', _('Veri yok')),
            ('not_empty', _('Veri var')),
        )

    def queryset(self, request, queryset):
        if self.value() == 'empty':
            return queryset.filter(stats__isnull=True) | queryset.filter(stats__exact='')
        if self.value() == 'not_empty':
            return queryset.exclude(stats__isnull=True).exclude(stats__exact='')



class MatchStatsAdmin(admin.ModelAdmin):
    # Admin panelinde listede görünecek alanlar
    list_display = ('id', 'tarih', 'update_date', 'stats_summary')
    
    # Admin panelinde filtreleme yapabileceğimiz alanlar
    list_filter = ('tarih', 'update_date', EmptyStatsFilter)  # Özel filtreyi ekledik
    
    # Admin panelinde arama yapabileceğimiz alanlar
    search_fields = ('id', 'tarih')
    
    # Admin panelinde gösterilen JSON alanının özetini almak için özel bir metot
    def stats_summary(self, obj):
        # 'stats' alanındaki JSON verisinden bir özet döndürme
        if obj.stats:
            return str(obj.stats)[:300] + "..." if len(str(obj.stats)) > 10 else str(obj.stats)
        return "Veri yok"


admin.site.register(MatchStats, MatchStatsAdmin)







from django.contrib import admin
from .models import MatchInfo  # Aynı dizindeki models.py dosyasından MatchInfo modelini içeri aktarıyoruz

@admin.register(MatchInfo)  # Modeli admin paneline eklemek için dekoratör kullanıyoruz
class MatchInfoAdmin(admin.ModelAdmin):
    # Admin panelinde hangi alanların gösterileceğini belirt
    list_display = (
        "match_id", "tournament_name", "tournament_category_name", "season_name", "home_team_name", "away_team_name", 
        "home_score_period1", "away_score_period1", "start_timestamp"
    )
    # Admin panelinde hangi alanlardan arama yapılabileceğini belirt
    search_fields = ("match_id", "tournament_name", "home_team_name", "away_team_name")
    # Admin panelinde hangi alanlara göre filtreleme yapılabileceğini belirt
    list_filter = ("season_name", "tournament_category_name", "home_team_name", "away_team_name")





from django.contrib import admin
from .models import PlayerPerformance

@admin.register(PlayerPerformance)
class PlayerPerformanceAdmin(admin.ModelAdmin):
    # Admin panelinde gösterilecek alanlar
    list_display = ('match_id', 'team_name', 'team_id', 'player_name', 'player_id', 'position', 'home')

    # Arama yapılabilecek alanlar
    search_fields = ('player_name', 'team_name', 'player_id', 'match_id')

    # Admin panelinde filtrelenebilecek alanlar
    list_filter = ('team_name', 'position', 'player_position')

    # Varsayılan sıralama
    ordering = ('match_id', 'team_name')

    # Varsayılan olarak 'team' alanı home olarak gösterilsin
    def home(self, obj):
        return obj.team == "home"

    home.boolean = True  # True/False alanları için



=======
>>>>>>> ecd6c88f7ec7bd98d4581c9ee8c5d25a2c400714
