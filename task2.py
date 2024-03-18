import asyncio
import string
from collections import defaultdict
from concurrent.futures import ThreadPoolExecutor
import requests
import matplotlib.pyplot as plt


# Функція для завантаження тексту з URL
def get_text(url):
    try:
        response = requests.get(url)
        response.raise_for_status()  # Перевірка на помилки HTTP
        return response.text
    except requests.RequestException as e:
        print(f"Помилка: {e}")
        return None


# Функція для видалення знаків пунктуації з тексту
def remove_punctuation(text):
    return text.translate(str.maketrans("", "", string.punctuation))


# Мапувальна функція для підрахунку кількості входжень кожного слова у тексті
def map_function(word):
    return word, 1


# Функція Shuffle для групування мапованих значень за ключами
def shuffle_function(mapped_values):
    shuffled = defaultdict(list)
    for key, value in mapped_values:
        shuffled[key].append(value)
    return shuffled.items()


# Функція редукції для підсумовування кількості входжень кожного слова
def reduce_function(key_values):
    key, values = key_values
    return key, sum(values)


# Основна функція для виконання MapReduce
async def map_reduce(text):
    try:
        text = remove_punctuation(text)
        words = text.split()

        if words:
            with ThreadPoolExecutor() as executor:
                mapped_values = list(executor.map(map_function, words))

            shuffled_values = shuffle_function(mapped_values)

            with ThreadPoolExecutor() as executor:
                reduced_values = list(
                    executor.map(reduce_function, shuffled_values)
                )

            return dict(reduced_values)
        print("No words to visualize")
    except Exception as e:
        print(f"Error occurred during map reduce: {e}")
        return


# Функція для візуалізації топ N слів
def visualize_top_words(reduced_words, n=10):
    # Сортування словника за значеннями (кількістю входжень)
    sorted_word_counts = sorted(reduced_words.items(), key=lambda x: x[1], reverse=True)
    words, counts = [], []

    for word, count in sorted_word_counts[:n]:
        words.append(word)
        counts.append(count)

    # Візуалізація топ слів за допомогою горизонтального стовпчикового графіка
    plt.figure(figsize=(10, 6))
    plt.barh(words, counts, color="skyblue")
    plt.xlabel("Кількість")
    plt.ylabel("Слова")
    plt.title(f"Топ {n} слів")
    plt.gca().invert_yaxis()
    plt.show()

async def main():
    # URL-адреса для завантаження тексту
    url = "https://gutenberg.net.au/ebooks01/0100021.txt"

    # Отримання тексту з URL
    text = get_text(url)

    if text:
        # Виконання MapReduce на тексті
        words_counts = await map_reduce(text)

        # Візуалізація топ-слів з найвищою частотою використання
        visualize_top_words(words_counts)


if __name__ == "__main__":
    asyncio.run(main())
