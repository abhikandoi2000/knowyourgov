from flask import Flask, url_for, render_template, request, make_response
from string import capwords

import models, config

app = Flask('knowyourgov')
app.config.from_object(config)
app.jinja_env.filters['capwords'] = capwords

from knowyourgov import routes