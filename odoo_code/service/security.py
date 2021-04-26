# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

import odoo
import odoo.exceptions

def login(db, login, password):
    res_users = odoo.registry(db)['res.users']
    try:
        return res_users._login(db, login, password)
    except odoo.exceptions.AccessDenied:
        return False

def check(db, uid, passwd):
    res_users = odoo.registry(db)['res.users']
    return res_users.check(db, uid, passwd)

def compute_session_token(session, env):
    self = env['res.users'].browse(session.uid)
    print('######### self in security: ', self)
    print('######### uid from security: ', session.uid)
    print('######### sid from security: ', session.sid)
    return self._compute_session_token(session.sid)

def check_session(session, env):
    self = env['res.users'].browse(session.uid)
    expected = self._compute_session_token(session.sid)
    if expected and odoo.tools.misc.consteq(expected, session.session_token):
        return True
    self._invalidate_session_cache()
    return False

# def getUid(session, env):
#     self = env['res.users'].browse(session.login)
#     return  self.getUserByLogin(session.login)
def getUid(env, login):
    self = env['res.users']
    return  self.getUserByLogin(login)