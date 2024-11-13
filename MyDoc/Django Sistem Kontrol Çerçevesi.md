***Soru:*** 6.2 System check framework
The system check framework is a set of static checks for validating Django projects. It detects common problems and
provides hints for how to fix them. The framework is extensible so you can easily add your own checks.
For details on how to add your own checks and integrate them with Django’s system checks, see the System check
topic guide.
6.2.1 API reference
CheckMessage
class CheckMessage(level, msg, hint=None, obj=None, id=None)
The warnings and errors raised by system checks must be instances of CheckMessage. An instance encapsulates a
single reportable error or warning. It also provides context and hints applicable to the message, and a unique identifier
that is used for filtering purposes.
Constructor arguments are:   bu kısımla başlayan django doküman ı nelerden  bahsediyor

**Cevap:** Bu bölüm, Django'nun "System check framework" (Sistem kontrol çerçevesi) hakkında bilgi veriyor. **Django dokümanı**, aşağıdaki konuları ele alıyor:

1. **System check framework**: Django projelerini statik kontrollerle doğrulamak için kullanılan bir sistemdir. Bu sistem, yaygın sorunları algılayıp, nasıl düzeltileceğine dair ipuçları sunar.
  
2. **Çerçevenin genişletilebilirliği**: Geliştiriciler kendi özel kontrollerini ekleyebilir ve bunları Django'nun mevcut kontrolleriyle entegre edebilir. Bu, çerçevenin esnek ve özelleştirilebilir olduğunu gösterir.

3. **CheckMessage Sınıfı**: 
    - Bu sınıf, sistem kontrolleri sırasında ortaya çıkan uyarı veya hataları temsil eder.
    - Bir hata veya uyarı mesajını tek bir nesne içinde kapsar ve mesajla ilgili ipuçları, objeler ve benzersiz bir kimlik sağlar.
    - Bu benzersiz kimlikler, kontrollerin filtrelenmesi için kullanılabilir.

4. **CheckMessage Yapıcı Parametreleri**:
    - `level`: Uyarı veya hata seviyesi.
    - `msg`: Verilen mesajın kendisi.
    - `hint`: Mesajı çözmek için ipucu.
    - `obj`: Mesajla ilgili olan nesne (varsa).
    - `id`: Kontrol kimliği, mesajların ayırt edilebilmesi için kullanılır.

Bu çerçeve, projelerdeki yaygın hataları tespit etmek için güçlü bir araçtır ve geliştiricilerin projelerini daha kararlı ve güvenli hale getirmesine yardımcı olur.

***Soru:*** level The severity of the message. Use one of the predefined values: DEBUG, INFO, WARNING, ERROR,
CRITICAL. If the level is greater or equal to ERROR, then Django will prevent management commands from
executing. Messages with level lower than ERROR (i.e. warnings) are reported to the console, but can be
silenced.
msg A short (less than 80 characters) string describing the problem. The string should not contain newlines.
hint A single-line string providing a hint for fixing the problem. If no hint can be provided, or the hint is self-evident
from the error message, the hint can be omitted, or a value of None can be used.
obj Optional. An object providing context for the message (for example, the model where the problem was discovered).
The object should be a model, field, or manager or any other object that defines a __str__() method.
The method is used while reporting all messages and its result precedes the message.
id Optional string. A unique identifier for the issue. Identifiers should follow the pattern applabel.X001, where
X is one of the letters CEWID, indicating the message severity (C for criticals, E for errors and so). The number
can be allocated by the application, but should be unique within that application.
There are subclasses to make creating messages with common levels easier. When using them you can omit the level
argument because it is implied by the class name.
class Debug(msg, hint=None, obj=None, id=None)
class Info(msg, hint=None, obj=None, id=None)
class Warning(msg, hint=None obj=None, id=None)
class Error(msg, hint=None, obj=None, id=None)
class Critical(msg, hint=None, obj=None, id=None)  bunları tek tek açıklar mısın ve nasıl kullanacağım

