from django.contrib.auth.models import User
from django.utils import timezone
import pathlib
from django.core.files.storage import FileSystemStorage
from django.db import models
from django.conf import settings
from django.urls import reverse
import stripe


from django.utils import timezone


# Create your models here.

STRIPE_SECRET_KEY = "sk_test_51PbVREDUVZyD9P5hMx44bCmUwBMlf0xjyLHEGrCliSwPrcyADzuH7RtHmfmtDWacsjoYuUcHgauWBrFTHFZHx6lP00yxOBc8hs"
stripe.api_key = STRIPE_SECRET_KEY


PROTECTED_MEDIA_ROOT = settings.PROTECTED_MEDIA_ROOT
protected_storage = FileSystemStorage(location=str(PROTECTED_MEDIA_ROOT))


class ClasificacionPadre(models.Model):
    nombre = models.CharField(max_length=120)
    image = models.ImageField(upload_to="clasificacion/", blank=True, null=True)

    def __str__(self):
        return self.nombre


class ClasificacionHija(models.Model):
    nombre = models.CharField(max_length=120)
    padre = models.ForeignKey(ClasificacionPadre, on_delete=models.CASCADE, related_name='hijos')

    def __str__(self):
        return f"{self.padre.nombre} > {self.nombre}"

class ClasificacionNieta(models.Model):
    nombre = models.CharField(max_length=120)
    padre = models.ForeignKey(ClasificacionHija, on_delete=models.CASCADE, related_name='nietos')

    def __str__(self):
        return f"{self.padre.padre.nombre} > {self.padre.nombre} > {self.nombre}"

class Product(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, default=1, on_delete=models.CASCADE
    )
    description = models.TextField(blank=True, null=True)
    short_description = models.CharField(max_length=150, blank=True, null=True)
    stripe_product_id = models.CharField(max_length=220, blank=True, null=True)
    supply = models.IntegerField(default=1)
    image = models.ImageField(upload_to="products/", blank=True, null=True)
    name = models.CharField(max_length=120)
    clasificacion = models.ManyToManyField(
        ClasificacionHija, blank=True, related_name="pro"
    )
    keywords = models.TextField(blank=True, null=True)

    clasificaciones_padre = models.ForeignKey(
        ClasificacionPadre, on_delete=models.CASCADE, related_name="productos_padre",default=1
    )
    clasificaciones_nieta = models.ManyToManyField(
        ClasificacionNieta, blank=True, related_name="productos_nietos"
    )
    handle = models.SlugField(unique=True)  # slug
    price = models.DecimalField(max_digits=10, decimal_places=2, default=9.99)
    og_price = models.DecimalField(max_digits=10, decimal_places=2, default=9.99)
    stripe_price_id = models.CharField(max_length=220, blank=True, null=True)
    stripe_price = models.IntegerField(default=999)  # 100 * price
    price_changed_timestamp = models.DateTimeField(
        auto_now=False, auto_now_add=False, blank=True, null=True
    )
    active = models.BooleanField(default=True)
    timestamp = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def usuarios_que_dieron_like(self):
        return [like.user for like in self.like.all()]

    @property
    def display_name(self):
        return self.name+" | "+self.handle

    @property
    def display_price(self):
        return self.price

    def __str__(self):
        return self.display_name


    def save(self, *args, **kwargs):
        if self.name:
            stripe_product_r = stripe.Product.create(name=self.name)
            self.stripe_product_id = stripe_product_r.id
        if not self.stripe_price_id:
            stripe_price_obj = stripe.Price.create(
                product=self.stripe_product_id,
                unit_amount=self.stripe_price,
                currency="usd",
            )
            self.stripe_price_id = stripe_price_obj.id
        if self.price != self.og_price:
            # price changed
            self.og_price = self.price
            # trigger an API request for the price
            self.stripe_price = int(self.price * 100)
            if self.stripe_product_id:
                stripe_price_obj = stripe.Price.create(
                    product=self.stripe_product_id,
                    unit_amount=self.stripe_price,
                    currency="usd",
                )
                self.stripe_price_id = stripe_price_obj.id
            self.price_changed_timestamp = timezone.now()
        if self.keywords:
            self.keywords = ', '.join([keyword.strip().lower() for keyword in self.keywords.split(',')])
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse("products:detail", kwargs={"handle": self.handle})

    def get_manage_url(self):
        return reverse("products:manage", kwargs={"handle": self.handle})



