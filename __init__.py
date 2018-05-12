# -*- coding: utf-8 -*-

from CTFd.plugins import register_plugin_assets_directory, challenges, keys
from CTFd.plugins.keys import get_key_class
from CTFd.models import db, Solves, WrongKeys, Keys, Challenges, Files, Tags, Teams
from CTFd import utils
from CTFd.utils import admins_only, is_admin
import json
import datetime
from flask import jsonify, session, request
from flask_sqlalchemy import SQLAlchemy
import sys

# REC FUTURE : Désolé pour les commentaires en anglais-français.


class IntermediateFlagChallengeModel(Challenges):
    __mapper_args__ = {'polymorphic_identity': 'intermediateflagchallenge'}
    id = db.Column(None, db.ForeignKey('challenges.id'), primary_key=True)

    def __init__(self, name, description, value, category, type='intermediateflagchallenge'):
        self.name = name
        self.description = description
        self.value = value
        self.category = category
        self.type = type


class IntermediateFlagPartialSolve(db.Model):
    __table_args__ = (db.UniqueConstraint('chalid', 'teamid'), {})
    id = db.Column(db.Integer, primary_key=True)
    chalid = db.Column(db.Integer, db.ForeignKey('challenges.id'))
    teamid = db.Column(db.Integer, db.ForeignKey('teams.id'))
    ip = db.Column(db.String(46))
    flags = db.Column(db.Text)
    date = db.Column(db.DateTime, default=datetime.datetime.utcnow)
#    team = db.relationship('Teams', foreign_keys="Solves.teamid", lazy='joined')
#    chal = db.relationship('Challenges', foreign_keys="Solves.chalid", lazy='joined')


    def __init__(self, teamid, chalid, ip, flags):
        self.ip = ip
        self.chalid = chalid
        self.teamid = teamid
        self.flags = flags


    def __repr__(self):
        return '<solve {}, {}, {}, {}>'.format(self.teamid, self.chalid, self.ip, self.flags)


