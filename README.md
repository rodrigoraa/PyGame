# Caça ao Cristal

## Descrição geral

**Caça ao Cristal** é um jogo feito em Python usando a biblioteca Pygame. O jogador controla um personagem azul dentro de uma janela de 800x600 pixels e deve coletar cristais amarelos que aparecem em posições aleatórias da tela.

Conforme o jogador coleta os cristais, o placar aumenta, a dificuldade cresce aos poucos e inimigos vermelhos aparecem na tela. Se o jogador encostar em um inimigo, o jogo entra em estado de **Game Over**.

## Objetivo do jogador

O objetivo do jogador é coletar o maior número possível de cristais sem colidir com os inimigos. Cada cristal coletado soma 1 ponto ao placar. A partida continua enquanto o jogador conseguir desviar dos inimigos.

## Requisitos para executar

Para executar o projeto, é necessário ter:

- Python instalado no computador.
- Biblioteca `pygame` instalada.

Para instalar o Pygame, use o comando:

```bash
pip install pygame
```

## Como executar o jogo

Abra o terminal na pasta do projeto e execute:

```bash
python caca_ao_cristal.py
```

Se o seu sistema usar `python3`, o comando pode ser:

```bash
python3 caca_ao_cristal.py
```

## Controles

- **Setas do teclado** ou **WASD**: movimentam o jogador.
- **ESC**: sai do jogo.
- **ENTER**: reinicia a partida depois do Game Over.

## Funcionamento do jogador

O jogador é representado na tela por um quadrado azul com borda branca. No código, ele é criado com `pygame.Rect`:

```python
jogador = pygame.Rect(380, 280, 40, 40)
```

Esse retângulo possui posição e tamanho. Os valores `380` e `280` indicam a posição inicial do jogador na tela, enquanto `40` e `40` indicam largura e altura.

O `pygame.Rect` facilita o controle do personagem porque fornece propriedades como `left`, `right`, `top`, `bottom`, `x`, `y`, `centerx` e `centery`. Essas propriedades ajudam tanto na movimentação quanto na detecção de colisões.

O movimento acontece dentro do loop principal usando:

```python
teclas = pygame.key.get_pressed()
```

Esse comando verifica continuamente quais teclas estão pressionadas. Assim, enquanto o jogador segura uma seta ou uma tecla WASD, a posição do retângulo é alterada.

O jogador fica limitado dentro da área da tela com o uso de `max()` e `min()`. Por exemplo, ao mover para a esquerda, o código impede que `jogador.left` fique menor que `0`. Ao mover para cima, o limite mínimo é `60`, porque existe uma barra superior usada para mostrar o placar e a mensagem do jogo.

## Funcionamento do cristal

O cristal é o item coletável do jogo. Ele possui tamanho fixo definido pela constante:

```python
TAMANHO_CRISTAL = 26
```

A função `nova_posicao_cristal()` gera uma nova posição aleatória para o cristal usando `random.randint()`. O eixo X é escolhido dentro dos limites da largura da tela, e o eixo Y é escolhido a partir de `70`, evitando a barra superior.

Antes de retornar o novo cristal, o código verifica se ele nasceu em cima do jogador:

```python
if not cristal.colliderect(jogador):
    return cristal
```

Se houver colisão com o jogador, a função tenta gerar outra posição. Isso evita que o cristal apareça diretamente sobre o personagem.

Na tela, o cristal é desenhado pela função `desenhar_cristal()`. Ele não usa imagem externa. O desenho é feito com formas geométricas, usando `pygame.draw.polygon()`. Os pontos formam um losango amarelo com borda branca.

A coleta acontece quando o retângulo do jogador encosta no retângulo do cristal:

```python
if jogador.colliderect(cristal):
```

Quando isso acontece, o placar aumenta, um novo cristal é criado e a dificuldade do jogo é atualizada.

## Explicação da colisão

O jogo usa o método `colliderect()` do Pygame para verificar colisões entre retângulos.

Mesmo que alguns objetos sejam desenhados como polígonos ou elipses, a colisão é calculada com base no `pygame.Rect` de cada elemento. Isso simplifica bastante a lógica.

A colisão entre jogador e cristal é usada para detectar a coleta:

```python
jogador.colliderect(cristal)
```

