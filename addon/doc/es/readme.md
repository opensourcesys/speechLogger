### Complemento Speech Logger para NVDA

Autor: Luke Davis, con la colaboración de James Scholes

Un complemento de [NVDA](https://nvaccess.org/) para registrar voz en un archivo o archivos.
Puede registrar la voz generada en la máquina local en un archivo de texto.
También puede registrar el habla de una máquina remota recibida a través del complemento [NVDA Remote](https://nvdaremote.com/), ya sea al mismo archivo o a uno diferente.

### Configuración

Para configurar este complemento, abre el menú de NVDA, ve a Preferencias, luego Opciones, luego Speech Logger (NVDA+N, P, S, luego presiona S hasta llegar allí, en un teclado predeterminado en inglés de EE. UU.).

Nota: el complemento solo se puede configurar en el perfil de configuración normal de NVDA. El complemento no reconoce el perfil. Si puede pensar en algún caso de uso que requiera que funcione de manera diferente en diferentes perfiles, por favor comuníquese con el autor o presente un issue en el [repo de GitHub](https://github.com/opensourcesys/speechLogger/issues/).

Están disponibles los siguientes ajustes:

* El direcotrio del registro. Puede ingresar o buscar el directorio de destino deseado, que ya debe existir. Variables del sistema como %temp%, %userprofile%, etc., se pueden utilizar en este campo.
* Nombre de archivo de registro local. El archivo creado se colocará en el directorio anterior. Esto contendrá la voz registrada mientras el modo de registro local esté activado. Esto puede ser lo mismo que el archivo de registro remoto. Déjelo en blanco para deshabilitar completamente este tipo de registro.
* Nombre de archivo de registro remoto. El archivo creado se colocará en el directorio anterior. Esto contendrá el registro de voz mientras el modo de registro remoto está activado. Puede ser el mismo que el archivo de registro local. Déjelo en blanco para deshabilitar completamente este tipo de registro.
* Separador. Este cuadro combinado le permite elegir uno de los separadores de expresiones disponibles. Vea abajo para más información.
* Separador personalizado. Este campo le permite ingresar un separador de expresión personalizado (ver a continuación), que se usa si se elige "personalizado" en el cuadro combinado.

#### Separador de expresiones

Cuando NVDA pronuncia algo como "papelera de reciclaje 1 de 55" mientras lee tu escritorio, esto se considera como dos anunciados separados. El primero es el nombre del elemento ("Papelera de reciclaje", en este ejemplo), y el segundo es la información de posición del objeto ("1 de 55", en este ejemplo).

Dependiendo de lo que estés leyendo y de cómo hayas configurado NVDA, puede haber varios anunciados separados que sucedan durante una sola secuencia de voz.

En el registro normal de NVDA a nivel de depuración, cada expresión individual se separa con dos espacios, como está escrito en el ejemplo anterior.

Speech Logger le permite separar anunciados de la misma manera que lo hace NVDA (con dos espacios), o mediante una de algunas alternativas razonables (una nueva línea, una coma y un espacio, dos guiones bajos), o mediante una secuencia personalizada de su propia invención. .

Si, por ejemplo, quisiera que su separador de expresiones tuviera dos signos de dólar ($$), configuraría el cuadro combinado como "personalizado" e ingresaría "$$" (sin las comillas), en el campo separador personalizado. Si quisiera que fuera una pestaña, podría ingresar "\t".

### Iniciar y detener el registro

Este complemento tiene dos gestos configurados de forma predeterminada. Puedes cambiarlos en la categoría Tools de gestos de entrada de NVDA.
Busque "Alterna el registro de voz local" y "Alterna el registro de voz remota".

* NVDA+Alt+L: iniciar/detener el registro de voz local.
* NVDA+Shift+Alt+L: iniciar/detener el registro de voz remota.

### Una nota sobre el registro de voz remota

Este complemento está diseñado para funcionar con el complemento NVDA Remote, para el registro de voz remota.

Es importante saber que no es posible iniciar el registro de sesiones remotas hasta que realmente inicie una. No hay forma de, por ejemplo, comenzar a iniciar sesión y esperar, en modo de espera, hasta que se inicie una sesión remota y comenzar a iniciar sesión en ese momento.

Sin embargo, una vez iniciado, el registro continuará en las sesiones remotas.

### Comentarios y solicitudes de funciones

Si desea sugerir una función o informar un error, comuníquese por correo electrónico o presente un [issue](https://github.com/opensourcesys/speechLogger/issues/).

Como siempre, agradezco saber que mis complementos son útiles y para qué los usa la gente.