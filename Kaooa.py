import turtle
import math

# Function to calculate intersection point of two lines
def find_intersection(p1, p2, q1, q2):
    x1, y1 = p1
    x2, y2 = p2
    x3, y3 = q1
    x4, y4 = q2

    x_num = (x1 * y2 - y1 * x2) * (x3 - x4) - (x1 - x2) * (x3 * y4 - y3 * x4)
    y_num = (x1 * y2 - y1 * x2) * (y3 - y4) - (y1 - y2) * (x3 * y4 - y3 * x4)
    denom = (x1 - x2) * (y3 - y4) - (y1 - y2) * (x3 - x4)

    if denom != 0:
        x = x_num / denom
        y = y_num / denom
        return (x, y)
    else:
        return None

# Function to draw a star with buttons at intersections
def draw_star_with_buttons(size, button_radius):
    turtle.pencolor("#D8D9DA")
    turtle.width(4)
    lines = []
    for _ in range(5):
        # Move to the next position
        current_pos = turtle.position()
        turtle.forward(size)
        next_pos = turtle.position()
        # Draw the star side
        lines.append([current_pos, next_pos])
        turtle.right(144)
    return lines

# Function to find intersection points for all combinations of lines
def find_all_intersections(lines):
    intersections = []
    for i in range(len(lines)):
        for j in range(i + 1, len(lines)):
            intersection_point = find_intersection(lines[i][0], lines[i][1], lines[j][0], lines[j][1])
            if intersection_point:
                intersections.append(intersection_point)
    return intersections

def is_inside_circle(point, center, radius):
    x, y = point
    cx, cy = center
    distance = math.sqrt((x - cx) ** 2 + (y - cy) ** 2)
    return distance <= radius


neighbours = {
    0: [[2,1], [5,6]],
    1: [[2,0],[3,-1],[7,-1],[8,4]],
    2: [[0,-1],[1,3],[5,9],[7,-1]],
    3: [[1,2],[8,6]],
    4: [[6,5],[8,1]],
    5: [[0,-1],[2,7],[6,4],[9,-1]],
    6: [[4,-1],[5,0],[8,3],[9,-1]],
    7: [[1,8],[2,5]],
    8: [[1,7],[3,-1],[4,-1],[6,9]],
    9: [[5,2],[6,8]]
}

# Function to draw clickable button
def draw_clickable_button(center, radius, color="blue", text=""):

    # Create the circular button
    turtle.penup()
    turtle.goto(center[0], center[1] - radius)
    turtle.pendown()
    turtle.fillcolor(color)
    turtle.begin_fill()
    turtle.circle(radius)
    turtle.end_fill()

    # Write the text inside the button
    turtle.penup()
    turtle.goto(center[0], center[1] - radius)
    turtle.pendown()
    turtle.color("white")
    turtle.write(text, align="center", font=("Arial", 12, "normal"))
    turtle.bgcolor("#272829")

    # Register the button click handler
    turtle.onscreenclick(screen_click)

# Set up the Turtle screen
screen = turtle.Screen()
screen.setup(width=1280, height=1280)
screen.title("Kaooa")
# screen.bgpic("pic.png")
turtle.speed(0)
turtle.pensize(2)
turtle.penup()
turtle.setx(-200)
turtle.pendown()
turtle.tracer(0)
# Draw a star with buttons at intersections
lines = draw_star_with_buttons(500, 25)
points = find_all_intersections(lines)
sur_crow=7
i=0
crow_count=0
previous_yellow_button = None
def check_valid(cur_point_ind,prev_point_ind):
    if button_colors[cur_point_ind]==0:
        for neighbour in neighbours[prev_point_ind]:
            if neighbour[0]==cur_point_ind:
                return 1
            elif neighbour[1]== cur_point_ind:
                if button_colors[neighbour[0]]==1:
                    return points[neighbour[0]]
    return 0
def check(ind):
    for neighbour in neighbours[ind]:
        if button_colors[neighbour[0]]==0 or (neighbour[1]!=-1 and button_colors[neighbour[1]]==0):
            return True
    return False
