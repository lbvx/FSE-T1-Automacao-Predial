# Trabalho 1 (2022-2)

Trabalho 1 da disciplina de Fundamentos de Sistemas Embarcados (2022/2)

## 1. Objetivos

Este trabalho tem por objetivo a criação de um sistema distribuído de automação predial para monitoramento e acionamento de sensores e dispositivos de um prédio com múltiplas salas. O sistema deve ser desenvolvido para funcionar em um conjunto de placas Raspberry Pi com um servidor central responsável pelo controle e interface com o usuário e servidores distribuídos para leitura e acionamento dos dispositivos. Dentre os dispositivos envolvidos estão o monitoramento de temperatura e umidade, sensores de presença, sensores de fumaça, sensores de contagem de pessoas, sensores de abertura e fechamento de portas e janelas, acionamento de lâmpadas, aparelhos de ar-condicionado, alarme e aspersores de água em caso de incêndio.

A Figura 1 mostra a arquitetura do sistema.

![Figura](/figuras/arquitetura_trabalho_1.png)

<!-- Na Figura 2 é possível ver a distribuição dos sensores no prédio.

![Figura](/figuras/planta_baixa_predio.png) -->

## 2. Componentes do Sistema

Para simplificar a implementação e logística de testes do trabalho, a quantidade de salas do prédio e o número de sensores foi reduzido a um mínimo representativo. Estarão disponíveis para teste 4 placas Raspberry Pi para executar os Servidores Distribuídos e o Servidor Central. A configuração do sistema está detalhada abaixo:

O sistema do Servidor Central será composto por:
1. 01 placa Raspberry Pi 4;

O sistema do Servidor Distribuído será composto por:
1. 01 Placa Raspberry Pi 4;
2. 01 Sensore de Temperatura (DHT22)
3. 01 Circuito de potência com 5 relés para acionametno de Lâmpadas / Aparelhos de Ar-Condicionado, etc.;
4. 02 Sensores de fechamento de portas/janelas;
5. 01 Sensore de presença;
6. 01 Sensore de fumaça;
7. 02 Sensores de Contagem de Pessoas (Cada pessoa que passa aciona o sinal do sensor por aprox. 200 ms, são 2 sensores por sala);
8. 01 Alarme (Buzzer).

## 3. Conexões entre os módulos do sistema

1. Os servidores distribuídos deverão se comunicar com o servidor central através do Protocolo TCP/IP (O formato das mensagens ficam à cargo do aluno. A sugestão é o uso do formato JSON);
2. Cada instância do servidor distribuído (uma por sala) deve rodar em um processo paralelo em portas distintas); 
3. O sistema de alarme do servidor Central deverá ser acionado indicando na tela do sistema que o mesmo está em operação;
4. O sensores de temperatura / umidade (DHT22) estão conectados diretamete à porta GPIO e da placa Raspberry Pi do Servidor Distribuído (o número do pino está detalhado na tabela);
5. As lâmpadas, aparelhos de ar-condicionado e os diversos sensores estão ligados aos pinos da GPIO conforme a Tabela 1.

| Item                                              | Sigla | GPIO | Direção |
|---------------------------------------------------|:------:|:----:|:-------:|
| ***Configuração 01 - Sala 01 e Sala 03***         |        |      |         |
| Lâmpada 01 da Sala                                | L_01   |  18  | Saída   |
| Lâmpada 02 da Sala                                | L_02   |  23  | Saída   |
| Ar-Condicionado                                   | AC     |  24  | Saída   |  
| Projetor Multimídia                               | PR     |  25  | Saída   |  
| Alarme (sirene / buzzer)                                   | AL_BZ  |  08  | Saída   |  
| Sensor de Presença                                | SPres  |  07  | Entrada |
| Sensor de Fumaça                                  | SFum   |  01  | Entrada |
| Sensor de Janela                                  | SJan   |  12  | Entrada |
| Sensor de Porta                                   | SPor   |  16  | Entrada |
| Sensor de Contagem de Pessoas Entrada             | SC_IN  |  20  | Entrada |
| Sensor de Contagem de Pessoas Saída               | SC_OUT |  21  | Entrada |
| Sensor de Temperatura / Umidade DHT22             | DHT22  |  04  | 1-Wire  |  
| ***Configuração 02 - Sala 02 e Sala 04***         |        |      |         |
| Lâmpada 01 da Sala                                | L_01   |  26  | Saída   |
| Lâmpada 02 da Sala                                | L_02   |  19  | Saída   |
| Ar-Condicionado                                   | AC     |  13  | Saída   |  
| Projetor Multimídia                               | PR     |  06  | Saída   |  
| Alarme (sirene / buzzer)                                   | AL_BZ  |  05  | Saída   |  
| Sensor de Presença                                | SPres  |  00  | Entrada |
| Sensor de Fumaça                                  | SFum   |  11  | Entrada |
| Sensor de Janela                                  | SJan   |  09  | Entrada |
| Sensor de Porta                                   | SPor   |  10  | Entrada |
| Sensor de Contagem de Pessoas Entrada             | SC_IN  |  22  | Entrada |
| Sensor de Contagem de Pessoas Saída               | SC_OUT |  27  | Entrada |
| Sensor de Temperatura / Umidade DHT22             | DHT22  |  18  | 1-Wire  | 

