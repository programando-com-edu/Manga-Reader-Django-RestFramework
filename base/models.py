from django.contrib.auth import get_user_model
from django.db import models

from comics.models import Chapter


class ComicsRead(models.Model):
    user = models.ForeignKey(get_user_model(), verbose_name='Usuário', on_delete=models.PROTECT)
    last_chapter = models.ForeignKey(Chapter, verbose_name="Último capítulo lido", on_delete=models.PROTECT)
    start_date = models.DateTimeField(auto_now_add=True)
    last_time = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.last_chapter.comic
