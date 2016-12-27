import os

import boto3
from flask import g, redirect, render_template, request, url_for
from werkzeug.utils import secure_filename

from scrimmage import app, db
from scrimmage.decorators import team_required
from scrimmage.models import Bot, GameRequest, Game
from scrimmage.tasks import compile

@app.route('/team')
@team_required
def manage_team():
  settable_bots = [bot for bot in g.team.bots if bot.is_settable()]
  outgoing_requests = g.team.outgoing_requests()
  return render_template('manage_team.html', settable_bots=settable_bots, outgoing_requests=outgoing_requests)


@app.route('/team/games')
@team_required
def show_games():
  pagination = (Game.query.filter((Game.challenger_id == g.team.id) | (Game.opponent_id == g.team.id))
                          .order_by(Game.create_time.desc())
                          .paginate())
  return render_template('show_games.html', pagination=pagination)


@app.route('/team/create_bot', methods=['POST'])
@team_required
def create_bot():
  file = request.files['file']
  name = request.form['name']
  if len(file.filename) == 0 or not name:
    return ('', 204)

  name = secure_filename(name)
  key = os.path.join('bots', str(g.team.id), name)
  s3_client = boto3.client('s3')
  s3_client.put_object(Body=file, Bucket=app.config['S3_BUCKET'], Key=key)

  new_bot = Bot(g.team, name)
  db.session.add(new_bot)
  db.session.commit()
  compile.delay(new_bot.id)
  return redirect(url_for('manage_team'))


@app.route('/team/set_bot', methods=['POST'])
@team_required
def set_bot():
  bot_id = int(request.form['bot_id'])
  bot = Bot.query.get(bot_id)
  g.team.set_current_bot(bot)
  db.session.commit()
  return redirect(url_for('manage_team'))
