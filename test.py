from topic.excel_table_ import *
from topic.number_systems_ import *


def pr(**p):
    print(**p)

if __name__ == '__main__':
    test_task1 = CalcFromIndirectInformation()
    test_task1.make_task()
    print(test_task1.generated_text)
    print(test_task1.values_params)
    print(test_task1.calculate_answer(**test_task1.values_params))
    print(test_task1.task_image)

    # test_task2 = DecToOtherNumberSystemWithLetters()
    # test_task2.render_text()
    # print(test_task2.generated_text)
    # print(test_task2.values_params)
    # print(test_task2.calculate_answer(**test_task1.values_params))

