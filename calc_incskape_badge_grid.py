#!/usr/bin/env python


empty_page="""<?xml version="1.0" encoding="UTF-8" standalone="no"?>
<!-- Created with Inkscape (http://www.inkscape.org/) -->

<svg
   width="210mm"
   height="297mm"
   viewBox="0 0 210 297"
   version="1.1"
   id="svg5"
   inkscape:version="1.2.2 (1:1.2.2+202212051552+b0a8486541)"
   sodipodi:docname="Zeichnung.svg"
   xmlns:inkscape="http://www.inkscape.org/namespaces/inkscape"
   xmlns:sodipodi="http://sodipodi.sourceforge.net/DTD/sodipodi-0.dtd"
   xmlns="http://www.w3.org/2000/svg"
   xmlns:svg="http://www.w3.org/2000/svg">
  <sodipodi:namedview
     id="namedview7"
     pagecolor="#ffffff"
     bordercolor="#000000"
     borderopacity="0.25"
     inkscape:showpageshadow="2"
     inkscape:pageopacity="0.0"
     inkscape:pagecheckerboard="0"
     inkscape:deskcolor="#d1d1d1"
     inkscape:document-units="mm"
     showgrid="false"
     inkscape:zoom="0.99475561"
     inkscape:cx="429.25116"
     inkscape:cy="571.49715"
     inkscape:window-width="2560"
     inkscape:window-height="1489"
     inkscape:window-x="0"
     inkscape:window-y="0"
     inkscape:window-maximized="1"
     inkscape:current-layer="layer1" />
  <defs
     id="defs2" />
  <g
     inkscape:label="Ebene 1"
     inkscape:groupmode="layer"
     id="layer1" />
</svg>
"""


