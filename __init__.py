# -*- coding: utf-8 -*-

from CTFd.plugins import register_plugin_assets_directory, challenges, keys
from CTFd.plugins.keys import get_key_class
from CTFd.models import db, Solves, WrongKeys, Keys, Challenges, Files, Tags, Teams, Awards
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


class IntermediateAwardHandler():
    """
    Handle the relations between the CTFd Awards and the winnings of Intermediate Flags.
    An Award specific to this plugin is called "interm-awards".

    award formatting of the field 'name' : plugin_intermflag_{chal_id}_{key_id}
    """

    # REC FUTURE : the key_id are publicly shown to the team. They may extrapolate the number of intermediate flags to obtain.
    # We don't care about that for the moment.

    def __init__(self, chal_id, team_id):
        self.chal_id = chal_id
        self.team_id = team_id
        self.dict_chal_keys = None


    def _init_dict_chal_keys(self):
        """
        Initializes self.dict_chal_keys, with all the keys of the challenge.
        self.dict_chal_keys is a dict with :
         - key : key_id (primary key of the Key) (that makes three times the word "key", not my fault).
         - value : Key. Object returned by a sqlalchemy query, of the DB table Key.
        """
        # Gets all key definitions
        chal_keys = Keys.query.filter_by(chal=self.chal_id).all()
        self.dict_chal_keys = {
            chal_key.id:chal_key
            for chal_key in chal_keys }


    def _award_infos(self, award_name):
        if self.dict_chal_keys is None:
            raise Exception("self.dict_chal_keys is None. Not supposed to happen.")
        award_name_details = award_name.split('_')
        if len(award_name_details) < 3:
            return None
        _, __, chal_id, chal_key_id = award_name_details
        try:
            chal_id = int(chal_id)
            chal_key_id = int(chal_key_id)
        except ValueError:
            return None
        if chal_id != self.chal_id:
            # Not supposed to happen.
            return None
        chal_key = self.dict_chal_keys.get(chal_key_id)
        if chal_key is None:
            return None
        chal_key_info = json.loads(chal_key.data)
        return {
            'key_id': chal_key_id,
            'chal': chal_key.chal,
            'type': chal_key.type,
            'congrat_msg': chal_key_info['congrat_msg'],
            'congrat_img_url': chal_key_info['congrat_img_url'],
            'doc_url': chal_key_info['doc_url'],
            'score': chal_key_info['award'],
            # REC TODO
            'public' : False,
            'cancel_score': False }


    def get_all(self):
        """
        Returns a list, sorted by date, of all the interm-awards won by all the teams, for this challenge.
        The data returned depends on the team_id.
        If an interm-award is won by the current team and by others, its description, icon and score will be returned.
        If an interm-award is won only by other teams, its description, icon and score will be hidden.
        If an interm-award is a 'public flag', its description, icon and score will always be returned.

        :return:
        a list of tuples :
         - interm-award id
         - date of earning
         - team name
         - original value (not set to null in case of keys with 'cancel points' checked)
         - interm-award text (or None)
         - interm-award icon (or None)
        """

        self._init_dict_chal_keys()

        # Gets award informations
        filter_award_name = 'plugin_intermflag_' + str(self.chal_id) + '_%'
        awards_query_result = db.session.query(
            Awards.id.label('award_id'), Awards.date, Awards.name.label('award_name'),
            Teams.id.label('team_id'), Teams.name.label('team_name')
        ).join(Teams).filter(Awards.name.like(filter_award_name)).order_by(Awards.date).all()

        # Joins award datas and key datas
        awards = [
            (award.award_id, award.date, award.team_id, award.team_name, self._award_infos(award.award_name))
            for award in awards_query_result
        ]
        awards = [
            award
            for award in awards
            if award[-1] is not None
        ]

        # Hides descrip, icon and scores that the team should not know.
        key_ids_of_team = [
            award_infos['key_id']
            for award_id, _, award_team_id, __, award_infos in awards
            if award_team_id == self.team_id ]
        for award in awards:
            award_id, _, award_team_id, __, award_infos = award
            if award_infos['key_id'] not in key_ids_of_team and not award_infos['public']:
                award_infos['congrat_msg'] = None
                award_infos['congrat_img_url'] = None
                award_infos['score'] = None

        # Removes unneeded fields
        awards = [
            (award_id, award_date, award_team_name, award_infos['congrat_msg'], award_infos['congrat_img_url'], award_infos['score'])
            for award_id, award_date, award_team_id, award_team_name, award_infos in awards ]
        return awards


    def add(self, chal_key):
        """
        Adds an award, corresponding to the chal_key in parameters.
        Does not check if an award for this chal_key and this team has already been given.
        It has to be done before.

        :chal_key: an object returned by a query on the Keys Model.
        """
        # REC FUTURE : check if the key in param is a key of the challenge.
        key_infos = json.loads(chal_key.data)
        award_score = key_infos['award']
        award_name = 'plugin_intermflag_%s_%s' % (self.chal_id, chal_key.id)
        award = Awards(teamid=self.team_id, name=award_name, value=award_score)
        award.description = "Plug-in intermediate flag. TODO fill that later."
        db.session.add(award)
        db.session.commit()


    def is_chal_solved(self):
        """
        Returns a boolean. True : the team obtained all the intermediate flags with a score positive or zero.
        (The "negative" flags are not compulsory).
        """

        self._init_dict_chal_keys()
        # Gets award informations
        filter_award_name = 'plugin_intermflag_' + str(self.chal_id) + '_%'
        awards_of_team = Awards.query.filter_by(teamid=self.team_id).filter(Awards.name.like(filter_award_name)).all()
        # Joins award datas and key datas
        awards = [
            self._award_infos(award.name)
            for award in awards_of_team
        ]
        awards = [ award for award in awards if award is not None ]
        # Builds two sets
        chal_key_ids_to_obtain = [
            chal_key_id for chal_key_id, chal_key_fields
            in self.dict_chal_keys.items()
            if json.loads(chal_key_fields.data)['award'] >= 0
        ]
        chal_key_ids_to_obtain = set(chal_key_ids_to_obtain)
        chal_key_ids_obtained = [ award['key_id'] for award in awards ]
        chal_key_ids_obtained = set(chal_key_ids_obtained)
        # The challenge is solved if the set of keys to obtain (all the positive keys) is included in the set of keys obtained.
        return chal_key_ids_to_obtain.issubset(chal_key_ids_obtained)


    # REC TODO toutes ces autres fonctions
    # get_mine
    # check(team, key)
    # set zeros(chal, team)
    # get authorized files (chal, team)


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

        # REC TODO : duplicate code (en partie) avec juste au-desus

        # Liste de tuples de 3 éléments :
        #  - id
        #  - solution (le flag à trouver) (en fait c'est vide)
        #  - type ("static" ou "regex")
        #  - data (JSON string)
        keys = []
        index_key = 0

        while ('key_id[%s]' % index_key) in request.form:
            key_id = request.form['key_id[%s]' % index_key]
            #key_solution = request.form['key_solution[%s]' % index_key]

            if key_id.isdigit():

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

                key_infos = (key_id, '', key_type, key_data)
                keys.append(key_infos)

            index_key += 1

        # REC FUTURE. Vérifier qu'on n'est en trait de modifier uniquement les flags du challenge passé en paramètre.
        # C'est une vérif facultative, puisque seul l'admin a le droit de faire cette action,
        # et les admins ont droit de modifier toutes les questions. (D'ailleurs c'est pas très pratique).
        record_keys = []
        for key_id, _, key_type, key_data in keys:
            record_key = Keys.query.filter_by(id=key_id).first()
            if record_key:
                record_key.type = key_type
                record_key.data = key_data
                record_keys.append(record_key)

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
        # REC TODO : nettoyer les awards.
        IntermediateFlagPartialSolve.query.filter_by(chalid=challenge.id).delete()
        IntermediateFlagChallengeModel.query.filter_by(id=challenge.id).delete()
        db.session.commit()


    @staticmethod
    def attempt(chal, request):
        """
        This method is used to check whether a given input is right or wrong. It does not make any changes and should
        return a boolean for correctness and a string to be shown to the user.
        In fact it does make changes : award attribution.
        It is also in charge of parsing the user's input from the request itself.
        :param chal: The Challenge object from the database
        :param request: The request the user submitted
        :return: (boolean, string)
        """

        provided_key = request.form['key'].strip()
        chal_keys = Keys.query.filter_by(chal=chal.id).all()
        team_id = Teams.query.filter_by(id=session['id']).first().id
        chal_id = request.path.split('/')[-1]

        for chal_key in chal_keys:
            # REC FUTURE : Si il y a deux fois le même flag intermédiaire, on ne peut pas résoudre le challenge,
            # car c'est la première clé partielle qui sera checkée à chaque fois. Eh bien osef.
            if get_key_class(chal_key.type).compare(chal_key.flag, provided_key):
                # REC TODO. un vrai check.
                if True:
                    print('REC TODO yop')
                    db.session.expunge_all()
                    interm_award_handler = IntermediateAwardHandler(chal_id, team_id)
                    interm_award_handler.add(chal_key)
                    return True, 'Correct'
                else:
                    return True, 'You already have this flag'

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
        team_id = Teams.query.filter_by(id=session['id']).first().id
        chal_id = request.path.split('/')[-1]
        try:
            chal_id = int(chal_id)
        except ValueError:
            return

        provided_key = request.form['key'].strip()
        db.session.expunge_all()

        interm_award_handler = IntermediateAwardHandler(chal_id, team_id)
        if not interm_award_handler.is_chal_solved():
            return

        db.session.expunge_all()
        # REC TODO : mettre à 0 les award qui doivent l'être.
        # REC FUTURE : La valeur "provided_key" n'est pas très significative. C'est le dernier flag intermédiaire obtenu pour valider le challenge.
        # Osef, un petit peu. Faudrait trouver le moyen de les stocker tous.
        solve = Solves(teamid=team_id, chalid=chal_id, ip=utils.get_ip(req=request), flag=provided_key)
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


    @app.route('/intermflags/awards_all/<int:chal_id>')
    def interm_flags_awards_all(chal_id):
        team_id = Teams.query.filter_by(id=session['id']).first().id
        interm_award_handler = IntermediateAwardHandler(chal_id, team_id)
        return jsonify(interm_award_handler.get_all())


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

