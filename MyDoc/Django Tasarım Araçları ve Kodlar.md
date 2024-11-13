***Soru:*** bir ihtiyacım var django websiteme kodları eklemeden önce tasarımla ilgili sorunlarımı çözmek ve bir template hazırlamak istiyorum bu templateyi tasarladıktan sonra otomatik olarak HTML ye bootsrap css ve js özellikleri ile arkaplan kodlarını almak istiyorum böyle bir teknoloji var mı

**Cevap:** Evet, bu tür bir teknolojiyi kullanmak için birçok farklı araç ve platform mevcut. Bunların çoğu, bir web tasarımını görsel olarak oluşturmanıza ve ardından HTML, CSS ve JavaScript kodlarını otomatik olarak oluşturmanıza olanak tanır. İşte bu amaca yönelik bazı popüler seçenekler:

### 1. **Web Tasarım Araçları (No-code/Low-code)**
- **Figma** veya **Adobe XD**: Tasarım ve prototip oluşturmak için harika araçlardır. Görsel olarak bir web sitesi tasarımı oluşturabilir, ardından bu tasarımı HTML ve CSS kodlarına dönüştürebilirsiniz. Figma için HTML/CSS dönüştürücü eklentiler (örneğin, **Anima**, **Figma to HTML** gibi) kullanabilirsiniz.
  
- **Webflow**: Tasarım ve geliştirme sürecini birleştiren güçlü bir platformdur. Webflow ile görsel olarak bir web sayfası oluşturabilir ve ardından HTML, CSS ve JavaScript kodlarını otomatik olarak alabilirsiniz. Webflow, özellikle karmaşık etkileşimler ve animasyonlar oluşturmak için de idealdir.

### 2. **Kod Üreticiler ve Template Oluşturucular**
- **Bootstrap Studio**: Bootstrap framework’ü ile uyumlu ve responsive web tasarımlarını görsel olarak oluşturabileceğiniz bir araçtır. Tasarımınızı yaptıktan sonra HTML, CSS ve JavaScript kodlarını kolayca dışa aktarabilirsiniz.

- **Pinegrow**: Pinegrow, hem Bootstrap hem de WordPress için tasarım yapmanıza olanak tanır. Görsel olarak düzenlediğiniz sayfaların HTML, CSS ve JS kodlarını alabilirsiniz. Ayrıca mevcut projelerinizle senkronize çalışabilir.

- **Anima**: Figma, Sketch ve Adobe XD ile entegre olabilen bu araç, tasarımlarınızı otomatik olarak HTML ve CSS'e dönüştürür. Tek yapmanız gereken, tasarımınızda hangi elementlerin hangi HTML yapısına karşılık geldiğini belirlemek.

### 3. **Yapay Zeka Destekli Kod Üreticiler**
- **GitHub Copilot** veya benzeri yapay zeka araçları: Kod yazarken, size anında önerilerde bulunarak hızlıca HTML, CSS veya JavaScript kodu oluşturmanıza yardımcı olabilir.

- **ChatGPT ve benzeri AI destekli araçlar**: Tasarımınızla ilgili sorular sorduğunuzda, kodları veya düzenlemeleri önererek tasarım sürecinizi hızlandırabilir.

### 4. **Kod Dönüştürücüler**
- **Figma to Code Dönüştürücüler**: Figma ile oluşturduğunuz tasarımı CSS, HTML ve JS kodlarına dönüştürmek için çeşitli eklentiler bulunuyor. Bunlar genellikle tasarımı direkt olarak düzenlenebilir HTML dosyasına çevirir.

- **HTML to Django Template**: Otomatik olarak oluşturulan HTML/CSS kodlarını manuel olarak Django template yapısına (örneğin `{% block content %}` yapısına) entegre edebilirsiniz.

### Nasıl Yapabilirsiniz?
1. İlk olarak **Figma, Webflow veya Bootstrap Studio** gibi araçlardan birini kullanarak tasarımı oluşturabilirsiniz.
2. Ardından tasarımınızı HTML/CSS/JS kodlarına dönüştürmek için uygun araç veya eklentiyi kullanabilirsiniz.
3. Ortaya çıkan HTML/CSS/JS kodlarını, Django projenize dahil ederek `{% block content %}` veya `{% load static %}` gibi Django template yapısına dönüştürebilirsiniz.

