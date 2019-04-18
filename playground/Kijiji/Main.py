import subprocess

#subprocess.call(" python3 kijijiscr.py " + "https://www.kijiji.ca/b-for-rent/gta-greater-toronto-area/c30349001l1700272 -f kijiji_1.txt", shell=True)


#for i in range(1,100):
    #subprocess.call(" python3 kijijiscr.py " + "https://www.kijiji.ca/b-for-rent/gta-greater-toronto-area/page-"+str(i)+"/c30349001l1700272 -f kijiji_1.txt", shell=True)

#subprocess.call(" python Kijiji-Scraper.py " + "https://www.kijiji.ca/b-for-rent/gta-greater-toronto-area/c30349001l1700272 -f kijiji_GTA.txt", shell=True)
#for i in range(2,100):
    #subprocess.call(" python Kijiji-Scraper.py " + "https://www.kijiji.ca/b-for-rent/gta-greater-toronto-area/page-"+str(i)+"/c30349001l1700272 -f kijiji_GTA.txt", shell=True)


#subprocess.call(" python Kijiji-Scraper.py " + "https://www.kijiji.ca/b-for-rent/gta-greater-toronto-area/basement-for-rent/k0c30349001l1700272?origin=ps -f kijiji_GTA_basement.txt", shell=True)
#for j in range(2,100):
    #print(j)
    #subprocess.call(" python Kijiji-Scraper.py " + "https://www.kijiji.ca/b-for-rent/gta-greater-toronto-area/basement-for-rent/page-"+str(j)+"/k0c30349001l1700272 -f kijiji_GTA_basement.txt", shell=True)


#subprocess.call(" python kijijiscr.py " + "https://www.kijiji.ca/b-for-rent/gta-greater-toronto-area/apartment/k0c30349001l1700272?origin=ps -f kijiji_GTA_apt.txt", shell=True)
#for m in range(2,100):
    #print(m)
    #subprocess.call(" python kijijiscr.py " + "https://www.kijiji.ca/b-for-rent/gta-greater-toronto-area/apartment/page-"+str(m)+"/2/k0c30349001l1700272 -f kijiji_GTA_apt.txt", shell=True)

#subprocess.call(" python Kijiji-Scraper.py " + "https://www.kijiji.ca/b-for-rent/gta-greater-toronto-area/house-for-rent/k0c30349001l1700272?origin=ps -f kijiji_GTA_house.txt", shell=True)
#for n in range(2,100):
    #print(n)
    #subprocess.call(" python Kijiji-Scraper.py " + "https://www.kijiji.ca/b-for-rent/gta-greater-toronto-area/house-for-rent/page-"+str(n)+"/2/k0c30349001l1700272 -f kijiji_GTA_house.txt", shell=True)


#subprocess.call(" python Kijiji-Scraper.py " + "https://www.kijiji.ca/b-for-rent/gta-greater-toronto-area/1-bedroom-apartment/k0c30349001l1700272?origin=ps -f kijiji_GTA_one_bed.txt", shell=True)
#for o in range(2,100):
    #print(o)
    #subprocess.call(" python Kijiji-Scraper.py " + "https://www.kijiji.ca/b-for-rent/gta-greater-toronto-area/1-bedroom-apartment/page-"+str(o)+"/2/k0c30349001l1700272 -f kijiji_GTA_one_bed.txt", shell=True)

subprocess.call(" python Kijiji-Scraper.py " + "https://www.kijiji.ca/b-for-rent/gta-greater-toronto-area/2-bedroom-apartment/k0c30349001l1700272?origin=ps -f kijiji_GTA_two_bed.txt", shell=True)
for p in range(2,100):
    print(p)
    subprocess.call(" python Kijiji-Scraper.py " + "https://www.kijiji.ca/b-for-rent/gta-greater-toronto-area/2-bedroom-apartment/page-"+str(p)+"/2/k0c30349001l1700272 -f kijiji_GTA_two_bed.txt", shell=True)
