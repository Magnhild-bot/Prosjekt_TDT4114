import pandas as pd
import os
from Functions_FetchData import data_reader
from Functions_FetchData import download_temp_file
import json
import pandasql as psql
from pandasql import sqldf

script_dir= os.path.dirname(os.path.abspath(__file__)) #dir til dette scriptet
project_dir=os.path.dirname(script_dir)#dir til hele prosjektmappen
data_dir=os.path.join(project_dir,'data')


#------------Cheks what information the file contains by using the data_reader function-------------


#1:
Airpollutant_data=(os.path.join(data_dir, 'PM10.xlsx'))
data_reader(Airpollutant_data,20)


print('    ')
print('    ')
print('Tester ny fil...........')
print('    ')


#2:
csv_url = "https://sdi.eea.europa.eu/webdav/datastore/public/eea_t_national-emissions-reported_p_2024_v01_r00/CSV/UNFCCC_v27.csv"
CO2_data = download_temp_file(csv_url) #fra test_filbehandling
data_reader(CO2_data, 30)


#3

data_json = {
    "dataset": {
        "dimension": {
            "UtslpTilLuft": {
                "label": "kilde (aktivitet)",
                "category": {
                    "index": {
                        "0": 0,
                        "1": 1,
                        "2": 2,
                        "3": 3,
                        "4": 4,
                        "5": 5,
                        "6": 6,
                        "7": 7,
                        "9": 8
                    },
                    "label": {
                        "0": "Alle kilder",
                        "1": "Olje- og gassutvinning",
                        "2": "Industri og bergverk",
                        "3": "Energiforsyning",
                        "4": "Oppvarming i andre næringer og husholdninger",
                        "5": "Veitrafikk",
                        "6": "Luftfart, sjøfart, fiske, motorredskaper m.m.",
                        "7": "Jordbruk",
                        "9": "Andre kilder"
                    },
                    "link": {
                        "describedby": [
                            {
                                "extension": {
                                    "UtslpTilLuft": "urn:ssb:classification:klass:113"
                                }
                            }
                        ]
                    },
                    "extension": {
                        "show": "code_value"
                    }
                }
            },
            "UtslpKomp": {
                "label": "komponent",
                "category": {
                    "index": {
                        "A10": 0
                    },
                    "label": {
                        "A10": "Klimagasser i alt"
                    },
                    "extension": {
                        "show": "value"
                    }
                }
            },
            "Tid": {
                "label": "år",
                "category": {
                    "index": {
                        "1990": 0,
                        "1991": 1,
                        "1992": 2,
                        "1993": 3,
                        "1994": 4,
                        "1995": 5,
                        "1996": 6,
                        "1997": 7,
                        "1998": 8,
                        "1999": 9,
                        "2000": 10,
                        "2001": 11,
                        "2002": 12,
                        "2003": 13,
                        "2004": 14,
                        "2005": 15,
                        "2006": 16,
                        "2007": 17,
                        "2008": 18,
                        "2009": 19,
                        "2010": 20,
                        "2011": 21,
                        "2012": 22,
                        "2013": 23,
                        "2014": 24,
                        "2015": 25,
                        "2016": 26,
                        "2017": 27,
                        "2018": 28,
                        "2019": 29,
                        "2020": 30,
                        "2021": 31,
                        "2022": 32
                    },
                    "label": {
                        "1990": "1990",
                        "1991": "1991",
                        "1992": "1992",
                        "1993": "1993",
                        "1994": "1994",
                        "1995": "1995",
                        "1996": "1996",
                        "1997": "1997",
                        "1998": "1998",
                        "1999": "1999",
                        "2000": "2000",
                        "2001": "2001",
                        "2002": "2002",
                        "2003": "2003",
                        "2004": "2004",
                        "2005": "2005",
                        "2006": "2006",
                        "2007": "2007",
                        "2008": "2008",
                        "2009": "2009",
                        "2010": "2010",
                        "2011": "2011",
                        "2012": "2012",
                        "2013": "2013",
                        "2014": "2014",
                        "2015": "2015",
                        "2016": "2016",
                        "2017": "2017",
                        "2018": "2018",
                        "2019": "2019",
                        "2020": "2020",
                        "2021": "2021",
                        "2022": "2022"
                    }
                }
            },
            "ContentsCode": {
                "label": "statistikkvariabel",
                "category": {
                    "index": {
                        "UtslippCO2ekvival": 0
                    },
                    "label": {
                        "UtslippCO2ekvival": "Utslipp til luft (1 000 tonn CO2-ekvivalenter, AR4)"
                    },
                    "unit": {
                        "UtslippCO2ekvival": {
                            "base": "1 000 tonn CO2-ekvivalenter",
                            "decimals": 0
                        }
                    }
                }
            }
        },
        "value": [
            51342, 48947, 47303, 49245, 51153, 51576, 54452, 54405, 54493, 55506,
            54866, 56110, 54874, 55412, 55806, 54713, 54661, 56338, 54784, 52187,
            54460, 53553, 52931, 53177, 53587, 54098, 53225, 52524, 52632, 50902,
            49235, 49074, 48691, 8204, 8076, 8665, 9186, 9978, 10162, 11051, 11536,
            11202, 11720, 13057, 14017, 13696, 13840, 14063, 14015, 13624, 15072,
            14729, 13606, 13716, 13410, 13513, 13483, 14173, 14707, 14409, 14144,
            13961, 13801, 13099, 12041, 11997, 19676, 18100, 15758, 16729, 17652,
            16939, 17526, 17192, 17493, 17293, 17125, 16604, 15579, 15355, 15625,
            15170, 14737, 14401, 13907, 11321, 12090, 12095, 11797, 11828, 11477,
            11759, 11428, 11829, 11852, 11406, 11300, 11667, 11509, 341, 397, 390,
            410, 466, 469, 561, 493, 538, 523, 485, 541, 583, 715, 605, 591, 648,
            948, 802, 2015, 2453, 2240, 1729, 1770, 1767, 1765, 1749, 1906, 1902,
            1794, 1732, 1761, 1499, 2708, 2448, 2235, 2261, 2279, 2320, 2853, 2415,
            2185, 2423, 1873, 2084, 2264, 2653, 2263, 1783, 1881, 1677, 1498, 1635,
            1933, 1401, 1275, 1224, 1009, 903, 1007, 882, 761, 568, 491, 553, 586,
            7423, 7305, 7336, 7510, 7408, 7528, 7904, 7890, 8119, 8546, 8374, 8875,
            8952, 9093, 9388, 9522, 9800, 10032, 9897, 9744, 9995, 9933, 9962, 10010,
            10223, 10257, 9991, 9125, 9365, 8730, 8342, 8704, 8693, 5302, 5112, 5465,
            5669, 5862, 6558, 6965, 7251, 7467, 7530, 6502, 6592, 6550, 6474, 6586,
            6430, 6788, 7007, 6787, 6733, 7172, 7262, 7471, 7593, 7649, 7455, 7384,
            7492, 7736, 7672, 7372, 7441, 7676, 4871, 4810, 4779, 4760, 4751, 4798,
            4831, 4784, 4775, 4758, 4622, 4557, 4547, 4629, 4599, 4617, 4528, 4539,
            4510, 4461, 4369, 4386, 4397, 4442, 4393, 4329, 4364, 4377, 4389, 4424,
            4424, 4335, 4244, 4175, 4128, 4067, 3937, 3842, 3757, 3659, 3583, 3575
        ]
    }
}

with open("ekvivalenter_data.json", "w", encoding="utf-8") as f:
    json.dump(data_json, f, ensure_ascii=False, indent=4)

data_ekvivalenter = data_reader("ekvivalenter_data.json", 20)


pysqldf = lambda q: sqldf(q, globals())

#Trying to use pandas SQL
# Set directories
script_dir= os.path.dirname(os.path.abspath(__file__))
project_dir=os.path.dirname(script_dir)
data_dir=os.path.join(project_dir,'data')

df = data_reader(CO2_data, 30)
#print(df.columns)  #Checked the names of the columns
 #Query using pandasql - se på CO2
print('\n--- SQL Query Example: Top 10 rows where Year = 2020 ---')
query = """
SELECT * 
FROM df
WHERE Year = 2020
  AND Pollutant_name = 'CO2'
LIMIT 10
"""
result = psql.sqldf(query, locals())
print(result)