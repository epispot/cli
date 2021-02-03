from __init__ import *
from __init__ import __version__, __repo_data_url__


@click.group()
def cli():
    pass


@cli.command()
def version():
    """
    Gets version info
    """

    click.echo('This release is version '+__version__)
    click.echo('The latest releases & more can be found from the repodata source below:')
    click.echo(__repo_data_url__)


@cli.command()
def sources():
    """
    Credits, papers, references, & further readings
    """

    click.echo(click.style('\nCredits\n', fg='green', bold=True))
    click.echo('The epi-cli would not have been possible without the many people who have contributed to the epispot '
               'organization on Github in order to end COVID-19. The repodata source is linked below:')
    click.echo('    Repodata source: '+__repo_data_url__)
    click.echo('    The epispot organization on Github: https://www.github.com/epispot\n')
    click.echo('COVID-19 data is gathered using the COVID-19-Data API along with a regions file to map certain regions '
               'to countries. If your country or region is missing, submit an issue on Github or add it yourself in '
               'the data/regions.csv file.')
    click.echo('    COVID-19-Data API: https://github.com/jrclarete/COVID-19-Cases')
    click.echo('    Issue Link on Github: '+__repo_data_url__+'/issues/new\n')
    click.echo('Lastly, the click package was used to port covid19-tracker onto a CLI')
    click.echo('    Click Documentation: https://click.palletsprojects.com/en/7.x/')

    click.echo(click.style('\nArticles\n', fg='green', bold=True))
    click.echo('The main Medium blog posts that inspired the epispot package are linked below:')
    click.echo('    https://towardsdatascience.com/infectious-disease-modelling-part-i-understanding-sir-28d60e29fdfc')
    click.echo('    https://q9i.medium.com/reopening-safely-the-data-science-approach-289fd86ef63')

    click.echo(click.style('\nFurther Reading\n', fg='green', bold=True))
    click.echo('    No docs have been posted at this time. Use --help to get command info.\n')


@cli.command()
def countries():
    """
    List all available countries & regions
    """

    country_list = open('data/list-of-countries.csv', 'r').readlines()
    country_list = [country.replace('\n', '') for country in country_list]
    click.echo('Countries listed below')
    click.echo(', '.join(country_list))


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


def find_only_countries(string):
    """
    Finds country by abbreviation
    For example:
        Bra for Brazil
        CR for Costa Rica
    Not case-sensitive
    Does NOT include regions or continents
    """

    country_list = open('data/list-of-countries.csv').readlines()
    matches = []

    for country in country_list[:223]:

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


