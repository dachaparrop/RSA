import sympy

def gcd(a, b):
    while b != 0:
        a, b = b, a % b
    return a

def mod_inverse(e, phi):
    d, x1, x2, y1 = 0, 0, 1, 1
    temp_phi = phi
    
    while e > 0:
        temp1, temp2 = temp_phi // e, temp_phi - (temp_phi // e) * e
        temp_phi, e = e, temp2
        x = x2 - temp1 * x1
        y = d - temp1 * y1
        x2, x1 = x1, x
        d, y1 = y1, y
    
    if temp_phi == 1:
        return d + phi

def is_prime(num):
    return sympy.isprime(num)

def generate_keypair(p, q):
    if not (is_prime(p) and is_prime(q)):
        raise ValueError('Ambos números deben ser primos.')
    elif p == q:
        raise ValueError('p y q no pueden ser iguales.')
    
    n = p * q
    phi = (p-1) * (q-1)

    e = 65537  # Valor estándar y eficiente para e
    
    if gcd(e, phi) != 1:
        raise ValueError("e no es coprimo con phi(n), lo cual es improbable.")

    d = mod_inverse(e, phi)
    
    return ((e, n), (d, n))

def encrypt(pk, plaintext):
    key, n = pk
    cipher = [pow(ord(char), key, n) for char in plaintext]
    return cipher

def decrypt(pk, ciphertext):
    key, n = pk
    plain = ''.join([chr(pow(char, key, n)) for char in ciphertext])
    return plain

def generate_large_primes(bits):
    p = sympy.randprime(2**(bits-1), 2**bits)
    q = sympy.randprime(2**(bits-1), 2**bits)
    return p, q

# Ejemplo de uso:

# bits = 1024  # Genera números primos de 1024 bits
# p, q = generate_large_primes(bits)
# print(f"Número primo p: {p}")
# print(f"Número primo q: {q}")

# public, private = generate_keypair(p, q)
# print("Clave pública:", public)
# print("Clave privada:", private)

# mensaje = "Hola Mundo"
# cifrado = encrypt(public, mensaje)
# print("Mensaje cifrado:", cifrado)

# descifrado = decrypt(private, cifrado)
# print("Mensaje descifrado:", descifrado)