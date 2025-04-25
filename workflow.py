import sys
import subprocess
import os
import shutil

def generate_input_file():
    """Generates the input file for CORSIKA simulation."""
    print("\nPlease fill in the following fields (use TAB to separate multiple options):\n")
    
    # Collect user parameters
    RUNNR = input("run number [DEFAULT: 1]: ") or "1"
    NSHOW = input("number of showers to generate [DEFAULT: 1]: ") or "1"
    PRMPAR = input("prim. particle (1=gamma, 14=proton, 5626=iron, ...) [DEFAULT: 14]: ") or "14"
    ESLOPE = input("slope of primary energy spectrum [DEFAULT: -2.7]: ") or "-2.7"
    ERANGE = input("energy range of primary particle (GeV) [DEFAULT: 1.E3   1.E3]: ") or "1.E3  1.E3"
    THETAP = input("range of zenith angle (degree) [DEFAULT: 0. 0.]: ") or "0.  0."
    PHIP = input("range of azimuth angle (degree) [DEFAULT: -180.   180.]: ") or "-180. 180."
    SEED1 = input("seed for 1. random number sequence [DEFAULT: 1   0   0]: ") or "1    0   0"
    SEED2 = input("seed for 2. random number sequence [DEFAULT: 2   0   0]: ") or "2    0   0"
    OBSLEV = input("observation level (in cm) [DEFAULT: 0.]: ") or "0."
    MAGNET = input("magnetic field centr. Europe [DEFAULT: 20.0 42.8]: ") or "20.0  42.8"
    HADFLG = input("flags hadr.interact.&fragmentation [DEFAULT: 0  0   0   0   0   2]: ") or "0    0   0   0   0   2"
    ECUTS = input("energy cuts for particles [DEFAULT: 1.   1.  0.001   0.001]: ") or "1.   1.  0.001   0.001"
    MUADDI = input("additional info for muons (T/F) [DEFAULT: T]: ") or "T"
    MUMULT = input("muon multiple scattering angle (T/F) [DEFAULT: T]: ") or "T"
    ELMFLG = input("em. interaction flags (NKG,EGS) [DEFAULT: T T]: ") or "T    T"
    STEPFC = input("mult. scattering step length fact [DEFAULT: 1.0]: ") or "1.0"
    RADNKG = input("outer radius for NKG lat.dens.distr. [DEFAULT: 200.E2]: ") or "200.E2"
    LONGI = input("longit.distr. & step size & fit & outfile [DEFAULT: T    10. T   T]: ") or "T    10. T   T"
    ECTMAP = input("cut on gamma factor for printout [DEFAULT: 1.E11]: ") or "1.E11"
    MAXPRT = input("max. number of printed events [DEFAULT: 1]: ") or "1"
    DEBUG = input("debug flag and log.unit for out [DEFAULT: F  6   F   1000000]: ") or "F  6   F   1000000"
    
    # Generate file content
    user_content = f"""RUNNR   {RUNNR} run number
NSHOW   {NSHOW} number of showers to generate
PRMPAR  {PRMPAR}    prim. particle (1=gamma, 14=proton, ...)
ESLOPE  {ESLOPE}    slope of primary energy spectrum
ERANGE  {ERANGE}    energy range of primary particle (GeV)
THETAP  {THETAP}    range of zenith angle (degree)
PHIP    {PHIP}  range of azimuth angle (degree)
SEED    {SEED1} seed for 1. random number sequence
SEED    {SEED2} seed for 2. random number sequence
*THIN   1.E2    1.E2 0. thinning definition
*THINH  10. 10. relative threshold and weight for hadron thinning
OBSLEV  {OBSLEV}    observation level (in cm)
MAGNET  {MAGNET}    magnetic field centr. Europe
HADFLG  {HADFLG}    flags hadr.interact.&fragmentation
ECUTS   {ECUTS} energy cuts for particles
MUADDI  {MUADDI}    additional info for muons
MUMULT  {MUMULT}    muon multiple scattering angle
ELMFLG  {ELMFLG}    em. interaction flags (NKG,EGS)
STEPFC  {STEPFC}    mult. scattering step length fact
RADNKG  {RADNKG}    outer radius for NKG lat.dens.distr.
PLOTSH  T
EPOPAR  input   ../epos/epos.param  !initialization input file for epos
EPOPAR  fname   pathnx  ../epos/    !initialization input file for epos
EPOPAR  fname   inics   ../epos/epos.inics  !initialization input file for epos
EPOPAR  fname   iniev   ../epos/epos.iniev  !initialization input file for epos
EPOPAR  fname   initl   ../epos/epos.initl  !initialization input file for epos
EPOPAR  fname   inirj   ../epos/epos.inirj  !initialization input file for epos
EPOPAR  fname   hpf ../epos/urqmd34/tables.dat
EPOPAR  fname   check   none    !dummy output file for epos
EPOPAR  fname   histo   none    !dummy output file for epos
EPOPAR  fname   data    none    !dummy output file for epos
EPOPAR  fname   copy    none    !dummy output file for epos
LONGI   {LONGI} longit.distr. & step size & fit & outfile
ECTMAP  {ECTMAP}    cut on gamma factor for printout
MAXPRT  {MAXPRT}    max. number of printed events
DIRECT  ./  output directory
USER    you user
*PAROUT F   F   suppress DAT file
DEBUG   {DEBUG} debug flag and log.unit for out
EXIT    terminates input
"""
    
    # Save the file
    with open("user_card", "w") as file:
        file.write(user_content)

