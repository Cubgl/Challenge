import os


class Finder:
    def __init__(self):
        self.list_topics_data = []
        self.list_topics_names = []
        self.get_list_topics()

    def get_list_topics(self):
        for elem in os.listdir('./topic'):
            if os.path.isfile('./topic/' + elem) and elem.endswith('.py'):
                filename = './topic/' + elem
                module_name = f'topic.{elem[:-3]}'
                exec(f'import {module_name} as module')
                doc_str = eval('module.__doc__')
                if doc_str is not None:
                    self.list_topics_names.append(doc_str.strip())
                    self.list_topics_data.append(self.get_names_class(filename))

    def get_names_class(self, filename):
        list_classes = []
        with open(filename) as file_obj:
            lines = file_obj.readlines()
        for num, line in enumerate(lines):
            pos_class = line.find('class')
            if pos_class != -1:
                part_str = line[pos_class + 6:]
                try:
                    pos_colon = part_str.index('(Task):')
                    name_class = part_str[:pos_colon]
                    list_classes.append(name_class)
                except IndexError as e:
                    print('Ошибка в описании класса (нет двоеточия) в строке {num + 1}: {line}')
        return list_classes
