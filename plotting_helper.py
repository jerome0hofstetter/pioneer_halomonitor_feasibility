import numpy as np
import matplotlib.pyplot as plt
from matplotlib.widgets import CheckButtons,TextBox,Button,RadioButtons
from utils_math import *


def plot_histogram_radius(ax,xpos,ypos,zpos,id,show_id,radius_cutoff=0,bin_amount=200,aggreg=True,rad_normalized=True,peak_scaling=True,smooth=False):
    """
    given a matplotlib axis, the hitdatas x,y,z and id as well as some settings parameter
    create a histogram for the radius (r² = xpos²+ypos²) on that axis
    filtering is in the form of 

    "show_id" : list of ids that should be considered

    "radius_cutoff": radius cutoff (absolute value), if positive include [0,cutoff] else include [cutoff,infinity]
    the settings

    "bin_amount" : bincount for histogram

    "aggreg" : either (if True) one histogram with all hits else for each different id the plot is made seperatly

    "rad_normalized" : weight hits depending on radius, 1/r or weight all hits equaly

    "peak_scaling" : for aggreg=False scale seperate each histogram to peak at 1 or scale such that area is 1

    "smooth" : try to smooth the plot or not #TODO improve
    """
    r = np.sqrt(xpos**2 + ypos**2)
    if show_id is None or len(show_id)==0:
        return
    filter_list =[]
    if aggreg:
        filter_list.append((np.isin(id, show_id),None))
    else:
        filter_list = [(id==i,i) for i in show_id]

    ax.set_title(f"{'radius corrected' if rad_normalized else 'radius'} Histogram,\n{'peak normalized' if peak_scaling else 'area normalized'}")
    ax.set_xlabel("Radius")
    ax.set_ylabel("Frequency")
    radcondition = np.sign(radius_cutoff) *r < radius_cutoff if radius_cutoff!=0 else True
    colormap = get_pdid_color_map()
    for filter,particle in filter_list:
        filter = filter & radcondition
        weights = None
        if rad_normalized:
            weights = 1/r[filter]
        bin_edges,counts,total_sum = get_outline_histo(r[filter],bin_amount,weights=weights,smooth=smooth)
        if peak_scaling:
            counts = counts/np.max(counts)
        else:
            counts = counts/total_sum
        color = colormap[particle][0] if particle else "black"
        label = colormap[particle][1] if particle else "aggregate"
        ax.plot(bin_edges,counts,label =label, color=color)
    ax.legend()


def plot_histogram_angle(ax,xpos,ypos,zpos,id,show_id,radius_cutoff=0,bin_amount=200,aggreg=True,angle_mod = 360,angle_shift=-45,peak_scaling=True,smooth=False):
    """
    given a matplotlib axis, the hitdatas x,y,z and id as well as some settings parameter
    create a histogram for the angle in degrees (xpos,ypos considered, center 0,0) 
    filtering is in the form of :

    "show_id" : list of ids that should be considered

    "radius_cutoff": radius cutoff (absolute value), if positive include [0,cutoff] else include [cutoff,infinity]

    the settings:

    "angle_mod" : take radius modulo this

    "angle_shift" : angle shift, radius domain then is [angle_shift,angle_shift+angle_mod]

    "bin_amount" : bincount for histogram

    "aggreg" : either (if True) one histogram with all hits else for each different id the plot is made seperatly

    "peak_scaling" : for aggreg=False scale seperate each histogram to peak at 1 or scale such that area is 1

    "smooth" : try to smooth the plot or not #TODO improve

    """
    r = np.sqrt(xpos**2 + ypos**2)
    angle = (np.rad2deg(np.arctan2(ypos, xpos)) -angle_shift)%angle_mod +angle_shift
    if show_id is None or len(show_id)==0:
        return
    filter_list =[]
    if aggreg:
        filter_list.append((np.isin(id, show_id),None))
    else:
        filter_list = [(id==i,i) for i in show_id]
        
    
    ax.set_title(f"Angle Histogram, \n{'peak normalized' if peak_scaling else 'area normalized'}")
    ax.set_xlabel("angle (degrees)")
    ax.set_ylabel("Frequency")
    radcondition = np.sign(radius_cutoff) *r < radius_cutoff if radius_cutoff!=0 else True
    colormap = get_pdid_color_map()
    for filter,particle in filter_list:
        filter = filter & radcondition
        bin_edges,counts,total_sum = get_outline_histo(angle[filter],bin_amount,smooth=smooth)
        if peak_scaling:
            counts = counts/np.max(counts)
        else:
            counts = counts/total_sum
        color = colormap[particle][0] if particle else "black"
        label = colormap[particle][1] if particle else "aggregate"
        ax.plot(bin_edges,counts,label =label, color=color)
    ax.legend()


