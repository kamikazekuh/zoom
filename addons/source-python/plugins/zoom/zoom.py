from commands.client import ClientCommand
from entities.hooks import EntityCondition
from entities.hooks import EntityPreHook
from listeners import get_button_combination_status
from listeners import ButtonStatus
from listeners import OnButtonStateChanged
from memory import make_object
from players.constants import PlayerButtons
from players.entity import Player
from weapons.entity import Weapon

zoom_button = PlayerButtons.ATTACK2
zoom_level = 30
zoom_weapons = ['weapon_357']

def toggle_zoom(player):
    weapon = player.active_weapon
    if weapon is None or weapon.classname not in zoom_weapons:
        return

    player.fov = player.default_fov if player.fov == zoom_level else zoom_level

if zoom_button is not None:
    @OnButtonStateChanged
    def on_buttons_state_changed(player, old, new):
        if get_button_combination_status(old, new, zoom_button) != ButtonStatus.PRESSED:
            return

        toggle_zoom(player)

@ClientCommand('do_zoom')
def do_zoom(command, index, team_only=False):
    toggle_zoom(Player(index))

@EntityPreHook(EntityCondition.is_player, 'weapon_switch')
def pre_weapon_switch(stack_data):
    player = make_object(Player, stack_data[0])
    player.fov = player.default_fov
