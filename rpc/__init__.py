"""
Python RPC Library - A simple RPC implementation similar to C++ rpclib

This library provides both server and client implementations for RPC communication
using MessagePack for serialization and TCP sockets for transport.
"""

from .server import Server
from .client import Client

__version__ = "1.0.0"
__all__ = ["Server", "Client"] 