from django.db import models

class Lineups(models.Model):
    match_id = models.IntegerField(primary_key=True)
    data = models.JSONField()

class Incidents(models.Model):
    match_id = models.IntegerField(primary_key=True)
    data = models.JSONField()

class Graph(models.Model):
    match_id = models.IntegerField(primary_key=True)
    data = models.JSONField()

class MatchInfo(models.Model):
    match_id = models.IntegerField(primary_key=True)
    data = models.JSONField()

class Odds(models.Model):
    match_id = models.IntegerField(primary_key=True)
    data = models.JSONField()

class Statistics(models.Model):
    match_id = models.IntegerField(primary_key=True)
    data = models.JSONField()
