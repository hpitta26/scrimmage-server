from flask import render_template, request, session, redirect, url_for

from scrimmage import app, db
from scrimmage.decorators import admin_required
from scrimmage.models import Team

@app.route('/admin/teams', methods=['GET'])
@admin_required
def admin_teams():
  teams = Team.query.all()
  return render_template('admin/teams.html', teams=teams)

@app.route('/admin/teams/create', methods=['POST'])
@admin_required
def admin_teams_create():
  team_name = request.form['team_name']
  team = Team(team_name)
  db.session.add(team)
  db.session.commit()
  return redirect(url_for('admin_teams'))

@app.route('/admin/team/<int:team_id>/delete', methods=['POST'])
@admin_required
def admin_team_delete(team_id):
  team = Team.query.get(team_id)
  db.session.delete(team)
  db.session.commit()
  return redirect(url_for('admin_teams'))
