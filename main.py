from argparse import ArgumentParser
from os import path
import re
import xml.etree.ElementTree as ET

# normal regex: /^Sender:\s*(?<sender>.*)\n+Thema:\s*(?<thema>.*)\n+Titel:\s*(?<titel>.*)\n+Datum:\s*(?<datum>.*)\n+Zeit:\s*(?<zeit>.*)\n+Dauer:\s*(?<dauer>.*)\n+Größe:\s*(?<size>.*)\n+Website\n+(?<website>[a-zA-Z0-9:\/.\n\-_]*)\nURL\n+(?<url>[a-zA-Z0-9:\/.\n\-_]*)\n(?<description>[\n\w\W]*)/gm
PARSE_REGEX_RAW = r"Sender:\s*(?P<sender>.*)\n+Thema:\s*(?P<thema>.*)\n+Titel:\s*(?P<titel>.*)\n+Datum:\s*(?P<datum>.*)\n+Zeit:\s*(?P<zeit>.*)\n+Dauer:\s*(?P<dauer>.*)\n+Größe:\s*(?P<size>.*)\n+Website\n+(?P<website>[a-zA-Z0-9:\/.\n\-_]*)\nURL\n+(?P<url>[a-zA-Z0-9:\/.\n\-_]*)\n(?P<description>[\n\w\W]*)"
PARSE_REGEX = re.compile(PARSE_REGEX_RAW, re.MULTILINE)

def main():
    parser = ArgumentParser()

    parser.add_argument("-i", "--input", help="input file", required=True, type=str)
    parser.add_argument("-o", "--output", help="output file", required=True, type=str)

    args = parser.parse_args()

    input_file, output_file = args.input, args.output

    print(f"Input file: {input_file}")
    print(f"Output file: {output_file}")

    if not path.exists(input_file):
        print(f"File '{input_file}' does not exist")
        return

    data = None

    with open(input_file, "r", encoding="utf-8") as f:
        data = f.read()
        print(f"Data: {data}")

    match = PARSE_REGEX.match(data)

    if not match:
        print("File does not appear to be in the correct format")
        return

    data = match.groupdict()

    for key in data:
        data[key] = data[key].strip()

    # sender, thema, titel, datum, zeit, dauer, size, website, url, description
    nfo_data = {
        "title": data["titel"],
        "plot": data["description"],
        "aired": data["datum"],
        "duration": data["dauer"],
        "size": data["size"],
        "website": data["website"],
        "url": data["url"]
    }

    # write as xml
    root = ET.Element("episodedetails")

    for key in nfo_data:
        ET.SubElement(root, key).text = nfo_data[key]

    tree = ET.ElementTree(root)

    ET.indent(tree.getroot())

    tree.write(output_file, encoding="utf-8", xml_declaration=True, method="xml")

if __name__ == "__main__":
    main()