class calc_incskape_badge_grid():
    def __init__(self, badge_width=87, 
                 bagde_height=54, 
                 tamplate_file_name="Template.svg"):
        self.badge_width = badge_width
        self.bagde_height = bagde_height
        self.tamplate_file_name = tamplate_file_name

        # A4
        self.paper_width = 210
        self.paper_height = 297



    def calc_xy_array_pos(self):
        self.pos_x_array = [] # vertical lines
        for i in range(self.count_with+1):
            pos_x = self.offset_width + i*self.badge_width
            self.pos_x_array.append(pos_x)
            # print(pos_x)
        self.pos_y_array = [] # horrizontal lines
        for i in range(self.count_height+1):
            pos_y = self.offset_heigth + i*self.bagde_height
            self.pos_y_array.append(pos_y)
            # print(pos_y)
        return self.pos_x_array, self.pos_y_array

    def get_auxiliary_line_horrizontal(self, pos_x, pos_y, guide):
        auxiliary_line_horrizontal = (f'    <sodipodi:guide\n'
                                f'       position="{pos_x},{pos_y}"\n'
                                f'       orientation="0,-1"\n'
                                f'       id="guide{guide}" />\n')
        return auxiliary_line_horrizontal
    
    def get_auxiliary_line_vertical(self, pos_x, pos_y, guide):
        auxiliary_line_vertical = (f'    <sodipodi:guide\n'
                           f'       position="{pos_x},{pos_y}"\n'
                           f'       orientation="1,0"\n'
                           f'       id="guide{guide}" />\n')
        return auxiliary_line_vertical

    def get_cutting_line_horrizontal(self, pos_y, abst_x, first_vert, last_vert, pathID):
        # print(first_vert, last_vert)
        # print(last_vert - abst_x)
        # print(paper_width - abst_x)
        cutting_line_horrizontal = (f'    <path\n'
           f'       style="fill:none;stroke:#000000;stroke-width:0.264583px;stroke-linecap:butt;stroke-linejoin:miter;stroke-opacity:1"\n'
           f'       d="M {abst_x},{pos_y} H {first_vert - abst_x}"\n'
           f'       id="path{pathID}" />\n')
        cutting_line_horrizontal = cutting_line_horrizontal + (f'    <path\n'
           f'       style="fill:none;stroke:#000000;stroke-width:0.264583px;stroke-linecap:butt;stroke-linejoin:miter;stroke-opacity:1"\n'
           f'       d="M {last_vert  + abst_x},{pos_y} H {self.paper_width -  abst_x}"\n'
           f'       id="path{pathID + 1}" />\n')
        return cutting_line_horrizontal
    
    def get_cutting_line_vertical(self, pos_x, abst_y, first_horr, last_horr, pathID):
        # print(first_horr, last_horr)
        # print(last_horr - abst_y)
        # print(paper_height + abst_y)
        cutting_line_vertical = (f'    <path\n'
                       f'       style="fill:none;stroke:#000000;stroke-width:0.264583px;stroke-linecap:butt;stroke-linejoin:miter;stroke-opacity:1"\n'
                       f'       d="M {pos_x},{abst_y} V {first_horr - abst_y}"\n'
                       f'       id="path{pathID}" />\n')
        cutting_line_vertical = cutting_line_vertical + (f'    <path\n'
                       f'       style="fill:none;stroke:#000000;stroke-width:0.264583px;stroke-linecap:butt;stroke-linejoin:miter;stroke-opacity:1"\n'
                       f'       d="M  {pos_x},{last_horr + abst_y } V {self.paper_height - abst_y}"\n'
                       f'       id="path{pathID+1}" />\n')
        return cutting_line_vertical

    def create_auxiliary_lines(self):
        auxiliary_lines = ''
        guide=10
        guide_count = 0
        for pos_x in self.pos_x_array:
            auxiliary_lines = auxiliary_lines + self.get_auxiliary_line_vertical(pos_x, 0.0, guide)
            guide += 10
            guide_count +=1
        
        for pos_y in self.pos_y_array:
            auxiliary_lines = auxiliary_lines + self.get_auxiliary_line_horrizontal(0.0,pos_y, guide)
            guide += 10
            guide_count +=1
        auxiliary_lines = auxiliary_lines + "       </sodipodi:namedview>\n"
        # print(auxiliary_lines)
        return auxiliary_lines

    def create_cutting_lines(self):
        cutting_lines=""
        path_count = 0
        path = 10
        abst_y = 2.0
        abst_x=2.0
        for pos_x in self.pos_x_array:
            cutting_lines = cutting_lines +  self.get_cutting_line_vertical(pos_x, abst_y, self.pos_y_array[0], self.pos_y_array[-1], path)
            path += 10
            path_count +=1
        
        for pos_y in self.pos_y_array:
            cutting_lines = cutting_lines + self.get_cutting_line_horrizontal(pos_y, abst_x, self.pos_x_array[0], self.pos_x_array[-1], path)
            path += 10
            path_count +=1
        # print(cutting_lines)
        return cutting_lines

    def get_start_end_auxiliary_line_index(self, data):
        start_line = "<sodipodi:namedview"
        # end_line = "</sodipodi:namedview>"
        start_index = None
        end_index = None
        start_found = False
        for i, line in enumerate(data):
            if start_line in line:
                start_index = i
                # print(i, data[i])
                start_found = True
            
            # if end_line in line:
            #     # print(i, data[i])
            #     end_index = i
            #     break
        
        if end_index == None:
            for i in range(start_index, len(data)):
                # print(i, data[i])
                if "/>" in data[i]:
                    # print(i, data[i])
                    end_index = i
                    data[i] = data[i].replace("/>", ">")
                    break
        return start_index, end_index

    def get_start_end_cutting_line_index(self, data):
        start_line = "<g"
        start_index = None
        end_index = None
        start_found = False
        for i, line in enumerate(data):
            # print(i, line)
            if start_line in line:
                start_index = i
                # print(i, data[i])
                start_found = True
                break
                
        if end_index == None:
            for i in range(start_index, len(data)):
                # print(i, data[i])
                if "/>" in data[i]:
                    # print(i, data[i])
                    end_index = i
                    # data[i] = data[i].replace("/>", ">")
                    break
                    
        return start_index, end_index

    def write_svg_data(self, file_name=None):
        if file_name is None:
            file_name = self.new_tamplate_file_name
        print(f"Write new data to: {file_name}")
        with open(file_name, 'w') as f:
            for line in self.data:
                f.write(f"{line}\n")

    def main(self):
        # print(self.paper_width / self.badge_width)
        self.count_with = int(self.paper_width / self.badge_width)
        # self.count_with
        # print(self.paper_height / self.bagde_height)
        self.count_height = int(self.paper_height / self.bagde_height)
        # self.count_height

        self.offset_width = (self.paper_width - self.count_with*self.badge_width)/2
        # self.offset_width
        
        self.offset_heigth = (self.paper_height - self.count_height*self.bagde_height)/2
        # self.offset_heigth

        self.calc_xy_array_pos()
        # print(self.pos_x_array, self.pos_y_array)

        auxiliary_lines_string = self.create_auxiliary_lines()
        # print(auxiliary_lines_string)

        cutting_lines_string = self.create_cutting_lines()
        # print(cutting_lines_string)


        # #################################
        # # # Use EmptyPage instead of file
        self.data = empty_page.split("\n")
        # ##################################
        for i, d in enumerate(self.data):
            # print(i, d.strip())
            self.data[i] = d.replace("\n", "")
            # print(i, data[i])

        start_index, end_index = self.get_start_end_auxiliary_line_index(self.data)

        # nur Hilfslinien einfügen in leeres "EmptyPage"
        for i, element in enumerate(auxiliary_lines_string.split("\n")):
            # print(i+end_index+1, element)
            self.data.insert(i+end_index+1, element)

        start_index, end_index = self.get_start_end_cutting_line_index(self.data)

        # nur schnittmarken einfügen in leeres "EmptyPage"
        for i, element in enumerate(cutting_lines_string.split("\n")):
            # print(i+end_index+1, element)
            self.data.insert(i+end_index+1, element)
        # self.data

        self.new_tamplate_file_name=self.tamplate_file_name.replace(".svg", f"_({self.badge_width}-{self.bagde_height}).svg")
        print(f"Target filename: '{self.new_tamplate_file_name}'")


