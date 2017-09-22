package.path = "/repo/cadet/?.lua;" .. package.path
local httpd = require 'httpd'
local Cadet = require("cadet")

App = {}

function App.secret(env, headers, query)
  local res = Cadet.response
  local write = Cadet.write

  res.headers["Content-Type"] = "text/html"
  res.status = 200

  write("<h1>ze secret!: </h1>")

  if query["user"] == "john" and query["pass"] == "n00b" then
     write("this is the secret I've been looking for")
  else
     write("wrong login or pass")
  end

  return Cadet.finish()
end

function App.index(env, headers, query)
  local res = Cadet.response
  local write = Cadet.write

  res.headers["Content-Type"] = "text/html"
  res.status = 200

  write("<h1>hello lua world</h1>")

  return Cadet.finish()
end

httpd.register_handler("index", App.index)
httpd.register_handler("secret", App.secret)

