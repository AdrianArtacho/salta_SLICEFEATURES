# import feat_relnorm
import pyt.paths.create_folder as create_folder
import gui.gui_enterstring as gui_enterstring
import pyt.paths.copy_file as copy_file
import pyt.paths.delete_file as delete_file
import pyt.paths.filesinfolder as filesinfolder

def main(folder_to_copyover, local_folder='OUTPUT',
         destination_folder = '../tmm2python/TMMMatlabCode/MotionSegmentation/INPUT',
         verbose=True):
    
    file_list = filesinfolder.main(local_folder+'/'+folder_to_copyover)

    if verbose:
        print("folder_to_copyover:", folder_to_copyover)
        print("file_list:", file_list)
    
    # exit()
    new_folder_name = gui_enterstring.main("Enter the name for the set", "Enter set name:", "sliced features", 
         font = ("Arial", 16), default_text=folder_to_copyover, 
         verbose=False)

    if verbose:
        print("new_folder_name:", new_folder_name)

    create_folder.main(new_folder_name, local_folder=destination_folder)

    for file in file_list:
        filepath = local_folder+'/'+folder_to_copyover+'/'+file
        print("filepath:", filepath)
        print("destination_folder:", destination_folder)
        print("new_folder_name:", new_folder_name)

        copy_file.main(filepath, destination_folder, new_folder_name)
    
if __name__ == '__main__':
    folder_to_copyover = 'exp16a_inert-left'
    main(folder_to_copyover)