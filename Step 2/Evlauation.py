import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

from SnakeAgent import SnakeAgent


# تنظیمات محیط
WIDTH = 20
HEIGHT = 20

EPISODES = 100
MAX_STEPS = 5000


class SnakeEvaluator:

    def __init__(self):
        self.agent = SnakeAgent()
        self.results = []

    # تولید سیب در خانه خالی
    def spawn_apple(self, snake):

        empty_cells = [
            (x, y)
            for x in range(WIDTH)
            for y in range(HEIGHT)
            if (x, y) not in snake
        ]

        if len(empty_cells) == 0:
            return None

        index = np.random.randint(len(empty_cells))

        return empty_cells[index]

    # اجرای یک بازی
    def run_episode(self, episode):

        snake = [
            (5, 10),
            (4, 10),
            (3, 10)
        ]

        apple = self.spawn_apple(snake)

        score = 0
        steps = 0
        reason = "max_steps"

        while steps < MAX_STEPS:

            if apple is None:
                reason = "board_completed"
                break

            # دریافت تصمیم Agent
            action = self.agent.get_action(
                snake,
                apple,
                WIDTH,
                HEIGHT
            )

            if action is None:
                reason = "no_safe_move"
                break

            # محاسبه سر جدید
            new_head = (
                snake[0][0] + action[0],
                snake[0][1] + action[1]
            )

            eating = new_head == apple

            # بررسی برخورد با دیوار
            x, y = new_head

            if not (0 <= x < WIDTH and 0 <= y < HEIGHT):
                reason = "wall_collision"
                break

            # بررسی برخورد با بدن
            body = snake if eating else snake[:-1]

            if new_head in body:
                reason = "self_collision"
                break

            # حرکت مار
            snake.insert(0, new_head)

            if eating:
                score += 1
                apple = self.spawn_apple(snake)
            else:
                snake.pop()

            steps += 1

        # ثبت نتایج
        result = {
            "Episode": episode,
            "Score": score,
            "Steps": steps,
            "Survival": steps,
            "Reason": reason
        }

        return result

    # اجرای تمام آزمایش‌ها
    def evaluate(self):

        for episode in range(1, EPISODES + 1):

            result = self.run_episode(episode)

            self.results.append(result)

            print(
                f"Episode: {episode} | "
                f"Score: {result['Score']} | "
                f"Steps: {result['Steps']} | "
                f"Reason: {result['Reason']}"
            )

        self.save_data()
        self.analyze_data()
        self.plot_results()

    # ذخیره اطلاعات
    def save_data(self):

        df = pd.DataFrame(self.results)

        df.to_csv(
            "snake_results.csv",
            index=False
        )

        print("\nData saved successfully!")

    # تحلیل اطلاعات
    def analyze_data(self):

        df = pd.DataFrame(self.results)

        print("\n========== EVALUATION ==========")

        print("Average Score:",
              df["Score"].mean())

        print("Maximum Score:",
              df["Score"].max())

        print("Average Steps:",
              df["Steps"].mean())

        print("Average Survival:",
              df["Survival"].mean())

        print("\nGame End Reasons:")

        print(df["Reason"].value_counts())

        print("\n================================")

    # رسم نمودارها
    def plot_results(self):

        df = pd.DataFrame(self.results)

        # نمودار امتیاز هر بازی
        plt.figure(figsize=(10, 5))

        plt.plot(
            df["Episode"],
            df["Score"],
            marker="o"
        )

        plt.title("Agent Score per Episode")
        plt.xlabel("Episode")
        plt.ylabel("Score")
        plt.grid(True)

        plt.savefig("score_chart.png")
        plt.show()

        # نمودار تعداد حرکت‌ها
        plt.figure(figsize=

                   (10, 5))

        plt.plot(
            df["Episode"],
            df["Steps"],
            color="green"
        )

        plt.title("Steps per Episode")
        plt.xlabel("Episode")
        plt.ylabel("Steps")
        plt.grid(True)

        plt.savefig("steps_chart.png")
        plt.show()

        # نمودار علت پایان بازی
        plt.figure(figsize=(8, 5))

        df["Reason"].value_counts().plot(
            kind="bar"
        )

        plt.title("Game Over Reasons")
        plt.xlabel("Reason")
        plt.ylabel("Number of Games")

        plt.tight_layout()
        plt.savefig("reason_chart.png")
        plt.show()


# اجرای ارزیابی
if __name__ == "__main__":

    evaluator = SnakeEvaluator()

    evaluator.evaluate()