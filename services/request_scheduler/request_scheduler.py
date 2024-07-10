from concurrent.futures import ThreadPoolExecutor, as_completed


class RequestScheduler:
    def __init__(self, max_workers=8):
        self.max_workers = max_workers

    def execute(self, tasks):
        results = []

        with ThreadPoolExecutor(max_workers=self.max_workers) as executor:
            future_to_task = {executor.submit(task): task for task in tasks}

            for future in as_completed(future_to_task):
                try:
                    result = future.result()
                    results.append(result)
                except Exception as e:
                    results.append(e)

        return results

    def execute_generator(self, tasks):
        with ThreadPoolExecutor(max_workers=self.max_workers) as executor:
            future_to_task = {executor.submit(task): task for task in tasks}

            for future in as_completed(future_to_task):
                try:
                    yield future.result()
                except Exception as e:
                    yield e
