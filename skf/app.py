#!/usr/bin/env python3

# -*- coding: utf-8 -*-
"""
    Security Knowledge Framework is an expert system application
    that uses OWASP Application Security Verification Standard, code examples
    and helps developers in development.
    Copyright (C) 2021 Glenn ten Cate, Riccardo ten Cate
    This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU Affero General Public License as
    published by the Free Software Foundation, either version 3 of the
    License, or (at your option) any later version.
    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU Affero General Public License for more details.
    You should have received a copy of the GNU Affero General Public License
    along with this program. If not, see <http://www.gnu.org/licenses/>.
"""
import logging.config, os, re
from flask import Flask, Blueprint
from flask_cors import CORS, cross_origin
from skf import settings
from flask_sqlalchemy import SQLAlchemy
from skf.chatbot_tools import init_dataset
from skf.db_tools import init_md_knowledge_base, init_md_code_examples, load_initial_data, clean_db, clear_db, update_db, init_db
from skf.api.labs.endpoints.lab_items import ns as lab_namespace
from skf.api.labs.endpoints.lab_deployments import ns as lab_namespace
from skf.api.labs.endpoints.lab_delete import ns as lab_namespace
#from skf.api.labs_code.endpoints.lab_code_random_item import ns as lab_code_namespace
#from skf.api.labs_code.endpoints.lab_code_verify import ns as lab_code_namespace
from skf.api.projects.endpoints.project_items import ns as project_namespace
from skf.api.projects.endpoints.project_delete import ns as project_namespace
from skf.api.projects.endpoints.project_new import ns as project_namespace
from skf.api.projects.endpoints.project_stats import ns as project_namespace
from skf.api.projects.endpoints.project_update import ns as project_namespace
from skf.api.projects.endpoints.project_item import ns as project_namespace
from skf.api.sprints.endpoints.sprint_item import ns as sprints_namespace
from skf.api.sprints.endpoints.sprint_delete import ns as sprints_namespace
from skf.api.sprints.endpoints.sprint_new import ns as sprints_namespace
from skf.api.sprints.endpoints.sprint_stats import ns as sprints_namespace
from skf.api.sprints.endpoints.sprint_update import ns as sprints_namespace
from skf.api.sprints.endpoints.sprint_results import ns as sprints_namespace
from skf.api.sprints.endpoints.sprint_results_export import ns as sprints_namespace
from skf.api.sprints.endpoints.sprint_results_export_external import ns as sprints_namespace
from skf.api.sprints.endpoints.sprint_results_delete import ns as sprints_namespace
from skf.api.sprints.endpoints.sprint_results_update import ns as sprints_namespace
from skf.api.checklist.endpoints.checklist_items import ns as checklist_namespace
from skf.api.checklist.endpoints.checklist_item import ns as checklist_namespace
from skf.api.checklist.endpoints.checklist_item_update import ns as checklist_namespace
from skf.api.checklist.endpoints.checklist_question_correlation_update import ns as checklist_namespace
from skf.api.checklist.endpoints.checklist_item_new import ns as checklist_namespace
from skf.api.checklist.endpoints.checklist_item_delete import ns as checklist_namespace
from skf.api.checklist.endpoints.checklist_item_question import ns as checklist_namespace
from skf.api.checklist.endpoints.checklist_type_create import ns as checklist_namespace
from skf.api.checklist.endpoints.checklist_type_update import ns as checklist_namespace
from skf.api.checklist.endpoints.checklist_type_delete import ns as checklist_namespace
from skf.api.checklist.endpoints.checklist_type_item import ns as checklist_namespace
from skf.api.checklist.endpoints.checklist_type_items import ns as checklist_namespace
from skf.api.checklist.endpoints.checklist_type_items_with_filter import ns as checklist_namespace
from skf.api.checklist.endpoints.checklist_items_questions import ns as checklist_namespace
from skf.api.checklist_category.endpoints.checklist_category_create import ns as checklist_category
from skf.api.checklist_category.endpoints.checklist_category_delete import ns as checklist_category
from skf.api.checklist_category.endpoints.checklist_category_items import ns as checklist_category
from skf.api.checklist_category.endpoints.checklist_category_item import ns as checklist_category
from skf.api.checklist_category.endpoints.checklist_category_update import ns as checklist_category
#from skf.api.chatbot.endpoints.chatbot_question import ns as chatbot_namespace
from skf.api.code.endpoints.code_item import ns as code_namespace
from skf.api.code.endpoints.code_items import ns as code_namespace
from skf.api.code.endpoints.code_items_new import ns as code_namespace
from skf.api.code.endpoints.code_item_delete import ns as code_namespace
from skf.api.code.endpoints.code_item_update import ns as code_namespace
from skf.api.code.endpoints.checklist_kb_code_items_delete import ns as code_namespace
from skf.api.code.endpoints.checklist_kb_code_items_new import ns as code_namespace
from skf.api.code.endpoints.checklist_kb_code_items import ns as code_namespace
from skf.api.kb.endpoints.kb_items import ns as kb_namespace
from skf.api.kb.endpoints.kb_item import ns as kb_namespace
from skf.api.kb.endpoints.kb_item_update import ns as kb_namespace
from skf.api.kb.endpoints.kb_item_delete import ns as kb_namespace
from skf.api.kb.endpoints.kb_item_new import ns as kb_namespace
from skf.api.questions.endpoints.question_item import ns as questions_namespace
from skf.api.questions.endpoints.question_items import ns as questions_namespace
from skf.api.questions.endpoints.question_store import ns as questions_namespace
from skf.api.questions.endpoints.question_item_update import ns as question_post_item_update
from skf.api.questions.endpoints.question_item_new import ns as question_post_item_new
from skf.api.questions.endpoints.question_item_delete import ns as question_post_item_update
from skf.api.search.endpoints.search_kb import ns as search_namespace
from skf.api.search.endpoints.search_lab import ns as search_namespace
from skf.api.search.endpoints.search_code import ns as search_namespace
from skf.api.search.endpoints.search_checklist import ns as search_namespace
from skf.api.search.endpoints.search_project import ns as search_namespace
from skf.api.training.endpoints.training_profile_item import ns as training_namespace
from skf.api.training.endpoints.training_profile_items import ns as training_namespace
from skf.api.training.endpoints.training_course_item import ns as training_namespace
from skf.api.training.endpoints.training_course_progress import ns as training_namespace
from skf.api.training.endpoints.training_course_progress_update import ns as training_namespace
from elasticapm.contrib.flask import ElasticAPM


