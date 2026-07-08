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
# * Basic: no extra notes, only mind map entities organised hierarchically
# * Advanced: extra notes, alongside the mind map entities

# USAGE = execute the program via the command-line interface (CLI)
# * Basic example (from current folder location):
#   `python3 csv_to_plantuml_mind_map.py ../data/mind_map/test_input_basic.csv`
#   Outputs file `output.txt` at current folder location

# ASSUMPTIONS =
# * Code running with python3
# * Code running on UNIX machines
# * Csv file format ends with `.csv`
# * Csv first row/line (id = 0) is the header
# * Csv first column (id = 0) is the first level,
#   then second column (id = 1) is second level, etc.
# * Csv only contains one level entity per row/line
# * Csv only contains sequential level increases
# * Plantuml mind map file format ends with `.txt`
# * Plantuml mind map uses OrgMode syntax
# * Plantuml mind map uses default config

# TODO =
# * (Optional) Save `os.path.realpath()` when receiving the input from CLI

# 3) Libraries (imports)

from dataclasses import dataclass
import argparse
from argparse import RawTextHelpFormatter
from inspect import cleandoc as cl
import re
import os
import sys
import logging as log_tool
import csv

# 4) Global variables

global_allowed_role_values = ["input", "output"]
global_allowed_mode_values = ["append", "overwrite"]
global_output_file_name = "output.txt"
global_csv_file_extension = "csv"
global_csv_header_line_id = 0
global_plantuml_file_extension = "txt"
global_plantuml_wrap_width = 200
global_plantuml_max_message_size = 150
global_plantuml_root_node_name = "ROOT"

global_current_file_name = os.path.splitext(os.path.basename(__file__))[0]

global_log_format = "[%(levelname)s] [%(asctime)s] - %(message)s"
global_log_level = "DEBUG"
global_log_file_suffix = f"-{global_log_level.lower()}.log"
global_log_file_name = f"{global_current_file_name}{global_log_file_suffix}"
global_log_file_write_mode = "w+"
global_stream_channel = sys.stdout

logger = log_tool.getLogger(__name__)
logger.setLevel(global_log_level)
formatter = log_tool.Formatter(global_log_format)
file_handler = log_tool.FileHandler(
    f"{global_log_file_name}",
    global_log_file_write_mode,
)
file_handler.setFormatter(formatter)
logger.addHandler(file_handler)
console_handler = log_tool.StreamHandler(
    global_stream_channel,
)
console_handler.setFormatter(formatter)
logger.addHandler(console_handler)

# 5) Data types

@dataclass(frozen=True)
class CsvFile:
    required_extension = global_csv_file_extension
    allowed_role_values = global_allowed_role_values

    path: str
    role: str = allowed_role_values[0]

    def get_file_name(self):
        filename, _ = os.path.splitext(self.path)
        return filename

    def __post_init__(self):
        # Ensure non-emptiness
        if not self.path:
            raise ValueError(f"A path cannot be empty.")

        # Ensure restricted role value
        if self.role not in self.allowed_role_values:
            raise ValueError(f"Role value `{self.role}` not in `{self.allowed_role_values}`")

        # Ensure extension
        regex_pattern = f".*\.{self.required_extension}"
        regex_res = re.search(regex_pattern, self.path)
        if not regex_res:
            raise ValueError(f"Cannot find required extension `{self.required_extension}` in `{self}")

        # Ensure existence (if required)
        if self.role == self.allowed_role_values[0]:
            file_exists = False
            if os.path.isfile(self.path):
                file_exists = True
            if not file_exists:
                raise FileNotFoundError(f"File `{self}` not found")

@dataclass(frozen=True)
class CsvLine:
    value: list[str]

@dataclass(frozen=True)
class PlantUmlFile:
    required_extension = global_plantuml_file_extension
    allowed_role_values = global_allowed_role_values

    path: str
    role: str = allowed_role_values[1]


    def get_file_name(self):
        filename, _ = os.path.splitext(self.path)
        return filename

    def __post_init__(self):
        # Ensure non-emptiness
        if not self.path:
            raise ValueError(f"A path cannot be empty.")

        # Ensure restricted role value
        if self.role not in self.allowed_role_values:
            raise ValueError(f"Role value `{self.role}` not in `{self.allowed_role_values}`")

        # Ensure extension
        regex_pattern = f".*\.{self.required_extension}"
        regex_res = re.search(regex_pattern, self.path)
        if not regex_res:
            raise ValueError(f"Cannot find required extension `{self.required_extension}` in `{self}")

        # Ensure existence (if required)
        if self.role == self.allowed_role_values[0]:
            file_exists = False
            if os.path.isfile(self.path):
                file_exists = True
            if not file_exists:
                raise FileNotFoundError(f"File `{self}` not found")

@dataclass(frozen=True)
class PlantUmlLine:
    value: str

@dataclass(frozen=True)
class WriteMode:
    allowed_mode_values = global_allowed_mode_values
    value: str = allowed_mode_values[0]

# 6) Data groups (classes)

