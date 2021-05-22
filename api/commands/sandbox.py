# -*- coding: utf-8 -*-
from pprint import pprint
import traceback
from flask import current_app as app

from sandboxes.create_sandbox import create_sandbox


@app.manager.option('-n',
                    '--name',
                    help='Sandbox name',
                    default='ci')
@app.manager.option('-d',
                    '--delete',
                    help='Delete database first',
                    default='true')
def sandbox(name, delete):
    try:
        with_delete = delete == 'true'
        create_sandbox(name, with_delete)
    except Exception as e:
        print('ERROR: ' + str(e))
        traceback.print_tb(e.__traceback__)
        pprint(vars(e))
