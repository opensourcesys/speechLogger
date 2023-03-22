### Complemento NVDA Speech Logger

Autor: Luke Davis, com contribuições de James Scholes

Um complemento do [NVDA](https://nvaccess.org/) para registrar a fala em um arquivo ou arquivos.
Ele pode registrar a fala gerada na máquina local em um arquivo de texto.
Ele também pode registrar a fala de uma máquina remota recebida por meio do complemento [NVDA Remote](https://nvdaremote.com/), no mesmo arquivo ou em um arquivo diferente.

### Configuração

Para configurar este add-on, abra o menu do NVDA, vá para Preferências, depois Configurações, depois Speech Logger (NVDA+N, P, Ç, depois pressione S até chegar lá).

Nota: o add-on só pode ser configurado enquanto estiver no perfil de Configuração Normal do NVDA. O complemento não reconhece o perfil. Se você conseguir pensar em algum caso de uso que exija que ele opere de maneira diferente em diferentes perfis, entre em contato com o autor ou registre um problema no [repositório do GitHub](https://github.com/opensourcesys/speechLogger/issues/).

As seguintes configurações estão disponíveis:
* O diretório de registro. Você pode inserir ou procurar o diretório de destino desejado, que já deve existir. Variáveis ​​de sistema como %temp%, %userprofile%, etc., podem ser usadas neste campo.
* Nome do arquivo de registro local. O arquivo criado será colocado no diretório acima. Isso conterá a fala registrada enquanto o modo de registro local estiver ativado. Isso pode ser o mesmo que o arquivo de log remoto. Deixe em branco para desativar completamente esse tipo de registro.
* Nome do arquivo de registro remoto. O arquivo criado será colocado no diretório acima. Isso conterá a fala registrada enquanto o modo de registro remoto estiver ativado. Pode ser o mesmo que o arquivo de log local. Deixe em branco para desativar completamente esse tipo de registro.
* Separador. Esta caixa de combinação permite escolher um dos separadores de enunciados disponíveis. Veja abaixo para mais informações.
* Separador personalizado. Este campo permite que você insira um separador de elocução personalizado (veja abaixo), que é usado se "personalizado" for escolhido na caixa de combinação.

#### Separador de enunciados

Quando o NVDA fala algo como "`lixeira 1 de 55`" enquanto está lendo sua área de trabalho, isso é considerado duas declarações separadas. O primeiro é o nome do item ("`Lixeira`", neste exemplo), e o segundo é a informação da posição do objeto ("`1 de 55`", neste exemplo).

Dependendo do que você está lendo, e como você configurou o NVDA, pode haver vários enunciados separados que acontecem durante uma única sequência de fala.

No log normal do NVDA no nível de depuração, cada expressão individual é separada com dois espaços, como está escrito no exemplo acima.

O Speech Logger permite separar enunciados da mesma forma que o NVDA faz (com dois espaços), ou por uma das poucas alternativas razoáveis ​​(uma nova linha, uma vírgula e um espaço, dois sublinhados), ou por uma sequência personalizada de sua própria criação .

Se, por exemplo, você quiser que seu separador de elocução seja dois cifrões (`$$`), defina a caixa de combinação como "custom" e digite "`$$`" (sem as aspas), no separador personalizado campo. Se você quiser que seja uma guia, você pode inserir "`\t`".

### Iniciando e parando os logs

Este complemento tem dois gestos definidos por padrão. Você pode alterá-los na opção definir comandos do NVDA.
Procure "Alterna o registro da fala local" e "Alterna o registro da fala remota".
* NVDA+Alt+L: inicia/interrompe o registro da fala local.
* NVDA+Shift+Alt+L: iniciar/parar registro de fala remota.

### Uma observação sobre o registro remoto de fala

Este add-on destina-se a funcionar com o add-on NVDA Remote, para registro de fala remota.

É importante saber que não é possível iniciar o registro de sessões remotas até que você realmente inicie uma.
Não há como, por exemplo, iniciar o log e esperar, em stand-by, até que uma sessão remota seja iniciada e iniciar o log nesse momento.

No entanto, uma vez iniciado, o registro continuará habilitado para sessões remotas.

### Comentários e solicitações de recursos

Se você gostaria de sugerir um recurso ou relatar um bug, entre em contato por e-mail ou registre um [problema](https://github.com/opensourcesys/speechLogger/issues/).

Como sempre, gosto de saber que meus complementos são úteis e para que as pessoas os estão usando.
