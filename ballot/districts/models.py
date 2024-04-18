from django.db import models


class Province(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return {self.name}

    class Meta:
        verbose_name = 'Province'
        verbose_name_plural = 'Provinces'


class District(models.Model):
    name = models.CharField(max_length=100)
    province = models.ForeignKey(Province, on_delete=models.CASCADE)

    def __str__(self):
        return {self.name}

    class Meta:
        verbose_name = 'Province'
        verbose_name_plural = 'Provinces'
