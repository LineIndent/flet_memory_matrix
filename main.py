import flet
from flet import *
import random
import time


class GenerateGrid(UserControl):
    def __init__(self, difficulty):
        self.grid = Column(opacity=0, animate_opacity=200)
        self.incorrect = 0
        self.correct = 0
        self.blue_tiles = 0
        self.difficulty = difficulty
        super().__init__()

    def show_color(self, e):
        if e.control.data == "#4cbbb5":
            e.control.bgcolor = "#4cbbb5"
            e.control.opacity = 1
            e.control.update()
            self.correct += 1
            e.page.update()
        else:
            e.control.bgcolor = "#982c33"
            e.control.opacity = 1
            e.control.update()
            self.incorrect += 1
            e.page.update()

    def build(self):
        rows: list = [
            Row(
                alignment=MainAxisAlignment.CENTER,
                controls=[
                    Container(
                        width=54,
                        height=54,
                        animate=300,
                        on_click=lambda e: self.show_color(e),
                    )
                    for _ in range(5)
                ],
            )
            for _ in range(5)
        ]

        colors: list = ["#5c443b", "#4cbbb5"]

        for row in rows:
            for container in row.controls[:]:
                container.bgcolor = random.choices(
                    colors, weights=[10, self.difficulty]
                )[0]
                container.data = container.bgcolor
                if container.bgcolor == "#4cbbb5":
                    self.blue_tiles += 1

        self.grid.controls = rows
        return self.grid


def main(page: Page):
    page.horizontal_alignment = MainAxisAlignment.CENTER
    page.vertical_alignment = MainAxisAlignment.CENTER

    stage = Text(size=12, weight="bold")
    result = Text(size=16, weight="bold")
    start_button = Container(
        content=ElevatedButton(
            on_click=lambda e: start_game(e, GenerateGrid(2)),
            content=Text(
                "Start!",
                size=13,
                weight="bold",
            ),
            style=ButtonStyle(
                shape={
                    "": RoundedRectangleBorder(radius=8),
                },
                color={
                    "": "white",
                },
            ),
            height=48,
            width=255,
        )
    )

    def start_game(e, level):
        result.value = ""

        grid = level
        page.controls.insert(3, grid)
        page.update()

        grid.controls[0].opacity = 1
        grid.controls[0].update()

        stage.value = f"Stage: {grid.difficulty - 1}"
        stage.update()

        start_button.disabled = True
        start_button.update()

        time.sleep(1.5)

        for rows in grid.controls[0].controls[:]:
            for container in rows.controls[:]:
                if container.bgcolor == "#4cbbb5":
                    container.bgcolor = "#5c443b"
                    container.update()

        while True:
            if grid.correct == grid.blue_tiles:
                grid.grid.disabled: bool = True
                grid.grid.update()
                result.value: str = "GOOD JOB! You got all the tiles!"
                result.color: str = "green700"
                result.update()
                time.sleep(2)
                result.value = ""
                page.controls.remove(grid)
                page.update()
                difficulty = grid.difficulty + 1
                start_game(e, GenerateGrid(difficulty))
                break
            if grid.incorrect == 3:
                result.value = "Sorry, you ran out of tries. Try again!"
                result.color = "red700"
                result.update()
                time.sleep(2)
                page.controls.remove(grid)
                page.update()
                start_button.disabled = False
                start_button.update()
                break

    page.add(
        Row(
            alignment=MainAxisAlignment.CENTER,
            controls=[Text("Memory Matrix", size=22, weight="bold")],
        ),
        Row(
            alignment=MainAxisAlignment.CENTER,
            controls=[result],
        ),
        Divider(height=10, color="transparent"),
        Divider(height=10, color="transparent"),
        Row(
            alignment=MainAxisAlignment.CENTER,
            controls=[stage],
        ),
        Divider(height=10, color="transparent"),
        Row(
            alignment=MainAxisAlignment.CENTER,
            controls=[start_button],
        ),
    )
    page.update()


if __name__ == "__main__":
    flet.app(target=main, view="web_browser")
