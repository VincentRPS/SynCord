import time

import gevent

from syncord.api.client import APIClient
from syncord.gateway.client import GatewayClient
from syncord.gateway.packets import OPCode
from syncord.state import State, StateConfig
from syncord.types.user import Game, Status
from syncord.util.backdoor import DiscoBackdoorServer
from syncord.util.config import Config
from syncord.util.emitter import Emitter
from syncord.util.logging import LoggingClass


class ClientConfig(Config):
    """
    Configuration for the `Client`.

    Attributes
    ----------
    token : str
        Discord authentication token, can be validated using the
        `syncord.util.token.is_valid_token` function.
    shard_id : int
        The shard ID for the current client instance.
    shard_count : int
        The total count of shards running.
    guild_subscriptions : bool
        Whether to enable subscription events (e.g. presence and typing).
    max_reconnects : int
        The maximum number of connection retries to make before giving up (0 = never give up).
    log_level : str
        The logging level to use.
    manhole_enable : bool
        Whether to enable the manhole (e.g. console backdoor server) utility.
    manhole_bind : tuple(str, int)
        A (host, port) combination which the manhole server will bind to (if it's
        enabled using :attr:`manhole_enable`).
    encoder : str
        The type of encoding to use for encoding/decoding data from websockets,
        should be either 'json' or 'etf'.
    """

    token = ""
    shard_id = 0
    shard_count = 1
    guild_subscriptions = True
    max_reconnects = 5
    log_level = "info"

    manhole_enable = False
    manhole_bind = ("127.0.0.1", 8484)

    encoder = "json"


class Client(LoggingClass):
    """
    Class representing the base entry point that should be used in almost all
    implementation cases. This class wraps the functionality of both the REST API
    (`syncord.api.client.APIClient`) and the realtime gateway API
    (`syncord.gateway.client.GatewayClient`).

    Parameters
    ----------
    config : `ClientConfig`
        Configuration for this client instance.

    Attributes
    ----------
    config : `ClientConfig`
        The runtime configuration for this client.
    events : `Emitter`
        An emitter which emits Gateway events.
    packets : `Emitter`
        An emitter which emits Gateway packets.
    state : `State`
        The state tracking object.
    api : `APIClient`
        The API client.
    gw : `GatewayClient`
        The gateway client.
    manhole_locals : dict
        Dictionary of local variables for each manhole connection. This can be
        modified to add/modify local variables.
    manhole : Optional[`BackdoorServer`]
        Gevent backdoor server (if the manhole is enabled).
    """

    def __init__(self, config):
        super(Client, self).__init__()
        self.config = config

        self.events = Emitter()
        self.packets = Emitter()

        self.api = APIClient(self.config.token, self)
        self.gw = GatewayClient(self, self.config.max_reconnects, self.config.encoder)
        self.state = State(self, StateConfig(self.config.get("state", {})))

        if self.config.manhole_enable:
            self.manhole_locals = {
                "client": self,
                "state": self.state,
                "api": self.api,
                "gw": self.gw,
            }

            self.manhole = DiscoBackdoorServer(
                self.config.manhole_bind,
                banner="Disco Manhole",
                localf=lambda: self.manhole_locals,
            )
            self.manhole.start()

    def update_presence(self, status, game=None, afk=False, since=0.0):
        """
        Updates the current clients presence.

        Parameters
        ----------
        status : `user.Status`
            The clients current status.
        game : `user.Game`
            If passed, the game object to set for the user's presence.
        afk : bool
            Whether the client is currently afk.
        since : float
            How long the client has been afk for (in seconds).
        """
        if game and not isinstance(game, Game):
            raise TypeError("Game must be a Game model")

        if status is Status.IDLE and not since:
            since = int(time.time() * 1000)

        payload = {
            "afk": afk,
            "since": since,
            "status": status.lower(),
            "game": None,
        }

        if game:
            payload["game"] = game.to_dict()

        self.gw.send(OPCode.STATUS_UPDATE, payload)

    def run(self):
        """
        Run the client (e.g. the `GatewayClient`) in a new greenlet.
        """
        return gevent.spawn(self.gw.run)

    def run_forever(self):
        """
        Run the client (e.g. the `GatewayClient`) in the current greenlet.
        """
        return self.gw.run()
