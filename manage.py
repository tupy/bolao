# -*- coding:utf-8 -*-

from flask.ext import script
from flask.ext.script import Command

from bolao.database import create_all, drop_all

class CreateDB(Command):
    """
    Creates database using SQLAlchemy
    """

    def run(self):
        drop_all()
        create_all()
        self.populate()

    def populate(self):

      import json
      import datetime

      from bolao.database import db
      from bolao.models import Game, Team 
      
      def find_team(name, alias):
        team = Team.query.filter_by(alias=alias).first()
        if not team:
           team = Team(name=name, alias=alias)
           db.session.add(team)
        return team
      
      data = open('games.json')
      for _game in json.load(data):


        team1 = find_team(_game['team1'], _game['alias_team1'])
        team2 = find_team(_game['team2'], _game['alias_team2'])

        game = Game()
        game.team1 = team1
        game.team2 = team2
        game.time = datetime.datetime.strptime(_game['date'], '%Y-%m-%d')
        game.place = _game['place']
        game.round = _game['round']
        game.group = _game['group']

        db.session.add(game)
        db.session.commit()         
      

class DropDB(Command):
    """
    Drops database using SQLAlchemy
    """

    def run(self):
        drop_all()


if __name__ == "__main__":
    from bolao.main import app_factory

    manager = script.Manager(app_factory)
    manager.add_option("-c", "--config", dest="config", required=False, default='Dev')
    manager.add_command("create_db", CreateDB())
    manager.add_command("drop_db", DropDB())
    manager.run()
