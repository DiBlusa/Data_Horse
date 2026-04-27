class RoleBased:

    def __init__(self, id_user, id_role):
        self.id_user = id_user
        self.id_role = id_role

    @property
    def name(self):
        
        roles = {
            1: "vaqueiro",
            2: "cuidador",
            3: "dono",
        }
        return roles.get(self.id_role, "No role assigned")