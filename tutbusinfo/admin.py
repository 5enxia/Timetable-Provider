from django.contrib import admin

# Register your models here.
from .models import Station,TableIndex,TableBasic

class TableIndexInline(admin.TabularInline):
    model = TableIndex
    extra = 3

class StationAdmin(admin.ModelAdmin):
    inlines = [TableIndexInline]
    fields = ['name']

class TabelBasicInline(admin.TabularInline):
    model = TableBasic
    extra = 5
    ordering = ('left_campus',)

class TableIndexAdmin(admin.ModelAdmin):
    inlines = [TabelBasicInline]
    list_display = ('station','name')

class TableBasicAdmin(admin.ModelAdmin):
    list_display = ('row','left_campus','arrive_station','arrive_campus')    

admin.site.register(Station,StationAdmin)
admin.site.register(TableIndex,TableIndexAdmin)
admin.site.register(TableBasic,TableBasicAdmin)