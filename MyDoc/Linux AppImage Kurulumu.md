***Soru:*** Linux AppImage

don't forget to make it executable before run,
runs on old Linux distributions like openSUSE 13.1 (except VA-API due to driver version incompatibility),
you can use appimaged for system integration or you can extract files and integrate QMPlay2 manually,
OpenSSL 1.1.1w is compiled from sources,
dav1d 1.4.2, libass 0.17.2, FFmpeg 7.0.1, taglib 2.0.1, libva 2.21.0, librubberband 3.3.0, libgme 0.6.3, libsidplayfp 2.7.1, harfbuzz 8.5.0, Qt 5.15.14 are compiled from sources using Clang 12.0.1 with libc++,
compiled on Ubuntu 16.04,
requires glibc 2.18,  bu yönergeleri nasıl yerine getirecdeğim

**Cevap:** Bu yönergeleri adım adım izleyerek AppImage dosyasını çalıştırabilir ve sisteminize entegre edebilirsiniz:

### 1. **AppImage'i İndir**
Öncelikle ilgili AppImage dosyasını indirin.

### 2. **Yürütülebilir Hale Getirme**
İndirdiğiniz AppImage dosyasının çalıştırılabilir olmasını sağlamak için terminalde şu komutu kullanın:

```bash
chmod +x /path/to/your/AppImage
```
Bu komut, dosyaya yürütme izni verecektir. `/path/to/your/AppImage` kısmını dosyanın bulunduğu tam yol ile değiştirmelisiniz.

### 3. **AppImage'i Çalıştırma**
Yürütülebilir hale getirdikten sonra AppImage'i şu komutla çalıştırabilirsiniz:

```bash
./yourAppImage.AppImage
```

Eğer bir hata ile karşılaşırsanız, bu genellikle sistemin bazı gereksinimleri karşılamadığı anlamına gelebilir.

### 4. **Eski Linux Dağıtımları Üzerinde Çalıştırma**
AppImage, eski Linux dağıtımlarında (örneğin openSUSE 13.1) çalışabilir. Ancak VA-API (Video Acceleration API) bazı sürücü versiyonu uyumsuzlukları nedeniyle çalışmayabilir. Eğer videolarda performans sıkıntısı yaşarsanız, bunun nedeni bu olabilir.

### 5. **Sistem Entegrasyonu için appimaged Kullanma**
Sistem entegrasyonunu kolaylaştırmak için `appimaged` adlı bir aracı kullanabilirsiniz. Bu araç, AppImage dosyalarını otomatik olarak sisteminize entegre eder.

`appimaged` kurulumunu gerçekleştirmek için şu komutları kullanabilirsiniz:

```bash
wget https://github.com/AppImage/appimaged/releases/download/continuous/appimaged-x86_64.AppImage
chmod +x appimaged-x86_64.AppImage
./appimaged-x86_64.AppImage --install
```

Bu sayede AppImage dosyaları otomatik olarak masaüstüne ve menülere entegre edilecektir.

### 6. **Manuel Entegrasyon**
Eğer `appimaged` kullanmak istemezseniz, AppImage dosyasını elle açarak ve dosyaları manuel entegre ederek de kullanabilirsiniz. AppImage dosyasını şu komutla açabilirsiniz:

```bash
./yourAppImage.AppImage --appimage-extract
```

Bu işlem sonucunda `squashfs-root` adlı bir klasör oluşacak ve dosyaların içeriklerini buradan alarak sisteminize manuel olarak yerleştirebilirsiniz.

### 7. **OpenSSL ve Diğer Kütüphaneler**
Yukarıda belirtilen kütüphaneler (OpenSSL 1.1.1w, FFmpeg 7.0.1, Qt 5.15.14 vb.) AppImage ile birlikte derlenmiş olarak geliyor, bu yüzden sisteminize ek olarak kurmanıza gerek yok.

Ancak AppImage’i çalıştırdığınız eski sistemin glibc sürümünü kontrol etmeniz gerekiyor. AppImage’in çalışması için en az **glibc 2.18** gerekiyor. Bunu kontrol etmek için şu komutu kullanabilirsiniz:

```bash
ldd --version
```

Eğer sisteminizin glibc sürümü 2.18’den eskiyse, güncelleme yapmanız veya farklı bir Linux dağıtımı kullanmanız gerekebilir.

