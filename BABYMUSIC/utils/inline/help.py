from typing import Union
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from BABYMUSIC import app

def help_pannel(_, START: Union[bool, int] = None):
    first = [InlineKeyboardButton(text=_["CLOSE_BUTTON"], callback_data="close")]
    second = [
        InlineKeyboardButton(
            text=_["BACK_BUTTON"],
            callback_data="settingsback_helper",
        ),
    ]
    mark = second if START else first
    
    upl = InlineKeyboardMarkup(
        [
            [
                InlineKeyboardButton(text=_["H_B_1"], callback_data="help_hb1"),
                InlineKeyboardButton(text=_["H_B_3"], callback_data="help_hb3"),
                InlineKeyboardButton(text=_["H_B_6"], callback_data="help_hb6"),
            ],
            [
                InlineKeyboardButton(text=_["H_B_7"], callback_data="help_hb7"),
                InlineKeyboardButton(text=_["H_B_10"], callback_data="help_hb10"),
                InlineKeyboardButton(text=_["H_B_11"], callback_data="help_hb11"),
            ],
            [
                InlineKeyboardButton(text=_["H_B_12"], callback_data="help_hb12"),
                InlineKeyboardButton(text=_["H_B_13"], callback_data="help_hb13"),
                InlineKeyboardButton(text=_["H_B_15"], callback_data="help_hb15"),
            ],
            mark,
        ]
    )
    return upl

def help_back_markup(_):
    upl = InlineKeyboardMarkup(
        [
            [
                InlineKeyboardButton(
                    text=_["BACK_BUTTON"],
                    callback_data="settings_back_helper",
                ),
            ]
        ]
    )
    return upl

def private_help_panel(_):
    buttons = [
        [
            InlineKeyboardButton(
                text=_["S_B_4"],
                url=f"https://t.me/{app.username}?start=help",
            ),
        ],
    ]
    return buttons
