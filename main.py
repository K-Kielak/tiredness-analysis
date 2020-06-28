import logging

import click

from tiredness_analysis.runnables.extract_features import extract_features
from tiredness_analysis.runnables.plot_patterns import plot_patterns
from tiredness_analysis.runnables.process_videos import process_videos


@click.group()
@click.option('--debug', is_flag=True)
def cli(debug: bool):
    _setup_logging(debug)


def _setup_logging(debug: bool):
    level = logging.DEBUG if debug else logging.INFO
    message_format = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    log_formatter = logging.Formatter(fmt=message_format)
    console_handler = logging.StreamHandler()
    console_handler.setFormatter(log_formatter)
    console_handler.setLevel(level)
    logging.basicConfig(level=level, format=message_format)
    logger = logging.getLogger('tiredness_analysis')
    logger.setLevel(level)
    logger.addHandler(console_handler)
    logger.info(f'Debug mode is {"on" if debug else "off"}')


cli.add_command(process_videos)
cli.add_command(plot_patterns)
cli.add_command(extract_features)


if __name__ == '__main__':
    cli()