@cli.command()
@click.option('--c', 'country', default='world', help='Get cases from a specific country/region or even a cruise ship')
def cases(country):
    """
    Get case data for a specific country or continent
    Also includes UN-distinguished areas such as the Holy See
    Includes many cruise ships that were once quarantined
    """

    regions = open('data/regions.csv').readlines()
    regions_list = [line.split(',')[0] for line in regions]

    if country != 'world':
        case_info = covid.get_country_cases(country=country)

    if country == 'world':

        case_info = covid.get_global_cases()
        click.echo('The world has '+case_info['TotalCases']+' total confirmed cases')
        click.echo('More info where available is printed below:')

        if case_info['NewCases'] != '':
            click.echo('    The world has ' + case_info['NewCases'] + ' new cases today')
        if case_info['TotalDeaths'] != '':
            click.echo('    The world has ' + case_info['TotalDeaths'] + ' total deaths')
        if case_info['NewDeaths'] != '':
            click.echo('    The world has ' + case_info['NewDeaths'] + ' new deaths today')
        if case_info['TotalRecovered'] != '':
            click.echo('    The world has ' + case_info['TotalRecovered'] + ' total recovered patients')
        if case_info['NewRecovered'] != '':
            click.echo('    The world has ' + case_info['NewRecovered'] + ' new recovered patients today')
        if case_info['ActiveCases'] != '':
            click.echo('    The world has ' + case_info['ActiveCases'] + ' estimated active cases')
        if case_info['Critical'] != '':
            click.echo('    The world has ' + case_info['Critical'] + ' patients in critical condition')
        if case_info['CasesPerOneMillion'] != '':
            click.echo('    The world has ' + case_info['CasesPerOneMillion'] + ' cases per 1M')
        if case_info['DeathsPerOneMillion'] != '':
            click.echo('    The world has ' + case_info['DeathsPerOneMillion'] + ' deaths per 1M')
        if case_info['TotalTests'] != '':
            click.echo('    The world has ' + case_info['TotalTests'] + ' total tests')
        if case_info['TestsPerOneMillion'] != '':
            click.echo('    The world has ' + case_info['TestsPerOneMillion'] + ' total tests per 1M')

        click.echo('For reference, other statistics and notes are displayed below')
        if case_info['Population'] != '':
            click.echo('    The world has ' + case_info['Population'] + ' people')
        if case_info['LastUpdated'] != '':
            click.echo('    Data for ' + country + ' was last updated as of ' + case_info['LastUpdated'])

        click.echo(click.style('Note: ', bold=True, fg='yellow'), nl=False)
        click.echo('When obtaining case statistics of large regions (like the world), due to the complex political '
                   'processes that each country has before reporting coronavirus data, much of the data shown here may '
                   'not be 100% accurate and should be interpreted as a minimum estimate.')

    elif country in ['North America', 'South America', 'Europe', 'Africa', 'Asia', 'Australia']:
        
        case_info = covid.get_continent_cases(continent=country)
        click.echo(country+' has '+case_info['TotalCases']+' total confirmed cases')
        
        if case_info['NewCases'] != '':
            click.echo('    ' + country + ' has ' + case_info['NewCases'] + ' new cases today')
        if case_info['TotalDeaths'] != '':
            click.echo('    ' + country + ' has ' + case_info['TotalDeaths'] + ' total deaths')
        if case_info['NewDeaths'] != '':
            click.echo('    ' + country + ' has ' + case_info['NewDeaths'] + ' new deaths today')
        if case_info['TotalRecovered'] != '':
            click.echo('    ' + country + ' has ' + case_info['TotalRecovered'] + ' total recovered patients')
        if case_info['NewRecovered'] != '':
            click.echo('    ' + country + ' has ' + case_info['NewRecovered'] + ' new recovered patients today')
        if case_info['ActiveCases'] != '':
            click.echo('    ' + country + ' has ' + case_info['ActiveCases'] + ' estimated active cases')
        if case_info['Critical'] != '':
            click.echo('    ' + country + ' has ' + case_info['Critical'] + ' patients in critical condition')
        if case_info['CasesPerOneMillion'] != '':
            click.echo('    ' + country + ' has ' + case_info['CasesPerOneMillion'] + ' cases per 1M')
        if case_info['DeathsPerOneMillion'] != '':
            click.echo('    ' + country + ' has ' + case_info['DeathsPerOneMillion'] + ' deaths per 1M')
        if case_info['TotalTests'] != '':
            click.echo('    ' + country + ' has ' + case_info['TotalTests'] + ' total tests')
        if case_info['TestsPerOneMillion'] != '':
            click.echo('    ' + country + ' has ' + case_info['TestsPerOneMillion'] + ' total tests per 1M')

        click.echo('For reference, other statistics and notes are displayed below')
        if case_info['Population'] != '':
            click.echo('    ' + country + ' has ' + case_info['Population'] + ' people')
        if case_info['LastUpdated'] != '':
            click.echo('    Data for ' + country + ' was last updated as of ' + case_info['LastUpdated'])

        click.echo(click.style('Note: ', bold=True, fg='yellow'), nl=False)
        click.echo('When obtaining case statistics of large regions (like a continent), due to the complex political '
                   'processes that each country has before reporting coronavirus data, much of the data shown here may '
                   'not be 100% accurate and should be interpreted as a minimum estimate.')

    elif case_info is not None:

        click.echo(country+' has '+case_info['TotalCases']+' total confirmed cases')

        if case_info['NewCases'] != '':
            click.echo('    ' + country + ' has ' + case_info['NewCases'] + ' new cases today')
        if case_info['TotalDeaths'] != '':
            click.echo('    ' + country + ' has ' + case_info['TotalDeaths'] + ' total deaths')
        if case_info['NewDeaths'] != '':
            click.echo('    ' + country + ' has ' + case_info['NewDeaths'] + ' new deaths today')
        if case_info['TotalRecovered'] != '':
            click.echo('    ' + country + ' has ' + case_info['TotalRecovered'] + ' total recovered patients')
        if case_info['NewRecovered'] != '':
            click.echo('    ' + country + ' has ' + case_info['NewRecovered'] + ' new recovered patients today')
        if case_info['ActiveCases'] != '':
            click.echo('    ' + country + ' has ' + case_info['ActiveCases'] + ' estimated active cases')
        if case_info['Critical'] != '':
            click.echo('    ' + country + ' has ' + case_info['Critical'] + ' patients in critical condition')
        if case_info['CasesPerOneMillion'] != '':
            click.echo('    ' + country + ' has ' + case_info['CasesPerOneMillion'] + ' cases per 1M')
        if case_info['DeathsPerOneMillion'] != '':
            click.echo('    ' + country + ' has ' + case_info['DeathsPerOneMillion'] + ' deaths per 1M')
        if case_info['TotalTests'] != '':
            click.echo('    ' + country + ' has ' + case_info['TotalTests'] + ' total tests')
        if case_info['TestsPerOneMillion'] != '':
            click.echo('    ' + country + ' has ' + case_info['TestsPerOneMillion'] + ' total tests per 1M')

        click.echo('For reference, other statistics and notes are displayed below')
        if case_info['Population'] != '':
            click.echo('    ' + country + ' has ' + case_info['Population'] + ' people')
        if case_info['Continent'] != '':
            click.echo('    ' + country + ' is located in ' + case_info['Continent'])
        if case_info['LastUpdated'] != '':
            click.echo('    Data for ' + country + ' was last updated as of ' + case_info['LastUpdated'])

    elif country in regions_list:

        line_num = 0
        for line in range(len(regions)):
            if country == regions[line].split(',')[0]:
                line_num = line

        region_countries = regions[line_num].split(',')
        total_cases = 0
        exceptions = 0
        exception_cases = []

        for region_country in region_countries[1:]:
            case_info = covid.get_country_cases(country=region_country.replace('\n', ''))
            if case_info is not None:
                total_cases += int(case_info['TotalCases'].replace(',', ''))
            else:
                exceptions += 1
                exception_cases.append(region_country)

        click.echo(country+' has '+str(total_cases) + ' cases')
        if exceptions != 0:
            click.echo('This search raised '+str(exceptions)+' exceptions for the following countries')
            click.echo(exception_cases)

    else:

        click.echo('Country not found ...')
        click.echo('Searching for an abbreviation ...')

        guess = find_country(country)
        click.echo('Here are results for '+guess+':\n')
        case_info = covid.get_country_cases(country=guess)

        if case_info:

            click.echo(guess + ' has ' + case_info['TotalCases'] + ' total confirmed cases')

            if case_info['NewCases'] != '':
                click.echo('    ' + guess + ' has ' + case_info['NewCases'] + ' new cases today')
            if case_info['TotalDeaths'] != '':
                click.echo('    ' + guess + ' has ' + case_info['TotalDeaths'] + ' total deaths')
            if case_info['NewDeaths'] != '':
                click.echo('    ' + guess + ' has ' + case_info['NewDeaths'] + ' new deaths today')
            if case_info['TotalRecovered'] != '':
                click.echo('    ' + guess + ' has ' + case_info['TotalRecovered'] + ' total recovered patients')
            if case_info['NewRecovered'] != '':
                click.echo('    ' + guess + ' has ' + case_info['NewRecovered'] + ' new recovered patients today')
            if case_info['ActiveCases'] != '':
                click.echo('    ' + guess + ' has ' + case_info['ActiveCases'] + ' estimated active cases')
            if case_info['Critical'] != '':
                click.echo('    ' + guess + ' has ' + case_info['Critical'] + ' patients in critical condition')
            if case_info['CasesPerOneMillion'] != '':
                click.echo('    ' + guess + ' has ' + case_info['CasesPerOneMillion'] + ' cases per 1M')
            if case_info['DeathsPerOneMillion'] != '':
                click.echo('    ' + guess + ' has ' + case_info['DeathsPerOneMillion'] + ' deaths per 1M')
            if case_info['TotalTests'] != '':
                click.echo('    ' + guess + ' has ' + case_info['TotalTests'] + ' total tests')
            if case_info['TestsPerOneMillion'] != '':
                click.echo('    ' + guess + ' has ' + case_info['TestsPerOneMillion'] + ' total tests per 1M')

            click.echo('For reference, other statistics and notes are displayed below')
            if case_info['Population'] != '':
                click.echo('    ' + guess + ' has ' + case_info['Population'] + ' people')
            if case_info['Continent'] != '':
                click.echo('    ' + guess + ' is located in ' + case_info['Continent'])
            if case_info['LastUpdated'] != '':
                click.echo('    Data for ' + guess + ' was last updated as of ' + case_info['LastUpdated'])


