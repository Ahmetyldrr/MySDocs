from django.contrib import admin
from .models import Lineups, Incidents, Graph, MatchInfo, Odds, Statistics
import json


# JSON içindeki tüm öğe sayısını hesaplayan fonksiyon
def count_json_elements(data):
    if isinstance(data, dict):
        return sum(count_json_elements(value) for value in data.values()) + len(data)
    elif isinstance(data, list):
        return sum(count_json_elements(item) for item in data)
    else:
        return 1  # Dize, sayı, vb. gibi temel veri türleri için 1 olarak sayılır

# Her model için özel admin görünümleri
class BaseModelAdmin(admin.ModelAdmin):
    list_display = ('match_id', 'data_count')
    
    def data_count(self, obj):
        # JSON alanındaki tüm elemanları sayar
        return count_json_elements(obj.data)
    
    data_count.short_description = "JSON İçindeki Toplam Veri Sayısı"

# Modellerin admin panele eklenmesi
admin.site.register(Lineups, BaseModelAdmin)
admin.site.register(Incidents, BaseModelAdmin)
admin.site.register(Graph, BaseModelAdmin)
admin.site.register(MatchInfo, BaseModelAdmin)
admin.site.register(Odds, BaseModelAdmin)
admin.site.register(Statistics, BaseModelAdmin)
