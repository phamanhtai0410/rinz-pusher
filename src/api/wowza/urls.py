# -*- coding: utf-8 -*-

# .....%%%%%!.....%%%!!........%%!.......%!.........
# .....%!........%!..........%....%!.....%!.........
# .....%%%%%!.....%%%!!.....%......%!....%!.........
# .....%!.............%!.....%....%!.....%!.........
# .....%%%%%!.....%%%!.........%%!.......%%%%%%!....

# Created by ESOL TECHNOLOGY SOLUTION JOINT STOCK COMPANY
# More information: https://esoltech.net
# ----****----****----****----****----****----***----

# File: urls.py	
# Created at 18/10/2021
"""
   Description: 
        -
        -
"""

from flask import Blueprint

from src.api.wowza.controller import on_event_controller

rest_wowza = Blueprint('rest_wowza', __name__, url_prefix='/wowza')

rest_wowza.add_url_rule('on_event', methods=['POST'], view_func=on_event_controller)
