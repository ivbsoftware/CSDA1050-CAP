# CSDA1050-CAP
	
#Craigslist_Rental
	##-> Next Steps
	Time permitting I'd plan to take on the below items, in order of priority;
	-Convert maps to MTM and replot (for better visual)
	-Replot the maps with 1,2,3,etc bedroom data separately. 
	-attempt to pull full title and description (using stored listing URLS);
		does sentiment affect rental price?
		is there a way to establish housing type? (basement / condo / house)
		can a bedroom count be inferred? (for missing data and studio vs 1 bedroom)
	-Use OSMnx to attempt to calculate distance to nearest transit stop - have to figure out how to do this
	-Incorporate average income by neighborhood
		census data from https://www12.statcan.gc.ca/wds-sdw/cpr2016-eng.cfm
		census tract to postal code (https://www150.statcan.gc.ca/n1/en/catalogue/92-154-G) - though this seems to be a paid data source now, 
		listing lat/lon to postalcode (need to find resource)
	-build a model to see if rental price can be predicted given the factors;
		-bedroom
		-Lat/long
		-area
		-listing sentiment
		-average income in area
		-distance to closest transit stop