Bu adımları izleyerek, AppImage dosyasını çalıştırabilir ve sisteminize entegre edebilirsiniz.

***Soru:*** Extract the contents of an AppImage
An alternative to mounting the AppImages is to extract their contents. This allows for modifying the contents. The resulting directory is a valid AppDir, and users can create AppImages from them again using appimagetool.

Analog to mounting AppImages, there is a simple commandline switch to extract the contents of type 2 AppImages without external tools. Just call the AppImage with the parameter --appimage-extract. This will cause the runtime to create a new directory called squashfs-root, containing the contents of the AppImage’s AppDir.

Type 1 AppImages require the deprecated tool AppImageExtract to extract the contents of an AppImage. It’s very limited functionality wise, and requires a GUI to run. It creates a new directory in the user’s desktop directory.

See also

There is currently no way to use the former method without calling the target AppImage. This might not always be appropriate, e.g., if the AppImage is not trustworthy.

The AppImage team is working on implementing a mount option in appimagetool. Please see the related GitHub issue for progress on this.

Integrating AppImages into the desktop
AppImages are standalone bundles, and do not need to be installed. However, some users may want their AppImages to be available like distribution provided applications. This primarily involves being able to launch desktop applications from their desktop environments’ launchers. This concept is called desktop integration.  indirmeyi  asul yapacağım

**Cevap:** AppImage içeriğini çıkarmak için aşağıdaki adımları izleyerek başarılı bir şekilde işlemi gerçekleştirebilirsiniz:

### 1. **AppImage Dosyasını İndirme**
İlk olarak AppImage dosyasını indirin. Bunu tarayıcı üzerinden yapabilir veya terminalden `wget` komutunu kullanarak doğrudan indirme işlemi gerçekleştirebilirsiniz.

Örnek terminal komutu ile indirme:
```bash
wget https://example.com/path/to/your/appimage.AppImage
```

### 2. **İndirilen Dosyayı Yürütülebilir Hale Getirme**
İndirilen AppImage dosyasını çalıştırılabilir hale getirmek için şu komutu kullanın:

```bash
chmod +x yourAppImage.AppImage
```

Bu işlem, dosyanın çalıştırılabilir olmasını sağlayacaktır.

### 3. **AppImage İçeriğini Çıkarma**
Şimdi AppImage dosyasının içeriğini çıkarmak için `--appimage-extract` parametresini kullanabilirsiniz:

```bash
./yourAppImage.AppImage --appimage-extract
```

Bu komut, mevcut dizinde `squashfs-root` adlı bir klasör oluşturacak ve AppImage’in tüm içeriğini bu klasöre çıkartacaktır.

### 4. **İçeriği Düzenleme**
Artık `squashfs-root` klasöründe AppImage içeriğini düzenleyebilir, değiştirebilir ve ihtiyacınıza göre modifiye edebilirsiniz. Bu, özellikle uygulama dosyalarında değişiklik yapmanız veya farklı bir yapılandırma eklemek istediğinizde kullanışlıdır.

### 5. **AppImage'i Yeniden Oluşturma**
İçeriği düzenledikten sonra tekrar AppImage haline getirmek için `appimagetool` aracını kullanabilirsiniz. Eğer sisteminizde `appimagetool` kurulu değilse, şu şekilde kurabilirsiniz:

```bash
wget https://github.com/AppImage/AppImageKit/releases/download/continuous/appimagetool-x86_64.AppImage
chmod +x appimagetool-x86_64.AppImage
```

Daha sonra AppImage’i yeniden oluşturmak için şu komutu kullanabilirsiniz:

```bash
./appimagetool-x86_64.AppImage squashfs-root
```

Bu komut, düzenlediğiniz `squashfs-root` klasörünü tekrar bir AppImage haline getirecektir.

### 6. **Eski Tip AppImage (Type 1) Kullanıyorsanız**
Eğer elinizdeki AppImage bir "Type 1" AppImage ise, içeriği çıkarmak için `AppImageExtract` aracını kullanmanız gerekir. Bu aracın GUI (Grafik Kullanıcı Arayüzü) gerektirdiğini unutmayın. Ancak genellikle modern AppImage dosyaları "Type 2" olduğundan, yukarıdaki `--appimage-extract` yöntemi yeterli olacaktır.

