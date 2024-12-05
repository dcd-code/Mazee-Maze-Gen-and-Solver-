import os
import cv2 as cv
from tkinter import filedialog, Tk, messagebox, Button, Toplevel
from coloursss import *
# all necessary libraries imported

class Point:
    # Class to represent a point in the maze grid
    def __init__(self, x=0, y=0):
        self.x = x
        self.y = y

    def __add__(self, other):
        # Overload the addition operator to add two points
        return Point(self.x + other.x, self.y + other.y)

    def __eq__(self, other):
        # Overload equality operator to compare two points
        return self.x == other.x and self.y == other.y


def onMouse(event, x, y, flags, params):
    # Callback function to handle mouse events on the maze image
    global col, start, end, point_count
    s = 2  # Size of the marker for start/end points
    if event == cv.EVENT_LBUTTONUP:  # If left mouse button is released
        if point_count == 0:
            # Mark the start point with a red rectangle
            col = cv.rectangle(col, (x - s, y - s), (x + s, y + s), color=(0, 0, 255), thickness=-1)
            start = Point(x, y)  # Set the start point
            print(f'Start: {start.x}, {start.y}')
            point_count += 1
        elif point_count == 1:
            # Mark the end point with a yellow rectangle
            col = cv.rectangle(col, (x - s, y - s), (x + s, y + s), color=(255, 255, 0), thickness=-1)
            end = Point(x, y)  # Set the end point
            print(f'End: {end.x}, {end.y}')
            point_count += 1


def save_maze_image(img, name):
    # Save the maze image to a file
    filename = filedialog.asksaveasfilename(defaultextension=".png",
                                            filetypes=[("PNG files", "*.png"), ("All files", "*.*")], title=name)
    if filename:
        cv.imwrite(filename, img)  # Write the image to the file
        print(f"Saved maze as {filename}")
    else:
        print("No file selected. Not saving.")



def bfs(st, en):
    # Solve the maze using Breadth-First Search (BFS)
    global col, h, w, directions
    found = False  # Flag to indicate if a path was found
    queue = []  # Queue for BFS traversal
    visited = [[0 for _ in range(w)] for _ in range(h)]  # Track visited cells
    parent = [[Point() for _ in range(w)] for _ in range(h)]  # Track parent cells for path reconstruction

    queue.append(st)  # Start BFS from the start point
    visited[st.y][st.x] = 1  # Mark start point as visited

    step_count = 0  # Count steps during BFS
    update_frequency = 10  # Frequency of updates for visual feedback

    unsolved_maze = col.copy()  # Copy of the maze before solving

    while queue:
        parent_point = queue.pop(0)  # Dequeue the front point

        for direction in directions:  # Explore all possible directions
            daughter_cell = parent_point + direction
            if 0 < daughter_cell.x < w and 0 < daughter_cell.y < h:  # Check if within bounds
                if visited[daughter_cell.y][daughter_cell.x] == 0 and (
                        col[daughter_cell.y][daughter_cell.x][0] != 255 or
                        col[daughter_cell.y][daughter_cell.x][1] != 255 or
                        col[daughter_cell.y][daughter_cell.x][2] != 255):  # Check if the cell is not a wall

                    queue.append(daughter_cell)  # Add the cell to the queue
                    visited[daughter_cell.y][daughter_cell.x] = visited[parent_point.y][parent_point.x] + 1

                    col[daughter_cell.y][daughter_cell.x] = GREY  # Mark the cell as visited visually

                    parent[daughter_cell.y][daughter_cell.x] = parent_point  # Record the parent cell

                    step_count += 1  # Increment step count

                    if step_count % update_frequency == 0:  # Update display periodically
                        display_image = cv.resize(col, (800, 800))
                        cv.imshow('image', display_image)
                        cv.waitKey(1)

                    if daughter_cell == en:  # Stop if the end point is reached
                        queue.clear()
                        found = True
                        break

    if found:
        # Trace back the path from the end point to the start point
        point = en
        while point != st:
            cv.rectangle(col, (point.x - 1, point.y - 1), (point.x + 1, point.y + 1), (0, 255, 255), -1)
            point = parent[point.y][point.x]


        solved_maze = col.copy()  # Copy of the solved maze


        display_image = cv.resize(col, (800, 800))
        cv.imshow('image', display_image)
        cv.waitKey(0)

        handle_replay_or_save(unsolved_maze, solved_maze)  # Handle replay or save options

    else:
        print('No path found.')
        display_image = cv.resize(col, (800, 800))
        cv.imshow('image', display_image)
        cv.waitKey(0)


