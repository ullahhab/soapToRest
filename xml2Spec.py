from lxml import etree
import json

def xml_to_dict(elem):
    """Converts xml to a standard dictionary schema, stripping namespaces."""
    # Strip namespace if present
    tag = elem.tag
    if '}' in tag:
        tag = tag.split('}', 1)[1]

    children = list(elem)
    if not children:
        return {"type": "string", "pattern": "^[a-zA-Z0-9]$"}

    schema = {"type": "object", "properties": {}}
    for child in children:
        if isinstance(child, etree.__Comment):
            continue
        child_tag = child.tag
        if '}' in child_tag:
            child_tag = child_tag.split('}', 1)[1]
        schema["properties"][child_tag] = xml_to_dict(child)
    return schema

def xml_to_tree(xml_path):
    tree = etree.parse(xml_path)
    root = tree.getroot()
    return xml_to_dict(root)
def xml_to_openapi(xml_request_path, xml_response_path, title="Auto API Spec"):
    request_schema = xml_to_tree(xml_request_path)
    response_schema = xml_to_tree(xml_response_path)
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
#print(spec)