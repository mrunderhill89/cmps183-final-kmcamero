def getProjectActions(r):
    edit = A('Edit', _href=URL('projects','edit', args = [r.id], user_signature=True), _class='btn')
    editRoles = A('Edit Roles', _href=URL('projects', 'editRoles', args = [r.id], user_signature=True), _class='btn')
    delete = A('Delete', _href=URL('projects','delete', args = [r.id], user_signature=True), _class='btn')
    return edit + editRoles + delete

@auth.requires_login()
def index():
    t = db.Project
    #Get grid of projects owned by user
    q = (t.projectOwner == auth.user.id)
    owned = SQLFORM.grid(q
                    ,searchable = True
                    ,fields=[t.name, t.shortDesc, t.projectActive, t.unlisted]
                    ,csv = False
                    ,details = False
                    ,create = False
                    ,editable = False
                    ,deletable = False
                    ,links = [dict(header=T('Roles'), body = getTotalRoles)
                              ,dict(header=T('Roles Filled'), body = getFilledRoles)
                              ,dict(header=T('Actions'), body = getProjectActions)]
                    )
    return dict(owned = owned)

@auth.requires_login()
def add():
    form = SQLFORM(db.Project)
    if form.process().accepted:
        session.flash = 'Project added. Now please add roles to it.'
        redirect(URL('projects', 'editRoles', args=[form.vars.id], user_signature=True))
    return dict(form = form)

@auth.requires_signature()
def edit():
    my_record = db.Project(request.args(0))
    if my_record is None: 
        session.flash = 'Invalid edit request.'
        redirect(URL('projects', 'index'))
    form = SQLFORM(db.Project, record=my_record)
    if form.process().accepted:
        session.flash = 'Project Updated.'
        redirect(URL('projects', 'index'))
    return dict(form = form)

@auth.requires_signature()
def delete():
    my_record = db.Project(request.args(0))
    if my_record is None: 
        session.flash = 'Invalid delete request.'
        redirect(URL('projects', 'index'))
    if getFilledRoles(my_record) > 0:       
        session.flash = 'Project still has roles filled. Please empty them first.'
        redirect(URL('projects', 'index'))        
    form = SQLFORM.factory()
    form.add_button('Cancel', URL('default', 'index'))
    if form.process().accepted:
        my_record.delete_record()
        session.flash = 'Project Deleted.'
        redirect(URL('projects', 'index'))
    return dict(form = form)

@auth.requires_signature()
def addRole():
    project = db.Project(request.args(0))
    if project is None: 
        session.flash = 'Invalid project record.'
        redirect(URL('projects', 'index'))
    db.Role.holder.readable = False
    db.Role.holder.writable = False
    form = SQLFORM(db.Role)
    form.vars.project = project
    if form.process().accepted:
        session.flash = 'Role Added.'
        redirect(URL('projects', 'index'))
    return dict(form = form)

@auth.requires_signature()
def editRoles():
    project = db.Project(request.args(0))
    if project is None: 
        session.flash = 'Invalid project record.'
        redirect(URL('projects', 'index'))
    t = db.Role
    #Get grid of projects owned by user
    q = (t.project == project)
    form = SQLFORM.grid(q
                    ,searchable = True
                    ,fields=[t.name, t.shortDesc, t.holder]
                    ,csv = False
                    ,details = False
                    ,create = False
                    ,editable = False
                    ,deletable = False
                    ,links = [dict(header=T('Actions'), body = getRoleActions)]
                    )
    addRole = A('Add Role', _href=URL('projects', 'addRole', args = [project.id], user_signature=True), _class='btn')    
    return dict(form = form, addRole = addRole, project=project)

def getRoleActions(r):
    edit = A('Edit', _href=URL('projects','editRole', args = [r.id], user_signature=True), _class='btn')
    reject = ""
    if (r.holder != None):
        reject = A('Reject Holder', _href=URL('projects','rejectRole', args = [r.id], user_signature=True), _class='btn')
    else:
        delete = A('Delete', _href=URL('projects','deleteRole', args = [r.id], user_signature=True), _class='btn')
    return edit + reject + delete

@auth.requires_signature()
def editRole():
    my_record = db.Role(request.args(0))
    if my_record is None: 
        session.flash = 'Invalid project record.'
        redirect(URL('projects', 'index'))
    db.Role.holder.readable = False
    db.Role.holder.writable = False
    form = SQLFORM(db.Role, record=my_record)
    if form.process().accepted:
        session.flash = 'Role Added.'
        redirect(URL('projects', 'index'))
    return dict(form = form)

@auth.requires_signature()
def deleteRole():
    my_record = db.Role(request.args(0))
    if my_record is None: 
        session.flash = 'Invalid delete request.'
        redirect(URL('projects', 'index'))
    if my_record.holder != None:
        session.flash = 'Role still held by a user. Reject them first.'
        redirect(URL('projects', 'index'))        
    form = SQLFORM.factory()
    form.add_button('Cancel', URL('default', 'index'))
    if form.process().accepted:
        my_record.delete_record()
        session.flash = 'Role Deleted.'
        redirect(URL('projects', 'index'))
    return dict(form = form)