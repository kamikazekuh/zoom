# =============================================================================
# >> IMPORTS
# =============================================================================
from commands.client import ClientCommand
from listeners import OnPlayerRunCommand
from players.constants import PlayerButtons
from players.entity import Player

# =============================================================================
# >> CONFIG
# =============================================================================
zoom_button = PlayerButtons.ATTACK2
zoom_level = 30
zoom_weapons = ['weapon_357']
zoom_exclude = ['weapon_crossbow']

# =============================================================================
# >> CLASSES
# =============================================================================
class ZoomPlayer(Player):
    def __init__(self, index, caching=True):
        super().__init__(index, caching)
        self.pressed = False
        self.in_zoom = False
        
    def toggle_zoom(self):
        weapon = self.active_weapon
        if weapon is None or weapon.classname not in zoom_weapons:
            return

        self.fov = self.default_fov if self.fov == zoom_level else zoom_level 

# =============================================================================
# >> COMMANDS
# =============================================================================
@ClientCommand('do_zoom')
def _zoom_client_command(command,index,team_only=False):
    player = ZoomPlayer(index)
    weapon = player.active_weapon
    if weapon == None: return
    if weapon.classname in zoom_weapons:
        player.toggle_zoom()        

# =============================================================================
# >> LISTENERS
# =============================================================================
if zoom_button != None:        
    @OnPlayerRunCommand
    def on_player_run_command(ply, user_cmd):
        player = ZoomPlayer(ply.index)
        weapon = player.active_weapon
        default_pov = player.default_fov
        if weapon == None: return
        if user_cmd.buttons & zoom_button:
            if weapon.classname in zoom_weapons:
                if player.pressed == False:
                    if player.in_zoom == False:
                        player.pressed = True
                        player.fov = zoom_level
                        player.in_zoom = True
                    else:
                        player.fov = default_pov
                        player.in_zoom = 0
                        player.pressed = 1
        else:
            if player.pressed == 1:
                player.pressed = 0
        if weapon.classname not in zoom_weapons and weapon.classname not in zoom_exclude:
            player.fov = default_pov
            player.in_zoom = False
            player.pressed = False
