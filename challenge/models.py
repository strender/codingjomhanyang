from django.db import models

from tag.models import Tag
from account.models import Account

import datetime

week = datetime.timedelta(days=7)

class ChallengeManager(models.Manager):
    def create_challenge(self, start_date, subject, detail, thumbnail_url):
        chall = self.create(start_date = start_date,
                            finish_date = start_date + week,
                            subject = subject,
                            detail = detail,
                            thumbnail_url = thumbnail_url)

        return chall

# Create your models here.
class Challenge(models.Model):
    start_date = models.DateField()
    finish_date = models.DateField()

    subject = models.CharField(max_length = 50)
    detail = models.CharField(max_length = 200, default="")

    thumbnail_url = models.URLField(default="")

    objects = ChallengeManager()

    def __unicode__(self):
        return self.subject

    def is_active(self):
        now = datetime.datetime.now()

        if self.start_date <= now.date() <= self.finish_date:
            return True
        else:
            return False

    def d_day(self):
        now = datetime.datetime.now()

        d_day = now.date() - self.finish_date

        return -int(d_day.total_seconds()/60/60/24)

    def current_phase(self):
        now = datetime.datetime.now()

        if self.start_date + week*3 < now:
            return 2 # design
        elif self.start_date + week*2 < now:
            return 1 # dev
        elif self.start_date + week < now:
            return 0 # plan
