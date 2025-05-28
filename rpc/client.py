"""
RPC Client implementation
"""

import socket
import msgpack
from typing import Any, Union


class RPCResult:
    """
    Wrapper for RPC call results, similar to the C++ version's result handling.
    Provides type conversion methods like .as<int>() in C++.
    """
    
    def __init__(self, value: Any):
        self.value = value
    
    def as_int(self) -> int:
        """Convert result to int (similar to .as<int>() in C++)"""
        return int(self.value)
    
    def as_float(self) -> float:
        """Convert result to float"""
        return float(self.value)
    
    def as_str(self) -> str:
        """Convert result to string"""
        return str(self.value)
    
    def as_bool(self) -> bool:
        """Convert result to boolean"""
        return bool(self.value)
    
    def as_list(self) -> list:
        """Convert result to list"""
        return list(self.value)
    
    def as_dict(self) -> dict:
        """Convert result to dictionary"""
        return dict(self.value)
    
    def get(self) -> Any:
        """Get the raw result value"""
        return self.value
    
    def __str__(self) -> str:
        return str(self.value)
    
    def __repr__(self) -> str:
        return f"RPCResult({self.value!r})"


class Client:
    """
    RPC Client for making remote procedure calls.
    
    Similar to the C++ rpclib client, this allows you to:
    - Connect to an RPC server
    - Call remote functions with parameters
    - Get typed results
    """
    
    def __init__(self, host: str, port: int):
        """
        Initialize the RPC client.
        
        Args:
            host: Server hostname or IP address
            port: Server port number
        """
        self.host = host
        self.port = port
        self.socket: socket.socket = None
        self._connect()
    
    def _connect(self) -> None:
        """
        Establish connection to the RPC server.
        """
        try:
            self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.socket.connect((self.host, self.port))
            print(f"Connected to RPC server at {self.host}:{self.port}")
        except Exception as e:
            raise ConnectionError(f"Failed to connect to {self.host}:{self.port}: {e}")
    
    def call(self, method_name: str, *args, **kwargs) -> RPCResult:
        """
        Call a remote function.
        
        Args:
            method_name: Name of the remote function to call
            *args: Positional arguments to pass to the function
            **kwargs: Keyword arguments to pass to the function
            
        Returns:
            RPCResult object containing the result
            
        Raises:
            RuntimeError: If the remote call fails
            ConnectionError: If there's a connection issue
        """
        if not self.socket:
            raise ConnectionError("Not connected to server")
        
        # Prepare the request
        if args and kwargs:
            # If both args and kwargs are provided, combine them
            params = list(args) + [kwargs]
        elif kwargs:
            params = kwargs
        else:
            params = list(args)
        
        request = {
            "method": method_name,
            "params": params
        }
        
        try:
            # Send the request
            request_data = msgpack.packb(request)
            self.socket.send(request_data)
            
            # Receive the response
            response_data = self.socket.recv(4096)
            response = msgpack.unpackb(response_data, raw=False)
            
            # Check for errors
            if "error" in response:
                error_msg = response["error"]
                if "traceback" in response:
                    error_msg += f"\nServer traceback:\n{response['traceback']}"
                raise RuntimeError(f"Remote call failed: {error_msg}")
            
            # Return the result wrapped in RPCResult
            return RPCResult(response.get("result"))
            
        except socket.error as e:
            raise ConnectionError(f"Communication error: {e}")
        except Exception as e:
            raise RuntimeError(f"Call failed: {e}")
    
    def close(self) -> None:
        """
        Close the connection to the server.
        """
        if self.socket:
            self.socket.close()
            self.socket = None
            print("Disconnected from RPC server")
    
    def __enter__(self):
        """Context manager entry"""
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        """Context manager exit"""
        self.close()
    
    def __del__(self):
        """Destructor to ensure socket is closed"""
        self.close() 