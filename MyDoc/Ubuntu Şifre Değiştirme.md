***Soru:*** ubuntuda hesap şifresi değiştirme

**Cevap:** Ubuntu'da kullanıcı hesap şifresini değiştirmek için aşağıdaki adımları izleyebilirsin:

1. Terminali aç (`Ctrl + Alt + T` ile açabilirsin).
2. Şifresini değiştirmek istediğin kullanıcı için şu komutu yaz:
   ```
   passwd
   ```
3. Terminalde senden mevcut şifreni isteyecek. Mevcut şifreni gir.
4. Ardından yeni şifreyi iki kez girmen istenecek.

Eğer başka bir kullanıcının şifresini değiştirmek istiyorsan (yönetici yetkisine sahipsen), şu komutu kullanarak o kullanıcının şifresini değiştirebilirsin:
   ```
   sudo passwd kullanıcı_adı
   ```

Bu işlem sonrasında belirlediğin yeni şifre aktif olacaktır.

***Soru:*** root şifresi değiştirilir mi

**Cevap:** Evet, Ubuntu'da root (yönetici) şifresi değiştirilebilir. Root hesabının varsayılan olarak devre dışı olduğu çoğu Ubuntu sürümünde, önce root hesabını etkinleştirip şifresini ayarlaman gerekiyor. Aşağıdaki adımları izleyebilirsin:

### Root Şifresi Ayarlama veya Değiştirme:
1. Terminali aç (`Ctrl + Alt + T`).
2. Şu komutu kullanarak root için bir şifre belirle:
   ```
   sudo passwd root
   ```
3. Terminal, önce mevcut kullanıcı şifreni, ardından root için yeni bir şifre girmeni isteyecektir. Yeni root şifresini iki kez girerek doğrulayabilirsin.

Bu işlemi yaptıktan sonra root kullanıcısı için bir şifre ayarlanmış olacaktır. Root şifresini değiştirmek istersen, yukarıdaki adımları tekrar uygulayabilirsin.

### Root Kullanıcısını Aktif Etme (Eğer Gerekirse):
Ubuntu'da root kullanıcısı genellikle devre dışı olduğundan, root olarak giriş yapmak istersen önce root hesabını etkinleştirmen gerekebilir:
   ```
   sudo -i
   ```

Bu komutla geçici olarak root yetkilerini kazanabilirsin.