# =============================================================================
# >> IMPORTS
# =============================================================================
from commands.client import ClientCommand
from entities.entity import BaseEntity
from events import Event
from filters.players import PlayerIter
from listeners import OnClientActive, OnPlayerRunCommand
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
# >> GLOBAL VARS
# =============================================================================

pressed = {}
in_zoom = {}

# =============================================================================
# >> LOAD
# =============================================================================

for player in PlayerIter():
    pressed[player.userid] = 0
    in_zoom[player.userid] = 0

# =============================================================================
# >> LISTENERS
# =============================================================================
@OnClientActive
def on_client_active(index):
    in_zoom[Player(index).userid] = 0
    pressed[Player(index).userid] = 0
    
@ClientCommand('do_zoom')
def _zoom_client_command(command,index,team_only=False):
    player = Player(index)
    if player.active_weapon == None: return
    if player.active_weapon.classname in zoom_weapons:
        if in_zoom[player.userid] != 1:
            player.fov = zoom_level
            in_zoom[player.userid] = 1
        else:
            player.fov = 90
            in_zoom[player.userid] = 0

@OnPlayerRunCommand
def on_player_run_command(player, user_cmd):
    if zoom_button != None:
        if user_cmd.buttons & zoom_button:
            if player.active_weapon.classname in zoom_weapons:
                if pressed[player.userid] == 0:
                    if in_zoom[player.userid] != 1:
                        pressed[player.userid] = 1
                        player.fov = zoom_level
                        in_zoom[player.userid] = 1
                    else:
                        player.fov = 90
                        in_zoom[player.userid] = 0
                        pressed[player.userid] = 1
        else:
            if pressed[player.userid] == 1:
                pressed[player.userid] = 0
    if player.active_weapon != None:
        if player.active_weapon.classname not in zoom_weapons and player.active_weapon.classname not in zoom_exclude:
            player.fov = 90
            in_zoom[player.userid] = 0
            pressed[player.userid] = 0


        pressed[player.userid] = 0