class IntermediateFlagChallenge(challenges.CTFdStandardChallenge):

    id = 'intermediateflagchallenge'
    name = 'intermediateflagchallenge'

    templates = {  # Handlebars templates used for each aspect of challenge editing & viewing
        'create': '/plugins/CTFd-intermediate-flag-plugin/challenge-assets/interm-challenge-create.njk',
        'update': '/plugins/CTFd-intermediate-flag-plugin/challenge-assets/interm-challenge-update.njk',
        'modal': '/plugins/CTFd-intermediate-flag-plugin/challenge-assets/interm-challenge-modal.njk',
    }
    scripts = {  # Scripts that are loaded when a template is loaded
        'create': '/plugins/CTFd-intermediate-flag-plugin/challenge-assets/interm-challenge-create.js',
        'update': '/plugins/CTFd-intermediate-flag-plugin/challenge-assets/interm-challenge-update.js',
        'modal': '/plugins/CTFd-intermediate-flag-plugin/challenge-assets/interm-challenge-modal.js',
    }


    @staticmethod
    def create(request):
        """
        This method is used to process the challenge creation request.
        :param request:
        :return:
        """
        files = request.files.getlist('files[]')

        # Liste de tuples de 3 éléments :
        #  - solution (le flag à trouver)
        #  - type ("static" ou "regex")
        #  - data (JSON string)
        keys = []
        index_key = 0

        while ('key_solution[%s]' % index_key) in request.form:
            key_solution = request.form['key_solution[%s]' % index_key]

            if key_solution:

                key_type = request.form.get('key_type[%s]' % index_key, '')
                if key_type not in ('static', 'regex'):
                    key_type = 'static'

                award = request.form.get('award_interm[%s]' % index_key, 0)
                try:
                    award = int(award)
                except ValueError:
                    award = 0

                congrat_msg = request.form.get('congrat_msg[%s]' % index_key, '')
                congrat_img_url = request.form.get('congrat_img_url[%s]' % index_key, '')
                doc_url = request.form.get('doc_url[%s]' % index_key, '')

                key_data = {
                    'congrat_msg': congrat_msg,
                    'congrat_img_url': congrat_img_url,
                    'doc_url': doc_url,
                    'award': award,
                }
                key_data = json.dumps(key_data)

                key_infos = (key_solution, key_type, key_data)
                keys.append(key_infos)

            index_key += 1

        # Create challenge
        chal = IntermediateFlagChallengeModel(
            name=request.form['name'],
            description=request.form['description'],
            value=request.form['value'],
            category=request.form['category'],
            type=request.form['chaltype']
        )

        chal.hidden = 'hidden' in request.form
        max_attempts = request.form.get('max_attempts')
        if max_attempts and max_attempts.isdigit():
            chal.max_attempts = int(max_attempts)

        db.session.add(chal)
        db.session.commit()

        for key_solution, key_type, key_data in keys:
            record_key = Keys(chal.id, key_solution, key_type)
            record_key.data = key_data
            db.session.add(record_key)

        db.session.commit()

        for f in files:
            utils.upload_file(file=f, chalid=chal.id)

        db.session.commit()
        db.session.close()


    @staticmethod
    def read(challenge):
        """
        This method is in used to access the data of a challenge in a format processable by the front end.
        :param challenge:
        :return: Challenge object, data dictionary to be returned to the user
        """
        data = {
            'id': challenge.id,
            'name': challenge.name,
            'value': challenge.value,
            'description': challenge.description,
            'category': challenge.category,
            'hidden': challenge.hidden,
            'max_attempts': challenge.max_attempts,
            'type': challenge.type,
            'type_data': {
                'id': IntermediateFlagChallenge.id,
                'name': IntermediateFlagChallenge.name,
                'templates': IntermediateFlagChallenge.templates,
                'scripts': IntermediateFlagChallenge.scripts,
            }
        }
        return challenge, data


    @staticmethod
    def update(challenge, request):
        """
        This method is used to update the information associated with a challenge. This should be kept strictly to the
        Challenges table and any child tables.
        :param challenge:
        :param request:
        :return:
        """
        sys.stdout.flush()
        challenge.name = request.form['name']
        challenge.description = request.form['description']
        challenge.value = int(request.form.get('value', 0)) if request.form.get('value', 0) else 0
        challenge.max_attempts = int(request.form.get('max_attempts', 0)) if request.form.get('max_attempts', 0) else 0
        challenge.category = request.form['category']
        challenge.hidden = 'hidden' in request.form
        db.session.commit()
        db.session.close()


    @staticmethod
    def delete(challenge):
        """
        This method is used to delete the resources used by a challenge.
        :param challenge:
        :return:
        """
        WrongKeys.query.filter_by(chalid=challenge.id).delete()
        Solves.query.filter_by(chalid=challenge.id).delete()
        Keys.query.filter_by(chal=challenge.id).delete()
        files = Files.query.filter_by(chal=challenge.id).all()
        for f in files:
            utils.delete_file(f.id)
        Files.query.filter_by(chal=challenge.id).delete()
        Tags.query.filter_by(chal=challenge.id).delete()
        Challenges.query.filter_by(id=challenge.id).delete()
        IntermediateFlagPartialSolve.query.filter_by(chalid=challenge.id).delete()
        IntermediateFlagChallengeModel.query.filter_by(id=challenge.id).delete()
        db.session.commit()


    @staticmethod
    def attempt(chal, request):
        """
        This method is used to check whether a given input is right or wrong. It does not make any changes and should
        return a boolean for correctness and a string to be shown to the user.
        In fact it does make changes, but only in a specific table of the plugin : IntermediateFlagPartialSolve.
        It is also in charge of parsing the user's input from the request itself.
        :param chal: The Challenge object from the database
        :param request: The request the user submitted
        :return: (boolean, string)
        """

        provided_key = request.form['key'].strip()
        chal_keys = Keys.query.filter_by(chal=chal.id).all()
        teamid = Teams.query.filter_by(id=session['id']).first().id
        chalid = request.path.split('/')[-1] # REC TODO : renommer la variable. (et celle d'avant aussi)
        partial = IntermediateFlagPartialSolve.query.filter_by(teamid=teamid, chalid=chalid).first()

        if not partial:
            # There is no record in "partial", concerning this team and this challenge. Must create one.
            keys = {}
            for chal_key in chal_keys:
                keys[str(chal_key.id)] = False
            flags = json.dumps(keys)
            psolve = IntermediateFlagPartialSolve(teamid=teamid, chalid=chalid, ip=utils.get_ip(req=request), flags=flags)
            db.session.add(psolve)
            db.session.commit()

        for chal_key in chal_keys:
            # REC FUTURE : Si il y a deux fois le même flag intermédiaire. On ne peut pas résoudre le challenge,
            # car c'est la première clé partielle qui sera mise et remise à True à chaque fois. Eh bien osef.
            if get_key_class(chal_key.type).compare(chal_key.flag, provided_key):
                db.session.expunge_all()
                partial = IntermediateFlagPartialSolve.query.filter_by(teamid=teamid, chalid=chalid).first()
                keys = json.loads(partial.flags)
                keys[str(chal_key.id)] = True
                partial.flags = json.dumps(keys)
                db.session.commit()
                return True, 'Correct'

        return False, 'Incorrect'


    @staticmethod
    def solve(team, chal, request):
        """
        This method is used to insert Solves into the database in order to mark a challenge as solved.
        :param team: The Team object from the database
        :param chal: The Challenge object from the database
        :param request: The request the user submitted
        :return:
        """
        teamid = Teams.query.filter_by(id=session['id']).first().id
        chalid = request.path.split('/')[-1]
        provided_key = request.form['key'].strip()
        db.session.expunge_all()
        partial =  IntermediateFlagPartialSolve.query.filter_by(teamid=teamid, chalid=chalid).first()
        keys = json.loads(partial.flags)

        for key, solved in keys.iteritems():
            if not solved:
                return

        db.session.expunge_all()
        solve = Solves(teamid=teamid, chalid=chalid, ip=utils.get_ip(req=request), flag=provided_key)
        db.session.add(solve)
        db.session.commit()
        db.session.close()


    @staticmethod
    def fail(team, chal, request):
        """
        This method is used to insert WrongKeys into the database in order to mark an answer incorrect.
        :param team: The Team object from the database
        :param chal: The Challenge object from the database
        :param request: The request the user submitted
        :return:
        """
        chalid = request.path.split('/')[-1]
        teamid = Teams.query.filter_by(id=session['id']).first().id
        provided_key = request.form['key'].strip()
        wrong = WrongKeys(teamid=teamid, chalid=chalid, ip=utils.get_ip(request), flag=provided_key)
        db.session.add(wrong)
        db.session.commit()
        db.session.close()