Quando essa colisão acontece, o jogador ganha 1 ponto e o cristal muda de lugar.

A colisão entre jogador e inimigos também usa `colliderect()`. Cada inimigo possui um dicionário com um `retangulo`, que representa sua posição e seu tamanho. Se o jogador colidir com esse retângulo, a variável `fim_de_jogo` recebe `True`, encerrando a movimentação normal da partida.

## Explicação do placar

O placar inicia em zero:

```python
placar = 0
```

Sempre que o jogador coleta um cristal, o placar é incrementado:

```python
placar += 1
```

O placar é exibido na barra superior da tela. Para isso, o código usa uma fonte criada com `pygame.font.SysFont()`. A função `desenhar_texto()` recebe o texto, a fonte, a cor e a posição.

Dentro dessa função, `fonte.render()` transforma o texto em uma imagem, e `tela.blit()` desenha essa imagem na tela:

```python
imagem = fonte.render(texto, True, cor)
tela.blit(imagem, (x, y))
```

Assim, a pontuação aparece visualmente para o jogador durante a partida.

## NPCs e inimigos

Os inimigos são os obstáculos vermelhos do jogo. Eles aparecem conforme o jogador coleta cristais.

O primeiro inimigo aparece quando o placar chega a 1. Depois disso, novos inimigos aparecem quando o placar é múltiplo de 3:

```python
if placar == 1 or placar % 3 == 0:
    criar_inimigo()
```

Cada inimigo é criado pela função `criar_inimigo()`. Essa função escolhe aleatoriamente uma das bordas da tela: cima, baixo, esquerda ou direita. Dependendo da borda escolhida, o inimigo nasce em uma posição apropriada e recebe velocidades horizontal e vertical.

Os inimigos são armazenados em uma lista chamada `inimigos`. Cada inimigo é um dicionário com:

- `retangulo`: retângulo usado para posição, desenho e colisão.
- `velocidade_x`: velocidade no eixo horizontal.
- `velocidade_y`: velocidade no eixo vertical.

No loop principal, cada inimigo tem sua posição atualizada:

```python
retangulo.x += inimigo["velocidade_x"]
retangulo.y += inimigo["velocidade_y"]
```

Quando um inimigo encosta nas bordas da tela, sua direção é invertida. Isso faz com que ele rebata nas paredes e continue se movendo dentro da área jogável.

Se o jogador encostar em qualquer inimigo, ocorre Game Over:

```python
if jogador.colliderect(retangulo):
    fim_de_jogo = True
```

## Dificuldade do jogo

A dificuldade aumenta conforme o placar cresce.

A velocidade dos inimigos é calculada com base no placar:

```python
velocidade_inimigos = 3 + placar * 0.15
```

Isso significa que, quanto maior o placar, mais rápidos os inimigos ficam. A função `atualizar_velocidade_inimigos()` atualiza os inimigos que já estão na tela, mantendo a direção atual de cada um.

A velocidade do jogador também aumenta um pouco a cada 2 pontos:

```python
if placar % 2 == 0:
    velocidade_jogador += 0.2
```

O surgimento de novos inimigos também contribui para a dificuldade. O jogo começa sem inimigos, cria o primeiro no primeiro ponto e depois adiciona novos inimigos a cada 3 pontos.

## Loop principal

O loop principal é a parte do código que mantém o jogo funcionando enquanto a variável `rodando` for verdadeira:

```python
while rodando:
```

Dentro dele, o jogo executa várias etapas.

Primeiro, `relogio.tick(FPS)` controla a taxa de atualização do jogo. Como `FPS` vale `60`, o jogo tenta rodar a 60 quadros por segundo.

Depois, ocorre a captura de eventos com:

```python
for evento in pygame.event.get():
```

Nessa parte, o jogo verifica se o jogador fechou a janela, apertou ESC ou apertou ENTER depois do Game Over.

Em seguida, se o jogo não estiver em Game Over, a lógica principal é atualizada. Isso inclui:

- Movimento do jogador.
- Verificação de coleta do cristal.
- Atualização do placar.
- Criação de inimigos.
- Movimento dos inimigos.
- Verificação de colisão com inimigos.

Depois da lógica, acontece o desenho da tela. O fundo é preenchido, a barra superior é desenhada, os textos aparecem e os objetos visuais são renderizados.

