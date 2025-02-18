import random
from sympy import isprime


def importar_mensagem():
    try:
        with open("mensagem.txt", "r") as arquivo:
            mensagem = arquivo.read()
        return mensagem
    except FileNotFoundError:
        print("O arquivo 'mensagem.txt' não foi encontrado!")

def extended_gcd(a, b):
    if a == 0:
        return b, 0, 1
    g, x, y = extended_gcd(b % a, a)
    return g, y - (b // a) * x, x

def mod_inverse(a, p):
    a = a % p
    if a == 0:
        return None  # Sem inverso modular se a == 0
    g, x, _ = extended_gcd(a, p)
    if g != 1:
        return None
    return x % p

def is_on_curve(x, y, a, b, p):
    return (y * y) % p == (x * x * x + a * x + b) % p

def point_addition(P, Q, a, p):
    if P is None:
        return Q
    if Q is None:
        return P
    if P == Q:
        if P[1] == 0:
            return None
        lamb = (3 * P[0]**2 + a) * mod_inverse(2 * P[1], p)
        if lamb is None:
            return None
    else:
        if P[0] == Q[0]:
            return None
        inv = mod_inverse(Q[0] - P[0], p)
        if inv is None:
            return None
        lamb = (Q[1] - P[1]) * inv % p
    x_r = (lamb * lamb - P[0] - Q[0]) % p
    y_r = (lamb * (P[0] - x_r) - P[1]) % p
    return (x_r, y_r)

def scalar_multiplication(k, P, a, p):
    result = None
    addend = P
    while k:
        if k & 1:
            result = point_addition(result, addend, a, p)
        addend = point_addition(addend, addend, a, p)
        k >>= 1
    return result

def find_order(P, a, b, p):
    order = 1
    current = P
    while current is not None:
        current = point_addition(current, P, a, p)
        if current is None:
            return order
        order += 1
        if current == P:
            break
    return order

def encrypt_message(message, key):
    encrypted = []
    for i, char in enumerate(message):
        encrypted.append(chr((ord(char) + key[i % len(key)]) % 256))
    return ''.join(encrypted)

def decrypt_message(encrypted, key):
    decrypted = []
    for i, char in enumerate(encrypted):
        decrypted.append(chr((ord(char) - key[i % len(key)]) % 256))
    return ''.join(decrypted)

a = int(input("Digite o valor de a: "))
b = int(input("Digite o valor de b: "))

while True:
    try:
        p = int(input("Digite um número primo p "))
        if p > 0 and isprime(p):
            break
        else:
            print("O número deve ser primo e maior que 0!")
    except ValueError:
        print("Entrada inválida. Digite um número inteiro primo!")

E = []
for x in range(p):
    for y in range(p):
        if is_on_curve(x, y, a, b, p):
            E.append((x, y))

print(f"A curva tem {len(E)} pontos.")

g_points = random.sample(E, min(50, len(E)))

orders = []
for g in g_points:
    order = find_order(g, a, b, p)
    orders.append((g, order))
    print(f"Ponto: {g}, Ordem: {order}")

max_order_point = max(orders, key=lambda x: x[1])
G = max_order_point[0]
print(f"Ponto de maior ordem: {G} com ordem {max_order_point[1]}")


while True:
    try:
        m = int(input("Digite o valor de m: "))
        if m > 0:
            break
        else:
            print("O número deve maior que 0!")
    except ValueError:
        print("Entrada inválida. Digite um número inteiro primo!")

while True:
    try:
        n = int(input("Digite o valor de n: "))
        if n > 0:
            break
        else:
            print("O número deve maior que 0!")
    except ValueError:
        print("Entrada inválida. Digite um número inteiro primo!")

A = scalar_multiplication(m, G, a, p)
B = scalar_multiplication(n, G, a, p)
print(f"A = {A}")
print(f"B = {B}")

R = scalar_multiplication(m, B, a, p)
S = scalar_multiplication(n, A, a, p)
print(f"R = {R}")
print(f"S = {S}")

if R == S:
    print("O programa está OK: R = S")
else:
    print("O programa está incorreto: R ≠ S")

key = [R[0] % 256, R[1] % 256]  

#message = input("Digite a mensagem a ser criptografada: ")
message = importar_mensagem()
    
encrypted_message = encrypt_message(message, key)
print(f"Mensagem criptografada: {encrypted_message}")

decrypted_message = decrypt_message(encrypted_message, key)
print(f"Mensagem descriptografada: {decrypted_message}")
