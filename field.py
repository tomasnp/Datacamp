import matplotlib.pyplot as plt
import matplotlib.patches as patches

def plot_field(ax):
    """
    Draw a football field on the given axes.

    Parameters:
    ax (matplotlib.axes.Axes): The axes on which to draw the field.

    Returns:
    None
    """
    # terrain
    ax.plot([0,0],[0,80], color = "black")
    ax.plot([0,120],[80,80], color = "black")
    ax.plot([120,120],[80,0], color = "black")
    ax.plot([120,0],[0,0], color = "black")
    # surface de réparation
    ax.plot([0,18],[18,18], color = "black")
    ax.plot([0,18],[62,62], color = "black")
    ax.plot([120,102],[18,18], color = "black")
    ax.plot([120,102],[62,62], color = "black")
    ax.plot([18,18],[18,62], color = "black")
    ax.plot([102,102],[18,62], color = "black")
    # petit rectangle
    ax.plot([0,6],[30,30], color = "black")
    ax.plot([0,6],[50,50], color = "black")
    ax.plot([120,114],[30,30], color = "black")
    ax.plot([120,114],[50,50], color = "black")
    ax.plot([6,6],[30,50], color = "black")
    ax.plot([114,114],[30,50], color = "black")

    # point central
    ax.scatter(60,40, color = "black",s = 15)
    ax.plot([60,60],[80,0], color = "black")

    # point de penalty
    ax.scatter(12,40, color = "black",s = 15)
    ax.scatter(108,40, color = "black",s = 15)

    # Create the arc patch
    arc1 = patches.Arc((12, 40), 19, 19, angle=180, theta1=130, theta2=230, color='black')
    arc2 = patches.Arc((108, 40), 19, 19, angle=180, theta1=310, theta2=50, color='black')

    ax.add_patch(arc1)
    ax.add_patch(arc2)

    # rond central

    rond = patches.Arc((60, 40), 19, 19, angle=0, theta1=0, theta2=360, color='black')

    ax.add_patch(rond)


    # point de corner
    ax.scatter(0,0, color = "black")
    ax.scatter(120,0, color = "black")
    ax.scatter(0,80, color = "black")
    ax.scatter(120,80, color = "black")