Bu adımları izleyerek AppImage'in içeriğini çıkartabilir, düzenleyebilir ve yeniden oluşturabilirsiniz.

***Soru:*** AppImageAssistant_6-i686.AppImage
1.19 MB
Sep 10, 2016
AppImageAssistant_6-i686.AppImage.zsync
3.83 KB
Sep 10, 2016
AppImageAssistant_6-x86_64.AppImage
1.19 MB
Sep 10, 2016
AppImageAssistant_6-x86_64.AppImage.zsync
3.83 KB
Sep 10, 2016
AppImageExtract_6-i686.AppImage
640 KB
Sep 10, 2016
AppImageExtract_6-i686.AppImage.zsync
2.14 KB
Sep 10, 2016
AppImageExtract_6-x86_64.AppImage
640 KB
Sep 10, 2016
AppImageExtract_6-x86_64.AppImage.zsync
2.14 KB
Sep 10, 2016
AppImageMonitor_6-i686.AppImage
640 KB
Sep 10, 2016
AppImageMonitor_6-i686.AppImage.zsync
2.14 KB
Sep 10, 2016
AppImageMonitor_6-x86_64.AppImage
704 KB
Sep 10, 2016
AppImageMonitor_6-x86_64.AppImage.zsync
2.33 KB
Sep 10, 2016
AppRun_6-i686
6.55 KB
Sep 10, 2016
AppRun_6-x86_64
8.44 KB
Sep 10, 2016
Source code
(zip)
Sep 10, 2016
Source code
(tar.gz) hangisini indireceğim

**Cevap:** İhtiyacınıza ve sisteminize bağlı olarak aşağıdaki dosyalardan uygun olanı seçebilirsiniz:

1. **32-bit (i686) veya 64-bit (x86_64) sistem mi kullanıyorsunuz?**
   - Eğer 32-bit bir Linux sistemi kullanıyorsanız, `i686` dosyalarını indirmeniz gerekir.
   - 64-bit bir Linux sistemi kullanıyorsanız, `x86_64` dosyalarını indirmeniz gerekir.

2. **Hangi uygulamaya ihtiyacınız var?**
   - **AppImageAssistant**: AppImage dosyalarını oluşturmak ve yönetmek için kullanılır. Eğer yeni bir AppImage yaratmak istiyorsanız bunu kullanabilirsiniz.
     - 32-bit için: `AppImageAssistant_6-i686.AppImage`
     - 64-bit için: `AppImageAssistant_6-x86_64.AppImage`
   
   - **AppImageExtract**: Var olan bir AppImage dosyasını çıkartmak istiyorsanız, bu aracı kullanabilirsiniz. İçeriği dışarı çıkarmak için ihtiyacınız olan araç budur.
     - 32-bit için: `AppImageExtract_6-i686.AppImage`
     - 64-bit için: `AppImageExtract_6-x86_64.AppImage`
   
   - **AppImageMonitor**: AppImage dosyalarınızı izlemek ve yönetmek için bir araçtır.
     - 32-bit için: `AppImageMonitor_6-i686.AppImage`
     - 64-bit için: `AppImageMonitor_6-x86_64.AppImage`
   
   - **AppRun**: Bu dosya AppImage dosyalarını çalıştırmak için kullanılır, ancak genellikle manuel olarak indirmeniz gerekmez çünkü bu dosya AppImage dosyalarının içinde otomatik olarak bulunur.

### Özet:
Eğer amacınız AppImage'in içeriğini çıkartmaksa ve sisteminiz 64-bit ise, şunu indirmeniz gerekiyor:
- `AppImageExtract_6-x86_64.AppImage`

32-bit bir sistem kullanıyorsanız:
- `AppImageExtract_6-i686.AppImage`

Bu dosyalardan birini indirip yukarıda belirttiğim adımları izleyerek içeriği çıkartabilirsiniz.

***Soru:*** tamam app image assitan indirdim ne yapacğaıjm

**Cevap:** `AppImageAssistant` dosyasını indirdikten sonra adım adım şu işlemleri yapabilirsiniz:

### 1. **Yürütülebilir Hale Getirme**
İlk olarak indirdiğiniz `AppImageAssistant` dosyasını çalıştırılabilir hale getirmeniz gerekiyor. Terminali açın ve şu komutu kullanın:

