from lxml import etree
import json

def xml_to_dict(elem):
    """Converts xml to a standard dictionary schema"""
    children = list(elem)
    if not children:
        #print(type(elem).__name__)
        return {"type": "string", "pattern": "^[a-zA-Z0-9]$"}
    schema = {"type": "object", "properties": {}}
    for child in children:
        schema["properties"][child.tag] = xml_to_dict(child)
    return schema

def xml_to_openapi(xml_request_path, xml_response_path, title="Auto API Spec"):
    tree = etree.parse(xml_request_path)
    root = tree.getroot()
    request_schema = xml_to_dict(root)
    tree = etree.parse(xml_response_path)
    root = tree.getroot()
    response_schema = xml_to_dict(root)

    spec = {
        "openapi": "3.0.3",
        "info": {"title": title, "version": "1.0.0"},
        "paths": {
            "/example": {
                "post": {
                    "summary": "Auto-generated API from XML",
                    "requestBody": {
                        "required": True,
                        "content": {
                            "application/xml": {
                                "schema": request_schema
                            }
                        }
                    },
                    "responses": {
                        "200": {
                            "description": "Success",
                            "content": {
                                "application/xml": {
                                    "schema": response_schema
                                }
                            }
                        }
                    }
                }
            }
        }
    }

    return json.dumps(spec, indent=2)

spec = xml_to_openapi("RequestTester.xml", 'ResponseTester.xml')
print(spec)