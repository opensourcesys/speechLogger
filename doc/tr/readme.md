### NVDA Konuşma Kaydedici eklentisi

Yazar: Luke Davis, James Scholes'in katkılarıyla.  

Konuşmayı bir dosyaya veya dosyalara kaydetmek için bir [NVDA](https://nvaccess.org/) eklentisi.  
Yerel makinede oluşturulan konuşmayı bir metin dosyasına kaydedebilir.  
Ayrıca [NVDA Remote](https://nvdaremote.com/) eklentisi aracılığıyla alınan uzak bir makineden gelen konuşmayı aynı veya farklı bir dosyaya kaydedebilir.  

### Yapılandırma

Bu eklentiyi yapılandırmak için NVDA menüsünü açın, Tercihler'e, ardından Ayarlar'a, ardından Konuşma Kaydedici'ye gidin.  
(NVDA+N, T, L ve Konuşma kaydediciye erişene kadar K'ye basın.)  

Not: Eklenti yalnızca NVDA'nın Normal profilindeyken yapılandırılabilir. Eklentide, diğer profiller desteklenmiyor. Farklı profillerde farklı şekilde çalışmasını gerektiren bir kullanım durumu düşünürseniz, lütfen yazarla iletişime geçin veya [GitHub deposunda](https://github.com/opensourcesys/speechLogger/issues/) bir sorun bildirin.  

Aşağıdaki ayarlar mevcuttur:
* Günlük dizini. Halihazırda var olması gereken, istediğiniz hedef dizine girebilir veya göz atabilirsiniz. %temp%, %userprofile% vb. gibi sistem değişkenleri burada kullanılabilir.field.
* Yerel günlük dosya adı. Oluşturulan dosya yukarıdaki dizine yerleştirilecektir. Bu, yerel günlük modu devredeyken kaydedilen konuşmayı içerecektir. Bu, uzak günlük dosyasıyla aynı olabilir. Bu tür günlüğe kaydetmeyi tamamen devre dışı bırakmak için boş bırakın.
* Uzak günlük dosya adı. Oluşturulan dosya yukarıdaki dizine yerleştirilecektir. Bu, uzak günlük modu devredeyken kaydedilen konuşmayı içerecektir. Yerel günlük dosyasıyla aynı olabilir. Bu tür günlüğe kaydetmeyi tamamen devre dışı bırakmak için boş bırakın.
* Ayırıcı. Bu birleşik giriş kutusu, mevcut ifade ayırıcılarından birini seçmenizi sağlar. Daha fazla bilgi için aşağıya bakın.
* Özel ayırıcı. Bu alan, birleşik giriş kutusunda "özel" seçilmişse kullanılan özel bir ifade ayırıcı (aşağıya bakın) girmenizi sağlar.

#### söz ayırıcı

NVDA, masaüstünüzü okurken "`geri dönüşüm kutusu 1 / 55`" gibi bir şey söylediğinde, bu iki ayrı ifade olarak kabul edilir. İlki öğe adıdır (bu örnekte "'Geri dönüşüm kutusu'") ve ikincisi nesne konum bilgisidir (bu örnekte "'1 / 55'").

Ne okuduğunuza ve NVDA'yı nasıl yapılandırdığınıza bağlı olarak, tek bir konuşma sırasında meydana gelen birkaç ayrı ifade olabilir.  

Hata ayıklama düzeyindeki normal NVDA günlüğünde, yukarıdaki örnekte yazıldığı gibi her bir bireysel ifade iki boşlukla ayrılır.  

Konuşma Kaydedici, ifadeleri NVDA'nın yaptığı gibi (iki boşlukla) veya birkaç makul alternatiften biri (yeni satır, virgül ve boşluk, iki alt çizgi) veya kendi tasarladığınız özel bir sıra ile ayırmanıza olanak tanır. .  

Örneğin, sözce ayırıcınızın iki dolar işareti (`$$`) olmasını istiyorsanız, birleşik giriş kutusunu "özel" olarak ayarlar ve özel ayırıcıya ""$$`" (tırnak işaretleri olmadan) girersiniz. Tab. Sekme olmasını istiyorsanız, "`\t`" yazabilirsiniz.  

### Günlüğe kaydetmeyi başlatma ve durdurma

Bu eklentinin varsayılan olarak ayarlanmış iki hareketi vardır. Bunları NVDA Girdi Hareketleri, Tools kategorisinde değiştirebilirsiniz.
"Yerel konuşmanın günlüğe kaydedilmesini açar/kapatır" ve "Uzak konuşma günlüğünü açar/kapatır" öğelerine bakın.
* NVDA+Alt+L: yerel konuşma kaydını başlat/durdur.
* NVDA+Shift+Alt+L: uzak konuşma kaydını başlat/durdur.

### Uzaktan konuşma kaydı hakkında bir not

Bu eklentinin, uzaktan konuşma kaydı için NVDA Remote eklentisi ile çalışması amaçlanmıştır.  

Gerçekten bir bağlantı başlatana kadar uzak oturumlar için günlüğe kaydetmeye başlamanın mümkün olmadığını bilmek önemlidir.  
Örneğin, günlüğe kaydetmeye başlamanın ve uzak bir oturum başlayana kadar beklemede kalmasını ve o anda günlüğe kaydetmeye başlamasını sağlamanın bir yolu yoktur.  

Ancak, bir kez başlatıldığında, günlük kaydı uzak oturumlarda devam eder.  

### Geri bildirim ve özellik istekleri

Bir özellik önermek veya bir hata bildirmek isterseniz, lütfen e-posta ile ulaşın veya bir [sorun](https://github.com/opensourcesys/speechLogger/issues/) bildirin.  

Her zaman olduğu gibi, eklentilerimin yararlı olduğunu ve insanların bunları ne için kullandığını duymaktan mutlu olurum.
