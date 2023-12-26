from abc import ABC, abstractmethod


class TaskInterface(ABC):
    @abstractmethod
    def run(self, subject: str) -> int:
        raise NotImplementedError("run Method not implemented")


class Task1(TaskInterface):

    def run(self, subject: str):
        if isinstance(subject, str):
            return subject.upper()


class Task2(TaskInterface):

    def run(self, subject: str):
        if isinstance(subject, str):
            return subject.capitalize()


class Task3(TaskInterface):

    def run(self, subject: int):
        if isinstance(subject, int):
            return subject * 2


class TaskIterator:
    """
    A composite chain of responsability design pattern iterator
    """

    tasks: dict = {}

    def register(self, name: str, task: TaskInterface):
        if name not in self.tasks.keys():
            self.tasks[name] = task

    def unregister(self, name: str):
        if name in self.tasks.keys():
            del self.tasks[name]

    def run(self):
        results = {}
        for name, task in self.tasks.items():
            results[name] = [task.run(subject) for subject in self.subjects]
        return results

    def __init__(self, *subjects):
        self.subjects = subjects


if __name__ == "__main__":
    task1 = Task1()
    task2 = Task2()
    task3 = Task3()
    task_iterator = TaskIterator("subj1", 7, "subj2", "subj3", 99)
    task_iterator.register('T1', task1)
    task_iterator.register('T2', task2)
    task_iterator.unregister('T2')
    task_iterator.register('T2', task2)
    task_iterator.register('T3', task3)
    results = task_iterator.run()
    print(results)
