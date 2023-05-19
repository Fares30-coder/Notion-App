from django.db import models

class Video(models.Model):
    titre = models.CharField(max_length=100)
    description = models.TextField()
    fichier_video = models.FileField(upload_to='videos/')

class ResultatAnalyse(models.Model):
    video_liee = models.ForeignKey(Video, on_delete=models.CASCADE)
    resultats = models.TextField()

# Create your models here.
