import string
from consts import SIGNS_END_OF_SENTENCE, ABBRS


def check_input(input_str, const):
    if input_str is None:
        input_str = const
    elif not input_str.isdigit():
        raise SyntaxError("Invalid input")

    return int(input_str)


def text_clear(text):
    for i in string.punctuation + '\n':
        if i in text:
            text = text.replace(i, '')

    return text


def counter(all_word_list):
    count_dict = {}

    for word in all_word_list:
        if not count_dict.get(word, None):
            count_dict[word] = all_word_list.count(word)

    sorted_count_dict = sorted(count_dict.items(), key=lambda x: x[1], reverse=True)

    return sorted_count_dict


def get_amount_words_in_sentences(sentences_list):
    list_amount_words = []

    for i in range(1, len(sentences_list)):
        amount_words = sentences_list[i] - sentences_list[i - 1]

        if amount_words != 0:
            list_amount_words.append(amount_words)

    return list_amount_words


def get_average_amount_words(sentences_list):
    list_amount_of_words = get_amount_words_in_sentences(sentences_list)
    average_amount = sum(list_amount_of_words) / len(list_amount_of_words)

    return average_amount


def get_median_amount_words(sentences_list):
    list_of_amounts = get_amount_words_in_sentences(sentences_list)
    list_of_amounts.sort()
    median_amount = list_of_amounts[len(list_of_amounts) // 2]

    return median_amount


def get_sentences_start_list(text):
    new_text = text

    for sign in SIGNS_END_OF_SENTENCE:
        new_text = new_text.replace(sign, '.')

    for abbr in ABBRS:
        new_text = new_text.replace(abbr, abbr.strip('.'))

    full_list_words = new_text.split()
    sentences_start = [0]

    for i in range(1, len(full_list_words)):
        if full_list_words[i][0].isupper() and full_list_words[i - 1][-1] == '.':
            sentences_start.append(i)

    sentences_start.append(len(full_list_words))  # adding end of last sentence

    return sentences_start


def find_top_popular_ngramm(list_words, text, n, k):
    ngramm_dict = {}

    for word in list_words:
        for i in range(0, len(word) - n + 1):
            ngramm = word[i:i+n]
            if not ngramm_dict.get(ngramm, None):
                ngramm_dict[ngramm] = text.count(ngramm)

    sorted_ngramm_dict = sorted(ngramm_dict.items(), key=lambda x: x[1], reverse=True)

    return sorted_ngramm_dict[:k]