def screen_click(x, y):
    global i
    global previous_yellow_button
    global crow_count
    global sur_crow
    for point in points:
        if is_inside_circle((x, y), point, 25):
            color="#61677A"
            if i%2==0:
                # shouldnot click on empty space or vulture
                color = "#FFF6E0"
                # print(crow_count)
                if crow_count == 7:
                    if button_colors[points.index(point)]==1: 
                        color="#61677A"
                        crow_count=6
                        i=i-1
                    else:
                        print(i)
                        # i=i-1
                        continue
                else:
                    if button_colors[points.index(point)]==0:
                        crow_count+=1
                    else:
                        continue
                # print(crow_count)
                # print(f"crowcount:{crow_count}  i:{i}")
            else:
                if button_colors[points.index(point)]==0:
                    print(f"else:{i}")
                    print(f"else:{crow_count}")
                    if previous_yellow_button and check_valid(points.index(point),points.index(previous_yellow_button))==1:
                        if point != previous_yellow_button:
                            # Make the previously yellow button blue
                                button_colors[points.index(previous_yellow_button)] = 0
                                draw_clickable_button(previous_yellow_button, 25, color="#61677A")
                        previous_yellow_button = point
                        color="#E78895"
                    elif previous_yellow_button and type(check_valid(points.index(point),points.index(previous_yellow_button)))==tuple:
                        sur_crow-=1
                        draw_clickable_button(check_valid(points.index(point),points.index(previous_yellow_button)),25,color="#61677A")
                        button_colors[points.index(check_valid(points.index(point),points.index(previous_yellow_button)))]=0
                        if point != previous_yellow_button:
                            # Make the previously yellow button blue
                                button_colors[points.index(previous_yellow_button)] = 0
                                draw_clickable_button(previous_yellow_button, 25, color="#61677A")
                        previous_yellow_button = point
                        color="#E78895"
                    elif not previous_yellow_button:
                        previous_yellow_button = point
                        color = "#E78895"
                    else:
                        i -= 1
                else:
                    continue
            i += 1
            turtle.fillcolor(color)
            if color=="#FFF6E0":
                button_colors[points.index(point)]=1
            elif color=="#61677A":
                button_colors[points.index(point)]=0
            else:
                button_colors[points.index(point)]=2
            draw_clickable_button(point,25, color=color, text="")
            if previous_yellow_button:
                if not check(points.index(previous_yellow_button)):
                    # print(points.index(previous_yellow_button))
                    # print(button_colors)
                    turtle.clear()
                    turtle.penup()
                    turtle.pencolor("#61677A")
                    turtle.goto(0, 0)
                    turtle.write("Crows win!", align="center", font=("Arial", 50, "bold"))
                    turtle.done()
                    return
            if sur_crow<=3:
                turtle.clear()
                turtle.penup()
                turtle.pencolor("#E78895")
                turtle.goto(0, 0)
                turtle.write("Vulture wins!", align="center", font=("Arial", 50, "bold"))
                turtle.done()
                return
                
                
button_colors=[0]*10
# Draw clickable buttons at intersection points
for inde,point in enumerate(points):
    draw_clickable_button(point, 25, color="#61677A", text=str(inde))
text_turtle = turtle.Turtle()
text_turtle.speed(0)
text_turtle.penup()
text_turtle.pencolor("#D8D9DA")
def draw_text_buttons():
    # Crow Button
    text_turtle.penup()
    text_turtle.goto(-380,0)
    text_turtle.pendown()
    text_turtle.fillcolor("#FFF6E0")
    text_turtle.begin_fill()
    text_turtle.circle(30)
    text_turtle.end_fill()
    text_turtle.penup()
    text_turtle.goto(-380, -30)
    text_turtle.pendown()
    text_turtle.write("Crow", align="center", font=("Arial", 14, "bold"), move=True)

    # Vulture Button
    text_turtle.penup()
    text_turtle.goto(-380, -110)
    text_turtle.pendown()
    text_turtle.fillcolor("#E78895")
    text_turtle.begin_fill()
    text_turtle.circle(30)
    text_turtle.end_fill()
    text_turtle.penup()
    text_turtle.goto(-380, -140)
    text_turtle.pendown()
    text_turtle.write("Vulture", align="center", font=("Arial", 14, "bold"), move=True)

# Draw buttons for Crow and Vulture
draw_text_buttons()
text_turtle.penup()
text_turtle.goto(0, 300)
text_turtle.pendown()
text_turtle.write("The Kaooa Game", align="center", font=("Arial", 50, "bold"))
text_turtle.hideturtle()
# def startgame():
    
# Keep the window open
turtle.update()
turtle.done()

