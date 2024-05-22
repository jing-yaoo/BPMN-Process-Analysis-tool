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


# Activities
# Save all task IDs in a list
taskIds = []
for element in document.getElementsByTagNameNS("*", "task"):
  taskIds.append(element.getAttribute("id"))
print(f"\nTask IDs: {taskIds} \n")

# Count the number of tasks
taskCount = len(taskIds)
print(f"How many tasks do we have? {taskCount}\n")

taskList = []
dfa = {0:{'0':0, '1':1},}

for idx in range(0, taskCount):
    elements = document.getElementsByTagNameNS("*", "task")
    if not elements:
        continue
    taskList.append(elements[0])
    
for child in taskList[0].childNodes:
    if child.nodeType == Node.ELEMENT_NODE:
        if child.tagName == "bpmn:incoming":
            dfa.__setitem__("incoming",{child.firstChild.data})
        elif child.tagName == "bpmn:outgoing":
            dfa.__setitem__("outgoing", {child.firstChild.data})

# Gateways
# Get all gateway IDs
gatewayTypes = ["exclusiveGateway", "inclusiveGateway", "parallelGateway", "complexGateway"]
gatewayIds = []
for gatewayType in gatewayTypes:
    for element in document.getElementsByTagNameNS("*", gatewayType):
        gatewayIds.append(element.getAttribute("id"))
print(f"\nGateway IDs: {gatewayIds} \n")
gatewayCount = len(gatewayIds)
print(f"How many gateways do we have? {gatewayCount/2}\n")


# Retrieve first gateway and child nodes
for gatewayType in gatewayTypes:
    elements = document.getElementsByTagNameNS("*",gatewayType)
    if not elements:
        continue
    gateway = elements[0]

incoming = []
outgoing = []
for child in gateway.childNodes:
    if child.nodeType == Node.ELEMENT_NODE:
        if child.tagName == "bpmn:incoming":
            incoming.append(child.firstChild.data)
        elif child.tagName == "bpmn:outgoing":
            outgoing.append(child.firstChild.data)
            

print(gateway.getAttribute("id"))
print(incoming)
print(outgoing)
