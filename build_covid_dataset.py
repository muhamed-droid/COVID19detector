# USAGE
# python build_covid_dataset.py --covid covid-chestxray-dataset --output dataset/covid

# import the necessary packages
import pandas as pd
import argparse
import shutil
import os

# construct the argument parser and parse the arguments
ap = argparse.ArgumentParser()
ap.add_argument("-c", "--covid", required=True,
	help=r"dataset\dataset\covid") #path to base directory for COVID-19 dataset
ap.add_argument("-o", "--output", required=True,
	help=r"dataset\dataset\normal") #path to directory where 'normal' images will be stored
args = vars(ap.parse_args())

# construct the path to the metadata CSV file and load it
csvPath = os.path.sep.join([args["covid"], "metadata.csv"])
df = pd.read_csv(csvPath)

# loop over the rows of the COVID-19 data frame
for (i, row) in df.iterrows():
	# if (1) the current case is not COVID-19 or (2) this is not
	# a 'PA' view, then ignore the row
	if row["finding"] != "COVID-19" or row["view"] != "PA":
		continue

	# build the path to the input image file
	imagePath = os.path.sep.join([args["covid"], "images",
		row["covid"]])

	# if the input image file does not exist (there are some errors in
	# the COVID-19 metadeta file), ignore the row
	if not os.path.exists(imagePath):
		continue

	# extract the filename from the image path and then construct the
	# path to the copied image file
	filename = row["normal"].split(os.path.sep)[-1]
	outputPath = os.path.sep.join([args["plot"], filename])

	# copy the image
	shutil.copy2(imagePath, outputPath)