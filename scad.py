import copy
import opsc
import oobb
import oobb_base
import yaml
import os
import scad_help

def main(**kwargs):
    make_scad(**kwargs)

def make_scad(**kwargs):
    parts = []

    typ = kwargs.get("typ", "")

    if typ == "":
        #setup    
        #typ = "all"
        typ = "fast"
        #typ = "manual"

    oomp_mode = "project"
    oomp_mode = "oobb"

    test = False
    #test = True

    if typ == "all":
        filter = ""; save_type = "all"; navigation = True; overwrite = True; modes = ["3dpr"]; oomp_run = False; test = False
        #default
        #filter = ""; save_type = "all"; navigation = True; overwrite = True; modes = ["3dpr"]; oomp_run = True; test = False
    elif typ == "fast":
        filter = ""; save_type = "none"; navigation = False; overwrite = True; modes = ["3dpr"]; oomp_run = False
        #default
        #filter = ""; save_type = "none"; navigation = False; overwrite = True; modes = ["3dpr"]; oomp_run = False
    elif typ == "manual":
    #filter
        filter = ""
        #filter = "test"

    #save_type
        save_type = "none"
        #save_type = "all"
        
    #navigation        
        #navigation = False
        navigation = True    

    #overwrite
        overwrite = True
                
    #modes
        #modes = ["3dpr", "laser", "true"]
        modes = ["3dpr"]
        #modes = ["laser"]    

    #oomp_run
        oomp_run = True
        #oomp_run = False    

    #adding to kwargs
    kwargs["filter"] = filter
    kwargs["save_type"] = save_type
    kwargs["navigation"] = navigation
    kwargs["overwrite"] = overwrite
    kwargs["modes"] = modes
    kwargs["oomp_mode"] = oomp_mode
    kwargs["oomp_run"] = oomp_run
    
       
    # project_variables
    if True:
        pass
    
    # declare parts
    if True:

        directory_name = os.path.dirname(__file__) 
        directory_name = directory_name.replace("/", "\\")
        project_name = directory_name.split("\\")[-1]
        #max 60 characters
        length_max = 40
        if len(project_name) > length_max:
            project_name = project_name[:length_max]
            #if ends with a _ remove it 
            if project_name[-1] == "_":
                project_name = project_name[:-1]
                
        #defaults
        kwargs["size"] = "oobb"
        kwargs["width"] = 1
        kwargs["height"] = 1
        kwargs["thickness"] = 3
        #oomp_bits
        if oomp_mode == "project":
            kwargs["oomp_classification"] = "project"
            kwargs["oomp_type"] = "github"
            kwargs["oomp_size"] = "oomlout"
            kwargs["oomp_color"] = project_name
            kwargs["oomp_description_main"] = ""
            kwargs["oomp_description_extra"] = ""
            kwargs["oomp_manufacturer"] = ""
            kwargs["oomp_part_number"] = ""
        elif oomp_mode == "oobb":
            kwargs["oomp_classification"] = "oobb"
            kwargs["oomp_type"] = "part"
            kwargs["oomp_size"] = ""
            kwargs["oomp_color"] = ""
            kwargs["oomp_description_main"] = ""
            kwargs["oomp_description_extra"] = ""
            kwargs["oomp_manufacturer"] = ""
            kwargs["oomp_part_number"] = ""

        part_default = {} 
       
        part_default["project_name"] = project_name
        part_default["full_shift"] = [0, 0, 0]
        part_default["full_rotations"] = [0, 0, 0]
        

        sizes = []
        sizes.append([5,5])
        sizes.append([5,10])
        sizes.append([5,12])

        thicknesses = []
        thicknesses.append(3)
        thicknesses.append(1.5)

        extras = []
        extras.append("")
        extras.append("packaging_label_76_2_mm_width_50_8_mm_length")

        for siz in sizes:
            for thick in thicknesses:
                for ex in extras:
                    wid = siz[0]
                    hei = siz[1]
                    part = copy.deepcopy(part_default)
                    p3 = copy.deepcopy(kwargs)
                    p3["width"] = wid
                    p3["height"] = hei
                    p3["thickness"] = thick
                    if ex != "":
                        p3["extra"] = ex
                    part["kwargs"] = p3
                    nam = "base"
                    part["name"] = "clothing_garment_rail_divider"
                    if oomp_mode == "oobb":
                        p3["oomp_size"] = nam
                    if not test:
                        pass
                        parts.append(part)


    kwargs["parts"] = parts

    scad_help.make_parts(**kwargs)

    #generate navigation
    if navigation:
        sort = []
        
        sort.append("name")
        sort.append("width")
        sort.append("height")
        sort.append("thickness")
        sort.append("extra")
        scad_help.generate_navigation(sort = sort)


