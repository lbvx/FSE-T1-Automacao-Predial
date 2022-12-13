from Sala import Sala, SalaThread
from Conexao import ConexaoThread
import sys
from time import sleep
import socket

def main():
    config = sys.argv[1]
    st = SalaThread(config)
    st.start()
    # # st.sala.sistemaAlarme = True

    ct = ConexaoThread(st)
    ct.start()

    sockDistr = socket.create_connection(('127.0.0.1', 10200))

    # while True:
    #     print(f'Pessoas: {st.sala.pessoasQtd}')
    #     if not (st.sala.temp is None or st.sala.umid is None):
    #         print(f'T = {st.sala.temp:.1f}°')
    #         print(f'U = {st.sala.umid:.1f}%')
    #     else:
    #         print('Nao foi possivel ler temp/umid')

    #     print('ct:', ct.is_alive())
    #     sleep(2)

    ct.join()
    print('so long')

if __name__ == '__main__':
    main()
