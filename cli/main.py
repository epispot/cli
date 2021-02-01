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
    click.echo('    The epispot organization on Github: https://www.github.com/epispot')
    click.echo('COVID-19 data is gathered using the COVID-19-Data API along with a regions file to map certain regions '
               'to countries. If your country or region is missing, submit an issue on Github or add it yourself in '
               'the data/regions.csv file.')
    click.echo('    COVID-19-Data API: https://github.com/jrclarete/COVID-19-Cases')
    click.echo('    Issue Link on Github: '+__repo_data_url__+'/issues/new')
    click.echo('Lastly, the click package was used to port covid19-tracker onto a CLI')
    click.echo('    Click Documentation: https://click.palletsprojects.com/en/7.x/')


@cli.command()
def countries():
    """
    List all available countries & regions
    """

    country_list = open('data/list-of-countries.csv', 'r').readlines()
    country_list = [country.replace('\n', '') for country in country_list]
    click.echo('Countries listed below')
    click.echo(', '.join(country_list))


@cli.command()
@click.option('--country', default='world', help='Get cases from a specific country/region or even a cruise ship.')
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

    elif country in ['North America', 'South America', 'Europe', 'Africa', 'Asia', 'Australia']:
        case_info = covid.get_continent_cases(continent=country)
        click.echo(country+' has '+case_info['TotalCases']+' total confirmed cases')

    elif case_info is not None:
        click.echo(country+' has '+case_info['TotalCases']+' total confirmed cases')

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
        click.echo('Country not found')


if __name__ == '__main__':
    cli()
