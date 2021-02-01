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
@click.option('--country', help='Get cases from a specific country/region or even a cruise ship.')
@click.argument('country')
def cases(country):
    """
    Get case data for a specific country
    Also includes UN-distinguished areas such as the Holy See
    Includes many cruise ships that were once quarantined
    """

    case_info = covid.get_country_cases(country=country)

    # TODO: Error handling is incorrect
    if case_info['TotalCases'] is not None:
        click.echo(country+' has '+case_info['TotalCases']+' total confirmed cases')
    else:
        click.echo('No country found. Typo?')


if __name__ == '__main__':
    cli()
