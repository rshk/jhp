import os

from werkzeug.wrappers import Request, Response
from jinja2 import Environment, FileSystemLoader, TemplateNotFound, Template


@Request.application
def application(request):
    root_dir = os.getcwd()
    path = request.path  # todo: make sure path is sandboxed!
    if path in ('', '/'):
        path = '/index.html'
    # todo: if path is a directory, append index.html to template name
    env = Environment(loader=FileSystemLoader(root_dir))

    response = Response()
    response.status_code = 200
    response.content_type = 'text/html; charset=utf-8'

    ## Try to get the template
    try:
        template = env.get_template(path)
    except TemplateNotFound:
        response.status_code = 404
        try:
            template = env.get_template('404.html')
        except TemplateNotFound:
            response.content_type = 'text/plain'
            template = Template("PAGE NOT FOUND")

    ## Prepare and send the response
    rendered = template.render(request=request, response=response)
    response.set_data(rendered)
    return response


def main():
    from werkzeug.serving import run_simple
    ## todo: parse commandline options, etc.
    run_simple('localhost', 4000, application,
               use_debugger=True, use_reloader=True)


if __name__ == '__main__':
    main()
