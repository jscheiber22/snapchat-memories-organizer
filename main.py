import subprocess
import re
import os

magick_binary_loc = "/usr/local/bin/magick/magick"
intake_dir = "."
output_dir = ""
all_files = os.listdir(intake_dir)

for image in all_files:
    if image.endswith('.jpg'):
        image1 = image
        image1_YYYY_MM_DD = re.search(r'\d\d\d\d-\d\d-\d\d', image1)
        if image1_YYYY_MM_DD:
            image1_YYYY_MM_DD = image1_YYYY_MM_DD.group()
            image1_YYYY = image1_YYYY_MM_DD[:4]
            image1_MM = image1_YYYY_MM_DD[5:7]
            image1_DD = image1_YYYY_MM_DD[8:]
            new_datetime = image1_YYYY + image1_MM + image1_DD + '0000'
        else:
            print("no date found in " + image1)
            continue

        name_through_main_image1 = re.search(r'.*-main', image1)
        if name_through_main_image1:
            name_through_main_image1 = name_through_main_image1.group().replace('-main', '')
        else:
            print("no full name found in " + image1)
            continue

        # original name without -main and the extension pasted back on
        output_filename = name_through_main_image1 + image1[-4:]

        image2 = name_through_main_image1 + "-overlay.png"
        if image2 in all_files:
            subprocess.call('sudo {} convert {} -background none -flatten miff:- | sudo {} composite -gravity center - {} {} && sudo touch -t {} {}'.format(magick_binary_loc, image2, magick_binary_loc, image1, output_dir + output_filename, new_datetime, output_dir + output_filename), shell=True)
        # else: 
        #     subprocess.call('mv {} {}'.format(image1, output_dir + output_filename), shell=True)
