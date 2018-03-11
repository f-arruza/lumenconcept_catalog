import uuid

from django.db import models


class Category(models.Model):
    code = models.CharField('Code', max_length=20)
    name = models.CharField('Name', max_length=50)
    description = models.TextField('Description', blank=True)
    active = models.BooleanField('Active', default=True)

    def __str__(self):
        return self.name

    class Meta:
        db_table = 'category'
        verbose_name_plural = 'Categories'


class Catalog(models.Model):
    name = models.CharField('Name', max_length=50)
    banner = models.ImageField('Banner', upload_to='images/', blank=True)
    start_date = models.DateField('Start Date')
    end_date = models.DateField('End Date')
    description = models.TextField('Description', blank=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE,
                                 related_name='catalogs')
    provider = models.CharField('Provider', max_length=36)
    active = models.BooleanField('Active', default=True)

    def __str__(self):
        return self.name

    def clean(self):
        if self.end_date < self.start_date:
            raise ValidationError('The end date can not be before the start date')

    class Meta:
        db_table = 'catalog'
        verbose_name_plural = 'Catalogs'


class Tag(models.Model):
    name = models.CharField('Name', max_length=30)
    active = models.BooleanField('Active', default=True)

    def __str__(self):
        return self.name

    class Meta:
        db_table = 'tag'
        verbose_name_plural = 'Tags'


class Offer(models.Model):
    code = models.CharField('Code', max_length=36)
    title = models.CharField('Title', max_length=50)
    description = models.TextField('Description', blank=True)
    catalog = models.ForeignKey(Catalog, on_delete=models.CASCADE,
                                related_name='offers')
    price = models.DecimalField('Price', max_digits=20, decimal_places=2)
    reference_price = models.DecimalField('Reference Price', max_digits=20,
                                          decimal_places=2)
    stock = models.PositiveIntegerField('Stock', default=0)
    discount = models.DecimalField('Discount', max_digits=5, decimal_places=2,
                                   default=0.00)
    threshold = models.PositiveIntegerField('threshold', default=100)
    tags = models.ManyToManyField(Tag)
    active = models.BooleanField('Active', default=True)

    class Meta:
        db_table = 'offer'
        verbose_name_plural = 'Offers'

    def __str__(self):
        return self.catalog.name + ": " + self.title

    def clean(self):
        if self.reference_price < 0.00:
            raise ValidationError('The refence price can not be less than zero')
        if self.price < 0.00:
            raise ValidationError('The price can not be less than zero')
        if self.discount > 99:
            raise ValidationError('The discount can not be more than 99%')

    def save(self, *args, **kwargs):
        if self.price == 0.00 or self.reference_price == 0:
            discount = 0.00
        else:
            diff = self.reference_price - self.price
            discount = diff / self.reference_price
        self.discount = discount * 100

        if not self.id:
            self.code = uuid.uuid4()
        super(Offer, self).save(*args, **kwargs)


class MediaResource(models.Model):
    label = models.CharField('Label', max_length=30)
    path = models.ImageField('Path', upload_to='resources/')
    offer = models.ForeignKey(Offer, on_delete=models.CASCADE,
                              related_name='resources')

    def __str__(self):
        return self.label

    class Meta:
        db_table = 'media_resource'
        verbose_name_plural = 'MediaResources'


class OfferItem(models.Model):
    item = models.CharField('Item', max_length=50)
    count = models.PositiveIntegerField('Count', default=1)
    offer = models.ForeignKey(Offer, on_delete=models.CASCADE,
                              related_name='items')

    class Meta:
        db_table = 'offer_item'
        verbose_name_plural = 'OfferItems'

    def __str__(self):
        return self.offer.title + ": " + self.item