```bash
chmod +x AppImageAssistant_6-x86_64.AppImage
```
(Eğer 32-bit sistem kullanıyorsanız, `i686` versiyonu için komutu kullanın.)

### 2. **AppImageAssistant'i Çalıştırma**
Şimdi uygulamayı başlatmak için şu komutu kullanın:

```bash
./AppImageAssistant_6-x86_64.AppImage
```

Bu komut, AppImageAssistant'i başlatacaktır.

### 3. **Yeni Bir AppImage Oluşturma**
Eğer yeni bir uygulama veya dosya setinden AppImage oluşturmak istiyorsanız, uygulama size rehberlik edecektir. Temel adımlar genellikle şu şekildedir:

- **Bir AppDir Klasörü Oluşturun**: Bu klasörde uygulamanızın tüm dosyalarını toplayın. `AppRun`, `.desktop` dosyası ve uygulamanın çalıştırılabilir dosyaları bu klasörde yer almalıdır.
  
  Örnek olarak, `MyApp` adında bir uygulama için klasör oluşturabilirsiniz:
  ```bash
  mkdir MyApp.AppDir
  cp /path/to/your/app MyApp.AppDir/
  ```

- **.desktop Dosyası Ekleyin**: Uygulamanız için bir `.desktop` dosyası oluşturun. Bu dosya, masaüstü entegrasyonu için gereklidir ve şu yapıya sahip olmalıdır:
  ```bash
  [Desktop Entry]
  Name=MyApp
  Exec=MyAppExecutable
  Icon=myapp
  Type=Application
  Categories=Utility;
  ```

- **AppRun Dosyasını Ekleyin**: `AppRun` dosyasını da bu klasöre yerleştirmeniz gerekir. `AppRun` dosyası, uygulamanın nasıl başlatılacağını kontrol eder. Bu dosya genellikle AppImage sisteminin içinde gelir ama elle ekleyebilirsiniz.

### 4. **AppImage Oluşturma**
AppDir klasörünüz hazır olduktan sonra, AppImageAssistant ile bu klasörden bir AppImage oluşturabilirsiniz. Terminalde şu komutu kullanın:

```bash
./AppImageAssistant MyApp.AppDir MyApp.AppImage
```

Bu komut, `MyApp.AppDir` klasöründen bir `MyApp.AppImage` dosyası oluşturacaktır.

### 5. **Oluşturulan AppImage'i Test Etme**
Yeni oluşturduğunuz AppImage dosyasını test etmek için şu komutu kullanabilirsiniz:

```bash
./MyApp.AppImage
```

Eğer her şey doğru şekilde ayarlandıysa, uygulamanız bir AppImage olarak çalışmaya başlayacaktır.

Bu adımları takip ederek `AppImageAssistant` ile uygulamanızın bağımsız bir AppImage dosyasını oluşturabilirsiniz.

***Soru:*** QMPlay2  indirebilir misin ubuntuya

**Cevap:** To install **QMPlay2** on Ubuntu, you can follow one of the methods below:

### Method 1: Install via PPA
1. Open a terminal (Ctrl + Alt + T) and add the PPA repository:
   ```bash
   sudo add-apt-repository ppa:samrog131/ppa
   ```
2. Update your package list:
   ```bash
   sudo apt-get update
   ```
3. Install QMPlay2:
   ```bash
   sudo apt-get install qmplay2
   ```

### Method 2: Install via Flatpak
1. First, ensure Flatpak is installed on your system:
   ```bash
   sudo apt install flatpak
   ```
2. Install QMPlay2 using Flatpak:
   ```bash
   flatpak install flathub io.github.zaps166.QMPlay2
   ```

### Method 3: Install from Default Repositories (for Ubuntu 22.04)
If you're using Ubuntu 22.04 or newer, QMPlay2 is available in the official repositories. Simply run:
   ```bash
   sudo apt install qmplay2
   ```

After installation, you can launch QMPlay2 from the terminal with `qmplay2` or find it in the application menu under "Activities."

These methods provide multiple options depending on your preferred installation approach【15†source】【16†source】【17†source】.

***Soru:*** This video file cannot be played.
(Error Code: 232012)  uyarısı aldığım iptv sitemde bunu nasıl düeltirim

