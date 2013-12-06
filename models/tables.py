#Define database entries for the skill ranking system

# Skill defines the singleton instance of any skill name, and whether
# it's an acceptable skill to list publicly. Since users can come up
# with their own skills, there needs to be an admin-level reviewing system set up
# so that you can't list some nonsense skill like "beer drinking" on your profile.
#
# name - the name of the skill
# accepted - whether the skill has been accepted for public use by an admin.
# rejected - whether the skill has been rejected by an admin, and can't be used by others.
#  
db.define_table('Skill',
                Field('name','string', default='new skill'),
                Field('accepted', 'boolean', default = False),
                Field('rejected', 'boolean', default = False)
                )
#List ranks and minimum scores for each skill rank.
skillRanks = {'Learning/Rusty':[-1,1], 'Proficient':[0,2] , 'Expert':[40,3], 'Master':[100,4], 'Grandmaster':[1000,5], 'Super Saiyan':[9001,10]}
# SkillInstance holds information per-user on what skills the user has.
# They each contain a reference to the base skill, as well as ranking information.
#
# Owner - the user who owns this skill instance.
# Skill - the base skill that the instance represents.
# Rank - the user's self-selected rank. May change to an enum when I can figure out how to do that.
# Score - the user's total score from collected reviews.
# Reviews - the individual reviews held by each instance.
#
db.define_table('SkillInstance',
                Field('skillOwner', 'reference auth_user', default=auth.user_id),
                Field('skill', 'reference Skill'),
                Field('skillRank', requires=IS_IN_SET(skillRanks.keys()), default='Learning/Rusty'),
                Field('score', 'integer', default = 0),
                Field('reviews', 'reference Review')
                )

db.SkillInstance.skillRank.label = "Rank"

def getSkillName(name, row):
    return db.Skill(name).name or 'Unrecognized'

db.SkillInstance.skill.represent = getSkillName
# Reviews determine a user's score in a particular skill.
#
# sender - The person sending the review
# receiver - The person being reviewed
# anonymous - Whether the sender's name is visible to the receiver.
#             Note: The sender's ID is still stored to confirm that the
#                   sender is someone the receiver knows (to prevent trolling).
#                   This flag only prevents the receiver from casually knowing who sent the review.
# skillInstance - The particular skill instance being reviewed.
db.define_table('Review',
                Field('sender', 'reference auth_user', default=auth.user_id),
                Field('receiver', 'reference auth_user'),
                Field('anonymous', 'boolean', default=False),
                Field('skillInstance', 'reference SkillInstance'),
                Field('impact', 'integer', default=1),
                Field('feedback', 'text'),
                )
def getUserNameOrAnon(name, row):
    if (row.anonymous):
        return "Anonymous"
    user = db.auth_user(name)
    if (user is None):
        return "Unrecognized"
    return user.first_name + " " + user.last_name

db.Review.sender.represent = getUserNameOrAnon

# Data for handling projects and roles.
#
def getTotalRoles(r):
    roles = db.Role
    q = (roles.project == r)
    return db(q).count()

def getFilledRoles(r):
    roles = db.Role
    q = ((roles.project == r) & (roles.holder != None))
    return db(q).count()

db.define_table('Project',
                Field('name', 'string', default = 'Project'),
                Field('projectOwner', 'reference auth_user', default=auth.user_id),                                
                Field('shortDesc', 'string', default = ''),
                Field('longDesc', 'text', default = ''),
                Field('roles', 'list:reference Role', default = []),
                Field('projectActive', 'boolean', default = True),
                Field('unlisted', 'boolean', default = False)
                )
db.Project.ondelete = 'SET NULL'
db.Project.projectOwner.label = "Owner"
db.Project.projectOwner.writable = False
db.Project.roles.readable = False
db.Project.roles.writable = False
db.Project.shortDesc.label = "Short Description"
db.Project.longDesc.label = "Long Description"
db.Project.projectActive.label = "Active"
db.Project.unlisted.label = 'Unlisted'

db.define_table('Contact',
                Field('sender', 'reference auth_user', default=auth.user_id),
                Field('receiver', 'reference auth_user', default = None),
                Field('accepted', 'boolean', default = False),
                Field('blocked', 'boolean', default = False)
                )

def getProjectName(name, row):
    return db.Project(name) or 'Unrecognized'

db.define_table('Role',
                Field('name', 'string', default = 'Role'),
                Field('project', 'reference Project'),                                
                Field('holder', 'reference auth_user', default=None, requires=IS_EMPTY_OR(IS_IN_DB(db, db.auth_user.id))),                                
                Field('applicants', 'list:reference auth_user', default = []),
                Field('shortDesc', 'string', default = ''),
                Field('longDesc', 'text', default = ''),
                )
db.Role.project.represent = getProjectName
db.Role.project.writable = False
db.Role.shortDesc.label = "Short Description"
db.Role.longDesc.label = "Long Description"