from django.db import models


class ModelA(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name


class ModelB(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name


class ModelCentral(models.Model):
    name = models.CharField(max_length=255)
    foreign_key_a = models.ForeignKey(
        'ModelA',
        on_delete=models.CASCADE,
        blank=True,
        null=True
    )
    m2m_b = models.ManyToManyField(
        'ModelB',
        blank=True
    )

    def __str__(self):
        return self.name


class ModelFK(models.Model):
    name = models.CharField(max_length=255)
    foreign_key_c = models.ForeignKey(
        'ModelCentral',
        on_delete=models.CASCADE,
        blank=True,
        null=True
    )

    def __str__(self):
        return self.name


class ModelMM(models.Model):
    name = models.CharField(max_length=255)
    m2m_c = models.ManyToManyField(
        'ModelCentral',
        blank=True
    )

    def __str__(self):
        return self.name
