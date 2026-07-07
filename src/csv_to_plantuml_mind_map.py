#!/usr/bin/env python3

# 1) Licence

# Copyright 2026 Achille MARTIN
#
# Permission is hereby granted, free of charge,
# to any person obtaining a copy of this software and associated documentation
# files (the “Software”), to deal in the Software without restriction,
# including without limitation the rights to use, copy, modify, merge, publish,
# distribute, sublicense, and/or sell copies of the Software,
# and to permit persons to whom the Software is furnished to do so,
# subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included
# in all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED “AS IS”, WITHOUT WARRANTY OF ANY KIND,
# EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO
# THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE
# AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS
# OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY,
# WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE
# OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.

# 2) Guidance

# PURPOSE = Convert from csv format to plantuml mind map format
# * BASIC = no extra notes, only mind map entities organised hierarchically
# * ADVANCED = extra notes, alongside the mind map entities

# USAGE = execute the program via the command-line interface (CLI)

# 3) Libraries (imports)

from dataclasses import dataclass
import argparse
from argparse import RawTextHelpFormatter
from inspect import cleandoc as cl

# 4) Data types

@dataclass(frozen=True)
class CsvFile:
    path: str

@dataclass(frozen=True)
class CsvLine:
    value: str

@dataclass(frozen=True)
class PlantUmlFile:
    path: str

@dataclass(frozen=True)
class PlantUmlLine:
    value: str

@dataclass(frozen=True)
class WriteMode:
    allowed_values = ["append", "overwrite"]
    value: str = allowed_values[0]

# 5) Data groups (classes)

class Reader():
    def __init__(self, file_input: CsvFile):
        self.file_input = file_input

    def read_line(self, line_index: int) -> CsvLine:
        output = None
        if output is None:
            raise ReadError(f"Unable to read {self.file_input}, at line {line_index}")
        return output

class Converter():
    def __init__(self):
        pass

    def convert_line(self, line_input: CsvLine) -> PlantUmlLine:
        output = None
        if output is None:
            raise ConversionError(f"Unable to convert {line_input}")
        return output

class Writer():
    def __init__(self, file_output: PlantUmlFile):
        self.file_output = file_output

    def write_line(self, line_input: PlantUmlLine, mode: WriteMode):
        success = False
        if success == False:
            raise WriteError(f"Unable to write {line_input} to {self.file_output} with mode {mode}")

# 6) Operations (functions)

def parse_cli_args():
    parser= argparse.ArgumentParser(
        formatter_class = RawTextHelpFormatter,
    )
    parser.add_argument(
        "file_input",
        help=cl(
            """
            Path to file to convert (csv format)
            """
        ),
    )
    parser.add_argument(
        "-o",
        "--file-output",
        dest="file_output",
        metavar="FILE_OUTPUT",
        help=cl(
            """
            Path to file converted (PlantUML mind map format)
            By default, current working directory is used
            and file name is `output.txt`
            """
        ),
    )
    args = parser.parse_args()
    return args

# 7) Errors

class ReadError(Exception):
    def __init__(self, message):
        self.message = message
        super().__init__(self.message)

class ConversionError(Exception):
    def __init__(self, message):
        self.message = message
        super().__init__(self.message)

class WriteError(Exception):
    def __init__(self, message):
        self.message = message
        super().__init__(self.message)

# 8) Tests

# 9) Main

def main():
    cli_inputs=parse_cli_args()

if __name__ == "__main__":
    main()

# 10) Automated workflow

