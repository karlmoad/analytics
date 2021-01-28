# Analytics

This repo contains a number of scripts and other artifacts that are attributed to various 
objectives within the Clinical Analytics project space.

Python 3 is utilized.

libraries utilized:
- pandas
- numpy
- pyPDF2
- pyYAML
- azure-ai-textanalytics


### create a config file for azure settings named **config.yaml** with the following contents:

`azure:
  endpoint: <endpoint uri>
  key: <api key>`

### create subdirectory **dumps** relative to the location of the code, the program will output the results to this directory