def plot_2dhistogram_radius_angle(ax,fig,xpos,ypos,zpos,id,show_id,radius_cutoff=0,xbins=180,ybins=180,rad_normalized=True,angle_mod = 360,angle_shift=0):
    """
    given a matplotlib axis, the hitdatas x,y,z and id as well as some settings parameter
    create a 2dhistogram for the radius (r² = xpos²+ypos²) and angle in degrees (xpos,ypos considered, center 0,0) on that axis
    filtering is in the form of 
    
    "show_id" : list of ids that should be considered

    "radius_cutoff": radius cutoff (absolute value), if positive include [0,cutoff] else include [cutoff,infinity]
    the settings

    "angle_mod" : take radius modulo this

    "angle_shift" : angle shift, radius domain then is [angle_shift,angle_shift+angle_mod]

    "bin_amount" : bincount for histogram

    "aggreg" : either (if True) one histogram with all hits else for each different id the plot is made seperatly

    "rad_normalized" : weight hits depending on radius, 1/r or weight all hits equaly

    "peak_scaling" : for aggreg=False scale seperate each histogram to peak at 1 or scale such that area is 1

    "smooth" : try to smooth the plot or not #TODO improve

    """
    r = np.sqrt(xpos**2 + ypos**2)
    angle = (np.rad2deg(np.arctan2(ypos, xpos)) -angle_shift)%angle_mod +angle_shift
    if show_id is None or len(show_id)==0:
        return

    ax.set_title(f"radius Angle Histogram")
    ax.set_xlabel("angle (degrees)")
    ax.set_ylabel("radius")
    radcondition = np.sign(radius_cutoff) *r < radius_cutoff if radius_cutoff!=0 else True
    filter = np.isin(id, show_id) & radcondition
    weights=None
    if rad_normalized:
        weights = 1/r[filter]
    xedges,yedges,counts,total_sum = get_outline_histo2d(angle[filter],r[filter],xbins,ybins,weights=weights)
    X, Y = np.meshgrid(xedges, yedges)  
    pc = ax.pcolormesh(X, Y, counts, cmap='viridis', shading='auto')

    fig.colorbar(pc, ax=ax, label=f"{'1/r weighted' if rad_normalized else ''}Counts")


def plot_rough_flat(xpos,ypos,zpos,id):
    """
    for fast testing histogram of data xpos,ypos plot
    """
    colormap = get_pdid_color_map()
    color_from_id = [colormap[i][0] for i in id]
    plt.figure(figsize=(6, 6))
    plt.scatter(xpos, ypos, c = color_from_id, s=10)
    plt.title("2D Projection of Data on a Cone")
    plt.xlabel("x")
    plt.ylabel("y")
    plt.axis('equal')  
    plt.legend(handles=[plt.Line2D([0], [0], marker='o', color='w', markerfacecolor=color, markersize=10) for color,_ in colormap.values()],
           labels=[label for _, label in colormap.values()], title="Particles")

    plt.show()

def plot_rough_3d(xpos,ypos,zpos,fitresult=None):
    """
    for fast testing histogram of data xpos,ypos plot, plots in 3d


    - "fitresult" : None or expects the fitresult returned from :func:'utils.fit_cone'. If given it will plot the fitted cone via plot_surface
    """
    fig = plt.figure(figsize=(10, 7))
    ax = fig.add_subplot(111, projection='3d')

    # Create a 3D scatter plot
    ax.scatter(xpos, ypos, zpos, c='r', marker='o')
    if fitresult:
        x_fit = np.linspace(np.min(xpos), np.max(xpos), 200)
        y_fit = np.linspace(np.min(ypos), np.max(ypos), 200)
        x_fit, y_fit = np.meshgrid(x_fit, y_fit)
        radfilter = x_fit**2 + y_fit**2<np.max(np.abs(np.concatenate((x_fit, y_fit))))**2
        z_fit = cone_model(x_fit[radfilter],y_fit[radfilter],fitresult.best_values['a'],fitresult.best_values['x0'],fitresult.best_values['y0'],fitresult.best_values['z0'] )
        ax.plot_surface(x_fit, y_fit, z_fit, color='b', alpha=0.3, rstride=5, cstride=5)

    ax.set_xlabel('X Position')
    ax.set_ylabel('Y Position')
    ax.set_zlabel('Z Position')

    ax.set_title('Detector Positions in 3D Space')
    plt.show()


