class CaesarShift:
    def __init__(self):
        alpha = [i for i in range(65, 300) if chr(i).isalpha()]
        offsets = [alpha[0]]

        for i in range(len(alpha) - 1):
            if alpha[i + 1] - alpha[i] != 1:
                offsets.extend([alpha[i], alpha[i + 1]])

        offsets.append(alpha[-1])

        self.__offset = []

        for i in range(0, len(offsets) - 1, 2):
            left, right = offsets[i], offsets[i + 1]
            self.__offset.append((left, right - left + 1))

    def __crypto(self, text: str, key: int) -> str:
        result = ""
        key %= 26
        for char in text:
            if char.isalpha():
                value = ord(char)
                for left, offset in self.__offset:
                    if value < left:
                        result += char
                        break
                    elif left <= value < left + offset:
                        result += chr((value - left + key) % 26 + left)
                        break
            else:
                result += char
        return result

    def encode(self, text: str, key: str) -> str:
        encoded_text = self.__crypto(text, key)
        return ascii(encoded_text).replace('    ', '\\t')

    def decode(self, text: str, key: int) -> str:
        decoded_text = text.encode('utf-8').decode('unicode-escape')
        return self.__crypto(decoded_text, 26 - key % 26)


if __name__ == '__main__':
    cypher = CaesarShift()

    with open('caesar_shift.py', 'r') as file:
        message = file.read()

    key = 1293

    encrypted = cypher.encode(message, key)
    print(encrypted)

    decrypted = cypher.decode(encrypted, key)
    print(decrypted + '\n')
