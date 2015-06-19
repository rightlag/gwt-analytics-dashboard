import apiclient
import config
import flask
import httplib
import httplib2
import json

from apiclient import errors
from apiclient.discovery import build
from oauth2client import client
from flask.ext.triangle  import Triangle

app = flask.Flask(__name__)
Triangle(app)

HOST = '0.0.0.0'
PORT = 3000
CLIENT_ID = config.creds['CLIENT_ID']
CLIENT_SECRET = config.creds['CLIENT_SECRET']
OAUTH_SCOPES = [
    'https://www.googleapis.com/auth/webmasters.readonly',
]
REDIRECT_URI =  config.creds['REDIRECT_URI']

@app.route('/login')
def login():
    """Authenticate user via OAuth2 callback."""
    flow = client.OAuth2WebServerFlow(CLIENT_ID,
                                      CLIENT_SECRET,
                                      OAUTH_SCOPES,
                                      REDIRECT_URI,
                                      approval_prompt='force',
                                      access_type='offline')
    auth_uri = flow.step1_get_authorize_url()
    return flask.redirect(auth_uri)

@app.route('/oauth2callback')
def oauth2callback():
    """Generate OAuth2 callback redirect URL and redirect user to
    `index` route."""
    code = flask.request.args.get('code')
    if code:
        flow = client.OAuth2WebServerFlow(CLIENT_ID,
                                          CLIENT_SECRET,
                                          OAUTH_SCOPES)
        flow.redirect_uri = flask.request.base_url
        try:
            credentials = flow.step2_exchange(code)
        except client.FlowExchangeError, e:
            print e.message
        flask.session['credentials'] = credentials.access_token
    return flask.redirect(flask.url_for('index'))

@app.route('/sites', methods=['POST', 'GET'])
def sites():
    credentials = client.AccessTokenCredentials(
        flask.session.get('credentials'),
        'user-agent-value'
    )
    http = httplib2.Http()
    http = credentials.authorize(http)
    try:
        service = build('webmasters', 'v3', http=http)
        # Get all site URLs associated with account.
        sites = service.sites().list().execute()
        if not sites:
            # The current account does not have any sites associated
            # with it, redirect the user to the `index` route.
            return flask.render_template('index.html')
        site_urls = [site['siteUrl'] for site in sites.get('siteEntry')
                     if site['permissionLevel'] != 'siteUnverifiedUser']
        if flask.request.method == 'POST':
            # Cast HTTP request payload to a dictionary object and
            # check to ensure that the payload has content.
            data = json.loads(flask.request.data)
            if not data:
                res = flask.jsonify(message='category and platform required')
                res.status_code = httplib.BAD_REQUEST
                return res
            params = {
                'category': data.get('category', 'notFound'),
                'platform': data.get('platform', 'web'),
            }
        else:
            params = {
                'category': 'notFound',
                'platform': 'web',
            }
        sites = []
        for site_url in site_urls:
            site = {}
            site['siteUrl'] = site_url
            try:
                try:
                    urlCrawlErrorsCounts = (service
                                            .urlcrawlerrorscounts()
                                            .query(siteUrl=site_url, **params
                    ).execute()['countPerTypes'][0]['entries'][0]['count'])
                except KeyError, e:
                    # Site does not contain crawl errors - skip.
                    continue
                # Cast unicode to numeric value.
                urlCrawlErrorsCounts = int(urlCrawlErrorsCounts)
                if urlCrawlErrorsCounts > 0:
                    site['urlCrawlErrorsCounts'] = urlCrawlErrorsCounts
                    crawl_errors = service.urlcrawlerrorssamples().list(
                        siteUrl=site_url,
                        **params
                    ).execute()
                    # `urlCrawlErrorSample` key may not exist,
                    # therefore, use `get` method.
                    urlCrawlErrorsSamples = crawl_errors.get(
                        'urlCrawlErrorSample'
                    )
                    site['urlCrawlErrorsSamples'] = urlCrawlErrorsSamples
                    sites.append(site)
            except apiclient.http.HttpError, e:
                res = flask.jsonify(message=e._get_reason())
                res.status_code = int(e.resp['status'])
                return res
        return flask.jsonify(sites=sites)
    except client.AccessTokenCredentialsError, e:
        # The access token is expired or invalid and can't be refreshed,
        # redirect the user to the `login` route.
        res = flask.jsonify(message=e.message,
                            redirect=flask.url_for('login'))
        res.status_code = httplib.BAD_REQUEST
        return res

@app.route('/')
def index():
    try:
        credentials = client.AccessTokenCredentials(
            flask.session.get('credentials'),
            'user-agent-value'
        )
        return flask.render_template('index.html')
    except client.AccessTokenCredentialsError, e:
        return flask.redirect(flask.url_for('login'))

if __name__ == '__main__':
    app.secret_key = 'u%-?i`A+~i.o@Ps|h,9i/bl?|,s0TM2L7r.iLjwn;<O6*,ohr0@-+`t[-. -JX4h'
    app.run(host=HOST, port=PORT)
