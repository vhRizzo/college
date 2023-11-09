P = 337
G = 17


def calcula_pub(kpr):
    return G ** (kpr) % (P)


def calcula_key(other_kpu, kpr):
    return (other_kpu) ** kpr % P
