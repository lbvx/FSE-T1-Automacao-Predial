# Automação predial

## Central

Para rodar:

```sh
python3 main.py <ip> <porta>
```

### Como usar:

Os comandos disponíveis são

```
menu - exibe esse menu

salas - exibe salas conectadas

pessoas - exibe quantidade de pessoas no prédio

<nome da sala> - exibe estados de uma sala

ligar <sala> <output> - liga saídas de uma sala

desligar <sala> <output> - desliga saídas de uma sala
```

Os códigos das saídas estão de acordo com a seguinte tabela:

| Item                    | Sigla  |
|-------------------------|:------:|
| Lâmpada 01              | L_01   |
| Lâmpada 02              | L_02   |
| Ar-Condicionado         | AC     |  
| Projetor Multimídia     | PR     |  
| Alarme/Buzzer           | AL_BZ  |  

Para ligar/desligar uma porta em todas as salas ao mesmo tempo, utilize "tudo" no campo \<sala>.

Para ligar/desligar todas as portas de uma sala, utlize "tudo" no campo \<outputs>.

## Distribuído

Para rodar:

```sh
python3 main.py <config>
```

Onde \<config> é um arquivo JSON de configuração da placa, no mesmo padrão dos exemplos no repositório.
