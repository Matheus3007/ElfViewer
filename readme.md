# ElfViewer
Prova prática da disciplina PCS3732. Esse aplicativo permite a visualização da estrutura de memória de um arquivo .elf qualquer.

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

***
Para uma visão mais detalhista das funções do programa, verificar a pasta Doc do diretório, ela contém a descrição das funções e do funcionamento geral do projeto.