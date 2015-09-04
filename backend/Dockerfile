FROM gliderlabs/python-runtime:3.4

MAINTAINER dev@sounds.so

EXPOSE 8080

CMD ["/env/bin/python", "-m", "bottle", "-s", "cherrypy", "-b", "0.0.0.0:8080", "main"]
