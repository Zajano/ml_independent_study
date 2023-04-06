If no interaction with the code is desired, the html files within 'model generation' will allow for
browsing through the code and its comments

In order to interact or adjust code, Jupyter must be installed on the machine
(numerous sources and installation options available, pick your favorite)

OR - visit https://cocalc.com/ to use a free online Jupyter environment. 
To save changes, you may need to create an account
From the home page, select the 'Jupyter' tab and then 'run Jupyter now'
Once you see the, 'Select a kernel' pages select the "+ New" tab
On the bottom of this tab you will see a "drop files to upload" (or click to select them from your computer)
after doing this, you can click 'close' and the files will be available for you to browse through and execute!

Note that each cell may need to have the cells above it run to initialize necessary variables or import modules

The video walkthrough goes there the details of each cell in the project, to be adjusted as desired
The model files in "project continuance" are the work-in-progress models for a more raw view of the project being worked on
the model files in "model generation" were cleaned for an easier browsing experience, and are the ones used for the PDFs

the actual models are within the "models" directory of their respective host directory.
Their naming convention is:
[type of model]_[descriptor]_[accuracy]

where 
'type of model' is either a Decision Tree Classifier (dtc) or Random Forest Regression (rfr)

'descriptors' are 
'test' (used in examples for video), 
'all' (a more thorough inclusion of data in training), 
'limited' (targeted to limited selection of specified column), 
and 'true' (most truthful accuracy accounting for inflation by techhniques used on the frame)

And 'accuracy' is the reported accuracy of the chosen method for evaluation