No final de cada repetição do loop, o comando abaixo atualiza a janela:

```python
pygame.display.flip()
```

Esse comando faz com que tudo que foi desenhado apareça de fato na tela.

## Frontend e backend do jogo

Mesmo sendo um jogo simples em um único arquivo, é possível separar a ideia de frontend e backend.

### Frontend

O frontend é a parte visual, ou seja, tudo que aparece para o jogador:

- Janela criada pelo Pygame.
- Cores usadas no fundo, no jogador, no cristal, nos inimigos e nos textos.
- Barra superior cinza.
- Placar exibido na tela.
- Jogador azul.
- Cristal amarelo.
- Inimigos vermelhos.
- Mensagens de Game Over e reinício.

No código, essa parte aparece principalmente nas chamadas de desenho, como `pygame.draw.rect()`, `pygame.draw.polygon()`, `pygame.draw.ellipse()` e `tela.blit()`.

### Backend / lógica

O backend, neste projeto, corresponde à lógica interna que controla o funcionamento do jogo:

- Variáveis como `placar`, `fim_de_jogo`, `rodando`, `velocidade_jogador` e `velocidade_inimigos`.
- Geração aleatória da posição do cristal.
- Criação dos inimigos.
- Movimento do jogador.
- Movimento dos inimigos.
- Colisões com `colliderect()`.
- Incremento do placar.
- Aumento da dificuldade.
- Reinício da partida.

Essa separação ajuda a entender que o jogo tem uma parte que mostra as coisas na tela e outra parte que decide o que está acontecendo por trás.

## Estrutura do código

O arquivo principal `caca_ao_cristal.py` está organizado da seguinte forma:

### Imports

O código importa as bibliotecas usadas no projeto:

- `pygame`: cria a janela, desenha elementos, controla eventos, fontes e colisão.
- `random`: gera posições e escolhas aleatórias.
- `sys`: finaliza o programa com `sys.exit()`.

### Constantes

As constantes definem valores fixos importantes, como:

- `LARGURA` e `ALTURA`: tamanho da janela.
- `FPS`: quadros por segundo.
- Cores RGB, como `PRETO`, `BRANCO`, `AZUL`, `AMARELO`, `VERMELHO` e `CINZA`.
- `TAMANHO_CRISTAL`: tamanho do cristal.

### Criação da tela

A tela é criada com:

```python
tela = pygame.display.set_mode((LARGURA, ALTURA))
```

O título da janela é definido com:

```python
pygame.display.set_caption("Caça ao Cristal")
```

### Jogador

O jogador é criado com `pygame.Rect` e possui uma velocidade inicial. Ele é desenhado como um retângulo azul com borda branca.

### Item

O item é o cristal amarelo. Ele é criado pela função `nova_posicao_cristal()` e desenhado pela função `desenhar_cristal()`.

### Inimigos

Os inimigos ficam dentro da lista `inimigos`. Cada inimigo possui um retângulo e velocidades nos eixos X e Y. Eles são criados pela função `criar_inimigo()`.

### Funções auxiliares

O código possui funções auxiliares para deixar o funcionamento mais organizado:

- `nova_posicao_cristal()`: gera uma nova posição aleatória para o cristal.
- `criar_inimigo()`: cria um inimigo em uma das bordas da tela.
- `atualizar_velocidade_inimigos()`: atualiza a velocidade dos inimigos já existentes.
- `desenhar_texto()`: renderiza e desenha textos na tela.
- `desenhar_cristal()`: desenha o cristal com formas geométricas.
- `reiniciar_jogo()`: reinicia as principais variáveis da partida.

### Loop principal

O loop principal controla eventos, atualiza a lógica do jogo, desenha os elementos na tela e atualiza a janela com `pygame.display.flip()`.

## Como alterar o jogo

Esta seção mostra onde mexer no arquivo `caca_ao_cristal.py` para personalizar o jogo. As mudanças devem ser feitas com cuidado, porque alguns valores influenciam diretamente a movimentação, o desenho e a colisão.

### Alterar o tamanho da janela

O tamanho da janela é controlado pelas constantes:

```python
LARGURA = 800
ALTURA = 600
```

Para deixar a tela maior, por exemplo, é possível alterar para:

```python
LARGURA = 1000
ALTURA = 700
```

