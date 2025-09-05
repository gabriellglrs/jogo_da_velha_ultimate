<img width=100% src="https://capsule-render.vercel.app/api?type=waving&color=4C89F8&height=120&section=header"/>

<img width="1584" height="396" alt="LinkedIn cover - 29" src="https://github.com/user-attachments/assets/d1c05723-0bec-4ce7-8dee-1ef8c95ebf3e" />

<br>
<br>

# Ultimate Tic-Tac-Toe: Edição Aprimorada

Este projeto apresenta uma versão significativamente aprimorada do clássico jogo Ultimate Tic-Tac-Toe (também conhecido como Jogo da Velha Infinito), desenvolvido em Pygame. Esta edição foi redesenhada para oferecer uma experiência de usuário superior, com uma interface visualmente mais rica, modos de jogo expandidos e uma inteligência artificial da CPU mais sofisticada, capaz de desafiar jogadores em diversos níveis de habilidade.

<br>

<img width="1355" height="767" alt="image" src="https://github.com/user-attachments/assets/0af44358-5c17-4836-bfab-3df335b0bdb1" />
<img width="1919" height="1079" alt="image" src="https://github.com/user-attachments/assets/a8e953a5-d070-4cb0-8a7d-9bfbcc5e9c4d" />
<img width="1359" height="767" alt="image" src="https://github.com/user-attachments/assets/ce9596c3-da84-4e68-8e4b-3ad4cf9fe67c" />
<img width="1359" height="767" alt="image" src="https://github.com/user-attachments/assets/12191a66-759d-4bb0-8dda-d0d9ccdccafb" />

<br>

## ✨ Funcionalidades Destacadas

### 🎮 Modos de Jogo Versáteis

O jogo oferece múltiplos modos para garantir diversão e desafio para todos os tipos de jogadores:

*   **Humano vs Humano:** O modo tradicional para dois jogadores, perfeito para duelos locais.
*   **Humano vs CPU:** Desafie a inteligência artificial em três níveis de dificuldade distintos:
    *   **Fácil:** A CPU realiza jogadas aleatórias, ideal para iniciantes ou para uma partida relaxante.
    *   **Médio:** A CPU emprega estratégias básicas, focando em vencer e bloquear o jogador em cenários óbvios, proporcionando um desafio intermediário.
    *   **Difícil:** A CPU utiliza o avançado algoritmo **Minimax com poda alfa-beta** para calcular a melhor jogada possível. Este nível oferece um desafio estratégico robusto, exigindo que o jogador pense várias jogadas à frente.

### 🎨 Interface de Usuário (UI) Reimaginada

A interface foi completamente redesenhada para otimizar a experiência visual e a usabilidade:

*   **Experiência em Tela Cheia e Escalável:** O jogo agora é executado em **tela cheia (1920x1080)** e é **escalável**, adaptando-se a diferentes resoluções de monitor. Isso proporciona uma imersão completa e aproveita ao máximo o espaço disponível.
*   **Layout Amplo e Organizado:** A tela foi expandida para acomodar um design mais limpo e funcional. O tabuleiro principal, agora com **800x800 pixels**, é centralizado para garantir o foco total na jogabilidade.
*   **Barras Laterais Intuitivas:** Todos os controles e informações cruciais foram realocados para barras laterais dedicadas, eliminando distrações do centro da tela:
    *   **Lateral Esquerda:** Contém os controles de jogo essenciais (Reiniciar, Novo Jogo, Limpar Estatísticas) e uma exibição detalhada das estatísticas de vitórias e empates.
    *   **Lateral Direita:** Permite a seleção rápida dos modos de jogo (Humano, CPU Fácil, Médio, Difícil), indica o modo de jogo atual e oferece uma legenda de cores para os símbolos dos jogadores.
*   **Estética Refinada:** O espaçamento otimizado entre os elementos da UI e as bordas da tela, juntamente com uma **paleta de cores moderna e consistente**, contribui para um visual mais profissional e agradável. Efeitos de hover nas células disponíveis fornecem feedback visual instantâneo.

### 🌈 Sistema de Cores Consistente e Intuitivo

Para facilitar a identificação e melhorar a clareza visual, um sistema de cores padronizado foi implementado:

*   **Jogador X:** Sempre representado pela cor **Vermelha** (`#DC143C`).
*   **Jogador O:** Sempre representado pela cor **Azul** (`#1E90FF`), independentemente de ser um jogador humano ou a CPU.
*   **Cores da CPU:** Embora o símbolo 'O' seja azul, mensagens de status e indicadores de vitória da CPU podem usar cores específicas (Laranja para Fácil/Médio, Vermelho-Laranja para Difícil) para fornecer feedback visual adicional sobre o nível de dificuldade.

### 📊 Estatísticas do Jogo Persistentes

As estatísticas de vitórias (para X e O) e empates são rastreadas automaticamente e salvas em um arquivo `ultimate_tictactoe_stats.json`. Essas estatísticas são exibidas em tempo real na barra lateral esquerda, permitindo que os jogadores acompanhem seu desempenho ao longo do tempo.

