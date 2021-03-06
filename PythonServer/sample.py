#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import print_function

import os
import sys
import socket

import gensim
import numpy as np
import tensorflow as tf

from six.moves import cPickle

from model import Model

reload(sys)
sys.setdefaultencoding('UTF8')

emojis = [('😄').decode('utf-8'), ('😃').decode('utf-8'), ('😀').decode('utf-8'), ('😊').decode('utf-8'),
          ('☺').decode('utf-8'), ('😉').decode('utf-8'), ('😍').decode('utf-8'), ('😘').decode('utf-8'),
          ('😚').decode('utf-8'), ('😗').decode('utf-8'), ('😙').decode('utf-8'), ('😜').decode('utf-8'),
          ('😝').decode('utf-8'), ('😛').decode('utf-8'), ('😳').decode('utf-8'), ('😁').decode('utf-8'),
          ('😔').decode('utf-8'), ('😌').decode('utf-8'), ('😒').decode('utf-8'), ('😞').decode('utf-8'),
          ('😣').decode('utf-8'), ('😢').decode('utf-8'), ('😂').decode('utf-8'), ('😭').decode('utf-8'),
          ('😪').decode('utf-8'), ('😥').decode('utf-8'), ('😰').decode('utf-8'), ('😅').decode('utf-8'),
          ('😓').decode('utf-8'), ('😩').decode('utf-8'), ('😫').decode('utf-8'), ('😨').decode('utf-8'),
          ('😱').decode('utf-8'), ('😠').decode('utf-8'), ('😡').decode('utf-8'), ('😤').decode('utf-8'),
          ('😖').decode('utf-8'), ('😆').decode('utf-8'), ('😋').decode('utf-8'), ('😷').decode('utf-8'),
          ('😎').decode('utf-8'), ('😴').decode('utf-8'), ('😵').decode('utf-8'), ('😲').decode('utf-8'),
          ('😟').decode('utf-8'), ('😦').decode('utf-8'), ('😧').decode('utf-8'), ('😈').decode('utf-8'),
          ('👿').decode('utf-8'), ('😮').decode('utf-8'), ('😬').decode('utf-8'), ('😐').decode('utf-8'),
          ('😕').decode('utf-8'), ('😯').decode('utf-8'), ('😶').decode('utf-8'), ('😇').decode('utf-8'),
          ('😏').decode('utf-8'), ('😑').decode('utf-8'), ('👲').decode('utf-8'), ('👳').decode('utf-8'),
          ('👮').decode('utf-8'), ('👷').decode('utf-8'), ('💂').decode('utf-8'), ('👶').decode('utf-8'),
          ('👦').decode('utf-8'), ('👧').decode('utf-8'), ('👨').decode('utf-8'), ('👩').decode('utf-8'),
          ('👴').decode('utf-8'), ('👵').decode('utf-8'), ('👱').decode('utf-8'), ('👼').decode('utf-8'),
          ('👸').decode('utf-8'), ('😺').decode('utf-8'), ('😸').decode('utf-8'), ('😻').decode('utf-8'),
          ('😽').decode('utf-8'), ('😼').decode('utf-8'), ('🙀').decode('utf-8'), ('😿').decode('utf-8'),
          ('😹').decode('utf-8'), ('😾').decode('utf-8'), ('👹').decode('utf-8'), ('👺').decode('utf-8'),
          ('🙈').decode('utf-8'), ('🙉').decode('utf-8'), ('🙊').decode('utf-8'), ('💀').decode('utf-8'),
          ('👽').decode('utf-8'), ('💩').decode('utf-8'), ('🔥').decode('utf-8'), ('✨').decode('utf-8'),
          ('🌟').decode('utf-8'), ('💫').decode('utf-8'), ('💥').decode('utf-8'), ('💢').decode('utf-8'),
          ('💦').decode('utf-8'), ('💧').decode('utf-8'), ('💤').decode('utf-8'), ('💨').decode('utf-8'),
          ('👂').decode('utf-8'), ('👀').decode('utf-8'), ('👃').decode('utf-8'), ('👅').decode('utf-8'),
          ('👄').decode('utf-8'), ('👍').decode('utf-8'), ('👎').decode('utf-8'), ('👌').decode('utf-8'),
          ('👊').decode('utf-8'), ('✊').decode('utf-8'), ('✌').decode('utf-8'), ('👋').decode('utf-8'),
          ('✋').decode('utf-8'), ('👐').decode('utf-8'), ('👆').decode('utf-8'), ('👇').decode('utf-8'),
          ('👉').decode('utf-8'), ('👈').decode('utf-8'), ('🙌').decode('utf-8'), ('🙏').decode('utf-8'),
          ('☝').decode('utf-8'), ('👏').decode('utf-8'), ('💪').decode('utf-8'), ('🚶').decode('utf-8'),
          ('🏃').decode('utf-8'), ('💃').decode('utf-8'), ('👫').decode('utf-8'), ('👪').decode('utf-8'),
          ('👬').decode('utf-8'), ('👭').decode('utf-8'), ('💏').decode('utf-8'), ('💑').decode('utf-8'),
          ('👯').decode('utf-8'), ('🙆').decode('utf-8'), ('🙅').decode('utf-8'), ('💁').decode('utf-8'),
          ('🙋').decode('utf-8'), ('💆').decode('utf-8'), ('💇').decode('utf-8'), ('💅').decode('utf-8'),
          ('👰').decode('utf-8'), ('🙎').decode('utf-8'), ('🙍').decode('utf-8'), ('🙇').decode('utf-8'),
          ('🎩').decode('utf-8'), ('👑').decode('utf-8'), ('👒').decode('utf-8'), ('👟').decode('utf-8'),
          ('👞').decode('utf-8'), ('👡').decode('utf-8'), ('👠').decode('utf-8'), ('👢').decode('utf-8'),
          ('👕').decode('utf-8'), ('👔').decode('utf-8'), ('👚').decode('utf-8'), ('👗').decode('utf-8'),
          ('🎽').decode('utf-8'), ('👖').decode('utf-8'), ('👘').decode('utf-8'), ('👙').decode('utf-8'),
          ('💼').decode('utf-8'), ('👜').decode('utf-8'), ('👝').decode('utf-8'), ('👛').decode('utf-8'),
          ('👓').decode('utf-8'), ('🎀').decode('utf-8'), ('🌂').decode('utf-8'), ('💄').decode('utf-8'),
          ('💛').decode('utf-8'), ('💙').decode('utf-8'), ('💜').decode('utf-8'), ('💚').decode('utf-8'),
          ('❤').decode('utf-8'), ('💔').decode('utf-8'), ('💗').decode('utf-8'), ('💓').decode('utf-8'),
          ('💕').decode('utf-8'), ('💖').decode('utf-8'), ('💞').decode('utf-8'), ('💘').decode('utf-8'),
          ('💌').decode('utf-8'), ('💋').decode('utf-8'), ('💍').decode('utf-8'), ('💎').decode('utf-8'),
          ('👤').decode('utf-8'), ('👥').decode('utf-8'), ('💬').decode('utf-8'), ('👣').decode('utf-8'),
          ('💭').decode('utf-8'), ('🐶').decode('utf-8'), ('🐺').decode('utf-8'), ('🐱').decode('utf-8'),
          ('🐭').decode('utf-8'), ('🐹').decode('utf-8'), ('🐰').decode('utf-8'), ('🐸').decode('utf-8'),
          ('🐯').decode('utf-8'), ('🐨').decode('utf-8'), ('🐻').decode('utf-8'), ('🐷').decode('utf-8'),
          ('🐽').decode('utf-8'), ('🐮').decode('utf-8'), ('🐗').decode('utf-8'), ('🐵').decode('utf-8'),
          ('🐒').decode('utf-8'), ('🐴').decode('utf-8'), ('🐑').decode('utf-8'), ('🐘').decode('utf-8'),
          ('🐼').decode('utf-8'), ('🐧').decode('utf-8'), ('🐦').decode('utf-8'), ('🐤').decode('utf-8'),
          ('🐥').decode('utf-8'), ('🐣').decode('utf-8'), ('🐔').decode('utf-8'), ('🐍').decode('utf-8'),
          ('🐢').decode('utf-8'), ('🐛').decode('utf-8'), ('🐝').decode('utf-8'), ('🐜').decode('utf-8'),
          ('🐞').decode('utf-8'), ('🐌').decode('utf-8'), ('🐙').decode('utf-8'), ('🐚').decode('utf-8'),
          ('🐠').decode('utf-8'), ('🐟').decode('utf-8'), ('🐬').decode('utf-8'), ('🐳').decode('utf-8'),
          ('🐋').decode('utf-8'), ('🐄').decode('utf-8'), ('🐏').decode('utf-8'), ('🐀').decode('utf-8'),
          ('🐃').decode('utf-8'), ('🐅').decode('utf-8'), ('🐇').decode('utf-8'), ('🐉').decode('utf-8'),
          ('🐎').decode('utf-8'), ('🐐').decode('utf-8'), ('🐓').decode('utf-8'), ('🐕').decode('utf-8'),
          ('🐖').decode('utf-8'), ('🐁').decode('utf-8'), ('🐂').decode('utf-8'), ('🐲').decode('utf-8'),
          ('🐡').decode('utf-8'), ('🐊').decode('utf-8'), ('🐫').decode('utf-8'), ('🐪').decode('utf-8'),
          ('🐆').decode('utf-8'), ('🐈').decode('utf-8'), ('🐩').decode('utf-8'), ('🐾').decode('utf-8'),
          ('💐').decode('utf-8'), ('🌸').decode('utf-8'), ('🌷').decode('utf-8'), ('🍀').decode('utf-8'),
          ('🌹').decode('utf-8'), ('🌻').decode('utf-8'), ('🌺').decode('utf-8'), ('🍁').decode('utf-8'),
          ('🍃').decode('utf-8'), ('🍂').decode('utf-8'), ('🌿').decode('utf-8'), ('🌾').decode('utf-8'),
          ('🍄').decode('utf-8'), ('🌵').decode('utf-8'), ('🌴').decode('utf-8'), ('🌲').decode('utf-8'),
          ('🌳').decode('utf-8'), ('🌰').decode('utf-8'), ('🌱').decode('utf-8'), ('🌼').decode('utf-8'),
          ('🌐').decode('utf-8'), ('🌞').decode('utf-8'), ('🌝').decode('utf-8'), ('🌚').decode('utf-8'),
          ('🌑').decode('utf-8'), ('🌒').decode('utf-8'), ('🌓').decode('utf-8'), ('🌔').decode('utf-8'),
          ('🌕').decode('utf-8'), ('🌖').decode('utf-8'), ('🌗').decode('utf-8'), ('🌘').decode('utf-8'),
          ('🌜').decode('utf-8'), ('🌛').decode('utf-8'), ('🌙').decode('utf-8'), ('🌍').decode('utf-8'),
          ('🌎').decode('utf-8'), ('🌏').decode('utf-8'), ('🌋').decode('utf-8'), ('🌌').decode('utf-8'),
          ('🌠').decode('utf-8'), ('⭐').decode('utf-8'), ('☀').decode('utf-8'), ('⛅').decode('utf-8'),
          ('☁').decode('utf-8'), ('⚡').decode('utf-8'), ('☔').decode('utf-8'), ('❄').decode('utf-8'),
          ('⛄').decode('utf-8'), ('🌀').decode('utf-8'), ('🌁').decode('utf-8'), ('🌈').decode('utf-8'),
          ('🌊').decode('utf-8'), ('🎍').decode('utf-8'), ('💝').decode('utf-8'), ('🎎').decode('utf-8'),
          ('🎒').decode('utf-8'), ('🎓').decode('utf-8'), ('🎏').decode('utf-8'), ('🎆').decode('utf-8'),
          ('🎇').decode('utf-8'), ('🎐').decode('utf-8'), ('🎑').decode('utf-8'), ('🎃').decode('utf-8'),
          ('👻').decode('utf-8'), ('🎅').decode('utf-8'), ('🎄').decode('utf-8'), ('🎁').decode('utf-8'),
          ('🎋').decode('utf-8'), ('🎉').decode('utf-8'), ('🎊').decode('utf-8'), ('🎈').decode('utf-8'),
          ('🎌').decode('utf-8'), ('🔮').decode('utf-8'), ('🎥').decode('utf-8'), ('📷').decode('utf-8'),
          ('📹').decode('utf-8'), ('📼').decode('utf-8'), ('💿').decode('utf-8'), ('📀').decode('utf-8'),
          ('💽').decode('utf-8'), ('💾').decode('utf-8'), ('💻').decode('utf-8'), ('📱').decode('utf-8'),
          ('☎').decode('utf-8'), ('📞').decode('utf-8'), ('📟').decode('utf-8'), ('📠').decode('utf-8'),
          ('📡').decode('utf-8'), ('📺').decode('utf-8'), ('📻').decode('utf-8'), ('🔊').decode('utf-8'),
          ('🔉').decode('utf-8'), ('🔈').decode('utf-8'), ('🔇').decode('utf-8'), ('🔔').decode('utf-8'),
          ('🔕').decode('utf-8'), ('📢').decode('utf-8'), ('📣').decode('utf-8'), ('⏳').decode('utf-8'),
          ('⌛').decode('utf-8'), ('⏰').decode('utf-8'), ('⌚').decode('utf-8'), ('🔓').decode('utf-8'),
          ('🔒').decode('utf-8'), ('🔏').decode('utf-8'), ('🔐').decode('utf-8'), ('🔑').decode('utf-8'),
          ('🔎').decode('utf-8'), ('💡').decode('utf-8'), ('🔦').decode('utf-8'), ('🔆').decode('utf-8'),
          ('🔅').decode('utf-8'), ('🔌').decode('utf-8'), ('🔋').decode('utf-8'), ('🔍').decode('utf-8'),
          ('🛁').decode('utf-8'), ('🛀').decode('utf-8'), ('🚿').decode('utf-8'), ('🚽').decode('utf-8'),
          ('🔧').decode('utf-8'), ('🔩').decode('utf-8'), ('🔨').decode('utf-8'), ('🚪').decode('utf-8'),
          ('🚬').decode('utf-8'), ('💣').decode('utf-8'), ('🔫').decode('utf-8'), ('🔪').decode('utf-8'),
          ('💊').decode('utf-8'), ('💉').decode('utf-8'), ('💰').decode('utf-8'), ('💴').decode('utf-8'),
          ('💵').decode('utf-8'), ('💷').decode('utf-8'), ('💶').decode('utf-8'), ('💳').decode('utf-8'),
          ('💸').decode('utf-8'), ('📲').decode('utf-8'), ('📧').decode('utf-8'), ('📥').decode('utf-8'),
          ('📤').decode('utf-8'), ('✉').decode('utf-8'), ('📩').decode('utf-8'), ('📨').decode('utf-8'),
          ('📯').decode('utf-8'), ('📫').decode('utf-8'), ('📪').decode('utf-8'), ('📬').decode('utf-8'),
          ('📭').decode('utf-8'), ('📮').decode('utf-8'), ('📦').decode('utf-8'), ('📝').decode('utf-8'),
          ('📄').decode('utf-8'), ('📃').decode('utf-8'), ('📑').decode('utf-8'), ('📊').decode('utf-8'),
          ('📈').decode('utf-8'), ('📉').decode('utf-8'), ('📜').decode('utf-8'), ('📋').decode('utf-8'),
          ('📅').decode('utf-8'), ('📆').decode('utf-8'), ('📇').decode('utf-8'), ('📁').decode('utf-8'),
          ('📂').decode('utf-8'), ('✂').decode('utf-8'), ('📌').decode('utf-8'), ('📎').decode('utf-8'),
          ('✒').decode('utf-8'), ('✏').decode('utf-8'), ('📏').decode('utf-8'), ('📐').decode('utf-8'),
          ('📕').decode('utf-8'), ('📗').decode('utf-8'), ('📘').decode('utf-8'), ('📙').decode('utf-8'),
          ('📓').decode('utf-8'), ('📔').decode('utf-8'), ('📒').decode('utf-8'), ('📚').decode('utf-8'),
          ('📖').decode('utf-8'), ('🔖').decode('utf-8'), ('📛').decode('utf-8'), ('🔬').decode('utf-8'),
          ('🔭').decode('utf-8'), ('📰').decode('utf-8'), ('🎨').decode('utf-8'), ('🎬').decode('utf-8'),
          ('🎤').decode('utf-8'), ('🎧').decode('utf-8'), ('🎼').decode('utf-8'), ('🎵').decode('utf-8'),
          ('🎶').decode('utf-8'), ('🎹').decode('utf-8'), ('🎻').decode('utf-8'), ('🎺').decode('utf-8'),
          ('🎷').decode('utf-8'), ('🎸').decode('utf-8'), ('👾').decode('utf-8'), ('🎮').decode('utf-8'),
          ('🃏').decode('utf-8'), ('🎴').decode('utf-8'), ('🀄').decode('utf-8'), ('🎲').decode('utf-8'),
          ('🎯').decode('utf-8'), ('🏈').decode('utf-8'), ('🏀').decode('utf-8'), ('⚽').decode('utf-8'),
          ('⚾').decode('utf-8'), ('🎾').decode('utf-8'), ('🎱').decode('utf-8'), ('🏉').decode('utf-8'),
          ('🎳').decode('utf-8'), ('⛳').decode('utf-8'), ('🚵').decode('utf-8'), ('🚴').decode('utf-8'),
          ('🏁').decode('utf-8'), ('🏇').decode('utf-8'), ('🏆').decode('utf-8'), ('🎿').decode('utf-8'),
          ('🏂').decode('utf-8'), ('🏊').decode('utf-8'), ('🏄').decode('utf-8'), ('🎣').decode('utf-8'),
          ('☕').decode('utf-8'), ('🍵').decode('utf-8'), ('🍶').decode('utf-8'), ('🍼').decode('utf-8'),
          ('🍺').decode('utf-8'), ('🍻').decode('utf-8'), ('🍸').decode('utf-8'), ('🍹').decode('utf-8'),
          ('🍷').decode('utf-8'), ('🍴').decode('utf-8'), ('🍕').decode('utf-8'), ('🍔').decode('utf-8'),
          ('🍟').decode('utf-8'), ('🍗').decode('utf-8'), ('🍖').decode('utf-8'), ('🍝').decode('utf-8'),
          ('🍛').decode('utf-8'), ('🍤').decode('utf-8'), ('🍱').decode('utf-8'), ('🍣').decode('utf-8'),
          ('🍥').decode('utf-8'), ('🍙').decode('utf-8'), ('🍘').decode('utf-8'), ('🍚').decode('utf-8'),
          ('🍜').decode('utf-8'), ('🍲').decode('utf-8'), ('🍢').decode('utf-8'), ('🍡').decode('utf-8'),
          ('🍳').decode('utf-8'), ('🍞').decode('utf-8'), ('🍩').decode('utf-8'), ('🍮').decode('utf-8'),
          ('🍦').decode('utf-8'), ('🍨').decode('utf-8'), ('🍧').decode('utf-8'), ('🎂').decode('utf-8'),
          ('🍰').decode('utf-8'), ('🍪').decode('utf-8'), ('🍫').decode('utf-8'), ('🍬').decode('utf-8'),
          ('🍭').decode('utf-8'), ('🍯').decode('utf-8'), ('🍎').decode('utf-8'), ('🍏').decode('utf-8'),
          ('🍊').decode('utf-8'), ('🍋').decode('utf-8'), ('🍒').decode('utf-8'), ('🍇').decode('utf-8'),
          ('🍉').decode('utf-8'), ('🍓').decode('utf-8'), ('🍑').decode('utf-8'), ('🍈').decode('utf-8'),
          ('🍌').decode('utf-8'), ('🍐').decode('utf-8'), ('🍍').decode('utf-8'), ('🍠').decode('utf-8'),
          ('🍆').decode('utf-8'), ('🍅').decode('utf-8'), ('🌽').decode('utf-8'), ('🏠').decode('utf-8'),
          ('🏡').decode('utf-8'), ('🏫').decode('utf-8'), ('🏢').decode('utf-8'), ('🏣').decode('utf-8'),
          ('🏥').decode('utf-8'), ('🏦').decode('utf-8'), ('🏪').decode('utf-8'), ('🏩').decode('utf-8'),
          ('🏨').decode('utf-8'), ('💒').decode('utf-8'), ('⛪').decode('utf-8'), ('🏬').decode('utf-8'),
          ('🏤').decode('utf-8'), ('🌇').decode('utf-8'), ('🌆').decode('utf-8'), ('🏯').decode('utf-8'),
          ('🏰').decode('utf-8'), ('⛺').decode('utf-8'), ('🏭').decode('utf-8'), ('🗼').decode('utf-8'),
          ('🗾').decode('utf-8'), ('🗻').decode('utf-8'), ('🌄').decode('utf-8'), ('🌅').decode('utf-8'),
          ('🌃').decode('utf-8'), ('🗽').decode('utf-8'), ('🌉').decode('utf-8'), ('🎠').decode('utf-8'),
          ('🎡').decode('utf-8'), ('⛲').decode('utf-8'), ('🎢').decode('utf-8'), ('🚢').decode('utf-8'),
          ('⛵').decode('utf-8'), ('🚤').decode('utf-8'), ('🚣').decode('utf-8'), ('⚓').decode('utf-8'),
          ('🚀').decode('utf-8'), ('✈').decode('utf-8'), ('💺').decode('utf-8'), ('🚁').decode('utf-8'),
          ('🚂').decode('utf-8'), ('🚊').decode('utf-8'), ('🚉').decode('utf-8'), ('🚞').decode('utf-8'),
          ('🚆').decode('utf-8'), ('🚄').decode('utf-8'), ('🚅').decode('utf-8'), ('🚈').decode('utf-8'),
          ('🚇').decode('utf-8'), ('🚝').decode('utf-8'), ('🚋').decode('utf-8'), ('🚃').decode('utf-8'),
          ('🚎').decode('utf-8'), ('🚌').decode('utf-8'), ('🚍').decode('utf-8'), ('🚙').decode('utf-8'),
          ('🚘').decode('utf-8'), ('🚗').decode('utf-8'), ('🚕').decode('utf-8'), ('🚖').decode('utf-8'),
          ('🚛').decode('utf-8'), ('🚚').decode('utf-8'), ('🚨').decode('utf-8'), ('🚓').decode('utf-8'),
          ('🚔').decode('utf-8'), ('🚒').decode('utf-8'), ('🚑').decode('utf-8'), ('🚐').decode('utf-8'),
          ('🚲').decode('utf-8'), ('🚡').decode('utf-8'), ('🚟').decode('utf-8'), ('🚠').decode('utf-8'),
          ('🚜').decode('utf-8'), ('💈').decode('utf-8'), ('🚏').decode('utf-8'), ('🎫').decode('utf-8'),
          ('🚦').decode('utf-8'), ('🚥').decode('utf-8'), ('⚠').decode('utf-8'), ('🚧').decode('utf-8'),
          ('🔰').decode('utf-8'), ('⛽').decode('utf-8'), ('🏮').decode('utf-8'), ('🎰').decode('utf-8'),
          ('♨').decode('utf-8'), ('🗿').decode('utf-8'), ('🎪').decode('utf-8'), ('🎭').decode('utf-8'),
          ('📍').decode('utf-8'), ('🚩').decode('utf-8'), ('1⃣').decode('utf-8'), ('3⃣').decode('utf-8'),
          ('4⃣').decode('utf-8'), ('5⃣').decode('utf-8'), ('6⃣').decode('utf-8'), ('7⃣').decode('utf-8'),
          ('8⃣').decode('utf-8'), ('9⃣').decode('utf-8'), ('0⃣').decode('utf-8'), ('🔟').decode('utf-8'),
          ('🔢').decode('utf-8'), ('#⃣').decode('utf-8'), ('🔣').decode('utf-8'), ('⬆').decode('utf-8'),
          ('⬇').decode('utf-8'), ('⬅').decode('utf-8'), ('➡').decode('utf-8'), ('🔠').decode('utf-8'),
          ('🔡').decode('utf-8'), ('🔤').decode('utf-8'), ('↗').decode('utf-8'), ('↖').decode('utf-8'),
          ('↘').decode('utf-8'), ('↙').decode('utf-8'), ('↔').decode('utf-8'), ('↕').decode('utf-8'),
          ('🔄').decode('utf-8'), ('◀').decode('utf-8'), ('▶').decode('utf-8'), ('🔼').decode('utf-8'),
          ('🔽').decode('utf-8'), ('↩').decode('utf-8'), ('↪').decode('utf-8'), ('ℹ').decode('utf-8'),
          ('⏪').decode('utf-8'), ('⏩').decode('utf-8'), ('⏫').decode('utf-8'), ('⏬').decode('utf-8'),
          ('⤵').decode('utf-8'), ('⤴').decode('utf-8'), ('🆗').decode('utf-8'), ('🔀').decode('utf-8'),
          ('🔁').decode('utf-8'), ('🔂').decode('utf-8'), ('🆕').decode('utf-8'), ('🆙').decode('utf-8'),
          ('🆒').decode('utf-8'), ('🆓').decode('utf-8'), ('🆖').decode('utf-8'), ('📶').decode('utf-8'),
          ('🎦').decode('utf-8'), ('🈁').decode('utf-8'), ('🈯').decode('utf-8'), ('🈳').decode('utf-8'),
          ('🈵').decode('utf-8'), ('🈴').decode('utf-8'), ('🈲').decode('utf-8'), ('🉐').decode('utf-8'),
          ('🈹').decode('utf-8'), ('🈺').decode('utf-8'), ('🈶').decode('utf-8'), ('🈚').decode('utf-8'),
          ('🚻').decode('utf-8'), ('🚹').decode('utf-8'), ('🚺').decode('utf-8'), ('🚼').decode('utf-8'),
          ('🚾').decode('utf-8'), ('🚰').decode('utf-8'), ('🚮').decode('utf-8'), ('🅿').decode('utf-8'),
          ('♿').decode('utf-8'), ('🚭').decode('utf-8'), ('🈷').decode('utf-8'), ('🈸').decode('utf-8'),
          ('🈂').decode('utf-8'), ('🛂').decode('utf-8'), ('🛄').decode('utf-8'), ('🛅').decode('utf-8'),
          ('🛃').decode('utf-8'), ('🉑').decode('utf-8'), ('㊙').decode('utf-8'), ('㊗').decode('utf-8'),
          ('🆑').decode('utf-8'), ('🆘').decode('utf-8'), ('🆔').decode('utf-8'), ('🚫').decode('utf-8'),
          ('🔞').decode('utf-8'), ('📵').decode('utf-8'), ('🚯').decode('utf-8'), ('🚱').decode('utf-8'),
          ('🚳').decode('utf-8'), ('🚷').decode('utf-8'), ('🚸').decode('utf-8'), ('⛔').decode('utf-8'),
          ('✳').decode('utf-8'), ('❇').decode('utf-8'), ('❎').decode('utf-8'), ('✅').decode('utf-8'),
          ('✴').decode('utf-8'), ('💟').decode('utf-8'), ('🆚').decode('utf-8'), ('📳').decode('utf-8'),
          ('📴').decode('utf-8'), ('🆎').decode('utf-8'), ('🅾').decode('utf-8'), ('💠').decode('utf-8'),
          ('➿').decode('utf-8'), ('♻').decode('utf-8'), ('♈').decode('utf-8'), ('♉').decode('utf-8'),
          ('♊').decode('utf-8'), ('♋').decode('utf-8'), ('♌').decode('utf-8'), ('♍').decode('utf-8'),
          ('♎').decode('utf-8'), ('♏').decode('utf-8'), ('♐').decode('utf-8'), ('♑').decode('utf-8'),
          ('♒').decode('utf-8'), ('♓').decode('utf-8'), ('⛎').decode('utf-8'), ('🔯').decode('utf-8'),
          ('🏧').decode('utf-8'), ('💹').decode('utf-8'), ('💲').decode('utf-8'), ('💱').decode('utf-8'),
          ('©').decode('utf-8'), ('®').decode('utf-8'), ('™').decode('utf-8'), ('‼').decode('utf-8'),
          ('⁉').decode('utf-8'), ('❗').decode('utf-8'), ('❓').decode('utf-8'), ('❕').decode('utf-8'),
          ('❔').decode('utf-8'), ('🔝').decode('utf-8'), ('🔚').decode('utf-8'), ('🔙').decode('utf-8'),
          ('🔜').decode('utf-8'), ('🔃').decode('utf-8'), ('🕛').decode('utf-8'), ('🕧').decode('utf-8'),
          ('🕐').decode('utf-8'), ('🕜').decode('utf-8'), ('🕑').decode('utf-8'), ('🕝').decode('utf-8'),
          ('🕒').decode('utf-8'), ('🕞').decode('utf-8'), ('🕓').decode('utf-8'), ('🕟').decode('utf-8'),
          ('🕔').decode('utf-8'), ('🕠').decode('utf-8'), ('🕕').decode('utf-8'), ('🕖').decode('utf-8'),
          ('🕗').decode('utf-8'), ('🕘').decode('utf-8'), ('🕙').decode('utf-8'), ('🕚').decode('utf-8'),
          ('🕡').decode('utf-8'), ('🕢').decode('utf-8'), ('🕣').decode('utf-8'), ('🕤').decode('utf-8'),
          ('🕥').decode('utf-8'), ('🕦').decode('utf-8'), ('✖').decode('utf-8'), ('➕').decode('utf-8'),
          ('➖').decode('utf-8'), ('➗').decode('utf-8'), ('♠').decode('utf-8'), ('♥').decode('utf-8'),
          ('♣').decode('utf-8'), ('♦').decode('utf-8'), ('💮').decode('utf-8'), ('💯').decode('utf-8'),
          ('✔').decode('utf-8'), ('☑').decode('utf-8'), ('🔘').decode('utf-8'), ('🔗').decode('utf-8'),
          ('➰').decode('utf-8'), ('〰').decode('utf-8'), ('〽').decode('utf-8'), ('🔱').decode('utf-8'),
          ('◼').decode('utf-8'), ('◻').decode('utf-8'), ('◾').decode('utf-8'), ('◽').decode('utf-8'),
          ('▪').decode('utf-8'), ('▫').decode('utf-8'), ('🔺').decode('utf-8'), ('🔲').decode('utf-8'),
          ('🔳').decode('utf-8'), ('⚫').decode('utf-8'), ('⚪').decode('utf-8'), ('🔴').decode('utf-8'),
          ('🔵').decode('utf-8'), ('🔻').decode('utf-8'), ('⬜').decode('utf-8'), ('⬛').decode('utf-8'),
          ('🔶').decode('utf-8'), ('🔷').decode('utf-8'), ('🔸').decode('utf-8'), ('🔹').decode('utf-8'),
          ('🇦🇫').decode('utf-8'), ('🇦🇱').decode('utf-8'), ('🇩🇿').decode('utf-8'), ('🇦🇸').decode('utf-8'),
          ('🇦🇩').decode('utf-8'), ('🇦🇴').decode('utf-8'), ('🇦🇮').decode('utf-8'), ('🇦🇬').decode('utf-8'),
          ('🇦🇷').decode('utf-8'), ('🇦🇲').decode('utf-8'), ('🇦🇼').decode('utf-8'), ('🇦🇺').decode('utf-8'),
          ('🇦🇹').decode('utf-8'), ('🇦🇿').decode('utf-8'), ('🇧🇸').decode('utf-8'), ('🇧🇭').decode('utf-8'),
          ('🇧🇩').decode('utf-8'), ('🇧🇧').decode('utf-8'), ('🇧🇾').decode('utf-8'), ('🇧🇪').decode('utf-8'),
          ('🇧🇿').decode('utf-8'), ('🇧🇯').decode('utf-8'), ('🇧🇲').decode('utf-8'), ('🇧🇹').decode('utf-8'),
          ('🇧🇴').decode('utf-8'), ('🇧🇦').decode('utf-8'), ('🇧🇼').decode('utf-8'), ('🇧🇷').decode('utf-8'),
          ('🇻🇬').decode('utf-8'), ('🇧🇳').decode('utf-8'), ('🇧🇬').decode('utf-8'), ('🇧🇫').decode('utf-8'),
          ('🇧🇮').decode('utf-8'), ('🇰🇭').decode('utf-8'), ('🇨🇲').decode('utf-8'), ('🇨🇦').decode('utf-8'),
          ('🇨🇻').decode('utf-8'), ('🇰🇾').decode('utf-8'), ('🇨🇫').decode('utf-8'), ('🇨🇱').decode('utf-8'),
          ('🇨🇳').decode('utf-8'), ('🇨🇴').decode('utf-8'), ('🇰🇲').decode('utf-8'), ('🇨🇩').decode('utf-8'),
          ('🇨🇬').decode('utf-8'), ('🇨🇰').decode('utf-8'), ('🇨🇷').decode('utf-8'), ('🇭🇷').decode('utf-8'),
          ('🇨🇺').decode('utf-8'), ('🇨🇼').decode('utf-8'), ('🇨🇾').decode('utf-8'), ('🇨🇿').decode('utf-8'),
          ('🇩🇰').decode('utf-8'), ('🇩🇯').decode('utf-8'), ('🇩🇲').decode('utf-8'), ('🇩🇴').decode('utf-8'),
          ('🇪🇨').decode('utf-8'), ('🇪🇬').decode('utf-8'), ('🇸🇻').decode('utf-8'), ('🇬🇶').decode('utf-8'),
          ('🇪🇷').decode('utf-8'), ('🇪🇪').decode('utf-8'), ('🇪🇹').decode('utf-8'), ('🇫🇴').decode('utf-8'),
          ('🇫🇯').decode('utf-8'), ('🇫🇮').decode('utf-8'), ('🇫🇷').decode('utf-8'), ('🇬🇫').decode('utf-8'),
          ('🇹🇫').decode('utf-8'), ('🇬🇦').decode('utf-8'), ('🇬🇲').decode('utf-8'), ('🇬🇪').decode('utf-8'),
          ('🇩🇪').decode('utf-8'), ('🇬🇭').decode('utf-8'), ('🇬🇮').decode('utf-8'), ('🇬🇷').decode('utf-8'),
          ('🇬🇩').decode('utf-8'), ('🇬🇵').decode('utf-8'), ('🇬🇺').decode('utf-8'), ('🇬🇹').decode('utf-8'),
          ('🇬🇳').decode('utf-8'), ('🇬🇼').decode('utf-8'), ('🇬🇾').decode('utf-8'), ('🇭🇹').decode('utf-8'),
          ('🇭🇳').decode('utf-8'), ('🇭🇰').decode('utf-8'), ('🇭🇺').decode('utf-8'), ('🇮🇸').decode('utf-8'),
          ('🇮🇳').decode('utf-8'), ('🇮🇩').decode('utf-8'), ('🇮🇷').decode('utf-8'), ('🇮🇶').decode('utf-8'),
          ('🇮🇪').decode('utf-8'), ('🇮🇱').decode('utf-8'), ('🇮🇹').decode('utf-8'), ('🇨🇮').decode('utf-8'),
          ('🇯🇲').decode('utf-8'), ('🇯🇵').decode('utf-8'), ('🇯🇴').decode('utf-8'), ('🇰🇿').decode('utf-8'),
          ('🇰🇪').decode('utf-8'), ('🇰🇮').decode('utf-8'), ('🇰🇼').decode('utf-8'), ('🇰🇬').decode('utf-8'),
          ('🇱🇦').decode('utf-8'), ('🇱🇻').decode('utf-8'), ('🇱🇧').decode('utf-8'), ('🇱🇸').decode('utf-8'),
          ('🇱🇷').decode('utf-8'), ('🇱🇾').decode('utf-8'), ('🇱🇮').decode('utf-8'), ('🇱🇹').decode('utf-8'),
          ('🇱🇺').decode('utf-8'), ('🇲🇴').decode('utf-8'), ('🇲🇰').decode('utf-8'), ('🇲🇬').decode('utf-8'),
          ('🇲🇼').decode('utf-8'), ('🇲🇾').decode('utf-8'), ('🇲🇻').decode('utf-8'), ('🇲🇱').decode('utf-8'),
          ('🇲🇹').decode('utf-8'), ('🇲🇶').decode('utf-8'), ('🇲🇷').decode('utf-8'), ('🇲🇽').decode('utf-8'),
          ('🇲🇩').decode('utf-8'), ('🇲🇳').decode('utf-8'), ('🇲🇪').decode('utf-8'), ('🇲🇸').decode('utf-8'),
          ('🇲🇦').decode('utf-8'), ('🇲🇿').decode('utf-8'), ('🇲🇲').decode('utf-8'), ('🇳🇦').decode('utf-8'),
          ('🇳🇵').decode('utf-8'), ('🇳🇱').decode('utf-8'), ('🇳🇨').decode('utf-8'), ('🇳🇿').decode('utf-8'),
          ('🇳🇮').decode('utf-8'), ('🇳🇪').decode('utf-8'), ('🇳🇬').decode('utf-8'), ('🇳🇺').decode('utf-8'),
          ('🇰🇵').decode('utf-8'), ('🇲🇵').decode('utf-8'), ('🇳🇴').decode('utf-8'), ('🇴🇲').decode('utf-8'),
          ('🇵🇰').decode('utf-8'), ('🇵🇼').decode('utf-8'), ('🇵🇸').decode('utf-8'), ('🇵🇦').decode('utf-8'),
          ('🇵🇬').decode('utf-8'), ('🇵🇾').decode('utf-8'), ('🇵🇪').decode('utf-8'), ('🇵🇭').decode('utf-8'),
          ('🇵🇱').decode('utf-8'), ('🇵🇹').decode('utf-8'), ('🇵🇷').decode('utf-8'), ('🇶🇦').decode('utf-8'),
          ('🇷🇪').decode('utf-8'), ('🇷🇴').decode('utf-8'), ('🇷🇺').decode('utf-8'), ('🇷🇼').decode('utf-8'),
          ('🇼🇸').decode('utf-8'), ('🇸🇲').decode('utf-8'), ('🇸🇹').decode('utf-8'), ('🇸🇦').decode('utf-8'),
          ('🇸🇳').decode('utf-8'), ('🇷🇸').decode('utf-8'), ('🇸🇨').decode('utf-8'), ('🇸🇱').decode('utf-8'),
          ('🇸🇬').decode('utf-8'), ('🇸🇰').decode('utf-8'), ('🇸🇮').decode('utf-8'), ('🇸🇧').decode('utf-8'),
          ('🇸🇴').decode('utf-8'), ('🇿🇦').decode('utf-8'), ('🇰🇷').decode('utf-8'), ('🇸🇸').decode('utf-8'),
          ('🇪🇸').decode('utf-8'), ('🇱🇰').decode('utf-8'), ('🇸🇩').decode('utf-8'), ('🇸🇷').decode('utf-8'),
          ('🇸🇿').decode('utf-8'), ('🇸🇪').decode('utf-8'), ('🇨🇭').decode('utf-8'), ('🇸🇾').decode('utf-8'),
          ('🇹🇯').decode('utf-8'), ('🇹🇿').decode('utf-8'), ('🇹🇭').decode('utf-8'), ('🇹🇱').decode('utf-8'),
          ('🇹🇬').decode('utf-8'), ('🇹🇴').decode('utf-8'), ('🇹🇹').decode('utf-8'), ('🇹🇳').decode('utf-8'),
          ('🇹🇷').decode('utf-8'), ('🇹🇲').decode('utf-8'), ('🇹🇨').decode('utf-8'), ('🇹🇻').decode('utf-8'),
          ('🇺🇬').decode('utf-8'), ('🇺🇦').decode('utf-8'), ('🇦🇪').decode('utf-8'), ('🇬🇧').decode('utf-8'),
          ('🇺🇾').decode('utf-8'), ('🇺🇸').decode('utf-8'), ('🇻🇮').decode('utf-8'), ('🇺🇿').decode('utf-8'),
          ('🇻🇨').decode('utf-8'), ('🇻🇺').decode('utf-8'), ('🇻🇪').decode('utf-8'), ('🇻🇳').decode('utf-8'),
          ('🇾🇪').decode('utf-8'), ('🇿🇲').decode('utf-8'), ('🇿🇼').decode('utf-8'), ('🇦').decode('utf-8'),
          ('🇧').decode('utf-8'), ('🇨').decode('utf-8'), ('🇩').decode('utf-8'), ('🇪').decode('utf-8'),
          ('🇫').decode('utf-8'), ('🇬').decode('utf-8'), ('🇭').decode('utf-8'), ('🇮').decode('utf-8'),
          ('🇯').decode('utf-8'), ('🇰').decode('utf-8'), ('🇱').decode('utf-8'), ('🇲').decode('utf-8'),
          ('🇳').decode('utf-8'), ('🇴').decode('utf-8'), ('🇵').decode('utf-8'), ('🇶').decode('utf-8'),
          ('🇷').decode('utf-8'), ('🇸').decode('utf-8'), ('🇹').decode('utf-8'), ('🇺').decode('utf-8'),
          ('🇻').decode('utf-8'), ('🇼').decode('utf-8'), ('🇽').decode('utf-8'), ('🇾').decode('utf-8'),
          ('🇿').decode('utf-8'), ('👨‍👩‍👦').decode('utf-8'), ('👨‍👩‍👧').decode('utf-8'),
          ('👨‍👩‍👦‍👦').decode('utf-8'), ('👨‍👩‍👧‍👧').decode('utf-8'), ('👩‍👩‍👦').decode('utf-8'),
          ('👩‍👩‍👧').decode('utf-8'), ('👩‍👩‍👧‍👦').decode('utf-8'), ('👩‍👩‍👦‍👦').decode('utf-8'),
          ('👩‍👩‍👧‍👧').decode('utf-8'), ('👨‍👨‍👦').decode('utf-8'), ('👨‍👨‍👧').decode('utf-8'),
          ('👨‍👨‍👧‍👦').decode('utf-8'), ('👨‍👨‍👦‍👦').decode('utf-8'), ('👨‍👨‍👧‍👧').decode('utf-8'),
          ('👩‍❤‍👩').decode('utf-8'), ('👨‍❤‍👨').decode('utf-8'), ('👩‍❤‍💋‍👩').decode('utf-8'),
          ('👨‍❤‍💋‍👨').decode('utf-8'), ('🖖').decode('utf-8'), ('🖕').decode('utf-8'), ('🙂').decode('utf-8'),
          ('🤗').decode('utf-8'), ('🤔').decode('utf-8'), ('🙄').decode('utf-8'), ('🤐').decode('utf-8'),
          ('🤓').decode('utf-8'), ('☹').decode('utf-8'), ('🙁').decode('utf-8'), ('🙃').decode('utf-8'),
          ('🤒').decode('utf-8'), ('🤕').decode('utf-8'), ('🤑').decode('utf-8'), ('⛑').decode('utf-8'),
          ('🕵').decode('utf-8'), ('🗣').decode('utf-8'), ('🕴').decode('utf-8'), ('🤘').decode('utf-8'),
          ('🖐').decode('utf-8'), ('✍').decode('utf-8'), ('👁').decode('utf-8'), ('❣').decode('utf-8'),
          ('🕳').decode('utf-8'), ('🗯').decode('utf-8'), ('🕶').decode('utf-8'), ('🛍').decode('utf-8'),
          ('📿').decode('utf-8'), ('☠').decode('utf-8'), ('🤖').decode('utf-8'), ('🦁').decode('utf-8'),
          ('🦄').decode('utf-8'), ('🐿').decode('utf-8'), ('🦃').decode('utf-8'), ('🕊').decode('utf-8'),
          ('🦀').decode('utf-8'), ('🕷').decode('utf-8'), ('🕸').decode('utf-8'), ('🦂').decode('utf-8'),
          ('🏵').decode('utf-8'), ('☘').decode('utf-8'), ('🌶').decode('utf-8'), ('🧀').decode('utf-8'),
          ('🌭').decode('utf-8'), ('🌮').decode('utf-8'), ('🌯').decode('utf-8'), ('🍿').decode('utf-8'),
          ('🍾').decode('utf-8'), ('🍽').decode('utf-8'), ('🏺').decode('utf-8'), ('🗺').decode('utf-8'),
          ('🏔').decode('utf-8'), ('⛰').decode('utf-8'), ('🏕').decode('utf-8'), ('🏖').decode('utf-8'),
          ('🏜').decode('utf-8'), ('🏝').decode('utf-8'), ('🏞').decode('utf-8'), ('🏟').decode('utf-8'),
          ('🏛').decode('utf-8'), ('🏗').decode('utf-8'), ('🏘').decode('utf-8'), ('🏙').decode('utf-8'),
          ('🏚').decode('utf-8'), ('🛐').decode('utf-8'), ('🕋').decode('utf-8'), ('🕌').decode('utf-8'),
          ('🕍').decode('utf-8'), ('🖼').decode('utf-8'), ('🛢').decode('utf-8'), ('🛣').decode('utf-8'),
          ('🛤').decode('utf-8'), ('🛳').decode('utf-8'), ('⛴').decode('utf-8'), ('🛥').decode('utf-8'),
          ('🛩').decode('utf-8'), ('🛫').decode('utf-8'), ('🛬').decode('utf-8'), ('🛰').decode('utf-8'),
          ('🛎').decode('utf-8'), ('🛌').decode('utf-8'), ('🛏').decode('utf-8'), ('🛋').decode('utf-8'),
          ('⏱').decode('utf-8'), ('⏲').decode('utf-8'), ('🕰').decode('utf-8'), ('🌡').decode('utf-8'),
          ('⛈').decode('utf-8'), ('🌤').decode('utf-8'), ('🌥').decode('utf-8'), ('🌦').decode('utf-8'),
          ('🌧').decode('utf-8'), ('🌨').decode('utf-8'), ('🌩').decode('utf-8'), ('🌪').decode('utf-8'),
          ('🌫').decode('utf-8'), ('🌬').decode('utf-8'), ('☂').decode('utf-8'), ('⛱').decode('utf-8'),
          ('☃').decode('utf-8'), ('☄').decode('utf-8'), ('🕎').decode('utf-8'), ('🎖').decode('utf-8'),
          ('🎗').decode('utf-8'), ('🎞').decode('utf-8'), ('🎟').decode('utf-8'), ('🏷').decode('utf-8'),
          ('🏌').decode('utf-8'), ('⛸').decode('utf-8'), ('⛷').decode('utf-8'), ('⛹').decode('utf-8'),
          ('🏋').decode('utf-8'), ('🏎').decode('utf-8'), ('🏍').decode('utf-8'), ('🏅').decode('utf-8'),
          ('🏏').decode('utf-8'), ('🏐').decode('utf-8'), ('🏑').decode('utf-8'), ('🏒').decode('utf-8'),
          ('🏓').decode('utf-8'), ('🏸').decode('utf-8'), ('🕹').decode('utf-8'), ('⏭').decode('utf-8'),
          ('⏯').decode('utf-8'), ('⏮').decode('utf-8'), ('⏸').decode('utf-8'), ('⏹').decode('utf-8'),
          ('⏺').decode('utf-8'), ('🎙').decode('utf-8'), ('🎚').decode('utf-8'), ('🎛').decode('utf-8'),
          ('*⃣').decode('utf-8'), ('🖥').decode('utf-8'), ('🖨').decode('utf-8'), ('⌨').decode('utf-8'),
          ('🖱').decode('utf-8'), ('🖲').decode('utf-8'), ('📽').decode('utf-8'), ('📸').decode('utf-8'),
          ('🕯').decode('utf-8'), ('🗞').decode('utf-8'), ('🗳').decode('utf-8'), ('🖋').decode('utf-8'),
          ('🖊').decode('utf-8'), ('🖌').decode('utf-8'), ('🖍').decode('utf-8'), ('🗂').decode('utf-8'),
          ('🗒').decode('utf-8'), ('🗓').decode('utf-8'), ('🖇').decode('utf-8'), ('🗃').decode('utf-8'),
          ('🗄').decode('utf-8'), ('🗑').decode('utf-8'), ('🗝').decode('utf-8'), ('⛏').decode('utf-8'),
          ('⚒').decode('utf-8'), ('🛠').decode('utf-8'), ('⚙').decode('utf-8'), ('🗜').decode('utf-8'),
          ('⚗').decode('utf-8'), ('⚖').decode('utf-8'), ('⛓').decode('utf-8'), ('🗡').decode('utf-8'),
          ('⚔').decode('utf-8'), ('🛡').decode('utf-8'), ('🏹').decode('utf-8'), ('⚰').decode('utf-8'),
          ('⚱').decode('utf-8'), ('🏳').decode('utf-8'), ('🏴').decode('utf-8'), ('⚜').decode('utf-8'),
          ('⚛').decode('utf-8'), ('🕉').decode('utf-8'), ('✡').decode('utf-8'), ('☸').decode('utf-8'),
          ('☯').decode('utf-8'), ('✝').decode('utf-8'), ('☦').decode('utf-8'), ('⛩').decode('utf-8'),
          ('☪').decode('utf-8'), ('☮').decode('utf-8'), ('☢').decode('utf-8'), ('☣').decode('utf-8'),
          ('🗨').decode('utf-8'), ('👁‍🗨').decode('utf-8')]