Como o jogo usa `LARGURA` e `ALTURA` nos limites de movimento, na criação dos inimigos e na geração do cristal, a maior parte do código se adapta automaticamente ao novo tamanho.

### Alterar a velocidade do jogador

A velocidade inicial do jogador fica nesta variável:

```python
velocidade_jogador = 5
```

Se quiser que o jogador se mova mais rápido, aumente o valor:

```python
velocidade_jogador = 7
```

Se quiser deixar o jogo mais difícil, também é possível diminuir:

```python
velocidade_jogador = 3
```

Durante a partida, essa velocidade aumenta um pouco a cada 2 pontos:

```python
if placar % 2 == 0:
    velocidade_jogador += 0.2
```

Para aumentar mais rápido, troque `0.2` por um valor maior. Para não aumentar a velocidade do jogador, remova essa parte ou coloque `0`.

### Alterar a velocidade dos inimigos

A velocidade inicial dos inimigos é definida aqui:

```python
velocidade_inimigos = 3
```

Para inimigos mais rápidos desde o começo:

```python
velocidade_inimigos = 5
```

Para inimigos mais lentos:

```python
velocidade_inimigos = 2
```

Além disso, a dificuldade aumenta conforme o placar:

```python
velocidade_inimigos = 3 + placar * 0.15
```

O número `3` é a velocidade base, e `0.15` é o quanto a velocidade cresce a cada ponto. Para aumentar a dificuldade mais rápido, use um valor como `0.25`. Para deixar o aumento mais suave, use `0.05`.

### Alterar quando os inimigos aparecem

Os inimigos aparecem nesta condição:

```python
if placar == 1 or placar % 3 == 0:
    criar_inimigo()
```

Isso significa que o primeiro inimigo aparece no primeiro cristal coletado, e depois aparece um novo inimigo a cada 3 pontos.

Para criar inimigos a cada 2 pontos, altere para:

```python
if placar == 1 or placar % 2 == 0:
    criar_inimigo()
```

Para deixar o jogo mais fácil, criando inimigos a cada 5 pontos:

```python
if placar == 1 or placar % 5 == 0:
    criar_inimigo()
```

### Alterar as cores

As cores ficam definidas no início do código em formato RGB:

```python
PRETO = (18, 18, 26)
BRANCO = (245, 245, 245)
AZUL = (50, 140, 255)
AMARELO = (255, 215, 0)
VERMELHO = (230, 60, 60)
CINZA = (80, 80, 90)
```

Cada cor usa três números: vermelho, verde e azul. Cada número vai de `0` até `255`.

Exemplos:

- `(255, 0, 0)`: vermelho.
- `(0, 255, 0)`: verde.
- `(0, 0, 255)`: azul.
- `(255, 255, 255)`: branco.
- `(0, 0, 0)`: preto.

### Alterar a cor do jogador

O jogador é desenhado com a cor `AZUL`:

```python
pygame.draw.rect(tela, AZUL, jogador)
```

Para mudar a cor do boneco, existem duas opções. A primeira é mudar o valor da constante `AZUL`:

```python
AZUL = (0, 255, 0)
```

Nesse exemplo, o jogador ficaria verde.

A segunda opção é criar uma nova cor, por exemplo:

```python
ROXO = (140, 80, 255)
```

Depois, usar essa cor no desenho do jogador:

```python
pygame.draw.rect(tela, ROXO, jogador)
```

### Alterar a cor do cristal

O cristal é desenhado com `AMARELO` e contorno `BRANCO`:

```python
pygame.draw.polygon(tela, AMARELO, pontos)
pygame.draw.polygon(tela, BRANCO, pontos, 2)
```

Para mudar a cor principal do cristal, altere `AMARELO`. Para mudar a borda, altere `BRANCO` ou troque o nome da cor usada no segundo `pygame.draw.polygon()`.

### Alterar a cor dos inimigos

Os inimigos são desenhados com `VERMELHO` e contorno `BRANCO`:

```python
pygame.draw.ellipse(tela, VERMELHO, inimigo["retangulo"])
pygame.draw.ellipse(tela, BRANCO, inimigo["retangulo"], 2)
```

Para mudar a cor dos inimigos, altere o valor de `VERMELHO` ou troque `VERMELHO` por outra cor criada no início do código.

