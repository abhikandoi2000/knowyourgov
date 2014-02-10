![Know Your Government](https://gcdc2013-know-your-gov.appspot.com/static/img/logo.png)

Know Your Government is an attempt to raise awareness about political leaders in India in common person. [Read more about the application](https://gcdc2013-know-your-gov.appspot.com/about)

This application was submitted for Google Cloud Developer Challenge and was amongone of the [finalists](http://www.google.com/events/gcdc2013/finalists.html) for India region

#Application Deploy URL
[https://gcdc2013-know-your-gov.appspot.com/](https://gcdc2013-know-your-gov.appspot.com/)

We know it's a bit long ;)

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
* Youtube API

# Development

* Clone this repo (`git clone git@github.com:abhikandoi2000/knowyourgov.git`)
* Download [Python SDK](https://developers.google.com/appengine/downloads#Google_App_Engine_SDK_for_Python "Python SDK for Google App Engine") for Google App Engine
* Unzip the downloaded SDK
* Change directory to project directory (`cd ~/path/to/knowyourgov`)
* Run the application locally (`~/path/to/sdk/dev_appserver.py .`)
* Visit `http://localhost:8080/` using your browser to see it in action.

# Populating the datastore

A `GET` request to `/updatedb/politicians` will populate the politician database.

A `GET` request to `/updatedb/csvdata` will add additional information about the politician from different sources.

A `GET` request to `/updatedb/partyinfo` will add information about major national political parties.

*Make sure that the website is up and running before you do so.*