**Cevap:** The **Error Code: 232012** is commonly associated with video playback issues, particularly when streaming content such as IPTV. This error often occurs due to various reasons, such as browser incompatibility, network problems, or video encoding issues. Here are some steps you can take to fix it:

### 1. **Clear Browser Cache and Cookies**
   - This error may occur if there's corrupted data in the browser cache. Clear the cache and cookies, then reload the IPTV site.
   - In most browsers, you can clear the cache by going to settings -> privacy -> clear browsing data.

### 2. **Update or Change Browser**
   - Ensure that you're using the latest version of your browser. Sometimes older versions do not support certain video formats.
   - If you're using a less common browser, switch to a more widely supported one like Google Chrome, Firefox, or Microsoft Edge.

### 3. **Disable Browser Extensions**
   - Browser extensions, especially ad-blockers or security add-ons, can interfere with video playback. Try disabling these extensions or accessing the IPTV site in incognito/private browsing mode.

### 4. **Enable Flash or HTML5**
   - Ensure that the website supports **HTML5** for video playback. If the website still relies on **Flash**, ensure that it’s enabled, although many browsers have deprecated Flash support.

### 5. **Check Internet Connection**
   - An unstable or slow internet connection can result in playback errors. Verify that you have a stable and fast connection suitable for video streaming.

### 6. **Adjust Video Quality**
   - Try reducing the video quality to a lower setting. High-quality streams may fail to load properly if the network bandwidth is insufficient.

### 7. **Firewall or Security Software**
   - Sometimes, security software or a firewall can block certain streaming content. Ensure that your firewall or antivirus software is not blocking the IPTV service.

### 8. **Update Video Player (If Applicable)**
   - Some IPTV platforms use their own video players. Ensure that the player is up to date or try using an alternative video player that supports streaming protocols like **VLC**.

If none of these solutions work, check with your IPTV provider to ensure the streaming service is not experiencing issues or using a video format that your browser or system cannot handle.

***Soru:*** türkçe yaz ve bana en önemli çözüm yolu sun

**Cevap:** **Error Code: 232012** hatası, genellikle IPTV sitelerinde video oynatma problemleri sırasında karşılaşılan bir hatadır. Bu tür hatalar çeşitli nedenlerden kaynaklanabilir, örneğin tarayıcı uyumsuzluğu, internet bağlantı sorunları veya video kodlama hataları gibi. Aşağıda en etkili çözüm yolunu ve diğer adımları paylaşıyorum:

### En Önemli Çözüm: **Tarayıcı Cache ve Çerezleri Temizleme**
Bu hata genellikle tarayıcıdaki bozuk verilerden kaynaklanır. Bu nedenle, tarayıcınızın **önbelleğini (cache)** ve **çerezlerini temizlemek** büyük olasılıkla sorunu çözecektir. Adımlar:

1. **Tarayıcı ayarlarına** gidin.
2. **Gizlilik ve güvenlik** bölümünden **tarama verilerini temizle** seçeneğini bulun.
3. **Önbellek ve çerezleri** işaretleyerek temizleyin.
4. Ardından sayfayı yeniden yükleyin.

### Diğer Çözüm Yolları:
1. **Tarayıcı Güncellemesi veya Değiştirilmesi:**
   - En son sürümde olduğunuzdan emin olun. Eski tarayıcılar bazı video formatlarını desteklemeyebilir.
   - Mümkünse başka bir tarayıcı (Google Chrome, Firefox gibi) deneyin.

2. **İnternet Bağlantınızı Kontrol Edin:**
   - Düşük hız veya kararsız bağlantılar bu hataya yol açabilir. İnternet hızınızı test edin ve gerekirse daha stabil bir bağlantı kullanın.

3. **Tarayıcı Eklentilerini Devre Dışı Bırakma:**
   - Reklam engelleyici gibi eklentiler video oynatmayı engelleyebilir. Tüm eklentileri devre dışı bırakıp tekrar deneyin.

Bu adımlar, en yaygın nedenleri çözmeye yönelik en etkili çözümler olacaktır.