### ⚡ Experiência de Jogo Aprimorada

*   **Delay da CPU:** A CPU introduz um pequeno atraso (1 segundo) antes de fazer sua jogada em todos os níveis de dificuldade, simulando uma experiência de jogo mais natural e menos abrupta.
*   **Feedback Visual:** Além dos efeitos de hover, mensagens de status claras são exibidas para guiar o jogador durante a partida.

## 🚀 Como Rodar o Jogo

### Pré-requisitos

Certifique-se de ter o **Python 3** e a biblioteca **Pygame** instalados em seu sistema. Caso não os tenha, você pode instalá-los facilmente via pip:

```bash
pip install pygame
```

### Execução

1.  Baixe o arquivo `ultimate_tic_tac_toe.py` (ou o nome do arquivo principal do código) para o seu computador.
2.  Abra um terminal ou prompt de comando na pasta onde você salvou o arquivo.
3.  Execute o jogo com o seguinte comando:

    ```bash
    python ultimate_tic_tac_toe.py
    ```

## 🕹️ Controles

### Mouse

*   **Clique:** Use o mouse para selecionar as células no tabuleiro e interagir com os botões da interface.
*   **Hover:** Passe o mouse sobre as células disponíveis para visualizar um efeito de destaque.

### Atalhos do Teclado

*   `R` ou `N`: Reiniciar o jogo.
*   `1`: Mudar para o modo Humano vs Humano.
*   `2`: Mudar para o modo Humano vs CPU (Fácil).
*   `3`: Mudar para o modo Humano vs CPU (Médio).
*   `4`: Mudar para o modo Humano vs CPU (Difícil).

## 🧠 Regras do Ultimate Tic-Tac-Toe

O Ultimate Tic-Tac-Toe é uma variação complexa e estratégica do jogo da velha tradicional. Ele é jogado em um tabuleiro 3x3 de tabuleiros de Tic-Tac-Toe menores. As regras são as seguintes:

1.  **Jogada Inicial:** O primeiro jogador pode fazer sua jogada em qualquer célula de qualquer um dos nove tabuleiros pequenos.
2.  **Próxima Jogada:** A posição da célula onde o jogador anterior jogou determina em qual tabuleiro pequeno o próximo jogador deve jogar. Por exemplo, se o Jogador X jogar na célula superior direita de um tabuleiro pequeno, o Jogador O deve fazer sua próxima jogada no tabuleiro pequeno que corresponde à posição superior direita do tabuleiro principal.
3.  **Tabuleiros Vencidos:** Quando um jogador consegue três de seus símbolos em linha (horizontal, vertical ou diagonal) em um tabuleiro pequeno, ele 


marca essa posição no tabuleiro principal com seu símbolo.
4.  **Tabuleiros Cheios/Empatados:** Se um tabuleiro pequeno ficar completamente preenchido sem um vencedor, ele é considerado um empate e marca a posição correspondente no tabuleiro principal como um empate.
5.  **Jogada Livre:** Se a jogada de um jogador o direcionar para um tabuleiro pequeno que já foi vencido ou empatado, ele tem a liberdade de jogar em qualquer tabuleiro pequeno que ainda esteja ativo (ou seja, que não tenha sido vencido nem empatado).
6.  **Vitória no Jogo Principal:** O jogo é vencido quando um jogador consegue alinhar três de seus símbolos (horizontal, vertical ou diagonal) no tabuleiro principal, seguindo as mesmas regras do Tic-Tac-Toe tradicional.
7.  **Empate Geral:** Se o tabuleiro principal ficar completamente preenchido sem que nenhum jogador consiga uma vitória, o jogo é declarado um empate.

## 📂 Estrutura do Projeto

O projeto é composto pelos seguintes arquivos:

*   `ultimate_tic_tac_toe.py`: O arquivo principal do jogo, contendo toda a lógica de jogo, a interface de usuário (UI) e a implementação da inteligência artificial da CPU.
*   `ultimate_tictactoe_stats.json`: Um arquivo JSON onde as estatísticas de vitórias e empates do jogo são salvas e carregadas automaticamente, garantindo a persistência dos dados entre as sessões.

## 🤝 Contribuição

Contribuições são muito bem-vindas! Se você tiver ideias para melhorias, encontrar bugs ou quiser adicionar novas funcionalidades, sinta-se à vontade para:

*   Abrir uma `issue` no repositório do projeto para relatar problemas ou sugerir novas funcionalidades.
*   Enviar um `Pull Request` com suas alterações. Certifique-se de que seu código siga as boas práticas e que os testes, se houver, sejam aprovados.

Seu feedback e colaboração são essenciais para tornar este jogo ainda melhor!



---

 <br>

 <br>
<div align="center">
  <img src="https://github.com/user-attachments/assets/ed7208b8-6bdc-4c82-98aa-8c8cb9c1428f" height="150"/>
</div>

<img width=100% src="https://capsule-render.vercel.app/api?type=waving&color=4C89F8&height=120&section=footer"/>

