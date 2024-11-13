***Soru:*** dijitalocean server ımı tıpkı yeni başlamış gibi sıfırdan resetlemek isterim

**Cevap:** DijitalOcean sunucunuzu sıfırlamak ve yeniden başlatmak için aşağıdaki adımları takip edebilirsiniz. Bu işlem sunucunuzdaki tüm verilerin silinmesine ve sunucunun fabrika ayarlarına geri dönmesine neden olacaktır, bu yüzden devam etmeden önce önemli verilerinizi yedeklediğinizden emin olun.

### DijitalOcean Sunucunuzu Sıfırlama Adımları

1. **Sunucuya Yedek Alma (Opsiyonel)**
   - Eğer sunucudaki verilerinizi yedeklemek istiyorsanız, SSH ile sunucunuza bağlanın ve verilerinizi başka bir yere aktarın:
     ```bash
     rsync -avz /home/ahmety önemli-dosyalar /path/to/backup/
     ```
   - Veya bir snapshot (anlık görüntü) oluşturabilirsiniz. Snapshot almak için DigitalOcean panelinden `Snapshots` sekmesine gidin ve bir anlık görüntü oluşturun.

2. **DijitalOcean Paneline Giriş Yapın**
   - [DigitalOcean](https://cloud.digitalocean.com/login) hesabınıza giriş yapın.

3. **Proje ve Droplet Seçimi**
   - Giriş yaptıktan sonra, sıfırlamak istediğiniz sunucunun (droplet) bulunduğu projeyi seçin.
   - Ardından, sıfırlamak istediğiniz `Droplet`'i seçin.

4. **Droplet Sıfırlama (Rebuild İşlemi)**
   - `Droplet` detay sayfasına girdikten sonra, sol menüden `Destroy` sekmesini seçin.
   - `Rebuild Droplet` seçeneğine tıklayın. 
   - Açılan ekranda, sunucunuzu yeniden oluşturmak için kullanılacak imajı seçebilirsiniz (örneğin Ubuntu 20.04 veya başka bir işletim sistemi imajı).
   - `Rebuild Droplet` butonuna basarak işlemi başlatın.

5. **Yeniden Başlama**
   - `Rebuild` işlemi sunucunuzun tüm verilerini silecek ve seçtiğiniz imajla sıfırdan kurulmasına neden olacaktır.
   - İşlem tamamlandığında, yeni bir IP adresi ve SSH erişim bilgileri ile sunucuya bağlanabilirsiniz.
   - Yeniden oluşturulan sunucuda, SSH anahtarlarınız veya root şifreniz de varsayılan hale gelir. Bu bilgileri yeniden ayarlamanız gerekecek.

6. **SSH ile Bağlanma**
   - `Rebuild` işlemi tamamlandıktan sonra sunucunuza SSH ile şu şekilde bağlanabilirsiniz:
     ```bash
     ssh root@your_new_droplet_ip
     ```
   - İlk bağlandığınızda root şifrenizi veya SSH anahtarınızı yeniden eklemeniz gerekecektir.

7. **Yedeklerinizi Geri Yükleyin (Opsiyonel)**
   - Yedeklediğiniz dosyalarınızı geri yüklemek için, yedeğinizi aldığız yere SSH ile bağlanarak sunucunuza aktarabilirsiniz:
     ```bash
     rsync -avz /path/to/backup/ root@your_new_droplet_ip:/home/ahmety
     ```

Bu adımları uygulayarak sunucunuzu sıfırlayabilirsiniz. Eğer daha karmaşık bir kurulum veya yapılandırma gerekiyorsa, detayları bana iletebilirsiniz.

***Soru:*** bu hesabıma ekstra bir parasal yük veir mi

**Cevap:** Droplet'inizi sıfırlama işlemi (Rebuild) genellikle hesabınıza ek bir maliyet getirmez. Ancak, belirli durumlar ve ek hizmetlerin kullanımı maliyetlerinizi artırabilir. İşte bu konuyla ilgili bazı önemli noktalar:

### Ek Maliyet Yaratabilecek Durumlar:
1. **Snapshots (Anlık Görüntü):**
   - Rebuild işleminden önce bir `Snapshot` (anlık görüntü) oluşturduysanız, bu snapshot hesabınıza ek maliyet olarak yansıtılabilir. Snapshotlar, disk alanına göre ücretlendirilir ve genellikle aylık olarak maliyet hesaplanır. Snapshotları kullanmadığınızda silmeyi düşünebilirsiniz.
   
2. **Ek Droplet veya Sunucu Oluşturma:**
   - Rebuild işlemi sırasında **yeni bir Droplet oluşturmazsınız**, var olan Droplet üzerinde işlem yaparsınız. Bu yüzden ek bir Droplet oluşturmadığınız sürece ekstra bir maliyet oluşmaz.
   
3. **Disk Alanı ve Veri Transferi:**
   - Rebuild işlemi sırasında ek bir disk alanı veya veri transferi kullanmadığınız sürece ek bir maliyet oluşmaz. Ancak yeni işletim sistemi kurulumları veya yeni verilerin yüklenmesi ekstra disk alanı kullanımına neden olabilir.
   
4. **Ek Hizmetler ve Eklentiler:**
   - DigitalOcean üzerinde kullanılan `Load Balancer`, `Block Storage` veya `Databases` gibi ek hizmetler rebuild işleminden etkilenmez ve bu hizmetlerin normal maliyeti işlem sırasında devam eder. Bu hizmetlerin kullanımı maliyeti artırabilir.

### Öneriler:
- **Snapshot'ları Kontrol Edin:** Snapshot oluşturup oluşturmadığınızı kontrol edin ve gereksiz snapshotları silin. Panelde `Images` sekmesinden Snapshot'ları görebilir ve silebilirsiniz.
- **Ekstra Droplet Oluşturmadığınızdan Emin Olun:** Rebuild işlemi mevcut Droplet'i kullanır, bu yüzden ekstra bir Droplet oluşturmadığınızdan emin olun.
- **Fatura Detaylarınızı Kontrol Edin:** Herhangi bir beklenmeyen maliyet olup olmadığını görmek için DigitalOcean hesabınızda `Billing` sekmesine gidip maliyet detaylarını inceleyebilirsiniz.

Bu açıklamalar doğrultusunda, rebuild işlemi için ekstra bir maliyet oluşmayacaktır. Ancak snapshotlar veya ek hizmetler varsa bunlar aylık maliyet olarak yansıyabilir.

***Soru:*** root tan normal kullanucuma nası lgeçerim

**Cevap:** Root kullanıcısından normal kullanıcıya geçmek için SSH veya terminal bağlantısı üzerinden aşağıdaki yöntemleri kullanabilirsiniz. Bu yöntemlerle root yetkilerinden çıkarak normal kullanıcıya geçiş yapabilirsiniz.

### 1. **Normal Kullanıcıya Geçiş: `su - [kullanıcı_adı]` Komutu**
Eğer root kullanıcısında iseniz ve normal bir kullanıcıya geçmek istiyorsanız, `su` komutunu kullanabilirsiniz:

```bash
su - ahmety
```

Bu komut, `ahmety` adlı normal kullanıcıya geçmenizi sağlar. Komut çalıştıktan sonra ilgili kullanıcının yetkileriyle çalışmaya başlarsınız. Eğer bu kullanıcıya geçiş yaparken parola sorarsa, `ahmety` kullanıcısının parolasını girmeniz gerekecektir.

### 2. **Kullanıcı Geçişi için `sudo -i -u [kullanıcı_adı]` Komutunu Kullanma**
Bir başka yöntem de `sudo` komutunu kullanmaktır. `sudo` komutuyla geçiş yaparak normal kullanıcıya ait bir oturum açabilirsiniz:

```bash
sudo -i -u ahmety
```

Bu komut, `ahmety` kullanıcısına geçiş yapar ve doğrudan `ahmety` kullanıcısının terminaline ulaşmanızı sağlar.

### 3. **`ssh` Kullanarak Normal Kullanıcıya Geçme**
Eğer uzaktan bağlantı (SSH) üzerinden root kullanıcısı olarak giriş yaptıysanız, normal kullanıcıya geçiş yapmanın bir diğer yolu `ssh` komutudur:

```bash
ssh ahmety@localhost
```

Bu komut, yerel makinede `ahmety` kullanıcısına bağlanmanızı sağlar. `localhost` ifadesi yerel sunucuyu işaret eder ve `ahmety` kullanıcısının parolasını girerek geçiş yapabilirsiniz.

### 4. **Çıkış Yapıp Normal Kullanıcı ile Tekrar Giriş Yapma**
Root oturumundan çıkıp normal kullanıcı ile giriş yapabilirsiniz:

```bash
exit
```

Ardından normal kullanıcınız ile tekrar giriş yapabilirsiniz:

```bash
ssh ahmety@sunucu_ip_adresi
```

Bu yöntemlerle root kullanıcısından normal kullanıcıya geçiş yapabilirsiniz.

***Soru:*** eski droplet kaldırdım ve yeni açtım tek droplet varsa fiyat aynıdır değil mi

**Cevap:** Evet, DigitalOcean üzerinde sadece bir adet Droplet varsa ve mevcut Droplet'i silip yerine yenisini oluşturduysanız, **toplam maliyet değişmez**. Fiyatlandırma yalnızca aktif olan Droplet sayısına ve seçilen Droplet planına (örneğin CPU, RAM, Disk Alanı) göre yapılır.

### Detaylı Açıklama:
1. **Droplet Fiyatlandırma:** DigitalOcean, Droplet'lerinizi belirlediğiniz plana göre ücretlendirir. Örneğin, 2 GB RAM ve 1 CPU çekirdeğine sahip bir Droplet için aylık sabit bir ücret ödersiniz. Mevcut Droplet'i silip yenisini oluşturduğunuzda, aynı plan seçildiği sürece aylık ödediğiniz ücret değişmez.

2. **Ekstra Ücretler:**
   - **Silinen Droplet'e Ait Ekstra Snapshot veya Yedekler:** Silinen Droplet ile ilişkilendirilmiş snapshotlar veya yedekler varsa, bu dosyalar hala hesabınızda yer kaplayabilir ve ek ücretlendirmeye sebep olabilir. Bu yüzden Droplet'i silmeden önce snapshotları ve yedekleri silmek maliyeti düşürebilir.
   - **Ek Hizmetler (Block Storage, Load Balancer, vb.):** Eğer bu ek hizmetleri kullanıyorsanız ve sadece Droplet silme işlemi yaptıysanız, bu hizmetler için ücretlendirme devam eder.

3. **Yeniden Oluşturulan Droplet:**
   - Silip yeniden oluşturduğunuz Droplet aynı plan ve yapılandırma ile oluşturulduysa, aynı ücreti ödemeye devam edersiniz. DigitalOcean yalnızca aktif Droplet'leri ve ek hizmetleri faturalandırır.

### Özet:
Eğer sadece eski Droplet'i silip yerine yeni bir tane eklediyseniz ve başka ek Droplet veya hizmet yoksa, hesabınıza yansıyan toplam maliyet **aynı kalacaktır**. 

Yine de, bu tür değişiklikler yaptıktan sonra maliyetlerinizi kontrol etmek için **DigitalOcean hesabınızın `Billing` (Faturalama) sekmesinden** maliyet detaylarınızı gözden geçirmenizi öneririm. Bu sayede beklenmeyen bir durum olup olmadığını görebilirsiniz.

***Soru:*** peki dropletimi silersem ücret ödemem artık değik mi

**Cevap:** Evet, **Droplet'i tamamen sildiğinizde** o Droplet için artık ücret ödemezsiniz. DigitalOcean yalnızca aktif olarak kullanılan kaynaklar (Droplet, Block Storage, Load Balancer vb.) için ücret alır. Eğer tek Droplet'inizi silerseniz ve başka bir ek hizmet kullanmıyorsanız, o Droplet için herhangi bir ücretlendirme yapılmaz. Ancak dikkat etmeniz gereken bazı durumlar vardır:

### Önemli Noktalar:
1. **Droplet'in Silinmesi:**
   - Droplet'i tamamen silmek için DigitalOcean panelinden `Droplet`'i seçip `Destroy` seçeneğine tıklayabilirsiniz. Bu işlem yapıldığında Droplet'iniz ve içindeki tüm veriler kalıcı olarak silinir.

2. **Faturalandırma:**
   - Droplet silindiğinde, o Droplet için aylık faturalandırma durur. Eğer Droplet'i ay ortasında silerseniz, yalnızca o aya kadar kullandığınız günler için ücretlendirilirsiniz.
   - Örneğin, Droplet'i ayın 15'inde sildiyseniz, yalnızca ayın 1'i ile 15'i arasındaki kullanım için ödeme yaparsınız.

3. **Snapshot ve Yedekler (Backups):**
   - Eğer Droplet'i silmeden önce bir `Snapshot` veya `Yedek` (Backup) oluşturduysanız, bu dosyalar hesabınızda kalmaya devam eder ve **ekstra ücret** olarak yansıtılır.
   - Snapshotlar, disk alanına göre ücretlendirilir ve genellikle aylık olarak faturalandırılır. Snapshotları silmediğiniz sürece hesabınızdan düşmez.

4. **Ekstra Hizmetler:**
   - `Block Storage`, `Load Balancer` gibi ek hizmetler, Droplet silinse bile aktif kalabilir ve bunlar için ayrı bir ücretlendirme yapılır. Eğer bu hizmetleri kullanmıyorsanız, ilgili hizmetleri de silmeniz gereklidir.

5. **Fatura Detaylarını Kontrol Edin:**
   - Droplet'i sildikten sonra `Billing` sekmesinden fatura detaylarını kontrol edebilirsiniz. Eğer beklenmedik bir ücretlendirme görürseniz, bu muhtemelen snapshotlar veya ek hizmetlerle ilgilidir.

### Özet:
- **Droplet'i silerseniz:** Droplet için ücret ödemezsiniz.
- **Snapshot veya yedekler varsa:** Bu dosyalar için ücret ödemeye devam edersiniz.
- **Ek hizmetler varsa:** Bu hizmetler ayrı ayrı ücretlendirilmeye devam eder.

Droplet'i silme işlemi sonrasında oluşabilecek herhangi bir beklenmedik maliyet veya hizmeti kontrol etmek için, DigitalOcean panelinden `Billing` sekmesini incelemenizi öneririm.