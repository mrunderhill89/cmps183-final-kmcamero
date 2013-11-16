@auth.requires_login()
def index():
    sDB = db.Skill
    iDB = db.SkillInstance
    #Get grid of skill instances owned by user
    q = (iDB.skillOwner == auth.user.id)
    owned = SQLFORM.grid(q
                    ,searchable = True
                    ,fields=[iDB.skill, iDB.skillRank, iDB.score, iDB.reviews]
                    ,csv = False
                    ,details = False
                    ,create = False
                    ,editable = False
                    ,deletable = False
                    ,links = [dict(header=T('Actions'), 
                                       body = lambda r: A('Edit', _class='btn', _href = URL('skillset', 'editSkill', args = [r.id]))
                                       )]
                    )
    return dict(owned = owned)

def getAvailableRanks(score):
    aranks = []
    for rank in skillRanks.keys():
        minScore = skillRanks[rank][0]
        if (score >= minScore or minScore < 0):
            aranks.append(rank)
    return aranks

def is_rejected_skill(form):
    sDB = db.Skill
    q = db(sDB.name == form.vars.skillName)
    if q.count() > 0:
        r = q.select().first()
        if r.rejected :
            form.errors.skillName = "This skill name was rejected by an admin."

def is_already_has_skill(form):
    iDB = db.SkillInstance
    sDB = db.Skill
    #Check if we already have that skill. If not, then it passes automatically
    skill = db(sDB.name == form.vars.skillName).select().first()
    if (skill is not None):
        q = db((iDB.skillOwner == auth.user.id) & (iDB.skill == skill))
        if (q.count() > 0):
            form.errors.skillName = "You already have that skill."

def is_new_skill(form):
    sDB = db.Skill
    q = db(sDB.name == form.vars.skillName)
    #If the skill isn't in the database already, create it
    if q.count() <= 0:
        sDB.insert(name = form.vars.skillName)

@auth.requires_login()
def addSkill():
    form = SQLFORM.factory(
                            Field('skillName', requires=IS_NOT_EMPTY()),
                            Field('skillRank', requires=IS_IN_SET(getAvailableRanks(0)))
                            )
    form.add_button('Cancel', URL('default', 'index'))
    if form.process(onvalidation=[is_new_skill, is_rejected_skill, is_already_has_skill]).accepted:
        skill = db(db.Skill.name == form.vars.skillName).select().first()
        db.SkillInstance.insert(skill = skill.id, skillRank = form.vars.skillRank)
        session.flash = 'Skill Added.'
        redirect(URL('skillset', 'index'))
    return dict(form = form)


@auth.requires_login()
def editSkill():
    my_record = db.SkillInstance(request.args(0))
    my_skill = db.Skill(my_record.skill).name or 'Unrecognized'
    if my_record is None: 
        session.flash = 'Invalid edit request.'
        redirect(URL('skillset', 'index'))
    
    form = SQLFORM.factory(
                            Field('skillRank', requires=IS_IN_SET(getAvailableRanks(my_record.score)), default=my_record.skillRank)
                            )
    form.add_button('Cancel', URL('default', 'index'))
    if form.process().accepted:
        my_record.update_record(skillRank = form.vars.skillRank)
        session.flash = 'Skill Updated.'
        redirect(URL('skillset', 'index'))
    return dict(form = form)
"""
projects: Allows the user to view, add, edit, and delete their own projects.
    Subpages:
        addProject
        editProject
        deleteProject
        viewProject
browseProjects
"""