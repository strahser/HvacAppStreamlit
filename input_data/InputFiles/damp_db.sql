BEGIN TRANSACTION;
CREATE TABLE "air_loc_ex" (
"S_ID" INTEGER,
  "loc_ex_air" INTEGER
);
INSERT INTO "air_loc_ex" VALUES(837893,4000);
INSERT INTO "air_loc_ex" VALUES(837895,2000);
INSERT INTO "air_loc_ex" VALUES(837896,1000);
CREATE TABLE "category" (
"space_category" TEXT,
  "lighting" INTEGER,
  "group_human_work" TEXT,
  "area_for_person" REAL,
  "min_temp" INTEGER,
  "max_temp" INTEGER,
  "phi_min" INTEGER,
  "phi_max" INTEGER,
  "Sup_air_mult" INTEGER,
  "Ex_air_mult" INTEGER,
  "sup_air_human" INTEGER,
  "equipment" TEXT,
  "fresh_air" REAL
);
INSERT INTO "category" VALUES('office',20,'light',7.0,18,25,40,60,2,2,60,'computer',0.8);
INSERT INTO "category" VALUES('medicine',35,'medium',10.0,20,23,45,46,5,5,60,NULL,0.75);
INSERT INTO "category" VALUES('live_category',50,NULL,NULL,20,23,30,60,5,5,60,NULL,1.0);
CREATE TABLE "category_load" (
"space_category" TEXT,
  "heat_load" INTEGER
);
INSERT INTO "category_load" VALUES('live_category',5000);
CREATE TABLE "climate_data" (
"climate_label" TEXT,
  "climate_data" INTEGER
);
INSERT INTO "climate_data" VALUES('t_нар_зим',-20);
CREATE TABLE "column_names" (
"Old_name" TEXT,
  "New_name" TEXT,
  "definition" TEXT
);
INSERT INTO "column_names" VALUES('S_ID','S_ID','space id');
INSERT INTO "column_names" VALUES('S_Number','Номер пом.','room number');
INSERT INTO "column_names" VALUES('S_Name','Наим. пом.','room name');
INSERT INTO "column_names" VALUES('S_height','Высота пом.','room heght');
INSERT INTO "column_names" VALUES('Area','Площадь пом.','room area');
INSERT INTO "column_names" VALUES('S_Volume','Объем пом.','room volume');
INSERT INTO "column_names" VALUES('level','Этаж','room level');
INSERT INTO "column_names" VALUES('S_SA_Load_human','Прит. возд. Люди','supply requiement air fo human');
INSERT INTO "column_names" VALUES('S_EA_Load_human','Выт.возд.Люди','exaust requiement air fo human');
INSERT INTO "column_names" VALUES('fresh_air','Свежий возд','fresh supply air ');
INSERT INTO "column_names" VALUES('S_SA_Load_mult','Прит.возд.крат.',NULL);
INSERT INTO "column_names" VALUES('S_EA_Load_mult','Выт.возд.крат.',NULL);
INSERT INTO "column_names" VALUES('S_SA_max','Прит. возд.расчетный',NULL);
INSERT INTO "column_names" VALUES('S_EA_max','Выт. возд.расчетный',NULL);
INSERT INTO "column_names" VALUES('S_SA_fresh','Прит. возд.свеж',NULL);
INSERT INTO "column_names" VALUES('S_SA_recirc','Выт. возд.циркул',NULL);
INSERT INTO "column_names" VALUES('space_category','Категория пом.',NULL);
INSERT INTO "column_names" VALUES('group_human_work','Группа работ',NULL);
INSERT INTO "column_names" VALUES('area_for_person','Пл.на человека',NULL);
INSERT INTO "column_names" VALUES('sup_air_human','SAH',NULL);
INSERT INTO "column_names" VALUES('h_num_cal','h_num',NULL);
INSERT INTO "column_names" VALUES('Sup_air_exc','SAEX',NULL);
INSERT INTO "column_names" VALUES('Ex_air_exc','EAEX',NULL);
INSERT INTO "column_names" VALUES('h_heat_sum','h_h_sum',NULL);
INSERT INTO "column_names" VALUES('electrical_load_sum','el_sum',NULL);
INSERT INTO "column_names" VALUES('lighting_heat_sum','lig_sum',NULL);
INSERT INTO "column_names" VALUES('radiation_load','radiat_load',NULL);
INSERT INTO "column_names" VALUES('equip_heat_load','eq_load',NULL);
INSERT INTO "column_names" VALUES('heat_loss','heat_loss',NULL);
INSERT INTO "column_names" VALUES('S_Cold_Load','S_Cold',NULL);
INSERT INTO "column_names" VALUES('S_Heat_loss','S_Heat_loss',NULL);
INSERT INTO "column_names" VALUES('equip_heat','eq_h',NULL);
INSERT INTO "column_names" VALUES('eq_id','eq__id',NULL);
INSERT INTO "column_names" VALUES('unit_power,kW','un_pow',NULL);
INSERT INTO "column_names" VALUES('quat','quat',NULL);
INSERT INTO "column_names" VALUES('k_ur','k_u_ur',NULL);
INSERT INTO "column_names" VALUES('k_lr','k_l_lr',NULL);
INSERT INTO "column_names" VALUES('k_sr','k_s_sr',NULL);
INSERT INTO "column_names" VALUES('k_mt','k_m_mt',NULL);
INSERT INTO "column_names" VALUES('n','n',NULL);
INSERT INTO "column_names" VALUES('electrical_load','el_load',NULL);
INSERT INTO "column_names" VALUES('human_heat','h_heat',NULL);
INSERT INTO "column_names" VALUES('lighting','l_norm',NULL);
INSERT INTO "column_names" VALUES('id','id',NULL);
INSERT INTO "column_names" VALUES('name','surfece',NULL);
INSERT INTO "column_names" VALUES('area','area',NULL);
INSERT INTO "column_names" VALUES('orientation','orient',NULL);
INSERT INTO "column_names" VALUES('heat_load, w/m2','heat_load',NULL);
INSERT INTO "column_names" VALUES('k-ef','k-e_ef',NULL);
INSERT INTO "column_names" VALUES('dt_C','dt',NULL);
INSERT INTO "column_names" VALUES('k-orientation','k-orient',NULL);
INSERT INTO "column_names" VALUES('min_temp','min_t',NULL);
INSERT INTO "column_names" VALUES('max_temp','max_t',NULL);
CREATE TABLE "config" (
"system_type" TEXT,
  "system_flow" TEXT,
  "system_name" TEXT
);
INSERT INTO "config" VALUES('Supply_system','S_SA_max','S_sup_name');
INSERT INTO "config" VALUES('Exhaust_system','S_EA_max','E_ex_name');
INSERT INTO "config" VALUES('Fan_coil_system','S_Cold_Load','S_coold_name');
CREATE TABLE "device_orientation" (
"orientation" TEXT,
  "single_orientation" TEXT
);
INSERT INTO "device_orientation" VALUES('up','corner');
INSERT INTO "device_orientation" VALUES('down','center');
INSERT INTO "device_orientation" VALUES('left',NULL);
INSERT INTO "device_orientation" VALUES('right',NULL);
INSERT INTO "device_orientation" VALUES('center_horizontal',NULL);
INSERT INTO "device_orientation" VALUES('center_vertical',NULL);
CREATE TABLE "device_type" (
"type_index" TEXT,
  "family_device_name" TEXT,
  "device_orientation_option1" TEXT,
  "device_orientation_option2" TEXT,
  "single_device_orientation" TEXT,
  "wall_offset" INTEGER,
  "ceiling_offset" INTEGER,
  "calculation_options" REAL,
  "device_area" REAL,
  "directive_terminals" REAL,
  "directive_length" REAL
);
INSERT INTO "device_type" VALUES('supply_round_area_20_d_l_c','ADSK_Диффузор_Круглый_Приточный','down','left','corner',500,500,NULL,20.0,NULL,NULL);
INSERT INTO "device_type" VALUES('s_s_m','ADSK_Диффузор_Прямоугольный_Приточный','down','left','corner',500,500,NULL,NULL,NULL,NULL);
INSERT INTO "device_type" VALUES('e_r_m','ADSK_Диффузор_Круглый_Вытяжной','up','right','corner',500,500,NULL,NULL,NULL,NULL);
INSERT INTO "device_type" VALUES('e_s_m','ADSK_Диффузор_Прямоугольный_Вытяжной','up','right','corner',500,500,NULL,NULL,NULL,NULL);
INSERT INTO "device_type" VALUES('f_42Gwc_m','42GWC Carrier_univ','center_vertical','center_horizontal','center',500,500,NULL,NULL,NULL,NULL);
CREATE TABLE "devices" (
"S_ID" INTEGER,
  "S_Number" INTEGER,
  "S_Name" TEXT,
  "Supply_system" TEXT,
  "Exhaust_system" TEXT,
  "Fan_coil_system" TEXT
);
INSERT INTO "devices" VALUES(837890,1,'Помещение',NULL,NULL,NULL);
INSERT INTO "devices" VALUES(837891,2,'Помещение','s_s_m','e_r_m','f_42Gwc_m');
INSERT INTO "devices" VALUES(837892,3,'Помещение','s_s_m','e_r_m','f_42Gwc_m');
INSERT INTO "devices" VALUES(837893,4,'Помещение','s_s_m','e_r_m','f_42Gwc_m');
INSERT INTO "devices" VALUES(837894,5,'Помещение','s_s_m','e_r_m','f_42Gwc_m');
INSERT INTO "devices" VALUES(837895,6,'Помещение','s_s_m','e_r_m','f_42Gwc_m');
INSERT INTO "devices" VALUES(837896,7,'Помещение','s_s_m','e_s_m','f_42Gwc_m');
INSERT INTO "devices" VALUES(837897,8,'Помещение','s_s_m','e_r_m','f_42Gwc_m');
INSERT INTO "devices" VALUES(837898,9,'Помещение','s_s_m','e_r_m','f_42Gwc_m');
INSERT INTO "devices" VALUES(837899,11,'Помещение','s_s_m','e_r_m','f_42Gwc_m');
INSERT INTO "devices" VALUES(837900,12,'Помещение','s_s_m','e_r_m','f_42Gwc_m');
INSERT INTO "devices" VALUES(837901,13,'Помещение','s_s_m','e_r_m','f_42Gwc_m');
INSERT INTO "devices" VALUES(837902,14,'Помещение','s_s_m','e_r_m','f_42Gwc_m');
INSERT INTO "devices" VALUES(837903,15,'Помещение','s_s_m','e_r_m','f_42Gwc_m');
INSERT INTO "devices" VALUES(837904,16,'Помещение','s_s_m','e_r_m','f_42Gwc_m');
INSERT INTO "devices" VALUES(837905,17,'Помещение','s_s_m','e_r_m','f_42Gwc_m');
INSERT INTO "devices" VALUES(837906,19,'Помещение','s_s_m','e_r_m','f_42Gwc_m');
INSERT INTO "devices" VALUES(837907,20,'Помещение','s_s_m','e_r_m','f_42Gwc_m');
INSERT INTO "devices" VALUES(837908,21,'Помещение','s_s_m','e_r_m','f_42Gwc_m');
INSERT INTO "devices" VALUES(837909,22,'Помещение','s_s_m','e_r_m','f_42Gwc_m');
INSERT INTO "devices" VALUES(837910,23,'Помещение','s_s_m','e_r_m','f_42Gwc_m');
INSERT INTO "devices" VALUES(837911,24,'Помещение','s_s_m','e_r_m','f_42Gwc_m');
INSERT INTO "devices" VALUES(837912,25,'Помещение','s_s_m','e_r_m','f_42Gwc_m');
INSERT INTO "devices" VALUES(837913,26,'Помещение','s_s_m','e_r_m','f_42Gwc_m');
INSERT INTO "devices" VALUES(837914,27,'Помещение','s_s_m','e_r_m','f_42Gwc_m');
INSERT INTO "devices" VALUES(837915,28,'Помещение','s_s_m','e_r_m','f_42Gwc_m');
INSERT INTO "devices" VALUES(837916,30,'Помещение','s_s_m','e_r_m','f_42Gwc_m');
INSERT INTO "devices" VALUES(837917,31,'Помещение',NULL,'e_r_m','f_42Gwc_m');
INSERT INTO "devices" VALUES(837918,32,'Помещение','supply_round_area_20_d_l_c','e_r_m','f_42Gwc_m');
INSERT INTO "devices" VALUES(837919,33,'Помещение','supply_round_area_20_d_l_c','e_r_m','f_42Gwc_m');
INSERT INTO "devices" VALUES(837920,45,'Помещение','supply_round_area_20_d_l_c','e_r_m','f_42Gwc_m');
INSERT INTO "devices" VALUES(837921,46,'Помещение','supply_round_area_20_d_l_c','e_r_m','f_42Gwc_m');
INSERT INTO "devices" VALUES(837922,47,'Помещение','supply_round_area_20_d_l_c','e_r_m','f_42Gwc_m');
INSERT INTO "devices" VALUES(837923,48,'Помещение','supply_round_area_20_d_l_c','e_r_m','f_42Gwc_m');
INSERT INTO "devices" VALUES(837924,49,'Помещение','supply_round_area_20_d_l_c','e_r_m','f_42Gwc_m');
INSERT INTO "devices" VALUES(837925,50,'Помещение','supply_round_area_20_d_l_c','e_r_m','f_42Gwc_m');
INSERT INTO "devices" VALUES(837926,51,'Помещение','supply_round_area_20_d_l_c','e_r_m','f_42Gwc_m');
INSERT INTO "devices" VALUES(837927,52,'Помещение','supply_round_area_20_d_l_c','e_r_m','f_42Gwc_m');
INSERT INTO "devices" VALUES(837928,53,'Помещение','supply_round_area_20_d_l_c','e_r_m','f_42Gwc_m');
INSERT INTO "devices" VALUES(837929,54,'Помещение','supply_round_area_20_d_l_c','e_r_m','f_42Gwc_m');
INSERT INTO "devices" VALUES(928204,55,'Помещение','supply_round_area_20_d_l_c','e_r_m','f_42Gwc_m');
INSERT INTO "devices" VALUES(928205,56,'Помещение','supply_round_area_20_d_l_c','e_r_m','f_42Gwc_m');
INSERT INTO "devices" VALUES(928206,57,'Помещение','supply_round_area_20_d_l_c','e_r_m','f_42Gwc_m');
INSERT INTO "devices" VALUES(928207,58,'Помещение','supply_round_area_20_d_l_c','e_r_m','f_42Gwc_m');
INSERT INTO "devices" VALUES(928208,59,'Помещение','supply_round_area_20_d_l_c','e_r_m','f_42Gwc_m');
INSERT INTO "devices" VALUES(928209,60,'Помещение','supply_round_area_20_d_l_c','e_r_m','f_42Gwc_m');
INSERT INTO "devices" VALUES(928210,61,'Помещение','supply_round_area_20_d_l_c','e_r_m','f_42Gwc_m');
INSERT INTO "devices" VALUES(928211,62,'Помещение','supply_round_area_20_d_l_c','e_r_m','f_42Gwc_m');
CREATE TABLE "ducts_round" (
"diameter" INTEGER,
  "wall thickness" REAL
);
INSERT INTO "ducts_round" VALUES(100,0.5);
INSERT INTO "ducts_round" VALUES(125,0.5);
INSERT INTO "ducts_round" VALUES(140,0.5);
INSERT INTO "ducts_round" VALUES(160,0.5);
INSERT INTO "ducts_round" VALUES(180,0.5);
INSERT INTO "ducts_round" VALUES(200,0.5);
INSERT INTO "ducts_round" VALUES(225,0.5);
INSERT INTO "ducts_round" VALUES(250,0.5);
INSERT INTO "ducts_round" VALUES(280,0.5);
INSERT INTO "ducts_round" VALUES(325,0.5);
INSERT INTO "ducts_round" VALUES(355,0.5);
INSERT INTO "ducts_round" VALUES(400,0.5);
INSERT INTO "ducts_round" VALUES(450,0.7);
INSERT INTO "ducts_round" VALUES(500,0.7);
INSERT INTO "ducts_round" VALUES(560,0.7);
INSERT INTO "ducts_round" VALUES(630,0.7);
INSERT INTO "ducts_round" VALUES(710,0.7);
INSERT INTO "ducts_round" VALUES(800,0.7);
INSERT INTO "ducts_round" VALUES(900,0.9);
INSERT INTO "ducts_round" VALUES(1000,0.9);
INSERT INTO "ducts_round" VALUES(1120,0.9);
INSERT INTO "ducts_round" VALUES(1250,0.9);
INSERT INTO "ducts_round" VALUES(1400,1.2);
INSERT INTO "ducts_round" VALUES(1600,1.2);
INSERT INTO "ducts_round" VALUES(1800,1.4);
INSERT INTO "ducts_round" VALUES(2000,1.4);
CREATE TABLE "electrical_heat_base" (
"S_ID" INTEGER,
  "eq_id" INTEGER,
  "unit_power,kW" INTEGER,
  "quat" INTEGER,
  "k_ur" REAL,
  "k_lr" REAL,
  "k_sr" INTEGER,
  "k_mt" REAL,
  "n" REAL,
  "electrical_load" REAL
);
INSERT INTO "electrical_heat_base" VALUES(837890,1,20,1,0.9,0.8,1,0.6,0.8,9792.0);
INSERT INTO "electrical_heat_base" VALUES(837890,2,5,1,0.9,0.8,1,0.4,0.8,1872.0);
INSERT INTO "electrical_heat_base" VALUES(837890,3,10,1,0.9,0.8,1,0.4,0.8,3744.0);
INSERT INTO "electrical_heat_base" VALUES(837890,4,4,1,0.9,0.8,1,0.4,0.8,1.49760000000000026432e+03);
INSERT INTO "electrical_heat_base" VALUES(837902,5,8,1,0.9,0.8,1,0.4,0.8,2.99520000000000052864e+03);
INSERT INTO "electrical_heat_base" VALUES(837902,6,6,1,0.9,0.8,1,0.4,0.8,2.24640000000000039648e+03);
INSERT INTO "electrical_heat_base" VALUES(837902,7,8,1,0.9,0.8,1,0.4,0.8,2.99520000000000052864e+03);
INSERT INTO "electrical_heat_base" VALUES(837902,8,12,1,0.9,0.8,1,0.4,0.8,4.49280000000000079296e+03);
CREATE TABLE "equipment_heat_base" (
"equipment" TEXT,
  "equip_heat" INTEGER
);
INSERT INTO "equipment_heat_base" VALUES('computer',300);
CREATE TABLE "exaust_air_c" (
"family_device_name" TEXT,
  "family_instance_name" TEXT,
  "max_flow" REAL,
  "normal_velocity" INTEGER,
  "geometry" TEXT,
  "dimension1" INTEGER,
  "device_purpose" TEXT,
  "manufacture" TEXT,
  "sys_flow_parametr_name" TEXT,
  "sys_name_parametr" TEXT
);
INSERT INTO "exaust_air_c" VALUES('ADSK_Диффузор_Круглый_Вытяжной','ДВ_100',5.65199999999999924682e+01,2,'o',100,'air exaust','Systemair','ADSK_Расход воздуха','ИмяСистемы');
INSERT INTO "exaust_air_c" VALUES('ADSK_Диффузор_Круглый_Вытяжной','ДВ_125',88.3125,2,'o',125,'air exaust','Systemair','ADSK_Расход воздуха','ИмяСистемы');
INSERT INTO "exaust_air_c" VALUES('ADSK_Диффузор_Круглый_Вытяжной','ДВ_160',144.6912,2,'o',160,'air exaust','Systemair','ADSK_Расход воздуха','ИмяСистемы');
INSERT INTO "exaust_air_c" VALUES('ADSK_Диффузор_Круглый_Вытяжной','ДВ_200',2.26079999999999969872e+02,2,'o',200,'air exaust','Systemair','ADSK_Расход воздуха','ИмяСистемы');
INSERT INTO "exaust_air_c" VALUES('ADSK_Диффузор_Круглый_Вытяжной','ДВ_250',353.25,2,'o',250,'air exaust','Systemair','ADSK_Расход воздуха','ИмяСистемы');
CREATE TABLE "exaust_air_r" (
"family_device_name" TEXT,
  "family_instance_name" TEXT,
  "max_flow" INTEGER,
  "normal_velocity" INTEGER,
  "geometry" TEXT,
  "dimension1" INTEGER,
  "device_purpose" TEXT,
  "manufacture" TEXT,
  "sys_flow_parametr_name" TEXT,
  "sys_name_parametr" TEXT
);
INSERT INTO "exaust_air_r" VALUES('ADSK_Диффузор_Прямоугольный_Вытяжной','300х300',648,2,'s',300,'air exaust','Systemair','ADSK_Расход воздуха','ИмяСистемы');
INSERT INTO "exaust_air_r" VALUES('ADSK_Диффузор_Прямоугольный_Вытяжной','450х450',1458,2,'s',450,'air exaust','Systemair','ADSK_Расход воздуха','ИмяСистемы');
INSERT INTO "exaust_air_r" VALUES('ADSK_Диффузор_Прямоугольный_Вытяжной','600х600',2592,2,'s',600,'air exaust','Systemair','ADSK_Расход воздуха','ИмяСистемы');
CREATE TABLE "fancoils" (
"family_device_name" TEXT,
  "family_instance_name" TEXT,
  "max_flow" INTEGER,
  "normal_velocity" INTEGER,
  "geometry" TEXT,
  "dimension1" INTEGER,
  "device_purpose" TEXT,
  "manufacture" TEXT,
  "sys_flow_parametr_name" TEXT,
  "sys_name_parametr" TEXT
);
INSERT INTO "fancoils" VALUES('42GWC Carrier_univ','42GWC 200',2000,2,'D',400,'fancoil','CARRIER','FANCOIL_01','ИмяСистемы');
INSERT INTO "fancoils" VALUES('42GWC Carrier_univ','42GWC 300',4000,2,'D',500,'fancoil','CARRIER','FANCOIL_01','ИмяСистемы');
INSERT INTO "fancoils" VALUES('42GWC Carrier_univ','42GWC 400',6000,2,'D',600,'fancoil','CARRIER','FANCOIL_01','ИмяСистемы');
INSERT INTO "fancoils" VALUES('42GWC Carrier_univ','42GWC 500',8000,2,'D',700,'fancoil','CARRIER','FANCOIL_01','ИмяСистемы');
INSERT INTO "fancoils" VALUES('42GWC Carrier_univ','42GWC 600',10000,2,'D',800,'fancoil','CARRIER','FANCOIL_01','ИмяСистемы');
CREATE TABLE "heat_loss_orientation" (
"orientation" TEXT,
  "k-orientation" REAL
);
INSERT INTO "heat_loss_orientation" VALUES('n',1.1);
INSERT INTO "heat_loss_orientation" VALUES('s',1.0);
INSERT INTO "heat_loss_orientation" VALUES('w',1.1);
INSERT INTO "heat_loss_orientation" VALUES('e',1.05);
INSERT INTO "heat_loss_orientation" VALUES('h',1.0);
CREATE TABLE "heat_loss_surfaces" (
"surface_name" TEXT,
  "k-ef" REAL
);
INSERT INTO "heat_loss_surfaces" VALUES('wall',4.00568807706943896818e-01);
INSERT INTO "heat_loss_surfaces" VALUES('windows',2.403412846241662848e+00);
INSERT INTO "heat_loss_surfaces" VALUES('curtain',2.403412846241662848e+00);
INSERT INTO "heat_loss_surfaces" VALUES('floor_1',0.476);
INSERT INTO "heat_loss_surfaces" VALUES('floor_2',0.232);
INSERT INTO "heat_loss_surfaces" VALUES('floor_3',0.116);
INSERT INTO "heat_loss_surfaces" VALUES('floor_4',0.07);
INSERT INTO "heat_loss_surfaces" VALUES('roof',3.00426605780207856e-01);
INSERT INTO "heat_loss_surfaces" VALUES('doors',1.3882978723404255561e+00);
CREATE TABLE "human_heat_base" (
"group_human_work" TEXT,
  "human_heat" INTEGER
);
INSERT INTO "human_heat_base" VALUES('light',150);
INSERT INTO "human_heat_base" VALUES('medium',200);
INSERT INTO "human_heat_base" VALUES('hevy',290);
CREATE TABLE "input" (
"S_ID_old" REAL,
  "S_ID" INTEGER,
  "S_Number" INTEGER,
  "S_Name" TEXT,
  "S_height" REAL,
  "S_area" REAL,
  "S_Volume" REAL,
  "S_level" TEXT,
  "h_n" TEXT,
  "space_category" TEXT
);
INSERT INTO "input" VALUES(NULL,837890,1,'Помещение',2438.4,52.3366875000002,127.617778800001,'Этаж 01',NULL,'office');
INSERT INTO "input" VALUES(NULL,837891,2,'Помещение',2438.4,71.8717500000003,175.252075200001,'Этаж 01',NULL,'medicine');
INSERT INTO "input" VALUES(NULL,837892,3,'Помещение',2438.4,20.3038750000001,49.5089688000002,'Этаж 01',NULL,'office');
INSERT INTO "input" VALUES(NULL,837893,4,'Помещение',2438.4,24.4331250000006,59.5777320000014,'Этаж 01',NULL,'medicine');
INSERT INTO "input" VALUES(NULL,837894,5,'Помещение',2438.4,51.0450000000009,124.468128000002,'Этаж 01',NULL,'office');
INSERT INTO "input" VALUES(NULL,837895,6,'Помещение',2438.4,22.3835004333363,54.5799262778649,'Этаж 01','no','live_category');
INSERT INTO "input" VALUES(NULL,837896,7,'Помещение',2438.4,70.2260194068302,171.239125721615,'Этаж 01',NULL,'live_category');
INSERT INTO "input" VALUES(NULL,837897,8,'Помещение',2438.4,60.35625,147.17268,'Этаж 01',NULL,'medicine');
INSERT INTO "input" VALUES(NULL,837898,9,'Помещение',2438.4,59.022136708625,143.919598265996,'Этаж 01',NULL,'office');
INSERT INTO "input" VALUES(NULL,837899,11,'Помещение',2438.4,246.674999999994,601.492319999984,'Этаж 01','no','medicine');
INSERT INTO "input" VALUES(NULL,837900,12,'Помещение',2438.4,28.1681250000002,68.6851560000006,'Этаж 02',NULL,'office');
INSERT INTO "input" VALUES(NULL,837901,13,'Помещение',2438.4,55.5581250000001,135.472932,'Этаж 02',NULL,'medicine');
INSERT INTO "input" VALUES(NULL,837902,14,'Помещение',2438.4,61.7831250000009,150.651972000002,'Этаж 02',NULL,'office');
INSERT INTO "input" VALUES(NULL,837903,15,'Помещение',2438.4,24.4331250000006,59.5777320000014,'Этаж 02',NULL,'medicine');
INSERT INTO "input" VALUES(NULL,837904,16,'Помещение',2438.4,51.0450000000009,124.468128000002,'Этаж 02',NULL,'office');
INSERT INTO "input" VALUES(NULL,837905,17,'Помещение',2438.4,246.674999999994,601.492319999984,'Этаж 02',NULL,'medicine');
INSERT INTO "input" VALUES(NULL,837906,19,'Помещение',2438.4,22.3835004333363,54.5799262778649,'Этаж 02',NULL,'office');
INSERT INTO "input" VALUES(NULL,837907,20,'Помещение',2438.4,126.315236062017,308.00750214975,'Этаж 02',NULL,'medicine');
INSERT INTO "input" VALUES(NULL,837908,21,'Помещение',2438.4,156.140963207304,380.734651861625,'Этаж 02',NULL,'office');
INSERT INTO "input" VALUES(NULL,837909,22,'Помещение',2438.4,59.0221367086248,143.919598265995,'Этаж 02',NULL,'medicine');
INSERT INTO "input" VALUES(NULL,837910,23,'Помещение',2438.4,82.6368750000007,201.501756000002,'Этаж 03',NULL,'office');
INSERT INTO "input" VALUES(NULL,837911,24,'Помещение',2438.4,55.5581250000001,135.472932,'Этаж 03',NULL,'medicine');
INSERT INTO "input" VALUES(NULL,837912,25,'Помещение',2438.4,61.7831250000009,150.651972000002,'Этаж 03',NULL,'office');
INSERT INTO "input" VALUES(NULL,837913,26,'Помещение',2438.4,24.9000000000006,60.7161600000014,'Этаж 03',NULL,'medicine');
INSERT INTO "input" VALUES(NULL,837914,27,'Помещение',2438.4,51.0450000000009,124.468128000002,'Этаж 03',NULL,'office');
INSERT INTO "input" VALUES(NULL,837915,28,'Помещение',2438.4,247.087499999994,602.498159999984,'Этаж 03',NULL,'medicine');
INSERT INTO "input" VALUES(NULL,837916,30,'Помещение',2438.4,22.7461051137033,55.4641014335026,'Этаж 03',NULL,'office');
INSERT INTO "input" VALUES(NULL,837917,31,'Помещение',2438.4,78.5535004297582,191.545285984051,'Этаж 03',NULL,'office');
INSERT INTO "input" VALUES(NULL,837918,32,'Помещение',2438.4,68.9426251361959,168.1096971321,'Этаж 03',NULL,'medicine');
INSERT INTO "input" VALUES(NULL,837919,33,'Помещение',2438.4,59.0221367086248,143.919598265995,'Этаж 03',NULL,'office');
INSERT INTO "input" VALUES(NULL,837920,45,'Помещение',2438.4,246.674999999994,601.492319999984,'Этаж 04',NULL,'medicine');
INSERT INTO "input" VALUES(NULL,837921,46,'Помещение',2438.4,82.6368750000007,201.501756000002,'Этаж 04',NULL,'office');
INSERT INTO "input" VALUES(NULL,837922,47,'Помещение',2438.4,55.5581250000001,135.472932,'Этаж 04',NULL,'medicine');
INSERT INTO "input" VALUES(NULL,837923,48,'Помещение',2438.4,61.7831250000009,150.651972000002,'Этаж 04',NULL,'office');
INSERT INTO "input" VALUES(NULL,837924,49,'Помещение',2438.4,24.4331250000006,59.5777320000014,'Этаж 04',NULL,'medicine');
INSERT INTO "input" VALUES(NULL,837925,50,'Помещение',2438.4,51.0450000000009,124.468128000002,'Этаж 04',NULL,'office');
INSERT INTO "input" VALUES(NULL,837926,51,'Помещение',2438.4,22.3835004333363,54.5799262778649,'Этаж 04',NULL,'medicine');
INSERT INTO "input" VALUES(NULL,837927,52,'Помещение',2438.4,126.315236062017,308.00750214975,'Этаж 04',NULL,'office');
INSERT INTO "input" VALUES(NULL,837928,53,'Помещение',2438.4,156.140963207304,380.734651861625,'Этаж 04',NULL,'medicine');
INSERT INTO "input" VALUES(NULL,837929,54,'Помещение',2438.4,59.0221367086248,143.919598265995,'Этаж 04',NULL,'office');
INSERT INTO "input" VALUES(NULL,928204,55,'Помещение',2438.4,11.9953125000003,29.2493700000007,'Этаж 01',NULL,'medicine');
INSERT INTO "input" VALUES(NULL,928205,56,'Помещение',2438.4,40.0928750000008,97.762466400002,'Этаж 01',NULL,'office');
INSERT INTO "input" VALUES(NULL,928206,57,'Помещение',2438.4,93.395963207304,227.737243861625,'Этаж 01',NULL,'office');
INSERT INTO "input" VALUES(NULL,928207,58,'Помещение',2438.4,53.5694007000398,130.624057203106,'Этаж 01',NULL,'office');
INSERT INTO "input" VALUES(NULL,928208,59,'Помещение',2438.4,30.6581250000003,74.7567720000008,'Этаж 02',NULL,'office');
INSERT INTO "input" VALUES(NULL,928209,60,'Помещение',2438.4,21.9431250000002,53.5061160000003,'Этаж 02',NULL,'office');
INSERT INTO "input" VALUES(NULL,928210,61,'Помещение',2438.4,84.708303440923,206.553254287282,'Этаж 03',NULL,'office');
INSERT INTO "input" VALUES(NULL,928211,62,'Помещение',2438.4,45.8070862130591,111.695999021923,'Этаж 03',NULL,'office');
CREATE TABLE "medium_property" (
"system_type" TEXT,
  "short_sys_type" TEXT,
  "medium" TEXT,
  "k_roughness" REAL,
  "density" REAL,
  "viscosity" REAL,
  "heat_capacity" REAL,
  "power_or_flow" TEXT,
  "t_max" REAL,
  "t_min" REAL,
  "dt" INTEGER,
  "velocity_branch_normal" REAL,
  "velocity_root_normal" REAL,
  "prefix" TEXT,
  "diameter_type" TEXT,
  "k_local_pressure" REAL
);
INSERT INTO "medium_property" VALUES('heating_1st','HE1','water',0.2,0.97,3.263e-07,4.19,'power',90.0,70.0,20,0.5,0.8,'Q','pipes',2.0);
INSERT INTO "medium_property" VALUES('heating_2nd','HE2','water',0.2,0.97,3.263e-07,4.19,'power',90.0,70.0,20,0.5,0.8,'Q','pipes',2.0);
INSERT INTO "medium_property" VALUES('cooling_1st','CE1','water',0.2,0.97,3.263e-07,4.19,'power',12.0,8.0,4,0.5,1.5,'Q','pipes',2.0);
INSERT INTO "medium_property" VALUES('cooling_2nd','CE2','water',0.2,0.97,3.263e-07,4.19,'power',12.0,8.0,4,0.5,1.5,'Q','pipes',2.0);
INSERT INTO "medium_property" VALUES('recuperation','RE1','water',0.2,0.97,3.263e-07,4.19,'power',16.0,8.0,8,0.5,1.5,'Q','pipes',2.0);
INSERT INTO "medium_property" VALUES('ventilation','Air','air',0.2,1.205,1.49999999999999955591e-05,1.005,'flow',NULL,NULL,0,8.0,10.0,'L','ducts_round',1.3);
CREATE TABLE "pipes" (
"type" TEXT,
  "diameter" INTEGER
);
INSERT INTO "pipes" VALUES('Carbon steel',15);
INSERT INTO "pipes" VALUES('Carbon steel',20);
INSERT INTO "pipes" VALUES('Carbon steel',25);
INSERT INTO "pipes" VALUES('Carbon steel',32);
INSERT INTO "pipes" VALUES('Carbon steel',40);
INSERT INTO "pipes" VALUES('Carbon steel',50);
INSERT INTO "pipes" VALUES('Carbon steel',65);
INSERT INTO "pipes" VALUES('Carbon steel',80);
INSERT INTO "pipes" VALUES('Carbon steel',100);
INSERT INTO "pipes" VALUES('Carbon steel',125);
INSERT INTO "pipes" VALUES('Carbon steel',150);
INSERT INTO "pipes" VALUES('Carbon steel',200);
INSERT INTO "pipes" VALUES('Carbon steel',250);
INSERT INTO "pipes" VALUES('Carbon steel',300);
INSERT INTO "pipes" VALUES('Carbon steel',350);
INSERT INTO "pipes" VALUES('Carbon steel',400);
INSERT INTO "pipes" VALUES('Carbon steel',450);
INSERT INTO "pipes" VALUES('Carbon steel',500);
INSERT INTO "pipes" VALUES('Carbon steel',600);
INSERT INTO "pipes" VALUES('Carbon steel',700);
INSERT INTO "pipes" VALUES('Carbon steel',800);
INSERT INTO "pipes" VALUES('Carbon steel',900);
INSERT INTO "pipes" VALUES('Carbon steel',1000);
INSERT INTO "pipes" VALUES('Carbon steel',1100);
INSERT INTO "pipes" VALUES('Carbon steel',1200);
CREATE TABLE "project_property" (
"variable" TEXT,
  "definition" TEXT
);
INSERT INTO "project_property" VALUES('project_number','AAA.BBB.CCC.');
INSERT INTO "project_property" VALUES('project_name','Test Building');
CREATE TABLE "revit_export" (
"S_ID" INTEGER,
  "S_Number" INTEGER,
  "S_Name" TEXT,
  "S_height" REAL,
  "S_area" REAL,
  "S_Volume" REAL,
  "S_level" TEXT,
  "space_category" TEXT,
  "min_temp" INTEGER,
  "max_temp" INTEGER,
  "S_Cold_Load" REAL,
  "S_Heat_loss" REAL,
  "S_SA_max" REAL,
  "S_EA_max" REAL,
  "S_SA_fresh" REAL,
  "S_SA_recirc" REAL,
  "S_sup_name" TEXT,
  "E_ex_name" TEXT,
  "S_coold_name" TEXT,
  "S_heat_name" TEXT,
  "S_recuperation_system_name" TEXT
);
INSERT INTO "revit_export" VALUES(837890,1,'Помещение',2438.4,52.34,127.62,'Этаж 01','office',18,25,38457.93,837890.0,480.0,480.0,384.0,96.0,'S01','E02','C01','T01','S01_E01');
INSERT INTO "revit_export" VALUES(837891,2,'Помещение',2438.4,71.87,175.25,'Этаж 01','medicine',20,23,4115.51,0.0,876.26,876.26,657.2,219.07,'S02','E01','C01','T01','S01_E01');
INSERT INTO "revit_export" VALUES(837892,3,'Помещение',2438.4,20.3,49.51,'Этаж 01','office',18,25,1756.08,0.0,NULL,180.0,144.0,36.0,NULL,'E01','C01','T01','S01_E01');
INSERT INTO "revit_export" VALUES(837893,4,'Помещение',2438.4,24.43,59.58,'Этаж 01','medicine',20,23,1455.16,0.0,4297.89,297.89,3223.42,1074.47,'S01','E01','C01','T01','S01_E01');
INSERT INTO "revit_export" VALUES(837894,5,'Помещение',2438.4,51.05,124.47,'Этаж 01','office',18,25,4620.9,0.0,480.0,480.0,384.0,96.0,'S01','E01','C01','T01','S01_E01');
INSERT INTO "revit_export" VALUES(837895,6,'Помещение',2438.4,22.38,54.58,'Этаж 01','live_category',20,23,6119.18,5000.0,2272.9,272.9,2272.9,0.0,'S02','E01','C01','T01','S01_E01');
INSERT INTO "revit_export" VALUES(837896,7,'Помещение',2438.4,70.23,171.24,'Этаж 01','live_category',20,23,8511.3,5000.0,1856.2,856.2,1856.2,0.0,'S01','E01','C01','T01','S01_E01');
INSERT INTO "revit_export" VALUES(837897,8,'Помещение',2438.4,60.36,147.17,'Этаж 01','medicine',20,23,NULL,0.0,735.86,NULL,551.9,183.97,'S01',NULL,NULL,'T01','S01_E01');
INSERT INTO "revit_export" VALUES(837898,9,'Помещение',2438.4,59.02,143.92,'Этаж 01','office',18,25,5230.44,0.0,540.0,540.0,432.0,108.0,'S01','E01','C01','T01','S01_E01');
INSERT INTO "revit_export" VALUES(837899,11,'Помещение',2438.4,246.67,601.49,'Этаж 01','medicine',20,23,8633.62,0.0,3007.46,3007.46,2255.6,751.87,'S01','E01','C01','T01','S01_E01');
INSERT INTO "revit_export" VALUES(837900,12,'Помещение',2438.4,28.17,68.69,'Этаж 02','office',18,25,2813.36,0.0,300.0,300.0,240.0,60.0,'S02','E02','C02','T02',NULL);
INSERT INTO "revit_export" VALUES(837901,13,'Помещение',2438.4,55.56,135.47,'Этаж 02','medicine',20,23,3144.53,0.0,677.36,677.36,508.02,169.34,'S02','E02','C02','T02',NULL);
INSERT INTO "revit_export" VALUES(837902,14,'Помещение',2438.4,61.78,150.65,'Этаж 02','office',18,25,30744.86,837902.0,540.0,540.0,432.0,108.0,'S02','E01','C02','T02',NULL);
INSERT INTO "revit_export" VALUES(837903,15,'Помещение',2438.4,24.43,59.58,'Этаж 02','medicine',20,23,1455.16,0.0,297.89,297.89,223.42,74.47,'S01','E02','C02','T02',NULL);
INSERT INTO "revit_export" VALUES(837904,16,'Помещение',2438.4,51.05,124.47,'Этаж 02','office',18,25,4620.9,0.0,480.0,480.0,384.0,96.0,'S02','E02','C02','T02',NULL);
INSERT INTO "revit_export" VALUES(837905,17,'Помещение',2438.4,246.67,601.49,'Этаж 02','medicine',20,23,13633.62,0.0,3007.46,3007.46,2255.6,751.87,'S02','E02','C02','T02',NULL);
INSERT INTO "revit_export" VALUES(837906,19,'Помещение',2438.4,22.38,54.58,'Этаж 02','office',18,25,2247.67,0.0,240.0,240.0,192.0,48.0,'S02','E02','C02',NULL,NULL);
INSERT INTO "revit_export" VALUES(837907,20,'Помещение',2438.4,126.32,308.01,'Этаж 02','medicine',20,23,7021.03,0.0,1540.04,1540.04,1155.03,385.01,'S02','E02','C02','T02',NULL);
INSERT INTO "revit_export" VALUES(837908,21,'Помещение',2438.4,156.14,380.73,'Этаж 02','office',18,25,13472.82,0.0,1380.0,1380.0,1104.0,276.0,'S02','E02','C02','T02',NULL);
INSERT INTO "revit_export" VALUES(837909,22,'Помещение',2438.4,59.02,143.92,'Этаж 02','medicine',20,23,3265.77,0.0,719.6,719.6,539.7,179.9,'S02','E02','C02','T02',NULL);
INSERT INTO "revit_export" VALUES(837910,23,'Помещение',2438.4,82.64,201.5,'Этаж 03','office',18,25,7052.74,0.0,720.0,720.0,576.0,144.0,'S03','E03','C03','T03',NULL);
INSERT INTO "revit_export" VALUES(837911,24,'Помещение',2438.4,55.56,135.47,'Этаж 03','medicine',20,23,3144.53,0.0,677.36,677.36,508.02,169.34,'S03',NULL,NULL,'T03',NULL);
INSERT INTO "revit_export" VALUES(837912,25,'Помещение',2438.4,61.78,150.65,'Этаж 03','office',18,25,5285.66,0.0,540.0,540.0,432.0,108.0,'S03','E02','C03','T03',NULL);
INSERT INTO "revit_export" VALUES(837913,26,'Помещение',2438.4,24.9,60.72,'Этаж 03','medicine',20,23,1471.5,0.0,303.58,303.58,227.69,75.9,NULL,'E03','C03','T03',NULL);
INSERT INTO "revit_export" VALUES(837914,27,'Помещение',2438.4,51.05,124.47,'Этаж 03','office',18,25,4620.9,0.0,480.0,480.0,384.0,96.0,'S03','E03','C03','T03',NULL);
INSERT INTO "revit_export" VALUES(837915,28,'Помещение',2438.4,247.09,602.5,'Этаж 03','medicine',20,23,13648.06,0.0,3012.49,3012.49,2259.37,753.12,'S02','E03','C03','T03',NULL);
INSERT INTO "revit_export" VALUES(837916,30,'Помещение',2438.4,22.75,55.46,'Этаж 03','office',18,25,2254.92,0.0,240.0,240.0,192.0,48.0,'S03','E03','C03','T03',NULL);
INSERT INTO "revit_export" VALUES(837917,31,'Помещение',2438.4,78.55,191.55,'Этаж 03','office',18,25,6971.07,0.0,720.0,720.0,576.0,144.0,'S03','E03','C03','T03',NULL);
INSERT INTO "revit_export" VALUES(837918,32,'Помещение',2438.4,68.94,168.11,'Этаж 03','medicine',20,23,3812.99,0.0,840.55,840.55,630.41,210.14,'S03','E03','C03','T03',NULL);
INSERT INTO "revit_export" VALUES(837919,33,'Помещение',2438.4,59.02,143.92,'Этаж 03','office',18,25,5230.44,0.0,540.0,540.0,432.0,108.0,'S03','E03','C03','T03',NULL);
INSERT INTO "revit_export" VALUES(837920,45,'Помещение',2438.4,246.67,601.49,'Этаж 04','medicine',20,23,50634.87,2964.31,3007.46,3007.46,2255.6,751.87,'S04','E04','C04','T04',NULL);
INSERT INTO "revit_export" VALUES(837921,46,'Помещение',2438.4,82.64,201.5,'Этаж 04','office',18,25,19448.27,943.4,720.0,720.0,576.0,144.0,'S04','E04','C04','T04',NULL);
INSERT INTO "revit_export" VALUES(837922,47,'Помещение',2438.4,55.56,135.47,'Этаж 04','medicine',20,23,11478.25,667.65,677.36,677.36,508.02,169.34,'S04','E04','C04','T04',NULL);
INSERT INTO "revit_export" VALUES(837923,48,'Помещение',2438.4,61.78,150.65,'Этаж 04','office',18,25,14553.13,705.33,540.0,540.0,432.0,108.0,'S04','E04','C04','T04',NULL);
INSERT INTO "revit_export" VALUES(837924,49,'Помещение',2438.4,24.43,59.58,'Этаж 04','medicine',20,23,5120.13,293.61,297.89,297.89,223.42,74.47,'S04','E04','C04','T04',NULL);
INSERT INTO "revit_export" VALUES(837925,50,'Помещение',2438.4,51.05,124.47,'Этаж 04','office',18,25,12277.65,582.74,480.0,480.0,384.0,96.0,'S04','E04','C04','T04',NULL);
INSERT INTO "revit_export" VALUES(837926,51,'Помещение',2438.4,22.38,54.58,'Этаж 04','medicine',20,23,4740.95,268.98,272.9,272.9,204.67,68.22,'S04','E04','C04','T04',NULL);
INSERT INTO "revit_export" VALUES(837927,52,'Помещение',2438.4,126.32,308.01,'Этаж 04','office',18,25,30023.59,1442.04,1140.0,1140.0,912.0,228.0,'S04','E04','C04','T04',NULL);
INSERT INTO "revit_export" VALUES(837928,53,'Помещение',2438.4,156.14,380.73,'Этаж 04','medicine',20,23,32086.08,1876.36,1903.67,1903.67,1427.75,475.92,'S04','E04','C04','T04',NULL);
INSERT INTO "revit_export" VALUES(837929,54,'Помещение',2438.4,59.02,143.92,'Этаж 04','office',18,25,14083.76,673.81,540.0,540.0,432.0,108.0,'S04','E04','C04','T04',NULL);
INSERT INTO "revit_export" VALUES(928204,55,'Помещение',2438.4,12.0,29.25,'Этаж 01','medicine',20,23,819.84,0.0,146.25,146.25,109.69,36.56,'S04','E04','C04','T04',NULL);
INSERT INTO "revit_export" VALUES(928205,56,'Помещение',2438.4,40.09,97.76,'Этаж 01','office',18,25,3501.86,0.0,360.0,360.0,288.0,72.0,'S04','E04','C04','T04',NULL);
INSERT INTO "revit_export" VALUES(928206,57,'Помещение',2438.4,93.4,227.74,'Этаж 01','office',18,25,8167.92,0.0,840.0,840.0,672.0,168.0,'S04','E04','C04','T04',NULL);
INSERT INTO "revit_export" VALUES(928207,58,'Помещение',2438.4,53.57,130.62,'Этаж 01','office',18,25,4671.39,0.0,480.0,480.0,384.0,96.0,'S04','E04','C04','T04',NULL);
INSERT INTO "revit_export" VALUES(928208,59,'Помещение',2438.4,30.66,74.76,'Этаж 02','office',18,25,2863.16,0.0,300.0,300.0,240.0,60.0,'S04','E04','C04','T04',NULL);
INSERT INTO "revit_export" VALUES(928209,60,'Помещение',2438.4,21.94,53.51,'Этаж 02','office',18,25,2238.86,0.0,240.0,240.0,192.0,48.0,'S04','E04','C04','T04',NULL);
INSERT INTO "revit_export" VALUES(928210,61,'Помещение',2438.4,84.71,206.55,'Этаж 03','office',18,25,7544.17,0.0,780.0,780.0,624.0,156.0,'S04','E04','C04','T04',NULL);
INSERT INTO "revit_export" VALUES(928211,62,'Помещение',2438.4,45.81,111.7,'Этаж 03','office',18,25,4066.14,0.0,420.0,420.0,336.0,84.0,'S04','E04','C04','T04',NULL);
CREATE TABLE "sheet_names" (
"var_calculated_name" TEXT,
  "excel_sheet_name" TEXT,
  "ru_browser_name" TEXT,
  "group_sum_column" TEXT,
  "main_column_names" TEXT
);
INSERT INTO "sheet_names" VALUES('hb_total','Total Heat Balance','Общий тепловой баланс',NULL,'S_ID,S_Number,S_Name,S_height,S_area,S_Volume,S_level,space_category');
INSERT INTO "sheet_names" VALUES('heat_load_balance','Heat load balance','Суммарный баланс теплопоступления',NULL,'S_ID,S_Number,S_Name,S_height,S_area,S_Volume,S_level,space_category');
INSERT INTO "sheet_names" VALUES('heat_loss_balance','Heat loss balance','Суммарный баланс тепловых потерь',NULL,'S_ID,S_Number,S_Name,S_height,S_area,S_Volume,S_level,space_category');
INSERT INTO "sheet_names" VALUES('hb_human','Human load balance','Тепловыделения от людей','human_heat_sum','S_ID,S_Number,S_Name,S_height,S_area,S_Volume,S_level,space_category,human_heat, h_n_c');
INSERT INTO "sheet_names" VALUES('hb_lighting','Lighting load balance','Тепловыделения от освещения','lighting_heat_sum','S_ID,S_Number,S_Name,S_height,S_area,S_Volume,S_level,space_category,lighting');
INSERT INTO "sheet_names" VALUES('hb_equipment','Equipment load balance','Тепловыделения от оборудования','equipment_heat_sum','S_ID,S_Number,S_Name,S_height,S_area,S_Volume,S_level,space_category,equip_heat, h_n_c');
INSERT INTO "sheet_names" VALUES('h_loss','Heat losses','Тепловые потери ограждения','heat_loss_sum','S_ID,S_Number,S_Name,S_height,S_area,S_Volume,S_level,space_category');
INSERT INTO "sheet_names" VALUES('hb_rad','Radiation load','Тепловыделения от солнечной радиации','radiation_load_sum','S_ID,S_Number,S_Name,S_height,S_area,S_Volume,S_level,space_category');
INSERT INTO "sheet_names" VALUES('ab_max','Air balance total','Максимальный расход воздуха в помещении','max_heat_sum','S_ID,S_Number,S_Name,S_height,S_area,S_Volume,S_level,space_category');
INSERT INTO "sheet_names" VALUES('ab_human','Air balance humans','Расход воздуха по гигеиническим нормам','human_heat_sum','S_ID,S_Number,S_Name,S_height,S_area,S_Volume,S_level,space_category');
INSERT INTO "sheet_names" VALUES('ab_mult','Air balance by air multiplicities','Расход воздуха по нормам кратности','mult_heat_sum','S_ID,S_Number,S_Name,S_height,S_area,S_Volume,S_level,space_category');
CREATE TABLE "sun_radiation_load" (
"heat_sun_key" TEXT,
  "heat_load, w/m2" INTEGER
);
INSERT INTO "sun_radiation_load" VALUES('windows_w',350);
INSERT INTO "sun_radiation_load" VALUES('windows_s',360);
INSERT INTO "sun_radiation_load" VALUES('windows_n',100);
INSERT INTO "sun_radiation_load" VALUES('windows_e',350);
INSERT INTO "sun_radiation_load" VALUES('wall_w',5);
INSERT INTO "sun_radiation_load" VALUES('wall_s',5);
INSERT INTO "sun_radiation_load" VALUES('wall_n',5);
INSERT INTO "sun_radiation_load" VALUES('wall_e',5);
INSERT INTO "sun_radiation_load" VALUES('roof_h',150);
INSERT INTO "sun_radiation_load" VALUES('doors_w',10);
INSERT INTO "sun_radiation_load" VALUES('doors_s',10);
INSERT INTO "sun_radiation_load" VALUES('doors_n',10);
INSERT INTO "sun_radiation_load" VALUES('doors_e',10);
CREATE TABLE "supply_air_c" (
"family_device_name" TEXT,
  "family_instance_name" TEXT,
  "max_flow" REAL,
  "normal_velocity" INTEGER,
  "geometry" TEXT,
  "dimension1" INTEGER,
  "device_purpose" TEXT,
  "manufacture" TEXT,
  "sys_flow_parametr_name" TEXT,
  "sys_name_parametr" TEXT
);
INSERT INTO "supply_air_c" VALUES('ADSK_Диффузор_Круглый_Приточный','ДП_100',5.65199999999999924682e+01,2,'o',100,'air supply','Systemair','ADSK_Расход воздуха','ИмяСистемы');
INSERT INTO "supply_air_c" VALUES('ADSK_Диффузор_Круглый_Приточный','ДП_125',88.3125,2,'o',125,'air supply','Systemair','ADSK_Расход воздуха','ИмяСистемы');
INSERT INTO "supply_air_c" VALUES('ADSK_Диффузор_Круглый_Приточный','ДП_160',144.6912,2,'o',160,'air supply','Systemair','ADSK_Расход воздуха','ИмяСистемы');
INSERT INTO "supply_air_c" VALUES('ADSK_Диффузор_Круглый_Приточный','ДП_200',2.26079999999999969872e+02,2,'o',200,'air supply','Systemair','ADSK_Расход воздуха','ИмяСистемы');
INSERT INTO "supply_air_c" VALUES('ADSK_Диффузор_Круглый_Приточный','ДП_250',353.25,2,'o',250,'air supply','Systemair','ADSK_Расход воздуха','ИмяСистемы');
CREATE TABLE "supply_air_r" (
"family_device_name" TEXT,
  "family_instance_name" TEXT,
  "max_flow" INTEGER,
  "normal_velocity" INTEGER,
  "geometry" TEXT,
  "dimension1" INTEGER,
  "device_purpose" TEXT,
  "manufacture" TEXT,
  "sys_flow_parametr_name" TEXT,
  "sys_name_parametr" TEXT
);
INSERT INTO "supply_air_r" VALUES('ADSK_Диффузор_Прямоугольный_Приточный','300х300',648,2,'s',300,'air supply','Systemair','ADSK_Расход воздуха','ИмяСистемы');
INSERT INTO "supply_air_r" VALUES('ADSK_Диффузор_Прямоугольный_Приточный','450х450',1458,2,'s',450,'air supply','Systemair','ADSK_Расход воздуха','ИмяСистемы');
INSERT INTO "supply_air_r" VALUES('ADSK_Диффузор_Прямоугольный_Приточный','600х600',2592,2,'s',600,'air supply','Systemair','ADSK_Расход воздуха','ИмяСистемы');
CREATE TABLE "surfaces" (
"surface_name" TEXT,
  "surf_area" REAL,
  "space_id" INTEGER,
  "orientation" TEXT
);
INSERT INTO "surfaces" VALUES('wall',40.5,837891,'n');
INSERT INTO "surfaces" VALUES('wall',15.2,837891,'w');
INSERT INTO "surfaces" VALUES('wall',9.6,837893,'n');
INSERT INTO "surfaces" VALUES('wall',15.2,837893,'e');
INSERT INTO "surfaces" VALUES('wall',20.0,837894,'n');
INSERT INTO "surfaces" VALUES('wall',11.8,837895,'e');
INSERT INTO "surfaces" VALUES('wall',10.4,837895,'s');
INSERT INTO "surfaces" VALUES('wall',11.8,837898,'w');
INSERT INTO "surfaces" VALUES('wall',23.2,837898,'s');
INSERT INTO "surfaces" VALUES('wall',13.4,837899,'w');
INSERT INTO "surfaces" VALUES('wall',13.4,837899,'e');
INSERT INTO "surfaces" VALUES('wall',11.0,837900,'n');
INSERT INTO "surfaces" VALUES('wall',21.8,837901,'n');
INSERT INTO "surfaces" VALUES('wall',15.2,837901,'w');
INSERT INTO "surfaces" VALUES('wall',24.2,837902,'n');
INSERT INTO "surfaces" VALUES('wall',9.6,837903,'n');
INSERT INTO "surfaces" VALUES('wall',15.2,837903,'e');
INSERT INTO "surfaces" VALUES('wall',20.0,837904,'n');
INSERT INTO "surfaces" VALUES('wall',13.4,837905,'w');
INSERT INTO "surfaces" VALUES('wall',13.4,837905,'e');
INSERT INTO "surfaces" VALUES('wall',11.8,837906,'e');
INSERT INTO "surfaces" VALUES('wall',10.4,837906,'s');
INSERT INTO "surfaces" VALUES('wall',37.2,837907,'s');
INSERT INTO "surfaces" VALUES('wall',41.1,837908,'s');
INSERT INTO "surfaces" VALUES('wall',11.8,837909,'w');
INSERT INTO "surfaces" VALUES('wall',23.2,837909,'s');
INSERT INTO "surfaces" VALUES('wall',32.4,837910,'n');
INSERT INTO "surfaces" VALUES('wall',21.8,837911,'n');
INSERT INTO "surfaces" VALUES('wall',15.2,837911,'w');
INSERT INTO "surfaces" VALUES('wall',24.2,837912,'n');
INSERT INTO "surfaces" VALUES('wall',9.8,837913,'n');
INSERT INTO "surfaces" VALUES('wall',20.0,837914,'n');
INSERT INTO "surfaces" VALUES('wall',13.4,837915,'w');
INSERT INTO "surfaces" VALUES('wall',10.6,837916,'s');
INSERT INTO "surfaces" VALUES('wall',37.2,837917,'s');
INSERT INTO "surfaces" VALUES('wall',11.8,837919,'w');
INSERT INTO "surfaces" VALUES('wall',23.2,837919,'s');
INSERT INTO "surfaces" VALUES('wall',13.4,837920,'w');
INSERT INTO "surfaces" VALUES('wall',13.4,837920,'e');
INSERT INTO "surfaces" VALUES('wall',32.4,837921,'n');
INSERT INTO "surfaces" VALUES('wall',21.8,837922,'n');
INSERT INTO "surfaces" VALUES('wall',15.2,837922,'w');
INSERT INTO "surfaces" VALUES('wall',24.2,837923,'n');
INSERT INTO "surfaces" VALUES('wall',9.6,837924,'n');
INSERT INTO "surfaces" VALUES('wall',15.2,837924,'e');
INSERT INTO "surfaces" VALUES('wall',20.0,837925,'n');
INSERT INTO "surfaces" VALUES('wall',11.8,837926,'e');
INSERT INTO "surfaces" VALUES('wall',10.4,837926,'s');
INSERT INTO "surfaces" VALUES('wall',37.2,837927,'s');
INSERT INTO "surfaces" VALUES('wall',41.1,837928,'s');
INSERT INTO "surfaces" VALUES('wall',11.8,837929,'w');
INSERT INTO "surfaces" VALUES('wall',23.2,837929,'s');
INSERT INTO "surfaces" VALUES('wall',13.7,928204,'n');
INSERT INTO "surfaces" VALUES('wall',24.2,928205,'n');
INSERT INTO "surfaces" VALUES('wall',41.1,928206,'s');
INSERT INTO "surfaces" VALUES('wall',37.2,928207,'s');
INSERT INTO "surfaces" VALUES('wall',12.0,928208,'n');
INSERT INTO "surfaces" VALUES('wall',8.6,928209,'n');
INSERT INTO "surfaces" VALUES('wall',41.1,928210,'s');
INSERT INTO "surfaces" VALUES('curtain',15.2,837913,'e');
INSERT INTO "surfaces" VALUES('curtain',13.4,837915,'e');
INSERT INTO "surfaces" VALUES('curtain',11.8,837916,'e');
INSERT INTO "surfaces" VALUES('windows',2.7,837891,'n');
INSERT INTO "surfaces" VALUES('windows',2.7,837891,'w');
INSERT INTO "surfaces" VALUES('windows',2.7,837891,'n');
INSERT INTO "surfaces" VALUES('windows',2.7,837893,'n');
INSERT INTO "surfaces" VALUES('windows',2.7,837893,'e');
INSERT INTO "surfaces" VALUES('windows',2.7,837894,'n');
INSERT INTO "surfaces" VALUES('windows',2.7,837895,'s');
INSERT INTO "surfaces" VALUES('windows',2.7,837895,'e');
INSERT INTO "surfaces" VALUES('windows',2.7,837898,'s');
INSERT INTO "surfaces" VALUES('windows',2.7,837898,'w');
INSERT INTO "surfaces" VALUES('windows',2.7,837899,'e');
INSERT INTO "surfaces" VALUES('windows',2.7,837900,'n');
INSERT INTO "surfaces" VALUES('windows',2.7,837901,'n');
INSERT INTO "surfaces" VALUES('windows',2.7,837901,'w');
INSERT INTO "surfaces" VALUES('windows',2.7,837902,'n');
INSERT INTO "surfaces" VALUES('windows',2.7,837903,'n');
INSERT INTO "surfaces" VALUES('windows',2.7,837903,'e');
INSERT INTO "surfaces" VALUES('windows',2.7,837904,'n');
INSERT INTO "surfaces" VALUES('windows',2.7,837905,'e');
INSERT INTO "surfaces" VALUES('windows',2.7,837906,'s');
INSERT INTO "surfaces" VALUES('windows',2.7,837906,'e');
INSERT INTO "surfaces" VALUES('windows',2.7,837907,'s');
INSERT INTO "surfaces" VALUES('windows',2.7,837907,'s');
INSERT INTO "surfaces" VALUES('windows',2.7,837907,'s');
INSERT INTO "surfaces" VALUES('windows',2.7,837908,'s');
INSERT INTO "surfaces" VALUES('windows',2.7,837908,'s');
INSERT INTO "surfaces" VALUES('windows',2.7,837908,'s');
INSERT INTO "surfaces" VALUES('windows',2.7,837909,'s');
INSERT INTO "surfaces" VALUES('windows',2.7,837909,'w');
INSERT INTO "surfaces" VALUES('windows',2.7,837910,'n');
INSERT INTO "surfaces" VALUES('windows',2.7,837911,'n');
INSERT INTO "surfaces" VALUES('windows',2.7,837911,'w');
INSERT INTO "surfaces" VALUES('windows',2.7,837912,'n');
INSERT INTO "surfaces" VALUES('windows',2.7,837913,'n');
INSERT INTO "surfaces" VALUES('windows',2.7,837914,'n');
INSERT INTO "surfaces" VALUES('windows',2.7,837916,'s');
INSERT INTO "surfaces" VALUES('windows',2.7,837917,'s');
INSERT INTO "surfaces" VALUES('windows',2.7,837917,'s');
INSERT INTO "surfaces" VALUES('windows',2.7,837917,'s');
INSERT INTO "surfaces" VALUES('windows',2.7,837919,'s');
INSERT INTO "surfaces" VALUES('windows',2.7,837919,'w');
INSERT INTO "surfaces" VALUES('windows',2.7,837920,'e');
INSERT INTO "surfaces" VALUES('windows',2.7,837921,'n');
INSERT INTO "surfaces" VALUES('windows',2.7,837922,'n');
INSERT INTO "surfaces" VALUES('windows',2.7,837922,'w');
INSERT INTO "surfaces" VALUES('windows',2.7,837923,'n');
INSERT INTO "surfaces" VALUES('windows',2.7,837924,'n');
INSERT INTO "surfaces" VALUES('windows',2.7,837924,'e');
INSERT INTO "surfaces" VALUES('windows',2.7,837925,'n');
INSERT INTO "surfaces" VALUES('windows',2.7,837926,'s');
INSERT INTO "surfaces" VALUES('windows',2.7,837926,'e');
INSERT INTO "surfaces" VALUES('windows',2.7,837927,'s');
INSERT INTO "surfaces" VALUES('windows',2.7,837927,'s');
INSERT INTO "surfaces" VALUES('windows',2.7,837927,'s');
INSERT INTO "surfaces" VALUES('windows',2.7,837928,'s');
INSERT INTO "surfaces" VALUES('windows',2.7,837928,'s');
INSERT INTO "surfaces" VALUES('windows',2.7,837928,'s');
INSERT INTO "surfaces" VALUES('windows',2.7,837929,'s');
INSERT INTO "surfaces" VALUES('windows',2.7,837929,'w');
INSERT INTO "surfaces" VALUES('windows',2.7,928205,'n');
INSERT INTO "surfaces" VALUES('windows',2.7,928206,'s');
INSERT INTO "surfaces" VALUES('windows',2.7,928206,'s');
INSERT INTO "surfaces" VALUES('windows',2.7,928206,'s');
INSERT INTO "surfaces" VALUES('windows',2.7,928207,'s');
INSERT INTO "surfaces" VALUES('windows',2.7,928207,'s');
INSERT INTO "surfaces" VALUES('windows',2.7,928207,'s');
INSERT INTO "surfaces" VALUES('windows',2.7,928210,'s');
INSERT INTO "surfaces" VALUES('windows',2.7,928210,'s');
INSERT INTO "surfaces" VALUES('windows',2.7,928210,'s');
INSERT INTO "surfaces" VALUES('doors',2.0,837899,'w');
CREATE VIEW heat_surface_loss AS SELECT input.'S_ID', input.'S_Number', input.'S_Name', input.'S_height', input.'S_area', input.'S_Volume', input.'S_level', input.'h_n', input.'space_category',surfaces.'surface_name', surfaces.'surf_area', surfaces.'orientation',category.'min_temp',heat_loss_orientation.'k-orientation',heat_loss_surfaces.'k-ef', climate_data.climate_data as tнар, surfaces.'surf_area'*heat_loss_orientation.'k-orientation'*heat_loss_surfaces.'k-ef'*(category.'min_temp'-climate_data.climate_data) as heat_loss FROM input LEFT JOIN category ON input.'space_category'=category.'space_category' LEFT JOIN surfaces ON input.'S_ID'=surfaces.'space_id' LEFT JOIN heat_loss_surfaces ON surfaces.'surface_name'=heat_loss_surfaces.'surface_name' LEFT JOIN heat_loss_orientation ON surfaces.'orientation'=heat_loss_orientation.'orientation' CROSS JOIN climate_data Where climate_data.climate_label ='t_нар_зим';
COMMIT;
