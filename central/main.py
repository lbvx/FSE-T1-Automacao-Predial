import sys
from Conexao import ConexaoCentral
from Interface import Interface

def main(argv):
    end = argv[1], int(argv[2])
    ct = ConexaoCentral(end)
    it = Interface(ct)
    ct.start()
    it.start()
    it.join()

if __name__ == '__main__':
    main(sys.argv)