def execute_command(command: str) -> str:
    """Executes a shell command and handles errors."""
    try:
        result = subprocess.run(command, shell=True, check=True, text=True, capture_output=True)
        return result.stdout
    except subprocess.CalledProcessError as e:
        print(f"Error executing command: {e}")
        print(f"Command output: {e.stdout}")
        print(f"Command error: {e.stderr}")
        sys.exit(1)

def plottracks(runnr):
    """Runs plottracks with interactive option selection."""
    run_number_str = f"{runnr:06d}"
    
    # Check required files first
    required_files = [
        f"DAT{run_number_str}.track_em",
        f"DAT{run_number_str}.track_mu", 
        f"DAT{run_number_str}.track_hd"
    ]
    
    missing_files = [f for f in required_files if not os.path.exists(f)]
    if missing_files:
        print(f"\nError: Track files not found: {', '.join(missing_files)}")
        return []

    # Ask for confirmation before proceeding with questions
    confirm = input("\nDo you want to run plottracks? (y/n) [DEFAULT: y]: ").lower() or "y"
    if confirm != 'y':
        print("Plottracks execution canceled by user.")
        return []

    # 1. Projection selection
    print("\n[1] Projection type:")
    print("  1 = x-z")
    print("  2 = y-z")
    print("  3 = x-y")
    while True:
        projection = input("  Choose (1-3) [DEFAULT: 1]: ") or "1"
        if projection in ['1', '2', '3']:
            break
        print("  Invalid option! Choose 1, 2 or 3.")

    # 2. View radius
    print("\n[2] View radius (in km):")
    while True:
        radius = input("  Enter value [DEFAULT: 5]: ") or "5"
        try:
            float(radius)
            break
        except ValueError:
            print("  Invalid value! Enter a number.")

    # 3. Background color
    print("\n[3] Background color:")
    print("  b = Black")
    print("  w = White")
    while True:
        background = input("  Choose (b/w) [DEFAULT: w]: ").lower() or "w"
        if background in ['b', 'w']:
            break
        print("  Invalid option! Choose 'b' or 'w'.")

    # 4. Energy cuts
    print("\n[4] Minimum energy cuts (in GeV):")
    print("  Format: em mu had [DEFAULT: 0 0 0]")
    while True:
        energy_cuts = input("  Enter cuts: ")
        if not energy_cuts:
            energy_cuts = "0 0 0"
            break
        
        parts = energy_cuts.split()
        if len(parts) == 3:
            try:
                [float(x) for x in parts]
                break
            except ValueError:
                print("  Invalid values! Use numbers (ex: '0.001 0.1 0.1')")
        else:
            print("  Incorrect format! Enter 3 values separated by spaces.")

    # Show summary and final confirmation
    print("\n" + "-"*60)
    print("Selected options summary:")
    print(f"  Projection: {'x-z' if projection == '1' else 'y-z' if projection == '2' else 'x-y'}")
    print(f"  Radius: {radius} km")
    print(f"  Background: {'Black' if background == 'b' else 'White'}")
    print(f"  Energy cuts: {energy_cuts}")
    print("-"*60)
    
    final_confirm = input("\nRun plottracks with these settings? (y/n) [DEFAULT: y]: ").lower() or "y"
    if final_confirm != 'y':
        print("Execution canceled by user.")
        return []

    # Build input sequence
    input_sequence = f"{projection}\n{radius}\n{background}\n{energy_cuts}\n{run_number_str}\n"

    # Execute plottracks
    try:
        print("\nRunning plottracks...")
        result = subprocess.run(
            f"echo '{input_sequence}' | ./plottracks",
            shell=True,
            check=True,
            text=True,
            capture_output=True,
            timeout=30
        )
        print(result.stdout)
    except subprocess.TimeoutExpired:
        print("  Warning: plottracks exceeded execution time limit")
        return []
    except subprocess.CalledProcessError as e:
        print(f"\nError executing plottracks (status {e.returncode}):")
        print(f"Output: {e.stdout}")
        print(f"Error: {e.stderr}")
        return []

    # Process outputs
    output_files = []
    for particle in ['em', 'mu', 'had', 'all']:
        ppm_file = f"track{run_number_str}.{particle}.ppm"
        png_file = ppm_file.replace('.ppm', '.png')
        
        if os.path.exists(ppm_file):
            try:
                if shutil.which('convert'):
                    subprocess.run(f"convert {ppm_file} {png_file}", shell=True, check=True)
                    output_files.append(png_file)
                    print(f"  Generated: {png_file}")
                else:
                    print("  Warning: ImageMagick not found, keeping .ppm file")
                    output_files.append(ppm_file)
            except subprocess.CalledProcessError:
                print(f"  Warning: Failed to convert {ppm_file} to PNG")
                output_files.append(ppm_file)
        else:
            print(f"  Warning: Output file {ppm_file} was not generated")

    return output_files

