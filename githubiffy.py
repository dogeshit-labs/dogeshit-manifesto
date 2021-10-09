#!/usr/bin/env python3
import argparse
import os
import pathlib
import re
import urllib.parse

RENDER_URL = "https://render.githubusercontent.com/render/math?"

def directory(string):
    if not pathlib.Path(string).is_dir():
        raise ValueError()
    return string

def file(string):
    if not pathlib.Path(string).is_file():
        raise ValueError()
    return string

def make_url(latex):
   encoded_tex = urllib.parse.quote_plus(latex)
   query_str = urllib.parse.urlencode({ 'math' : encoded_tex})
   return RENDER_URL + query_str

def make_inline_tag(latex, eq_no):
    return "![Inline Equation {}]({})".format(eq_no, make_url(latex))

def make_standalone_tag(latex, eq_no, size=None):
    if size not in (None, "large", "Large", "LARGE", "huge", "Huge"):
        raise ValueError("Unsupported size: {}. Valid sizes are 'large', 'Large', 'LARGE', 'huge', and 'Huge'".format(size))
    size = '' if not size else size
    tag = "![Equation {}]({})".format(eq_no, make_url(size + ' ' + latex))
    return "<br>\n{}\n<br>".format(tag)

def inline_replace(match):
    global inline_match_count
    inline_match_count = inline_match_count + 1
    return make_inline_tag(match.groups()[0], inline_match_count)

def format_inline_equations(text):
    global inline_match_count
    inline_match_count = 0
    p = re.compile(r'\$([^$\n]+)\$', re.MULTILINE)
    return p.sub(inline_replace, text)

def standalone_replace(match):
    global eq_match_count
    eq_match_count = eq_match_count + 1
    return make_standalone_tag(match.groups()[0], eq_match_count)

def format_equations(text):
    global eq_match_count
    eq_match_count = 0
    p = re.compile(r'\$\$\n(.*)\n\$\$', re.MULTILINE)
    return p.sub(standalone_replace, text)

def format_content(filename):
    with open(filename, 'r') as f:
        content = f.read()
    content = format_inline_equations(content)
    return format_equations(content)

def write_formatted(filename, content, out_dir):
    basename = os.path.basename(filename)
    base, ext = os.path.splitext(basename)
    outfile = os.path.join(out_dir, base + '.gf' + ext)
    with open(outfile, 'w') as o:
        o.write(content)

def main(files, out_dir):
    for filename in files:
        content = format_content(filename)
        write_formatted(filename, content, out_dir)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        prog="githubiffy",
        description="Convert pandoc makdown LaTeX to image links that are rendered by Github"
    )
    parser.add_argument("files", nargs="+", type=file, help="The pandoc markdown files to convert")
    parser.add_argument("-d", "--dir", type=directory, default="build", help="The output directory to write the converted files to.")
    args = parser.parse_args()
    main(args.files, args.dir)
