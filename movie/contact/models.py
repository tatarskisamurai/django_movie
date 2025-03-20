from django.db import models

class Contact(models.Model):
   email = models.EmailField()
   data = models.DateTimeField(auto_now_add=True)

   def __str__(self):
      return self.email
