from topic.number_systems_ import BinToDec, OctToDec

def pr(**p):
    print(**p)

if __name__ == '__main__':
    test_task1 = BinToDec()
    print(test_task1.generated_text)
    print(test_task1.values_params)
    print(test_task1.calculate_answer(**test_task1.values_params))

    test_task2 = OctToDec()
    print(test_task2.generated_text)
    print(test_task2.values_params)
    print(test_task2.calculate_answer(**test_task2.values_params))