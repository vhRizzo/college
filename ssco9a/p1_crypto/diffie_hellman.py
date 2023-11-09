P = 337
G = 15


def calcula_pub(kpr):
    return G ** (kpr) % (P)


def calcula_key(other_kpu, kpr):
    return (other_kpu) ** kpr % P
