from django.db import models
import re


class Showmanager(models.Manager):
    def login_validator(self, postData):
        errors = {}
        EMAIL_REGEX = re.compile(
            r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
        if not EMAIL_REGEX.match(postData['email']):
            errors['email'] = "Invalid email address!"
        if len(postData['password']) < 6:
            errors["password"] = "Password should be at least 6 characters"
        return errors

    def reg_validator(self, postData):
        errors = {}
        EMAIL_REGEX = re.compile(
            r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
        if not EMAIL_REGEX.match(postData['email']):
            errors['email'] = "Invalid email address!"
        if len(postData['username']) < 2:
            errors["username"] = "Username should be at least 2 characters"
        if len(postData['password']) < 6:
            errors['password'] = "Password needs to be at least 6 characters"
        if postData['password'] != postData['c_password']:
                errors['c_password'] = "passwords do not match"
                errors["password"] = "Password should be at least 6 characters"
        try:
            User.objects.get(email=postData['email'])
            print("hello!")
            errors['email_unique'] = 'That email address is already in use'
        except:
            pass
        try:
            User.objects.get(username = postData['username'])
            errors['username_unique'] = 'That username is already in use'
        except:
            pass
        return errors
    def job_validator(self, postData):
        errors={}
        if len(postData['title']) < 3:
            errors['title'] = "The job title must contain at least three characters!"
        if len(postData['description']) < 3:
            errors['description'] = "The job description must contain at least three characters!"
        if len(postData['location']) < 3:
            errors['location'] = "The job location must contain at least three characters!"
        return errors


class User(models.Model):
    username = models.CharField(max_length=55, default="NewUser")
    firstn = models.CharField(max_length=55, default="first name")
    namesuf = models.CharField(max_length=55, default="last name")
    email = models.EmailField(default="email")
    password = models.CharField(max_length=55)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = Showmanager()

class Blog (models.Model):
    blog_name = models.CharField(max_length=55)
    category = models.CharField(max_length=21)
    blog_creator = models.ForeignKey(User, related_name="user_who_created", on_delete=models.CASCADE)
    likes = models.ManyToManyField(, related_name="category_liked")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

class Blog_post (models.Model):
    blog_post_data = models.CharField(max_length=1000)
    blog_category = models.ForeignKey(Blog, related_name="category_of_blog", on_delete=models.CASCADE)
    blog_author = models.ForeignKey(Blog, related_name="author_of_blog", on_delete=models.CASCADE)
    blog_thread = models.ForeignKey(Blog, related_name="blog_name_thread", on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

class Blog_comments(models.Model):
    comment = models.CharField(max_length=256)
    comment_poster = models.ForeignKey(User, related_name="poster_username", on_delete=models.CASCADE)
    comment_blog = models.ForeignKey(Blog, related_name="blog_commented_on", on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)