import numpy as np


def generate_key_matrix(size):
    while True:
        # генерируем случайную квадратную матрицу заданного размера
        key_matrix = np.random.randint(0, 256, size=(size, size), dtype=np.uint8)

        # проверяем, что определитель матрицы не равен нулю и не имеет общих делителей с размером алфавита (256)
        if np.linalg.det(key_matrix) != 0 and np.gcd(int(np.linalg.det(key_matrix)), 256) == 1:
            break

    # вычисляем обратную матрицу с помощью LU-разложения
    inv_key_matrix = np.linalg.inv(key_matrix)

    # приводим элементы матрицы к типу uint8 и по модулю 256
    key_matrix = np.mod(key_matrix.astype(np.uint8), 256)
    inv_key_matrix = np.mod(inv_key_matrix.astype(np.uint8), 256)

    return key_matrix, inv_key_matrix

def determinant(matrix):
    return int(round(np.linalg.det(matrix)))


def encode(message, key):
    message_size = len(message)
    block_size = len(key)
    key_matrix = np.array(key)
    blocks = [message[i:i + block_size] for i in range(0, message_size, block_size)]
    encoded_blocks = []
    for block in blocks:
        if len(block) < block_size:
            block += ' ' * (block_size - len(block))  # добавление пробелов
        block_matrix = np.array([ord(char) for char in block])
        block_matrix = block_matrix.reshape(-1, block_size)
        encoded_block_matrix = np.matmul(block_matrix, key_matrix) % 256
        encoded_block = "".join([chr(char) for char in encoded_block_matrix.reshape(-1)])
        encoded_blocks.append(encoded_block)
    encoded_message = "".join(encoded_blocks)
    return encoded_message

def decode(message, key):
    message_size = len(message)
    block_size = len(key)
    key_matrix = np.array(key)
    blocks = [message[i:i + block_size] for i in range(0, message_size, block_size)]
    decoded_blocks = []
    for block in blocks:
        block_matrix = np.array([ord(char) for char in block])
        decoded_block_matrix = np.matmul(block_matrix, inv_key) % 256
        decoded_block = "".join([chr(char) for char in decoded_block_matrix.reshape(-1)])
        decoded_blocks.append(decoded_block)
    decoded_message = "".join(decoded_blocks).rstrip()  # убираем лишние пробелы в конце
    return decoded_message


message = "Hello"
length = 4
key, inv_key = generate_key_matrix(int(length))
encoded_message = encode(message, key)
decoded_message = decode(message, key)
