# fitness_data_summarizer
Tiny utility to read data from Apple Health/Fitness and provide some stats they don't (like monthly/yearly distance walked)

Use:
* Export Apple Health data from the app in iOS to your Google Drive or somewhere accessible
* Download health data (.zip file), uncompress
* Set up your Python environment the way you see fit - project requires `python.dateutil` and `lxml` packages
* `python apple_workout_parser.py --file <XML file> --year <4-digit year> [--month <1-12>]`
* XML file to use is (typically?) called `export.xml` in the standard Apple exported .zip file

