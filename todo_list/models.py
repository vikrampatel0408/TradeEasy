from django.db import models

class List(models.Model):
    item = models.CharField(max_length=200)
    completed = models.BooleanField(default=False)
    
class T_List(models.Model):
    t_amt = models.FloatField()
    u_id = models.IntegerField()
    def __str__(self) -> str:
        return "Total Amount :",self.t_amt ,"User ID:",self.u_id

class crypto_tbl(models.Model):
    b_img = models.CharField(max_length=400)
    b_price = models.FloatField()
    b_amt = models.FloatField()
    b_token = models.FloatField()
    b_name = models.CharField(max_length=200)
    u_id = models.IntegerField()
    def __str__(self) -> str:
        return "Price:",self.b_price,"Amount:",self.b_amt,"Token:",self.b_token,"Name:",self.b_name

class Contact(models.Model):
    email = models.CharField(max_length=110)
    message = models.TextField()
    def __str__(self) ->str :
       return "Email:",self.email,"Message :",self.message