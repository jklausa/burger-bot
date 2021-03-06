from burgerpy.common import Module, Config
import simplejson as json

import re
from random import randint

regex = re.compile('.*(:+)([-_]+)([Dd]+).*')
texts = ["EBIN", "5/5", "well memed", "EBIN 5/5", "BRETTY GOOD"]
p = 2


class EbinModule(Module):
    def modulate(self, string):
        r = randint(0, 3)
        letter = string[0]

        return string + letter * r

    def pick_text(self):
        r = randint(0, 10)

        if r <= p:
            return texts[randint(0, len(texts) - 1)]
        else:
            return ''

    def generate_msg(self, matches):
        colons = self.modulate(matches.group(1))
        dashes = self.modulate(matches.group(2))
        the_Ds = self.modulate(matches.group(3))
        text = self.pick_text()

        return colons + dashes + the_Ds + ' ' + text

    def on_msg(self, method, channel, props, body):
        body = json.loads(body)
        content = body["content"]
        origin = body["channel"]

        if body["from"] == self.app_config.irc_nick:
            return

        match = regex.match(content)
        if match:
            msg = self.generate_msg(match)
            msg = self.compose_msg(origin, msg)
            self.send_result(body["source"], msg)

if __name__ == "__main__":
    config = Config()
    em = EbinModule(config)
    em.listen("burger.privmsg", em.on_msg)
    em.run()
