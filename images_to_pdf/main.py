from os import listdir
from os.path import isdir
from logging import INFO, getLogger
import click

from .logging.logger import init_logger
from .images_to_pdf import (
    get_relative_path,
    get_list_of_relative_path,
    get_list_of_images,
    convert_images_color,
    image_to_pdf
)
from .merge_pdf import merge_pdf_files

@click.group()
@click.pass_context
@click.version_option()
def main(ctx):
    init_logger(INFO)
    ctx.obj = {
        'LOGGER': getLogger(__name__.split('.')[0])
    }

@main.command()
@click.pass_obj
@click.option(
    '--images-path',
    '-i',
    required=True,
    type=click.Path(
        exists=True,
        dir_okay=True,
        readable=True
    ),
    help='Path of image/s file/s folder/s'
)
@click.option(
    '--pdf-path',
    '-p',
    required=True,
    type=click.Path(
        exists=True,
        dir_okay=True,
        writable=True
    ),
    help='Path where generated PDF file/s will be stored'
)
def convert_to_pdf(context_object, images_path, pdf_path):
    """Command to create pdf chapter from folder with images pages"""

    if not isdir(images_path):
        raise click.FileError(images_path, 'isn\'t a directory')

    if not isdir(pdf_path):
        raise click.FileError(pdf_path, 'isn\'t a directory')

    raw_images_folders = listdir(images_path)
    context_object['LOGGER'].info(
        'Number of chapter folder to convert: %d',
        len(raw_images_folders)
    )

    for folder in raw_images_folders:
        chapter_number = folder.split(' ')[1]
        pdf_filename = '{}/{}.pdf'.format(pdf_path, chapter_number)

        context_object['LOGGER'].info('Start of the creation %s', pdf_filename)
        context_object['LOGGER'].debug('Chapter number: %s', chapter_number)

        raw_images_path = sorted(get_list_of_relative_path(get_relative_path(images_path, folder)))

        context_object['LOGGER'].debug(raw_images_path)

        images = get_list_of_images(raw_images_path)
        converted_images = convert_images_color(images)
        image_to_pdf(converted_images, pdf_filename)

        context_object['LOGGER'].info('End of the creation %s', pdf_filename)

    context_object['LOGGER'].info('End of the creation of all chapters detected')

@main.command()
@click.pass_obj
@click.option(
    '--filename',
    '-f',
    required=True,
    help='File name of the book'
)
@click.argument(
    'pdf_files',
    nargs=-1,
    type=click.Path(
        exists=True,
        dir_okay=True,
        readable=True
    )
)
def merge_pdf(context_object, filename, pdf_files):
    """Command to merge pdf chapter into one pdf book"""
    context_object['LOGGER'].info('Start merge of input files')
    context_object['LOGGER'].debug(pdf_files)

    merge_pdf_files(list(pdf_files), filename)

    context_object['LOGGER'].info('Files merge in %s', filename)
