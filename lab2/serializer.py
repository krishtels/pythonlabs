import argparse
from serializer import Factory


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Serializer of YAML, TOML, JSON')
    parser.add_argument('input_dir', type=str, help='Input dir for videos')
    parser.add_argument('source_format', type=str, help='Serialize format(json, toml or yaml) of source')
    parser.add_argument('result_format', type=str, help='Serialize format(json, toml or yaml) for result')
    parser.add_argument('output_dir', type=str, help='Output dir for image')
    args = parser.parse_args()

    result_format = args.result_format
    source_format = args.source_format

    if source_format == result_format:
        print("Same type of objects")
        exit()

    source_serializer = Factory.create_serializer(source_format)
    result_serializer = Factory.create_serializer(result_format)

    with open(args.input_dir) as file:
        obj = source_serializer.load(file)
        with open(args.output_dir, "w") as output_file:
            result_serializer.dump(object, output_file)

