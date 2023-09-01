# Konuşma Kaydedici #

* Yazar: Luke Davis, James Scholes'un katkılarıyla
* [Kararlı sürümü indirin][1]
* NVDA uyumluluğu: 2019.3.1 ve sonrası

Konuşmayı dosya veya dosyalara kaydetmek için bir
[NVDA](https://nvaccess.org/) eklentisi. Yerel makinede oluşturulan
konuşmayı bir metin dosyasına kaydedebilir. Ayrıca uzak bir makineden [NVDA
Uzaktan Destek](https://nvdaremote.com/) eklentisi aracılığıyla alınan
konuşmayı aynı veya farklı bir dosyaya kaydedebilir.

### Yapılandırma

Bu eklentiyi yapılandırmak için NVDA menüsünü açın, Tercihler'e, ardından
Ayarlar'a ve ardından Konuşma Kaydedici'ye gidin (NVDA+N, T, L, ardından
varsayılan ABD İngilizcesi klavyede oraya ulaşana kadar K tuşuna
basın). Ayrıca Girdi Hareketleri "Yapılandırma" kategorisinde eklentinin
ayarlarını doğrudan hızlı bir şekilde açmak için atayabileceğiniz ve
kullanabileceğiniz atanmamış bir hareket vardır. Not: Eklenti yalnızca
NVDA'nın Normal Yapılandırma profilindeyken yapılandırılabilir. Eklenti
profil uyumlu değildir. Farklı profillerde farklı şekilde çalışmasını
gerektiren bir kullanım durumu aklınıza geliyorsa, lütfen yazarla iletişime
geçin veya [GitHub deposunda][2] bir sorun bildirin.

### Aşağıdaki ayarlar mevcuttur:

* Günlük dizini. Halihazırda var olması gereken, istediğiniz hedef dizini
  girebilir veya bu dizine göz atabilirsiniz. Bu alanda %temp%,
  %userprofile% gibi sistem değişkenleri kullanılabilir.
* Yerel günlük dosya adı. Oluşturulan dosya yukarıdaki dizine
  yerleştirilecektir. Bu, yerel günlük modu devredeyken günlüğe kaydedilen
  konuşmayı içerecektir. Bu, uzak günlük dosyasıyla aynı olabilir. Bu tür
  günlüğü tamamen devre dışı bırakmak için boş bırakın.
* Uzak günlük dosya adı. Oluşturulan dosya yukarıdaki dizine
  yerleştirilecektir. Bu, uzak günlük modu devredeyken günlüğe kaydedilen
  konuşmayı içerecektir. Yerel günlük dosyasıyla aynı olabilir. Bu tür
  günlüğü tamamen devre dışı bırakmak için boş bırakın.
* Ayırıcı. Bu birleşik giriş kutusu, mevcut ifade ayırıcılardan birini
  seçmenize izin verir. Daha fazla bilgi için aşağıya bakın.
* Özel ayırıcı. Bu alan, açılan kutuda "özel" seçilirse kullanılan özel bir
  deyim ayırıcı (aşağıya bakın) girmenizi sağlar.
* Zaman damgası modu. Bu açılan kutu, zaman damgası olmaması ile her günlük
  oturumunun başında ve sonunda bir zaman damgası arasında seçim yapmanızı
  sağlar.
* Tümünü söyle (sonuna kadar oku) modunda konuşmayı günlüğe kaydedin. Bu
  eklenti, NVDA+Aşağı Ok (dizüstü bilgisayar düzeninde NVDA+a) tuşlarına
  bastığınızda oluşturulan konuşmayı günlüğe kaydeder. Bu tür uzun
  anlatıların günlüğe kaydedilmesini istemiyorsanız, bu kutunun işaretini
  kaldırın.
* Başlangıçta günlüğe kaydetmeye başla. NVDA başladığında konuşmanın
  otomatik olarak günlüğe kaydedilmesini istiyorsanız, bu seçeneği "Her
  Zaman" olarak ayarlayabilirsiniz. Bu yalnızca yerel konuşma için
  geçerlidir ve varsayılan değer "asla" dır.

#### İfade ayırıcı

NVDA masaüstünüzü okurken "`geri dönüşüm kutusu 1 tire 55 gibi bir şey
söylediğinde, bu iki ayrı ifade olarak kabul edilir.  Birincisi öğe adı
("`Geri dönüşüm kutusu`", bu örnekte), ikincisi ise nesne konum bilgisidir
("`1 tire 55`, bu örnekte).

Ne okuduğunuza ve NVDA'yı nasıl yapılandırdığınıza bağlı olarak, tek bir
konuşma dizisi sırasında birden çok farklı ifade olabilir.

Hata ayıklama seviyesindeki normal NVDA günlüğünde, yukarıdaki örnekte
yazıldığı gibi her bir ifade iki boşlukla ayrılır.

Konuşma Kaydedici, ifadeleri NVDA'nın yaptığı gibi (iki boşlukla) veya
birkaç makul alternatiften biriyle (yeni satır, virgül ve boşluk, sekme, iki
alt çizgi) veya özel bir sıra ile ayırmanıza olanak tanır. kendi tasarımın.

Örneğin, ifade ayırıcınızın iki dolar işareti (`$$`) olmasını istiyorsanız,
birleşik giriş kutusunu "özel" olarak ayarlar ve özel ayırıcıya "`$$`"
(tırnak işaretleri olmadan) girersiniz. alan. Yeni bir satır ve ardından bir
sekme olmasını istiyorsanız, "`\\n\\t`" girebilirsiniz.

### Günlüğe kaydetmeyi başlatma ve durdurma

Bu eklentinin varsayılan olarak ayarlanmış iki hareketi vardır. Bunları NVDA
Girdi Hareketleri iletişim kutusunda Araçlar kategorisinden
değiştirebilirsiniz. "Yerel konuşmanın günlüğe kaydedilmesini açar/kapatır"
ve "Uzaktan konuşmanın günlüğe kaydedilmesini açar/kapatır" ifadelerine
bakın.

* NVDA+Alt+L: yerel konuşma kaydını başlat/durdur.
* NVDA+Shift+Alt+L: uzaktan konuşma kaydını başlat/durdur.

### Uzaktan konuşma kaydı hakkında bir not

Bu eklenti, uzak konuşmanın günlüğe kaydedilmesi için NVDA Uzaktan Destek
eklentisiyle çalışmak üzere tasarlanmıştır.

Gerçekte bir tane başlatana kadar uzak oturumlar için günlüğe kaydetmeye
başlamanın mümkün olmadığını bilmek önemlidir. Örneğin, günlüğe kaydetmeye
başlamanın ve uzak bir oturum başlayana kadar bekleme modunda beklemesini
sağlamanın ve o sırada günlüğe kaydetmeye başlamasının bir yolu yoktur.

Ancak, bir kez başlatıldıktan sonra günlük kaydı uzak oturumlarda devam
edecektir.

### Geri bildirim ve özellik istekleri

Bir özellik önermek veya bir hata bildirmek istiyorsanız, lütfen e-posta ile
iletişime geçin veya bir [sorun][2] gönderin.

Her zaman olduğu gibi, eklentilerimin yararlı olduğunu ve insanların bunları
ne için kullandığını duymaktan memnuniyet duyuyorum.

[[!tag dev stable]]

[1]: https://www.nvaccess.org/addonStore/legacy?file=speechLogger

[2]: https://github.com/opensourcesys/speechLogger/issues/new