**Cevap:** Django’nun **System Check Framework** ile ilgili `CheckMessage` sınıfı ve alt sınıfları, sistem kontrolleri sırasında uyarı ve hata mesajlarını raporlamanıza yardımcı olur. Bu mesajların nasıl oluşturulacağını ve farklı bileşenlerin ne anlama geldiğini tek tek açıklayalım:

### `level` (Seviye)
- Mesajın ciddiyetini belirtir.
- **Önceden tanımlanmış değerler:**
  - **DEBUG**: Geliştirme sırasında faydalı olabilecek düşük öncelikli mesajlar.
  - **INFO**: Genel bilgi sağlayan mesajlar.
  - **WARNING**: Uyarılar, genellikle düzeltilmesi gereken potansiyel sorunlar.
  - **ERROR**: Ciddi bir hata, işlem yürütülmeden önce düzeltilmesi gerekir.
  - **CRITICAL**: Çok önemli bir hata, uygulamanın çalışmasını engelleyebilir.

  **Kullanım örneği**: 
  Eğer mesajın seviyesi `ERROR` veya daha üstü bir değer (ERROR, CRITICAL) ise, Django bu mesajı oluşturduğunda ilgili yönetim komutları çalıştırılamaz. Daha düşük seviyelerdeki mesajlar (`WARNING`, `INFO`, `DEBUG`) yalnızca konsola rapor edilir ve komutların yürütülmesini engellemez. 

### `msg` (Mesaj)
- **Kısa ve öz bir açıklama sağlar (80 karakterden az)**.
- Yeni satır karakterleri içermez.
- Sorunu açıklamak için kullanılır.

  **Kullanım örneği**:
  ```python
  msg = "Database connection is missing."
  ```

### `hint` (İpucu)
- **Tek satırlık bir öneri** sunar, sorunun nasıl çözülebileceğine dair ipucu verir.
- Eğer ipucu belirgin ise veya verilemiyorsa, `None` olabilir.

  **Kullanım örneği**:
  ```python
  hint = "Check if the database configuration is correct in settings."
  ```

### `obj` (Nesne - Opsiyonel)
- Mesajın bağlamını sağlayan nesnedir. Örneğin, hata bir model veya alan ile ilgiliyse, bu model veya alanı `obj` parametresi ile mesaj bağlamında kullanabilirsiniz.
- Nesne, `__str__()` metodunu tanımlamış olmalıdır, böylece raporlama sırasında bu metodun sonucu mesajın önüne eklenir.

  **Kullanım örneği**:
  ```python
  obj = my_model_instance  # Hatanın ilgili olduğu model veya obje
  ```

### `id` (Kimlik - Opsiyonel)
- Mesajın **benzersiz bir kimliği**. Bu kimlikler, mesajları tanımlamak ve gerektiğinde filtrelemek için kullanılır.
- Kimlikler şu kalıbı izler: `applabel.X001`, burada:
  - `applabel`: Uygulama adı.
  - `X`: Mesajın ciddiyetini ifade eden bir harf (C: Critical, E: Error, W: Warning, I: Info, D: Debug).
  - `001`: Uygulama içinde benzersiz olan bir sayı.

  **Kullanım örneği**:
  ```python
  id = "myapp.W001"
  ```

---

### Alt Sınıflar

**Bu sınıflar**, mesaj oluşturmayı kolaylaştırır ve `level` parametresini doğrudan belirtmeye gerek kalmaz. Örneğin, `Warning` sınıfını kullanırken `level` otomatik olarak `WARNING` olur.

#### 1. `Debug`
- `msg`, `hint`, `obj` ve `id` ile bir debug mesajı oluşturur. Bu, hata ayıklama sırasında kullanılan en düşük ciddiyetteki mesajlardır.

  **Kullanım örneği**:
  ```python
  from django.core.checks import Debug
  message = Debug("This is a debug message.", hint="No action needed.")
  ```

