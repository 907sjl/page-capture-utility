# page-capture-utility
A Python wrapper for Playwright used to export modern HTML pages to PDF files. A 
table of contents file contains the list of URLs to render and export as individual 
PDF files.   

Modern HTML pages rely on Javascript and embedded network connections to servers 
with dynamic content. Playwright and Chromium allow these pages to execute 
scripts and render dynamic content before exporting them to PDF files.        

## Command Line     
```
usage: page_capture_utility.py [-h] toc dest_folder

Create PDF files that are printed snapshots of HTML pages. Supports modern
HTML pages that use javascript or websockets to render.A table of contents
file contains the list of pages to snapshot. Use this together with
pdf_splicer to compile or add pages into reports.

positional arguments:
  toc          Required: Table of contents file
  dest_folder  Required: Folder for destination PDF files

options:
  -h, --help   show this help message and exit
```    

## Table of Contents File    
The table of contents file lists URLS for the script to download and export 
as PDF files.    

It has five columns:
1. **Folder**: (Required) A sub-folder in the output folder to write to
2. **File Name**: (Required) The name of the destination PDF file
3. **URL**: (Required) The URL of the page to download
4. **Width**: (Required) The width of this page in inches
5. **Height**: (Required) The height of this page in inches

Each row in the table of contents file is intended to be a new PDF file with the image of an HTML page.    
