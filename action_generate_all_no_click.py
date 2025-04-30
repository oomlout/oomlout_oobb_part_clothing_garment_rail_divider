import copy
import os
import sys
import subprocess

def main(**kwargs):
    
    #run scad
    if True:
        import scad
        kwargs2 = copy.deepcopy(kwargs)
        kwargs2["typ"] = "all"
        scad.main(**kwargs2)
    

    
    

    #run action_generate_all_no_click
    if True:        
        import action_generate_resolutions_overwrite
        action_generate_resolutions_overwrite.main(**kwargs)
        import action_generate_readme_outputs_overwrite
        action_generate_readme_outputs_overwrite.main(**kwargs)



    #push to git
    if True:
        directory_current = os.getcwd()
        git_command = f'cd {directory_current}&git add *&git commit -m "auto commit"&git push'
        print(f"git_command: {git_command}")
        os.system(git_command) #


        

if __name__ == '__main__':
    kwargs = {}
    main(**kwargs)