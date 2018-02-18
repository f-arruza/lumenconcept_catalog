from django.db import models


class Category(models.Model):
    TYPE = (
        ('01', 'PRODUCT'),
        ('02', 'SERVICE'),
    )

    code = models.CharField('Code', max_length=20, blank=False, null=False)
    name = models.CharField('Name', max_length=50, blank=False)
    description = models.TextField('Description', blank=True)
    type = models.CharField('Type', max_length=2, choices=TYPE, default='01',
                            blank=False
                           )
    active = models.BooleanField('Active', default=True)

    def __str__(self):
        return self.name

    class Meta:
        db_table = 'category'
        verbose_name_plural = 'Categories'


class Tag(models.Model):
    name = models.CharField('Name', max_length=30, blank=False)
    active = models.BooleanField('Active', default=True)

    def __str__(self):
        return self.name

    class Meta:
        db_table = 'tag'
        verbose_name_plural = 'Tags'


class Item(models.Model):
    code = models.CharField('Code', max_length=20, blank=False, null=False)
    name = models.CharField('Name', max_length=50, blank=False)
    description = models.TextField('Description', blank=True)
    image = models.ImageField('Image', upload_to='images/', null=True)
    score = models.DecimalField('Score', max_digits=3,
                                 decimal_places=2, default=0.00,
                                 blank=False
                               )
    price = models.DecimalField('Price', max_digits=20, decimal_places=2,
                                default=0.00, blank=False
                               )
    provider_id = models.CharField('Provider', max_length=40, blank=False, null=False)
    category = models.ForeignKey(Category, on_delete=models.CASCADE,
                                    related_name='items',
                                    blank=False,
                                    null=False
                                )
    tags = models.ManyToManyField(Tag)
    active = models.BooleanField('Active', default=True)

    def __str__(self):
        return self.name

    class Meta:
        db_table = 'item'
        verbose_name_plural = 'Items'