## 4. Requisitos

Os sistema de controle possui os seguintes requisitos:

### Servidor Central

O código do Servidor Central pode ser desenvolvido em **Python**, **C** ou **C++**. Em qualquer uma das linguagens devem haver instruções explicitas de como instalar e rodar. Para C/C++ basta o Makefile e incluir todas as dependências no próprio projeto.

O servidor central tem as seguintes responsabilidades:  
1. Manter conexão com o servidor distribuído (TCP/IP);  
2. Prover uma **interface** que mantenham atualizadas as seguintes informações:  
    a. **Estado das entradas** (Sensores);  
    b. **Estado das Saídas** (lâmpadas, aparelhos de ar, etc.);   
    c. **Valor da temperatura e umidade** de cada sala a cada 2 segundos;  
    d. **Contador de Ocupação** (Número de Pessoas) presentes no prédio como um todo e a ocupação individual de cada sala;  
3. Prover **mecanismo na interface** para:  
    a. Acionar manualmente lâmpadas, aparelhos de ar-condicionado e projetores das salas;   
    b. **Acionamento do sistema de alarme** que, quando estiver ligado, deve tocar um som de alerta (acionar a sirene/buzzer) ao detectar presenças ou abertura de portas/janelas;  
    c. **Acionamento de alarme de incêncio** que, ao detectar presença de fumaça a qualquer momento deve soar o alarme;
4. Manter **log** (em arqvuio CSV) dos comandos acionados pelos usuários e do acionamento dos alarmes com data e hora e cada evento;  

### Servidores Distribuídos

