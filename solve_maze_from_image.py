import os
import cv2 as cv
from tkinter import filedialog, Tk, messagebox, Button, Toplevel
from coloursss import *

class Point:
    def __init__(self, x=0, y=0):
        self.x = x
        self.y = y

    def __add__(self, other):
        return Point(self.x + other.x, self.y + other.y)

    def __eq__(self, other):
        return self.x == other.x and self.y == other.y


def onMouse(event, x, y, flags, params):
    global col, start, end, point_count
    s = 2
    if event == cv.EVENT_LBUTTONUP:
        if point_count == 0:
            col = cv.rectangle(col, (x - s, y - s), (x + s, y + s), color=(0, 0, 255), thickness=-1)
            start = Point(x, y)
            print(f'Start: {start.x}, {start.y}')
            point_count += 1
        elif point_count == 1:
            col = cv.rectangle(col, (x - s, y - s), (x + s, y + s), color=(255, 255, 0), thickness=-1)
            end = Point(x, y)
            print(f'End: {end.x}, {end.y}')
            point_count += 1


def save_maze_image(img, name):
    filename = filedialog.asksaveasfilename(defaultextension=".png",
                                            filetypes=[("PNG files", "*.png"), ("All files", "*.*")], title=name)
    if filename:
        cv.imwrite(filename, img)
        print(f"Saved maze as {filename}")
    else:
        print("No file selected. Not saving.")


def bfs(st, en):
    global col, h, w, directions
    found = False
    queue = []
    visited = [[0 for _ in range(w)] for _ in range(h)]
    parent = [[Point() for _ in range(w)] for _ in range(h)]

    queue.append(st)
    visited[st.y][st.x] = 1

    step_count = 0
    update_frequency = 10

    unsolved_maze = col.copy()

    while queue:
        parent_point = queue.pop(0)

        for direction in directions:
            daughter_cell = parent_point + direction
            if 0 < daughter_cell.x < w and 0 < daughter_cell.y < h:
                if visited[daughter_cell.y][daughter_cell.x] == 0 and (
                        col[daughter_cell.y][daughter_cell.x][0] != 255 or
                        col[daughter_cell.y][daughter_cell.x][1] != 255 or
                        col[daughter_cell.y][daughter_cell.x][2] != 255):

                    queue.append(daughter_cell)
                    visited[daughter_cell.y][daughter_cell.x] = visited[parent_point.y][parent_point.x] + 1

                    col[daughter_cell.y][daughter_cell.x] = GREY

                    parent[daughter_cell.y][daughter_cell.x] = parent_point

                    step_count += 1

                    if step_count % update_frequency == 0:
                        display_image = cv.resize(col, (800, 800))
                        cv.imshow('image', display_image)
                        cv.waitKey(1)

                    if daughter_cell == en:
                        queue.clear()
                        found = True
                        break

    if found:
        point = en
        while point != st:
            cv.rectangle(col, (point.x - 1, point.y - 1), (point.x + 1, point.y + 1), (0, 255, 255), -1)
            point = parent[point.y][point.x]

        solved_maze = col.copy()

        display_image = cv.resize(col, (800, 800))
        cv.imshow('image', display_image)
        cv.waitKey(0)

        handle_replay_or_save(unsolved_maze, solved_maze)

    else:
        print('No path found.')
        display_image = cv.resize(col, (800, 800))
        cv.imshow('image', display_image)
        cv.waitKey(0)


def handle_replay_or_save(unsolved_maze, solved_maze):
    root = Tk()
    root.withdraw()

    replay = messagebox.askyesno("Replay", "Do you want to replay the animation?")
    if replay:
        print("Replay")
        safe_destroy(root)
        return
    else:
        save = messagebox.askyesno("Save", "Do you want to save the maze?")
        if not save:
            print("Not saving")
            safe_destroy(root)
            return
        else:
            custom_save_dialog(root, unsolved_maze, solved_maze)

    cv.destroyAllWindows()
    safe_destroy(root)


def custom_save_dialog(root, unsolved_maze, solved_maze):
    def save_solved():
        save_maze_image(solved_maze, "Save Solved Maze")
        top.destroy()

    def save_unsolved():
        save_maze_image(unsolved_maze, "Save Unsolved Maze")
        top.destroy()

    def save_both():
        save_maze_image(unsolved_maze, "Save Unsolved Maze")
        save_maze_image(solved_maze, "Save Solved Maze")
        top.destroy()

    def exit_without_saving():
        print("Saving cancelled")
        top.destroy()

    top = Toplevel(root)
    top.title("Save Options")

    Button(top, text="Save Solved Maze", command=save_solved).pack(pady=5)
    Button(top, text="Save Unsolved Maze", command=save_unsolved).pack(pady=5)
    Button(top, text="Save Both", command=save_both).pack(pady=5)
    Button(top, text="Exit Without Saving", command=exit_without_saving).pack(pady=5)

    top.wait_window()


def solve_maze_from_image():
    global col, h, w, directions, point_count, start, end

    root = Tk()
    root.withdraw()

    response = messagebox.askyesnocancel("Upload Image",
                                         "Click 'Yes' Upload an image of a maze. Click 'No' to use the default image, or 'Cancel' to exit.")
    if response is None:
        print("Cancelled")
        safe_destroy(root)
        return
    elif response:
        file_path = filedialog.askopenfilename()
        if not file_path:
            print("No file selected.")
            safe_destroy(root)
            return
        _, file_extension = os.path.splitext(file_path)
        if file_extension.lower() not in ['.jpg', '.jpeg', '.png']:
            print(f"{file_extension} unsupported")
            safe_destroy(root)
            return
    else:
        file_path = '12345.jpg'

    point_count = 0
    start = Point()
    end = Point()
    directions = [Point(0, -1), Point(0, 1), Point(1, 0), Point(-1, 0)]
    img = cv.imread(file_path, 0)
    img = cv.resize(img, (512, 512))
    ret, thresh = cv.threshold(img, 150, 255, cv.THRESH_BINARY_INV)
    thresh = cv.resize(thresh, (512, 512))
    col = cv.cvtColor(thresh, cv.COLOR_GRAY2BGR)
    h, w, _ = col.shape

    cv.namedWindow('image')
    cv.setMouseCallback('image', onMouse)
    while True:
        cv.imshow('image', col)
        if cv.waitKey(100) == 27 or point_count == 2:
            break

    bfs(start, end)
    cv.destroyAllWindows()
    safe_destroy(root)


def safe_destroy(window):
    try:
        if window.winfo_exists():
            window.destroy()
    except:
        pass


if __name__=="__main__":
    solve_maze_from_image()