class RatingProduct(models.Model):
    product = models.OneToOneField(Product, on_delete=models.CASCADE, related_name='rating_product')
    average_rating = models.DecimalField(max_digits=3, decimal_places=2, default=0.00)

    def update_average_rating(self):
        ratings = Rating.objects.filter(average=self)
        if ratings.exists():
            total_score = 0
            for ratin in ratings:
                total_score = total_score + ratin.score
            self.average_rating = total_score / ratings.count()
        else:
            self.average_rating = 0
        self.save()


class Rating(models.Model):
    average = models.ForeignKey(Rating_product, on_delete=models.CASCADE, related_name='average',default=1)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    score = models.PositiveIntegerField()  # Suponiendo que el rating va de 1 a 5

    class Meta:
        unique_together = ('average', 'user')  # Un usuario solo puede evaluar un producto una vez




class ProductView(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True)  # Opcional, si deseas rastrear usuarios
    timestamp = models.DateTimeField(auto_now_add=True)

class ProductOffer(models.Model):
    product = models.OneToOneField(Product, on_delete=models.CASCADE, related_name='offer')
    precio_nuevo = models.DecimalField(max_digits=10, decimal_places=2)
    precio_viejo = models.DecimalField(max_digits=10, decimal_places=2)
    start_date = models.DateTimeField()
    end_date = models.DateTimeField(null=True, blank=True)
    is_active = models.BooleanField(default=False)
    is_premium = models.BooleanField(default=False)  # Nuevo campo para ofertas premium


    def __str__(self):
        return self.product.name
    def descuento(self):
        porciento_descuento = round((self.precio_nuevo * 100 / self.precio_viejo) - 100, 1)
        return porciento_descuento

    def is_offer_active(self):
        now = timezone.now()
        print(self.product)
        if self.start_date <= now and (self.end_date is None or self.end_date >= now) and not self.is_active:
            # La oferta está activa, actualiza los precios del producto
            self.product.price = self.precio_nuevo
            self.product.save()
            self.save()
            self.is_active = True
            self.save()
            # print("es true con cambios")
            return True

        if self.is_active and self.start_date <= now and (self.end_date is None or self.end_date >= now):
            # print("es true sin cambios")
            return True

        if self.end_date is not None and self.end_date < now:
            self.product.price = self.precio_viejo
            self.product.save()
            self.delete()
            # print("es false con cambios")
            return False
        self.is_active = False
        self.save()
        # print("es false sin cambios")
        return False

    def eliminar_oferta(self):
        if self.is_offer_active() == True:
            self.product.price = self.precio_viejo
            self.product.save()
            self.delete()
        else:
            self.delete()

    def get_time_remaining(self):
        now = timezone.now()
        if self.end_date is None:
            return "Oferta sin fecha de finalización definida"

        if self.end_date is not None and self.end_date > now:
            time_remaining = self.end_date - now
            days, seconds = time_remaining.days, time_remaining.seconds
            hours = seconds // 3600
            minutes = (seconds % 3600) // 60
            return {
                'days': days,
                'hours': hours,
                'minutes': minutes,
            }
        return None  # La oferta ya ha terminado







def handle_product_attachment_upload(instance, filename):
    return f"products/{instance.product.handle}/attachements/{filename}"

class ProductImage(models.Model):
    product =models.ForeignKey(Product, on_delete=models.CASCADE)
    name = models.CharField(max_length=120,null=True,blank=True)
    file = models.FileField(upload_to=handle_product_attachment_upload, storage= protected_storage )
    is_free = models.BooleanField(default=False)
    active = models.BooleanField(default=True)
    timestamp = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def save(self, *args, **kwargs):
        if not self.name:
            self.name = pathlib.Path(self.file.name).name # stem , suffix
        super().save(*args,**kwargs)

    @property
    def display_name(self):
        return self.name or pathlib.Path(self.file.name).name

    def get_download_url(self):
        # return f"products/{self.product.handle}/download/{self.pk}/"
        return reverse("products:download",kwargs={"handle": self.product.handle, "pk":self.pk})



class Likes(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE,related_name='like')
    timestamp = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ['user', 'product']  # Un usuario solo puede dar like a un producto una vez

