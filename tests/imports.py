"""
This module tests that all of disco can be imported, mostly to help reduce issues
with untested code that will not even parse/run on Py2/3
"""
from syncord.api.client import *
from syncord.api.http import *
from syncord.api.ratelimit import *
from syncord.bot.bot import *
from syncord.bot.command import *
from syncord.bot.parser import *
from syncord.bot.plugin import *
from syncord.bot.storage import *
from syncord.gateway.client import *
from syncord.gateway.events import *
from syncord.gateway.ipc import *
from syncord.gateway.packets import *
# Not imported, GIPC is required but not provided by default
# from syncord.gateway.sharder import *
from syncord.types.base import *
from syncord.types.channel import *
from syncord.types.guild import *
from syncord.types.invite import *
from syncord.types.message import *
from syncord.types.permissions import *
from syncord.types.user import *
from syncord.types.voice import *
from syncord.types.webhook import *
from syncord.util.backdoor import *
from syncord.util.config import *
from syncord.util.functional import *
from syncord.util.hashmap import *
from syncord.util.limiter import *
from syncord.util.logging import *
from syncord.util.serializer import *
from syncord.util.snowflake import *
from syncord.util.websocket import *
