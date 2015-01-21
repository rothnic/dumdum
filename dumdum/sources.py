__author__ = 'rothnic'

from core import DataSource

# Create datasource for RDatasets to retrieve any csv file provided
RDatasets = DataSource(url='http://vincentarelbundock.github.io/Rdatasets/datasets.html',
                       req_str='csv',
                       prefix='http://vincentarelbundock.github.io/Rdatasets/')