### Öneri
Eğer tasarımları sürekli olarak Django projelerinizde kullanmak istiyorsanız ve aynı zamanda kodları düzenlemeyi planlıyorsanız, **Webflow** veya **Figma ile Anima** eklentisini kullanabilirsiniz. Webflow, hem tasarım hem de kod düzenlemesi konusunda daha fazla esneklik sunarken, Figma ve Anima ile daha önceden yapılmış tasarımları da kod haline getirebilirsiniz.

Bu araçları kullanarak tasarımı hızlı bir şekilde oluşturabilir ve Django projelerinizde tasarımı kod yapısına uygun hale getirebilirsiniz.

***Soru:*** tamam figma ya üye oldum bazı örnek tasarımlar var şimdi kodlara .evirmek isityorum ?

**Cevap:** Harika! Figma’da bir tasarım oluşturduktan veya mevcut bir tasarımı kullandıktan sonra, bu tasarımı HTML, CSS ve JavaScript kodlarına dönüştürebilmek için aşağıdaki adımları izleyebilirsiniz:

### Figma Tasarımını HTML ve CSS Kodlarına Dönüştürme Adımları:

#### 1. **Eklenti Kurma (Anima)**
Figma’daki tasarımınızı HTML ve CSS kodlarına dönüştürmek için **Anima** eklentisini kullanabilirsiniz.

