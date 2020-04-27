from django.db import models


class Category(models.Model):
    title = models.CharField(max_length=150)
    summary = models.TextField(blank=True)
    main_image = models.ImageField(
        upload_to='Photos/Categories/%Y/%m/%d/', blank=True)

    def __str__(self):
        return self.title
