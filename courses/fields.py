from django.db import models
from django.core.exceptions import ObjectDoesNotExist

class OrderField(models.PositiveIntegerField):
    def __init__(self, for_fields=None, *args, **kwargs):
        self.for_fields = for_fields
        super().__init__(*args, **kwargs)
        
    def pre_save(self, model_instance, add):
        if getattr(model_instance, self.attname) is None:
            # no current value
            try:
                queryset = self.model.objects.all()
                if self.for_fields:
                    # filter by objects with same field values for fields in "for_fields"
                    query = {field: getattr(model_instance, field) for field in self.for_fields}
                    queryset = queryset.filter(**query)
                # get the order of the last item
                last_content = queryset.latest(self.attname)
                value = last_content.order + 1
            except ObjectDoesNotExist:
                value = 1
            setattr(model_instance, self.attname, value)
            return value
        else:
            return super().pre_save(model_instance, add)
                    
    