from django.db import models

class Topic(models.Model):
    """Um assunto sobre o qual o usuário está aprendendo"""
    text = models.CharField(max_length=200)
    date_added = models.DateField(auto_now_add=True)

    def __str__(self):
        """Devolve uma represnetação em string do modelo"""
        return self.text

class Entry(models.Model):
    """Algo específico aprendido do assunto"""
    topic = models.ForeignKey(Topic, on_delete=models.CASCADE)
    text = models.TextField()
    date_added = models.DateField(auto_now_add=True)
    
    class Meta:
        verbose_name_plural = 'entries'

    def __str__(self):
        """Devolve uma string do modelo"""
        return self.text[:50] + '...'




