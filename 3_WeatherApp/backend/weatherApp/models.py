from django.db import models
from django.core.validators import RegexValidator

alphanumeric = RegexValidator(r"[a-zA-Z]*$", "Only Alphabet characters are allowed")

class City(models.Model):
    name = models.CharField(
        max_length=30, 
        unique=True,
        validators=[alphanumeric]
        )
    
    class Meta:
        verbose_name_plural = "cities"
    
    def __str__(self) -> str:
        return self.name