### Alterar o tamanho do jogador

O tamanho do jogador é definido na criação do `pygame.Rect`:

```python
jogador = pygame.Rect(380, 280, 40, 40)
```

Os dois últimos números são largura e altura. Para deixar o jogador maior:

```python
jogador = pygame.Rect(380, 280, 60, 60)
```

Para deixar menor:

```python
jogador = pygame.Rect(380, 280, 30, 30)
```

Importante: a mesma criação aparece também dentro da função `reiniciar_jogo()`. Se mudar o tamanho do jogador no início do código, é recomendado mudar também dentro dessa função, para o jogador continuar com o mesmo tamanho depois de reiniciar.

### Alterar o tamanho do cristal

O tamanho do cristal fica nesta constante:

```python
TAMANHO_CRISTAL = 26
```

Para deixar o cristal maior:

```python
TAMANHO_CRISTAL = 35
```

Para deixar menor:

```python
TAMANHO_CRISTAL = 18
```

Como o cristal também usa `pygame.Rect`, mudar esse valor altera tanto o tamanho visual quanto a área de colisão.

### Alterar o tamanho dos inimigos

O tamanho dos inimigos fica dentro da função `criar_inimigo()`:

```python
tamanho = 32
```

Para inimigos maiores:

```python
tamanho = 45
```

Para inimigos menores:

```python
tamanho = 24
```

Inimigos maiores tornam o jogo mais difícil, porque a área de colisão também aumenta.

### Alterar textos da tela

Os textos exibidos na tela ficam nas chamadas da função `desenhar_texto()`.

Texto da barra superior:

```python
desenhar_texto("Colete os cristais e evite os inimigos", fonte_pequena, BRANCO, 230, 20)
```

Texto de fim de jogo:

```python
desenhar_texto("FIM DE JOGO", fonte_media, VERMELHO, 300, 230)
```

Para mudar a mensagem, basta alterar o texto entre aspas.

### Alterar as fontes

As fontes são criadas no início do código:

```python
fonte_placar = pygame.font.SysFont("arial", 28, True)
fonte_media = pygame.font.SysFont("arial", 36, True)
fonte_pequena = pygame.font.SysFont("arial", 22)
```

O primeiro valor é o nome da fonte, o segundo é o tamanho, e o terceiro indica se o texto fica em negrito.

Exemplo para aumentar o placar:

```python
fonte_placar = pygame.font.SysFont("arial", 34, True)
```

### Alterar a taxa de quadros

O jogo usa:

```python
FPS = 60
```

Esse valor define quantas vezes por segundo o jogo tenta atualizar a tela. O padrão `60` deixa o movimento fluido. Em geral, não é necessário alterar esse valor.

### Alterar a posição inicial do jogador

A posição inicial do jogador fica nos dois primeiros números do `pygame.Rect`:

```python
jogador = pygame.Rect(380, 280, 40, 40)
```

Nesse caso, `380` é a posição no eixo X e `280` é a posição no eixo Y.

Para começar mais à esquerda:

```python
jogador = pygame.Rect(100, 280, 40, 40)
```

Para começar mais acima:

```python
jogador = pygame.Rect(380, 100, 40, 40)
```

Essa alteração também deve ser repetida dentro de `reiniciar_jogo()`, porque essa função recria o jogador quando a partida é reiniciada.

## Tecnologias utilizadas

- **Python**: linguagem principal do projeto.
- **Pygame**: biblioteca usada para criar a janela, desenhar elementos, controlar eventos, fontes e colisões.
- **Random**: módulo usado para gerar posições e escolhas aleatórias.
- **Sys**: módulo usado para encerrar o programa corretamente.

## Conclusão

O projeto **Caça ao Cristal** cumpre a proposta da atividade porque implementa um jogo em Pygame com item aleatório, coleta por colisão, placar e incremento de dificuldade.

O jogo possui um jogador controlado pelo teclado, um cristal que aparece em posições aleatórias, inimigos que surgem e se movimentam pela tela, detecção de colisões com `colliderect()` e uma tela de Game Over com possibilidade de reinício usando ENTER.

Assim, o código demonstra conceitos importantes de desenvolvimento de jogos 2D, como loop principal, eventos, desenho na tela, movimentação, colisão, placar e dificuldade progressiva.
