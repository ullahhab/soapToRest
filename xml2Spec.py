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

def xml_to_openapi(xml_path, title="Auto API Spec"):
    tree = etree.parse(xml_path)
    root = tree.getroot()
    schema = xml_to_dict(root)

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
                                "schema": schema
                            }
                        }
                    },
                    "responses": {
                        "200": {
                            "description": "Success",
                            "content": {
                                "application/xml": {
                                    "schema": schema
                                }
                            }
                        }
                    }
                }
            }
        }
    }

    return json.dumps(spec, indent=2)

file = open("tester.xml", 'r')
file = file.read()
print(file)

spec = xml_to_openapi("tester.xml")
print(spec)