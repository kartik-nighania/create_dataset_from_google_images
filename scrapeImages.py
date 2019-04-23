# TO USE: python2 scrapeImages.py --search "cat" --num_images 10
# TO USE: python2 scrapeImages.py --filename 500celebs.txt --num_images 10 --list_count 500

from bs4 import BeautifulSoup
import requests
import re
import urllib2
import os
import argparse
import sys
import json

def get_soup(url,header):
    return BeautifulSoup(urllib2.urlopen(urllib2.Request(url,headers=header)),'html.parser')

def main(args):
	parser = argparse.ArgumentParser(description='Scrape Google images')
	parser.add_argument('-s', '--search', default='', type=str, help='search term')
	parser.add_argument('-n', '--num_images', default=10, type=int, help='num images to save')
    parser.add_argument('-i', '--list_count', default=1, type=int, help='number of lines to search in the textfile specified')
    parser.add_argument('-f', '--filepath', default='', type=str, help='location of text file having search list')
	args = parser.parse_args()

	#raw_input(args.search)
    query = args.search
	max_images = args.num_images
    file_directory = args.filepath
	image_type="Action"
	query= query.split()
	query='+'.join(query)
	url="https://www.google.co.in/search?q="+query+"&source=lnms&tbm=isch"
	header={'User-Agent':"Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/43.0.2357.134 Safari/537.36"}
	soup = get_soup(url,header)

    # file reader to open our txt file
    f = open(directory, "r")

    # create folder named dataset
    save_directory = os.path.join(os.getcwd(), 'dataset')
    os.mkdir(save_directory)

    for numberOfImages in range(int(list_count)):
        
        # create folder for the current search line - can have multiple images inside.
        folder_name = f.readline()
        folder_name.replace(' ', '_')
        save_directory = os.path.join(save_directory, folder_name)
        os.mkdir(save_directory)

        # contains the link for Large original images, type of  image
        ActualImages=[]
        for a in soup.find_all("div",{"class":"rg_meta"}):
            link , Type =json.loads(a.text)["ou"]  ,json.loads(a.text)["ity"]
            ActualImages.append((link,Type))
        for i , (img , Type) in enumerate( ActualImages[0:max_images]):
            try:
                req = urllib2.Request(img, headers={'User-Agent' : header})
                raw_img = urllib2.urlopen(req).read()
                if len(Type)==0:
                    f = open(os.path.join(save_directory , "img" + "_"+ str(i)+".jpg"), 'wb')
                else :
                    f = open(os.path.join(save_directory , "img" + "_"+ str(i)+"."+Type), 'wb')
                f.write(raw_img)
                f.close()
            except Exception as e:
                print "could not load : "+img
                print e
        
        # move one folder up for another image folder

if __name__ == '__main__':
    from sys import argv
    try:
        main(argv)
    except KeyboardInterrupt:
        pass
    sys.exit()
