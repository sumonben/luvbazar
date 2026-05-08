from django.db import models

# Create your models here.

class Division(models.Model):
    name=models.CharField(max_length=50,unique=True)
    name_en=models.CharField(max_length=50,unique=True)
    link=models.CharField(max_length=100,null=True,blank=True)
    is_active=models.BooleanField(default=False)
    class Meta:
        ordering = ['name']
    def __str__(self):
        return self.name+'('+self.name_en+')'

class District(models.Model):
    name=models.CharField(max_length=100,unique=True)
    name_en=models.CharField(max_length=100,unique=True)
    lattitude=models.CharField(max_length=100,blank=True,null=True)
    longitude=models.CharField(max_length=100, blank=True,null=True)
    division=models.ForeignKey(Division, on_delete=models.CASCADE,blank=True,null=True)
    link=models.CharField(max_length=100,null=True,blank=True)
    is_active=models.BooleanField(default=False)
    class Meta:
        ordering = ['name_en']
    def __str__(self):
        return self.name+'('+self.name_en+')'

class Upazilla(models.Model):
    name=models.CharField(max_length=100)
    name_en=models.CharField(max_length=100)
    district=models.ForeignKey(District, on_delete=models.CASCADE,blank=True,null=True)
    link=models.CharField(max_length=100,null=True,blank=True)
    is_active=models.BooleanField(default=False)
    class Meta:
        ordering = ['name_en']
    def __str__(self):
        return self.name+'('+self.name_en+')'

class Union(models.Model):
    name=models.CharField(max_length=100)
    name_en=models.CharField(max_length=100)
    upazilla=models.ForeignKey(Upazilla, on_delete=models.CASCADE,blank=True,null=True)
    link=models.CharField(max_length=100,null=True,blank=True)
    is_active=models.BooleanField(default=False)

    class Meta:
        ordering = ['name_en']
    def __str__(self):
        return self.name+'('+self.name_en+')'
    
class Ward(models.Model):
    name=models.CharField(max_length=25)
    name_en=models.CharField(max_length=25)
    ward_no=models.CharField(max_length=10)
    ward_no_en=models.CharField(max_length=10,default='02')
    link=models.CharField(max_length=15,null=True,blank=True)
    is_active=models.BooleanField(default=False)
    class Meta:
        ordering = ['name_en']
    def __str__(self):
        return self.name+'('+self.name_en+')'

class PostOffice(models.Model):
    name=models.CharField(max_length=100)
    name_en=models.CharField(max_length=100)
    post_code=models.CharField(max_length=15,null=True,blank=True)
    post_code_en=models.CharField(max_length=15,null=True,blank=True)
    link=models.CharField(max_length=100,null=True,blank=True)
    is_active=models.BooleanField(default=False)
    class Meta:
        ordering = ['name_en']
    def __str__(self):
        return self.name+'('+self.name_en+')'
 
class Village(models.Model):
    name=models.CharField(max_length=25)
    name_en=models.CharField(max_length=25)
    ward=models.ForeignKey(Ward, on_delete=models.SET_NULL,blank=True,null=True)
    post_office=models.ForeignKey(PostOffice, on_delete=models.SET_NULL,blank=True,null=True)
    link=models.CharField(max_length=50,null=True,blank=True)
    is_active=models.BooleanField(default=False)

    class Meta:
        ordering = ['name_en']
    def __str__(self):
        return self.name+'('+self.name_en+')'
    
