from Sala import Sala, SalaThread
from Conexao import ConexaoDistribuido
import sys

def main(argv):
    config = argv[1]
    sala = Sala(config)
    st = SalaThread(sala)
    st.start()
    # sala.sistemaAlarme = True

    ct = ConexaoDistribuido(sala)
    ct.start()

    # while True:
    #     print(f'Pessoas: {st.sala.pessoasQtd}')
    #     # if not (st.sala.temp is None or st.sala.umid is None):
    #     #     print(f'T = {st.sala.temp:.1f}°')
    #     #     print(f'U = {st.sala.umid:.1f}%')
    #     # else:
    #     #     print('Nao foi possivel ler temp/umid')

    #     sleep(2)

    try:
        st.join()
    except KeyboardInterrupt:
        ct.encerra()
        st.encerra()

if __name__ == '__main__':
    main(sys.argv)
