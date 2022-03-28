from text_tool import text_clear, check_input, get_sentences_start_list, counter, get_median_amount_words, \
    get_average_amount_words, find_top_popular_ngramm
from consts import K, N


def main():
    text = input("Enter your text\n")
    k_input = input("Enter k\n")
    n_input = input("Enter n\n")

    k_input = check_input(k_input, K)
    n_input = check_input(n_input, N)

    sentences_start_list = get_sentences_start_list(text)
    text = text_clear(text.lower())
    list_word = text.split()

    counted_words_dict = counter(list_word)
    average_amount_words = get_average_amount_words(sentences_start_list)
    median_amount = get_median_amount_words(sentences_start_list)
    top_ngramm = find_top_popular_ngramm(list_word, text, n_input, k_input)

    print(counted_words_dict)
    print(average_amount_words)
    print(median_amount)
    print(top_ngramm)


if __name__ == '__main__':
    main()