def tracks2root(runnr=1):
    """Converts binary track files to text."""
    run_number_str = f"{runnr:06d}"
    
    content = f"""import struct

files = [
    {{"input": "DAT{run_number_str}.track_mu", "output": "results_mu"}},
    {{"input": "DAT{run_number_str}.track_em", "output": "results_em"}},
    {{"input": "DAT{run_number_str}.track_hd", "output": "results_hd"}}
]

for file in files:
    datafile = file["input"]
    results = file["output"]

    with open(datafile, "rb") as infile, open(results, "w") as outfile:
        while True:
            buffer2 = infile.read(48)
            if not buffer2:
                break
            buffer = buffer2[4:44]
            properties = struct.unpack("10f", buffer)
            outfile.write(" ".join(map(str, properties)) + "\\n")
"""
    with open('tracks2root.py', 'w') as file:
        file.write(content)

def process_files(file_list: list):
    """Optimizes files for animation by removing invalid lines."""
    for file_name in file_list:
        with open(file_name, 'r') as file, open(f'ED{file_name}', 'w') as output_file:
            for line in file:
                line = line.strip()
                words = line.split(' ')
                if '' not in words and words[2] != words[6]:
                    output_file.write(' '.join(words) + '\n')

def blender_visu_script():
    """Generates Blender script for visualization."""
    content = """import bpy
import time
from math import cos
import os

file_names = ['EDresults_em_5k', 'EDresults_mu', 'EDresults_hd']
limit = -1

def make_curve(points, loop2):
    curveData = bpy.data.curves.new(f'myCurve{loop2}', type='CURVE')
    curveData.dimensions = '3D'
    curveData.resolution_u = 4
    polyline = curveData.splines.new('POLY')
    polyline.points.add(len(points)-1)
    for i, coord in enumerate(points):
        x, y, z = coord
        polyline.points[i].co = (x, y, z, 1)
    curveOB = bpy.data.objects.new(f'myCurve{loop2}', curveData)
    curveData.bevel_resolution = 6
    curveData.bevel_depth = 0.001667
    scn = bpy.context.scene
    scn.collection.objects.link(curveOB)
    bpy.ops.object.shade_smooth()
    
def remove_materials_objects():
    for material in bpy.data.materials:
        bpy.data.materials.remove(material)
    for object in bpy.data.objects:
        bpy.data.objects.remove(object)
    for curve in bpy.data.curves:
        bpy.data.curves.remove(curve)
        
def create_material(loop):
    bpy.data.materials.new(name='base'+f'{loop}')
    mat = bpy.data.materials[f'base{loop}']
    mat.use_nodes = True
    Princi = mat.node_tree.nodes['Principled BSDF']
    if loop == 0:
        Princi.inputs['Base Color'].default_value = (1.0, 0.028571, 0.021429, 0.4)
    elif loop == 1:
        Princi.inputs['Base Color'].default_value = (0.028571, 1, 0.021429, 0.4)
    elif loop == 2:
        Princi.inputs['Base Color'].default_value = (0.028571, 0.021429, 1, 0.4)
    else:
        Princi.inputs['Base Color'].default_value = (cos(loop*3.14), 1/cos(loop*3.14), cos(loop*3.14*2), 0.4)
    Princi.inputs['Roughness'].default_value = 0.445455
    Princi.inputs['Specular'].default_value = 0.08636365830898285
    
def insert_material(loop, loop2):
    mat = bpy.data.materials['base'+f'{loop}']
    curve = bpy.data.objects[f'myCurve{loop2}']
    curve.data.materials.append(mat)
    
def animate(t_i, t_f, loop2):
    if t_i > t_f:
        d = t_f
        t_f = t_i
        t_i = d
    scene = bpy.context.scene
    curve = bpy.data.curves[f'myCurve{loop2}']
    scene.frame_set(t_f)
    curve.keyframe_insert(data_path='bevel_factor_end')
    scene.frame_set(t_i)
    curve.bevel_factor_end = 0
    curve.keyframe_insert(data_path='bevel_factor_end')
    curve.animation_data.action.fcurves[0].keyframe_points[0].interpolation = 'LINEAR'
    curve.bevel_factor_mapping_end = 'SPLINE'
    
def process_curve_data(data):
    x = []
    y = []
    xend = []
    yend = []
    new_data = []
    for line in data:
        line = line.replace('\\n', '')
        l = line.split(' ')
        new_data.append(l)
        x.append(float(l[2])/1000000)
        xend.append(float(l[6])/1000000)
        y.append(float(l[3])/1000000)
        yend.append(float(l[7])/1000000)
    xif = inif(x, xend)
    yif = inif(y, yend)
    mesmax = mesmalinha(xif)
    mesmay = mesmalinha(yif)
    mesma = (mesmax, mesmay)
    all_curves_x = []
    all_curves_y = []
    for loop, data in enumerate(mesma):
        for line in data:
            indexes = []
            for j in range(0, len(line)):
                if loop == 0:
                    indexes.append(x.index(line[j][0]))
                else:
                    indexes.append(y.index(line[j][0]))
            data_to_save = []
            for g in range(0, len(line)):
                data_to_save.append(new_data[indexes[g]])
            if loop == 0:
                all_curves_x.append(data_to_save)
            else:
                all_curves_y.append(data_to_save)
    if len(all_curves_x) < len(all_curves_y):
        maior_curva = all_curves_y.copy()
        menor_curva = all_curves_x.copy()
    else:
        maior_curva = all_curves_x.copy()
        menor_curva = all_curves_y.copy()
    all_curves = []
    for data in maior_curva:
        if data in menor_curva:
            all_curves.append(data)
    return all_curves
    
def mesmalinha(initial_final):
    lines = []
    initials = [f[0] for f in initial_final]
    finals = [f[1] for f in initial_final]
    k = 0
    for i, f in initial_final:
        if f in initials and i not in finals:
            lines.append([[i, f]])
            continue
        count_bif = 0
        for curve in lines:
            for xi, xf in curve:
                if i == xi or i == xf:
                    count_bif += 1
                if count_bif > 1:
                    lines.append([[i, f]])
                    break
            if count_bif > 1:
                break
        if count_bif > 1:
            continue
        loop = 0
        for curve in lines:
            for xi, xf in curve:
                if i == xf:
                    lines[loop].append([i, f])
            loop += 1
    return lines
    
def inif(li, lf):
    tu = []
    for i in range(0, len(li)):
        tu.append([li[i], lf[i]])
    return tu
    
# Main execution
start_time = time.time()
remove_materials_objects()
loop2 = 0
last_frame = 0
for loop, file_name in enumerate(file_names):
    file_path = os.path.join('data', file_name)
    if not os.path.exists(file_path):
        print(f'File {file_path} not found. Skipping.')
        continue
    with open(file_path, 'r') as file:
        tabraw = file.readlines(limit)
    curve_data = process_curve_data(tabraw)
    create_material(loop)
    for curve in curve_data:
        loop2 += 1
        points = []
        for count, l in enumerate(curve):
            x = float(l[2])/1000000
            y = float(l[3])/1000000
            z = float(l[4])/1000000
            tini = float(l[5])*1000000
            xend = float(l[6])/1000000
            yend = float(l[7])/1000000
            zend = float(l[8])/1000000
            tend = float(l[9])*1000000
            points.append((x, y, z))
            if count == 0:
                initial_time = int(tini)
            final_time = int(tend)
            if initial_time == final_time:
                final_time = initial_time + 1
        make_curve(points, loop2)
        insert_material(loop, loop2)
        animate(initial_time, final_time, loop2)
        if final_time > last_frame:
            last_frame = final_time
            
# Configure camera and render settings
bpy.ops.object.light_add(type='SUN', align='WORLD', location=(0, -5.04, 4.6), rotation=(1.05418, 0, 0))
bpy.ops.object.camera_add(enter_editmode=False, align='VIEW', location=(0, -5.5, 1.5), rotation=(1.39626, 0, 0))
bpy.context.scene.camera = bpy.data.objects['Camera']
bpy.context.scene.render.resolution_x = 1080
bpy.context.scene.render.resolution_y = 1920
bpy.data.worlds['World'].node_tree.nodes['Background'].inputs[0].default_value = (0., 0., 0., 1)
bpy.context.scene.frame_end = last_frame + 10
bpy.context.scene.eevee.use_bloom = True
bpy.context.scene.eevee.use_gtao = True
bpy.context.scene.eevee.use_ssr = True
bpy.context.scene.eevee.use_motion_blur = True

# Save the Blender file
bpy.ops.wm.save_mainfile(filepath=os.path.join(os.getcwd(), 'output.blend'))
"""
    with open('blender_script.py', 'w') as file:
        file.write(content)

