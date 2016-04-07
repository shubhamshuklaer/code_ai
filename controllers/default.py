# -*- coding: utf-8 -*-
# this file is released under public domain and you can use without limitations

#########################################################################
## This is a sample controller
## - index is the default action of any application
## - user is required for authentication and authorization
## - download is for downloading files uploaded in the db (does streaming)
#########################################################################

def get_run_result(cmd):
    import subprocess,shlex
    args = shlex.split(cmd)
    try:
        ret_val=subprocess.check_output(args,stderr=subprocess.STDOUT)
    # http://stackoverflow.com/a/8235171/2258503
    except subprocess.CalledProcessError as e:
        ret_val="Return code: "+str(e.returncode)+"\n"+e.output
    return ret_val.decode('utf8').strip()


def code():
    import os
    import re
    from bs4 import BeautifulSoup as bs
    import urllib

    prob_code=request.vars['prob_code']
    if get_run_result("spoj is_configured") == "0":
        redirect(URL('spoj_not_configured'))
    if get_run_result("spoj is_problem_started -p "+prob_code) == "0":
        redirect(URL('start_problem',vars=request.vars))

    if "no_load_prob" in request.vars:
        load_prob=False
    else:
        load_prob=True
    if load_prob:
        r = urllib.urlopen('http://spoj.com/problems/'+prob_code).read()
        soup=bs(r,"lxml")
        problem_body=soup.find(id="problem-body")
    else:
        problem_body="Remove no_load_prob to load problem"
    return dict(problem_body=XML(problem_body),prob_code=prob_code)

def get_lang_info_helper(language):
    import os
    cmds=get_run_result('spoj get_lang_info -l '+language).splitlines()
    cmpile_cmd=cmds[0].split(":")[1].strip()
    run_cmd=cmds[1].split(":")[1].strip()
    extension=cmds[2].split(":")[1].strip()
    if cmpile_cmd == "None":
        cmpile_cmd=""
    if run_cmd == "None":
        run_cmd=""
    if extension == "None":
        extension=""
    return cmpile_cmd,run_cmd,extension

def start_problem():
    import os
    prob_code=request.vars['prob_code']
    if 'language' in request.vars:
        language=request.vars["language"]
        cmpile_cmd=request.vars["cmpile_cmd"]
        run_cmd=request.vars["run_cmd"]
        extension=request.vars["extension"]
        os.system("spoj set_lang_info -l '"+language+"' --cmpile_cmd '"+cmpile_cmd+"' --run_cmd '"+run_cmd+"' --extension '"+extension+"'")
        os.system("spoj start -n "+prob_code+" -l "+language)
        del request.vars['language']
        del request.vars['cmpile_cmd']
        del request.vars['run_cmd']
        del request.vars["extension"]
        redirect(URL('code',vars=request.vars))
    else:
        ret_val=get_run_result('spoj language')
        lang_list=[s.strip() for s in ret_val.splitlines()]
        lang_list.pop(0)
        lang_dict=dict()
        for lang in lang_list:
            lang_dict[lang.split(":")[1].strip()]=lang.split(":")[0].strip()
        default_lang=get_run_result('spoj get_language')
        default_cmpile_cmd,default_run_cmd,default_extension=get_lang_info_helper(default_lang)
        return dict(lang_dict=lang_dict,default_lang=default_lang,default_cmpile_cmd=default_cmpile_cmd,default_run_cmd=default_run_cmd,default_extension=default_extension)

def get_lang_info():
    language=request.vars["language"]
    cmpile_cmd,run_cmd,extension=get_lang_info_helper(language)
    import json
    # if we send a dict it actually send some default html with the dict as paramaters
    return json.dumps(dict(cmpile_cmd=cmpile_cmd,run_cmd=run_cmd,extension=extension))


def spoj_not_configured():
    return dict(error_text="spoj not configured, run spoj config --config_all")

def add_input():
    prob_code=request.vars['prob_code']
    import os
    os.system('spoj add_input -n -p '+prob_code);

def submit():
    prob_code=request.vars['prob_code']
    import os
    ret_val=get_run_result('spoj submit -p '+prob_code)
    return ret_val[ret_val.find("Result"):]

def run():
    import os
    prob_code=request.vars['prob_code']
    test_case_num=request.vars['test_case_num']
    return get_run_result('spoj run '+test_case_num+' -p '+prob_code+' -c')

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


