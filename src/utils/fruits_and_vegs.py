with open("Vegetables_list.txt","r") as origvegfile:
    with open("formatted_veg_list.txt","w") as vegfile:
        for line in origvegfile:
            changedline = line.replace("<li>","")
            changedline = changedline.replace("</li>","")
            vegfile.write(changedline)
            
