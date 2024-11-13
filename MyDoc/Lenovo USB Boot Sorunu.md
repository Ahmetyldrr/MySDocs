***Soru:*** lenova bilgisayarımda boot yaptığımda usb göremiyorum bu yüaden ubuntu yükeleyemedim

**Cevap:** Lenovo bilgisayarında USB'den boot yaparken USB'nin görünmemesi birkaç farklı sorundan kaynaklanabilir. Sorunu çözmek için şu adımları izleyebilirsin:

### 1. **BIOS/UEFI Ayarlarını Kontrol Et**
- Bilgisayarını açarken **F2**, **Delete**, veya **F12** gibi BIOS'a girmek için kullanılan tuşa basarak BIOS'a gir.
- **Boot Mode** ayarını kontrol et. Eğer **UEFI** olarak ayarlandıysa, **Legacy Support** seçeneğini açman gerekebilir. Bu, bazı durumlarda USB'nin görünmesini sağlar.
    - **Boot Mode** > **UEFI**'den **Legacy Support**'a veya **Legacy Mode**'a geçiş yap.
    - Bazı BIOS'larda **CSM (Compatibility Support Module)** adında bir ayar da olabilir. Bu ayar da **Legacy Boot** için gereklidir.
  
### 2. **Boot Sırasını Değiştir**
- **Boot Priority (Boot Sırası)** menüsünde USB cihazlarının önceliğini kontrol et.
    - **USB HDD** veya **USB FDD** gibi seçeneklerin yukarıda olduğundan emin ol.
    - Eğer USB görünmüyorsa, bilgisayarı **Legacy Mode**'da yeniden başlattıktan sonra tekrar kontrol et.

### 3. **Secure Boot'u Kapat**
- BIOS'ta **Secure Boot** aktif olabilir. Bu özellik bazı işletim sistemlerinin veya USB aygıtlarının görünmesini engelleyebilir.
    - **Secure Boot**'u **Disable** yap ve ayarları kaydedip çık.

### 4. **Doğru USB Portunu Kullan**
- Bilgisayarında birden fazla USB portu varsa, özellikle **USB 2.0** portlarını kullanmayı dene. Bazı durumlarda **USB 3.0** portları boot sırasında tanınmayabilir.

### 5. **USB Medyasını Doğru Oluşturduğundan Emin Ol**
- USB'yi boot edilebilir bir şekilde hazırlamak için doğru yöntemi kullandığından emin ol. **Rufus** gibi bir araç kullanarak **ISO** dosyasını USB'ye yazdırırken, **GPT** yerine **MBR** seçeneğiyle oluşturmayı deneyebilirsin.
    - Eğer UEFI modda boot etmek istiyorsan, Rufus'ta **GPT Partition Scheme** ve **UEFI (non-CSM)** seçeneğini seçmen gerekebilir.

### 6. **Başka USB Aygıtları veya Kablo Deneyin**
- USB cihazının ya da kablosunun arızalı olup olmadığını kontrol et. Farklı bir USB cihazı ya da başka bir kabloyla tekrar denemekte fayda var.

Bu adımları denedikten sonra hala sorun yaşıyorsan, hangi adımda sorun olduğunu belirterek tekrar sorabilirsin.

***Soru:*** Secure Boot'u Disable yap ve ayarları kaydedip çık.  bunu nasıl yağacağım

**Cevap:** Lenovo bilgisayarında **Secure Boot**'u devre dışı bırakmak için şu adımları izleyebilirsin:

### 1. **BIOS'a Gir**
- Bilgisayarını kapat ve yeniden başlat.
- Bilgisayar açılırken hemen **F2**, **F1**, **Delete**, veya **Esc** tuşlarından birine basarak BIOS'a girmeye çalış. Lenovo bilgisayarlarda genellikle **F2** veya **F1** tuşları kullanılır.
- BIOS'a girmek için hangi tuşa basman gerektiğini açılış ekranında görebilirsin.

### 2. **Secure Boot Seçeneğini Bul**
- BIOS'a girdikten sonra, **Security** veya **Boot** menüsünü bul.
- Menüde **Secure Boot** ayarını araman gerek. Her BIOS'ta menü düzeni farklı olabilir, ancak genelde **Security** veya **Boot** altında bulunur.

### 3. **Secure Boot'u Devre Dışı Bırak**
- **Secure Boot** seçeneğinin üzerine gel ve **Enter** tuşuna bas.
- Açılan menüde **Disable** seçeneğini seç.
  
### 4. **Ayarları Kaydet ve Çık**
- **F10** tuşuna basarak yaptığın değişiklikleri kaydet.
- Kaydetmek için **Yes** veya **OK** seçeneğini seç.

### 5. **Bilgisayarı Yeniden Başlat**
- Ayarları kaydettikten sonra bilgisayarın yeniden başlatılacak. Artık **Secure Boot** devre dışı bırakıldığı için USB cihazın tanınabilir olmalı.

### Önemli Not:
Bazı BIOS sürümlerinde **Secure Boot** seçeneğini devre dışı bırakabilmek için önce **Administrator Password** oluşturman gerekebilir. Eğer **Secure Boot** devre dışı bırakılmıyorsa, bu ayarı bulduktan sonra bir **Supervisor** veya **Administrator Password** belirlemen gerekebilir.

Bu adımları takip ederek Secure Boot'u devre dışı bırakabilirsin. Eğer hala sorun yaşıyorsan, BIOS menüsünde hangi adımda takıldığını belirtirsen yardımcı olabilirim.