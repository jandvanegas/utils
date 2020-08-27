#!/home/jandux/utils/venv/bin/python
import getopt
import sys
import subprocess
import re
import pdf2image
import os


def get_next_image(output_file):
    occurrences = subprocess.Popen(["awk", "/!.*\(image.*jpg\)/{print $0}", output_file], stdout=subprocess.PIPE)
    occurrences.wait()
    last_image = subprocess.Popen(('tail', '-n', '1'), stdin=occurrences.stdout, stdout=subprocess.PIPE)
    last_image = last_image.stdout.read().decode("utf-8")
    image_number = re.findall("[0-9]+", last_image)
    if len(image_number) == 0:
        return 1
    assert len(image_number) == 1, f"Some error when finding the last image. This is what was found: {image_number}"
    image_number = int(image_number[0])
    return image_number + 1


def insert_images(input_file, output_file):
    first_image = get_next_image(output_file)
    print(f'The next image is {first_image}')
    number_of_images = read_images_from_pdf(first_image, input_file)
    assert number_of_images > 0, "Images were not found in the input file"
    with open(output_file, "a") as file_object:
        for index in range(number_of_images):
            file_object.write("\n![](image_" + str(index + first_image) + '.jpg)\n')


def read_images_from_pdf(first_image, input_file):
    images = pdf2image.convert_from_path(input_file, output_folder=".", fmt='jpg')
    for image_index, image in enumerate(images):
        new_name = 'image_' + str(image_index + first_image) + '.jpg'
        print(new_name)
        os.rename(image.filename, new_name)
    return len(images)


def main(argv):
    input_file = ''
    output_file = ''
    try:
        opts, args = getopt.getopt(argv, "hi:o:", ["ifile=", "ofile="])
    except getopt.GetoptError:
        print('insertImages.py -i <input_file> -o <output_file>')
        sys.exit(2)
    for opt, arg in opts:
        if opt == '-h':
            print('insertImages.py -i <input_file> -o <output_file>')
            sys.exit()
        elif opt in ("-i", "--ifile"):
            input_file = arg
        elif opt in ("-o", "--ofile"):
            output_file = arg
    print(f"Input file is {input_file}")
    print(f'Output file is {output_file}')
    insert_images(input_file, output_file)


if __name__ == "__main__":
    main(sys.argv[1:])
