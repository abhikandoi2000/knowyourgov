from flask import Flask, url_for, render_template, request, make_response

from knowyourgov import models, config

app = Flask('knowyourgov')
app.config.from_object(config)

from knowyourgov import routes