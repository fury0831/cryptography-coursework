"""Elliptic-curve arithmetic and a nonconfidential public-offset demonstration.

See ATTRIBUTION.md for source context and README.md for scope and limitations.
No original notebook input or output is included.
"""

def is_prime(n):
    if n < 2:
        return False
    if n == 2:
        return True
    if n % 2 == 0:
        return False

    d = 3
    while d * d <= n:
        if n % d == 0:
            return False
        d = d + 2

    return True


def check_curve(a, b, p):
    if p <= 3:
        print("error: p should be a prime number greater than 3")
        return False
    if not is_prime(p):
        print("error: p must be prime")
        return False

    value = (4 * a ** 3 + 27 * b ** 2) % p
    if value == 0:
        print("error: invalid curve, 4a^3 + 27b^2 = 0 mod p")
        return False

    return True


def right_side(x, a, b, p):
    return (x ** 3 + a * x + b) % p


def is_on_curve(point, a, b, p):
    if point is None:
        return True

    x = point[0]
    y = point[1]
    return (y ** 2) % p == right_side(x, a, b, p)


def inverse_mod(k, p):
    k = k % p
    if k == 0:
        return None
    return pow(k, p - 2, p)


def point_neg(point, p):
    if point is None:
        return None

    x = point[0]
    y = point[1]
    return (x % p, (-y) % p)


def point_add(point1, point2, a, p):
    if point1 is None:
        return point2
    if point2 is None:
        return point1

    x1 = point1[0] % p
    y1 = point1[1] % p
    x2 = point2[0] % p
    y2 = point2[1] % p

    if x1 == x2 and (y1 + y2) % p == 0:
        return None

    if x1 == x2 and y1 == y2:
        inv = inverse_mod(2 * y1, p)
        if inv is None:
            return None
        slope = (3 * x1 ** 2 + a) * inv
    else:
        inv = inverse_mod(x2 - x1, p)
        if inv is None:
            return None
        slope = (y2 - y1) * inv

    slope = slope % p
    x3 = (slope * slope - x1 - x2) % p
    y3 = (slope * (x1 - x3) - y1) % p
    return (x3, y3)


def scalar_mult(n, point, a, p):
    if n == 0 or point is None:
        return None

    if n < 0:
        return scalar_mult(-n, point_neg(point, p), a, p)

    result = None
    addend = point

    while n > 0:
        if n % 2 == 1:
            result = point_add(result, addend, a, p)
        addend = point_add(addend, addend, a, p)
        n = n // 2

    return result


def legendre_symbol(n, p):
    n = n % p
    if n == 0:
        return 0

    value = pow(n, (p - 1) // 2, p)
    if value == p - 1:
        return -1

    return value


def make_two_roots(root, p):
    root = root % p
    other = (-root) % p

    roots = [root]
    if other != root:
        roots.append(other)

    return roots


def square_roots_mod_prime(n, p):
    n = n % p

    if n == 0:
        return [0]

    if legendre_symbol(n, p) != 1:
        return []

    # This follows the method in ecc_cycle.ipynb: p = 3 mod 4.
    if p % 4 == 3:
        root = pow(n, (p + 1) // 4, p)
        return make_two_roots(root, p)

    print("error: this root method needs p % 4 == 3")
    return []


def roots_for_x(x, a, b, p):
    value = right_side(x, a, b, p)
    return square_roots_mod_prime(value, p)


def find_points_by_roots(a, b, p):
    points = []

    x = 0
    while x < p:
        roots = roots_for_x(x, a, b, p)

        i = 0
        while i < len(roots):
            points.append((x, roots[i]))
            i = i + 1

        x = x + 1

    return points


def count_curve_points_by_roots(a, b, p):
    count = 1

    x = 0
    while x < p:
        roots = roots_for_x(x, a, b, p)
        count = count + len(roots)
        x = x + 1

    return count


def factor_number(n):
    factors = []

    d = 2
    while d * d <= n:
        if n % d == 0:
            factors.append(d)
            while n % d == 0:
                n = n // d
        d = d + 1

    if n > 1:
        factors.append(n)

    return factors


def point_order_from_group_order(point, a, p, group_order, factors):
    order = group_order

    i = 0
    while i < len(factors):
        q = factors[i]

        while order % q == 0:
            smaller = order // q

            if scalar_mult(smaller, point, a, p) is None:
                order = smaller
            else:
                break

        i = i + 1

    return order


def find_char_index(alphabet, ch):
    i = 0
    while i < len(alphabet):
        if alphabet[i] == ch:
            return i
        i = i + 1

    return None


def char_to_point(ch, alphabet, letter_start, P, a, p):
    index = find_char_index(alphabet, ch)

    if index is None:
        print("error: character is not in alphabet:", ch)
        return None

    number = letter_start + index
    return scalar_mult(number, P, a, p)


def point_to_char(point, alphabet, letter_start, P, a, p):
    i = 0
    while i < len(alphabet):
        candidate = scalar_mult(letter_start + i, P, a, p)

        if candidate == point:
            return alphabet[i]

        i = i + 1

    print("error: point does not match any character:", point)
    return ""


def message_to_points(message, alphabet, letter_start, P, a, p):
    message_points = []

    i = 0
    while i < len(message):
        point = char_to_point(message[i], alphabet, letter_start, P, a, p)

        if point is None:
            return []

        message_points.append(point)
        i = i + 1

    return message_points


def points_to_message(message_points, alphabet, letter_start, P, a, p):
    message = ""

    i = 0
    while i < len(message_points):
        ch = point_to_char(message_points[i], alphabet, letter_start, P, a, p)
        message = message + ch
        i = i + 1

    return message


def check_mapping(alphabet, letter_start, P, a, p):
    used_points = []

    if scalar_mult(letter_start + len(alphabet), P, a, p) is None:
        print("warning: mapping may be too close to the cycle boundary")

    i = 0
    while i < len(alphabet):
        point = scalar_mult(letter_start + i, P, a, p)

        if point is None:
            print("error: a character maps to the point at infinity")
            return False

        j = 0
        while j < len(used_points):
            if used_points[j] == point:
                print("error: two characters map to the same point")
                return False
            j = j + 1

        used_points.append(point)
        i = i + 1

    return True


def create_keys(Q, n, k, a, p):
    n = n % k
    if n == 0:
        n = 1

    public_nQ = scalar_mult(n, Q, a, p)
    private_key = scalar_mult(k - n, Q, a, p)

    return public_nQ, private_key, n


def encrypt_point(message_point, public_nQ, a, p):
    return point_add(message_point, public_nQ, a, p)


def decrypt_point(cipher_point, private_key, a, p):
    return point_add(cipher_point, private_key, a, p)


def encrypt_message(message, public_nQ, alphabet, letter_start, P, a, p):
    message_points = message_to_points(message, alphabet, letter_start, P, a, p)
    cipher_points = []

    i = 0
    while i < len(message_points):
        cipher_point = encrypt_point(message_points[i], public_nQ, a, p)
        cipher_points.append(cipher_point)
        i = i + 1

    return cipher_points, message_points


def decrypt_message(cipher_points, private_key, alphabet, letter_start, P, a, p):
    message_points = []

    i = 0
    while i < len(cipher_points):
        message_point = decrypt_point(cipher_points[i], private_key, a, p)
        message_points.append(message_point)
        i = i + 1

    message = points_to_message(message_points, alphabet, letter_start, P, a, p)
    return message, message_points
