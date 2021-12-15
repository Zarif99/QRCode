from django.db import models
from django.urls import reverse
from django.utils.text import slugify
from time import time
from io import BytesIO
from django.core.files import File
from PIL import Image
from django.conf import settings
from qrcode import make


def gen_slug(s):
    new_slug = slugify(s, allow_unicode=True)
    return new_slug + '-' + str(int(time()))


SELECTIVE_STATUS = [
    ('Обнаружено', 'Обнаружено'),
    ('Не обнаружено', 'Не обнаружено'),

]
GENDER = [
    ('мужской', 'мужской'),
    ('женщина', 'женщина'),

]


class Customer(models.Model):
    slug = models.SlugField(max_length=50, unique=True)
    full_name = models.CharField(max_length=50)
    date_delivery = models.DateTimeField(auto_now_add=True)
    selective_status = models.CharField(choices=SELECTIVE_STATUS, max_length=20)
    image = models.ImageField(upload_to='images/')

    # create new1
    result_date = models.DateTimeField()
    date_of_birth = models.DateField()
    gender = models.CharField(choices=GENDER, max_length=20)
    address = models.CharField(max_length=50)

    # create new2
    id_service = models.CharField(max_length=20, unique=True)
    biomaterial_date = models.CharField(max_length=25)

    def str(self):
        return self.full_name

    def get_absolute_url(self):
        return reverse('customer_detail', kwargs={'slug': self.slug})

    def save(self, *args, **kwargs):
        if not self.id:
            self.slug = gen_slug(self.full_name)

        qr_image = make(f'{settings.DOMAIN}/{self.slug}')
        qr_offset = Image.new('RGB', (400, 390), 'white')
        qr_offset.paste(qr_image)
        file_name = f'{self.full_name}qr.png'
        stream = BytesIO()
        qr_offset.save(stream, 'PNG')
        self.image.save(file_name, File(stream), save=False)
        qr_offset.close()
        super().save(*args, **kwargs)
