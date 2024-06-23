from xml.dom.minidom import parse, Node, parseString


# Set the id attribute for all elements that have an attribute named "id"
def set_id_attribute(parent, attribute_name="id"):
    if parent.nodeType == Node.ELEMENT_NODE:
        if parent.hasAttribute(attribute_name):
            parent.setIdAttribute(attribute_name)
    for child in parent.childNodes:
        set_id_attribute(child, attribute_name)

# Parse XML from a filename
document = parse("/Users/jin/jin-git/HiWi/data/delivery process simple.bpmn")
set_id_attribute(document)



# START OF ACTIVITIES
# Save all task IDs in a list
taskIds = []
for element in document.getElementsByTagNameNS("*", "task"):
    taskIds.append(element.getAttribute("id"))

# Count the number of tasks
taskCount = len(taskIds)

taskList = []
dfa = {}

# Retrieve Start Event
startElement = document.getElementsByTagNameNS("*", "startEvent")[0]
startElementName = str(startElement.getAttribute("name"))
dfa[startElementName] = {}
for child in startElement.childNodes:
    if child.nodeType == Node.ELEMENT_NODE:
        if child.tagName == "outgoing":
            dfa[startElementName]['outgoing'] = child.firstChild.data

# Retrieve End Event
endElement = document.getElementsByTagNameNS("*", "endEvent")[0]
endElementName = str(endElement.getAttribute("name"))
dfa[endElementName] = {'incoming': []}
for child in endElement.childNodes:
    if child.nodeType == Node.ELEMENT_NODE:
        if child.tagName == "incoming":
            dfa[endElementName]['incoming'].append(child.firstChild.data)

# Retrieve Tasks
for idx in range(0, taskCount):
    elements = document.getElementsByTagNameNS("*", "task")
    if not elements:
        continue
    taskList.append(elements[idx])  # Saves all task elements in a list

for idx in range(0, taskCount):
    task_name = str(taskList[idx].getAttribute("name"))
    if task_name not in dfa:
        dfa[task_name] = {}
    for child in taskList[idx].childNodes:
        if child.nodeType == Node.ELEMENT_NODE:
            if child.tagName == "incoming":
                dfa[task_name]['incoming'] = child.firstChild.data
            elif child.tagName == "outgoing":
                dfa[task_name]['outgoing'] = child.firstChild.data



# START OF GATEWAYS
# Get all gateway IDs
gatewayTypes = ["exclusiveGateway", "inclusiveGateway", "parallelGateway", "complexGateway"]
gatewayIds = []
gatewayIdx = 0
gatewayList = []

for gatewayType in gatewayTypes:
    gatewayIdx += 1
    for element in document.getElementsByTagNameNS("*", gatewayType):
        gatewayIds.append(str(gatewayType) + f"{gatewayIdx}: " + element.getAttribute("id"))
        gatewayList.append(element)
        element.setAttribute("name", str(gatewayType) + f"{gatewayIdx}_" + element.getAttribute("id"))

# print(f"\nGateway List: {gatewayIds} \n")
# print(f"How many gateways do we have? {len(gatewayIds) / 2}\n")

gatewayCount = len(gatewayIds)

for idx in range(0, gatewayCount):
    elements = document.getElementsByTagNameNS("*", "gateway")
    if not elements:
        continue
    gatewayList.append(elements[idx])  # Saves all task elements in a list

for idx in range(0, gatewayCount):
    gatewayName = str(gatewayList[idx].getAttribute("name"))
    dfa[gatewayName] = {'incoming': [], 'outgoing': []}
    if gatewayName not in dfa:
        dfa[gatewayName] = {}
    for child in gatewayList[idx].childNodes:
        if child.nodeType == Node.ELEMENT_NODE:
            if child.tagName == "incoming":
                dfa[gatewayName]['incoming'].append(child.firstChild.data)
            elif child.tagName == "outgoing":
                dfa[gatewayName]['outgoing'].append(child.firstChild.data)

