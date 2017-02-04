#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import print_function
import numpy as np
import tensorflow as tf

import argparse
import time
import os
from six.moves import cPickle

from utils import TextLoader
from model import Model

from six import text_type
import os

import sys
reload(sys)
sys.setdefaultencoding('UTF8')

def main():
    initializeModel()

def initializeModel():
    cwd = os.getcwd()
    save_dir = cwd + "/save/"
    print(save_dir)
    with open(os.path.join(save_dir, 'config.pkl'), 'rb') as f:
        saved_args = cPickle.load(f)
    with open(os.path.join(save_dir, 'chars_vocab.pkl'), 'rb') as f:
        chars, vocab = cPickle.load(f)
    model = Model(saved_args, True, useDropout=False)
    with tf.Session() as sess:
        tf.initialize_all_variables().run()
        saver = tf.train.Saver(tf.all_variables())
        ckpt = tf.train.get_checkpoint_state(save_dir)
        if ckpt and ckpt.model_checkpoint_path:
            saver.restore(sess, ckpt.model_checkpoint_path)
            print("Initalized")
            message = ""
            while(message != "exit"):
                message = raw_input("Type your stuff:")
                print(message)
                print(sample(message, chars, sess, vocab, model))

emojis = ['👌', '😂', '👀', '😍', '💯', '✔', '🎃', '❤', '🔥', '💦', '👍', '👏', '😭', '👻', '💩', '🏻', '👎', '🐸', '😊', '👋', '🍕', '😉', '🏿', '☑', '🔫', '🏼', '😘', '👴', '🍆', '👭', '♥', '🎶', '🔝', '😎', '🌃', '🎺', '😁', '🙏', '🔪', '🇺', '🇸', '😢', '🙌', '😏', '😩', '💖', '😀', '🚫', '☺', '😱', '❌', '😜', '👅', '💀', '💉', '😄', '🏽', '❗', '😅', '😆', '💕', '🎵', '🙇', '💪', '🏾', '🎩', '😈', '😃', '😡', '👉', '❓', '👽', '😳', '🍅', '‍', '👊', '🐍', '✋', '😑', '🚨', '👟', '🎉', '😋', '😬', '🇧', '♊', '🇬', '✌', '🐃', '❄', '⃣', '😔', '📅', '😛', '🍑', '💃', '‼', '🆗', '😫', '😤', '😞', '🌊', '💰', '😝', '🍍', '💋', '💜', '👨', '😐', '😒', '😠', '💘', '🔑', '🙈', '🍴', '💥', '👦', '💙', '✖', '😇', '😥', '👈', '✊', '✨', '☀', '😕', '💁', '😻', '😮', '🚬', '💍', '👓', '🙅', '🆙', '💨', '🅰', '😲', '😵', '😷', '🤔', '⚡', '😨', '👪', '🏢', '☝', '👮', '💒', '💾', '⭐', '😰', '👑', '💣', '💻', '🐻', '👆', '🇹', '👩', '⬆', '🙊', '👳', '✈', '🎈', '☁', '🔔', '✅', '🍁', '😣', '😚', '😖', '💗', '🎂', '🐒', '🙋', '😹', '💚', '🌟', '💧', '🇮', '🖕', '⬇', '🍻', '🌹', '☠', '👶', '🍇', '😙', '▶', '🐛', '👼', '🐐', '🇨', '👧', '😦', '➡', '😓', '💸', '🏃', '💔', '😴', '👄', '😽', '🐶', '🍌', '🍺', '😌', '😧', '⬛', '🚂', '🍓', '🎤', '😪', '🍝', '🤑', '🐔', '💵', '🇦', '👐', '👇', '👿', '🇷', '💛', '👹', '🇲', '🐝', '🏆', '💫', '🌚', '🍋', '🐱', '⚠', '💞', '🌽', '💲', '😯', '👬', '😶', '💓', '🚀', '😟', '🍞', '☕', '🐓', '🍀', '🎷', '🐧', '🙀', '💤', '🤗', '🌈', '🇪', '🎊', '🎼', '🙆', '👖', '🌌', '💎', '🙉', '🚃', '🍪', '👱', '💇', '💢', '🌎', '💺', '🌞', '🗽', '🍟', '🍔', '🐴', '🇳', '🦄', '🛰', '💏', '🍎', '🍗', '🔛', '🔭', '🙄', '🍰', '💊', '🐼', '📝', '😸', '🌙', '♻', '🔨', '▪', '👯', '👁', '🌿', '🐕', '🙃', '🌍', '🗣', '👺', '🌲', '🏀', '🇵', '🇩', '🌴', '😗', '😺', '👸', '🐳', '🚲', '📢', '🍩', '👂', '👫', '⚾', '🆘', '🍷', '🚚', '🎅', '⏰', '🕔', '🕙', '🕥', '⚽', '🐢', '🐷', '🤓', '⌛', '🎸', '🤘', '🌸', '🚺', '💟', '🙂', '⬜', '⬅', '🇱', '🍤', '📒', '📞', '🐙', '🚓', '🐈', '🐵', '😿', '👤', '🍼', '📣', '🚹', '🔞', '♣', '👕', '♦', '📚', '➕', '🏄', '🇻', '🈶', '⛵', '🐬', '🌝', '🔊', '🚗', '🕣', '☹', '💭', '🕯', '🚶', '🐦', '⁉', '💝', '⚪', '⛔', '🌏', '😾', '🎁', '💅', '☎', '🕛', '🔴', '😼', '🎓', '🏈', '🐀', '🎆', '⏳', '🌳', '🌶', '🐟', '🎧', '📲', '🌋', '🐣', '🚪', '👵', '📖', '💑', '♠', '✂', '💡', '🍾', '⌚', '🦀', '🐾', '👥', '🔯', '🚮', '🚑', '🍦', '🐥', '🏥', '🇰', '🏠', '🆒', '👠', '📱', '🐎', '🉐', '🚩', '👙', '🍏', '🍸', '🍳', '🐺', '☢', '👃', '🚔', '🐊', '🇽', '🐰', '🍊', '🙎', '💬', '🇫', '📕', '🙍', '🍬', '🍉', '🅾', '🌷', '🔦', '👾', '❎', '🏌', '🍒', '✡', '🏊', '⭕', '◻', '☔', '⚰', '🌱', '🤖', '👲', '💂', '➖', '♨', '🌠', '👣', '🗿', '🍫', '❕', '🔺', '🐤', '🍭', '🐮', '🍖', '🎄', '📯', '🐠', '💄', '⚓', '🍃', '🎯', 'ℹ', '🐲', '🌼', '🖐', '🐘', '🕐', '💆', '👷', '🇴', '❔', '🔜', '🍹', '🐨', '🔵', '🐩', '📈', '🏡', '🕵', '🅱', '♏', '📷', '🐭', '💐', '◾', '🚧', '🐋', '🤕', '🎥', '👰', '✝', '🍄', '🇯', '🇭', '🐄', '🌰', '📦', '🗡', '◼', '🍽', '🎮', '🔳', '🐯', '🌻', '✏', '🐑', '🌺', '🍵', '👞', '🐖', '⛽', '🆕', '🤐', '🇾', '🚿', '🌾', '🚼', '🐞', '🎀', '🔮', '🚷', '🏅', '⚔', '🌵', '🐌', '🍶', '◀', '🔙', '🚽', '🕑', '🍂', '🐉', '🔟', '🎲', '🚋', '✍', '📧', '🐇', '⛄', '🌮', '🐽', '🏋', '🍯', '🎟', '📠', '♿', '🤒', '📍', '💳', '🚁', '🏒', '🔚', '🐜', '🔒', '🛀', '👔', '♒', '🎹', '🙁', '🛫', '👗', '🌐', '🔎', '🍲', '🏇', '🎨', '🌭', '📹', '🍣', '💶', '🚒', '🦃', '⤵', '💽', '📸', '🔍', '📬', '☮', '☪', '🌀', '👢', '🔢', '🍠', '©', '💼', '🍜', '🇿', '🚙', '🏫', '🎇', '⏩', '🔄', '📉', '💴', '🕊', '🎻', '🛬', '🐗', '⚫', '🚴', '📟', '🚌', '🏳', '⏱', '🔇', '📘', '🏎', '📜', '⤴', '♎', '〰', '➰', '🎭', '🔌', '🎬', '🌑', '🔬', '🏚', '⚖', '🏁', '☣', '↩', '🔁', '🌛', '🚦', '↕', '🍧', '🆓', '🌅', '☃', '⛪', '🕒', '🗑', '☄', '🌜', '🔧', '🐂', '🔼', '▫', '🌧', '📛', '🔱', '🎾', '🗻', '🧀', '🐏', '🦁', '⚒', '🍥', '🖥', '💌', '💷', '🚸', '🖖', '🌬', '〽', '🎱', '📴', '🗓', '🏛', '🌕', '🚘', '🇼', '🔋', '🐆', '📆', '🎣', '🔐', '👛', '🛠', '🐹', '🌫', '📁', '🏹', '⛳', '👒', '🚜', '📗', '⛏', '🚕', '📵', '🕶', '⏬', '🔩', '📨', '♓', '📰', '🍈', '®', '🎙', '🛂', '🖒', '🕓', '🗨', '✉', '❣', '🐡', '🌪', '📑', '🌉', '✴', '🐅', '📃', '🚄', '🍱', '✒', '📄', '🎳', '🏪', '🌄', '👜', '🍙', '🕝', '🔘', '💹', '🔃', '👡', '🏩', '🚏', '🏤', '⛰', '🔷', '🕠', '🗾', '🏰', '🕖', '🍡', '🐪', '🔶', '❇', '🔆', '⛓', '📻', '♑', '🚢', '☘', '🌨', '🕰', '🕧', '👘', '🐚', '🔖', '🕳', '📶', '🌩', '🏉', '🍨', '🚅', '👚', '🎰', '📌', '☯', '🔓', '🌆', '🎚', '🖊', '🛌', '🍮', '🚛', '🏭', '🍛', '🐁', '🔽', '🏣', '↗', '🚖', '☂', '🔲', '🚾', '🚐', '🛡', '↔', '🚤', '🕜', '📽', '📂', '🔹', '🕹', '🔻', '🌡', '📼', '📀', '🕚', '📊', '↪', '🗯', '🕗', '⏫', '💠', '🕌', '🗼', '📓', '🅿', '⏲', '🛏', '⚙', '🏦', '🔏', '🍚', '🃏', '♐', '💈', '🛎', '🕦', '🤣', '🍿', '⌨', '🎫', '🕤', '🍐', '🐫', '🌯', '📤', '🏕', '💱', '🎎', '♌', '🈁', '🚞', '🎞', '🔗', '🚣', '🎢', '🔸', '📩', '♍', '🖇', '⛈', '🕴', '📪', '🎒', '🕘', '🔕', '🕋', '🎗', '⛅', '🏗', '↘', '🏜', '⏪', '📥', '📐', '🗝', '↖', '🎖', '🛩', '🌇', '🅴', '🏍', '🏂', '📙', '🖋', '🛐', '🚰', '🚵', '🚉', '🕟', '🎪', '🔀', '🎽', '🔉', '📎', '🎠', '✳', '🏖', '🚎', '🏐', '🚇', '🏙', '🏮', '📮', '🕕', '🇶', '🔈', '🎌', '🎛', '🉑', '🍘', '🌒', '🚈', '🆎', '🗞', '🚊', '🖱', '🚭', '🖲', '🌂', '🚯', '🕞', '💮', '🐿', '📔', '⛸', '🎐', '↙', '🖓', '🎑', '🌔', '🏨', '🔂', '🕸', '🎡', '🦂', '♈', '🎿', '🚻', '🌗', '⚜', '🏘', '🌖', '📏', '🌘', '🛁', '🌓', '👝', '🍢', '🏧', '🖨', '🎋', '🏵', '⛷', '🕢', '🕷', '🗳', '➗', '🚝', '🏯', '⛲', '🏞', '🚆', '🔅', '⛹', '🕡', '🏏', '🖑', '🆃', '⛑', '🈵', '⛴', '🏬', '🖍', '◽', '🚱', '🛢', '♉', '⚱', '⚗', '📿', '⏯', '🗺', '📭', '🖼', '🕎', '🚥', '🗃', '⛎', '㊙', '➿', '🔣', '🆂', '🛳', '📫', '🔠', '🏓', '🚍', '🈳', '🕍', '🛅', '🗜', '🏸', '🕉', '🛣', '⏹', '📋', '🛍', '㊗', '🈲', '🛃', '🏔', '🎍', '🛥', '🔤', '🌤', '🛋', '🆁', '🌦', '⚛', '⛱', '🈷', '🚡', '☦', '🎏', '🀄', '🤢', '🔡', '🈚', '🚠', '🏝', '🏑', '🏺', '🔰', '🅸', '☸', '🖌', '🏷', '⏭', '🈴', '🏟', '🤷', '🎦', '🛄', '🌥', '🈯', '🎴', '📳', '🚳', '🆄', '🗄', '🗒', '🏴', '🅷', '🈹', '🌁', '🤙', '⏸', '🗂', '🤤', '⏮', '⛩', '🦑', '🚟', '🦇', '🈺', '🛤', '🅞', '📇', '🅵', '🅔', '🖎', '🅢', '⏺', '🤵', '🅣', '🅳', '🈸', '🆚', '🤦', '🦍', '🥓', '🅶', '🂡', '🤠', '🦲', '🅝', '🥚', '🅘', '🤡', '🅡', '🅐', '🅗', '🄴', '🤺', '🥊', '🅛', '🄲', '🕿', '🥒', '🄸', '🅚', '🅤', '🅦', '🦋', '🖙', '🅒', '🄽', '🆇', '🤴', '🤧', '🄷', '🤚', '🤳', '🅓', '🗩', '🗵', '🖚', '🥕', '🥜', '🤞', '🗶', '🅹', '🥗', '🥙', '🢫', '🄶', '🢡', '🅕', '🅖', '🥘', '🥖', '🄱', '🅑', '🆀', '🠖', '🄰', '🡆', '🦐', '🖘', '🤛', '🢧', '🠊', '🤝', '🠦', '🠢', '🠂', '🤌', '🤜', '🄼', '🡂', '🠪', '🡒', '🢂', '🢒', '🠲', '🥔', '🢣', '🡪', '🡲', '🥉', '🅙', '🡺', '🠮', '🠾', '🧃', '🄵', '🗫', '🄹', '🢖', '🥞', '🈈', '🢩', '🠆', '🄺', '🗭', '🈃', '🠞', '🅥', '🗲', '🖗', '🠚', '🢥', '🠶', '🡢', '🢚', '🥥', '🝌', '🅟']
default_probs = [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0.012804271, 1, 1, 1, 1, 1, 0.010434004, 1, 0.0036065835, 0.0012086612, 0.012079476, 0.0078257956, 0.0025536809, 1, 0.0048261913, 1, 0.0016998997, 1, 0.0021656705, 0.010512861, 0.00049156992, 0.0011123506, 1, 1, 0.004199388, 0.0091370698, 2.0104701e-06, 1, 0.00062635692, 0.0015871037, 1, 0.0017148766, 0.00011963949, 0.00024274513, 0.0019275718, 1.0336684e-06, 0.0027228564, 0.002727269, 2.2318018e-06, 0.0011078481, 0.00010681443, 0.00088135316, 0.00023847389, 0.00055947865, 1, 0.0011865876, 8.6053682e-05, 0.0072322679, 0.00011635887, 0.00050962734, 0.00099435786, 0.0016047901, 0.00028926731, 1, 1, 0.00065233046, 5.4051859e-05, 0.00061061542, 1, 0.0013294665, 0.0035455965, 1, 1, 0.00095985906, 0.00053147681, 0.0016662838, 0.00053073023, 0.00083760166, 1, 0.001048861, 0.00024140878, 0.00076506718, 0.0003754638, 0.0024275624, 0.002488733, 0.0010222744, 1.982806e-07, 1, 0.00014175242, 0.00059018971, 0.0017630972, 0.00020872722, 0.0013329769, 0.00019048394, 1, 0.0001448329, 1.5653942e-06, 0.0002636938, 0.00030531659, 0.00053560536, 0.00057157344, 1, 0.00059137173, 9.2421404e-05, 0.00070063374, 1, 0.00022375786, 4.1995947e-05, 4.7336457e-06, 0.00022394785, 9.5996977e-05, 0.0011016988, 0.00039346411, 0.00048331832, 0.0003897073, 8.174705e-05, 0.0010838958, 0.00013157044, 3.7834634e-05, 1.0634808e-05, 0.00013085661, 0.00084740919, 4.9897039e-06, 9.7770411e-05, 2.7438859e-06, 0.00091777241, 1.5409378e-05, 0.00026037995, 0.00030705149, 5.0117011e-05, 0.00010719179, 0.00034188488, 0.00014745705, 7.257879e-05, 0.00032428117, 0.00022974791, 0.00068987702, 0.00072516315, 0.0001295939, 0.00036936262, 4.9783368e-05, 0.00012427388, 0.00066980277, 0.00040763011, 0.0002413289, 1.6141052e-05, 8.3767714e-05, 0.0010213595, 6.6095777e-06, 6.9832902e-05, 9.3492876e-05, 1.8272269e-05, 0.0003495893, 0.0001829587, 0.00035941633, 0.0001678199, 0.00030892866, 0.00042839459, 0.0002421606, 0.00016186212, 0.00024436568, 7.4343647e-05, 0.00024033638, 1, 0.00081355975, 7.1822069e-05, 6.6820703e-06, 0.00054686971, 1.0063439e-05, 3.0343921e-05, 4.1265877e-05, 0.00020481904, 0.00013105836, 0.00013272079, 0.00010581831, 0.00010221433, 2.2487367e-05, 6.0867209e-05, 1.0646072e-05, 6.1245395e-05, 0.00012056483, 7.6584893e-06, 2.045839e-05, 3.0118696e-05, 5.9409889e-05, 0.00040933525, 0.00016084398, 0.00013365224, 0.00026694263, 0.00014992936, 0.0010292537, 6.2899853e-05, 0.00018006937, 8.6517539e-05, 8.9140252e-05, 2.1251864e-05, 8.1263926e-05, 2.0068352e-05, 3.35891e-07, 0.0013147242, 0.0005048454, 9.4805859e-05, 0.00030021355, 1.5183011e-05, 3.9164279e-05, 3.7734462e-05, 2.705445e-06, 3.9461815e-05, 0.0003232109, 0.00011336684, 6.9367772e-05, 4.2055988e-05, 2.1222579e-05, 0.00011476166, 0.00011648193, 0.00014437354, 0.00037019452, 0.00012910036, 2.4001867e-05, 0.00015288405, 0.00014106694, 3.4921843e-05, 0.00015755768, 7.2341623e-05, 1.6934289e-05, 0.0007693001, 1.1781452e-05, 0.00027481219, 0.0003796106, 6.996865e-05, 5.9583344e-05, 0.00015662986, 0.00012801861, 5.1037197e-05, 1.7819839e-05, 8.7210328e-06, 0.00081221008, 9.4566742e-05, 0.00063644582, 3.9337818e-05, 2.3138395e-05, 8.8330271e-06, 2.0279018e-05, 1.3349746e-06, 9.8986748e-05, 6.2454841e-05, 7.6127308e-06, 7.5559983e-05, 0.00011915368, 0.00015065943, 3.3306642e-05, 8.5459076e-05, 0.00022878039, 4.6420111e-05, 2.5244051e-05, 1.8334427e-05, 0.00011305008, 0.00010232869, 2.2771934e-05, 1.8084242e-05, 5.5616387e-05, 3.3229291e-05, 5.3403314e-06, 2.9773086e-05, 9.2899121e-05, 3.9623897e-05, 0.00017022291, 0.00036916492, 0.00013826109, 1.6369349e-05, 5.0956805e-05, 6.1402774e-05, 2.6943953e-05, 3.5019293e-05, 3.2622025e-05, 0.00016388898, 1.3376542e-05, 1.9500729e-05, 8.4083062e-05, 9.762554e-05, 7.1128001e-05, 3.314087e-05, 0.00015721237, 3.3862423e-05, 5.8942554e-05, 4.4828907e-05, 6.5447901e-05, 3.5559573e-05, 1.8495795e-06, 8.4154213e-05, 4.1544183e-05, 1.052967e-05, 8.4085499e-08, 1.9437044e-05, 8.7217149e-06, 7.5753203e-05, 5.2359514e-06, 4.8784867e-05, 5.0756205e-07, 2.7451382e-05, 4.1680934e-05, 2.4565197e-05, 9.5852905e-05, 0.00033726773, 1.0874055e-05, 1.0937039e-05, 5.2844712e-06, 1.2922647e-05, 1.6125834e-05, 0.00013779603, 4.6093119e-06, 1.0165937e-05, 5.2795669e-05, 1.593152e-05, 0.0001591613, 4.919948e-07, 1.7007345e-05, 0.00011714857, 1.51694e-06, 2.4246885e-05, 8.7667126e-05, 1.2903159e-06, 1.6079121e-05, 0.0001274151, 0.00042955586, 2.6868513e-05, 0.00020612645, 5.7438068e-05, 1.7747117e-05, 4.0976076e-05, 3.2088225e-05, 1.4285704e-05, 8.5051448e-05, 7.8461035e-06, 1.6044037e-06, 3.8078648e-05, 6.4408094e-05, 1.1749788e-05, 2.8696447e-06, 6.4657838e-06, 0.00011008008, 7.621244e-05, 3.1495987e-05, 7.8224948e-06, 7.5746379e-06, 1.0116285e-05, 7.6286606e-06, 4.0104393e-07, 4.8492635e-05, 4.0978812e-05, 4.9915195e-07, 9.2179944e-06, 2.285874e-06, 1.0578648e-05, 2.2647295e-05, 4.2723856e-05, 6.776012e-05, 4.6427435e-06, 7.4204661e-07, 1.1697307e-05, 9.2207469e-05, 2.1503431e-06, 3.696699e-06, 5.7436759e-05, 1.0275574e-05, 0.00010873148, 2.7570995e-05, 1.1359302e-05, 2.0632133e-06, 4.1152616e-05, 2.1511441e-05, 5.3503922e-05, 0.00014944834, 1.8831377e-05, 3.2325035e-05, 2.0270047e-05, 7.3267976e-05, 1.4529101e-05, 2.3190485e-05, 2.1682721e-05, 5.2394057e-07, 1.6918502e-05, 1.2358943e-05, 1.4661067e-05, 6.0769187e-05, 1.9459476e-06, 2.8514121e-05, 1.0532337e-06, 1.3925296e-06, 2.5461156e-06, 1.4325856e-05, 0.00010624818, 9.1687916e-06, 1.1397798e-06, 7.1284761e-05, 2.5966861e-05, 1.2121403e-05, 1.0562089e-06, 2.8486398e-05, 9.426969e-06, 2.252394e-05, 1.6720588e-06, 1.5885475e-05, 6.0094521e-06, 4.7130593e-06, 1.6548158e-05, 1.4298256e-05, 4.9149326e-06, 2.3743941e-07, 1.2019231e-05, 8.8544493e-06, 4.6565008e-05, 2.4243452e-06, 1.3059497e-05, 1.0765484e-05, 4.6449668e-06, 1.8021608e-05, 8.6292175e-06, 1.8298111e-05, 1.8095248e-05, 4.1759536e-06, 9.8491628e-06, 2.1364158e-05, 1.0897081e-05, 1.4794484e-05, 2.6085701e-05, 8.7147137e-06, 2.8097106e-06, 6.7503224e-06, 3.700595e-05, 2.441146e-05, 9.062486e-07, 4.1743688e-06, 2.9365998e-05, 1.7833236e-05, 6.0060975e-05, 1.0186628e-05, 1.7307906e-05, 1.2247075e-06, 5.8780188e-06, 1.1203668e-05, 3.4232871e-05, 1.4712673e-06, 1.8243991e-05, 7.8204066e-06, 2.5320564e-06, 1.6999918e-05, 2.5212026e-07, 3.5120813e-06, 7.7151562e-06, 6.1911128e-06, 1.32236e-05, 1.4477732e-05, 7.5054311e-05, 1.4386891e-05, 5.3353251e-05, 1.986624e-05, 2.2079841e-05, 4.2137481e-07, 0.00011921927, 0.0001468683, 1.4597335e-05, 6.7101942e-06, 6.6745713e-05, 3.8359826e-06, 1.6731348e-05, 4.1180392e-06, 4.5300762e-06, 6.2806052e-05, 0.00015746994, 1.0445769e-06, 2.0952337e-05, 6.9382686e-06, 2.6447099e-06, 2.8194113e-06, 3.4786157e-05, 9.8161127e-07, 3.1681073e-05, 1.604982e-06, 6.3002757e-05, 9.063614e-06, 8.5992806e-06, 2.8220852e-06, 6.3106208e-06, 1.1523802e-05, 3.8937659e-07, 8.241288e-05, 4.1723711e-06, 1.4626167e-05, 2.5656578e-07, 4.586213e-06, 6.4097912e-06, 3.3712815e-05, 1.4118369e-05, 2.6370497e-05, 1.2477633e-05, 8.6669734e-06, 4.266878e-06, 4.5405523e-06, 2.8488396e-06, 4.350205e-06, 9.1363045e-06, 5.5951996e-06, 2.928886e-05, 2.5876927e-05, 7.1425391e-05, 1.6266082e-05, 9.277278e-06, 5.964941e-05, 9.8317219e-07, 2.5904567e-06, 2.0765217e-06, 1.6423005e-06, 5.9934922e-05, 3.1188283e-06, 5.5740666e-06, 1.1387345e-06, 9.4630705e-06, 1.132598e-06, 2.7206847e-06, 1.0373261e-06, 5.9134632e-06, 1.45329e-05, 1.0213549e-06, 0.00014343408, 3.500732e-06, 2.3507287e-06, 1.0330061e-06, 2.7293386e-06, 2.4949186e-05, 1.8151872e-05, 4.4889868e-05, 3.7124755e-07, 4.6329493e-05, 1.2427779e-05, 2.632999e-05, 9.4016505e-06, 5.0237577e-06, 1.3316077e-06, 7.0878641e-06, 4.0085292e-06, 4.6576711e-06, 1.1863453e-07, 2.181659e-05, 3.5793298e-06, 1.01466e-06, 1.1454948e-05, 2.512812e-06, 1.9770707e-06, 1.6107208e-05, 1.6835033e-05, 6.9694775e-06, 2.3190119e-06, 4.8473798e-06, 6.8651138e-07, 8.2664255e-06, 2.1371686e-06, 1.2645055e-05, 1.4351125e-05, 5.1157997e-07, 1.0717164e-07, 2.5263978e-06, 2.1053285e-05, 2.4486922e-06, 1.1734777e-06, 1.3742188e-05, 2.4445006e-05, 1.9742031e-06, 6.2243248e-06, 2.8047779e-07, 2.1509993e-06, 7.7952637e-07, 2.524417e-05, 9.2925919e-05, 1.3436523e-06, 3.0775579e-06, 4.2029383e-06, 1.0849583e-06, 5.9988242e-06, 1.172453e-06, 2.7451068e-05, 3.405351e-06, 9.3464914e-06, 7.2297655e-07, 3.3785458e-05, 6.1027831e-06, 6.2452962e-08, 1.3354629e-07, 3.4192983e-06, 2.4433351e-07, 3.1180459e-08, 6.9731834e-07, 5.8357665e-07, 1.7645478e-06, 3.960703e-06, 2.0720788e-06, 1.6469681e-06, 3.0282777e-07, 7.209444e-06, 6.407884e-06, 4.1504458e-07, 5.696269e-06, 9.8847261e-07, 3.6997744e-06, 2.0931475e-06, 5.4136594e-06, 8.9127502e-07, 8.7102552e-07, 2.656981e-06, 1.1198049e-05, 1.7745382e-06, 7.9128846e-08, 8.4262983e-06, 4.871441e-06, 9.985848e-06, 5.0549675e-06, 3.4317845e-06, 1.340537e-06, 7.3392209e-07, 5.547484e-07, 1.6965196e-05, 2.54529e-06, 2.1632819e-05, 9.1283264e-06, 3.2179639e-07, 7.4006778e-07, 1.3689911e-06, 1.5830917e-06, 1.9887952e-06, 2.9498676e-07, 6.8977954e-07, 4.4677877e-06, 7.7942076e-07, 4.1013977e-06, 2.8629095e-06, 4.2698416e-06, 2.2969398e-06, 7.5282023e-06, 1.2476407e-07, 4.7178511e-07, 2.2721595e-06, 7.5861608e-06, 1.2811375e-05, 1.8778094e-07, 5.3187983e-07, 2.9034711e-06, 3.6613467e-06, 3.3656772e-06, 4.9657757e-07, 8.117612e-07, 6.9718039e-06, 4.705335e-06, 6.6696048e-06, 4.6896912e-06, 2.1953745e-06, 1.3231515e-06, 2.830943e-06, 1.160158e-06, 1.7040749e-06, 6.5074005e-07, 3.4216178e-08, 1.0725621e-05, 1.7283477e-05, 1.7083804e-06, 3.5272432e-08, 1.988694e-05, 1.4215928e-07, 3.3216651e-07, 3.3902379e-06, 1.783975e-07, 3.9177914e-07, 2.7660183e-06, 7.1158729e-07, 2.130298e-05, 2.7488832e-06, 1.0944385e-05, 6.4749161e-06, 4.7501854e-07, 3.2108721e-06, 1.1465198e-05, 4.4373928e-06, 5.1850975e-06, 6.2993223e-08, 7.1175424e-07, 6.3961375e-06, 2.4911975e-07, 3.1988543e-06, 6.316892e-07, 1.7302137e-06, 3.029173e-07, 4.5243255e-06, 1.9932536e-06, 3.4462661e-05, 7.399168e-07, 4.5901511e-06, 1.7572429e-06, 3.6655745e-06, 1.0163824e-05, 1.6539e-06, 8.4240337e-06, 5.7595139e-06, 1.0952712e-06, 2.5324478e-06, 1.1649749e-05, 6.6077878e-06, 2.6291384e-06, 2.4745152e-06, 2.0889277e-06, 4.3063741e-07, 9.9501574e-07, 1.4480513e-06, 2.0549267e-06, 6.8917598e-07, 3.9023311e-07, 2.3261575e-06, 2.434326e-06, 3.239858e-07, 3.1886429e-07, 1.0819206e-06, 2.1760143e-06, 1.2936772e-06, 2.6831217e-06, 7.1982976e-07, 9.6590998e-07, 1.7275172e-05, 1.1413025e-06, 1.8767112e-06, 1.2811394e-06, 4.8677606e-07, 5.8749811e-06, 9.2176208e-07, 1.6256343e-05, 2.9742745e-07, 3.03354e-06, 4.6431687e-06, 1.1934496e-06, 5.3633446e-08, 1.2023311e-05, 1.2341183e-05, 5.9661522e-07, 1.7148567e-07, 6.2100239e-06, 6.1000566e-07, 4.0305807e-05, 4.551614e-07, 1.3857519e-06, 4.3089813e-06, 6.8738791e-07, 9.1076618e-07, 7.1885421e-07, 3.7154365e-07, 6.9209935e-05, 1.0473061e-06, 5.3370087e-07, 5.0556298e-07, 1.2915034e-05, 2.8405434e-06, 7.241003e-06, 2.6735636e-06, 1.393682e-07, 7.2348968e-07, 1.6941863e-07, 4.8780372e-08, 1.872878e-06, 3.3230799e-06, 8.9801993e-08, 2.522535e-07, 1.3305801e-05, 1.7060498e-05, 2.4618129e-07, 7.644548e-07, 2.7160804e-06, 4.2440456e-06, 2.1648523e-07, 1.9486479e-06, 1.0598778e-06, 2.5586061e-07, 4.5805544e-07, 4.1690279e-07, 1.3759701e-06, 1.0026925e-08, 5.6634195e-07, 3.6637778e-06, 4.9948147e-07, 2.2783522e-06, 1.0150195e-07, 1.0412237e-05, 7.3934683e-07, 5.2292614e-07, 1.7079235e-07, 1.8053079e-06, 1.8457488e-06, 1.136135e-07, 1.906127e-06, 1.2058622e-07, 5.3432632e-07, 2.9097718e-08, 5.7939536e-07, 9.8327712e-07, 8.0725579e-07, 7.8525263e-06, 5.0151482e-07, 5.918801e-06, 1.1979594e-08, 4.6839968e-06, 4.6127152e-06, 1.1859115e-06, 7.0103938e-06, 7.7373116e-08, 4.1858641e-07, 3.6335175e-07, 2.2539227e-06, 1.0851844e-05, 5.4998982e-06, 4.8379007e-07, 5.5451784e-07, 2.7772414e-06, 2.2469135e-06, 6.6974712e-06, 1.261561e-06, 1.0860659e-06, 3.9202655e-07, 1.0618527e-06, 8.4203548e-06, 4.0655061e-07, 3.1029322e-06, 1.7445467e-05, 8.4754896e-07, 1.5616041e-06, 6.3854231e-06, 6.5336708e-06, 1.5088277e-07, 4.4566789e-07, 1.2925698e-06, 1.1439433e-07, 4.4145995e-06, 2.0021268e-07, 8.1643816e-07, 2.7525229e-07, 9.7143008e-08, 8.2632056e-07, 3.4219604e-06, 7.4560944e-06, 5.4250893e-07, 5.3763654e-07, 5.3595868e-06, 2.458855e-08, 2.2740064e-06, 7.3091961e-08, 2.1119506e-07, 2.0999034e-08, 4.359855e-07, 5.6337882e-08, 9.3968413e-07, 9.3225225e-07, 8.8293045e-06, 5.742487e-07, 8.0437087e-07, 2.4890685e-08, 3.6013908e-08, 1.5135029e-07, 5.8018195e-06, 4.9343896e-08, 2.1684655e-06, 1.3943254e-07, 1.0569108e-05, 4.665057e-07, 4.2871153e-07, 8.9144322e-07, 1.000507e-08, 3.8456087e-06, 1.1329215e-07, 5.2958399e-07, 1.6192239e-07, 1.5163982e-07, 1.594507e-06, 7.6050344e-07, 3.1728437e-08, 2.8647651e-07, 2.8432413e-07, 7.1346273e-07, 4.6415174e-08, 2.4503868e-07, 3.8679718e-06, 3.1350505e-06, 9.9360852e-07, 5.1532294e-07, 5.4469218e-08, 1.2170718e-06, 4.3373194e-07, 2.9674191e-10, 1.7046787e-07, 7.6532137e-07, 4.2348374e-09, 6.6746825e-06, 4.0194695e-06, 2.1144364e-08, 1.5208393e-06, 7.00459e-07, 1.3703626e-06, 1.5495609e-06, 2.2425804e-06, 2.7642697e-08, 6.1823187e-07, 2.6580808e-06, 3.484237e-07, 9.2493083e-06, 1.1773315e-06, 1.5120516e-07, 1.3371655e-07, 1.8834887e-06, 1.2415902e-06, 4.0383078e-08, 2.3575704e-07, 2.1010474e-06, 1.9266158e-08, 2.7161619e-07, 4.1287826e-06, 8.2508623e-06, 1.6853497e-06, 5.8867865e-08, 3.1601681e-07, 1.8792464e-07, 2.4616133e-05, 1.4406008e-08, 1.8304701e-06, 1.6868989e-07, 1.1939322e-06, 1.1806867e-06, 4.8251344e-08, 2.4219696e-06, 4.9934522e-07, 1.049678e-06, 8.2462799e-07, 3.5072751e-06, 2.9254943e-07, 4.0939398e-07, 1.2022984e-06, 6.2446948e-06, 8.4421522e-08, 8.6669814e-08, 8.5101874e-07, 2.8707439e-07, 8.2540851e-07, 1.9045271e-07, 1.1373388e-06, 3.0494236e-06, 2.9731329e-08, 1.5695898e-05, 7.3182395e-07, 1.2824749e-05, 5.8250939e-06, 4.596439e-07, 3.3104129e-07, 2.1833957e-08, 7.3811253e-07, 1.1192571e-07, 9.5774312e-06, 1.8093367e-07, 6.025839e-07, 2.1953367e-06, 3.4836368e-08, 1.0755929e-07, 1.3737956e-07, 1.2984019e-05, 2.9321922e-07, 1.0012921e-07, 7.2132266e-06, 7.6835931e-07, 1.3063502e-06, 4.527509e-07, 9.8581972e-07, 4.3552507e-07, 5.7431575e-06, 1.0559269e-06, 2.6584294e-07, 1.1414164e-05, 9.6673932e-07, 3.1098659e-09, 2.2500343e-07, 2.8689044e-07, 2.1023261e-06, 4.2879144e-08, 9.4279123e-08, 1.2813965e-05, 2.3857794e-07, 1.7165321e-07, 1.4315796e-06, 1.852584e-06, 2.0001448e-08, 9.1991268e-07, 2.9391688e-07, 7.7974346e-07, 2.5999926e-08, 1.5453431e-06, 1.2976238e-06, 4.1073847e-07, 1.5525087e-08, 2.0797404e-06, 5.5247187e-07, 1.1387519e-06, 2.4038688e-06, 1.1871936e-08, 6.296263e-07, 3.8690564e-06, 1.236752e-06, 5.5239599e-07, 2.163808e-07, 8.1563151e-08, 3.5271526e-06, 3.6210227e-07, 6.8392723e-08, 1.3206471e-07, 8.0591548e-08, 3.1038201e-06, 1.9896139e-07, 3.0855031e-07, 1.4576496e-07, 6.9846813e-08, 6.7362059e-08, 9.4074221e-07, 2.6597293e-06, 2.0549815e-06, 2.4670632e-07, 2.1274229e-07, 5.7083497e-07, 2.198168e-07, 1.5345268e-08, 6.3496043e-07, 4.3348155e-06, 8.2307236e-07, 9.5821262e-10, 1.712055e-08, 1.9966708e-06, 1.4143967e-06, 3.1702518e-06, 3.6585268e-06, 3.429481e-06, 3.1635977e-08, 1.9203175e-07, 1.4856452e-07, 3.3673578e-07, 5.3063252e-07, 4.7529702e-06, 2.6381775e-08, 6.5237543e-07, 1.0871271e-06, 2.6616295e-08, 5.4184011e-06, 6.3768113e-08, 2.8876618e-08, 3.4346181e-07, 2.0458147e-06, 1.6621983e-06, 2.407557e-07, 3.3340722e-08, 1.6117741e-06, 1.4661492e-06, 1.7564888e-06, 5.4620148e-09, 3.3607125e-06, 8.2018055e-08, 1.1320278e-06, 1.5500449e-07, 4.610479e-07, 8.7165881e-07, 4.0974337e-06, 1.2040081e-06, 6.3926308e-08, 8.5293783e-07, 1.1621684e-07, 2.5202567e-06, 1.3540958e-05, 1.5081422e-08, 1.9471022e-06, 8.2777092e-09, 2.2088435e-07, 1.6144476e-10, 1.3936508e-06, 3.5779217e-07, 4.0100809e-10, 2.0177094e-08, 1.1673072e-10, 3.0060932e-07, 6.9617283e-07, 2.9372524e-07, 5.5990026e-09, 7.8362508e-09, 1.848242e-07, 3.3682153e-09, 2.7612532e-06, 5.7889658e-09, 2.3667233e-09, 1.3747031e-06, 3.3066601e-06, 7.8672292e-07, 7.2204387e-10, 3.1579156e-10, 1.7248238e-09, 4.050813e-08, 6.3742116e-11, 3.4401284e-09, 3.8809058e-09, 1.9512306e-08, 6.9611173e-07, 3.1434166e-09, 1.0960218e-09, 8.9360483e-08, 1.7203956e-08, 1.5640475e-07, 3.2470555e-09, 1.3785168e-08, 1.0007899e-07, 5.0648669e-07, 3.109175e-07, 1.6135334e-06, 1.7731206e-06, 4.0882546e-09, 3.8802761e-09, 1.3807075e-06, 9.32962e-07, 3.764991e-09, 2.3832462e-07, 5.2442942e-07, 1.4886207e-07, 2.3436194e-06, 3.8584627e-08, 2.4465061e-07, 2.201886e-07, 1.6984603e-07, 1.5194765e-06, 2.8792599e-07, 6.1623052e-07, 7.2060238e-09, 1.1091779e-06, 4.1899114e-08, 1.105156e-08, 7.930759e-08, 4.0310763e-07, 6.9235706e-09, 2.6238672e-07, 4.2390418e-08, 2.1983692e-07, 5.9923605e-07, 9.1072224e-08, 1.1937176e-07, 1.6926005e-07, 1.7112454e-08, 6.1235546e-08, 7.8962096e-08, 2.5652342e-09, 9.4090851e-08, 5.2504767e-08, 4.0016651e-08, 5.8298895e-08, 9.9243749e-08, 1.1161404e-07, 1.3775134e-07, 3.6775614e-07, 1.4356777e-07, 8.0240142e-08, 4.6523482e-08, 2.8806589e-08, 1.2194529e-07, 2.062507e-08, 3.2282536e-08, 3.3056176e-07, 1.1376203e-07, 4.6495007e-08, 3.5021309e-08, 2.6115347e-07, 2.8822449e-06, 2.4478538e-08, 4.2643432e-08, 3.071802e-08, 4.7358082e-08, 5.5191998e-07, 6.9478131e-07, 6.0421587e-07, 3.4387526e-08, 1.2686763e-07, 4.1531521e-08, 7.5338257e-08, 2.756977e-08, 7.1620015e-08, 5.2768613e-08, 1.7125001e-07, 5.5318118e-08, 2.6243524e-07, 1.2080746e-07, 1.2734506e-06, 7.4674013e-08, 7.8824108e-08, 2.7486026e-08, 1.1127032e-07, 3.2751529e-08, 1.8521743e-06, 1.5738631e-07, 2.3427958e-07]