#### 2. `Info`
- Bilgilendirici mesajlar için kullanılır. 

  **Kullanım örneği**:
  ```python
  from django.core.checks import Info
  message = Info("The migration file is missing.", hint="Run 'python manage.py makemigrations'.")
  ```

#### 3. `Warning`
- Uyarılar için kullanılır, genellikle potansiyel sorunlar için öneriler verir.

  **Kullanım örneği**:
  ```python
  from django.core.checks import Warning
  message = Warning("Database connection is not secure.", hint="Use SSL for database connections.", id="myapp.W002")
  ```

#### 4. `Error`
- Ciddi hatalar için kullanılır, bu hatalar yönetim komutlarının çalışmasını engelleyebilir.

  **Kullanım örneği**:
  ```python
  from django.core.checks import Error
  message = Error("Invalid database configuration.", hint="Check DATABASES setting in settings.py.", id="myapp.E001")
  ```

#### 5. `Critical`
- Kritik hatalar için kullanılır, bu hatalar uygulamanın çalışmasını ciddi şekilde etkileyebilir.

  **Kullanım örneği**:
  ```python
  from django.core.checks import Critical
  message = Critical("Application is missing a required setting.", hint="Set the required configuration in settings.py.", id="myapp.C001")
  ```

---

### Kullanım Örneği
Aşağıda bir örnek sistem kontrolü ile nasıl kullanabileceğinizi gösteriyorum:

```python
from django.core.checks import register, Warning

@register()
def check_database_settings(app_configs, **kwargs):
    from django.conf import settings
    
    errors = []
    
    if 'default' not in settings.DATABASES:
        errors.append(
            Warning(
                "No default database is configured.",
                hint="Add 'default' database configuration in your settings.",
                obj=settings,
                id='myapp.W001'
            )
        )
    
    return errors
```

Bu örnek, Django’nun `check` komutunu çalıştırdığınızda, veritabanı ayarlarını kontrol eder ve herhangi bir sorun varsa bir uyarı mesajı verir.

***Soru:*** peki bu mesajları hangi kodlara ekleyeceğim ve nerden sonuççarını takip edeceğim

**Cevap:** Django'nun **System Check Framework**'ü, belirli alanları kontrol etmek ve raporlamak için kullanılabilecek bir mekanizmadır. Bu mekanizmayı kullanarak özelleştirilmiş kontrol fonksiyonları yazabilir ve bunları uygulama yüklenirken çalışacak şekilde kaydedebilirsiniz.

Aşağıda bu kontrol fonksiyonlarını **hangi kodlara ekleyeceğinizi** ve **nereden sonuçları takip edebileceğinizi** adım adım açıklıyorum:

### 1. **Check Fonksiyonlarının Yazılması ve Kaydedilmesi**

Kontrolleri bir Python fonksiyonu olarak tanımlayıp, bu fonksiyonu `django.core.checks.register` dekoratörü ile kaydedersiniz. Örneğin, bir uygulamanın `checks.py` dosyasına aşağıdaki gibi bir kontrol fonksiyonu ekleyebilirsiniz:

**Örnek: Kontrol Fonksiyonu Yazma**

```python
# myapp/checks.py
from django.core.checks import register, Warning

@register()
def check_database_settings(app_configs, **kwargs):
    from django.conf import settings
    
    errors = []
    
    # Varsayılan veritabanı ayarını kontrol et
    if 'default' not in settings.DATABASES:
        errors.append(
            Warning(
                "No default database is configured.",
                hint="Add 'default' database configuration in your settings.",
                id='myapp.W001'
            )
        )
    
    return errors
```

Bu kontrol fonksiyonu, veritabanı ayarlarını denetler ve "default" veritabanı ayarı eksikse bir `Warning` (uyarı) mesajı döner.

### 2. **Kontrol Fonksiyonlarını Uygulama İçine Entegre Etmek**

