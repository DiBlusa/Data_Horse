class RoleBased:

    def __init__(self, id_user, id_role):
        self.id_user = id_user
        self.id_role = id_role

    @property
    def name(self):
        
        roles = {
            1: "visitor",
            2: "caregiver",
            3: "Admin",
        }
        return roles.get(self.id_role, "No role assigned")