def get_total(country):
    """
    Runs through all available functions and metrics to return total cases
    Does not print to terminal
    """

    regions = open('data/regions.csv').readlines()
    regions_list = [line.split(',')[0] for line in regions]

    if country != 'world':

        case_info = covid.get_country_cases(country=country)

        if case_info is None:
            guess = find_only_countries(country)
            case_info = covid.get_country_cases(country=guess)

        case_list = [case_info['TotalCases'], case_info['TotalDeaths'], case_info['TotalRecovered'],
                     case_info['ActiveCases'], case_info['Critical'],
                     case_info['TotalTests']]

    if country == 'world':
        case_info = covid.get_global_cases()
        case_list = [case_info['TotalCases'], case_info['TotalDeaths'], case_info['TotalRecovered'],
                     case_info['ActiveCases'], case_info['Critical'],
                     case_info['TotalTests']]

    for k in range(len(case_list)):
        if case_list[k] == '':
            case_list[k] = '0'

    return case_list


@cli.command()
@click.option('--c', 'countries', help='String of comma-separated country names or abbreviations to compare')
def compare(countries):
    """
    Compare multiple countries or regions
    Must be in a comma-separated string, spaces unnecessary but valid
    DO NOT use a region or continent
    """

    countries = countries.replace(' ', '').split(',')

    country_cases = []
    for country in countries:
        country_cases.append((country, get_total(country)))

    x = [i[0] for i in country_cases]
    y = [i[1] for i in country_cases]
    max_y = 0

    for country in range(len(y)):
        for stat in range(len(y[country])):

            y[country][stat] = int(y[country][stat].replace(',', ''))
            if y[country][stat] > max_y:
                max_y = y[country][stat]

    ind = np.arange(len(countries))
    width = 1 / (4 * len(countries))

    plt.bar(ind, [i[0] for i in y], label='Total Cases', width=width, color='#44aa44')
    plt.bar(ind + width, [i[2] for i in y], label='Total Recovered', width=width, color='#880088')
    plt.bar(ind + 2 * width, [i[3] for i in y], label='Estimated Active Cases', width=width, color='#00aaff')
    plt.bar(ind + 3 * width, [i[1] for i in y], label='Total Deaths', width=width, color='#ff6600')
    plt.bar(ind + 4 * width, [i[4] for i in y], label='Critical Condition', width=width, color='#ff8800')
    plt.xlabel('Country')
    plt.ylabel('Case Count')

    plt.xticks(ind + 4 * width / 2, x)
    plt.legend(loc='best')
    plt.show()


if __name__ == '__main__':
    cli()
