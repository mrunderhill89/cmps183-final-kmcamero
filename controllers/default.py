# -*- coding: utf-8 -*-
# this file is released under public domain and you can use without limitations

#########################################################################
## This is a sample controller
## - index is the default action of any application
## - user is required for authentication and authorization
## - download is for downloading files uploaded in the db (does streaming)
## - call exposes all registered services (none by default)
#########################################################################


def index():
    return dict()

def skillset():
    return dict()

def addSkill():
    return dict()

def editSkill():
    return dict()
"""
projects: Allows the user to view, add, edit, and delete their own projects.
    Subpages:
        addProject
        editProject
        deleteProject
        viewProject
browseProjects
"""
@auth.requires_login()
def projects():
    t = db.Project
    #Get grid of projects owned by user
    q = (t.projectOwner == auth.user.id)
    owned = SQLFORM.grid(q
                    ,searchable = True
                    ,fields=[t.name, t.shortDesc, t.startDate, t.endDate]
                    ,csv = False
                    ,details = False
                    ,create = False
                    ,editable = False
                    ,deletable = False
                    )
    return dict(owned = owned)

@auth.requires_login()
def addProject():
    return dict()

@auth.requires_login()
def editProject():
    return dict()

@auth.requires_login()
def deleteProject():
    return dict()

def browseProjects():
    return dict()

def viewProject():
    return dict()

def contacts():
    return dict()

def reviews():
    return dict()

def user():
    """
    exposes:
    http://..../[app]/default/user/login
    http://..../[app]/default/user/logout
    http://..../[app]/default/user/register
    http://..../[app]/default/user/profile
    http://..../[app]/default/user/retrieve_password
    http://..../[app]/default/user/change_password
    http://..../[app]/default/user/manage_users (requires membership in
    use @auth.requires_login()
        @auth.requires_membership('group name')
        @auth.requires_permission('read','table name',record_id)
    to decorate functions that need access control
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


@auth.requires_signature()
def data():
    """
    http://..../[app]/default/data/tables
    http://..../[app]/default/data/create/[table]
    http://..../[app]/default/data/read/[table]/[id]
    http://..../[app]/default/data/update/[table]/[id]
    http://..../[app]/default/data/delete/[table]/[id]
    http://..../[app]/default/data/select/[table]
    http://..../[app]/default/data/search/[table]
    but URLs must be signed, i.e. linked with
      A('table',_href=URL('data/tables',user_signature=True))
    or with the signed load operator
      LOAD('default','data.load',args='tables',ajax=True,user_signature=True)
    """
    return dict(form=crud())