class Reader():
    def __init__(self, file_input: CsvFile):
        self.file_input = file_input

    def read_line(self, line_index: int) -> CsvLine:
        output = None
        with open(self.file_input.path, "r") as f:
            csv_reader = csv.reader(f)
            for row_id, row_data in enumerate(csv_reader):
                if row_id == line_index:
                    output = CsvLine(value=row_data)
                    break
        if output is None:
            raise ReadError(f"Unable to read {self.file_input}, at line index {line_index}")
        logger.debug(f"[Reader::read_line] - Read line data `{output}` at line index `{line_index}` from file `{self.file_input}`")
        return output

    def get_total_lines(self) -> int:
        line_count = None
        with open(self.file_input.path, "r") as f:
            csv_reader = csv.reader(f)
            line_count = sum(1 for row in csv_reader)
        if line_count is None:
            raise ReadError(f"Unable to count lines in {self.file_input}")
        logger.debug(f"[Reader::get_total_lines] - Calculated a total of `{line_count}` lines from file `{self.file_input}`")
        return line_count

class Converter():
    def __init__(self):
        pass

    def convert_line(self, line_input: CsvLine) -> PlantUmlLine:
        output = None
        for column_id, column_data in enumerate(line_input.value):
            if column_data:
                # Figure out node level from column id
                # and include root level in the calculation
                node_level_indicator = "*" * (column_id + 1 + 1)
                output = PlantUmlLine(
                    value=cl(
                        f"""
                        {node_level_indicator}:
                        {column_data}
                        ;
                        """
                    )
                )
                break
        if output is None:
            raise ConversionError(f"Unable to convert {line_input}")
        return output

class Writer():
    def __init__(self, file_output: PlantUmlFile):
        self.file_output = file_output

    def write_line(self, line_input: PlantUmlLine, mode: WriteMode = WriteMode()):
        success = False
        file_write_mode = None
        if mode.value == global_allowed_mode_values[0]:
            file_write_mode = "a"
        elif mode.value == global_allowed_mode_values[1]:
            file_write_mode = "w"
        else:
            raise Exception(f"Unable to identify mode value via `{mode}`")
        with open(self.file_output.path, file_write_mode) as f:
            f.write(line_input.value)
        success = True
        if success == False:
            raise WriteError(f"Unable to write {line_input} to {self.file_output} with mode {mode}")
        logger.debug(f"[Writer::write_line] - Wrote line data `{line_input.value}` to file `{self.file_output}`")

class ParseFileInputAction(argparse.Action):
    def __call__(self, parser, namespace, value, option_string=None):
        assert type(value) == str
        parsed_file_input = CsvFile(path=value, role="input")
        setattr(namespace, self.dest, parsed_file_input)

class ParseFileOutputAction(argparse.Action):
    def __call__(self, parser, namespace, value, option_string=None):
        assert type(value) == str
        parsed_file_input = PlantUmlFile(path=value, role="output")
        setattr(namespace, self.dest, parsed_file_input)

# 7) Operations (functions)

def parse_cli_args():
    parser= argparse.ArgumentParser(
        formatter_class = RawTextHelpFormatter,
    )
    parser.add_argument(
        "file_input",
        action=ParseFileInputAction,
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
        action=ParseFileOutputAction,
        help=cl(
            f"""
            Path to file converted (PlantUML mind map txt format)
            By default, current working directory is used
            and file name is `{global_output_file_name}`
            """
        ),
    )
    args = parser.parse_args()
    return args

# 8) Errors

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

# 9) Tests

# 10) Main

def main():
    logger.info("[main] - Parsing CLI inputs...")
    cli_inputs=parse_cli_args()
    if cli_inputs.file_output is None:
        cli_inputs.file_output = PlantUmlFile(path=global_output_file_name, role="output")
    logger.info("[main] - ...DONE")

    logger.debug(
        cl(
            f"""
            [main] - Parsed the following CLI inputs:
            * File input = {cli_inputs.file_input}
            * File output = {cli_inputs.file_output}
            """
        )
    )

    logger.info("[main] - Initialise output file...")
    file_writer = Writer(cli_inputs.file_output)
    output_file_header = cl(
        f"""
        @startmindmap

        skinparam wrapWidth {global_plantuml_wrap_width}
        skinparam maxMessageSize {global_plantuml_max_message_size}

        title {cli_inputs.file_output.get_file_name()}

        * {global_plantuml_root_node_name}
        right side
        """
    )
    file_writer.write_line(line_input=PlantUmlLine(output_file_header), mode=WriteMode("overwrite"))
    logger.info("[main] - ...DONE")

    logger.info("[main] - Converting file input to file output line by line...")
    file_reader = Reader(cli_inputs.file_input)
    converter = Converter()
    total_lines = file_reader.get_total_lines()
    for line_id in range(total_lines):
        # Skip header line
        if line_id == global_csv_header_line_id:
            continue
        output_file_line_return = "\n\n"
        file_writer.write_line(line_input=PlantUmlLine(output_file_line_return), mode=WriteMode("append"))
        extracted_line_data = file_reader.read_line(line_id)
        converted_line_data = converter.convert_line(extracted_line_data)
        file_writer.write_line(line_input=converted_line_data, mode=WriteMode("append"))
    logger.info("[main] - ...DONE")

    logger.info("[main] - Finalise output file...")
    file_writer = Writer(cli_inputs.file_output)
    output_file_line_return = "\n\n"
    file_writer.write_line(line_input=PlantUmlLine(output_file_line_return), mode=WriteMode("append"))
    output_file_end = cl(
        f"""
        @endmindmap
        """
    )
    file_writer.write_line(line_input=PlantUmlLine(output_file_end), mode=WriteMode("append"))
    logger.info("[main] - ...DONE")


if __name__ == "__main__":
    main()

# 11) Automated workflow
# N/A for now
