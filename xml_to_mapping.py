from lxml import etree
import csv


def xslt_to_mapping(xslt_path, csv_path):
    xslt_tree = etree.parse(xslt_path)
    ns = {"xsl": "http://www.w3.org/1999/XSL/Transform"}

    mappings = []

    # Extract value-of mappings
    for node in xslt_tree.xpath("//xsl:value-of", namespaces=ns):
        input_xpath = node.get("select")
        output_elem = node.getparent().tag
        mappings.append((input_xpath, output_elem))

    # Write to CSV
    with open(csv_path, "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(["input_xpath", "output_field"])
        writer.writerows(mappings)

    return mappings

mappings = xslt_to_mapping("request.xslt", "mappings.csv")
for m in mappings:
    print(m)