O código do Servidor Distribuído deve ser desenvolvido em **C**/**C++** ou **Python**;  

Os servidores distribuídos tem as seguintes responsabilidades:  
1. Manter os valores de **temperatura e umidade** atualizados a cada 2 segundos (Sendo requisitado pelo servidor central periodicamente ou enviado via mensagem *push*);  
2. Acionar **Lâmpadas, aparelhos de Ar-Condicionado e projetores** (mantendo informação sobre seu estado) conforme comandos do Servidor Central e retornando uma mensagem de confirmação para o mesmo sobre o sucesso ou não do acionamento;  
3. Manter o estado dos **sensores de presença e abertura de portas/janelas** informando ao servidor central imediatamente (*mensagem push*) quando detectar o acionamento de qualquer um deles;  
4. Manter o estado dos **sensores de fumaça** informando ao servidor central imediatamente (*mensagem push*) quando detectar o acionamento de qualquer um deles;  
5. Efetuar a contagem de pessoas entrando e saindo da sala para controle de ocupação;
6. Cada instância dos servidores distribuídos deve ser iniciada conforme o arquivo descrição JSON disponível neste repositório (Somente a porta local de cada servidor deve ser modificada no arquivo para cada aluno conforme a distribuição de portas disponibilizada para a turma).

### Geral

1. Os códigos em C/C++ devem possuir Makefile para compilação;
2. Cada serviço (programa) deve poder ser iniciado independente dos demais e ficar aguardando o acionamento dos demais;
3. Deverá haver um arquivo README no repositório descrevento o modo de instalação/execução e o modo de uso do programa.

## 5. Detalhes de Implementação

1. Os sensores de contagem de pessoas serão acionados por aprox. 200 ms (podendo variar em aprox. 100 ms para mais ou para menos). Neste caso, o sistema deverá detectar e contar corretamente somente uma entrada ou saída.
2. O programa não poderá usar 100% da CPU em nenhum caso. Todas as threads/processos deverão funcionar com algum tipo de temporizador ou sleep para desocupar o processador em algum momento ou através de chamadas blocantes.
3. O programa do Servidor Distribuído deve ser genérico para poder ser associado a qualquer sala do prédio e inicializado à partir de um arquivo de configuração (JSON), disponível neste repositório.
4. Os **sensores de presença** nos corredores terão duas funções:  
   a. Caso o **sistema de alarme** esteja **ligado**, deverão acionar a sirene/buzzer;  
   b. Caso o **sistema de alarme** esteja **desligado**, deverão **acender as duas lâmpadas da sala por 15 segundos** e depois apagar;
5. Deve haver um meio de **ligar** _**todas as lâmpadas do prédio ou por sala**_. E de **desligar** **_todas as cargas do prédio ou por sala_** (Lampadas, projetores e aparelhos de Ar-Condicionado).
6. Ao acionar o sistema de alarme, deve haver uma verificação se o sensores que ativam o alarme estão ligados. Neste caso, o sistema deve alertar o usuário e não permitir o acionamento do sistema alarme enquanto todos os itens que o acionam estejam desativados.

## 6. Critérios de Avaliação

A avaliação será realizada seguindo os seguintes critérios:

|   ITEM    |   DETALHE  |   VALOR   |
|-----------|------------|:---------:|
|**Servidor Central**    |       |       |
|**Interface (Monitoramento)**  |   Interface gráfica (via terminal, web, etc) apresentando o estado de cada dispositivo (entradas e saídas), a temperatura, umidade e o número de pessoas ocupando o prédio sendo atualizada periodicamente.  |   1,0   |
|**Interface (Acionamento de Dispositivos)** |   Mecanismo para acionamento de lâmpadas, aparelhos de ar-condicionado e projetores individualmente ou em grupos. |   1,0   |
|**Acionamento do Alarme**   |   Mecanismo de ligar/desligar alarme e acionamento do alarme de acordo com o estado dos sensores com alerta no acionamento. |   0,5   |
|**Alarme de Incêndio**   |   Implementação da rotina de acionamento do alarme de incêncio. |   0,5   |
|**Log (CSV)**   |   Geração de Log em arquivo CSV.  |   0,5 |
|**Servidores Distribuídos**    |       |       |
|**Inicialização (Arquivo de Configuração)**    |   Correta inicialização do serviço à partir do arquivo de configuração JSON.  |   0,5   |
|**Leitura de Temperatura / Umidade**    |   Leitura, armazenamento e envio dos valores de temperatura / umidade por sala.  |   0,7   |
|**Acionamento de Dispositivos** |   Correto acionamento de lâmpadas, aparelhos de ar-condicionado e aspersor pelo comando do Servidor Central.    |   0,7   |
|**Estado dos Sensores** |   Correta leitura e envio (*mensagem push*) para o Servidor Central um alerta pelo acionamento dos sensores de presença / abertura de portas/janelas e sensor de fumaça.   |   0,8  |
|**Contagem de pessoas** |   Correta leitura dos sensores de contagem de pessoas (Por sala e Total).   |   0,8  |
|**Geral**    |       |       |
|**Comunicação TCP/IP**  |   Correta implementação de comunicação entre os servidores usando o protocolo TCP/IP, incluindo as mensagens do tipo *push*. |   1,5   |
|**Qualidade do Código / Execução** |   Utilização de boas práticas como o uso de bons nomes, modularização e organização em geral, bom desempenho da aplicação sem muito uso da CPU. |  1,5 |
|**Pontuação Extra** |   Qualidade e usabilidade acima da média. |   0,5   |

## 7. Referências

### Bibliotecas em Python - GPIO

- gpiozero (https://gpiozero.readthedocs.io)
- RPi.GPIO (https://pypi.org/project/RPi.GPIO/)

A documentação da RPi.GPIO se encontra em
https://sourceforge.net/p/raspberry-gpio-python/wiki/Examples/

### Bibliotecas em C/C++ GPIO

- WiringPi (http://wiringpi.com/) - Descontinuada
- BCM2835 (http://www.airspayce.com/mikem/bcm2835/)
- PiGPIO (http://abyz.me.uk/rpi/pigpio/index.html)
- sysfs (https://elinux.org/RPi_GPIO_Code_Samples)

### Lista de Exemplos em diversas linguagens - GPIO 

Há um compilado de exemplos de acesso à GPIO em várias linguages de programação como C, C#, Ruby, Perl, Python, Java e Shell (https://elinux.org/RPi_GPIO_Code_Samples).

### Sensor de Temperatura e Umidade (DHT22)

- Python (https://learn.adafruit.com/dht-humidity-sensing-on-raspberry-pi-with-gdocs-logging/python-setup)
- C/C++ - BCM2835 (https://gist.github.com/rm-hull/5862591)
- C/C++ - WirinfPi - (https://github.com/Qengineering/DHT22-Raspberry-Pi)
- Exemplo de uso do DHT22 em C - WiringPi (https://github.com/nebulx29/dht22)
