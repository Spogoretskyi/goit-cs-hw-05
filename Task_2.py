from concurrent.futures import ThreadPoolExecutor
from collections import defaultdict
import matplotlib.pyplot as plt
import string


class TextAnalyzer:
    def __init__(self, logger):
        self.logger = logger

    def map_function(self, word):
        return word, 1

    @staticmethod
    def shuffle_function(mapped_values):
        shuffled = defaultdict(list)
        for key, value in mapped_values:
            shuffled[key].append(value)
        return shuffled.items()

    @staticmethod
    def reduce_function(key_values):
        key, values = key_values
        return key, sum(values)

    async def map_reduce(self, text):
        try:
            text = self.remove_punctuation(text)
            words = text.split()

            if words:
                with ThreadPoolExecutor() as executor:
                    mapped_values = list(executor.map(self.map_function, words))

                shuffled_values = self.shuffle_function(mapped_values)

                with ThreadPoolExecutor() as executor:
                    reduced_values = list(
                        executor.map(self.reduce_function, shuffled_values)
                    )

                return dict(reduced_values)
            self.logger.warning("No words to visualize")
        except Exception as e:
            self.logger.error(f"Error occurred during map reduce: {e}")
            return {}

    async def visualize_top_words(self, text, num_words):
        try:
            self.logger.info(f"Processing vizualization top words...")
            result = await self.map_reduce(text)

            if not result:
                self.logger.warning("No result to visualize")
                return

            sorted_result = sorted(result.items(), key=lambda x: x[1], reverse=True)
            top_words = [pair[0] for pair in sorted_result[:num_words]]
            frequencies = [pair[1] for pair in sorted_result[:num_words]]

            plt.bar(top_words, frequencies)
            plt.xlabel("Words")
            plt.ylabel("Frequencies")
            plt.title(f"Top {num_words} words")
            plt.show()

            self.logger.info(f"Vizualization top words is done")
        except Exception as e:
            self.logger.error(f"Error occurred during visualization: {e}")

    @staticmethod
    def remove_punctuation(text):
        return text.translate(str.maketrans("", "", string.punctuation))