def plot_by_radius_corrected(xpos,ypos,zpos,id):
    """
    for fast testing different plots histograms for radius or angle, if for radius then its weighted by 1/r
    """
    
    r = np.sqrt(xpos**2 + ypos**2)
    angle = (np.rad2deg(np.arctan2(ypos, xpos)) + 45)%360 -45 # in degrees
    mod_angle = (angle + 45) % 90 - 45

    fig, ax = plt.subplots(2, 3, figsize=(12, 6))
    ax = ax.flatten()
    # Histogram for radius
    n,bins,patches = ax[0].hist(r, bins=100, density=True,color='blue', alpha=0.7)
    ax[0].set_title("Histogram of Radius")
    ax[0].set_xlabel("Radius")
    ax[0].set_ylabel("Frequency")

    bin_centers = (bins[:-1] + bins[1:]) / 2 
    n_corrected = n / bin_centers
    bin_widths = np.diff(bins)
    ax[1].bar(bin_centers, n_corrected, width=bin_widths,color='r', label='radius corrected histogram')

    ax[1].set_xlabel('Radius')
    ax[1].set_ylabel('Frequency corrected')

    # Histogram for angle
    ax[2].hist(angle, bins=120,density=True, color='green', alpha=0.7)
    ax[2].set_title("Histogram of Angle -45 - 275 degree")
    ax[2].set_xlabel("Angle (degrees)")
    ax[2].set_ylabel("propability")

    ax[3].hist(mod_angle, bins=120,density=True, color='green', alpha=0.7)
    ax[3].set_title("Histogram of Angle mod 90 , -45 -45 degrees")
    ax[3].set_xlabel("Angle (degrees)")
    ax[3].set_ylabel("propability")
    hist = ax[4].hist2d(r, angle, bins=150, cmap='plasma')
    fig.colorbar(hist[3], ax=ax[4])
    ax[4].set_xlabel("radius")
    ax[4].set_ylabel("angle (degrees)")
    #plot_histogram_radius(ax[5],xpos,ypos,zpos,id,np.unique(id))
    #plot_2dhistogram_radius_angle(ax[5],fig,xpos,ypos,zpos,id,np.unique(id),0,rad_normalized=True)
    plot_histogram_angle(ax[5],xpos,ypos,zpos,id,np.unique(id),angle_mod=180,aggreg=False,peak_scaling=False,smooth=True)

    # Show the plot
    plt.tight_layout()
    plt.show()
    

