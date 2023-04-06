USAGE INSTRUCTIONS FOR bgg_graphs.py

The files used for the final products, and described in the report, are in the folder "final files"

"progress files" contains an unorganized array of files that were used throughout the quarter
to help me learn and become familiar with the tools and data I was using. There are comments
if the files, but there is no defined usage for them.

"graphs" contains png files of the graphsultimately chosen for generation, as well as their
oddly behaving counterparts used in the examples of the report. 

IF DATA COLLECTION IS DESIRED:

There are 3 data gathering methods to select from: driver_scraping.py, API_scraping.py, and combined.py
	-It is recommended to use “API_scraping” as it is the most reliable as well as the fastest method. 
	-“driver_scraping” is capable of collecting page views and number of fans, but cannot filter out game expansions
	-“Combined_scraping” attempts to use both methods to gather data that either one could not alone

BEFORE running data collection, the user must edit the variables at the top of the selected file 
(in the "DEFINE FOR PROGRAM USE" section) to choose how many games they wish to gather data on 
and the filename of the csv the data will be saved to. 

The data will automatically go into a file in the same directory as the chosen scraping file to run.

Depending on the method selected and how many gamems to collect, scraping will take anywhere from
several hours to infinity years.

USING BGG_GRAPHS.PY:

BEFORE being run the user must open the file and adjust the variables within the “Define for program use” section
From here set "want_display" and "want_file" to the appropriate value for the desired outcome.

If "want_display" is True, when a graph appears the user must decide what they will do with it 
(save or simply close out the window) before the program will continue. 

If "want_file" is True, then the user must also provide the path to where they want to save the graph images, 
or “graphs_loc” can be set to an empty string (“”) and the graph images will be saved into the same directory as bgg_graphs.py

Finally, the user must set the variable for each graph they want to generate to “True”. 

It has been observed that graph generation is perplexingly inconsistent on rare occasions, so if a graph looks “wrong” 
the program may simply need to be run again.

There are a few graphing functions that have started to be parameterized - arguments in main() are set to
generate the expected graphs (in Graphs folder), but other entries can be made to just see what happens.
Spoiler: it probably breaks the graphs. 