# print(f"\n{dfa}\n")


# START OF TREE: ADJACENCY LIST

mergedList = taskList + gatewayList
tree = {}
startElementName = str(startElement.getAttribute("name"))
tree[startElementName] = []

endElementName = str(endElement.getAttribute("name"))
tree[endElementName] = []


# Match gateways and startevents
for gateway in gatewayList:
    gatewayName = str(gateway.getAttribute("name"))
    if gatewayName not in tree:
        tree[gatewayName] = []

    for idx in range(0, len(dfa.get(gatewayName).get('incoming'))):
        if dfa.get(startElementName).get('outgoing') == dfa.get(gatewayName).get('incoming')[idx]:
            tree[startElementName].append(gatewayName)

# Match tasks and startevents
for task in taskList:
    taskName = str(task.getAttribute("name"))
    if taskName not in tree:
        tree[taskName] = []

    for idx in range(0, len(dfa.get(taskName).get('incoming'))):
        if dfa.get(startElementName).get('outgoing') == dfa.get(taskName).get('incoming')[idx]:
            tree[startElementName].append(taskName)

# Match tasks and endEvents
for task in taskList:
    taskName = str(task.getAttribute("name"))
    if taskName not in tree:
        tree[taskName] = []

    for idx in range(0, len(dfa.get(endElementName).get('incoming'))):
        if dfa.get(endElementName).get('incoming')[idx] == dfa.get(taskName).get('outgoing'):
            tree[taskName].append(endElementName)

# Match gateways and endEvents
for gateway in gatewayList:
    gatewayName = str(gateway.getAttribute("name"))
    if gatewayName not in tree:
        tree[gatewayName] = []

    for idx in range(0, len(dfa.get(endElementName).get('incoming'))):
        for k in range(0, len(dfa.get(gatewayName).get('outgoing'))):
            if dfa.get(endElementName).get('incoming')[idx] == dfa.get(gatewayName).get('outgoing')[k]:
                tree[gatewayName].append(endElementName)

# Match the incoming and outgoing of tasks
for idx in range(0, len(mergedList)):
    if mergedList[idx].getAttribute('name') not in tree:
        tree[mergedList[idx].getAttribute('name')] = []
    for index in range(0, len(mergedList)):
        if mergedList[index].getAttribute('name') not in tree:
            tree[mergedList[index].getAttribute('name')] = []
        if dfa.get(str(mergedList[idx].getAttribute('name'))).get('outgoing') == dfa.get(
                str(mergedList[index].getAttribute('name'))).get('incoming'):
            # print(f"Matched {mergedList[idx].getAttribute('name')} and {mergedList[index].getAttribute('name')}")
            tree[str(mergedList[idx].getAttribute('name'))].append(str(mergedList[index].getAttribute('name')))

# Match tasks and gateways using the DFA
for task in taskList:
    taskName = str(task.getAttribute("name"))
    if taskName not in tree:
        tree[taskName] = []
    for gateway in gatewayList:
        gatewayName = str(gateway.getAttribute("name"))
        if gatewayName not in tree:
            tree[gatewayName] = []

        # Matching gateways to tasks
        for idx in range(0, len(dfa.get(gatewayName).get('outgoing'))):
            if dfa.get(taskName).get('incoming') == dfa.get(gatewayName).get('outgoing')[idx]:
                # print(f"Matched {gateway.getAttribute('name')} to {task.getAttribute('name')}")
                tree[gatewayName].append(taskName)

        for idx in range(0, len(dfa.get(gatewayName).get('incoming'))):
            if dfa.get(taskName).get('outgoing') == dfa.get(gatewayName).get('incoming')[idx]:
                # print(f"Matched {task.getAttribute('name')} to {gateway.getAttribute('name')}")
                tree[taskName].append(gatewayName)


# print(f"\nHere is the tree {tree}\n")
# for key, value in tree.items():
#     print(f"'{key}': {value}")