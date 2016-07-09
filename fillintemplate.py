import sys
from jinja2 import Environment, FileSystemLoader
env = Environment(loader=FileSystemLoader('config'))
template = env.get_template(sys.argv[1])
import json
with open("config.json") as fh:
	config=json.loads(fh.read())
output_from_parsed_template = template.render(config=config)
print output_from_parsed_template
