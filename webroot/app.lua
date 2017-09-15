package.path = "/repo/cadet/?.lua;" .. package.path
local httpd = require 'httpd'
local Cadet = require("cadet")

App = {}

function App.index(env, headers, query)
  local res = Cadet.response
  local write = Cadet.write

  res.headers["Content-Type"] = "text/html"
  res.status = 200

  write("<h1>hello lua world</h1>")

  return Cadet.finish()
end

httpd.register_handler("index", App.index)

