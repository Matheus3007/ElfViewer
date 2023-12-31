# ElfViewer
Prova prática da disciplina PCS3732. Esse aplicativo permite a visualização da estrutura de memória de um arquivo .elf qualquer.

Uma demonstração do projeto pode ser vista no video abaixo:
https://youtu.be/TW_w94GM_XA

# Como buildar
Primeiro, clone o repositório para a sua máquina
```
git clone https://github.com/Matheus3007/ElfViewer
```
Em seguida, instale as dependencias do Python
```
pip install pygame tqdm tabulate pandas json 
```
Isso feito, tudo deve estar OK na sua máquina.

# Executando
Para executar, basta rodar python `./main.py` e um display irá abrir requisitando um arquivo de texto. Esse arquivo deve ser um disassemble de qualquer executável ARM32, feito através de um comando `objdump -S`, para que dessa forma, todas as informações necessárias para a renderização da imagem.

Ao final da execução, é possível sair apertando `esc`, e quando isso é feito, uma imagem com a saída inicial do programa é salva em `output.png`. Bem legal se você quer usar alguma coisa de plano de fundo ou pra demonstração!
## Parâmetros
Alguns parâmetros opcionais podem ser fornecidos para o programa ao chamar a main. Eles são os seguintes (a ordem deve ser respeitada):
| Parâmetro   | Descrição                                                                                          | Opções                      |
|-------------|----------------------------------------------------------------------------------------------------|-----------------------------|
| Tamanho     | Define o tamanho da renderização, default é average.                                               | Tiny, Average, Large, Linux |
| Linearidade | Define a forma como as instruções são posicionadas, se de acordo com a memória ou sequencialmente. | Linear, Relative            |
| Tema        | Tema de cores da renderização. Mais estético mesmo.                                                | Ver pasta temas             |

É importante notar que os parâmetros não podem ser passados desordenados e não podem ser omitidos caso um seguinte queira ser utilizado (se quiser mudar o tema tem que passar todos os três parâmetros).

Um exemplo de chamada é o seguinte:
```
python main.py tiny linear DraculasDelight
```
Este comando chama o programa no modo de renderização tiny, com instruções posicionadas sequencialmente e com o tema de cores Dracula.

Isto feito, fornecer o caminho para o arquivo desejado. No caso, dentro da pasta `./dumps` deste projeto existem algumas saídas para teste e demonstração.

### Temas fornecidos
#### Funcionais
- AluHighlight | Highlight de instruções de ALU
- BranchHighlight | Highlight de instruções de Branch
- CoprocHighlight | Highlight de instruções de Coprocessador
- MemoryHighlight | Highlight de instruções de Memória
- StackHighlight | Highlight de instruções de Stack

#### Estéticos
- BarbieBrigade | Rosa
- DebuggersDream | Tema default, alto contraste
- DraculasDelight | Tema estilo *Dracula*
- GreyGrievance | Tema Grayscale
- MonokaiMadness | Tema estilo *Monokai* 
- NordicNausea | Tema estilo *Nord*
- RuthlessRats | Tema da Atlética da Poli
- SolarizedSummer | Tema estilo *Solarized Dark*
- TerminalTragedy | Tema em tons de verde e laranja

***
Para uma visão mais detalhista das funções do programa, verificar a pasta Doc do diretório, ela contém a descrição das funções e do funcionamento geral do projeto.