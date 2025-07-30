from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Topic(models.Model):
    """Assunto que o usuário está aprendendo"""
    text = models.CharField(max_length=200)
    date_added = models.DateTimeField(auto_now_add=True)

    owner = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        """Retorna uma representação em String do model""" 
        return self.text
    
class Entry(models.Model):
    """Caixa de texto do tópico que o usuário está aprendendo"""
    topic = models.ForeignKey(Topic, on_delete=models.CASCADE)
    text = models.TextField()
    date_added = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name_plural = 'entries'
    
    def __str__(self):
        """Retorna uma representação em string do model"""
        return self.text[:50]+'...'