tags = [['happy', 'joy', 'pleased', 'smile'], ['happy', 'joy', 'haha', 'smiley'], ['smile', 'happy', 'grinning'],
        ['proud', 'blush'], ['blush', 'pleased', 'relaxed'], ['flirt', 'wink'], ['love', 'crush', 'heart', 'eyes'],
        ['flirt', 'kissing', 'heart'], ['kissing', 'eyes'], ['kissing'], ['kissing', 'smiling', 'eyes'],
        ['prank', 'silly', 'tongue', 'winking', 'eye'], ['prank', 'tongue', 'eyes'], ['tongue'], ['flushed'], ['grin'],
        ['pensive'], ['whew', 'relieved'], ['meh', 'unamused'], ['sad', 'disappointed'], ['struggling', 'persevere'],
        ['sad', 'tear', 'cry'], ['tears', 'joy'], ['sad', 'cry', 'bawling', 'sob'], ['tired', 'sleepy'],
        ['phew', 'sweat', 'nervous', 'disappointed', 'relieved'], ['nervous', 'cold', 'sweat'],
        ['hot', 'sweat', 'smile'], ['sweat'], ['tired', 'weary'], ['upset', 'whine', 'tired'],
        ['scared', 'shocked', 'oops', 'fearful'], ['horror', 'shocked', 'scream'], ['mad', 'annoyed', 'angry'],
        ['angry', 'rage'], ['smug', 'triumph'], ['confounded'], ['happy', 'haha', 'laughing', 'satisfied'],
        ['tongue', 'lick', 'yum'], ['sick', 'ill', 'mask'], ['cool', 'sunglasses'], ['zzz', 'sleeping'], ['dizzy'],
        ['amazed', 'gasp', 'astonished'], ['nervous', 'worried'], ['frowning'], ['stunned', 'anguished'],
        ['devil', 'evil', 'horns', 'smiling', 'imp'], ['angry', 'devil', 'evil', 'horns', 'imp'],
        ['surprise', 'impressed', 'wow', 'open', 'mouth'], ['grimacing'], ['meh', 'neutral'], ['confused'],
        ['silence', 'speechless', 'hushed'], ['mute', 'silence', 'mouth'], ['angel', 'innocent'], ['smug', 'smirk'],
        ['expressionless'], ['man', 'gua', 'pi', 'mao'], ['man', 'turban'], ['police', 'law', 'cop'],
        ['helmet', 'construction', 'worker'], ['guardsman'], ['child', 'newborn', 'baby'], ['child', 'boy'],
        ['child', 'girl'], ['mustache', 'father', 'dad', 'man'], ['girls', 'woman'], ['older', 'man'],
        ['older', 'woman'], ['boy', 'person', 'blond', 'hair'], ['angel'], ['blonde', 'crown', 'royal', 'princess'],
        ['smiley', 'cat'], ['smile', 'cat'], ['heart', 'eyes', 'cat'], ['kissing', 'cat'], ['smirk', 'cat'],
        ['horror', 'scream', 'cat'], ['sad', 'tear', 'crying', 'cat'], ['joy', 'cat'], ['pouting', 'cat'],
        ['monster', 'japanese', 'ogre'], ['japanese', 'goblin'], ['monkey', 'blind', 'ignore', 'see', 'evil'],
        ['monkey', 'deaf', 'hear', 'evil'], ['monkey', 'mute', 'hush', 'speak', 'evil'],
        ['dead', 'danger', 'poison', 'skull'], ['ufo', 'alien'], ['crap', 'hankey', 'ucl', 'poop', 'shit'],
        ['burn', 'lit', 'hell', 'fire'], ['shiny', 'sparkles'], ['star2'], ['star', 'dizzy'],
        ['explode', 'boom', 'collision'], ['angry', 'anger'], ['water', 'workout', 'cum', 'sweat', 'drops'],
        ['water', 'droplet'], ['sleeping', 'zzz'], ['wind', 'blow', 'fast', 'fart', 'dash'],
        ['hear', 'sound', 'listen', 'ear'], ['look', 'see', 'watch', 'eyes'], ['smell', 'nose'], ['taste', 'tongue'],
        ['kiss', 'lips'], ['approve', 'ok', '+1', 'thumbsup'], ['disapprove', 'bury', '-1', 'thumbsdown'],
        ['somegoodshitrightthere', 'zichen', 'imperial', 'ok', 'hand'], ['attack', 'facepunch', 'punch'],
        ['power', 'wank', 'wanking', 'wanker', 'fist'], ['victory', 'peace', 'out'], ['goodbye', 'wave'],
        ['highfive', 'stop', 'hand', 'raised', 'hand'], ['open', 'hands', 'jazz', 'hands'],
        ['point', 'up', '2', 'finger', 'blaster'], ['point', 'down'], ['point', 'right'], ['point', 'left'],
        ['hooray', 'raised', 'hands'], ['please', 'hope', 'wish', 'pray'], ['point', 'up'],
        ['praise', 'applause', 'idiot', 'clap'], ['flex', 'bicep', 'strong', 'workout', 'muscle'], ['walking'],
        ['exercise', 'workout', 'marathon', 'runner', 'running'], ['dress', 'tango', 'dancer'],
        ['date', 'straight', 'godsway', 'gayiswrong', 'bible', 'couple'], ['home', 'parents', 'child', 'family'],
        ['couple', 'date', 'wrong', 'hell', 'gayconversiontherapy', 'men', 'holding', 'hands'],
        ['couple', 'date', 'hell', 'lesbianconversiontherapy', 'women', 'holding', 'hands'], ['couplekiss'],
        ['couple', 'heart'], ['bunny', 'slut', 'slag', 'dancers'], ['ok', 'woman'], ['stop', 'halt', 'good'],
        ['information', 'desk', 'person'], ['pet', 'raising', 'hand', 'teachers', 'pet'],
        ['spa', 'relaxed', 'massage', 'happy', 'ending'], ['beauty', 'haircut'], ['beauty', 'manicure', 'nail', 'care'],
        ['marriage', 'wedding', 'bride', 'veil'], ['duck', 'face', 'person', 'pouting', 'duck'],
        ['sad', 'unhappy', 'person', 'frowning'], ['respect', 'thanks', 'bow'], ['hat', 'classy', 'magic', 'tophat'],
        ['king', 'queen', 'royal', 'crown'], ['womans', 'hat'], ['sneaker', 'sport', 'running', 'athletic', 'shoe'],
        ['mans', 'shoe', 'shoe'], ['shoe', 'sandal'], ['shoe', 'high', 'heel'], ['boot'], ['shirt', 'tshirt'],
        ['shirt', 'formal', 'necktie'], ['womans', 'clothes'], ['dress'], ['marathon', 'running', 'shirt', 'sash'],
        ['pants', 'jeans'], ['kimono'], ['beach', 'bikini'], ['business', 'briefcase'], ['bag', 'handbag'],
        ['bag', 'pouch'], ['purse'], ['glasses', 'eyeglasses'], ['ribbon'], ['weather', 'rain', 'umbrella'],
        ['makeup', 'lipstick'], ['yellow', 'heart'], ['blue', 'heart'], ['purple', 'heart'], ['green', 'heart'],
        ['love', 'heart'], ['broken', 'heart'], ['heartpulse'], ['heartbeat'], ['hearts'], ['sparkling', 'heart'],
        ['revolving', 'hearts'], ['love', 'heart', 'cupid'], ['email', 'envelope', 'love'], ['lipstick', 'kiss'],
        ['wedding', 'marriage', 'engaged', 'ring'], ['diamond', 'gem'], ['user', 'bust', 'silhouette'],
        ['users', 'group', 'team', 'busts', 'silhouette'], ['comment', 'speech', 'balloon'],
        ['feet', 'tracks', 'footprints'], ['thinking', 'thought', 'balloon'], ['pet', 'dog'], ['wolf'], ['pet', 'cat'],
        ['mouse'], ['pet', 'hamster'], ['bunny', 'rabbit'], ['frog', 'meme', 'pepe'], ['tiger'], ['koala'], ['bear'],
        ['pig', 'david', 'cameron'], ['pig', 'nose'], ['cow'], ['boar'], ['monkey'], ['monkey'], ['horse'], ['sheep'],
        ['elephant'], ['panda'], ['penguin'], ['bird'], ['baby', 'chick'], ['hatched', 'chick'], ['hatching', 'chick'],
        ['chicken'], ['nikolai', 'ucl', 'snake'], ['slow', 'turtle'], ['bug'], ['bee', 'honeybee'], ['ant'],
        ['bug', 'beetle'], ['slow', 'snail'], ['octopus'], ['sea', 'beach', 'shell'], ['tropical', 'fish'], ['fish'],
        ['dolphin', 'flipper'], ['sea', 'whale'], ['whale'], ['cow'], ['ram'], ['rat'], ['water', 'buffalo'], ['tiger'],
        ['rabbit'], ['dragon'], ['speed', 'racehorse'], ['goat'], ['rooster'], ['dog'], ['pig', 'david', 'cameron'],
        ['mouse'], ['ox'], ['dragon'], ['blowfish'], ['crocodile'], ['camel'], ['desert', 'dromedary', 'camel'],
        ['leopard'], ['cat'], ['dog', 'poodle'], ['feet', 'paw', 'prints'], ['flowers', 'bouquet'],
        ['flower', 'spring', 'cherry', 'blossom'], ['flower', 'tulip'], ['luck', 'four', 'leaf', 'clover'],
        ['flower', 'rose'], ['sunflower'], ['hibiscus'], ['canada', 'maple', 'leaf'], ['leaf', 'leaves'],
        ['autumn', 'fallen', 'leaf'], ['herb'], ['ear', 'rice'], ['mushroom'], ['cactus'], ['palm', 'tree'],
        ['wood', 'evergreen', 'tree'], ['wood', 'deciduous', 'tree'], ['chestnut'], ['plant', 'seedling'], ['blossom'],
        ['world', 'global', 'international', 'globe', 'meridians'], ['summer', 'sun'], ['full', 'moon'],
        ['moon'], ['moon'], ['waxing', 'crescent', 'moon'], ['quarter', 'moon'],
        ['moon', 'waxing', 'gibbous', 'moon'], ['full', 'moon'], ['waning', 'gibbous', 'moon'],
        ['quarter', 'moon'], ['waning', 'crescent', 'moon'], ['quarter', 'moon'],
        ['quarter', 'moon'], ['night', 'crescent', 'moon'],
        ['globe', 'world', 'international', 'earth', 'africa'],
        ['globe', 'world', 'international', 'earth', 'americas'], ['globe', 'world', 'international', 'earth', 'asia'],
        ['volcano'], ['milky', 'way'], ['stars'], ['star'], ['weather', 'sunny'],
        ['weather', 'cloud', 'partly', 'sunny'], ['cloud'], ['lightning', 'thunder', 'zap'],
        ['rain', 'weather', 'umbrella'], ['winter', 'cold', 'weather', 'ice', 'snowflake'],
        ['winter', 'christmas', 'frosty', 'snowman'], ['swirl', 'cyclone', 'tornado'], ['karl', 'foggy'],
        ['pride', 'lgbt', 'lgbtq', 'gay', 'rainbow'], ['sea', 'water', 'atlantic', 'pacific', 'ocean'],
        ['bamboo', 'panflute'], ['chocolates', 'gift', 'heart'], ['dolls'], ['school', 'satchel', 'bag', 'backpack'],
        ['education', 'college', 'university', 'graduation', 'mortar', 'board', 'imperial', 'ucl'], ['flags', 'wind'],
        ['festival', 'celebration', 'fireworks', 'yay'], ['sparkler', 'fireworks'], ['wind', 'chime'],
        ['rice', 'scene'], ['halloween', 'jack', 'lantern'], ['halloween', 'ghost', 'spooky', 'casper', 'spook'],
        ['christmas', 'claus', 'santa'], ['christmas', 'tree'], ['present', 'birthday', 'christmas', 'gift'],
        ['tanabata', 'tree'], ['party', 'tada'], ['celebration', 'confetti', 'ball'], ['party', 'birthday', 'balloon'],
        ['crossed', 'flags'], ['fortune', 'future', 'mystic', 'crystal', 'ball'], ['film', 'video', 'movie', 'camera'],
        ['photo', 'dslr', 'camera'], ['amateur', 'video', 'camera'], ['vhs', 'tapes', 'sextapes'], ['cd'], ['dvd'],
        ['minidisc'], ['save', 'floppy', 'disk'], ['desktop', 'screen', 'computer', 'pc', 'mac'],
        ['smartphone', 'mobile', 'phone', 'android', 'iphone'], ['phone', 'telephone'],
        ['phone', 'call', 'telephone', 'receiver'], ['pager'], ['fax'],
        ['signal', 'satellite', 'nsa', 'snowden', 'privacy'], ['tv'], ['podcast', 'radio'], ['volume', 'loud', 'sound'],
        ['volume', 'sound', 'quiet'], ['speaker', 'sound'], ['sound', 'volume', 'silent', 'mute'],
        ['sound', 'notification', 'bell', 'shame'], ['volume', 'off', 'bell'], ['announcement', 'loudspeaker'],
        ['mega', 'laserbeam'], ['time', 'hourglass', 'flowing', 'sand'], ['time', 'hourglass'],
        ['morning', 'alarm', 'clock'], ['time', 'watch'], ['security', 'unlock'], ['security', 'private', 'lock'],
        ['lock', 'ink', 'pen'], ['security', 'lock', 'key'], ['lock', 'password', 'key'],
        ['magnifying', 'right', 'investigate', 'investigation'], ['idea', 'aha', 'eureka', 'light', 'bulb'],
        ['flashlight', 'fleshlight'], ['high', 'brightness'], ['low', 'brightness'], ['electric', 'plug'],
        ['power', 'battery'], ['search', 'zoom', 'mag'], ['bathtub'], ['shower', 'bath'], ['bath', 'shower'],
        ['wc', 'shitbasket', 'poop', 'loo', 'lavatory', 'toilet'], ['tool', 'wrench'], ['nut', 'bolt'],
        ['tool', 'hammer'], ['door'], ['cigarette', 'smoking'], ['boom', 'bomb', 'muslim', 'islam', 'jihad'],
        ['shoot', 'weapon', 'bullet', 'gun', 'syria', 'america'],
        ['cut', 'chop', 'hocho', 'knife', 'edgy', 'shank', 'stab', 'mugged', 'murder', 'kill'],
        ['health', 'medicine', 'pill', 'drug', 'drugs', 'weed'],
        ['health', 'hospital', 'needle', 'syringe', 'drugs', 'drug', 'addicition', 'heroin'],
        ['dollar', 'cream', 'moneybag', 'jew', 'jewish'], ['yen'], ['money', 'dollar'], ['pound', 'money'], ['euro'],
        ['subscription', 'credit', 'card'], ['dollar', 'money', 'wings'], ['call', 'incoming', 'calling'],
        ['email', 'mail', 'outlook'], ['inbox', 'tray'], ['outbox', 'tray'], ['letter', 'email', 'envelope', 'mail'],
        ['envelope', 'arrow'], ['incoming', 'envelope'], ['postal', 'horn'], ['mailbox'], ['mailbox'],
        ['mailbox', 'mail'], ['mailbox', 'mail'], ['postbox'], ['shipping', 'package', 'present'],
        ['document', 'note', 'memo', 'pencil'], ['document', 'page', 'facing', 'up'], ['page', 'curl'],
        ['bookmark', 'tabs'], ['stats', 'metrics', 'bar', 'chart'],
        ['graph', 'metrics', 'bitcoin', 'chart', 'upwards', 'trend'],
        ['graph', 'metrics', 'pound', 'brexit', 'chart', 'downwards', 'trend'], ['document', 'scroll'], ['clipboard'],
        ['calendar', 'schedule', 'date'], ['schedule', 'calendar'], ['card', 'index'], ['directory', 'file', 'folder'],
        ['open', 'file', 'folder'], ['cut', 'scissors', 'snip'], ['location', 'pushpin'], ['paperclip'],
        ['black', 'nib'], ['pencil2'], ['straight', 'ruler'], ['triangular', 'ruler'], ['book'], ['green', 'book'],
        ['blue', 'book'], ['orange', 'book', 'red'], ['notebook'], ['notebook', 'decorative', 'cover'], ['ledger'],
        ['library', 'books'], ['book', 'open', 'book'], ['bookmark'], ['name', 'badge'],
        ['science', 'laboratory', 'investigate', 'microscope'], ['telescope', 'space', 'science'],
        ['press', 'newspaper'], ['design', 'paint', 'art'], ['film', 'clapper'], ['sing', 'microphone'],
        ['music', 'earphones', 'headphones'], ['musical', 'score', 'mozart'], ['musical', 'note'],
        ['music', 'song', 'tune', 'notes'], ['piano', 'musical', 'keyboard'], ['violin'], ['trumpet'], ['saxophone'],
        ['rock', 'guitar'], ['game', 'retro', 'space', 'invader', 'alien'],
        ['play', 'controller', 'console', 'video', 'game'], ['black', 'joker'], ['flower', 'playing', 'cards'],
        ['mahjong'], ['dice', 'gambling', 'game', 'die'], ['target', 'dart'], ['sports', 'football'],
        ['sports', 'basketball'], ['sports', 'soccer', 'football'], ['sports', 'baseball'], ['sports', 'tennis'],
        ['pool', 'billiards', '8ball'], ['rugby', 'football'], ['bowling'], ['golf'], ['mountain', 'bicyclist'],
        ['bicyclist', 'bike', 'cycle'], ['milestone', 'finish', 'checkered', 'flag'], ['horse', 'racing'],
        ['award', 'contest', 'winner', 'trophy'], ['ski'], ['snowboarder'], ['swimmer', 'swim'], ['surfer'],
        ['fishing', 'pole', 'fish'], ['cafe', 'espresso', 'coffee'], ['green', 'breakfast', 'tea'], ['sake'],
        ['milk', 'baby', 'bottle'], ['drink', 'beer'], ['drinks', 'cheers', 'beers'], ['drink', 'drunk', 'cocktail'],
        ['summer', 'vacation', 'tropical', 'drink'], ['wine', 'glass'], ['cutlery', 'fork', 'knife'], ['pizza'],
        ['burger', 'hamburger'], ['fries'], ['meat', 'chicken', 'poultry', 'leg'], ['meat', 'bone'],
        ['pasta', 'spaghetti'], ['curry'], ['tempura', 'fried', 'shrimp'], ['bento'], ['sushi'], ['fish', 'cake'],
        ['rice', 'ball'], ['rice', 'cracker'], ['rice'], ['noodle', 'ramen'], ['stew'], ['oden'], ['dango'],
        ['breakfast', 'egg'], ['toast', 'bread'], ['doughnut'], ['custard'], ['icecream'], ['ice', 'cream'],
        ['shaved', 'ice'], ['party', 'birthday', 'alone', 'old'], ['dessert', 'cake'], ['cookie'], ['chocolate', 'bar'],
        ['sweet', 'candy'], ['lollipop'], ['honey', 'pot'], ['apple', 'fruit'], ['fruit', 'green', 'apple'],
        ['tangerine', 'fruit'], ['lemon', 'fruit'], ['fruit', 'cherries'], ['grapes', 'fruit'], ['watermelon', 'fruit'],
        ['fruit', 'strawberry'], ['peach', 'fruit'], ['melon', 'fruit'], ['fruit', 'banana'], ['pear', 'fruit'],
        ['pineapple', 'fruit'], ['sweet', 'potato'],
        ['aubergine', 'eggplant', 'penis', 'dick', 'schlong', 'cock', 'sex', 'boner'], ['tomato', 'vegetable'],
        ['corn'], ['house', 'home'], ['house', 'garden'], ['school'], ['office'], ['post', 'office'], ['hospital'],
        ['bank'], ['convenience', 'store'], ['love', 'hotel', 'brothel'], ['hotel'], ['marriage', 'wedding'],
        ['church'], ['department', 'store'], ['european', 'post', 'office'], ['city', 'sunrise'], ['city', 'sunset'],
        ['japanese', 'castle'], ['european', 'castle'], ['camping', 'tent'], ['factory'], ['tokyo', 'tower'],
        ['japan', 'nippon', 'island'], ['mount', 'fuji'], ['sunrise', 'over', 'mountains'], ['sunrise'],
        ['night', 'stars'], ['statue', 'liberty'], ['bridge', 'at', 'night'], ['carousel', 'horse'],
        ['ferris', 'wheel'], ['fountain'], ['roller', 'coaster'], ['ship'], ['boat', 'sailboat'], ['ship', 'speedboat'],
        ['rowboat'], ['ship', 'anchor'], ['ship', 'launch', 'space', 'elon', 'rocket'], ['flight', 'airplane'],
        ['seat'], ['helicopter'], ['train', 'steam', 'locomotive'], ['tram'], ['station'], ['mountain', 'railway'],
        ['train2', 'train', 'hype'], ['train', 'bullettrain', 'side'], ['train', 'bullettrain', 'front', 'hype'],
        ['light', 'rail', 'train'], ['metro', 'underground', 'tube', 'subway'], ['monorail'], ['train'],
        ['railway', 'car'], ['trolleybus'], ['bus'], ['oncoming', 'bus'], ['blue', 'car'],
        ['oncoming', 'automobile', 'car'], ['car', 'red', 'car'], ['taxi'], ['oncoming', 'taxi'],
        ['articulated', 'lorry'], ['truck'], ['911', 'emergency', 'rotating', 'light', 'important', 'warning'],
        ['police', 'car', 'cops', 'blm'], ['oncoming', 'police', 'car'], ['fire', 'engine'], ['ambulance'], ['minibus'],
        ['bicycle', 'bike'], ['aerial', 'tramway'], ['suspension', 'railway'], ['mountain', 'cableway'],
        ['tractor', 'farm'], ['barber'], ['wait', 'coach', 'busstop'],
        ['golden', 'journey', 'admit', 'concert', 'ticket'],
        ['semaphore', 'red', 'green', 'amber', 'stop', 'pedestrian', 'crossing', 'vertical', 'traffic', 'light'],
        ['traffic', 'light'], ['error', 'hazard', 'danger', 'wip', 'warning'],
        ['wip', 'building', 'work', 'progress', 'construction'], ['beginner'],
        ['motor', 'car', 'petroleum', 'diesel', 'petrol', 'fuelpump'], ['japanese', 'izakaya', 'lantern', 'lantern'],
        ['casino', 'gambling', 'slot', 'machine'], ['spa', 'warm', 'pool', 'hotsprings'],
        ['easter', 'island', 'stone', 'moyai'], ['festival', 'glamping', 'circus', 'tent'],
        ['mask', 'theater', 'drama', 'performing', 'arts'], ['lollipop', 'location', 'round', 'pushpin'],
        ['flag', 'minesweeper', 'triangular', 'flag', 'post'], ['onef'], ['three'], ['four'], ['five'], ['six'],
        ['seven'], ['eight'], ['nine'], ['zero'], ['keycap', 'ten'], ['numbers', '1234'], ['number', 'hash'],
        ['symbols'], ['arrow', 'up'], ['arrow', 'down'], ['arrow', 'left'], ['arrow', 'right'],
        ['letters', 'capital', 'abcd'], ['abcd'], ['alphabet', 'abc'], ['arrow', 'upper', 'right'],
        ['arrow', 'upper', 'left'], ['arrow', 'lower', 'right'], ['arrow', 'lower', 'left'], ['left', 'right', 'arrow'],
        ['arrow', 'up', 'down'], ['loading', 'wait', 'update', 'sync', 'arrows', 'counterclockwise'],
        ['back', 'arrow', 'backward'], ['next', 'arrow', 'forward'], ['arrow', 'up', 'small'],
        ['arrow', 'down', 'small'], ['back', 'return', 'leftwards', 'arrow', 'hook'],
        ['next', 'arrow', 'right', 'hook'], ['info', 'help', 'information', 'source'], ['rewind'], ['fast', 'forward'],
        ['arrow', 'double', 'up'], ['arrow', 'double', 'down'], ['arrow', 'heading', 'down'],
        ['arrow', 'heading', 'up'], ['yes', 'ok'], ['shuffle', 'twisted', 'rightwards', 'arrows'], ['loop', 'repeat'],
        ['repeat', 'single', 'repeat'], ['fresh', 'new'], ['up'], ['coolio', 'cool'], ['freedom', 'free'],
        ['ng'], ['signal', 'strength', 'wifi', 'signal', 'strength'], ['theatre', 'film', 'movie', 'cinema'], ['koko'],
        ['u6307'], ['u7a7a'], ['u6e80'], ['u5408'], ['u7981'], ['ideograph', 'advantage'], ['u5272'], ['u55b6'],
        ['u6709'], ['u7121'], ['toilet', 'restroom'],
        ['washroom', 'toilet', 'loo', 'wc', 'wash', 'closet', 'facilities', 'gentlemens', 'bathroom', 'mens'],
        ['washroom', 'toilet', 'loo', 'wc', 'wash', 'closet', 'facilities', 'ladies', 'bathroom', 'womens'],
        ['baby'],
        ['washroom', 'toilet', 'loo', 'wc', 'wash', 'closet', 'facilities', 'gentlemens', 'bathroom', 'restroom', 'wc'],
        ['cup', 'glass', 'water', 'drink', 'potable', 'water'], ['recycle', 'rubbish', 'trash', 'dispose', 'litter'],
        ['parking'], ['disabled', 'accessibility', 'wheelchair'], ['smoking'], ['u6708'], ['u7533'], ['sa'],
        ['immigration', 'airport', 'visa', 'id', 'identification', 'check', 'passport', 'control'],
        ['airport', 'baggage', 'claim'], ['lost', 'found', 'left', 'luggage'], ['customs'], ['accept'], ['secret'],
        ['congratulations'], ['cl'], ['save', 'souls', 'help', 'emergency', 'sos'], ['identification', 'id'],
        ['block', 'forbidden', 'entry', 'sign'], ['alcohol', 'cigarette', 'law', 'underage'], ['mobile', 'phones'],
        ['clean', 'litter'], ['non-potable', 'water'], ['bicycles'], ['pedestrians'],
        ['school', 'children', 'crossing'], ['forbidden', 'limit', 'entry'], ['star', 'eight', 'spoked', 'asterisk'],
        ['sparkle'], ['scottish', 'scotland', 'negative', 'squared', 'cross', 'mark'],
        ['tick', 'yes', 'ok', 'nice', 'yeah', 'white', 'check', 'mark'], ['eight', 'pointed', 'black', 'star'],
        ['heart', 'decoration'], ['war', 'vs'], ['vibration', 'mode'], ['mute', 'off', 'mobile', 'phone', 'off'],
        ['ab'], ['o2'], ['diamond', 'shape', 'dot', 'inside'], ['loop'], ['environment', 'green', 'recycle'], ['aries'],
        ['taurus'], ['gemini'], ['cancer'], ['leo'], ['virgo'], ['libra'], ['scorpius'], ['sagittarius'], ['capricorn'],
        ['aquarius'], ['pisces'], ['ophiuchus'], ['six', 'pointed', 'star'], ['atm'],
        ['finance', 'stock', 'office', 'bank', 'chart'], ['rich', 'money', 'dollars', 'heavy', 'dollar', 'sign'],
        ['currency', 'exchange'], ['copyright', 'patent'], ['registered'], ['trademark', 'trade', 'mark', 'tm'],
        ['surprise', 'bangbang'], ['interrobang'], ['bang', 'exclamation', 'heavy', 'exclamation', 'mark'],
        ['confused', 'question'], ['grey', 'exclamation'], ['grey', 'question'], ['top'], ['end'], ['back'], ['soon'],
        ['arrows', 'clockwise'], ['clock12'], ['clock1230'], ['clock1'], ['clock130'], ['time', 'watch', 'clock2'],
        ['clock230'], ['clock3'], ['clock330'], ['clock4'], ['clock430'], ['clock5'], ['clock530'], ['clock6'],
        ['clock7'], ['clock8'], ['clock9'], ['clock10'], ['clock11'], ['clock630'], ['clock730'], ['clock830'],
        ['clock930'], ['clock1030'], ['clock1130'], ['heavy', 'multiplication'], ['heavy', 'plus', 'sign'],
        ['heavy', 'minus', 'sign'], ['heavy', 'division', 'sign'], ['cards', 'gambling', 'spades'],
        ['cards', 'gambling', 'hearts'], ['cards', 'gambling', 'clubs'], ['cards', 'gambling', 'diamonds'],
        ['white', 'flower'], ['nice', 'score', 'perfect', '100'], ['heavy', 'check', 'mark'],
        ['ballot', 'box', 'check'], ['radio', 'button'], ['hyperlink', 'chain', 'link'], ['curly', 'loop'],
        ['wavy', 'dash'], ['part', 'alternation', 'mark'], ['sea', 'trident'], ['black', 'medium', 'square'],
        ['white', 'medium', 'square'], ['black', 'medium', 'small', 'square'], ['white', 'medium', 'small', 'square'],
        ['black', 'small', 'square'], ['white', 'small', 'square'], ['small', 'red', 'triangle'],
        ['black', 'square', 'button'], ['white', 'square', 'button'], ['black', 'circle'], ['white', 'circle'],
        ['red', 'circle'], ['large', 'blue', 'circle'], ['small', 'red', 'triangle', 'down'],
        ['white', 'large', 'square'], ['black', 'large', 'square'], ['large', 'orange', 'diamond'],
        ['large', 'blue', 'diamond'], ['small', 'orange', 'diamond'], ['small', 'blue', 'diamond'],
        ['afghanistan'], ['albania'], ['algeria'],
        ['american samoa'], ['andorra'], ['angola'], ['anguilla'],
        ['antigua and barbuda'], ['argentina'], ['armenia'],
        ['aruba'],
        ['australia'],
        ['austria'], ['azerbaijan'], ['bahamas'], ['bahrain'],
        ['bangladesh'], ['barbados'], ['belarus'],
        ['belgium'], ['belize'], ['benin'], ['bermuda'],
        ['bhutan'], ['bolivia'], ['bosnia and herzegovina'],
        ['botswana'], ['brazil'], ['british virgin islands'],
        ['brunei darussalam'], ['bulgaria'], ['burkina faso'],
        ['burundi'], ['cambodia'], ['cameroon'],
        ['canada'], ['cape verde'],
        ['cayman islands'], ['central african republic'], ['chile'],
        ['china'], ['colombia'],
        ['comoros'], ['democratic republic of the congo'],
        ['republic of the congo'], ['cook islands'], ['costa rica'],
        ['croatia'], ['cuba'], ['curacao'], ['cyprus'],
        ['czech republic'], ['denmark'], ['djibouti'], ['dominica'],
        ['dominican republic'], ['ecuador'], ['egypt'],
        ['el salvador'], ['equatorial guinea'], ['eritrea'],
        ['estonia'], ['ethiopia'], ['faroe islands'], ['fiji'],
        ['finland'], ['france'], ['french guiana'],
        ['french southern territories'], ['gabon'], ['gambia'],
        ['georgia'], ['germany'],
        ['ghana'], ['gibraltar'], ['greece'],
        ['grenada'], ['guadeloupe'], ['guam'], ['guatemala'],
        ['guinea'], ['guinea-bissau'], ['guyana'], ['haiti'],
        ['honduras'], ['hong kong'], ['hungary'], ['iceland'],
        ['india'], ['indonesia'], ['iran'], ['iraq'],
        ['ireland'], ['israel'], ['italy'],
        ['ivory coast'], ['jamaica'], ['japan'], ['jordan'],
        ['kazakhstan'], ['kenya'], ['kiribati'], ['kuwait'],
        ['kyrgyzstan'], ['laos'], ['latvia'], ['lebanon'],
        ['lesotho'], ['liberia'], ['libya'], ['liechtenstein'],
        ['lithuania'], ['luxembourg'], ['macau'], ['macedonia'],
        ['madagascar'], ['malawi'], ['malaysia'], ['maldives'],
        ['mali'], ['malta'], ['martinique'], ['mauritania'],
        ['mexico'], ['moldova'], ['mongolia'],
        ['montenegro'], ['montserrat'], ['morocco'], ['mozambique'],
        ['myanmar'], ['namibia'], ['nepal'], ['netherlands'],
        ['new caledonia'], ['new zealand'], ['nicaragua'],
        ['niger'], ['nigeria'], ['niue'], ['north korea'],
        ['northern mariana islands'], ['norway'], ['oman'],
        ['pakistan'], ['palau'], ['palestine'], ['panama'],
        ['papua new guinea'], ['paraguay'], ['peru'],
        ['philippines'], ['polnad'], ['portugal'],
        ['puerto rico'], ['qatar'], ['reunion'],
        ['romania'], ['russia'], ['rwanda'],
        ['samoa'], ['san marino'], ['sao tome and principe'],
        ['saudi arabia'], ['senegal'], ['serbia'],
        ['seychelles'], ['sierra leone'], ['singapore'],
        ['slovakia'], ['slovenia'], ['solomon islands'],
        ['somalia'], ['south africa'], ['south korea'],
        ['south sudan'], ['spain'], ['sri lanka'],
        ['sudan'], ['suriname'], ['swaziland'], ['sweden'],
        ['switzerland'], ['syria'], ['tajikistan'],
        ['tanzania'], ['thailand'], ['east timor'], ['togo'],
        ['tonga'], ['trinidad and tobago'], ['tunisia'], ['turkey'],
        ['turkmenistan'], ['turks and caicos islands'], ['tuvalu'],
        ['uganda'], ['ukraine'], ['united arab emirates'],
        ['united kingdom', 'uk'], ['uruguay'],
        ['united states of america', 'us', 'america', 'usa'],
        ['us virgin islands'], ['uzbekistan'], ['st vincent grenadines'],
        ['vanuatu'], ['venezuela'], ['vietnam'], ['yemen'],
        ['zambia'], ['zimbabwe'], ['qwertyuiopasdf'], ['qwertyuiopasdf'],
        ['qwertyuiopasdf'], ['qwertyuiopasdf'], ['qwertyuiopasdf'], ['qwertyuiopasdf'], ['qwertyuiopasdf'],
        ['qwertyuiopasdf'], ['qwertyuiopasdf'], ['qwertyuiopasdf'], ['qwertyuiopasdf'], ['qwertyuiopasdf'],
        ['qwertyuiopasdf'], ['qwertyuiopasdf'], ['qwertyuiopasdf'], ['qwertyuiopasdf'], ['qwertyuiopasdf'],
        ['qwertyuiopasdf'], ['qwertyuiopasdf'], ['qwertyuiopasdf'], ['qwertyuiopasdf'], ['qwertyuiopasdf'],
        ['qwertyuiopasdf'], ['qwertyuiopasdf'], ['qwertyuiopasdf'], ['qwertyuiopasdf'],
        ['family', 'man', 'woman', 'boy', 'family', 'man', 'woman', 'boy'],
        ['family', 'man', 'woman', 'girl', 'family', 'man', 'woman', 'girl'],
        ['family', 'man', 'woman', 'boy', 'family', 'man', 'woman', 'boy', 'boy'],
        ['family', 'man', 'woman', 'girl', 'family', 'man', 'woman', 'girl', 'girl'],
        ['family', 'woman', 'boy', 'adopted', 'wrong', 'family', 'woman', 'woman', 'boy'],
        ['family', 'woman', 'girl', 'adopted', 'wrong', 'family', 'woman', 'woman', 'girl'],
        ['family', 'woman', 'girl', 'boy', 'adopted', 'wrong', 'family', 'woman', 'woman', 'girl', 'boy'],
        ['family', 'woman', 'boy', 'adopted', 'wrong', 'family', 'woman', 'woman', 'boy', 'boy'],
        ['family', 'woman', 'girl', 'adopted', 'wrong', 'family', 'woman', 'woman', 'girl', 'girl'],
        ['family', 'man', 'boy', 'adopted', 'wrong', 'family', 'man', 'man', 'boy'],
        ['family', 'man', 'girl', 'family', 'man', 'man', 'girl'],
        ['family', 'man', 'girl', 'boy', 'adopted', 'wrong', 'family', 'man', 'man', 'girl', 'boy'],
        ['family', 'man', 'boy', 'adopted', 'wrong', 'family', 'man', 'man', 'boy', 'boy'],
        ['family', 'man', 'girl', 'adopted', 'wrong', 'family', 'man', 'man', 'girl', 'girl'],
        ['couple', 'heart', 'woman', 'lesbian', 'gay', 'wrong', 'couple', 'heart', 'woman', 'woman'],
        ['couple', 'heart', 'man', 'gay', 'homosexual', 'couple', 'heart', 'man', 'man'],
        ['couple', 'kiss', 'woman', 'couplekiss', 'woman', 'woman'],
        ['couple', 'kiss', 'man', 'gay', 'couplekiss', 'man', 'man'], ['vulcan', 'salute', 'spock', 'vulcan', 'salute'],
        ['middle', 'finger', 'fuck', 'curse'], ['slightly', 'smiling'], ['hugging', 'hug', 'hugs', 'love'],
        ['thinking', 'think', 'thinker'], ['eye', 'roll', 'rolling', 'eyes'],
        ['zipper', 'mouth', 'zip', 'sealed', 'lips', 'lips', 'sealed'], ['nerd', 'nerdy', 'geek'], ['frowning'],
        ['slightly', 'frowning'], ['upside', 'down', 'flipped', 'what'], ['sick', 'ill', 'thermometer'],
        ['injured', 'head', 'bandage', 'head', 'bandaged', 'bandaged'], ['money', 'mouth', 'money'],
        ['helmet', 'white', 'cross'], ['detective', 'sleuth', 'private', 'eye', 'spy'],
        ['speaking', 'head', 'silhouette'], ['hovering', 'man', 'levitating', 'man'],
        ['horns', 'sign', 'rock', 'heavy', 'metal', 'devil', 'fingers'],
        ['raised', 'hand', 'fingers', 'splayed', 'splayed', 'hand'], ['writing', 'writing', 'hand'], ['eye'],
        ['exclamation', 'heart'], ['hole'], ['right', 'anger', 'bubble', 'zig', 'zag', 'bubble'],
        ['dark', 'sunglasses'], ['shopping', 'bags'], ['prayer', 'beads', 'dhikr', 'beads', 'rosary', 'beads'],
        ['skull', 'crossbones'], ['robot', 'bot'], ['lion', 'cute', 'lion', 'timid', 'lion'], ['unicorn'],
        ['chipmunk', 'squirrel'], ['turkey'], ['dove', 'dove', 'peace'], ['crab', 'cancer'], ['spider'],
        ['spider', 'web', 'cobweb'], ['scorpion'], ['rosette'], ['shamrock', 'st', 'patrick'],
        ['hot', 'pepper', 'chili', 'pepper', 'spice', 'spicy'], ['cheese'], ['hot', 'dog'], ['taco'],
        ['burrito', 'wrap'], ['popcorn'], ['champagne', 'sparkling', 'wine'], ['fork', 'knife', 'plate'],
        ['amphora', 'jar', 'vase'], ['world', 'map'], ['snow', 'capped', 'mountain', 'mont', 'fuji'], ['mountain'],
        ['camping', 'campsite', 'tent'], ['breach'], ['desert'], ['desert', 'island'],
        ['national', 'park', 'tree', 'green'], ['stadium'], ['classical', 'building'],
        ['building', 'construction', 'crane'], ['house', 'buildings', 'multiple', 'houses'], ['cityscape'],
        ['derelict', 'house', 'old', 'house', 'abandoned', 'house'],
        ['worship', 'building', 'worship', 'religious', 'building', 'religious'], ['kaaba', 'mecca'],
        ['mosque', 'minaret', 'domed', 'roof'], ['synagogue', 'temple', 'jewish'],
        ['picture', 'frame', 'painting', 'gallery'], ['oil', 'drum'],
        ['motorway', 'highway', 'road', 'interstate', 'freeway'], ['railway', 'track'], ['passenger', 'ship'],
        ['ferry'], ['motor', 'boat'], ['small', 'airplane'], ['airplane', 'departure', 'take', 'off'],
        ['airplane', 'arriving', 'airplane', 'arrival', 'landing'], ['satellite'], ['bellhop', 'bell'],
        ['sleeping', 'accommodation'], ['bed', 'bedroom'], ['couch', 'lamp', 'couch', 'sofa', 'lounge'], ['stopwatch'],
        ['timer', 'clock'], ['mantelpiece', 'clock'], ['thermometer', 'hot', 'weather', 'temperature'],
        ['thunder', 'cloud', 'rain'], ['white', 'sun', 'small', 'cloud'], ['white', 'sun', 'behind', 'cloud'],
        ['white', 'sun', 'behind', 'cloud', 'rain'], ['cloud', 'rain'], ['cloud', 'snow'], ['cloud', 'lightning'],
        ['cloud', 'tornado'], ['fog'], ['wind', 'blowing', 'mother', 'nature', 'blowing', 'wind'], ['open', 'umbrella'],
        ['planted', 'umbrella', 'umbrella', 'ground'], ['snowman', 'snow', 'snowing', 'snowman'],
        ['comet', 'light', 'beam', 'blue', 'beam'], ['menorah', 'candelabrum', 'chanukiah', 'jew', 'jewish'],
        ['military', 'medal', 'military', 'decoration'], ['reminder', 'ribbon', 'awareness', 'ribbon', 'cancer'],
        ['film', 'frames'], ['admission', 'ticket'], ['label'], ['golfer', 'golf', 'club'],
        ['ice', 'skate', 'ice', 'skating'], ['skier'], ['person', 'ball'], ['weight', 'lifter'],
        ['racing', 'car', 'formula', 'f1'], ['racing', 'motorcycle', 'motorcycle', 'motorbike'],
        ['sports', 'medal', 'sports', 'decoration'], ['cricket'], ['volleyball'], ['field', 'hockey'],
        ['ice', 'hockey'], ['table', 'tennis', 'ping', 'pong'], ['badminton'], ['joystick'],
        ['black', 'right', 'pointing', 'double', 'triangle', 'vertical', 'bar'],
        ['black', 'right', 'pointing', 'triangle', 'double', 'vertical', 'bar'],
        ['black', 'left', 'pointing', 'double', 'triangle', 'vertical', 'bar'], ['double', 'vertical', 'bar'],
        ['black', 'square', 'for', 'stop'], ['black', 'circle', 'for', 'record'], ['studio', 'microphone'],
        ['level', 'slider'], ['control', 'knobs'], ['keycap', 'asterisk', 'star', 'keycap'],
        ['desktop', 'computer', 'pc', 'tower', 'imac'], ['printer'], ['keyboard'],
        ['computer', 'mouse', 'three', 'button', 'mouse'], ['trackball'], ['film', 'projector'], ['camera', 'flash'],
        ['candle'], ['rolled', 'up', 'newspaper', 'newspaper', 'delivery'], ['ballot', 'ballot', 'box'],
        ['lower', 'left', 'fountain', 'pen'], ['lower', 'left', 'ballpoint', 'pen'], ['lower', 'left', 'paintbrush'],
        ['lower', 'left', 'crayon'], ['card', 'index', 'dividers'], ['spiral', 'note', 'pad'],
        ['spiral', 'calendar', 'pad'], ['linked', 'paperclips'], ['card', 'file', 'box'], ['file', 'cabinet'],
        ['wastebasket'], ['old', 'key'], ['pick'], ['hammer', 'pick'], ['hammer', 'wrench'], ['gear'], ['compression'],
        ['alembic'], ['scales', 'scales', 'justice'], ['chains'], ['dagger', 'dagger', 'knife', 'knife', 'weapon'],
        ['crossed', 'swords'], ['shield'], ['bow', 'arrow', 'bow', 'arrow', 'archery'], ['coffin', 'funeral', 'casket'],
        ['funeral', 'urn'], ['waving', 'white', 'flag'], ['waving', 'black', 'flag'], ['fleur', 'de', 'lis', 'scouts'],
        ['atom', 'atom'], ['om', 'pranava', 'aumkara', 'omkara'], ['star', 'david'], ['wheel', 'dharma'],
        ['yin', 'yang'], ['latin', 'cross', 'christian', 'cross'], ['orthodox', 'cross'],
        ['shinto', 'shrine', 'kami', 'michi'], ['star', 'crescent', 'star', 'crescent'], ['peace', 'peace', 'sign'],
        ['radioactive', 'radioactive', 'radioactive', 'sign'],
        ['biohazard', 'biohazard', 'biohazard', 'sign', 'toxic', 'nasty'], ['left', 'speech', 'bubble'],
        ['eye', 'speech', 'bubble', 'witness']]

