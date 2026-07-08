# CSV to PlantUML

## Purpose

Convert pre-defined `csv` format to specific [PlantUML](https://plantuml.com/) format.

Current `PlantUML` formats available:
* [Mind map](https://plantuml.com/mindmap-diagram)

## Usage

### Mind map conversion

* Pre-requisites: Python 3

* Run the example from current repo:

```bash
cd src &&
python3 csv_to_plantuml_mind_map.py "../data/mind_map/test_input_basic.csv"
```

The file `output.txt` will be created locally and will contain the PlantUML mind map format.
You can view the file with the [PlantUML executable](https://plantuml.com/download).

* (Optional) Run the unit tests from current repo:

```bash
cd src &&
python3 -m unittest csv_to_plantuml_mind_map.py -v
```
