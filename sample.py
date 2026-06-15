from dataclasses import dataclass


@dataclass(frozen=True)
class Task:
    title: str
    done: bool


def summarize_tasks(tasks: list[Task]) -> tuple[int, int]:
    completed = sum(task.done for task in tasks)
    remaining = len(tasks) - completed
    return completed, remaining


def main() -> None:
    tasks = [
        Task(title="Write code", done=True),
        Task(title="Review changes", done=False),
        Task(title="Run checks", done=True),
    ]

    completed, remaining = summarize_tasks(tasks)

    print("Task summary")
    print("-" * 20)
    for task in tasks:
        status = "done" if task.done else "todo"
        print(f"{task.title}: {status}")

    print("-" * 20)
    print(f"Completed: {completed}")
    print(f"Remaining: {remaining}")


if __name__ == "__main__":
    main()