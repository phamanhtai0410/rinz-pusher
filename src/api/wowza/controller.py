
# .....%%%%%!.....%%%!!........%%!.......%!.........
# .....%!........%!..........%....%!.....%!.........
# .....%%%%%!.....%%%!!.....%......%!....%!.........
# .....%!.............%!.....%....%!.....%!.........
# .....%%%%%!.....%%%!.........%%!.......%%%%%%!....

# Created by ESOL TECHNOLOGY SOLUTION JOINT STOCK COMPANY
# More information: https://esoltech.net
# ----****----****----****----****----****----***----

# File: controller.py	
# Created at 18/10/2021
"""
   Description: 
        -
        -
"""
from flask import request, g

from src.exceptions.handler import handle_exception
from src.utils.logger import Logger


@handle_exception()
def on_event_controller():
    Logger.debug(request.get_json())
    return {

    }