def sample(prime, chars, sess, vocab, model):

    chars_list, probs = model.rawsample(sess, chars, vocab, prime)

    #### SOME TESTING CODE ####

    # probs_file = open("probs.txt", "w")
    # emojis_file = open("emojis.txt", "w")
    # others_file = open("others.txt", "w")
    #
    # for i in range (0, len(chars_list)):
    #     if chars_list[i] in emojis:
    #         probs_file.write(repr(probs[i]))
    #         probs_file.write(", ")
    #         emojis_file.write(chars_list[i] + ", ")
    #
    #     else:
    #         probs_file.write("1, ")
    #         others_file.write(chars_list[i] + ", ")
    #
    # probs_file.close()
    # emojis_file.close()
    # others_file.close()

    #### ACTUAL CODE ####

    best_char1 = ' '
    best_prob1 = 0

    best_char2 = ' '
    best_prob2 = 0

    best_char3 = ' '
    best_prob3 = 0

    best_char4 = ' '
    best_prob4 = 0

    best_char5 = ' '
    best_prob5 = 0

    for i in range (0, len(chars_list)):
        if chars_list[i] in emojis:
            prob = probs[i] - default_probs[i]
            if prob > best_prob1:
                best_char5 = best_char4
                best_prob5 = best_prob4
                best_char4 = best_char3
                best_prob4 = best_prob3
                best_char3 = best_char2
                best_prob3 = best_prob2
                best_char2 = best_char1
                best_prob2 = best_prob1
                best_char1 = chars_list[i]
                best_prob1 = prob
            elif prob > best_prob2:
                best_char5 = best_char4
                best_prob5 = best_prob4
                best_char4 = best_char3
                best_prob4 = best_prob3
                best_char3 = best_char2
                best_prob3 = best_prob2
                best_char2 = chars_list[i]
                best_prob2 = prob
            elif prob > best_prob3:
                best_char5 = best_char4
                best_prob5 = best_prob4
                best_char4 = best_char3
                best_prob4 = best_prob3
                best_char3 = chars_list[i]
                best_prob3 = prob
            elif prob > best_prob4:
                best_char5 = best_char4
                best_prob5 = best_prob4
                best_char4 = chars_list[i]
                best_prob4 = prob
            elif prob > best_prob5:
                best_char5 = chars_list[i]
                best_prob5 = prob

    print("\nPreferred Option 1: " + best_char1)
    print(best_prob1)
    print("\nPreferred Option 2: " + best_char2)
    print(best_prob2)
    print("\nPreferred Option 3: " + best_char3)
    print(best_prob3)
    print("\nPreferred Option 4: " + best_char4)
    print(best_prob4)
    print("\nPreferred Option 5: " + best_char5)
    print(best_prob5)
    print("\n")

if __name__ == '__main__':
    main()
