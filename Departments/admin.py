from django.contrib import admin
from .models import Doctors, Nurses, ICT, HumanResource,Technicians,ContractWorkers
from django.contrib.admin import AdminSite
from django.utils.translation import gettext as _, gettext_lazy



class DoctorsAdmin(admin.ModelAdmin):
    list_display = ['first_name', 'last_name', 'position', 'joined', 'email',
                    'phone_number', 'specialty']
    list_filter = ['first_name', 'last_name', 'phone_number']
    search_fields = ['first_name', 'last_name', 'phone_number']
    list_per_page = 50

admin.site.register(Doctors, DoctorsAdmin)

class NursesAdmin(admin.ModelAdmin):
    list_display = ['first_name', 'last_name', 'position', 'joined', 'email',
                    'phone_number']
    list_filter = ['first_name', 'last_name', 'phone_number']
    search_fields = ['first_name', 'last_name', 'phone_number']
    list_per_page = 50
admin.site.register(Nurses, NursesAdmin)

class ICTAdmin(admin.ModelAdmin):
    list_display = ['first_name', 'last_name', 'position', 'joined', 'email',
                    'phone_number']
    list_filter = ['first_name', 'last_name', 'phone_number']
    search_fields = ['first_name', 'last_name', 'phone_number']
    list_per_page = 50
admin.site.register(ICT, ICTAdmin)

class HumanResourceAdmin(admin.ModelAdmin):
    list_display = ['first_name', 'last_name', 'position', 'joined', 'email',
                    'phone_number']
    list_filter = ['first_name', 'last_name', 'phone_number']
    search_fields = ['first_name', 'last_name', 'phone_number']
    list_per_page = 50
admin.site.register(HumanResource, HumanResourceAdmin)


class TechniciansAdmin(admin.ModelAdmin):
    list_display = ['first_name', 'last_name', 'position', 'joined', 'email',
                    'phone_number', ]
    list_filter = ['first_name', 'last_name', 'phone_number']
    search_fields = ['first_name', 'last_name', 'phone_number']
    list_per_page = 50
admin.site.register(Technicians, TechniciansAdmin)


class ContractWorkersAdmin(admin.ModelAdmin):
    list_display = ['first_name', 'last_name', 'position', 'joined', 'email',
                    'phone_number']
    list_filter = ['first_name', 'last_name', 'phone_number']
    search_fields = ['first_name', 'last_name', 'phone_number']
    list_per_page = 50
admin.site.register(ContractWorkers, ContractWorkersAdmin)



# Disable the 'delete_selected' action
admin.site.disable_action('delete_selected')
# Customize the admin site titles
admin.site.site_header = "Ralpha Hospital Administration"
admin.site.site_title = "Ralpha Hospital Admin Portal"
admin.site.index_title = "Welcome to Ralpha Hospital Administration"