def main():
    print("Welcome to the workflow for atmospheric shower simulations!")
    
    generate_input_file()
    
    runnr = 1
    with open("user_card", "r") as f:
        for line in f:
            if line.startswith("RUNNR"):
                runnr = int(line.split()[1])
                break
    
    run_number_str = f"{runnr:06d}"
    
    execute_command("./corsika78010Linux_EPOS_urqmd < user_card")
    
    plot_files = []
    if os.path.exists("./plottracks"):
        plot_files = plottracks(runnr)
    else:
        print("\nWarning: plottracks executable not found. Skipping image generation.")
    
    generate_animation = input("\nDo you want to generate the animation? (y/n) [DEFAULT: y]: ").lower() or "y"
    
    execute_command(f"mkdir -p data_run_{run_number_str}")
    
    if generate_animation == 'y':
        # Processing data
        print("\nProcessing data...")
        tracks2root(runnr)
        execute_command("python3 tracks2root.py")
        process_files(['results_em', 'results_mu', 'results_hd'])
        execute_command("rm results_*")
        execute_command("head -n 5000 EDresults_em > EDresults_em_5k")
        execute_command("mkdir data")
        execute_command("mv EDresults* data/")
        # Generate Blender animation
        print("\nGenerating animation (it may take a while)...")
        blender_visu_script()
        execute_command("blender -b -P blender_script.py -E CYCLES -o img###.png -a")
        execute_command("cat *.png | ffmpeg -f image2pipe -r 30 -i - output.mp4 -y")
        execute_command("rm *.png output.blend")
        execute_command(f"mv DAT* track* user_card data/ output.mp4 blender_script.py data_run_{run_number_str}/")
    else:
        execute_command(f"mv DAT* track* user_card data_run_{run_number_str}/")
        print("\nSkipping animation generation.")
    
    # Final message
    print("\n" + "="*60)
    print("Process completed successfully!".center(60))
    print(f"\nAll generated files were moved to: data_run_{run_number_str}".center(60))
    print("="*60)

main()
