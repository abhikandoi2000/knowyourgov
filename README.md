# know your government

Know your Government, entry for Google Cloud Developer Challenge

#Deploy URL
[https://gcdc2013-know-your-gov.appspot.com/](https://gcdc2013-know-your-gov.appspot.com/)

# Tech Stack

* Google App Engine
* Google Data Store
* Python
* Flask, Jinja2
* Google Maps API
* Google+ Signin
* Google News API
* Twitter API
* Alchemy Sentiment API
* Google Custom Search API

# Development

* Clone this repo (`git clone git@github.com:abhikandoi2000/knowyourgov.git`)
* Download [Python SDK](https://developers.google.com/appengine/downloads#Google_App_Engine_SDK_for_Python "Python SDK for Google App Engine") for Google App Engine
* Unzip the downloaded SDK
* Change directory to project directory (`cd ~/path/to/knowyourgov`)
* Run the application locally (`~/path/to/sdk/dev_appserver.py .`)
* Visit `http://localhost:8080/` using your browser to see it in action.

# Populating the datastore

A `GET` request to `/updatedb/politicians` will populate the database.

*Make sure that the website is up and running before you do so.*
