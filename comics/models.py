from django.db import models
from enum import Enum


class TypeCatalog(Enum):
    ASURA = 1


CATALOG_CHOICES = [
    (TypeCatalog.ASURA, 'Asura')
]


class Comic(models.Model):
    title = models.CharField(verbose_name='Nome da Obra', max_length=255)
    genre = models.CharField(verbose_name='Gêneros', max_length=255, null=True, blank=True)
    description = models.TextField(verbose_name='Descrição da obra', null=True, blank=True)
    banner = models.URLField(verbose_name='Link imagem banner', null=True, blank=True)
    link = models.URLField(verbose_name='Link da página da obra')
    catalog = models.PositiveIntegerField(choices=CATALOG_CHOICES, null=True, blank=True)

    def __str__(self):
        return self.title


class Chapter(models.Model):
    number = models.CharField(verbose_name='Número do capítulo', max_length=16)
    link = models.URLField(verbose_name='Link do capítulo')
    comic = models.ForeignKey(Comic, verbose_name='Obra', on_delete=models.PROTECT)

    def __str__(self):
        return f'{self.comic} - Cap. {self.number}'


class ChapterPage(models.Model):
    image_link = models.URLField(verbose_name='Imagem da página')
    chapter = models.ForeignKey(Chapter, verbose_name='Capitulo', on_delete=models.PROTECT)

