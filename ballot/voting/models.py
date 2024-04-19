from django.db import models
from django.core.exceptions import ValidationError

from districts.models import District


class ElectionHandler(models.Model):
    class ElectionStatusTypeChoice(models.TextChoices):
        PEN = 'pen', ('Pendiente')
        ABI = 'abi', ('Abierta')
        CER = 'cer', ('Cerrada')

    status = models.CharField(
        max_length=3, choices=ElectionStatusTypeChoice.choices, default=ElectionStatusTypeChoice.PEN
    )

    @property
    def next_status(self):
        next_status = self.ElectionStatusTypeChoice.ABI
        if self.status == self.ElectionStatusTypeChoice.ABI:
            next_status = self.ElectionStatusTypeChoice.CER
        elif self.status == self.ElectionStatusTypeChoice.CER:
            next_status = None

        return next_status

    class Meta:
        verbose_name = 'Election Handler'
        verbose_name_plural = 'Election Handlers'


class Voter(models.Model):
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    dni = models.PositiveIntegerField(unique=True)
    birth_date = models.DateField()
    has_voted = models.BooleanField(default=False)

    district = models.ForeignKey(District, on_delete=models.PROTECT, null=False)

    def __str__(self):
        return f'{self.first_name} {self.last_name}'

    class Meta:
        verbose_name = 'Voter'
        verbose_name_plural = 'Voters'

    def save(self, *args, **kwargs):
        if ElectionHandler.objects.all().first().status != 'pen':
            raise ValidationError(
                'No se puede crear/modificar registros con la elección abierta o finalizada '
            )

        super().save(*args, **kwargs)

    def delete(self, *args, **kwargs):
        if ElectionHandler.objects.all().first().status != 'pen':
            raise ValidationError(
                'No se puede crear/modificar registros con la elección abierta o finalizada '
            )

        super().delete(*args, **kwargs)


class PoliticalParty(models.Model):
    party_number = models.PositiveIntegerField(unique=True)
    party_name = models.CharField(max_length=50)
    president = models.CharField(max_length=100)
    vice_president = models.CharField(max_length=100)
    slogan = models.CharField(max_length=100)

    def __str__(self):
        return f'{self.party_number} - {self.party_name}'

    class Meta:
        verbose_name = 'Political Party'
        verbose_name_plural = 'Political Parties'

    def save(self, *args, **kwargs):
        if ElectionHandler.objects.all().first().status != 'pen':
            raise ValidationError(
                'No se puede crear/modificar registros con la elección abierta o finalizada '
            )

        super().save(*args, **kwargs)

    def delete(self, *args, **kwargs):
        if ElectionHandler.objects.all().first().status != 'pen':
            raise ValidationError(
                'No se puede crear/modificar registros con la elección abierta o finalizada '
            )

        super().delete(*args, **kwargs)


class Vote(models.Model):
    political_party = models.ForeignKey(
        PoliticalParty, on_delete=models.PROTECT, null=True, blank=True, default=None
    )
    district = models.ForeignKey(District, on_delete=models.PROTECT, null=False)

    def __str__(self):
        return f'Voto a {self.political_party.party_name} - ({self.district})'

    class Meta:
        verbose_name = 'Vote'
        verbose_name_plural = 'Votes'

    def save(self, *args, **kwargs):
        if ElectionHandler.objects.all().first().status != 'abi':
            raise ValidationError(
                'No se puede crear/modificar registros con la elección pendiente o finalizada '
            )

        super().save(*args, **kwargs)

    def delete(self, *args, **kwargs):
        raise ValidationError('No se puede eliminar votos')
