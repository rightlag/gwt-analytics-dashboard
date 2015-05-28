# gwt-analytics-dashboard

This repository contains the `0.0.0` release of the gwt-analytics-dashboard.

# Purpose
The purpose of this application is to report all crawl related errors in a simple and easy to use interface.

# Setting up

It is advised that you create a virtual environment before installing any Python dependencies. This can be done by executing:

    $ virtualenv venv
    $ source venv/bin/activate

Once you have your virtual environment installed and configured, you can complete the cloning process:

    $ git clone https://<username>@bitbucket.org/delphicdigital/gwt-analytics-dashboard.git
    $ cd gwt-analytics-dashboard
    $ pip install -r requirements.txt
    $ bower install

# Configuration
To successfully run the application, you must first configure the `app.py` module.

The following variables must be modified:

| Key           | Value                |
|---------------|----------------------|
| CLIENT_ID     | Google Client ID     |
| CLIENT_SECRET | Google Client Secret |
| REDIRECT_URI  | Google Redirect URI  |

These credentials can be obtained from the [Google Developers Console](https://console.developers.google.com)

A getting started guide can be found [here](https://developers.google.com/webmaster-tools/v3/prereqs)

# Running the server
Run the server by executing `python app.py`

# To-do
- Implement pagination
- Create unit tests