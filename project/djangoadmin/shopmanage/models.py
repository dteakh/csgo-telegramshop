from django.db import models


class Time(models.Model):
    class Meta:
        abstract = True

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class Users(Time):
    class Meta:
        verbose_name = 'Пользователи'
        verbose_name_plural = 'Пользователи'

    id = models.AutoField(primary_key=True)
    user_id = models.BigIntegerField(unique=True)
    feedback_rate = models.CharField(max_length=20, null=True)
    feedback_text = models.CharField(max_length=150, null=True)
    purchased = models.IntegerField(default=0)
    trade_link = models.CharField(max_length=150, null=True)

    def __str__(self):
        return f'{self.id} покупок: {self.purchased}'


QUALITY_CHOICES = [
    ('закалённое в боях', 'bs'),
    ('поношенное', 'ww'),
    ('после полевых испытаний', 'ft'),
    ('немного поношенное', 'mw'),
    ('прямо с завода', 'fn'),
]

TYPE_CHOICES = [
    ('снайперская винтовка', 'sniper'),
    ('штурмовая винтовка', 'rifle'),
    ('пистолет-пулемёт', 'smg'),
    ('пистолет', 'pistol'),
    ('нож', 'knife'),
    ('перчатки', 'gloves'),
    ('дробовик', 'shotgun'),
    ('прочее', 'other'),
]


class Items(Time):
    class Meta:
        verbose_name = 'Предмет'
        verbose_name_plural = 'Предметы'

    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100)
    quality = models.CharField(max_length=30, choices=QUALITY_CHOICES)
    item_float = models.FloatField()
    item_type = models.CharField(max_length=30, choices=TYPE_CHOICES)
    price = models.FloatField()
    picture = models.ImageField(upload_to='shopmanage/images')

    def __str__(self):
        return f'{self.id}: {self.name}'



class Purchases(Time):
    class Meta:
        verbose_name = 'Покупка'
        verbose_name_plural = 'Покупки'

    id = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=100)
    price = models.FloatField()
    buyer_id = models.BigIntegerField()
    buyer_link = models.CharField(max_length=150)
    delivered = models.BooleanField(default=False)

    def __str__(self):
        return f'{self.id} bought by {self.buyer_id}'