def plot_with_filter(xpos,ypos,zpos,id,add_extra_row = True,use_3d=False):
    """
    this is a more interactive  plotting function of the given hitdata

    points have a color corresponding to their id with checkboxes of the same color acting as label and filter for that id

    options:
    - "use_3d" : if the initial plot should be in 3d or 2d (only x and y)

    - "add_extra_row" : if a row below the plot should be added that can interactivly create different histograms
    """
    #prep
    colormap = get_pdid_color_map()
    string_to_id = {}
    for key in colormap.keys():
        string_to_id[colormap[key][1]] = key

    unique_id = np.unique(id)

    fig, ax = None,None

    if use_3d:
        fig = plt.figure(figsize=(10, 7))
        ax = fig.add_subplot(111, projection='3d')
    else:
        fig, ax = plt.subplots()
    right = 0.99
    left = 0.095
    top =0.93
    height_text = 0.045
    lowerheight = 0.07 if add_extra_row else 0
    bottom_buffer  =0.005
    plt.subplots_adjust(left=left,right=right,top=top,bottom =bottom_buffer +lowerheight+height_text  )   

    scatters = {}
    #coming label trigger
    def filter_toggle(label):
        key = string_to_id[label]
        vis = not scatters[key].get_visible()
        scatters[key].set_visible(vis)
        plt.draw()
    def get_active_ids():
        return [key for key in scatters.keys() if scatters[key].get_visible()]
    
    checklist = []
    width = (right-left)/len(unique_id)
    def cond_scatterplot(key,filt):
        if use_3d:
            scatters[key] = ax.scatter(xpos[filt],ypos[filt], zpos[filt],color=colormap[key][0], label=colormap[key][1],marker='.', s=12,alpha=0.5)
        else:
            scatters[key] = ax.scatter(xpos[filt],ypos[filt], color=colormap[key][0], label=colormap[key][1],marker='.', s=12,alpha=0.5)

    # for each unique_id do the scatterplot and save in a dict, further add a checkbutton that can toggle the visibility
    for i,key in enumerate(unique_id):
        filt = id==key
        cond_scatterplot(key,filt)
        rax = plt.axes([left+i*width,top,width,0.05])
        color = colormap[key][0]
        check = CheckButtons(rax, [colormap[key][1]], [True] ,    label_props={'color': [color]},
            frame_props={'edgecolor': [color]},
            check_props={'facecolor': [color]},
        )
        check.on_clicked(filter_toggle)
        checklist.append(check)

    # this adds a row below the plot with a radius filter and multiple interactive elements and 2 buttons
    # the 2 buttons open either 1d or 2d histographs with the data filtered via radiusfilter or id filter and some options set
    # via the interactive elements
    if add_extra_row:
        textbox_itself = 0.04
        textbox_text = 0.12
        textbox_width = textbox_itself + textbox_text
        go_width = 0.1
        option_width = (right-left - go_width - textbox_width)/3
        option_height = lowerheight
        d1plot_axes = plt.axes([left, bottom_buffer, go_width, lowerheight/2])
        d2plot_axes = plt.axes([left, bottom_buffer+lowerheight/2, go_width, lowerheight/2])
        option_axes = []
        for k in range(3):
            option_axes.append(plt.axes([left+go_width+option_width*k, bottom_buffer, option_width, option_height]))
        angular = RadioButtons(option_axes[0], ['360°', '180°','90°'])
        option1_buttons = CheckButtons(option_axes[1], ['1/r weighted', 'smooth',])
        option2_buttons = CheckButtons(option_axes[2], ['aggregate', 'peak_scaled',])
        def on_text_change(text):
            try:
                radius_limit = float(text)
                radfiltered = np.sqrt(xpos**2 + ypos**2)
                radcondition = np.sign(radius_limit) *radfiltered < radius_limit if radius_limit !=0 else True

                for key in unique_id:
                    filt = (id==key) & radcondition
                    visibility = scatters[key].get_visible()
                    scatters[key].remove() 
                    cond_scatterplot(key,filt)
                    scatters[key].set_visible(visibility)
                plt.draw()
            except ValueError:
                pass
        
        textbox_axes = plt.axes([right-textbox_itself, bottom_buffer+lowerheight/2, textbox_itself, lowerheight/2])
        textbox = TextBox(textbox_axes, 'r filter', initial="-0")
        textbox.on_submit(on_text_change)
        bin_textbox_axes = plt.axes([right-textbox_itself, bottom_buffer, textbox_itself, lowerheight/2])
        bin_textbox = TextBox(bin_textbox_axes, 'bincount', initial="100")
        plot1_button = Button(d1plot_axes, "plot 1d")
        plot2_button = Button(d2plot_axes, "plot 2d")

        #define the action of the two buttons and append them
        #get values from the interactive elements and plot either 1d histograms or 2dhistograms depending which button
        def plot_1d(event):
            radius_limit=0
            angle_mod = 360
            bincount=150
            try:
                radius_limit = float(textbox.text)
                angle_mod = float(angular.value_selected[:-1])
                bincount = abs(int(bin_textbox.text))
            except:
                pass

            fig, ax = plt.subplots(1, 2, figsize=(14, 7))
            show_id = get_active_ids()
            plot_histogram_radius(ax[0],xpos,ypos,zpos,id,show_id,rad_normalized=option1_buttons.get_status()[0],
                                  radius_cutoff=radius_limit,bin_amount=bincount,aggreg=option2_buttons.get_status()[0],
                                  peak_scaling=option2_buttons.get_status()[1],smooth=option1_buttons.get_status()[1])
            plot_histogram_angle(ax[1],xpos,ypos,zpos,id,show_id,radius_cutoff=radius_limit,angle_mod=angle_mod,aggreg=option2_buttons.get_status()[0],
                                 peak_scaling=option2_buttons.get_status()[1],smooth=option1_buttons.get_status()[1])

            plt.tight_layout()
            plt.show(block=False)      

        def plot_2d(event):
            radius_limit=0
            angle_mod = 360
            bincount=150
            try:
                radius_limit = float(textbox.text)
                angle_mod = float(angular.value_selected[:-1])
                bincount = abs(int(bin_textbox.text))
            except :
                pass
            fig, ax = plt.subplots()
            plot_2dhistogram_radius_angle(ax,fig,xpos,ypos,zpos,id,get_active_ids(),
                                          radius_cutoff=radius_limit,xbins = bincount,ybins=2*bincount,
                                          rad_normalized=option1_buttons.get_status()[0],angle_shift=-45,angle_mod=angle_mod)

            plt.show(block=False)
        plot1_button.on_clicked(plot_1d)
        plot2_button.on_clicked(plot_2d)

    # last setups
    if use_3d:
        pass
    else:
        ax.set_aspect('equal', adjustable='datalim')
    #ax.legend()
    plt.show()
