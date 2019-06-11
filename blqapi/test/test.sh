curl -i -X POST -H "Content-Type: application/json; indent=4" \
  -d '{
    "jsonrpc": "2.0",
    "method": "App.hello",
    "params": ["Flask"],
    "id": "1"
  }' http://localhost:5000/api

curl -i -X POST -H "Content-Type: application/json; indent=4" \
  -d '{
    "jsonrpc": "2.0",
    "method": "App.fails",
    "params": ["Flask"],
    "id": "1"
  }' http://localhost:5000/api

  curl -i -X POST -H "Content-Type: application/json; indent=4" \
  -d '{
    "jsonrpc": "2.0",
    "method": "App.sum",
    "params": {"a":1,"b": 2},
    "id": "1"
  }' http://localhost:5000/api