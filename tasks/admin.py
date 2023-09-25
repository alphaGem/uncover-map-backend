from django.contrib import admin
from import_export import resources,fields,widgets
from .models import Info
# Register your models here.
class InfoResource(resources.ModelResource):
    def before_import(self, dataset, result, using_transactions, **kwargs):
        """  delete all rows not in the import data set. Then call the same method in the parent to still sequence the DB """
        self.Meta.model.objects.all().delete()
    class Meta:
        model = Info