## EMOJIFIER - CORE ##

wordvec = gensim.models.Word2Vec.load_word2vec_format(os.getcwd() + '/GoogleNews-vectors-negative300.bin', binary=True)

threshold = 0.02 # score at which emoji is chosen

num_emojis = 3 # maximum number of emojis to return
decay_choose = 10 # decay in emoji value based on how many emojis already chosen

num_words = 1 # maximum number of words to be considered
decay_words = 20 # decay in word value based on how far back it is

sim_weight = 5 # determines weight (exponent) applied to similarity of *individual* tags

memeifier_on = False # full memeification on or off
emojifier_on = False # full emojification on or off

selected_emojis = []

def sample(old_prime, prime):

    old_prime = old_prime.strip()
    old_words = old_prime.split()

    prime = prime.strip()
    words = prime.split()

    change_indices = []
    for i in range(0, len(words)):
        if i >= len(old_words):
            change_indices.append(i)
        elif words[i] != old_words[i]:
            change_indices.append(i)

        if i >= len(selected_emojis):
            selected_emojis.append("")
    for i in range(0, len(selected_emojis)):
        if i >= len(words):
            selected_emojis[i] = ""

    if len(words) == 1:
        change_indices = [0]
        selected_emojis[0] = ""

    for change_index in change_indices:
        values = []
        for i in range(max(0, change_index - num_words + 1), change_index + 1):
            if i == max(0, change_index - num_words + 1):
                values = getValue(depunctuate(words[i]))
            else:
                values = [x + y for x, y in zip(map(lambda x: x / decay_words, values), getValue(depunctuate(words[i])))]
    
        emojistoadd = ""
        if values != []:
            sortedemo = sorted(zip(emojis, values), key = lambda x: x[1])
            for i in range(num_emojis):
                e, v = sortedemo[-(i + 1)]
                if v >= threshold * (1 + decay_choose * i / num_emojis):
                    emojistoadd += e
    
        if not emojistoadd == "":
            selected_emojis[change_index] = " "
            selected_emojis[change_index] += emojistoadd

    finalstring = ""
    for i in range(len(words)):
        finalstring += " "
        finalstring += words[i]
        finalstring += selected_emojis[i]

    if memeifier_on:
        depunctuated = depunctuate(finalstring)
        meme = memeify(depunctuated)
        finalstring = finalstring + meme[len(depunctuated) - 1:]

    if emojifier_on:
        finalstring = emojify(finalstring)

    return finalstring[1:]

