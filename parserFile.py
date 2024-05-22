from xml.dom.minidom import parse, Node, parseString

# Set the id attribute for all elements that have an attribute named "id"
def set_id_attribute(parent, attribute_name="id"):
    if parent.nodeType == Node.ELEMENT_NODE:
        if parent.hasAttribute(attribute_name):
            parent.setIdAttribute(attribute_name)
    for child in parent.childNodes:
        set_id_attribute(child, attribute_name)

# Parse XML from a filename
document = parse("/Users/jin/jin-git/HiWi/diagram (3).bpmn")
set_id_attribute(document)

# Save all task IDs in a list
taskIds = []
for element in document.getElementsByTagNameNS("*", "task"):
  taskIds.append(element.getAttribute("id"))
print(taskIds)

print(len(taskIds))

dfa = {0:{'0':0, '1':1},
       1:{'0':2, '1':0},
       2:{'0':1, '1':2}}

print (dfa.keys(1,'0'))
