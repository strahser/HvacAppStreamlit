import enum
from collections import namedtuple

SQL_EXAMPLE1 = """
			https://habr.com/ru/post/255825/   
			/*SELECT all tables names*/ 
			SELECT name FROM sqlite_master WHERE type='table'  
			SELECT all columns names  
			SELECT c.name FROM pragma_table_info('revit_export') c;  
			GROUP BY
			SELECT space_category,S_sup_name, sum(S_height*S_area) as "air" from  revit_export   
			GROUP BY space_category   

"""
SQL_EXAMPLE2 = """
			SELECT input. * , category.group_human_work, human_heat_base.human_heat,   
			round(input.S_area/ category.area_for_person) as human_number,   
			CASE    
			WHEN input.h_n  >0 THEN input.h_n* human_heat   
			ELSE input.S_area/ category.area_for_person * human_heat    
			END 'human heat sum',   
			count(*) as Total_rooms, sum(S_area) as Total_Area from input    
			JOIN category ON input.space_category = category.space_category   
			JOIN human_heat_base ON category.group_human_work=human_heat_base.group_human_work   
			GROUP BY S_level   
			HAVING  S_Number in (1,2,3,4)
"""
EXAMPLE_LIST = (SQL_EXAMPLE1, SQL_EXAMPLE2)


class SqlExample(enum.Enum):
	simple_example ="Simple Example", SQL_EXAMPLE1
	complex_example = "Complex Example", SQL_EXAMPLE2