def get_base(thing, **kwargs):

    prepare_print = kwargs.get("prepare_print", False)
    width = kwargs.get("width", 1)
    height = kwargs.get("height", 1)
    depth = kwargs.get("thickness", 3)                    
    rot = kwargs.get("rot", [0, 0, 0])
    pos = kwargs.get("pos", [0, 0, 0])
    extra = kwargs.get("extra", "")
    
    #add plate
    p3 = copy.deepcopy(kwargs)
    p3["type"] = "positive"
    p3["shape"] = f"oobb_plate"    
    p3["depth"] = depth
    #p3["holes"] = True         uncomment to include default holes
    #p3["m"] = "#"
    pos1 = copy.deepcopy(pos)         
    pos1[1] = -(height - 5) * 15/2
    p3["pos"] = pos1
    oobb_base.append_full(thing,**p3)
    
    #add holes seperate
    p3 = copy.deepcopy(kwargs)
    p3["type"] = "p"
    p3["shape"] = f"oobb_holes"
    p3["both_holes"] = True  
    p3["depth"] = depth
    pos11 = copy.deepcopy(pos1)
    if extra == "":
        p3["holes"] = ["right","corner","top","bottom"]
    elif extra == "packaging_label_76_2_mm_width_50_8_mm_length":
        p3["holes"] = ["top","bottom"]
        p3["height"] = height -1
        pos11[1] += - 15/2
    #p3["m"] = "#"
    

    p3["pos"] = pos11
    oobb_base.append_full(thing,**p3)

    #add rail cutout shape rounded_rectangle, radius 35/2 size wid,heigh,dept wid = 35 height = 117, position is x0 y-41
    if True:
        p3 = copy.deepcopy(kwargs)
        p3["type"] = "n"
        p3["shape"] = f"rounded_rectangle"
        p3["radius"] = 28/2
        wid = 28
        height = 163
        depth = depth
        size = [wid, height, depth]
        p3["size"] = size
        #p3["m"] = "#"
        pos1 = copy.deepcopy(pos)
        pos1[0] += 0
        pos1[1] += -67.5
        pos1[2] += 0
        p3["pos"] = pos1
        #p3["extra"] = extra
        oobb_base.append_full(thing,**p3)

    #add rail cylinder radius 33/2
    if True:
        p3 = copy.deepcopy(kwargs)
        p3["type"] = "n"
        p3["shape"] = f"oobb_cylinder"
        p3["radius"] = 33/2
        depth = depth
        p3["m"] = "#"
        pos1 = copy.deepcopy(pos)
        pos1[0] += 0
        pos1[1] += 0
        pos1[2] += 0
        p3["pos"] = pos1
        #p3["extra"] = extra
        oobb_base.append_full(thing,**p3)

    if extra == "packaging_label_76_2_mm_width_50_8_mm_length":
        #add label piece
        width_label  = 76.2
        height_label = 50.8

        #label holder big piece
        pos_holder = copy.deepcopy(pos)
        pos_holder[0] += 0
        pos_holder[1] += 50 - height_label/2
        pos_holder[2] += 0
        if True:
            extra_label_border = 3
            extra_label_clearance = 1
            depth_label_inset = 0.5   
            radius_label = 3/2
            p3 = copy.deepcopy(kwargs)
            p3["type"] = "positive"
            p3["shape"] = f"rounded_rectangle"
            wid = width_label + extra_label_border
            hei = height_label + extra_label_border
            dep = depth
            size = [wid, hei, dep]
            p3["size"] = size
            p3["radius"] = radius_label + extra_label_border/2
            p3["depth"] = dep
            p3["both_holes"] = True
            p3["holes"] = "left"
            #p3["m"] = "#"
            pos1 = copy.deepcopy(pos_holder)
            pos1[0] += 0
            pos1[1] += hei/2
            pos1[2] += 0
            p3["pos"] = pos1
            oobb_base.append_full(thing,**p3)

            #inset

            p4 = copy.deepcopy(p3)
            p4["type"] = "n"
            wid = width_label + extra_label_clearance
            hei = height_label + extra_label_clearance
            dep = depth_label_inset
            size = [wid, hei, dep]
            p4["size"] = size
            rad = radius_label + extra_label_clearance/2
            p4["radius"] = rad
            
            p4["both_holes"] = True
            p4["holes"] = "left"
            p4["m"] = "#"
            pos11 = copy.deepcopy(pos1)
            pos11[2] += 0#depth - depth_label_inset - dep/2
            p4["pos"] = pos11        
            oobb_base.append_full(thing,**p4)

    if prepare_print:
        #put into a rotation object
        components_second = copy.deepcopy(thing["components"])
        return_value_2 = {}
        return_value_2["type"]  = "rotation"
        return_value_2["typetype"]  = "p"
        pos1 = copy.deepcopy(pos)
        pos1[0] += 50
        return_value_2["pos"] = pos1
        return_value_2["rot"] = [180,0,0]
        return_value_2["objects"] = components_second
        
        thing["components"].append(return_value_2)

    
        #add slice # top
        p3 = copy.deepcopy(kwargs)
        p3["type"] = "n"
        p3["shape"] = f"oobb_slice"
        pos1 = copy.deepcopy(pos)
        pos1[0] += -500/2
        pos1[1] += 0
        pos1[2] += -500/2        
        p3["pos"] = pos1
        #p3["m"] = "#"
        oobb_base.append_full(thing,**p3)
    
if __name__ == '__main__':
    kwargs = {}
    main(**kwargs)