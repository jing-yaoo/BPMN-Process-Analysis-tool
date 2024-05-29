from xml.dom.minidom import parse, Node, parseString


# Set the id attribute for all elements that have an attribute named "id"
def set_id_attribute(parent, attribute_name="id"):
    if parent.nodeType == Node.ELEMENT_NODE:
        if parent.hasAttribute(attribute_name):
            parent.setIdAttribute(attribute_name)
    for child in parent.childNodes:
        set_id_attribute(child, attribute_name)


# Parse XML from a filename
document = parse("/Users/jin/jin-git/HiWi/data/diagram (3).bpmn")
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
dfa = {}

# Retrieve first task and child nodes
for idx in range(0, taskCount):
    elements = document.getElementsByTagNameNS("*", "task")
    if not elements:
        continue
    taskList.append(elements[idx]) # Saves all task elements in a list

for idx in range(0, taskCount):
    task_name = str(taskList[idx].getAttribute("name"))
    if task_name not in dfa:
        dfa[task_name] = {}
    for child in taskList[idx].childNodes:
        if child.nodeType == Node.ELEMENT_NODE:
            if child.tagName == "bpmn:incoming":
                dfa[task_name]['incoming'] = child.firstChild.data
            elif child.tagName == "bpmn:outgoing":
                dfa[task_name]['outgoing'] = child.firstChild.data

print(f"Task list length: {len(taskList)}")
print(taskList[3].getAttribute("id"))
print(f"Here's the incoming of the first task {dfa.get(str(taskList[0].getAttribute('name'))).get('incoming')}")
print(f"Here's the outgoing of the first task {dfa.get(str(taskList[0].getAttribute('name'))).get('outgoing')}")
print(f"Here's the DFA {dfa}")

#TODO Match the incoming and outgoing of the tasks
# for idx in range(0, taskCount):
   


# Gateways
# Get all gateway IDs
gatewayTypes = ["exclusiveGateway", "inclusiveGateway", "parallelGateway", "complexGateway"]
gatewayIds = []
for gatewayType in gatewayTypes:
    for element in document.getElementsByTagNameNS("*", gatewayType):
        gatewayIds.append(element.getAttribute("id"))
print(f"\nGateway IDs: {gatewayIds} \n")
gatewayCount = len(gatewayIds)
print(f"How many gateways do we have? {gatewayCount / 2}\n")

# Retrieve first gateway and child nodes
for gatewayType in gatewayTypes:
    elements = document.getElementsByTagNameNS("*", gatewayType)
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