def load(app):
    challenges.CHALLENGE_CLASSES['intermediateflagchallenge'] = IntermediateFlagChallenge
    register_plugin_assets_directory(app, base_path='/plugins/CTFd-intermediate-flag-plugin/challenge-assets/')
    app.db.create_all()


    @app.route('/admin/interm_flags_config/<int:chalid>')
    @admins_only
    def interm_flags_config(chalid):
        chal_keys = Keys.query.filter_by(chal=chalid).all()
        keys_infos = {}
        for key in chal_keys:
            key_info = json.loads(key.data)
            key_info['key_type'] = key.type
            keys_infos[key.id] = key_info
        return jsonify(keys_infos)


    def admin_keys_view(keyid):

        if request.method == 'GET':
            if keyid:
                saved_key = Keys.query.filter_by(id=keyid).first_or_404()
                key_class = get_key_class(saved_key.type)
                json_data = {
                    'id': saved_key.id,
                    'key': saved_key.flag,
                    'data': saved_key.data,
                    'chal': saved_key.chal,
                    'type': saved_key.type,
                    'type_name': key_class.name,
                    'templates': key_class.templates,
                }
                return jsonify(json_data)

        elif request.method == 'POST':
            chal = request.form.get('chal')
            flag = request.form.get('key')
            key_type = request.form.get('key_type')
            if not keyid:
                k = Keys(chal, flag, key_type)
                db.session.add(k)
            else:
                k = Keys.query.filter_by(id=keyid).first()
                k.flag = flag
                k.type = key_type
            db.session.commit()
            db.session.close()
            return '1'

    app.view_functions['admin_keys.admin_keys_view'] = admin_keys_view

