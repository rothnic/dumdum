__author__ = 'rothnic'

import pandas as pd
import urllib2
import lxml.html
import types


class DataSource(object):
    """Contains a method to get a dataframe for each dataset on page."""

    def __init__(self, url, req_str=None, prefix=None):
        """Initializes the methods from provided url.

        :param url: url for page with datasets
        :param req_str: required substring, used for file extensions
        :param prefix: url prefix to add to links, if required
        :return: None
        """
        self.url = url
        links = get_all_links(url, req_str)

        if prefix:
            links = [prefix + link for link in links]

        # add method for each dataset
        for link in links:

            # format name
            this_name = link.split("/")[-1]
            if '.' in this_name:
                this_name = this_name.split(".")[0]

            # add the method
            func = gen_web_source(this_name, link)
            self.__dict__[func.__name__] = types.MethodType(func, self)


def gen_web_source(source_name, url):
    """Creates a function to return pandas df for the data source info.

    :param source_name: name of the dataset, valid function name
    :param url: url to load
    :return: pandas dataframe
    """

    assert(isinstance(source_name, str))

    # create function name as get and the source name
    name = 'get_' + source_name

    def func(self):
        return pd.read_csv(url)

    func.__name__ = name

    return func


def get_all_links(url, req_str=None):
    """Returns all links from given url, with optional substring they must contain

    :param url: url for webpage with links to data
    :param req_str: substring required, can be used for file extensions
    :return: list of link strings
    """

    # connect to a URL
    website = urllib2.urlopen(url)
    html = website.read()

    links = lxml.html.parse(url).xpath("//a/@href")

    if req_str:
        links = [link for link in links if req_str in link]

    return links