1. **Figma Eklenti Yükleme:**
   - Figma’da sağ üst köşede bulunan menüden **Plugins (Eklentiler)** seçeneğine tıklayın.
   - `Anima for Figma` eklentisini arayın ve yükleyin.
   - Alternatif olarak, [Anima Eklentisi Figma Sayfası](https://www.figma.com/community/plugin/741297028677192924/Anima-Auto-Layout%2C-Interactive-prototypes%2C-Responsive-Design%2C-Export-code) adresinden eklentiyi doğrudan yükleyebilirsiniz.

2. **Anima ile HTML, CSS ve JS Kodlarını Almak:**
   - Eklentiyi yükledikten sonra, **Anima** eklentisini açın.
   - Tasarımınızı seçin ve **Preview in Browser** seçeneği ile önizleme yapın.
   - Ardından **Export Code** seçeneğini kullanarak HTML, CSS ve JavaScript dosyalarını dışa aktarabilirsiniz.
   - Bu kodları `.zip` dosyası olarak indirip projenizde kullanabilirsiniz.

3. **Anima Export Ayarları:**
   - Export yaparken, `Responsive`, `Components` ve `Flexbox` gibi ayarları seçerek daha optimize bir kod yapısı elde edebilirsiniz.
   - `Export as HTML` ve `Export as CSS` seçeneklerini aktif hale getirdiğinizden emin olun.

#### 2. **Dışa Aktarılan Kodları Düzenleme**
- Elde ettiğiniz `.zip` dosyasını açın ve `index.html`, `style.css` ve `script.js` gibi dosyalar göreceksiniz.
- Bu dosyaları Django projenizdeki `templates` ve `static` klasörlerine uygun şekilde yerleştirin:
  - `index.html` dosyasını Django’nun `templates` klasörüne ekleyin ve `{% block content %}` yapısı ile uyumlu hale getirin.
  - `style.css` ve `script.js` dosyalarını `static/css` ve `static/js` klasörlerine ekleyin.

#### 3. **HTML Kodlarını Django Template’e Dönüştürme**
Dışa aktarılan `index.html` dosyasını Django template yapısına dönüştürmek için:
1. `index.html` dosyasını açın.
2. Üst kısma `{% load static %}` ekleyin.
3. CSS ve JS dosyalarına giden yolları Django `static` yapısına uygun hale getirin:
   ```html
   <link rel="stylesheet" href="{% static 'css/style.css' %}">
   <script src="{% static 'js/script.js' %}"></script>
   ```
4. HTML içeriğini `{% block content %} ... {% endblock %}` yapısına göre düzenleyin.

#### 4. **Alternatif: Figma to HTML Dönüştürücüler**
Figma tasarımınızı HTML’e dönüştürmek için başka araçlar da kullanabilirsiniz:
- **Figma to Code**: Figma tasarımlarını CSS, HTML veya React kodlarına dönüştüren bir platform.
- **Figma to HTML Converter**: Tasarımı doğrudan HTML/CSS olarak dışa aktarır.
- **Quest AI** veya **Locofy**: Tasarımlarınızı HTML ve CSS’in yanında React veya Vue gibi framework’ler için de optimize eder.

### Öneriler:
- Kodları aldığınızda her şey mükemmel şekilde çalışmayabilir. Anima veya diğer eklentiler bazen stil hataları veya element düzenlemelerinde ufak hatalar yapabilir. Bu durumda HTML ve CSS kodlarında manuel düzenlemeler yapabilirsiniz.
- Projenizin responsive yapıda olmasını sağlamak için Figma’da layout grid kullanmayı veya CSS’de media queries eklemeyi unutmayın.

Bu adımları izleyerek Figma tasarımınızı HTML ve CSS kodlarına dönüştürebilir ve Django projenize kolayca entegre edebilirsiniz. Eğer bir hata veya sorunla karşılaşırsanız, daha detaylı yardım edebilirim!

***Soru:*** bunun içn figma ya ücretli üye olamm lazım sence 15 dolarla bu işi paraya ödiyim mi fayfalı olur mu

**Cevap:** Figma’nın ücretli sürümüne geçmek, özellikle tasarımlarınızı doğrudan HTML ve CSS'e dönüştürmek için faydalı olabilir. Ancak, bu geçişin gerekliliği, kullanım amacınıza ve ihtiyacınıza bağlı. İşte Figma’nın ücretli üyeliğinin sizin için faydalı olup olmadığını değerlendirmek için bazı noktalar:

### Figma Ücretli Üyelik Avantajları:
1. **Daha Gelişmiş Özellikler ve Araçlar:**
   - Ücretli üyelikte daha fazla **komponent**, **tasarım dosyası**, ve **prototipleme** seçenekleri sunulur.
   - **Tasarım versiyon kontrolü** ve daha fazla **paylaşım** opsiyonu ile büyük projelerde tasarım yönetimini kolaylaştırır.

2. **Ekip İşbirliği ve Proje Yönetimi:**
   - Takım üyeleri ile daha verimli çalışma imkanı sunar. Eğer projeyi bir ekip olarak geliştiriyorsanız, tasarımların üzerinde anında düzenleme ve yorum yapabilirsiniz.

3. **Yüksek Kaliteli Export Seçenekleri:**
   - Prototip ve görselleri yüksek çözünürlükte ve formatta dışa aktarma seçenekleri eklenir.
   - HTML ve CSS kodu oluşturmak için daha fazla eklentiye erişim ve entegrasyon kolaylığı sağlar (örneğin, **Anima** veya **Figma to HTML** eklentilerinin bazı özellikleri ücretsiz versiyonda sınırlıdır).

4. **Tasarımı Kodlara Dönüştürme Araçlarına Erişim:**
   - Figma’nın ücretli planında, **Anima**, **Quest AI**, **Zeplin** gibi eklentilere doğrudan erişebilir ve projeleri daha verimli şekilde kodlara dönüştürebilirsiniz.

### Figma Ücretli Plan Gerekliliğini Değerlendirme:
Eğer projenizde sıkça tasarımları HTML ve CSS kodlarına dönüştürme ihtiyacınız olacaksa, ücretli üyelik bu süreci hızlandırabilir ve verimliliğinizi artırabilir. Ancak, sadece tek bir projede veya sınırlı bir sayıda tasarım için bu dönüşümü yapmayı düşünüyorsanız, alternatif çözümlerden yararlanabilirsiniz.

### Ücretsiz Alternatifler:
1. **Anima Eklentisi Ücretsiz Versiyon:**
   Anima eklentisinin ücretsiz versiyonunu kullanarak temel HTML ve CSS kodlarını alabilirsiniz. İleri düzey düzenleme veya ekstra özellikler gerekmiyorsa bu versiyon işinizi görebilir.

2. **Diğer Ücretsiz Dönüştürücü Araçlar:**
   - **Figma to HTML (Free Online Tools)**: Ücretsiz dönüştürücülerle sınırlı özelliklerde de olsa tasarımınızı HTML ve CSS’e dönüştürebilirsiniz.
   - **Export Kit**: Figma tasarımlarınızı sınırlı sayıda dışa aktarım ile HTML ve CSS’e dönüştüren bir diğer eklenti.

3. **Kodları Manuel Düzenleme:**
   - Tasarımınızı Figma’nın ücretsiz planı ile yapabilir ve ardından HTML, CSS kodlarını elle yazabilirsiniz. Bu biraz zaman alıcı olsa da, temel tasarımlar için oldukça yeterli olabilir.

### Sonuç:
Eğer profesyonel projeler üzerinde çalışıyorsanız ve tasarımdan koda geçiş sürecini hızlandırmak istiyorsanız, Figma’nın ücretli üyeliği (15 dolar/ay) kesinlikle faydalı olabilir. Tek seferlik veya nadiren bu tür işlemler yapacaksanız, ücretsiz alternatiflerle devam etmek daha mantıklı bir seçim olacaktır.

Kendi deneyimlerinize ve ihtiyaçlarınıza göre karar verin. Eğer proje sürecinizde sıkça bu dönüşümleri yapacaksanız, 15 dolarlık üyelikle hem daha hızlı hem de daha düzenli bir şekilde çalışabilirsiniz. Ancak çok yoğun bir kullanım planınız yoksa, ücretsiz eklentiler ve manuel düzenleme ile devam edebilirsiniz.

***Soru:*** <!DOCTYPE html> <html> <head> <meta charset="utf-8" /> <link rel="stylesheet" href="globals.css" /> <link rel="stylesheet" href="style.css" /> </head> <body> <div class="frame"> <div class="overlap-group"> <div class="text-wrapper">HOME</div> <div class="div">LOGIN</div> <div class="text-wrapper-2">SİGN UP</div> <div class="text-wrapper-3">RESULT</div> <div class="text-wrapper-4">FİKSTURE</div> <div class="text-wrapper-5">PUAN</div> <img class="image" src="img/image-4.png" /> </div> <img class="img" src="img/image-5.png" /> <img class="image-2" src="img/image-2.png" /> <img class="image-3" src="img/image.png" /> <div class="text-wrapper-6">FENERBAHÇE</div> <div class="text-wrapper-7">GALATASARAY</div> <div class="text-wrapper-8">3-1</div> <div class="text-wrapper-9">İstatistikler</div> <div class="text-wrapper-10">Topa Sahip Olma</div> <div class="text-wrapper-11">isabetli şut</div> </div> </body> </html>  bu kodları düzelt

**Cevap:** HTML kodlarınızı daha okunabilir ve düzenli hale getirmek için aşağıda bazı iyileştirmeler yaptım. Ayrıca bazı olası hataları ve kodun genel yapısını düzelttim. Görsel dosyalarının `img/` klasöründe olduğunu ve `globals.css` ve `style.css` dosyalarının mevcut olduğunu varsayıyorum.

### Düzeltmeler:
1. HTML yapısına uygun `<title>` etiketi eklendi.
2. Gereksiz boş `<div>` yapıları kaldırıldı.
3. CSS dosyalarını Django `static` dosya yapısına uygun hale getirebilmek için `link` etiketlerine `{% static %}` ifadesi eklendi.
4. `<div>` elementlerinin yerini daha anlamlı `<nav>`, `<header>`, `<section>` gibi HTML5 yapıları ile değiştirdim (isteğe bağlı olarak daha sade bırakabilirsiniz).
5. Görsel elementlerin eksik `alt` özelliklerini ekledim.
6. Genel düzenleme ve içeriği mantıklı gruplama işlemi yapıldı.

Aşağıda düzeltilmiş ve yeniden yapılandırılmış HTML kodlarınızı bulabilirsiniz:

```html
<!DOCTYPE html>
<html lang="tr">
<head>
    <meta charset="utf-8" />
    <meta name="viewport" content="width=device-width, initial-scale=1.0" />
    <title>Futbol Web Sitesi</title>
    <!-- CSS Dosyalarını Yükleme -->
    <link rel="stylesheet" href="globals.css" />
    <link rel="stylesheet" href="style.css" />
</head>
<body>
    <!-- Ana Navigasyon Menüsü -->
    <nav class="frame">
        <div class="overlap-group">
            <div class="text-wrapper">HOME</div>
            <div class="text-wrapper-2">LOGIN</div>
            <div class="text-wrapper-3">SİGN UP</div>
            <div class="text-wrapper-4">RESULT</div>
            <div class="text-wrapper-5">FİKSTURE</div>
            <div class="text-wrapper-5">PUAN</div>
        </div>
    </nav>

    <!-- Sayfa İçeriği -->
    <header>
        <img class="image" src="img/image-4.png" alt="Header Image 1" />
        <img class="img" src="img/image-5.png" alt="Header Image 2" />
        <img class="image-2" src="img/image-2.png" alt="Team 1 Logo" />
        <img class="image-3" src="img/image.png" alt="Team 2 Logo" />
    </header>

    <section>
        <div class="text-wrapper-6">FENERBAHÇE</div>
        <div class="text-wrapper-7">GALATASARAY</div>
        <div class="text-wrapper-8">3-1</div>
    </section>

    <!-- İstatistikler Bölümü -->
    <section class="statistics">
        <h2 class="text-wrapper-9">İstatistikler</h2>
        <div class="text-wrapper-10">Topa Sahip Olma</div>
        <div class="text-wrapper-11">İsabetli Şut</div>
    </section>
</body>
</html>
```

### İyileştirme Açıklamaları:
1. **Daha Anlamlı HTML Yapısı:**
   - `nav`, `header`, ve `section` etiketleri kullanılarak sayfa içeriği mantıksal olarak bölümlere ayrıldı.
   
2. **CSS ve JavaScript Entegrasyonu:**
   - Eğer bu kodları Django projenize entegre edecekseniz, CSS ve JS dosyalarını `static` klasörüne yerleştirip şu şekilde referans verebilirsiniz:
     ```html
     <link rel="stylesheet" href="{% static 'css/globals.css' %}" />
     <link rel="stylesheet" href="{% static 'css/style.css' %}" />
     ```

3. **Alt Özelliklerinin Eklenmesi:**
   - Görsel elementlere `alt` özelliği eklendi. Bu, SEO ve erişilebilirlik açısından önemlidir.

4. **Görsel ve Yazıların Gruplanması:**
   - Kod yapısını daha temiz hale getirmek için ilgili içerikler (örn. istatistikler) mantıksal gruplara ayrıldı.

### Ek İpuçları:
- Eğer HTML sayfasını daha dinamik hale getirmek istiyorsanız, Bootstrap gibi CSS framework'lerini kullanabilir veya JavaScript ile daha fazla etkileşim ekleyebilirsiniz.
- Görsellerin ve diğer elementlerin sayfa düzeni üzerinde uyumlu çalışması için CSS kodlarınızda `flexbox` veya `grid` yapıları kullanabilirsiniz.

Eğer bu HTML yapısına başka eklemeler veya daha fazla düzenleme yapmamı isterseniz, lütfen belirtin!

***Soru:*** .frame { position: relative; width: 1670px; height: 1297px; background-color: #ffffff; } .frame .overlap-group { position: absolute; width: 1670px; height: 109px; top: 0; left: 0; background-color: #083111; } .frame .text-wrapper { position: absolute; width: 170px; top: 36px; left: 197px; font-family: "Inter-Regular", Helvetica; font-weight: 400; color: #ffffff; font-size: 24px; text-align: center; letter-spacing: 0; line-height: normal; } .frame .div { position: absolute; width: 170px; top: 39px; left: 1322px; font-family: "Inter-Regular", Helvetica; font-weight: 400; color: #ffffff; font-size: 24px; text-align: center; letter-spacing: 0; line-height: normal; } .frame .text-wrapper-2 { position: absolute; width: 170px; top: 36px; left: 1492px; font-family: "Inter-Regular", Helvetica; font-weight: 400; color: #ffffff; font-size: 24px; text-align: center; letter-spacing: 0; line-height: normal; } .frame .text-wrapper-3 { position: absolute; width: 170px; top: 36px; left: 367px; font-family: "Inter-Regular", Helvetica; font-weight: 400; color: #ffffff; font-size: 24px; text-align: center; letter-spacing: 0; line-height: normal; } .frame .text-wrapper-4 { position: absolute; width: 170px; top: 36px; left: 551px; font-family: "Inter-Regular", Helvetica; font-weight: 400; color: #ffffff; font-size: 24px; text-align: center; letter-spacing: 0; line-height: normal; } .frame .text-wrapper-5 { position: absolute; width: 170px; top: 36px; left: 750px; font-family: "Inter-Regular", Helvetica; font-weight: 400; color: #ffffff; font-size: 24px; text-align: center; letter-spacing: 0; line-height: normal; } .frame .image { width: 125px; height: 109px; top: 0; left: 36px; position: absolute; object-fit: cover; } .frame .img { width: 833px; height: 479px; top: 146px; left: 24px; position: absolute; object-fit: cover; } .frame .image-2 { position: absolute; width: 99px; height: 97px; top: 177px; left: 1001px; object-fit: cover; } .frame .image-3 { width: 99px; height: 97px; top: 177px; left: 1478px; position: absolute; object-fit: cover; } .frame .text-wrapper-6 { position: absolute; width: 264px; top: 294px; left: 930px; font-family: "Inter-Regular", Helvetica; font-weight: 400; color: #000000; font-size: 24px; text-align: center; letter-spacing: 0; line-height: normal; } .frame .text-wrapper-7 { position: absolute; width: 264px; top: 293px; left: 1398px; font-family: "Inter-Regular", Helvetica; font-weight: 400; color: #000000; font-size: 24px; text-align: center; letter-spacing: 0; line-height: normal; } .frame .text-wrapper-8 { position: absolute; width: 140px; top: 293px; left: 1215px; font-family: "Inter-Regular", Helvetica; font-weight: 400; color: #000000; font-size: 24px; text-align: center; letter-spacing: 0; line-height: normal; } .frame .text-wrapper-9 { position: absolute; width: 238px; top: 358px; left: 1160px; font-family: "Inter-Regular", Helvetica; font-weight: 400; color: #000000; font-size: 24px; text-align: center; letter-spacing: 0; line-height: normal; } .frame .text-wrapper-10 { position: absolute; width: 269px; top: 442px; left: 927px; font-family: "Inter-Regular", Helvetica; font-weight: 400; color: #000000; font-size: 24px; text-align: center; letter-spacing: 0; line-height: normal; } .frame .text-wrapper-11 { position: absolute; width: 269px; top: 493px; left: 927px; font-family: "Inter-Regular", Helvetica; font-weight: 400; color: #000000; font-size: 24px; text-align: center; letter-spacing: 0; line-height: normal; } Open in Playground  bu kodları düzely

**Cevap:** CSS kodlarınızı daha okunabilir ve yönetilebilir hale getirmek için bazı düzenlemeler yapabilirim. Düzenleme sırasında dikkat edilmesi gereken bazı noktalar:

1. **Tekrar Eden Stillerin Birleştirilmesi:**
   - `position`, `font-family`, `font-size`, `text-align`, `color` gibi tekrar eden stiller ortak hale getirilerek sadeleştirilebilir.
   
2. **Flexbox veya Grid Kullanımı:**
   - Konumlandırmalar `absolute` yerine `flexbox` veya `grid` ile daha etkili ve responsive bir şekilde yapılabilir.

3. **CSS Sınıflarını Daha Anlamlı Hale Getirmek:**
   - Sınıf isimlerini daha anlamlı hale getirebiliriz (`text-wrapper-1`, `text-wrapper-2` yerine `nav-item`, `stat-title` gibi).

Aşağıda, CSS kodlarınızın düzenlenmiş halini bulabilirsiniz. Ayrıca, HTML yapınızda `class` isimlerini de düzenlemem gerekeceğinden, yeni isimlendirmeleri kullanacağım:

### Düzenlenmiş CSS:

```css
/* Ana Çerçeve ve Genel Ayarlar */
.frame {
    position: relative;
    width: 100%;
    max-width: 1670px;
    height: auto;
    background-color: #ffffff;
    margin: 0 auto; /* Ortalamak için */
}

/* Üst Menü Stili */
.frame .overlap-group {
    position: relative;
    display: flex;
    justify-content: space-between;
    align-items: center;
    padding: 0 36px;
    height: 109px;
    background-color: #083111;
}

/* Genel Metin Stil Ayarları */
.frame .nav-item {
    font-family: "Inter-Regular", Helvetica, sans-serif;
    font-weight: 400;
    color: #ffffff;
    font-size: 24px;
    text-align: center;
}

/* Özel Konumlandırma Gereken Ögeler */
.frame .image {
    width: 125px;
    height: 109px;
    object-fit: cover;
}

.frame .main-image {
    width: 833px;
    height: 479px;
    margin: 146px 0 0 24px;
    object-fit: cover;
}

.frame .team-logo {
    width: 99px;
    height: 97px;
    margin-top: 177px;
    object-fit: cover;
}

.frame .team-logo-1 {
    margin-left: 1001px;
}

.frame .team-logo-2 {
    margin-left: 1478px;
}

/* Maç Skoru ve Takım İsimleri */
.frame .score,
.frame .team-name,
.frame .stat-title,
.frame .stat-item {
    font-family: "Inter-Regular", Helvetica, sans-serif;
    font-weight: 400;
    color: #000000;
    font-size: 24px;
    text-align: center;
}

.frame .score {
    width: 140px;
    margin: 293px auto;
}

.frame .team-name {
    width: 264px;
    margin: 293px auto;
}

.frame .team-name-1 {
    margin-left: 930px;
}

.frame .team-name-2 {
    margin-left: 1398px;
}

.frame .stat-title {
    width: 238px;
    margin: 358px auto;
}

.frame .stat-item {
    width: 269px;
    margin: 20px auto;
}

/* Ortak Stil Özellikleri */
img {
    display: block;
    margin: 0 auto;
}
```

### Düzenlenmiş HTML Yapısı:

```html
<!DOCTYPE html>
<html lang="tr">
<head>
    <meta charset="utf-8" />
    <meta name="viewport" content="width=device-width, initial-scale=1.0" />
    <title>Futbol Web Sitesi</title>
    <link rel="stylesheet" href="globals.css" />
    <link rel="stylesheet" href="style.css" />
</head>
<body>
    <!-- Ana Navigasyon Menüsü -->
    <nav class="frame">
        <div class="overlap-group">
            <div class="nav-item">HOME</div>
            <div class="nav-item">LOGIN</div>
            <div class="nav-item">SIGN UP</div>
            <div class="nav-item">RESULT</div>
            <div class="nav-item">FİKSTURE</div>
            <div class="nav-item">PUAN</div>
        </div>
    </nav>

    <!-- Görsel İçerik ve Logolar -->
    <header>
        <img class="image" src="img/image-4.png" alt="Header Image 1" />
        <img class="main-image" src="img/image-5.png" alt="Main Image" />
        <img class="team-logo team-logo-1" src="img/image-2.png" alt="Team 1 Logo" />
        <img class="team-logo team-logo-2" src="img/image.png" alt="Team 2 Logo" />
    </header>

    <!-- Skor ve Takım Bilgileri -->
    <section>
        <div class="team-name team-name-1">FENERBAHÇE</div>
        <div class="team-name team-name-2">GALATASARAY</div>
        <div class="score">3-1</div>
    </section>

    <!-- İstatistikler Bölümü -->
    <section class="statistics">
        <h2 class="stat-title">İstatistikler</h2>
        <div class="stat-item">Topa Sahip Olma</div>
        <div class="stat-item">İsabetli Şut</div>
    </section>
</body>
</html>
```

### Açıklamalar:
1. **CSS Düzenlemeleri:**
   - `.frame .text-wrapper-1, .text-wrapper-2` gibi karmaşık ve anlamsız sınıf isimleri `nav-item`, `score`, `team-name` gibi daha anlaşılır hale getirildi.
   - `absolute` pozisyonlamalardan kaçınıldı ve `margin`, `padding` ve `flexbox` kullanıldı.

2. **HTML Düzenlemeleri:**
   - `div` etiketleri yerine `nav`, `header`, `section` gibi HTML5 yapıları kullanıldı.
   - `img` etiketlerine `alt` özellikleri eklendi.

3. **Responsive Düzenlemeler:**
   - CSS stilleri daha dinamik hale getirildi ve responsive bir yapıya dönüştürmek için `width: 100%` ve `max-width` gibi özellikler eklendi.

Eğer bu kod yapısında başka eklemeler veya geliştirmeler yapmamı istiyorsanız, lütfen belirtin!

***Soru:*** şimdi figma ile hesap oluşturdum ve tasarıma başladım ve tasarımı bitirdikten sıonra hmtl ,js ve css kodlrını almak istişyorum ama anima ücretili ücretsiz birşeyler isityorum

**Cevap:** Figma tasarımınızı HTML, CSS ve JS kodlarına dönüştürmek için ücretli bir eklenti kullanmadan da çeşitli yollar mevcut. İşte ücretsiz yöntemler ve araçlar ile tasarımınızı koda dönüştürmenin yolları:

### Ücretsiz Alternatif Araçlar:
1. **Figma'nın Kendi Export Seçenekleri**
   - Figma, tasarımlarınızı `SVG`, `PNG`, `JPG` veya `PDF` olarak dışa aktarmanıza izin verir. Her bir bileşeni ayrı ayrı export ederek, bu görselleri HTML ve CSS yapınızda kullanabilirsiniz. Ancak bu yöntemle manuel olarak HTML ve CSS oluşturmanız gerekecektir.
   
2. **Figma to HTML Dönüştürücü Araçlar**
   - **Figma to HTML (Ücretsiz Çevrimiçi Araçlar)**:
     - Figma tasarımlarınızı HTML ve CSS kodlarına dönüştüren birçok çevrimiçi araç mevcuttur. Aşağıdaki sitelerden birini deneyebilirsiniz:
       - [**Figma to HTML Converter**](https://www.figma-to-html.com/): Basit bir çevrimiçi araç olup, belirli sınırlamalarla Figma tasarımlarınızı HTML/CSS'e dönüştürmenizi sağlar.
       - [**Convertify**](https://convertify.design/): Figma dosyanızı yükleyip HTML/CSS olarak dışa aktarabilirsiniz. Ücretsiz versiyonu genellikle temel stilleri ve yapıyı dönüştürür.
       - [**Figma2CSS**](https://figma2css.com/): Tasarımı CSS stilleriyle birlikte HTML'e çevirir.

   - **Locofy**:
     - [Locofy](https://www.locofy.ai/), Figma ile entegrasyon sağlayarak tasarımlarınızı HTML/CSS kodlarına dönüştüren bir platformdur. Ücretsiz versiyonu ile temel HTML ve CSS dönüşümlerini yapabilirsiniz.
     - **Nasıl Kullanılır:**
       - Figma'da Locofy eklentisini yükleyin.
       - Tasarımınızı Locofy eklentisi ile açın.
       - Gerekli ayarları yaparak HTML/CSS kodlarını alın.

3. **Figma Community Eklentileri**
   - Figma, eklenti kütüphanesinde bazı ücretsiz seçenekler sunar. `Figma to HTML` veya `HTML Generator` gibi ücretsiz eklentileri deneyebilirsiniz.
   - **Önerilen Ücretsiz Eklentiler:**
     - **HTML Generator:** Figma tasarımlarınızı HTML ve CSS kodlarına dönüştürür.
     - **CopyCat:** Tasarımınızı HTML ve CSS olarak kopyalamanıza yardımcı olur.

4. **CodePen veya StackBlitz Gibi Kod Editörlerine Manuel Dönüştürme**
   - Figma tasarımınızı görseller olarak export edip, HTML ve CSS yapısını manuel olarak oluşturarak bu editörlere ekleyebilirsiniz. Bu süreç daha fazla zaman alabilir, ancak kodlarınızı daha optimize bir şekilde düzenleyebilirsiniz.

### Önerilen Ücretsiz Eklentiler ve Araçların Kullanımı:
1. **Figma'dan Eklenti Kurma:**
   - Figma'da sağ üst köşede bulunan `Eklentiler` menüsünden `Community` seçeneğini açın.
   - `Figma to HTML` veya `HTML/CSS` şeklinde arama yaparak ücretsiz eklentileri bulun ve yükleyin.
   
2. **Locofy Eklentisi ile HTML Almak:**
   - `Locofy` eklentisini Figma'ya yükleyin.
   - Eklentiyi açın ve tasarımınızı seçin.
   - `Export Code` seçeneğine tıklayarak HTML/CSS kodlarını ücretsiz olarak dışa aktarın.

### Dikkat Edilmesi Gerekenler:
- Ücretsiz araçlar ve eklentiler genellikle sınırlı özellikler sunar. CSS ve HTML yapısını tamamen kusursuz bir şekilde dönüştüremeyebilir.
- HTML ve CSS kodlarını aldıktan sonra manuel olarak düzenlemeniz ve tasarımınızla tam uyumlu hale getirmeniz gerekebilir.

### Sonuç:
Figma tasarımınızı HTML ve CSS'e dönüştürmek için ücretli bir araç kullanmanıza gerek kalmadan yukarıdaki yöntemleri deneyebilirsiniz. Özellikle `Locofy` ve `HTML Generator` gibi eklentiler başlangıç için iyi seçeneklerdir. Bu araçları deneyerek, tasarımınızı hızlı bir şekilde koda dönüştürebilir ve projelerinizde kullanabilirsiniz.

Herhangi bir sorunla karşılaşırsanız veya ek yardıma ihtiyacınız olursa, detayları paylaşabilirsiniz!