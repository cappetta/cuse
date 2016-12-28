# Road Ratings Data Dictionary
This dataset was built and is maintained by the Department of Public Works’ street repair division. Over
the course of two years, every street in the city is rated based on a 1-10 scale.

# Definitions
* block – Block number for the street segment
* streetName – Street Name for the street segment
* streetType – Type of street:
    * AVE, BLVD, CIR, CT, DR, LN, PARK, PKWY, PL, RD, ST, TER,
* streetDirection – Direction of the street, if applicable:
    * N,S,E,W
* overall – The overall condition rating is considered completely subjective unless firm standards prove otherwise.  There is a scale of 1-10 where 10 is a newly paved road.  Below a 5 is considered a candidate for reconstruction.
* crack – A subjective sub-category, based on the amount and severity of the cracking. Scale of 1-5 with 5 indicating no cracking.
* patch – A rating subcategory, based on frequency and condition of utility cuts and patches. Scale of 1-5 with 5 indicating no patches.
* length – Length of the road in feet
* width – Width of the road in feet
* dateRated – Last date the road was rated
* dateLastOverlay – Date of last overlay, when the street was most recently paved. If blank, there is no record of paving having been performed since 1985.
* class – Class type of road:
    * PA: Principal Arterial
    * MA: Minor Arterial
    * CO: Collector
    * Local
* pavement – Pavement type
    * 6: street with curbs and at least 3 inches of asphalt over a concrete base
    * 4: street with full-depth asphalt (at least 7 inches) but without a concrete base or curbs
    * 3: street with no curbs, no improved sub base, and 3 inches or less of asphalt. These streets are almost always residential streets.
* flushOil– Flushing/Oiling. 
    * Context: There are 2 City ordinances that tax property owners for street maintenance: the flushing ordinance identifies the “improved “ streets (those having curbs) which will be flushed and swept. The oiling ordinance identifies Unimproved streets (those without curbs) which will receive a slurry seal at 4 year intervals.
* streetID – Street ID for each segment of roads. This can be joined with pothole data and street shapefile data.


* DataSets are located in the data folder