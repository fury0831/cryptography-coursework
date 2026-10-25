"""RSA arithmetic and factorization from an undergraduate coursework notebook.

See ATTRIBUTION.md for source context and README.md for scope and limitations.
No original notebook input or output is included.
"""

def read_one_record(line):
    line = line.strip()  # Remove whitespace from the beginning and end of the string.
    line = line[1:len(line)-1]  # Remove the outside parentheses.

    first_comma = line.find(",")  # Find the comma after n.
    n = int(line[0:first_comma])  # Convert the first number to an integer.

    list_start = line.find("[")  # Find where the cipher list begins.
    e = int(line[first_comma+1:list_start-2])  # Convert the second number to an integer.

    list_end = line.find("]")  # Find where the cipher list ends.
    message_text = line[list_start+1:list_end]  # Get only the numbers inside the brackets.
    pieces = message_text.split(",")  # Split the cipher numbers at the commas.

    message = []
    for piece in pieces:
        if piece.strip() != "":  # Ignore empty pieces.
            message.append(int(piece))  # Convert each cipher number to an integer.

    return [n, e, message]


def fme(a, b, c):
    result = 1  # Start with the multiplicative identity.
    a = a % c  # Reduce a before doing repeated squaring.

    while b > 0:
        if b % 2 == 1:  # If the current binary digit is 1, use this power of a.
            result = (result * a) % c
        a = (a * a) % c  # Square a for the next binary digit.
        b = b // 2  # Move to the next binary digit of b.

    return result


def gcd(a, b):
    while b != 0:
        a, b = b, a % b
    return a


def extended_gcd(a, b):
    old_r, r = a, b  # Remainders.
    old_x, x = 1, 0  # Coefficients for a.
    old_y, y = 0, 1  # Coefficients for b.

    while r != 0:
        q = old_r // r
        old_r, r = r, old_r - q * r
        old_x, x = x, old_x - q * x
        old_y, y = y, old_y - q * y

    return old_r, old_x, old_y


def mod_inverse(e, phi):
    gcd_value, x, y = extended_gcd(e, phi)  # Find x so that e*x + phi*y = gcd.
    if gcd_value != 1:  # The inverse exists only when gcd(e, phi) is 1.
        return None
    else:
        return x % phi


def compute_d(p, q, e):
    phi = (p - 1) * (q - 1)  # Euler phi for n = p*q.
    d = mod_inverse(e, phi)  # Private exponent d is the inverse of e mod phi.
    return d


def decrypt_numbers_to_string(num_list):
    result = ""
    for num in num_list:
        char = chr(num)  # Convert a character code back into a character.
        result = result + char
    return result


def smallest_prime_factor(n):
    if n < 2:  # Numbers below 2 are not prime.
        return None

    if n % 2 == 0:  # Check the only even prime factor first.
        return 2

    i = 3
    while i * i <= n:  # Only test factors up to sqrt(n).
        if n % i == 0:
            return i
        i += 2  # Skip even numbers.

    return n


def pollard_rho_factor(n):
    if n % 2 == 0:  # First check small factors.
        return 2
    if n % 3 == 0:  # Check another small factor before the loop.
        return 3

    c = 1  # Constant in the polynomial x^2 + c.
    while True:
        x = 2  # Slow pointer.
        y = 2  # Fast pointer.
        d = 1  # Current gcd result.

        while d == 1:
            x = (x * x + c) % n  # Move x one step.
            y = (y * y + c) % n  # Move y one step.
            y = (y * y + c) % n  # Move y a second step.

            difference = x - y  # Compare the two values.
            if difference < 0:
                difference = -difference  # Make the difference positive.

            d = gcd(difference, n)  # A nontrivial gcd gives a factor of n.

        if d != n:  # If d is not n, then d is a useful factor.
            return d

        c += 1


def factor_n(n):
    if n < 10000000000:  # Trial division is fine for the small first message.
        p = smallest_prime_factor(n)
    else:
        p = pollard_rho_factor(n)  # Use Pollard rho for larger numbers.

    q = n // p  # The other factor is n divided by p.

    if p > q:  # Put the smaller factor first.
        temp = p
        p = q
        q = temp

    return p, q


def decrypt_rsa_message(n, e, message):
    p, q = factor_n(n)  # First factor n into p and q.
    d = compute_d(p, q, e)  # Compute the private exponent.

    decrypted_numbers = []
    for num in message:
        decrypted_numbers.append(fme(num, d, n))  # Decrypt one cipher number.

    plaintext = decrypt_numbers_to_string(decrypted_numbers)  # Convert numbers to text.
    return p, q, d, plaintext
