from django.db import models
from django.db.models import Q
from django.contrib.auth.models import User

# Create your models here.

SEX_CHOICES = [
    ( 'Male', 'Male' ),
    ( 'Female', 'Female' ),
]

AGE_CHOICES = [
    ( 'Young', 'Young' ),
    ( 'Adult', 'Adult' ),
    ( 'Senior', 'Senior' ),
]

ADOPTION_REQUEST_STATUS = [
    ( 'Pending', 'Pending' ),
    ( 'Accepted', 'Accepted' ),
    ( 'Rejected', 'Rejected' ),
    ( 'Adopted by Another User', 'Adopted by Another User')
]


class Kind(models.Model):
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name


class Pet(models.Model):
    published_by = models.ForeignKey(User, related_name='published_by', on_delete=models.CASCADE)
    name = models.CharField(max_length=30)
    sex = models.CharField(max_length=10, choices=SEX_CHOICES)
    description = models.TextField(max_length=300)
    age = models.CharField(max_length=10, choices=AGE_CHOICES)
    breed = models.CharField(max_length=50)
    date = models.DateTimeField(auto_now=True)
    image = models.ImageField(upload_to='pics', default='img.jpg')
    favorites = models.ManyToManyField(User, related_name='favorite', blank=True)
    kind = models.ForeignKey(Kind, null=True, on_delete=models.RESTRICT)
    is_active = models.BooleanField(default=True)
    adopted = models.BooleanField(default=False)
    adopted_by = models.ForeignKey(User, related_name='adopted_by', null=True, on_delete=models.RESTRICT)

    def __str__(self):
        return self.name

    def delete(self):
        self.is_active = False
        self.save()

    def get_active():
        return Pet.objects.filter(is_active=True)

    def get_listings():
        return Pet.objects.filter(Q(is_active=True) & Q(adopted=False))
    
    def recent_dog_list():
        try:
            dog = Kind.objects.get(name='Dog')
            return Pet.get_active().filter(kind=dog).order_by('date')[0:4]
        except Kind.DoesNotExist:
            return None

    def recent_cat_list():
        try:
            cat = Kind.objects.get(name='Cat')
            return Pet.get_active().filter(kind=cat).order_by('date')[0:4]
        except Kind.DoesNotExist:
            return None

    def recent_other_list():
        try:
            cat = Kind.objects.get(name='Cat')
            dog = Kind.objects.get(name='Dog')
            return Pet.get_active().exclude(kind__in=(dog, cat)).order_by('date')[0:4]
        except Kind.DoesNotExist:
            return None


class AdoptionRequest(models.Model):
    reciever = models.ForeignKey(User, related_name='reciever', on_delete=models.CASCADE)
    sender = models.ForeignKey(User, related_name='sender', on_delete=models.CASCADE)
    pet = models.ForeignKey(Pet, on_delete=models.CASCADE)
    date = models.DateTimeField(auto_now=True)
    status = models.CharField(max_length=25, default='Pending', choices=ADOPTION_REQUEST_STATUS)