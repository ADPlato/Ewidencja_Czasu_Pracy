import xml.etree.ElementTree as ET

class User():
    def __init__(self, no, nr_id, name, card_id, state, time, io):
        self.no=no
        self.nr_id=nr_id
        self.name=name
        self.card_id=card_id
        self.state=state
        self.time=time
        self.io=io

    def __repr__(self):
        return f'{self.io}, {self.time}, {self.name}'


def get_from_xml(input_or_output:str):
    tree = ET.parse(input_or_output+".xml")
    root = tree.getroot()
    user_list=[]
    for users in root.findall('logItem'):
        no=users.find('no').text
        nr_id=users.find('id').text
        name=users.find('name').text
        card_id=users.find('cardId').text
        state=users.find('state').text
        time=users.find('time').text
        io=input_or_output
        user_list.append(User(no,nr_id,name,card_id,state,time,io))
    return user_list
