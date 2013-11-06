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
                Field('skillRank', 'string', default='Learning/Rusty'),
                Field('score', 'integer', default = 0),
                Field('reviews', 'reference Review')
                )
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

# Data for handling projects and roles.
#
db.define_table('Project',
                Field('name', 'string', default = 'Project'),
                Field('projectOwner', 'reference auth_user', default=auth.user_id),                                
                Field('shortDesc', 'string', default = ''),
                Field('longDesc', 'text', default = ''),
                Field('roles', 'list:reference Role'),
                Field('startDate', 'datetime'),
                Field('endDate', 'datetime')
                )

db.define_table('Role'
                )