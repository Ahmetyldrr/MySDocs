***Soru:*** django projelerinde normal tasarım ve otomaitk view kullanmanın farkı nedir

**Cevap:** Django projelerinde **normal tasarım** (manüel view'lar) ve **otomatik view'lar** (örneğin Django'nun generic class-based view'ları veya DRF'nin ViewSet'leri) arasında temel fark, **esneklik** ve **hızlı geliştirme** arasındaki dengedir. İşte bu iki yaklaşım arasındaki farkları detaylı bir şekilde açıklıyorum:

---

### **1. Normal Tasarım (Manüel View'lar)**
Bu yaklaşımda, view'larınızı kendiniz yazar ve her bir isteği ayrıntılı olarak kontrol edersiniz.

#### **Avantajları**
- **Tam Kontrol:** İsteği alıp, işleyip, istediğiniz herhangi bir çıktıyı döndürebilirsiniz. API, HTML, dosya veya başka bir şey.
- **Esneklik:** Karmaşık iş mantıklarını kolayca ekleyebilir ve her aşamayı özelleştirebilirsiniz.
- **Mantık Ayrımı:** Çok özgün ve farklı işlemler gerektiren projelerde daha iyi sonuç verir.

#### **Dezavantajları**
- **Daha Fazla Kod Yazma:** Her view için benzer kodları tekrar tekrar yazmanız gerekebilir (örneğin `GET`, `POST` işlemleri).
- **Hata Yapma Riski:** Tüm işlemleri kendiniz kodlarken, hataya açık bir süreç olabilir.
- **Yavaş Geliştirme:** Özellikle CRUD operasyonlarında, manüel yazım zaman kaybettirebilir.

---

### **2. Otomatik View'lar (Generic Class-Based View veya ViewSet Kullanımı)**
Django'nun generic class-based view'ları (örneğin `ListView`, `CreateView`) ve Django REST Framework (DRF) gibi frameworklerdeki ViewSet'ler, tekrarlayan işlemleri sizin için otomatikleştirir.

#### **Avantajları**
- **Hızlı Geliştirme:** CRUD operasyonları gibi yaygın işlemler birkaç satır kodla tamamlanabilir.
  - Örneğin bir `CreateView` veya `ModelViewSet`, form işlemleri veya API endpoint'leri oluşturmayı hızlandırır.
- **Yeniden Kullanılabilirlik:** Aynı yapıdaki işlemleri tekrar tekrar yazmanız gerekmez.
- **Django'nun Standartlarına Uygunluk:** Otomatik işlemler, Django'nun en iyi uygulamalarına (best practices) göre hazırlanmıştır.

#### **Dezavantajları**
- **Sınırlı Esneklik:** Eğer default davranışı değiştirmek isterseniz, bazen fazla "override" yapmanız gerekebilir. Bu, kodun karmaşıklaşmasına neden olabilir.
- **Daha Az Kontrol:** Django'nun sizin için yaptığı birçok işlem "arka planda" gerçekleşir, bu yüzden tam olarak ne olduğunu anlamak zor olabilir.
- **Basit İşlemlerde Avantajlı:** Karmaşık ve çok özel bir iş mantığı gerekiyorsa, generic view'lar yetersiz kalabilir.

---

### **Karşılaştırmalı Tablo**

| **Kriter**              | **Normal Tasarım**         | **Otomatik View'lar**         |
|--------------------------|----------------------------|--------------------------------|
| **Kod Yazma Miktarı**    | Fazla                     | Az                            |
| **Hızlı Geliştirme**     | Düşük                    | Yüksek                        |
| **Esneklik**             | Yüksek                   | Orta                          |
| **Öğrenme Eğrisi**       | Kolay                    | Orta                          |
| **Hata Riski**           | Yüksek                   | Düşük                         |
| **Karmaşık İş Mantığı**  | Daha uygun               | Zor uygulanabilir             |

---

### **Ne Zaman Hangisi Kullanılmalı?**
1. **Normal Tasarım (Manüel View'lar):**
   - Eğer projede özel iş mantıkları, çok fazla özelleştirme veya API işlemleri arasında karmaşık bağlantılar varsa tercih edilir.
   - Örneğin, bir ödeme sistemi veya özel bir raporlama uygulaması.

2. **Otomatik View'lar (Generic View'lar veya ViewSet'ler):**
   - CRUD operasyonları, basit API endpoint'leri veya Django’nun standart form işleme yapısıyla uyumlu basit projelerde tercih edilir.
   - Örneğin, bir blog sistemi veya kullanıcı yönetimi.

---

Sonuç olarak, **projeye ve ihtiyaçlara göre** bu iki yaklaşımı birleştirerek kullanmak en iyi yöntemdir. Eğer esneklik ve özelleştirme gerekiyorsa normal tasarım; hız ve standart işlemler gerekiyorsa otomatik view'lar tercih edilmelidir. 🔨🤖

***Soru:*** django tasarımında admin sayfasını özelleştirme istersem ne yapabilriim

**Cevap:** Django'da **admin sayfasını özelleştirmek**, genellikle projeye özgü ihtiyaçlara ve kullanıcı deneyimini geliştirmeye yönelik yapılır. Django admin, esnek bir yapıya sahip olduğu için birçok farklı özelleştirme yapabilirsiniz.

### Admin Sayfasını Özelleştirme Yöntemleri

---

#### **1. Admin Panel Başlığını ve Meta Verileri Özelleştirme**
Admin panelinin üst kısmındaki başlıkları ve meta bilgilerini değiştirebilirsiniz.

**`admin.py` Dosyasında:**
```python
from django.contrib import admin

admin.site.site_header = "Özel Yönetim Paneli"  # Üst başlık
admin.site.site_title = "Yönetim Paneli"         # Tarayıcı sekme başlığı
admin.site.index_title = "Admin Anasayfası"     # Admin ana sayfa başlığı
```

---

#### **2. Model Görünümlerini Özelleştirme**
Admin panelinde modellerin görünümünü daha kullanıcı dostu yapmak için `ModelAdmin` sınıfını kullanabilirsiniz.

##### **Alanları Özelleştirme (`list_display`, `list_filter`, vs.):**
```python
from django.contrib import admin
from .models import Product

class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'price', 'stock')  # Liste sayfasında gösterilecek alanlar
    list_filter = ('category',)               # Sağda filtreleme seçenekleri
    search_fields = ('name', 'description')   # Arama kutusu
    ordering = ('-created_at',)               # Varsayılan sıralama
    readonly_fields = ('created_at',)         # Düzenlenemez alanlar
    list_editable = ('price', 'stock')        # Liste sayfasında düzenlenebilir alanlar

admin.site.register(Product, ProductAdmin)
```

---

#### **3. Form Alanlarını Özelleştirme**
Admin'deki formlarını özel hale getirmek için `form` veya `fieldsets` kullanabilirsiniz.

##### **Form Alanlarının Sıralanması (`fieldsets`):**
```python
class ProductAdmin(admin.ModelAdmin):
    fieldsets = (
        ("Temel Bilgiler", {
            'fields': ('name', 'category', 'price')
        }),
        ("Stok ve Tarihler", {
            'fields': ('stock', 'created_at'),
            'classes': ('collapse',),  # Varsayılan olarak gizli
        }),
    )
admin.site.register(Product, ProductAdmin)
```

##### **Form Özelleştirme:**
Django'nun `forms` modülünü kullanarak özel validasyonlar veya alanlar ekleyebilirsiniz.

```python
from django import forms
from .models import Product

class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = '__all__'

    def clean_price(self):
        price = self.cleaned_data.get('price')
        if price < 0:
            raise forms.ValidationError("Fiyat negatif olamaz!")
        return price

class ProductAdmin(admin.ModelAdmin):
    form = ProductForm

admin.site.register(Product, ProductAdmin)
```

---

#### **4. Inline Modeller**
Bir modele bağlı başka bir modeli aynı sayfada düzenlemek için kullanılır.

```python
from .models import Order, OrderItem

class OrderItemInline(admin.TabularInline):  # StackedInline de kullanılabilir
    model = OrderItem
    extra = 1  # Boş ekleme alanı sayısı

class OrderAdmin(admin.ModelAdmin):
    inlines = [OrderItemInline]

admin.site.register(Order, OrderAdmin)
```

---

#### **5. Özel Admin Görünümleri**
Admin'de özel bir görünüm oluşturabilirsiniz (örneğin, belirli bir raporu göstermek).

**`admin.py` Dosyasında:**
```python
from django.urls import path
from django.http import HttpResponse
from django.contrib import admin

class CustomAdminView(admin.ModelAdmin):
    def get_urls(self):
        urls = super().get_urls()
        custom_urls = [
            path('custom-report/', self.custom_report)
        ]
        return custom_urls + urls

    def custom_report(self, request):
        # Özel rapor veya içerik döndürün
        return HttpResponse("Bu özel bir rapordur.")

admin.site.register(SomeModel, CustomAdminView)
```

---

#### **6. Admin Temasını Değiştirme**
Django'nun varsayılan admin temasını CSS ve JavaScript ile özelleştirebilirsiniz.

##### **Statik Dosyalar ve Şablonları Değiştirme:**
1. **Statik Dosyaları Ekleyin:**
   Admin paneline özel CSS veya JS eklemek için `static/admin/css/` veya `static/admin/js/` altına dosyalar koyun.

2. **Şablonları Geçersiz Kılın:**
   `templates/admin/` klasöründe Django admin için özel şablonlar oluşturabilirsiniz.
   Örneğin, **`templates/admin/base_site.html`**:
   ```html
   {% extends "admin/base.html" %}

   {% block title %}Özel Admin Başlığı{% endblock %}
   {% block branding %}
       <h1>Özel Yönetim Paneli</h1>
   {% endblock %}
   ```

---

#### **7. Üçüncü Parti Araçlar Kullanma**
Daha fazla özelleştirme istiyorsanız şu paketler çok faydalı olabilir:
- **[django-grappelli](https://django-grappelli.readthedocs.io/):** Admin paneline daha modern bir tasarım ekler.
- **[django-suit](https://djangosuit.com/):** Bootstrap tabanlı bir admin teması sağlar.
- **[django-import-export](https://django-import-export.readthedocs.io/):** CSV, Excel veya diğer dosya türlerinden veri import/export işlemleri.

---

### **Sonuç**
Django admin panelini özelleştirmek, hem tasarım hem de işlevsellik açısından büyük avantaj sağlar. İhtiyacınıza bağlı olarak:
- Küçük değişiklikler için `ModelAdmin`'i özelleştirin.
- Geniş kapsamlı özelleştirmeler için statik dosyalar ve şablonları geçersiz kılın.
- İhtiyaç duyduğunuzda üçüncü parti araçlardan destek alın. 

Her şey sizin kullanıcılarınızın ihtiyacına ve projenizin kapsamına bağlı! 😊

***Soru:*** django modellerinde temel yapıdan farklı bir tasarım nasıl yapılır

**Cevap:** Django modellerinde, temel yapıdan farklı bir tasarım yapmak, genellikle daha karmaşık veri yapıları, özel davranışlar veya projenin gereksinimlerine göre veritabanı etkileşimlerini özelleştirmek anlamına gelir. Django'nun model mimarisi oldukça esnek olduğu için, aşağıda belirttiğim yöntemlerle bu özelleştirmeleri yapabilirsiniz.

---

## **Django Modellerinde Farklı Tasarım Yöntemleri**

---

### **1. Model Mirası Kullanımı**
Django modellerinde miras kullanarak daha organize bir yapı oluşturabilirsiniz.

#### **Soyut Baz Model**
Soyut bir model oluşturup, diğer modellerin tekrar eden alanlarını bu modelde tutabilirsiniz.

```python
from django.db import models

class BaseModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True

class Product(BaseModel):
    name = models.CharField(max_length=255)
    price = models.DecimalField(max_digits=10, decimal_places=2)

class Category(BaseModel):
    title = models.CharField(max_length=255)
```

- **Avantajı:** Kod tekrarını azaltır ve daha temiz bir yapı sağlar.
- **Not:** Soyut modeller veritabanında bir tablo oluşturmaz, sadece diğer modeller için şablon görevi görür.

---

#### **Proxy Modeller**
Var olan bir modelin işlevselliğini değiştirmek için kullanılır. Yeni bir tablo oluşturmaz, mevcut tablodaki verilere farklı bir davranış ekler.

```python
class PublishedProductManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(is_published=True)

class PublishedProduct(Product):  # Proxy modeli
    objects = PublishedProductManager()

    class Meta:
        proxy = True
        ordering = ['-price']

# Kullanım
published_products = PublishedProduct.objects.all()
```

- **Avantajı:** Mevcut modeli değiştirmeden farklı sorgu mantıkları eklenebilir.
- **Not:** Proxy modelleri yeni alanlar ekleyemez.

---

#### **Multi-Table Mirası**
Bir modelin her bir alt sınıfını ayrı bir tabloda saklamak için kullanılır.

```python
class BaseContent(models.Model):
    title = models.CharField(max_length=255)

class Article(BaseContent):
    content = models.TextField()

class Video(BaseContent):
    video_url = models.URLField()
```

- **Avantajı:** Her modelin kendi tablosu olur, ilişkiler net şekilde ayrışır.
- **Not:** Çok tablalı sorgular biraz daha karmaşık ve maliyetli olabilir.

---

### **2. Özel Alanlar ve Validasyon**
Django'nun hazır alanlarını kullanmak yerine kendi özel alanlarınızı oluşturabilirsiniz.

#### **Özel Model Alanı**
Kendi alan tipinizi yazmak için `Field` sınıfını genişletin.

```python
from django.db import models

class PositiveIntegerField(models.IntegerField):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def validate(self, value, model_instance):
        if value < 0:
            raise ValueError("Değer negatif olamaz!")
        super().validate(value, model_instance)

class Product(models.Model):
    name = models.CharField(max_length=255)
    stock = PositiveIntegerField()
```

- **Avantajı:** Özel davranışları doğrudan alan seviyesinde tanımlayabilirsiniz.

---

#### **Özel Validasyon**
Alanlar veya model seviyesinde özel validasyon kuralları ekleyebilirsiniz.

```python
from django.core.exceptions import ValidationError

class Product(models.Model):
    name = models.CharField(max_length=255)
    price = models.DecimalField(max_digits=10, decimal_places=2)

    def clean(self):
        if self.price <= 0:
            raise ValidationError("Fiyat sıfır veya negatif olamaz.")
```

- **Not:** `clean()` metodu model düzeyindeki validasyonları ekler ve genellikle admin paneli/form işlemleriyle birlikte çalışır.

---

### **3. Özelleştirilmiş Manager ve QuerySet Kullanımı**
Özel `Manager` ve `QuerySet`'lerle sorguları özelleştirebilirsiniz.

#### **Özel Manager:**
```python
class PublishedManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(is_published=True)

class Product(models.Model):
    name = models.CharField(max_length=255)
    is_published = models.BooleanField(default=False)

    objects = models.Manager()  # Varsayılan
    published = PublishedManager()  # Özel
```

- Kullanım:
  ```python
  Product.published.all()  # Sadece yayımlanmış ürünler
  ```

#### **Özel QuerySet:**
Daha fazla özelleştirme için `QuerySet` oluşturabilirsiniz.

```python
class ProductQuerySet(models.QuerySet):
    def expensive(self):
        return self.filter(price__gt=100)

class Product(models.Model):
    name = models.CharField(max_length=255)
    price = models.DecimalField(max_digits=10, decimal_places=2)

    objects = ProductQuerySet.as_manager()
```

- Kullanım:
  ```python
  Product.objects.expensive()
  ```

---

### **4. Özel Veritabanı İlişkileri**
#### **Many-to-Many İlişkilerini Özelleştirme:**
Ara tabloyu manuel olarak tanımlayabilirsiniz.

```python
class Membership(models.Model):
    person = models.ForeignKey('Person', on_delete=models.CASCADE)
    group = models.ForeignKey('Group', on_delete=models.CASCADE)
    date_joined = models.DateField()
    is_admin = models.BooleanField(default=False)

class Person(models.Model):
    name = models.CharField(max_length=255)
    groups = models.ManyToManyField('Group', through='Membership')

class Group(models.Model):
    name = models.CharField(max_length=255)
```

---

### **5. Sinyaller Kullanımı**
Model davranışlarını özelleştirmek için Django sinyallerini kullanabilirsiniz.

```python
from django.db.models.signals import pre_save
from django.dispatch import receiver

@receiver(pre_save, sender=Product)
def update_stock(sender, instance, **kwargs):
    if instance.stock < 0:
        instance.stock = 0
```

---

### **6. Veri Tabanı Optimize Edici Tasarım**
#### **Index Kullanımı:**
Veritabanı sorgularını hızlandırmak için alanlara indeks ekleyebilirsiniz.

```python
class Product(models.Model):
    name = models.CharField(max_length=255, db_index=True)  # İndeks ekleme
    price = models.DecimalField(max_digits=10, decimal_places=2)

    class Meta:
        indexes = [
            models.Index(fields=['price']),
        ]
```

#### **Custom SQL Kullanımı:**
Daha karmaşık sorgular için doğrudan SQL kullanabilirsiniz.

```python
from django.db import connection

def get_custom_data():
    with connection.cursor() as cursor:
        cursor.execute("SELECT * FROM product WHERE price > %s", [100])
        return cursor.fetchall()
```

---

### **Sonuç**
Django modellerinde temel yapıdan farklı bir tasarım için:
1. **Miras yapısını ve soyut modelleri** kullanarak kodunuzu düzenleyebilirsiniz.
2. **Özel validasyonlar, alanlar ve QuerySet** ile davranışları özelleştirebilirsiniz.
3. **Veritabanı performansını artırmak için** indeksler ve optimize edilmiş sorgular ekleyebilirsiniz.

İhtiyacınıza göre bu yöntemleri birleştirerek, projenize en uygun model tasarımını oluşturabilirsiniz. 💡