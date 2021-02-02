
def find_country(string):
    """
    Finds country by abbreviation
    For example:
        Bra for Brazil
        CR for Costa Rica
        tm for The Mediterranean
    Not case-sensitive
    """

    country_list = open('data/list-of-countries.csv').readlines()
    matches = []

    for country in country_list:

        country_words = country.split(' ')

        if len(country_words) > 1:

            country_abbr = []
            for word in country_words:
                country_abbr.append(list(word)[0])

            country_abbr = ''.join(country_abbr)
            if country_abbr.lower() == string.lower():
                return country.replace('\n', '')

        else:

            country_letters = list(country.replace('\n', ''))
            string_letters = list(string)
            num_matches = 0

            for letter in range(0, min(len(country_letters), len(string_letters))):

                if country_letters[letter].lower() == string_letters[letter].lower():
                    num_matches += 1
                else:
                    break

            if num_matches != 0:
                matches.append((country.replace('\n', ''), num_matches))

    max_matching = ('[Country]', 0)
    for match in matches:
        if match[1] > max_matching[1]:
            max_matching = match

    return max_matching[0]


print(find_country('Arg'))