Kontrolleri bir Django uygulamasına entegre etmek için, genellikle bu kontrol fonksiyonlarını uygulamanın `apps.py` veya `checks.py` dosyasına eklersiniz. Eğer `checks.py` dosyası yoksa, oluşturabilirsiniz.

Ayrıca, `apps.py` dosyasında `ready` metodunu kullanarak `checks.py` dosyasını uygulama yüklenirken dahil edebilirsiniz:

**Örnek: Kontrol Fonksiyonlarını Dahil Etme**

```python
# myapp/apps.py
from django.apps import AppConfig

class MyAppConfig(AppConfig):
    name = 'myapp'

    def ready(self):
        # checks.py içindeki kontrolleri yükler
        from . import checks
```

Bu şekilde, `myapp` uygulamanız başlatıldığında kontrol fonksiyonları otomatik olarak yüklenir.

### 3. **Kontrol Sonuçlarını Takip Etmek**

Django, sistem kontrollerini **yönetim komutları** (management commands) aracılığıyla çalıştırır. `check` komutunu çalıştırarak tüm projedeki kontrolleri çalıştırabilir ve sonuçları konsolda görebilirsiniz.

#### **Kontrolleri çalıştırma:**
Kontrolleri manuel olarak çalıştırmak için terminalden şu komutu kullanabilirsiniz:

```bash
python manage.py check
```

Bu komut, projede tanımlanan tüm sistem kontrollerini çalıştırır ve terminalde sonuçları gösterir.

**Örnek Çıktı:**
Eğer bir kontrol başarısız olursa ya da bir uyarı varsa, sonuçlar şöyle görünebilir:

```
System check identified some issues:

WARNINGS:
myapp.W001: 
    No default database is configured.
    HINT: Add 'default' database configuration in your settings.

System check identified 1 issue (0 silenced).
```

Bu çıktıda, uyarı kimliği (`myapp.W001`), hata mesajı ve ipucu (`HINT`) açıkça belirtilmiştir.

### 4. **Kontrolleri Yönetme ve Sessize Alma**

Django, bazı uyarıları ya da hataları yönetmek için filtreleme mekanizması sağlar. Böylece bazı uyarıları göz ardı edebilir veya sessize alabilirsiniz.

#### **Uyarıları sessize almak:**

Eğer belirli bir kontrol kimliğini sessize almak isterseniz, ayarlar dosyasına (settings.py) şu şekilde ekleme yapabilirsiniz:

```python
SILENCED_SYSTEM_CHECKS = ['myapp.W001']
```

Bu ayar, belirli kontrol kimliklerinin çalıştırıldığında raporlanmamasını sağlar.

### 5. **Kontrolleri Özelleştirme ve Test Etme**

Kontrolleri özelleştirerek daha karmaşık projeler için de kullanabilirsiniz. Örneğin, belirli bir modeldeki alanların doğruluğunu kontrol edebilir, ayar dosyasında eksik olan yapılandırmaları denetleyebilir ya da yönetim komutlarının düzgün çalışıp çalışmadığını test edebilirsiniz.

#### **Model Kontrolü Yapma:**

Aşağıda bir model üzerinde nasıl kontrol yapabileceğinizi gösteren örnek bulunmaktadır:

```python
# myapp/checks.py
from django.core.checks import register, Error
from .models import MyModel

@register()
def check_model_fields(app_configs, **kwargs):
    errors = []
    
    # MyModel'deki belirli bir alanın varlığını kontrol edin
    if not hasattr(MyModel, 'required_field'):
        errors.append(
            Error(
                "MyModel is missing the 'required_field' field.",
                hint="Add 'required_field' to MyModel.",
                id='myapp.E002'
            )
        )
    
    return errors
```

Bu kontrol, `MyModel` adlı modelde bir `required_field` alanı olup olmadığını kontrol eder ve eksikse bir `Error` döndürür.

### Özet:

