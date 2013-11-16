def getTotalRoles(r):
    return 0

def getFilledRoles(r):
    return 0

@auth.requires_login()
def index():
    t = db.Project
    #Get grid of projects owned by user
    q = (t.projectOwner == auth.user.id)
    owned = SQLFORM.grid(q
                    ,searchable = True
                    ,fields=[t.name, t.shortDesc, t.projectActive]
                    ,csv = False
                    ,details = False
                    ,create = False
                    ,editable = True
                    ,deletable = False
                    ,links = [dict(header=T('Roles'), body = getTotalRoles)
                              ,dict(header=T('Roles Filled'), body = getFilledRoles)]
                    )
    return dict(owned = owned)

@auth.requires_login()
def addProject():
    form = SQLFORM(db.Project)
    if form.process().accepted:
        session.flash = 'Project posted'
        redirect(URL('projects', 'index'))
    return dict(form = form)

@auth.requires_login()
def editProject():
    return dict()

@auth.requires_login()
def deleteProject():
    return dict()