***Soru:*** Seçtiğiniz giriş açılamadı:
VLC, 'http://tr.hdiptv.us:8080/get.php?username=093ev8r1w4&password=65udskpvm7&type=m3u&output=ts' ortam kaynağı adresini (MRL) açamıyor. Ayrıntılar için günlük dosyasına bakın.
Seçtiğiniz giriş açılamadı:
VLC, 'http://tr.hdiptv.us:8080/get.php?username=093ev8r1w4&password=65udskpvm7&type=m3u_plus&output=ts' ortam kaynağı adresini (MRL) açamıyor. Ayrıntılar için günlük dosyasına bakın.   bu çalılşmıyoru VLC ubuntu ile bunu nasıl önlerim

**Cevap:** VLC'de aldığınız bu hata, **MRL (Media Resource Locator)** adresinin doğru biçimde açılmaması nedeniyle ortaya çıkar. Bu tür hatalar genellikle IPTV sunucularından gelen bağlantıların doğru yapılandırılmaması, internet bağlantısı veya VLC ayarlarıyla ilgili sorunlardan kaynaklanabilir. Bu sorunu çözmek için aşağıdaki adımları deneyebilirsiniz:

### 1. **Günlük Dosyasını Kontrol Edin**
   VLC’de sorunların detaylarını görmek için günlük dosyasını inceleyin. Bunu şu şekilde yapabilirsiniz:
   - VLC’de **Araçlar > Mesajlar (Ctrl + M)** menüsüne gidin.
   - Günlük seviyesini **Hata** olarak ayarlayın ve yayını yeniden oynatmaya çalışın.
   - Günlük dosyasındaki hatalar sorunun nedenini belirlemenize yardımcı olabilir.

### 2. **IPTV URL Formatını Kontrol Edin**
   - M3U URL'sinin doğru ve çalışır durumda olduğundan emin olun. Bazı durumlarda IPTV sağlayıcıları, URL formatında değişiklik yapabilir veya oturum süresi dolabilir.
   - URL'de `type=m3u_plus` veya `type=m3u` yerine diğer seçenekleri deneyin (örneğin, `type=m3u8`).

### 3. **Güvenlik Duvarı Ayarları**
   - Ubuntu'da güvenlik duvarı veya antivirüs yazılımlarınız, VLC'nin IPTV bağlantısını engelliyor olabilir. Geçici olarak güvenlik duvarını devre dışı bırakıp tekrar deneyin.
   
   Güvenlik duvarını kapatmak için şu komutları kullanabilirsiniz:
   ```bash
   sudo ufw disable
   ```

   Tekrar aktif etmek için:
   ```bash
   sudo ufw enable
   ```

### 4. **VLC Kullanıcı Aracısı (User Agent) Değiştirme**
   Bazı IPTV servis sağlayıcıları, bağlantılara yalnızca belirli medya oynatıcılar veya kullanıcı aracısı (user agent) olan tarayıcılar üzerinden erişime izin verebilir. VLC’de kullanıcı aracısını değiştirmek sorunu çözebilir:

   - VLC'de **Tercihler > Giriş/Kodekler > Ağ > HTTP Kullanıcı Aracısı** bölümüne gidin ve bu alanı aşağıdaki gibi bir değerle güncelleyin:
     ```bash
     Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:89.0) Gecko/20100101 Firefox/89.0
     ```

### 5. **VLC ve Codec Güncellemeleri**
   VLC ve kodeklerin güncel olup olmadığını kontrol edin. VLC'nin eski sürümleri IPTV protokollerini tam olarak desteklemeyebilir. VLC'yi şu komutlarla güncelleyebilirsiniz:
   
   ```bash
   sudo apt update
   sudo apt upgrade vlc
   ```

### 6. **Alternatif Oynatıcı Kullanın**
   Eğer VLC ile çözüm bulamazsanız, **Kodi** veya **Simple IPTV** gibi başka medya oynatıcılarını deneyebilirsiniz. Bu oynatıcılar da IPTV yayınlarını destekler ve bazen VLC ile yaşanan sorunları aşabilir.

Bu adımları izleyerek VLC ile IPTV yayınlarını tekrar düzgün bir şekilde oynatabilirsiniz.

***Soru:*** Kodi  ubuntuya indirsene

**Cevap:** Kodi'yi Ubuntu'ya yüklemek için aşağıdaki adımları takip edebilirsiniz:

### 1. **Terminali Açın**
   - `Ctrl + Alt + T` ile terminali açın.

