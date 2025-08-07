<img width=100% src="https://capsule-render.vercel.app/api?type=waving&color=4C89F8&height=120&section=header"/>

<img width="1584" height="396" alt="LinkedIn cover - 29" src="https://github.com/user-attachments/assets/d1c05723-0bec-4ce7-8dee-1ef8c95ebf3e" />

<br>
<br>

# Ultimate Tic-Tac-Toe

Um jogo de Ultimate Tic-Tac-Toe (Jogo da Velha Infinito) desenvolvido em Pygame, com múltiplos modos de jogo, incluindo um modo contra a CPU com diferentes níveis de dificuldade, e uma interface de usuário redesenhada para uma melhor experiência.
<br>
<br>
<img width="1205" height="735" alt="image" src="https://github.com/user-attachments/assets/43a0f06c-6940-48f1-996b-c49e3204cd40" />
<img width="1210" height="743" alt="image" src="https://github.com/user-attachments/assets/6f8a6beb-0e9c-4633-ac31-f43c608b280a" />
<br>
<br>
## ✨ Funcionalidades

### 🎮 Modos de Jogo
- **Humano vs Humano**: O modo clássico para dois jogadores.
- **Humano vs CPU**: Desafie o computador em três níveis de dificuldade:
  - **Fácil**: A CPU faz jogadas aleatórias.
  - **Médio**: A CPU utiliza estratégias básicas para tentar vencer e bloquear o jogador.
  - **Difícil**: A CPU emprega o algoritmo Minimax com poda alfa-beta para buscar a melhor jogada possível, proporcionando um desafio estratégico.

### 🎨 Interface de Usuário (UI) Aprimorada
- **Layout Largo**: A tela do jogo foi expandida para 1200x700 pixels, oferecendo mais espaço e uma visualização clara.
- **Tabuleiro Centralizado**: O tabuleiro principal de 600x600 pixels fica no centro da tela, garantindo foco total no jogo.
- **Barras Laterais Organizadas**: Todos os controles e informações foram movidos para as laterais da tela:
  - **Lateral Esquerda**: Controles de jogo (Reiniciar, Novo Jogo, Limpar Estatísticas) e exibição detalhada das estatísticas.
  - **Lateral Direita**: Seleção de modos de jogo (Humano, CPU Fácil, Médio, Difícil), indicação do modo atual e uma legenda de cores para os símbolos.
- **Espaçamento Otimizado**: Espaçamento de 50px entre a barra lateral direita e a borda da tela, proporcionando um visual mais limpo e menos "colado".

### 🌈 Sistema de Cores Consistente
- **Jogador X**: Sempre representado pela cor **Vermelha** (`#DC143C`).
- **Jogador O**: Sempre representado pela cor **Azul** (`#1E90FF`), seja um jogador humano ou a CPU.
- **Cores da CPU**: Embora o símbolo 'O' seja sempre azul, as mensagens de status da CPU e os indicadores de vitória ainda podem usar cores específicas (Laranja para Fácil/Médio, Vermelho-Laranja para Difícil) para feedback visual.

### 📊 Estatísticas do Jogo
- As vitórias de X, O e empates são rastreadas e salvas automaticamente em um arquivo `ultimate_tictactoe_stats.json`.
- As estatísticas são exibidas na barra lateral esquerda.

### ⚡ Experiência de Jogo
- **Delay da CPU**: A CPU espera 1 segundo antes de fazer sua jogada em todos os níveis de dificuldade, proporcionando uma experiência mais natural.
- **Feedback Visual**: Efeitos de hover nas células disponíveis e mensagens de status claras.

## 🚀 Como Rodar o Jogo

### Pré-requisitos
Certifique-se de ter o Python 3 e a biblioteca Pygame instalados. Se não tiver, você pode instalá-los usando pip:

```bash
pip install pygame
```

### Execução
1. Baixe o arquivo `python ultimate_tic_tac_toe.py  ` para o seu computador.
2. Abra um terminal ou prompt de comando na pasta onde você salvou o arquivo.
3. Execute o jogo com o seguinte comando:

```bash
python ultimate_tic_tac_toe.py  
```

## 🕹️ Controles

### Mouse
- **Clique**: Use o mouse para selecionar as células no tabuleiro.
- **Hover**: Passe o mouse sobre as células para ver o efeito de destaque.
- **Botões**: Clique nos botões nas laterais para controlar o jogo e mudar os modos.

### Atalhos do Teclado
- `R` ou `N`: Reiniciar o jogo.
- `1`: Mudar para o modo Humano vs Humano.
- `2`: Mudar para o modo Humano vs CPU (Fácil).
- `3`: Mudar para o modo Humano vs CPU (Médio).
- `4`: Mudar para o modo Humano vs CPU (Difícil).

## 🧠 Regras do Ultimate Tic-Tac-Toe

O Ultimate Tic-Tac-Toe é uma versão mais complexa do jogo da velha tradicional. Ele é jogado em um tabuleiro 3x3 de tabuleiros de Tic-Tac-Toe menores. As regras são as seguintes:

1. **Jogada Inicial**: O primeiro jogador pode jogar em qualquer célula de qualquer tabuleiro pequeno.
2. **Próxima Jogada**: A célula onde o jogador anterior jogou determina em qual tabuleiro pequeno o próximo jogador deve jogar. Por exemplo, se o jogador X jogar na célula superior direita de um tabuleiro pequeno, o jogador O deve jogar no tabuleiro pequeno que corresponde à posição superior direita do tabuleiro principal.
3. **Tabuleiros Vencidos**: Se um jogador vencer um tabuleiro pequeno, ele marca essa posição no tabuleiro principal.
4. **Tabuleiros Cheios/Empatados**: Se um tabuleiro pequeno ficar cheio sem um vencedor, ele é considerado um empate e marca essa posição no tabuleiro principal como um empate.
5. **Jogada Livre**: Se a jogada de um jogador o levar a um tabuleiro pequeno que já foi vencido ou empatado, ele pode jogar em qualquer tabuleiro pequeno que ainda esteja ativo (não vencido nem empatado).
6. **Vitória no Jogo Principal**: O jogo é vencido quando um jogador consegue três de seus símbolos em linha (horizontal, vertical ou diagonal) no tabuleiro principal, assim como no Tic-Tac-Toe tradicional.
7. **Empate Geral**: Se o tabuleiro principal ficar cheio sem um vencedor, o jogo é um empate.

## 📂 Estrutura do Projeto

- `ultimate_tictactoe_wide_layout.py`: O arquivo principal do jogo, contendo toda a lógica, UI e implementação da CPU.
- `ultimate_tictactoe_stats.json`: Arquivo JSON onde as estatísticas do jogo são salvas automaticamente.

## 🤝 Contribuição

Sinta-se à vontade para contribuir com melhorias, correções de bugs ou novas funcionalidades. Abra uma issue ou envie um Pull Request no repositório.

## 📄 Licença

Este projeto está licenciado sob a [SUA LICENÇA AQUI, ex: MIT License].

---

 <br>

 <br>
<div align="center">
  <img src="https://github.com/user-attachments/assets/ed7208b8-6bdc-4c82-98aa-8c8cb9c1428f" height="150"/>
</div>

<img width=100% src="https://capsule-render.vercel.app/api?type=waving&color=4C89F8&height=120&section=footer"/>

