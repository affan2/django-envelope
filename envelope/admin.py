from django.contrib import admin
from .models import CompanyContact, ProductContact, SolutionContact

admin.site.register(CompanyContact)
admin.site.register(ProductContact)
admin.site.register(SolutionContact)
