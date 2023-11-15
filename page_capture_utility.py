"""
page_capture_utility.py
A script to create PDF snapshots of HTML pages using the Playwright package.  This approach
supports modern HTML pages that leverage scripting and websockets.
https://907sjl.github.io/
"""

import os
import argparse
import asyncio

import pandas as pd
from pandas import DataFrame

from playwright.async_api import async_playwright

HELP_DESCRIPTION = ('Create PDF files that are printed snapshots of HTML pages.  Supports modern ' +
                    'HTML pages that use javascript or websockets to render.' +
                    'A table of contents file contains the list of pages to snapshot.  Use this ' +
                    'together with pdf_splicer to compile or add pages into reports.')
"""Description displayed on the command line using the help option."""


TOC_COLUMNS = {
    'Folder': 'string',
    'File Name': 'string',
    'URL': 'string',
    'Orientation': 'string',
    'Width': 'string',
    'Height': 'string'
}
"""Describes the columns of the table of contents file."""


def load_toc(toc_path: str) -> pd.DataFrame:
    """
    Loads the file with the list of source pages to snapshot.
    :param toc_path: The file path
    :return: A dataframe with the table of contents
    """
    print('Loading', toc_path, 'as table of contents')
    df = pd.read_csv(toc_path, dtype=TOC_COLUMNS)
    df.sort_values(by=['Folder', 'File Name'], ascending=[True, True], inplace=True)
    df.reset_index(drop=True, inplace=True)
    return df
# END load_toc


def parse_command_line_parameters() -> dict[str, str]:
    """
    Collects the command line parameters into a dictionary.
    :return: A dictionary of parameter names and values
    """
    parser = argparse.ArgumentParser(
        description=HELP_DESCRIPTION,
        formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    parser.add_argument('toc', help='Required: Table of contents file')
    parser.add_argument('dest_folder', help='Required: Folder for destination PDF files')
    args = parser.parse_args()
    config = vars(args)
    return config
# END parse_command_line_parameters


async def capture_pages(toc: DataFrame, dest_folder: str) -> None:
    """
    Loops through the table of contents to capture each page into a PDF.
    toc: the dataframe with the list of pages to snapshot
    dest_folder: the relative folder path for output pdf files
    :return: none
    """

    async with async_playwright() as p:
        browser = await p.chromium.launch()

        for index, row in toc.iterrows():
            folder_name = row['Folder']
            file_name = row['File Name']
            page_url = row['URL']
            # page_orientation = row['Orientation']
            width = row['Width'] + 'in'
            height = row['Height'] + 'in'

            target_file = os.path.join(dest_folder, folder_name, file_name)
            
            print('Loading', page_url, 'with 5 seconds delay...')
            page = await browser.new_page()
            await page.emulate_media(media="print")
            await page.goto(page_url)
            await page.wait_for_timeout(5000)
            
            await page.pdf(width=width, height=height, print_background=True, path=target_file)

        await browser.close()
# END capture_pages


"""
MAIN
"""
_parameters = parse_command_line_parameters()

_toc_df = load_toc(_parameters['toc'])

asyncio.run(capture_pages(_toc_df, _parameters['dest_folder']))
