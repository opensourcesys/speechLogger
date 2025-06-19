# Speech Logger #

### Complemento do registrador de fala NVDA

* Autor: Luke Davis, com contribuições de James Scholes
* Download [versão estável][1]
* Compatibilidade com NVDA: 2019.3.1 e posterior

Um complemento do [NVDA][3] para registrar a fala em um arquivo ou
arquivos.  Ele pode registrar a fala gerada no computador local em um
arquivo de texto.  Também pode registrar a fala de uma máquina remota
recebida por meio do complemento [NVDA Remote][5], no mesmo arquivo ou em um
arquivo diferente.

### Configuração

Para configurar esse complemento, abra o menu do NVDA, acesse Preferências,
Configurações e Registrador de fala (NVDA+N, P, S, depois pressione R até
chegar lá, em um teclado padrão em inglês dos EUA).  Há também um gesto não
atribuído na categoria Gestos de entrada “Configuração”, que você pode
atribuir e usar para abrir rapidamente as configurações do complemento
diretamente.  Observação: o complemento só pode ser configurado no perfil
Configuração Normal  do NVDA.  O complemento não é sensível ao perfil.  Se
você puder pensar em algum caso de uso que exija que ele funcione de forma
diferente em perfis diferentes, entre em contato com o autor ou registre um
problema no [repositório do GitHub][2].

### As seguintes configurações estão disponíveis:

* O diretório de registro. Você pode digitar ou procurar o diretório de
  destino desejado, que já deve existir. Variáveis do sistema, como %temp%,
  %userprofile%, etc., podem ser usadas nesse campo.
* Nome do arquivo de registro local. O arquivo criado será colocado no
  diretório acima. Ele conterá a fala registrada enquanto o modo de registro
  local estiver ativado. Ele pode ser o mesmo que o arquivo de registro
  remoto. Deixe em branco para desativar completamente esse tipo de
  registro.
* Nome do arquivo de registro remoto. O arquivo criado será colocado no
  diretório acima. Ele conterá a fala registrada enquanto o modo de registro
  remoto estiver ativado. Pode ser o mesmo que o arquivo de registro
  local. Deixe em branco para desativar completamente esse tipo de registro.
* Separador. Essa caixa de combinação permite que você escolha um dos
  separadores de enunciados disponíveis. Consulte abaixo para obter mais
  informações.
* Separador personalizado. Esse campo permite que você insira um separador
  de enunciado personalizado (veja abaixo), que será usado se
  “personalizado” for escolhido na caixa de combinação.
* Modo de registro de data e hora. Essa caixa de combinação permite escolher
  entre nenhum registro de data e hora e um registro de data e hora no
  início e no fim de cada sessão de registro.
* Registre a fala durante o modo dizer-todos (ler até o fim). Esse
  complemento registra a fala gerada quando você pressiona NVDA+Seta para
  baixo (NVDA+a no layout do laptop). Se preferir que esse tipo de narrativa
  de leitura longa não seja registrado, desmarque essa caixa.
* Iniciar o registro na inicialização. Você pode definir essa opção como
  “Sempre”, se quiser que a fala seja registrada automaticamente quando o
  NVDA for iniciado. Isso se aplica somente à fala local, e o padrão é
  “nunca”.

#### Separador de enunciados

Quando o NVDA fala algo como “`Lixeira 1 de 55`” enquanto está lendo sua
área de trabalho, isso é considerado dois enunciados separados.  A primeira
é o nome do item (“`Lixeira`”, neste exemplo) e a segunda é a informação da
posição do objeto (“`1 de 55`”, neste exemplo).

Dependendo do que você está lendo e de como o NVDA está configurado, pode
haver vários enunciados separados que ocorrem durante uma única sequência de
fala.

No registro normal do NVDA no nível de depuração, cada expressão individual
é separada por dois espaços, como está escrito no exemplo acima.

O Registrador de fala permite que você separe os enunciados da mesma forma
que o NVDA (com dois espaços), ou por uma das poucas alternativas razoáveis
(uma nova linha, uma vírgula e um espaço, uma tabulação, dois sublinhados),
ou por uma sequência personalizada de sua própria autoria.

Se, por exemplo, você quisesse que o separador de expressões fosse dois
cifrões (`$$`), definiria a caixa de combinação como “personalizado” e
digitaria “`$$`” (sem as aspas) no campo separador customizado.  Se você
quisesse que fosse uma nova linha seguida de uma tabulação, poderia digitar
“`\n\t`”.

### Controles:

Esse complemento tem dois atalhos de teclado definidos por padrão e um que
não está atribuído.

Os gestos padrão, que podem ser alterados na categoria “`Registrador de
fala`” dos gestos de entrada do NVDA, são:

* NVDA+Alt+L: iniciar/parar o registro da fala local.
* NVDA+Shift+Alt+L: iniciar/parar o registro de fala remota.

Eles são listados como “Alterna o registro da fala local” e “Alterna o
registro da fala remota”, respectivamente.

Além disso, ele tem um gesto não atribuído para abrir o painel de
configuração, que pode ser atribuído a partir da categoria `Registrador de
fala` nos gestos de entrada do NVDA.

### Uma nota sobre o registro remoto de fala

Esse complemento foi criado para funcionar com o complemento NVDA Remote,
para registro de fala remota.

É importante saber que não é possível iniciar o registro em log de sessões
remotas até que você realmente inicie uma.  Não há como, por exemplo,
iniciar o registro em log e fazer com que ele aguarde, em stand-by, até que
uma sessão remota seja iniciada e comece a registrar em log nesse momento.

No entanto, uma vez iniciado, o registro continuará em todas as sessões
remotas.

### Feedback e solicitações de recursos

Se quiser sugerir um recurso ou relatar um bug, entre em contato por e-mail
ou registre um [issue][2].

Se você achar esse complemento útil, seria de grande ajuda se você pudesse
[deixar uma avaliação][4].

Como sempre, aprecio saber que meus complementos são úteis e descobrir para
que as pessoas os estão utilizando.

[[!tag dev stable]]

[1]: https://www.nvaccess.org/addonStore/legacy?file=speechLogger

[2]: https://github.com/opensourcesys/speechLogger/issues/new

[3]: https://nvaccess.org/

[4]: https://github.com/nvaccess/addon-datastore/discussions/2636

[5]: https://nvdaremote.com/
