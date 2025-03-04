import matplotlib.pyplot as plt
import numpy as np
def angle_between_points(A, B, C):
    """Calculate the angle (in degrees) formed at point B by the lines BA and BC."""
    # Convert points to numpy arrays

    # Vectors BA and BC
    BA = A - B
    BC = C - B

    # Compute dot product and magnitudes
    dot_product = np.dot(BA, BC)
    norm_BA = np.linalg.norm(BA)
    norm_BC = np.linalg.norm(BC)

    # Compute the angle in radians
    angle_rad = np.arccos(dot_product / (norm_BA * norm_BC))

    # Convert to degrees
    angle_deg = np.degrees(angle_rad)

    return angle_deg


def create_cone_geometry(z_inner, inner_cone_rad, cone_angle,cone_length,thickness,outer_ending_angle, inner_ending_angle):
    '''
    the cone constructued is the rotationvolume of a specific trapezoid.
    D  ____d_____  C    
      /          \      
     /            \  
    /______________\  
    A       b       B
    for the construction one specifies C (x,y are the first two arguments), d (cone_length),height (thickness),
    the flaring angles and the general angle of d to the x-axis. with inner is the rightside (C,B) referred to, outer the leftside (A,D)
    returned are the positions of C,B,D,A together with the y_axis thickness 
    (given line paralell to y axis intersecting with d,b it would be the distance between those intersectionpoints)
    '''
    c_alpha = np.cos(np.pi / 180 * cone_angle)
    s_alpha = np.sin(np.pi / 180 * cone_angle)
    unit_dir_away = np.array((s_alpha,c_alpha))
    unit_dir_along = np.array((-c_alpha,s_alpha))
    y_axis_thickness = thickness/c_alpha
    
    C = np.array((z_inner,inner_cone_rad))
    D = C + unit_dir_along*cone_length 

    inner_flaring_angle = 90 -cone_angle-inner_ending_angle
    inner_angle_line_shift = thickness * np.tan(np.pi / 180 * inner_flaring_angle)
    B =C - thickness *unit_dir_away + inner_angle_line_shift*unit_dir_along 

    outer_flaring_angle = 90 -cone_angle-outer_ending_angle
    outer_angle_line_shift = thickness * np.tan(np.pi / 180 * outer_flaring_angle)
    A =D - thickness *unit_dir_away + outer_angle_line_shift*unit_dir_along 

    return (C,B,D,A),y_axis_thickness



# Define points (x-coordinates and y-coordinates)
points,thickness = create_cone_geometry(1,1,40,10,1,50,20)
x, y = zip(*points)

# Create scatter plot
plt.scatter(x, y, color='red', marker='o')

# Labels and title
plt.xlabel("X-axis")
plt.ylabel("Y-axis")
plt.axis("equal")

plt.title("Scatter Plot of Points")

# Show plot
plt.show()