import time

from compose.cli import command

class Monitor(object):
    def __init__(self, path, options):
        self.path = path
        self.options = options
        self.project = command.project_from_options(self.path, self.options)

    def run(timeout):
    	while True:
    		for service in self.project.services:
    			service.pull()
    		self.project.up()
    		time.sleep(timeout)