- **Kontrol fonksiyonları**, uygulamanızın belirli bölümlerini (ayarlar, modeller, vb.) kontrol etmek için yazılır ve `@register()` dekoratörü ile kaydedilir.
- Bu kontrolleri uygulamanızın `checks.py` veya `apps.py` dosyasına ekleyip uygulama başlatılırken yüklenmesini sağlayabilirsiniz.
- **Sonuçları** terminalde `python manage.py check` komutuyla takip edebilirsiniz.
- İstenmeyen uyarıları `SILENCED_SYSTEM_CHECKS` ayarı ile sessize alabilirsiniz.

Bu şekilde projelerinizde otomatik doğrulamalar yaparak yaygın hataların önüne geçebilirsiniz.

***Soru:*** o zaman aslında serverı çalıştırmadan önce check yaparak sistemin çalışıp çalışmadığını eskik bir aşan var mı kontrol etmek için kullanurım bu sisdtemi , peki bu sistemi veritabanına bağlayop match_id ile ilgili gelen veriler gelmemişse gibi durumlar içinde kullanabilir miyim , canlı bir serverda buna gerek var mı

**Cevap:** Evet, **Django’nun System Check Framework**'ü, serverı çalıştırmadan önce projenizdeki belirli yapıların doğru şekilde tanımlanıp tanımlanmadığını kontrol etmek için harika bir araçtır. Ancak bu sistem statik kontroller için tasarlanmıştır, yani **kod yapısını** (ayar dosyaları, modeller, sinyaller, vb.) doğrulamak amacıyla kullanılır. Sistemin düzgün çalışıp çalışmadığını, eksik ayarların veya yanlış yapılandırmaların olup olmadığını kontrol eder.

Ancak, **dinamik veriler** (örneğin veritabanına bağlı canlı veri kontrolleri) için bu framework uygun olmayabilir. Çünkü Django’nun **check framework**'ü genellikle server başlatılmadan veya komut çalıştırılmadan önce **statik kontroller** yapar, yani veritabanına veya diğer dinamik bileşenlere bağlanmaz.

### 1. **Dinamik Veriler İçin Kullanım**
Eğer sistemin belirli bir bölümünde **veritabanı verilerine bağlı bir kontrol** yapmak istiyorsanız (örneğin, `match_id` ile ilgili verilerin eksik olup olmadığını kontrol etmek gibi), bunu **System Check Framework** içinde doğrudan yapmanız önerilmez. Çünkü:
- System Check Framework, genel olarak **statik kod yapısındaki eksiklikleri** kontrol etmek için tasarlanmıştır.
- Veritabanına bağlanıp veri doğrulama yapmak, özellikle **canlı bir sunucuda** kullanıldığında performans sorunlarına yol açabilir.
- Canlı veritabanı işlemleri, uygulamanın çalışması sırasında yapılması gereken dinamik kontrollerdir.

### 2. **Canlı Veriler İçin Alternatif Çözümler**
Dinamik veri kontrollerini, veritabanı tabanlı işlemlerle yapmak istiyorsanız, bunun için farklı yaklaşımlar önerilir:

#### a. **Yönetim Komutları (Management Commands)**
Django’da kendi **yönetim komutlarınızı** yazarak, veritabanında veri doğrulama işlemleri yapabilirsiniz. Örneğin, belirli bir tabloya veya alana bakarak eksik `match_id` kayıtlarını kontrol edebilirsiniz.

**Örnek: `match_id` kontrolü için bir yönetim komutu**

```python
# myapp/management/commands/check_missing_match_id.py
from django.core.management.base import BaseCommand
from myapp.models import Match

class Command(BaseCommand):
    help = "Check for missing match_id in the database."

    def handle(self, *args, **kwargs):
        missing_matches = Match.objects.filter(match_id__isnull=True)
        
        if missing_matches.exists():
            self.stdout.write(self.style.WARNING(f"{missing_matches.count()} matches missing 'match_id'."))
        else:
            self.stdout.write(self.style.SUCCESS("All matches have 'match_id'."))
```

