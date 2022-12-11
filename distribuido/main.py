from Sala import Sala, SalaThread
import sys
from time import sleep

def main():
    config = sys.argv[1]
    st = SalaThread(Sala(config))
    st.start()
    st.sala.sistemaAlarme = True

    while True:
        sleep(2)
        print(f'Pessoas: {st.sala.pessoasQtd}')
        if not (st.sala.temp is None or st.sala.umid is None):
            print(f'T = {st.sala.temp:.1f}°')
            print(f'U = {st.sala.umid:.1f}%')
        else:
            print('Nao foi possivel ler temp/umid')

if __name__ == '__main__':
    main()
