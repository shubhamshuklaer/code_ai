# code_platform_web
* Run the web2py web server
* Import this project into web2py.
* [spoj code platform](https://github.com/shubhamshuklaer/code_platform/) must
be setup. Follow the configuration steps from the link.
* Run the file server in `file_server/file_server.py`. No arguments needed, but
spoj code platform must be set up.
* Open http://[host]/[project_name]/default/code?prob_code=GSS1, where 8000 is
the port web2py is running on.
* If you do not want to load problem statement(Internet problems) use
http://[host]/[project_name]/default/code?prob_code=GSS1&no_load_prob.
* Here eg of [host] can be localhost:8000 and [project_name]  code_platform_web.
