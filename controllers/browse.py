def getTopSkill(r):
    iDB = db.SkillInstance
    q = (iDB.skillOwner == r.id)
    top = None
    for skill in db(q).select():
        if (top is None) or (skill.score > top.score):
            top = skill
    return db.Skill(top.skill).name or 'None'

def browse_users():
    auth = db.auth_user
    #Get grid of projects owned by user
    q = (auth.unlisted == False)
    form = SQLFORM.grid(q
                    ,searchable = True
                    ,fields=[auth.first_name, auth.last_name, auth.email]
                    ,csv = False
                    ,details = False
                    ,create = False
                    ,editable = False
                    ,deletable = False
                    ,user_signature=False
                    ,links = [dict(header=T('Best Skill'), 
                                       body = getTopSkill
                                       ),
                              dict(header=T('Actions'), 
                                   body = getUserBrowseActions)]
                    )
    return dict(form= form)

def getUserBrowseActions(r):
    view = A('View', _class='btn', _href = URL('browse', 'view_user', args = [r.id], user_signature = False))
    return view

def getProjectBrowseActions(r):
    view = A('View', _class='btn', _href = URL('browse', 'view_project', args = [r.id]))
    join = ''
    contact = ''
    #If the current user doesn't know the owner, this button will let them contact them.
    return view

def view_user():
    user = db.auth_user(request.args(0))
    iDB = db.SkillInstance
    q = (iDB.skillOwner == user.id)
    skills = SQLFORM.grid(q
                        ,searchable = True
                        ,fields=[iDB.skill, iDB.skillRank, iDB.score, iDB.reviews]
                        ,csv = False
                        ,details = False
                        ,create = False
                        ,editable = False
                        ,deletable = False
                        ,user_signature = False
                        ,links = []
                        )
    rDB = db.Role
    q = (rDB.holder == user.id)
    activeProjects = SQLFORM.grid(q
                        ,searchable = True
                        ,fields=[iDB.skill, iDB.skillRank, iDB.score, iDB.reviews]
                        ,csv = False
                        ,details = False
                        ,create = False
                        ,editable = False
                        ,deletable = False
                        ,user_signature = False
                        ,links = []
                        )

    return dict(user=user, skills=skills)

def view_project():
    project = db.Project(request.args(0))
    owner = db.auth_user(project.projectOwner) or None
    rDB = db.Role
    q = (rDB.project == project)
    if (db(q).count() > 0):
        roles = SQLFORM.grid(q
                            ,searchable = True
                            ,fields=[rDB.name, rDB.shortDesc, rDB.holder]
                            ,csv = False
                            ,details = False
                            ,create = False
                            ,editable = False
                            ,deletable = False
                            ,user_signature = False
                            ,links = []
                            )
    else:
        roles = "No roles found for this project."
    return dict(project=project, owner=owner, roles=roles)


def browse_projects():
    proj = db.Project
    #Get grid of projects owned by user
    q = (proj.unlisted == False)
    t = db.Project
    form = SQLFORM.grid(q
                    ,searchable = True
                    ,fields=[t.name, t.shortDesc, t.projectActive]
                    ,csv = False
                    ,details = False
                    ,create = False
                    ,editable = False
                    ,deletable = False
                    ,links = [dict(header=T('Roles'), body = getTotalRoles)
                              ,dict(header=T('Roles Filled'), body = getFilledRoles)
                              ,dict(header=T('Actions'), body = getProjectBrowseActions)]
                    )
    return dict(form= form)