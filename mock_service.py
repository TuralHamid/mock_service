from http.server import BaseHTTPRequestHandler, HTTPServer
from multiprocessing import Process
from glob import glob
import json
import os

PATH_RESPONSE_FOLDER = "response"
PATH_CONFIG_FILE = os.path.join("config", "config.json")
PATH_HTML_FILE = os.path.join("ui", "index.html")
PATH_CSS_FILE = os.path.join("ui", "css", "index.css")
PATH_JS_FILE = os.path.join("ui", "js", "request.js")
PATH_IMG_FILE = os.path.join("ui", "img", "copy-icon.png")
HEADER_CONTENT_TYPE = "Content-Type"
HEADER_CONTENT_LENGTH = "Content-Length"
CONTENT_TYPE_JSON = "application/json"
CONTENT_TYPE_TEXT = "text/html"
CONTENT_TYPE_JS = "application/javascript"
CONTENT_TYPE_CSS = "text/css"
CONTENT_TYPE_PNG = "image/png"
STATUS_OK = 200
STATUS_ERROR = 404
JSON_INDENT = 2
ENCODING_TYPE = "UTF-8"
config = {}


class BasicServer(BaseHTTPRequestHandler):
    def handle_http(self, status, content_type, response):
        self.send_response(status)
        self.send_header(HEADER_CONTENT_TYPE, content_type)
        self.end_headers()
        self.wfile.write(bytes(response, ENCODING_TYPE))

    def do_GET(self):
        if ".css" in self.get_path():
            self.handle_http(STATUS_OK, CONTENT_TYPE_CSS, read_file(PATH_CSS_FILE))
        elif ".js" in self.get_path():
            self.handle_http(STATUS_OK, CONTENT_TYPE_JS, read_file(PATH_JS_FILE))
        elif ".png" in self.get_path():
            self.send_response(STATUS_OK)
            self.send_header(HEADER_CONTENT_TYPE, CONTENT_TYPE_PNG)
            self.end_headers()
            self.wfile.write(read_image(PATH_IMG_FILE))
        else:
            self.handle_path_request()

    def do_POST(self):
        if self.headers.get_content_type() == CONTENT_TYPE_JSON:
            length = int(self.headers.get(HEADER_CONTENT_LENGTH))
            body = self.rfile.read(length)
            if self.path == "/serviceNames":
                self.handle_http(STATUS_OK, CONTENT_TYPE_JSON, self.create_json_from_string(get_routes_as_json()))
            elif self.path == "/OPR_UPDATE":
                if self.is_data_json(body.decode(ENCODING_TYPE)):
                    name = json.loads(body.decode(ENCODING_TYPE))["serviceNameSelect"]
                    data = json.loads(body.decode(ENCODING_TYPE))["jsonTextArea"]
                    if self.is_data_json(data):
                        is_updated = update_file(os.path.join(PATH_RESPONSE_FOLDER, "{}.json".format(name)), data)
                        if is_updated:
                            self.handle_http(STATUS_OK, CONTENT_TYPE_TEXT, "JSON updated")
                        else:
                            self.handle_http(STATUS_ERROR, CONTENT_TYPE_TEXT, "JSON is NOT updated")
                    else:
                        self.handle_http(STATUS_ERROR, CONTENT_TYPE_TEXT, "Malformed JSON text")
                else:
                    self.handle_http(STATUS_ERROR, CONTENT_TYPE_TEXT, "Malformed JSON")
            elif self.path == "/OPR_INSERT":
                if self.is_data_json(body.decode(ENCODING_TYPE)):
                    name = json.loads(body.decode(ENCODING_TYPE))["serviceNameInput"]
                    requested_route = self.get_route_name(name, get_route_list())
                    if requested_route:
                        self.handle_http(STATUS_ERROR, CONTENT_TYPE_TEXT, "\"{}\" service already exists".format(name))
                    else:
                        data = json.loads(body.decode(ENCODING_TYPE))["jsonTextArea"]
                        if self.is_data_json(data):
                            is_added = write_file(os.path.join(PATH_RESPONSE_FOLDER, "{}.json".format(name)), data)
                            if is_added:
                                self.handle_http(STATUS_OK, CONTENT_TYPE_TEXT, "JSON added")
                            else:
                                self.handle_http(STATUS_ERROR, CONTENT_TYPE_TEXT, "JSON is NOT added")
                        else:
                            self.handle_http(STATUS_ERROR, CONTENT_TYPE_TEXT, "Malformed JSON text")
                else:
                    self.handle_http(STATUS_ERROR, CONTENT_TYPE_TEXT, "Malformed JSON")
            elif self.path == "/OPR_SELECT":
                if self.is_data_json(body.decode(ENCODING_TYPE)):
                    name = json.loads(body.decode(ENCODING_TYPE))["serviceNameSelect"]
                    requested_route = self.get_route_name(name, get_route_list())
                    if requested_route:
                        self.handle_http(STATUS_OK, CONTENT_TYPE_JSON, self.create_json_from_file(requested_route))
                    else:
                        self.handle_http(STATUS_ERROR, CONTENT_TYPE_TEXT, "\"{}\" service does not exist".format(name))
                else:
                    self.handle_http(STATUS_ERROR, CONTENT_TYPE_TEXT, "Malformed JSON")
            elif self.path == "/OPR_DELETE":
                if self.is_data_json(body.decode(ENCODING_TYPE)):
                    name = json.loads(body.decode(ENCODING_TYPE))["serviceNameSelect"]
                    requested_route = self.get_route_name(name, get_route_list())
                    if requested_route:
                        is_deleted = delete_file(requested_route)
                        if is_deleted:
                            self.handle_http(STATUS_OK, CONTENT_TYPE_TEXT, "\"{}\" service JSON deleted.".format(name))
                        else:
                            self.handle_http(STATUS_ERROR, CONTENT_TYPE_TEXT,
                                             "Cannot delete \"{}\" service JSON.".format(name))
                    else:
                        self.handle_http(STATUS_ERROR, CONTENT_TYPE_TEXT, "\"{}\" service does not exist".format(name))
                else:
                    self.handle_http(STATUS_ERROR, CONTENT_TYPE_TEXT, "Malformed JSON")
        else:
            self.handle_path_request()

    def handle_path_request(self):
        if self.path.count("/") == 1:
            if self.path.split("/")[1]:
                requested_route = self.get_route_name(self.get_path(), get_route_list())
                if requested_route:
                    self.handle_http(STATUS_OK, CONTENT_TYPE_JSON, self.create_json_from_file(requested_route))
                else:
                    self.handle_http(STATUS_ERROR, CONTENT_TYPE_TEXT,
                                     "\"{}\" service response does not exist".format(self.get_path()))
            else:
                self.handle_http(STATUS_OK, CONTENT_TYPE_TEXT, read_file(PATH_HTML_FILE))
        else:
            self.handle_http(STATUS_ERROR, CONTENT_TYPE_TEXT, "Wrong path")

    @staticmethod
    def get_route_name(requested_route, routes):
        for rt in routes:
            if os.path.basename(rt).split(".")[0] == requested_route:
                return rt
        return None

    def get_path(self):
        return os.path.basename(self.path)

    @staticmethod
    def is_data_json(data):
        try:
            json.loads(data)
        except ValueError:
            return False
        return True

    @staticmethod
    def create_json_from_file(filename):
        return json.dumps(json.loads(read_file(filename)), indent=JSON_INDENT, ensure_ascii=False)

    @staticmethod
    def create_json_from_string(text):
        return json.dumps(text, indent=JSON_INDENT, ensure_ascii=False)


