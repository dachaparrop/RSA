import sympy


def gcd(a, b):
    """
        Compute the greatest common divisor (GCD) of a and b.
    """
    
    while b != 0:
        a, b = b, a % b
    return a


def mod_inverse(e, phi):
    
    """
        Compute the modular multiplicative inverse of e modulo phi.
    """
    
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
    """
        Check if a number is prime.
    """
    
    return sympy.isprime(num)


def generate_keypair(p, q):
    """
        Generate a public and private key pair using primes p and q.
    """
    
    if not (is_prime(p) and is_prime(q)):
        raise ValueError('Both numbers must be prime.')
    elif p == q:
        raise ValueError('p and q cannot be the same.')
    
    n = p * q
    phi = (p-1) * (q-1)
    e = 65537  # Standard and efficient value for e
    
    if gcd(e, phi) != 1:
        raise ValueError("e is not coprime with phi(n), which is unlikely.")

    d = mod_inverse(e, phi)
    return ((e, n), (d, n))


def encrypt(pk, plaintext):
    """
        Encrypt the plaintext using the public key pk.
    """

    key, n = pk
    cipher = [pow(ord(char), key, n) for char in plaintext]
    return cipher


def decrypt(pk, ciphertext):
    """
        Decrypt the ciphertext using the private key pk.
    """

    key, n = pk
    plain = ''.join([chr(pow(char, key, n)) for char in ciphertext])
    return plain


def generate_large_primes(bits):
    """
        Generate two large prime numbers with the specified bit size.
    """

    p = sympy.randprime(2**(bits-1), 2**bits)
    q = sympy.randprime(2**(bits-1), 2**bits)
    
    return p, q