Bu komut, veritabanında `match_id` alanı eksik olan kayıtları kontrol eder ve sonucu terminalde gösterir. Bu komutu şu şekilde çalıştırabilirsiniz:

```bash
python manage.py check_missing_match_id
```

#### b. **Otomatik Görevler (Celery, cron job vb.)**
Canlı sunucularda, belirli aralıklarla veritabanında veri kontrolleri yapmak için **otomatik görevler** (örneğin, Celery kullanarak background task'ler) oluşturabilirsiniz. Bu görevler, sürekli olarak veritabanını kontrol eder ve eksik veya hatalı verileri tespit eder.

Örneğin, Celery kullanarak düzenli aralıklarla `match_id` kontrolü yapabilir ve bir sorun varsa yöneticilere e-posta ile bildirim gönderebilirsiniz.

#### c. **Signal Kullanımı**
Eğer veritabanına eklenen her yeni kayıt sırasında dinamik kontroller yapmak istiyorsanız, Django’nun **signals (sinyaller)** özelliğini kullanabilirsiniz. Örneğin, bir `Match` kaydı oluşturulurken, `match_id` gibi zorunlu alanların olup olmadığını kontrol edebilirsiniz.

**Örnek: Django Signals ile `match_id` kontrolü**

```python
# myapp/signals.py
from django.db.models.signals import pre_save
from django.dispatch import receiver
from myapp.models import Match
from django.core.exceptions import ValidationError

@receiver(pre_save, sender=Match)
def validate_match_id(sender, instance, **kwargs):
    if not instance.match_id:
        raise ValidationError("match_id cannot be null.")
```

Bu sinyal, `Match` modeli kaydedilmeden önce `match_id` alanının dolu olup olmadığını kontrol eder ve eğer eksikse bir `ValidationError` fırlatır.

### 3. **Canlı Sunucularda System Check Framework Kullanımı**
Canlı bir sunucuda, **System Check Framework**'ü genel olarak **statik ayarları** ve **kod yapısını** kontrol etmek için kullanabilirsiniz, ancak veritabanı kontrolleri gibi dinamik işlemleri bu sistem ile yapmak genellikle önerilmez. Bunun sebebi:
- **Performans sorunları**: Her sunucu başlatıldığında veritabanına sorgu yapmanız, performans sorunlarına yol açabilir.
- **Kapsam dışı**: Django’nun system check framework'ü, canlı veri doğrulaması yapmaktan çok, kodun doğru yapılandırıldığından emin olmayı hedefler.

**System Check Framework’ü ile yapılabilecek tipik kontroller:**
- Ayarların eksik olup olmadığını kontrol etmek (örn: veritabanı ayarları, dosya yolları).
- Model alanlarının doğru şekilde tanımlandığını doğrulamak.
- Uygulamanın doğru bağımlılıklara sahip olup olmadığını kontrol etmek.

**Canlı sunucular** için yukarıda bahsedilen **otomatik görevler**, **signals** ve **yönetim komutları** daha uygun bir yaklaşımdır.

---

### Sonuç:
- **System Check Framework**, statik kontroller için kullanılır ve canlı veritabanı verileriyle çalışmak için uygun değildir.
- **Veritabanı kontrolleri** (örneğin, `match_id` doğrulaması), yönetim komutları, sinyaller veya arka planda çalışan görevler ile yapılmalıdır.
- **Canlı sunucuda** performansı olumsuz etkilememek adına, System Check Framework'ü sadece **statik doğrulamalar** için kullanın ve veri tabanıyla ilgili dinamik işlemler için başka yöntemler kullanın.

Bu şekilde, hem sisteminizin sağlıklı çalıştığından emin olur hem de dinamik veri doğrulamalarını doğru araçlarla yapabilirsiniz. ✔️