def read_file(path):
    res_file = None
    try:
        res_file = open(path, 'r', encoding=ENCODING_TYPE)
        file_data = res_file.read()
        res_file.close()
        return file_data
    except Exception as ex:
        if ex:
            print("Error occurred while reading file, exception message: {}".format(ex))
    finally:
        if res_file:
            res_file.close()


def read_image(path):
    res_file = None
    try:
        res_file = open(path, 'rb')
        file_data = res_file.read()
        res_file.close()
        return file_data
    except Exception as ex:
        if ex:
            print("Error occurred while reading file, exception message: {}".format(ex))
    finally:
        if res_file:
            res_file.close()


def write_file(path, data):
    res_file = None
    try:
        res_file = open(path, 'w', encoding=ENCODING_TYPE)
        res_file.write(data)
        return True
    except Exception as ex:
        print("Error occurred while writing file, exception message: {}".format(ex))
    finally:
        if res_file:
            res_file.close()


def update_file(path, updated_content):
    res_file = None
    try:
        res_file = open(path, 'r+', encoding=ENCODING_TYPE)
        res_file.read()
        res_file.seek(0)
        res_file.write(updated_content)
        res_file.truncate()
        res_file.close()
        return True
    except Exception as ex:
        print("Error occurred while writing file, exception message: {}".format(ex))
    finally:
        if res_file:
            res_file.close()


def delete_file(path):
    try:
        os.remove(path)
        return True
    except Exception as ex:
        print("Error occurred while deleting file, exception message: {}".format(ex))


def init_config():
    global config
    config = json.loads(read_file(PATH_CONFIG_FILE))


def get_route_list():
    return glob(os.path.join(PATH_RESPONSE_FOLDER, "*"))


def get_routes_as_json():
    routes = []
    route_list = get_route_list()
    route_list.sort()
    for rt in route_list:
        routes.append({"serviceNameSelect": str(os.path.basename(rt).split(".")[0])})
    return routes


def run():
    print('Starting server...')
    init_config()
    if not os.path.exists(PATH_RESPONSE_FOLDER):
        os.mkdir(PATH_RESPONSE_FOLDER)
    server_address = (config['ip'], int(config['port']))
    httpd = HTTPServer(server_address, BasicServer)
    print("Server running on port: {}".format(config['port']))
    httpd.serve_forever()


if __name__ == '__main__':
    p = Process(target=run())
    p.start()
    p.join()
