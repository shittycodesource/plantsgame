from projectiles.projectile import Projectile

class Pea(Projectile):
    def __init__(self, group, shadow_group, pos_x, pos_y):
        super().__init__("Pea", group, shadow_group, pos_x, pos_y)
        self.group = group
        self.setup_shadow()