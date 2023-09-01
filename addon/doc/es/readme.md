# Speech Logger #

* Autor: Luke Davis, con colaboraciones de James Scholes
* Descargar [versión estable][1]
* Compatibilidad con NVDA: de 2019.3.1 en adelante

Un complemento de [NVDA](https://nvaccess.org/) para registrar el habla en
uno o varios archivos. Puede grabar la voz generada en el equipo local a un
archivo de texto. También puede grabar la voz recibida desde un equipo
remoto mediante el complemento [NVDA Remote](https://nvdaremote.com/) al
mismo archivo o a uno distinto.

### Configuración

Para configurar este complemento, abre el menú NVDA, ve a Preferencias,
luego a Opciones, y finalmente Speech Logger (NVDA+n, p, o, y s hasta llegar
allí en un teclado español). Hay también un gesto sin asignar en la
categoría "Configuración" del diálogo Gestos de entrada que puedes asignar y
usar para abrir rápidamente el diálogo de opciones del complemento. Nota: el
complemento sólo se puede configurar con el perfil normal de NVDA. Este
complemento no es sensible a perfiles. Si crees que hay un caso de uso en el
que pueda operar de manera diferente en perfiles distintos, contacta con el
autor o abre una incidencia en el [repositorio de GitHub][2].

### Se encuentran disponibles las siguientes opciones:

* La carpeta de registro. Puedes introducirla a mano o examinar para buscar
  el directorio de destino deseado, que debe existir ya. Las variables del
  sistema, como %temp% o %userprofile%, se pueden usar en este campo.
* Nombre de archivo de registro local. El archivo creado se situará en la
  carpeta de arriba. Contendrá el habla registrada mientras se usa el modo
  local. Puede ser el mismo archivo que el remoto. Déjalo en blanco para
  deshabilitar completamente este tipo de registro.
* Nombre de archivo de registro remoto. El archivo creado se situará en la
  carpeta de arriba. Contendrá el habla registrada mientras se usa el modo
  remoto. Puede ser el mismo archivo que el local. Déjalo en blanco para
  deshabilitar completamente este tipo de registro.
* Separador. Este cuadro combinado permite elegir uno de los separadores de
  secuencias disponibles. Más adelante se proporciona más información.
* Separador personalizado. Este campo permite introducir un separador de
  secuencias personalizado (lee más abajo), que se usa si se elige
  "personalizado" en el cuadro combinado.
* Modo de sello de tiempo. Este cuadro combinado permite elegir entre no
  usar marcas de tiempo, y una marca de tiempo al inicio y al final de cada
  sesión de registro.
* Modo registrar voz al verbalizar todo (leer hasta el final). El
  complemento registra la voz generada al pulsar NVDA+flecha abajo (NVDA+a
  en la distribución portátil). Si no quieres registrar textos tan largos,
  desmarca esta casilla.
* Iniciar registro al arrancar. Se puede configurar esta opción en "siempre"
  si quieres que se registre la voz automáticamente cuando NVDA se
  inicia. Esto sólo se aplica a la voz local, y el valor por defecto es
  "nunca".

#### SEPARADOR DE SECUENCIAS

Cuando NVDA verbaliza algo como "`Papelera de reciclaje  1 de 55`" al leer
el escritorio, esto se considera como dos secuencias separadas. La primera
es el nombre del elemento ("`Papelera de reciclaje`" en este ejemplo), y la
segunda es la información de posición del objeto ("`1 de 55`" en este
ejemplo).

Dependiendo de lo que leas y cómo esté configurado NVDA, puede haber varias
secuencias separadas que se suceden en un único mensaje de voz.

En el registro normal de NVDA con el nivel de depuración habilitado, cada
secuencia individual se separa con dos espacios, como se ha escrito en el
ejemplo anterior.

Speech Logger te permite separar las secuencias igual que lo hace NVDA (con
dos espacios), o con una de las pocas alternativas razonables (un salto de
línea, una coma y un espacio, un tabulador, dos guiones bajos), o con la
secuencia de caracteres que prefieras.

Si, por ejemplo, quisieras que tu separador de secuencias fuese dos signos
de dólar (`$$`), configurarías el cuadro combinado en "personalizado", e
introducirías "`$$`" (sin las comillas) en el campo de separador
personalizado. Si quisieras una línea en blanco seguida de un tabulador,
podrías introducir "`\n\t`".

### Iniciar y detener el registro

Este complemento tiene dos gestos configurados por defecto. Puedes
cambiarlos en la categoría Herramientas del diálogo Gestos de entrada de
NVDA. Busca "Conmuta el registro de la voz local" y "Conmuta el registro de
la voz remota".

* NVDA+alt+l: inicia o detiene el registro del habla local.
* NVDA+shift+alt+l: inicia o detiene el registro del habla remota.

### Nota sobre el registro del habla remota

Este complemento está pensado para funcionar con el complemento NVDA Remote
para registrar la voz remota.

Es importante saber que no es posible iniciar el registro de sesiones
remotas hasta que realmente inicies una. No hay forma, por ejemplo, de
iniciar el registro, mantenerlo en espera hasta que comience la sesión y
empezar a registrar en ese momento.

Sin embargo, una vez comience, el registro continuará durante todas las
sesiones remotas.

### Comentarios y solicitud de características

Si deseas sugerir una función o informar de un fallo, contacta por correo o
abre una [incidencia][2].

[[!tag dev stable]]

[[!tag dev stable]]

[1]: https://www.nvaccess.org/addonStore/legacy?file=speechLogger

[2]: https://github.com/opensourcesys/speechLogger/issues/new