def depunctuate(string):
    return ''.join(filter(lambda c: str.isalpha(c) or c == ' ', string)).lower()


def getValue(lastword):
    values = map(lambda x: similarity(lastword, x), tags)
    if np.max(values) == 0:
        values = map(lambda x: findtag(lastword, x), tags)
    return values


def getsimilarity(lastword, tocheck):
    if lastword in wordvec.vocab and tocheck in wordvec.vocab:
        return wordvec.similarity(lastword, tocheck)
    else:
        return 0


def similarity(lastword, localtags):
    values = map(lambda x: getsimilarity(lastword, x), localtags)
    values = map(lambda x: pow(x, sim_weight), values)
    return np.average(values)


def findtag(lastword, localtags):
    if lastword in localtags:
        return threshold * 5
    else:
        return 0

## EMOJIFIER - FULL ##

alphabet = "abcdefghijklmnopqrstuvwxyz"

emojibet = [('🅰').decode('utf-8'), ('🅱').decode('utf-8'), ('©').decode('utf-8'), ('↩').decode('utf-8'),
          ('🎼').decode('utf-8'), ('🎏').decode('utf-8'), ('🌊').decode('utf-8'), ('🙌').decode('utf-8'),
          ('ℹ').decode('utf-8'), ('🎷').decode('utf-8'), ('🎋').decode('utf-8'), ('🕒').decode('utf-8'),
          ('Ⓜ').decode('utf-8'), ('♑').decode('utf-8'), ('⚙️').decode('utf-8'), ('🅿').decode('utf-8'),
          ('🔍').decode('utf-8'), ('®️️').decode('utf-8'), ('⚡').decode('utf-8'), ('🌴').decode('utf-8'),
          ('⛎').decode('utf-8'), ('♈').decode('utf-8'), ('📈').decode('utf-8'), ('⚒').decode('utf-8'),
          ('✌').decode('utf-8'), ('Ⓩ').decode('utf-8')]