def handle_replay_or_save(unsolved_maze, solved_maze):
    # Handle user options for replaying or saving the maze
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
    # Dialog for saving the solved/unsolved maze images
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


import numpy as np  # Ensure numpy is imported for in-memory image handling

def solve_maze_from_image():
    # Main function to solve a maze from an uploaded image
    global col, h, w, directions, point_count, start, end

    root = Tk()
    root.withdraw()

    response = messagebox.askyesnocancel("Upload Image",
                                         "Click 'Yes' to upload an image of a maze. Click 'No' to use the default image, or 'Cancel' to exit.")
    if response is None:
        print("Cancelled")
        safe_destroy(root)
        return
    elif response:
        file_path = filedialog.askopenfilename()  # Open a file dialog to select the maze image
        if not file_path:
            print("No file selected.")
            safe_destroy(root)
            return


        # Handle file format checking and in-memory conversion
        file_base, file_extension = os.path.splitext(file_path)
        file_extension = file_extension.lower()
        if file_extension not in ['.jpg', '.jpeg', '.png']:
            print(f"Unsupported file format: {file_extension}")
            safe_destroy(root)
            return
        elif file_extension != '.png':
            # Convert to PNG format in memory
            img = cv.imread(file_path)
            if img is None:
                print("Error reading image for conversion.")
                safe_destroy(root)
                return
            print("Image converted to PNG format for internal processing.")
        else:
            img = cv.imread(file_path)
            if img is None:
                print("Error reading image.")
                safe_destroy(root)
                return
    else:
        file_path = '12345.jpg'  # Default image file
        img = cv.imread(file_path)
        if img is None:
            print("Error reading default image.")
            safe_destroy(root)
            return


    point_count = 0
    start = Point()  # Initialize start point
    end = Point()  # Initialize end point
    directions = [Point(0, -1), Point(0, 1), Point(1, 0), Point(-1, 0)]  # Possible movement directions
    img_gray = cv.cvtColor(img, cv.COLOR_BGR2GRAY)  # Convert image to grayscale for processing
    img_gray = cv.resize(img_gray, (512, 512))  # Resize the image to standard size
    ret, thresh = cv.threshold(img_gray, 150, 255, cv.THRESH_BINARY_INV)  # Apply binary thresholding
    thresh = cv.resize(thresh, (512, 512))  # Resize the thresholded image
    col = cv.cvtColor(thresh, cv.COLOR_GRAY2BGR)  # Convert to a color image for visualization
    h, w, _ = col.shape  # Get image dimensions

    cv.namedWindow('image')  # Create a window for displaying the image
    cv.setMouseCallback('image', onMouse)  # Set the mouse callback for selecting points
    while True:
        cv.imshow('image', col)  # Display the maze image
        if cv.waitKey(100) == 27 or point_count == 2:  # Exit on 'Esc' key or when two points are selected
            break

    bfs(start, end)  # Solve the maze using BFS
    cv.destroyAllWindows()
    safe_destroy(root)







def safe_destroy(window):
    # Safely destroy a Tkinter window if it exists
    try:
        if window.winfo_exists():
            window.destroy()
    except:
        pass


if __name__ == "__main__":
    solve_maze_from_image()  # Run the program separately