### 2. **Kodi PPA'sını Ekleyin**
   Aşağıdaki komutlarla Kodi’nin resmi PPA deposunu ekleyin:
   ```bash
   sudo add-apt-repository ppa:team-xbmc/ppa
   ```

### 3. **Depoları Güncelleyin**
   Depo listesini güncellemek için:
   ```bash
   sudo apt update
   ```

### 4. **Kodi'yi Kurun**
   Şimdi Kodi'yi kurmak için şu komutu kullanın:
   ```bash
   sudo apt install kodi
   ```

### 5. **Kodi'yi Başlatın**
   Kurulum tamamlandıktan sonra, Kodi'yi uygulamalar menüsünden veya terminalden şu komutla başlatabilirsiniz:
   ```bash
   kodi
   ```

Bu adımları izleyerek Ubuntu'da Kodi'yi başarılı bir şekilde yükleyip kullanabilirsiniz.

***Soru:*** tamam kodi başladı ağ akışı için url mi nerey ekleyecdğim

**Cevap:** Kodi’de ağ akışı (IPTV veya benzeri URL'ler) eklemek için aşağıdaki adımları izleyebilirsiniz:

### 1. **Kodi Ana Ekranından Başlayın**
   - Kodi açıldıktan sonra ana ekranda **“Add-ons”** (Eklentiler) seçeneğine gidin.

### 2. **Video Add-ons'ı Seçin**
   - Sol menüden **“Enter add-on browser”** veya doğrudan **“My add-ons”** (Benim eklentilerim) seçeneğine tıklayın.

### 3. **PVR IPTV Simple Client'i Kurun**
   - **PVR Clients** altına gidin ve **PVR IPTV Simple Client**'ı bulun.
   - **Install** (Yükle) düğmesine tıklayarak bu eklentiyi kurun.

### 4. **PVR IPTV Simple Client'i Yapılandırın**
   - Kurulum tamamlandıktan sonra **“Configure”** (Yapılandır) butonuna tıklayın.
   - **General** (Genel) sekmesinde, **M3U Playlist URL** seçeneğini göreceksiniz. Buraya IPTV M3U URL'nizi ekleyin.

### 5. **EPG Ayarları (İsteğe Bağlı)**
   - Eğer Elektronik Program Rehberi (EPG) URL'si de sağlanmışsa, **EPG Settings** (EPG Ayarları) bölümüne gidin ve **EPG URL** kısmına rehber URL'sini ekleyin.

### 6. **Değişiklikleri Kaydedin ve Kapatın**
   - Değişiklikleri kaydedin ve **PVR IPTV Simple Client** eklentisini etkinleştirin.

### 7. **TV Bölümüne Gidin**
   - Kodi ana ekranına geri dönün. Menüde artık **TV** veya **Live TV** bölümü göreceksiniz. Buradan ağ akışı URL’sini kullanarak kanalları izleyebilirsiniz.

Bu adımları izleyerek IPTV veya ağ akışı URL'nizi Kodi'ye başarıyla ekleyebilirsiniz.

***Soru:*** dan “My add-ons” (Benim eklentilerim)  tıkladıktan sonra ne yapacağım

**Cevap:** “My add-ons” (Benim eklentilerim) bölümüne girdikten sonra, **PVR IPTV Simple Client** eklentisini yüklemek ve ayarlamak için şu adımları izleyin:

### 1. **PVR Clients Kategorisini Bulun**
   - "My add-ons" bölümünde, **PVR Clients** (PVR İstemcileri) kategorisini bulun ve tıklayın.

### 2. **PVR IPTV Simple Client'ı Seçin**
   - "PVR Clients" altında **PVR IPTV Simple Client** eklentisini arayın ve tıklayın.

### 3. **Kurulum (Install) Yapın**
   - "PVR IPTV Simple Client" eklentisine tıkladıktan sonra açılan menüden **Install** (Yükle) butonuna tıklayın.

### 4. **Eklentiyi Yapılandırın**
   - Eklenti yüklendikten sonra, **Configure** (Yapılandır) butonuna tıklayın. Buradan ağ akışı URL'nizi ayarlayabilirsiniz.
   - **General** sekmesinde, **M3U Playlist URL** bölümüne IPTV sağlayıcınızdan aldığınız M3U URL'sini ekleyin.
   - Eğer bir **EPG URL** (Elektronik Program Rehberi) varsa, bunu **EPG Settings** kısmına ekleyebilirsiniz.

### 5. **Değişiklikleri Kaydedin ve Eklentiyi Etkinleştirin**
   - Ayarları yaptıktan sonra, değişiklikleri kaydedin ve eklentiyi etkinleştirin.

### 6. **Live TV Menüsünden İzleyin**
   - Ana ekrana dönün, menüde **TV** veya **Live TV** seçeneği belirecek. Bu bölümden IPTV kanallarını izleyebilirsiniz.

Bu adımlarla ağ akışı URL'nizi Kodi'ye ekleyebilir ve canlı TV izleyebilirsiniz.

***Soru:*** "My add-ons" bölümünde, PVR Clients (PVR İstemcileri) kategorisini bulun ve tıklayın.  bu seçenek yok

**Cevap:** Eğer **"PVR Clients"** kategorisini göremiyorsanız, muhtemelen **PVR IPTV Simple Client** eklentisi henüz yüklü değil. Bu durumda eklentiyi yüklemek için şu adımları deneyebilirsiniz:

### 1. **Kodi Eklenti Tarayıcısına Gidin**
   - Kodi ana ekranında **Add-ons** (Eklentiler) bölümüne gidin.
   - Sol üst köşede bulunan **Paket simgesine** (açık kutu simgesi) tıklayın.

### 2. **Eklenti Yükleyin**
   - **Install from Repository** (Depodan yükle) seçeneğine tıklayın.
   - Buradan **All repositories** (Tüm depolar) seçeneğini seçin.

### 3. **PVR Clients Kategorisini Bulun**
   - Açılan menüden **PVR Clients** kategorisini bulun ve tıklayın.
   - **PVR IPTV Simple Client** eklentisini arayıp seçin.

### 4. **Yükleme ve Yapılandırma**
   - **Install** (Yükle) butonuna tıklayın. Yükleme tamamlandıktan sonra **Configure** (Yapılandır) seçeneğini kullanarak M3U URL'nizi ekleyebilirsiniz.

### 5. **TV Menüsünden Canlı Yayını İzleyin**
   - Eklenti yüklendikten sonra **TV** menüsü ana ekranda aktif olacaktır ve IPTV kanallarınızı bu bölümden izleyebilirsiniz.

Eğer bu adımlar sorunu çözmezse, Kodi'nin en güncel sürümünü kullandığınızdan emin olun ve eklentilerin depolarda yer alıp almadığını kontrol edin.

***Soru:*** m3 linkimi neyere ekleyeceğim burada

**Cevap:** M3U linkinizi **PVR IPTV Simple Client** eklentisi ayarlarına eklemek için aşağıdaki adımları izleyebilirsiniz:

### 1. **Kodi Eklenti Tarayıcısına Gidin**
   - Ana ekrandan **Add-ons** (Eklentiler) bölümüne gidin.
   - Sol üst köşedeki **paket simgesine** (açık kutu) tıklayın.

### 2. **PVR IPTV Simple Client'i Seçin**
   - **My Add-ons** (Benim Eklentilerim) menüsünde, **PVR Clients** bölümüne gidin.
   - **PVR IPTV Simple Client** eklentisini seçin.

### 3. **Yapılandırma (Configure) Bölümüne Girin**
   - Eklenti yüklendikten sonra **Configure** (Yapılandır) butonuna tıklayın.

### 4. **M3U Playlist URL'sini Ekleyin**
   - Açılan pencerede **General** (Genel) sekmesine gidin.
   - **M3U Playlist URL** bölümünü bulun ve buraya IPTV sağlayıcınızdan aldığınız **M3U URL**'yi yapıştırın.

### 5. **Değişiklikleri Kaydedin**
   - Ayarları yaptıktan sonra **OK** butonuna tıklayarak değişiklikleri kaydedin.

### 6. **TV Menüsünden İzleyin**
   - Ana ekrana geri dönün. Artık ana menüde **TV** veya **Live TV** seçeneği aktif olacaktır.
   - Bu menüden IPTV kanallarınızı izlemeye başlayabilirsiniz.

Bu adımlar ile M3U linkinizi başarıyla ekleyip IPTV yayını izleyebilirsiniz.