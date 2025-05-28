# Python RPC Library

A simple and elegant RPC (Remote Procedure Call) library for Python, inspired by the C++ rpclib. This library provides both client and server implementations with a clean, easy-to-use API.

## Features

- **Simple API**: No IDL (Interface Definition Language) to learn, no code generation
- **Automatic signature capture**: Function signatures are automatically detected
- **Type conversion**: Built-in result type conversion similar to C++ rpclib
- **Concurrent connections**: Server handles multiple clients simultaneously
- **Async support**: Non-blocking server operation
- **Error handling**: Comprehensive error reporting with tracebacks
- **MessagePack serialization**: Efficient binary serialization

## Installation

### Option 1: Using Virtual Environment (Recommended)

1. Create and activate a virtual environment:
```bash
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

2. Install the required dependencies:
```bash
pip install -r requirements.txt
```

### Option 2: System-wide Installation

```bash
pip install msgpack
```

### Option 3: Install as Package

```bash
pip install -e .
```

## Quick Demo

Run the demo to see the library in action:
```bash
python demo.py
```

## Quick Start

### Server Example

```python
from rpc import Server

def foo():
    print("foo was called!")
    return "foo executed successfully"

# Create a server that listens on port 8080
srv = Server(8080)

# Bind functions to names for RPC calls
srv.bind("foo", foo)
srv.bind("add", lambda a, b: a + b)

# Run the server (blocking)
srv.run()
```

### Client Example

```python
from rpc import Client

# Connect to the server
client = Client("127.0.0.1", 8080)

# Call remote functions
result = client.call("add", 2, 3).as_int()
print(f"The result is: {result}")

# Close the connection
client.close()
```

## API Reference

### Server Class

#### `Server(port, host="localhost")`
Create a new RPC server.

- `port`: Port number to listen on
- `host`: Host address to bind to (default: "localhost")

#### `bind(name, function)`
Bind a function to a name for RPC calls.

- `name`: The name to bind the function to
- `function`: The function to bind (can be a regular function, lambda, or method)

#### `run()`
Start the server and run the main loop (blocking). Similar to `srv.run()` in C++ rpclib.

#### `async_run()`
Start the server in a separate thread (non-blocking). Returns the thread object. Similar to `srv.async_run()` in C++ rpclib.

#### `stop()`
Stop the server.

### Client Class

#### `Client(host, port)`
Create a new RPC client and connect to the server.

- `host`: Server hostname or IP address
- `port`: Server port number

#### `call(method_name, *args, **kwargs)`
Call a remote function. Returns an `RPCResult` object.

- `method_name`: Name of the remote function to call
- `*args`: Positional arguments to pass to the function
- `**kwargs`: Keyword arguments to pass to the function

#### `close()`
Close the connection to the server.

### RPCResult Class

The `RPCResult` class provides type conversion methods similar to C++ rpclib:

- `as_int()`: Convert result to int (similar to `.as<int>()` in C++)
- `as_float()`: Convert result to float
- `as_str()`: Convert result to string
- `as_bool()`: Convert result to boolean
- `as_list()`: Convert result to list
- `as_dict()`: Convert result to dictionary
- `get()`: Get the raw result value

## Examples

### Basic Server and Client

**Server (`examples/server_example.py`):**
```python
from rpc import Server

def foo():
    print("foo was called!")
    return "foo executed successfully"

srv = Server(8080)
srv.bind("foo", foo)
srv.bind("add", lambda a, b: a + b)
srv.run()
```

**Client (`examples/client_example.py`):**
```python
from rpc import Client

client = Client("127.0.0.1", 8080)
result = client.call("add", 2, 3).as_int()
print(f"add(2, 3) = {result}")
client.close()
```

### Async Server

```python
from rpc import Server
import time

srv = Server(8080)
srv.bind("add", lambda a, b: a + b)

# Start server asynchronously
server_thread = srv.async_run()

# Main thread can do other work
for i in range(10):
    print(f"Main thread working... {i}")
    time.sleep(1)

# Server continues running in background
server_thread.join()
```

## Running the Examples

1. **Start the server:**
```bash
python examples/server_example.py
```

2. **In another terminal, run the client:**
```bash
python examples/client_example.py
```

3. **For async server example:**
```bash
python examples/async_server_example.py
```

## Error Handling

The library provides comprehensive error handling:

```python
try:
    result = client.call("nonexistent_method")
except RuntimeError as e:
    print(f"RPC call failed: {e}")
except ConnectionError as e:
    print(f"Connection failed: {e}")
```

## Comparison with C++ rpclib

| C++ rpclib | Python RPC Library |
|------------|-------------------|
| `rpc::server srv(8080)` | `srv = Server(8080)` |
| `srv.bind("add", &add)` | `srv.bind("add", add)` |
| `srv.run()` | `srv.run()` |
| `srv.async_run()` | `srv.async_run()` |
| `rpc::client client("127.0.0.1", 8080)` | `client = Client("127.0.0.1", 8080)` |
| `client.call("add", 2, 3).as<int>()` | `client.call("add", 2, 3).as_int()` |

## Requirements

- Python 3.6+
- msgpack

## License

This project is inspired by the C++ rpclib and follows similar design principles. Feel free to use and modify according to your needs.