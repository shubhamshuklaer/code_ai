# -*- coding: utf-8 -*-
# this file is released under public domain and you can use without limitations

#########################################################################
## This is a sample controller
## - index is the default action of any application
## - user is required for authentication and authorization
## - download is for downloading files uploaded in the db (does streaming)
#########################################################################

def code():
    prob_code=request.vars['prob_code']
    if "no_load_prob" in request.vars:
        load_prob=False
    else:
        load_prob=True
    from bs4 import BeautifulSoup as bs
    import urllib
    if load_prob:
        r = urllib.urlopen('http://spoj.com/problems/'+prob_code).read()
        soup=bs(r,"lxml")
        problem_body=soup.find(id="problem-body")
    else:
        problem_body="Remove no_load_prob to load problem"
    import os
    import re
    return dict(problem_body=XML(problem_body),prob_code=prob_code)

def submit():
    prob_code=request.vars['prob_code']
    import os
    ret_val=os.popen('spoj submit -p '+prob_code).read()
    return ret_val[ret_val.find("Result"):]

def run():
    import os
    prob_code=request.vars['prob_code']
    test_case_num=request.vars['test_case_num']
    return os.popen('spoj run '+test_case_num+' -p '+prob_code+' -c').read()

def index():
    """
    example action using the internationalization operator T and flash
    rendered by views/default/index.html or views/generic.html

    if you need a simple wiki simply replace the two lines below with:
    return auth.wiki()
    """
    response.flash = T("Hello World Shubham")
    return dict(message=T('Welcome to web2py!'))


def user():
    """
    exposes:
    http://..../[app]/default/user/login
    http://..../[app]/default/user/logout
    http://..../[app]/default/user/register
    http://..../[app]/default/user/profile
    http://..../[app]/default/user/retrieve_password
    http://..../[app]/default/user/change_password
    http://..../[app]/default/user/bulk_register
    use @auth.requires_login()
        @auth.requires_membership('group name')
        @auth.requires_permission('read','table name',record_id)
    to decorate functions that need access control
    also notice there is http://..../[app]/appadmin/manage/auth to allow administrator to manage users
    """
    return dict(form=auth())


@cache.action()
def download():
    """
    allows downloading of uploaded files
    http://..../[app]/default/download/[filename]
    """
    return response.download(request, db)


def call():
    """
    exposes services. for example:
    http://..../[app]/default/call/jsonrpc
    decorate with @services.jsonrpc the functions to expose
    supports xml, json, xmlrpc, jsonrpc, amfrpc, rss, csv
    """
    return service()


