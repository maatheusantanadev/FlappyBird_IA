

---

# 🐦 Flappy Bird com IA (NEAT)

Este projeto é uma implementação do jogo **Flappy Bird** utilizando **Python + Pygame**, com integração da biblioteca **NEAT (NeuroEvolution of Augmenting Topologies)** para treinar uma **IA** capaz de jogar sozinha.

---

## 📌 Funcionalidades

* Jogo clássico do Flappy Bird feito em Pygame.
* Controle manual (pressionando **espaço** para pular).
* Estrutura preparada para integração com NEAT e evolução de agentes.
* Colisões precisas usando **máscaras** (pixel perfect collision).
* Sistema de pontuação.
* Configuração do NEAT personalizável (`config.txt`).

---

## 🛠 Tecnologias

* **Python 3.8+**
* **Pygame** para renderização e controle do jogo.
* **NEAT-Python** para evolução de redes neurais.
* **Os / Random** para manipulação de arquivos e gerar aleatoriedade.

---

## ⚙️ Configuração NEAT

O arquivo de configuração (`config.txt`) define parâmetros como:

* **Tamanho da população** (`pop_size`)
* **Taxa de mutação** para pesos e bias
* **Função de ativação** (`tanh`)
* **Critério de seleção e elitismo**
* **Número de entradas e saídas da rede neural**

> Você pode ajustar os valores para aumentar a performance ou dificuldade da IA.

---

## 🚀 Como Executar

1. **Clone o repositório**

```bash
git clone https://github.com/maatheusantanadev/FlappyBird_IA
cd FlappyBird_IA
```

2. **Instale as dependências**

```bash
pip install pygame neat-python
```

3. **Execute o jogo**

```bash
python main.py
```

---

## 🎮 Controles

* **Barra de espaço** → Faz o pássaro pular.
* **Fechar janela** → Sai do jogo.

---

## 🧠 Sobre a IA

O NEAT cria uma população inicial de redes neurais com conexões aleatórias.
Durante o treinamento:

* Cada rede controla um pássaro.
* A pontuação (fitness) aumenta conforme o pássaro sobrevive e passa canos.
* As melhores redes se reproduzem e mutam, melhorando o desempenho ao longo das gerações.

---

## 📜 Licença

Este projeto é de uso livre para estudos.
Sinta-se à vontade para modificar e compartilhar.

---