def emojify(message):
    return_message = ""
    for c in message:
        if c in alphabet:
            return_message += emojibet[alphabet.index(c)]
        else:
            return_message += c
    return return_message

## MEMEIFIER ##

args_save_dir ='save'
args_n = 500
args_sample = -2
with open(os.path.join(args_save_dir, 'config.pkl'), 'rb') as f:
    saved_args = cPickle.load(f)
with open(os.path.join(args_save_dir, 'chars_vocab.pkl'), 'rb') as f:
    chars, vocab = cPickle.load(f)
model = Model(saved_args, True, useDropout=False)
init = tf.global_variables_initializer()
sess = tf.Session()
sess.run(init)
saver = tf.train.Saver(tf.global_variables())
ckpt = tf.train.get_checkpoint_state(args_save_dir)
if ckpt and ckpt.model_checkpoint_path:
    saver.restore(sess, ckpt.model_checkpoint_path)

def memeify(args_prime):
    return model.sample(sess, chars, vocab, args_n, args_prime, args_sample)

## SERVER ##

TCP_IP = 'localhost'
TCP_PORT = 3000
BUFFER_SIZE = 1024

data = ''

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind((TCP_IP, TCP_PORT))
s.listen(1)

print("Server is running.")

#string = ""
#while True:
#    new_string = raw_input("enter new input: ")
#    old_string = string
#    string = new_string
#    print("old string was: " + old_string)
#    print("string is: " + string)
#    print(sample(old_string,string))

while True:
    conn, addr = s.accept()
    old_data = data
    data = conn.recv(BUFFER_SIZE)
    if data:
        conn.send(sample(old_data,data))

    conn.close()
