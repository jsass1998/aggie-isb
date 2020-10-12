required libraries:
	pip3 install apiclient
	pip3 install httplib2
	pip3 install selenium
	pip3 install openpyxl
	pip3 install geckodriver #pretty sure this handles the automated firefox, but I didn't look into it and didn't touch
	pip3 install PyPDF2

required installations:
	firefox product v18.05 was used, use older at risk

troubleshooting:
	had an issue with selenium and had to run this -> pip3 install --upgrade google-api-python-client google-auth-httplib2 google-auth-oauthlib
	gecko needs to be added to environmental path variables -> restart PC
	
directory heirarchy:

	|HOME
	|
	|
	|---CreateDB[PY]
	|---downloadPDFs[PY]
	|---main[PY]
	|---README[TXT]
	|(Created Folders/Files Below)
	|~~~__pycache__
	|~~~geckodriver[TXT]
	|~~~GradeDistributionsDB
	|~~~~~~~[semester][year] #note that 2015 was earliest accessible data
	|~~~~~~~~~~[CSV_Files][college]
	|~~~~~~~~~~~~~[CLEAN_][college][semester][year][CSV] #cleaned but not formatted, you can comment out the cleanup and uncomment the delete statement to remove
	|~~~~~~~~~~~~~[DIRTY_][college][semester][year][TXT] #raw data, you can comment out the cleanup and uncomment the delete statement to remove
	|~~~~~~~~~~~~~[formatted_][CLEAN_][college][semester][year][CSV] #formatted and cleaned, this is the data you want to keep
	|~~~~~~~~~~[GRADE][year][semester (1,2,3)][college][PDF]

running instructions (python file):
	once required libraries are present on computer use below command, no input commands required.
	python main.py

running instructions (executable):
	navigate to HOME->dist and run main
	
error codes:
	PDFReader exception caught: [FILENAME] --- the data you requested could not be retrieved, means the file cant be accessed by the downloadPDFs.py file, I tried
		my best to negate this error but there are certain cases (3) where the records must not be publicly available.