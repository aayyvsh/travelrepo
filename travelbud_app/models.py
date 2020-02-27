from django.db import models
import bcrypt
import datetime

# Create your models here.

class UserManager(models.Manager):
    def regValidator(self, postData):
        errors = {}
        usersWithUname = User.objects.filter(username = postData['uname'])
        if len(postData['name']) <1:
            errors['namerequired'] = 'Name required'
        elif len(postData['name']) <3:
            errors['namelength'] = 'Name needs more length'
        if len(postData['uname']) <1:
            errors['unamerequired'] = 'Username required'
        elif len(postData['uname']) <3:
            errors['unamelength'] = 'Username needs more length'
        elif len(usersWithUname) >0:
            errors['unametaken'] = "Username taken"
        if len(postData['pw']) <1:
            errors['passwordrequired'] = 'Password required'
        elif len(postData['pw']) <8:
            errors['passwordlength'] = 'Password needs more length'
        if postData['pw'] != postData['cpw']:
            errors['confirm'] = 'password do no match'

        return errors

    def loginValidator(self, postData):
        errors = {}
        usersWithUname = User.objects.filter(username = postData['uname'])
        if len(usersWithUname) ==0:
            errors['unameexist'] = 'Username does not exist'
        else: 
            user = usersWithUname[0]
            if bcrypt.checkpw(postData['pw'].encode(), user.password.encode()):
                print("password match")
            else:
                errors['pw'] = "Invalid password"
        return errors

    def tripValidator(self,postData):
        errors = {}
        if len(postData['dest']) <1:
            errors['destrequired'] = 'Destination required'
        if len(postData['desc']) <1:
            errors['descrequired'] = 'Description required'
        if len(postData['tdfrom']) <1:
            errors['fromrequired'] = 'Date from required'
        if len(postData['tdto']) <1:
            errors['torequired'] = 'Date to required'
        if postData['tdfrom'] > postData['tdto']:
            errors['wrongdate'] = 'Cannot Time Travel'
        present = datetime.date.today()
        # datefrom = datetime.datetime.strptime(postData['tdfrom'], "%Y-%m-%d").date()
        if postData['tdfrom'] <= str(present):
            errors['future'] = 'date must be in present'
        return errors

class User(models.Model):
    name= models.CharField(max_length=255)
    username= models.CharField(max_length=255)
    password= models.CharField(max_length=255)
    confirmPassword= models.CharField(max_length=255)
    created_at= models.DateTimeField(auto_now_add=True)
    updated_at= models.DateTimeField(auto_now=True)
    objects = UserManager()

class Trip(models.Model):
    destination= models.CharField(max_length=255)
    description= models.CharField(max_length=255)
    travelfrom= models.DateField()
    travelto= models.DateField()
    user= models.ForeignKey(User, related_name="trips", on_delete= models.CASCADE)
    joiners= models.ManyToManyField(User, related_name = 'trip_joiners')
    created_at= models.DateTimeField(auto_now_add=True)
    updated_at= models.DateTimeField(auto_now=True)