from skf.api.restplus import api
from skf.database import db

def create_app():
    flask_app = Flask(__name__)
    configure_app(flask_app)
    initialize_app(flask_app)
    db.init_app(flask_app)
    return flask_app

def configure_app(flask_app):
    """Configure the SKF app."""
    #cannot use SERVER_NAME because it will mess up the routing
    #flask_app.config['SERVER_NAME'] = settings.FLASK_SERVER_NAME
    flask_app.config['SQLALCHEMY_DATABASE_URI'] = settings.SQLALCHEMY_DATABASE_URI
    flask_app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = settings.SQLALCHEMY_TRACK_MODIFICATIONS
    flask_app.config['SWAGGER_UI_DOC_EXPANSION'] = settings.RESTPLUS_SWAGGER_UI_DOC_EXPANSION
    flask_app.config['RESTPLUS_VALIDATE'] = settings.RESTPLUS_VALIDATE
    flask_app.config['RESTPLUS_MASK_SWAGGER'] = settings.RESTPLUS_MASK_SWAGGER
    flask_app.config['ERROR_404_HELP'] = settings.RESTPLUS_ERROR_404_HELP
    flask_app.config['TESTING'] = settings.TESTING
    flask_app.config['FLASK_DEBUG'] = settings.FLASK_DEBUG
    flask_app.config['SQLALCHEMY_ECHO'] = settings.SQLALCHEMY_ECHO
    flask_app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = settings.SQLALCHEMY_TRACK_MODIFICATIONS
    #flask_app.config['RABBIT_MQ_CONN_STRING'] = settings.RABBIT_MQ_CONN_STRING
    #flask_app.config['RABBIT_MQ_DEPLOYMENT_WORKER'] = settings.RABBIT_MQ_DEPLOYMENT_WORKER
    #flask_app.config['RABBIT_MQ_DELETION_WORKER'] = settings.RABBIT_MQ_DELETION_WORKER
    flask_app.config['ELASTIC_APM'] = {
        # Set required service name. Allowed characters:
        # a-z, A-Z, 0-9, -, _, and space
        'SERVICE_NAME': 'skf-flask',
        # Use if APM Server requires a token
        'SECRET_TOKEN': '123',
        # Set custom APM Server URL (default: http://localhost:8200)
        'SERVER_URL': 'https://123.apm.us-central1.gcp.cloud.es.io:443',
        'CAPTURE_BODY': 'all',
    }

def initialize_app(flask_app):
    """Initialize the SKF app."""
    blueprint = Blueprint('api', __name__, url_prefix='/api')
    api.init_app(blueprint)
    api.add_namespace(lab_namespace)
    #api.add_namespace(lab_code_namespace)
    api.add_namespace(kb_namespace)
    api.add_namespace(code_namespace)
    api.add_namespace(project_namespace)
    api.add_namespace(sprints_namespace)
    api.add_namespace(checklist_namespace)
    api.add_namespace(checklist_category)
    #api.add_namespace(chatbot_namespace)
    api.add_namespace(questions_namespace)
    api.add_namespace(search_namespace)
    api.add_namespace(training_namespace)
    flask_app.register_blueprint(blueprint)

app = create_app()
#apm = ElasticAPM(app)

# TO DO FIX WILDCARD ONLY ALLOW NOW FOR DEV
cors = CORS(app, resources={r"/api/*": {"origins": settings.ORIGINS}})
logging.config.fileConfig('logging.conf')
log = logging.getLogger(__name__)


@app.cli.command('cleandb')
def cleandb_command():
    """Delete DB and creates a new database with all the Markdown files."""
    clean_db()
    log.info("cleaned the database.")


@app.cli.command('initdb')
def initdb_command():
    """Delete DB and creates a new database with all the Markdown files."""
    init_db()
    log.info("Created the database.")


@app.cli.command('initdataset')
def initdataset_command():
    """Creates the datasets needed for the chatbot."""
    init_dataset()
    log.info("Initialized the datasets.")


@app.cli.command('updatedb')
def updatedb_command():
    """Update the database with the markdown files."""
    update_db()
    log.info("Database updated with the markdown files.")
        

def main():
    """Main SKF method"""
    if settings.FLASK_DEBUG == 'False':
        log.info('>>>>> Starting development server http://'+settings.FLASK_HOST+":"+str(settings.FLASK_PORT)+' <<<<<')
        app.run(host=settings.FLASK_HOST, port=settings.FLASK_PORT, debug=False)    
    else:
        log.info('>>>>> Starting development server http://'+settings.FLASK_HOST+":"+str(settings.FLASK_PORT)+' <<<<<')
        app.run(host=settings.FLASK_HOST, port=settings.FLASK_PORT, debug=True)

if __name__ == "__main__":
    main()
