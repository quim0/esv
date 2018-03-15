SVG_HEADER = '''
<svg version="1.1"
     baseProfile="full"
     width="900" height="800"
     xmlns="http://www.w3.org/2000/svg">

  <rect width="100%" height="100%" fill="lightgrey" />
'''

SVG_FOOTER = '''
</svg>
'''

MEMORY_CELL_BASE_X = 50
MEMORY_CELL_BASE_Y = 100
MEMORY_CELL_STEP_Y = 50
SVG_MEMORY_CELL = '''
  <rect x="{x}" y="{y}" width="300" height="50" style="fill:blue;stroke:black;stroke-width:5;fill-opacity:0.1;" />
'''
SVG_MEMORY_TRANSPARENT_CELL = '''
  <rect x="{x}" y="{y}" width="300" height="50" style="fill-opacity:0;" />
'''
MEMORY_VALUE_BASE_X = 200
MEMORY_VALUE_BASE_Y = MEMORY_CELL_BASE_Y + 33
SVG_MEMORY_VALUE = '''
  <text x="{x}" y="{y}" font-size="24" text-anchor="middle" fill="black" font-family="monaco">{value}</text>
'''

REGISTER_ARROW_BASE_X = 340
REGISTER_ARROW_BASE_Y = 38 + 50
REGISTER_ARROW_SCALE = 4
SVG_REGISTER_ARROW = '''
  <path d="m 10,3 -5,5 5,5 z" fill="#797979" transform="translate({x}, {y}) scale({scale})"/>
'''
REGISTER_TEXT_BASE_X = 390
REGISTER_TEXT_BASE_Y = 80 + 50
SVG_REGISTER_TEXT = '''
  <text x="{x}" y="{y}" font-size="24" text-anchor="left" fill="black" font-family="monaco">{name}</text>
'''

CODE_BASE_X = 550
CODE_BASE_Y = 90 + 100
CODE_STEP_Y = 30
SVG_CODE_LINE = '''
  <text x="{x}" y="{y}" font-size="24" text-anchor="left" fill="black" font-family="monaco">{value}</text>
'''

PC_BASE_X = 500
PC_BASE_Y = 50 + 100
SVG_PC_REGISTER = '''
  <path d="m 6,3 5,5 -5,5 z" fill="#797979" transform="translate({x}, {y}) scale(4)" />
'''

class Image(object):
    def __init__(self):
        self._svg_str = SVG_HEADER
        self._cell_num = 0
        self._code_line_count = 0

        self.add_memory_cell('0x00000000_00000000', transparent=True)
        self.add_memory_cell('...', transparent=True)

    def add_memory_cell(self, value, transparent=False):
        cell = SVG_MEMORY_CELL
        if transparent:
            cell = SVG_MEMORY_TRANSPARENT_CELL
        self._svg_str += cell.format(x = MEMORY_CELL_BASE_X,
                                                y = self._cell_num * MEMORY_CELL_STEP_Y + MEMORY_CELL_BASE_Y)

        self._svg_str += SVG_MEMORY_VALUE.format(x = MEMORY_VALUE_BASE_X,
                                                 y = MEMORY_CELL_STEP_Y * self._cell_num + MEMORY_VALUE_BASE_Y,
                                                 value = value)
        self._cell_num += 1

    def add_register(self, cell_num, register_name):
        self._svg_str += SVG_REGISTER_ARROW.format(x = REGISTER_ARROW_BASE_X,
                                                   y = MEMORY_CELL_STEP_Y * cell_num + REGISTER_ARROW_BASE_Y,
                                                   scale = REGISTER_ARROW_SCALE)

        self._svg_str += SVG_REGISTER_TEXT.format(x = REGISTER_TEXT_BASE_X,
                                                  y = MEMORY_CELL_STEP_Y * cell_num + REGISTER_TEXT_BASE_Y,
                                                  name = register_name)

    def add_code_line(self, value):
        self._svg_str += SVG_CODE_LINE.format(x = CODE_BASE_X,
                                              y = CODE_STEP_Y * self._code_line_count + CODE_BASE_Y,
                                              value = value)

        self._code_line_count += 1

    def set_pc(self, line_num):
        self._svg_str += SVG_PC_REGISTER.format(x = PC_BASE_X,
                                                y = CODE_STEP_Y * line_num + PC_BASE_Y)

    def curr_memory_cell(self):
        return self._cell_num

    def curr_code_line(self):
        return self._code_line_count

    def save(self):
        self.add_memory_cell('...', transparent=True)
        self.add_memory_cell('0xffffffff_ffffffff', transparent=True)
        self._svg_str += SVG_FOOTER
        with open('fig.svg', 'w') as f:
            f.write(self._svg_str)
        # Reset svg
        self._svg_str = SVG_HEADER
