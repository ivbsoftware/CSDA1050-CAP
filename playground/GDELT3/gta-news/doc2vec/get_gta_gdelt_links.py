import requests
import lxml.html as lh
import os.path
import urllib
import zipfile
import glob

gdelt_base_url = 'http://data.gdeltproject.org/events/'

# Get the list of all the links on the gdelt file page
page = requests.get(gdelt_base_url+'index.html')
doc = lh.fromstring(page.content)
link_list = doc.xpath("//*/ul/li/a/@href")

# separate out those links that begin with four digits
file_list = [x for x in link_list if str.isdigit(x[0:4])]

# preview the list
print(file_list[0:5])

# Input Data
# geo-fence
lt1 = 43.403221
lt2 = 43.855401
lg1 = -79.639319
lg2 = -78.905820

# days back to process
days_back = 90

# Extract Relevant GDELT Rows
infilecounter = 0

dir_path = os.getcwd()
print('Working dir: ' + dir_path)

# make some dirs
local_path = dir_path + '\\data\\'
if not os.path.exists(local_path + 'gdelt-zips'):
    os.makedirs(local_path + 'gdelt-zips')
if not os.path.exists(local_path + 'gta-gdelt-data'):
    os.makedirs(local_path + 'gta-gdelt-data')

for compressed_file in file_list[infilecounter:]:
    print('gdelt-zips\\' + compressed_file),

    # if we dont have the compressed file stored locally, go get it. Keep trying if necessary.
    while not os.path.isfile(local_path + 'gdelt-zips\\' + compressed_file):
        print('...downloading,'),
        urllib.request.urlretrieve(url=gdelt_base_url + compressed_file,
                                   filename=local_path + 'gdelt-zips\\' + compressed_file)

    # extract the contents of the compressed file to a temporary directory
    print('...extracting,'),
    z = zipfile.ZipFile(file=local_path + 'gdelt-zips\\' + compressed_file, mode='r')
    z.extractall(path=local_path + 'tmp/')

    # parse each of the csv files in the working directory,
    print('...parsing,'),
    for infile_name in glob.glob(local_path + 'tmp/*'):

        # create only new files
        fdate = compressed_file.split(".")[0]
        fname ='gta.' + fdate + '.tsv'
        outfile_name = local_path + 'gta-gdelt-data\\' + fname
        if os.path.exists(outfile_name):
            continue

        # open the infile and outfile
        with open(infile_name, mode='r', encoding="utf8") as infile, \
                open(outfile_name, mode='w', encoding="utf8") as outfile:

            for line in infile:
                vals = line.split('\t')

                # extract geo-coordinates
                try:
                    lat = float(vals[53])  # ActionGeo_Lat
                    long = float(vals[54])  # ActionGeo_Long
                except Exception as e:
                    # means no coordinates provided, skipping
                    continue

                # only use events inside geo-fence
                if long >= lg1 and long <= lg2 and lat >= lt1 and lat <= lt2:
                    outfile.write(line)

        # delete the temporary file
        os.remove(infile_name)

    infilecounter += 1
    if infilecounter >= days_back:
        print('done')
        break