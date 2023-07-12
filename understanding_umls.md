## UMLS MySQL Walk Through

# RegEx MySQL Table -> Markdown Table
1. Replace: `\+(-)+` With: `\|--`
2. Replace: `^\|( )*` With: Nothing
3. Replace: `--\+$` With: `--`
4. Replace: `( )+` With: ` `


# Tables
```
mysql> show tables;
```

Tables_in_umls |
--|
AMBIGLUI |
AMBIGSUI |
DELETEDCUI |
DELETEDLUI |
DELETEDSUI |
MERGEDCUI |
MERGEDLUI |
MRAUI |
MRCOLS |
MRCONSO |
MRCUI |
MRDEF |
MRDOC |
MRFILES |
MRHIER |
MRHIST |
MRMAP |
MRRANK |
MRREL |
MRSAB |
MRSAT |
MRSMAP |
MRSTY |
MRXNS_ENG |
MRXNW_ENG |
MRXW_BAQ |
MRXW_CHI |
MRXW_CZE |
MRXW_DAN |
MRXW_DUT |
MRXW_ENG |
MRXW_EST |
MRXW_FIN |
MRXW_FRE |
MRXW_GER |
MRXW_GRE |
MRXW_HEB |
MRXW_HUN |
MRXW_ITA |
MRXW_JPN |
MRXW_KOR |
MRXW_LAV |
MRXW_NOR |
MRXW_POL |
MRXW_POR |
MRXW_RUS |
MRXW_SCR |
MRXW_SPA |
MRXW_SWE |
MRXW_TUR |

```
mysql> select * from MRCUI limit 10;
```
CUI1 | VER | REL | RELA | MAPREASON | CUI2 | MAPIN |
--|--|--|--|--|--|--
C0000002 | 2000AC | SY | NULL | NULL | C0007404 | Y |
C0000003 | 1999AA | SY | NULL | NULL | C0010504 | Y |
C0000024 | 1993AA | SY | NULL | NULL | C0043791 | Y |
C0000105 | 1995AA | SY | NULL | NULL | C0001964 | Y |
C0000136 | 1993AA | DEL | NULL | NULL | NULL | NULL |
C0000140 | 1993AA | DEL | NULL | NULL | NULL | NULL |
C0000158 | 1993AA | DEL | NULL | NULL | NULL | NULL |
C0000164 | 2003AB | RO | NULL | NULL | C0000163 | Y |
C0000177 | 1993AA | SY | NULL | NULL | C0014924 | Y |
C0000219 | 1993AA | DEL | NULL | NULL | NULL | NULL |

```
mysql> select * from MRCOLS;
```

COL | DES | REF | MIN | AV | MAX | FIL | DTY |
--|--|--|--|--|--|--|--
ATNL | Attribute name list for a source. | NULL | 0 | 69.84 | 1178 | MRSAB.RRF | varchar(4000) |
ATN | Attribute name | NULL | 2 | 10.38 | 62 | MRSAT.RRF | varchar(100) |
ATUI | Unique identifier for attribute. | NULL | 10 | 10.64 | 11 | MRSTY.RRF | varchar(11) |
ATUI | Unique identifier for attribute. | NULL | 10 | 10.85 | 11 | MRSAT.RRF | varchar(11) |
ATUI | Unique identifier for attribute. | NULL | 10 | 10.86 | 11 | MRDEF.RRF | varchar(11) |
ATV | Attribute value | NULL | 1 | 12.69 | 35985 | MRSAT.RRF | varchar(65000) |
AUI1 | Unique identifier for first atom | NULL | 0 | 8.52 | 9 | MRREL.RRF | varchar(9) |
AUI1 | Unique identifier for first atom | NULL | 8 | 8.54 | 9 | MRAUI.RRF | varchar(9) |
AUI2 | Unique identifier for second atom | NULL | 0 | 8.52 | 9 | MRREL.RRF | varchar(9) |
AUI2 | Unique identifier for second atom | NULL | 8 | 8.54 | 9 | MRAUI.RRF | varchar(9) |
AUI | Unique identifier for atom | NULL | 8 | 8.58 | 9 | MRHIER.RRF | varchar(9) |
AUI | Unique identifier for atom | NULL | 8 | 8.74 | 9 | MRDEF.RRF | varchar(9) |
AUI | Unique identifier for atom | NULL | 8 | 8.77 | 9 | MRCONSO.RRF | varchar(9) |
AV | Average Length, Characters | NULL | 4 | 4.12 | 6 | MRCOLS.RRF | numeric(5,2) |
BTS | Size in Bytes | NULL | 1 | 7.19 | 10 | MRFILES.RRF | integer |
CENC | Character encoding of a source as specified by IANA | NULL | 5 | 5.00 | 5 | MRSAB.RRF | varchar(20) |
CFR | CUI frequency for a source | NULL | 1 | 4.18 | 6 | MRSAB.RRF | integer |
CHANGEKEY | CONCEPTSTATUS (if history relates to a SNOMED CT concept) or DESCRIPTIONSTATUS (if history relates to a SNOMED CT atom or "description") | NULL | 0 | 0.00 | 0 | MRHIST.RRF | varchar(1000) |
CHANGETYPE | Source asserted code for type of change | NULL | 0 | 0.00 | 0 | MRHIST.RRF | varchar(1000) |
CHANGEVAL | SNOMED CT CONCEPTSTATUS or DESCRIPTIONSTATUS value after the change took place | NULL | 0 | 0.00 | 0 | MRHIST.RRF | varchar(1000) |
CLS | Number of columns | NULL | 1 | 1.12 | 2 | MRFILES.RRF | integer |
CODE | Unique Identifier or code for string in source | NULL | 0 | 4.46 | 56 | MRSAT.RRF | varchar(100) |
CODE | Unique Identifier or code for string in source | NULL | 1 | 7.50 | 95 | MRCONSO.RRF | varchar(100) |
COL | Column or data element name | NULL | 2 | 3.71 | 11 | MRCOLS.RRF | varchar(20) |
CUI1 | Unique identifier for first concept | NULL | 8 | 8.00 | 8 | MRAUI.RRF | char(8) |
CUI1 | Unique identifier for first concept | NULL | 8 | 8.00 | 8 | MRCUI.RRF | char(8) |
CUI1 | Unique identifier for first concept | NULL | 8 | 8.00 | 8 | MRREL.RRF | char(8) |
CUI2 | Unique identifier for second concept | NULL | 0 | 3.33 | 8 | MRCUI.RRF | char(8) |
CUI2 | Unique identifier for second concept | NULL | 8 | 8.00 | 8 | MRAUI.RRF | char(8) |
CUI2 | Unique identifier for second concept | NULL | 8 | 8.00 | 8 | MRREL.RRF | char(8) |
CUI | Unique identifier for concept | NULL | 0 | 0.00 | 0 | MRHIST.RRF | char(8) |
CUI | Unique identifier for concept | NULL | 8 | 8.00 | 8 | AMBIGLUI.RRF | char(8) |
CUI | Unique identifier for concept | NULL | 8 | 8.00 | 8 | AMBIGSUI.RRF | char(8) |
CUI | Unique identifier for concept | NULL | 8 | 8.00 | 8 | CHANGE/MERGEDCUI.RRF | char(8) |
CUI | Unique identifier for concept | NULL | 8 | 8.00 | 8 | MRCONSO.RRF | char(8) |
CUI | Unique identifier for concept | NULL | 8 | 8.00 | 8 | MRDEF.RRF | char(8) |
CUI | Unique identifier for concept | NULL | 8 | 8.00 | 8 | MRHIER.RRF | char(8) |
CUI | Unique identifier for concept | NULL | 8 | 8.00 | 8 | MRSAT.RRF | char(8) |
CUI | Unique identifier for concept | NULL | 8 | 8.00 | 8 | MRSTY.RRF | char(8) |
CUI | Unique identifier for concept | NULL | 8 | 8.00 | 8 | MRXNS_ENG.RRF | char(8) |
CUI | Unique identifier for concept | NULL | 8 | 8.00 | 8 | MRXNW_ENG.RRF | char(8) |
CUI | Unique identifier for concept | NULL | 8 | 8.00 | 8 | MRXW_ARA.RRF | char(8) |
CUI | Unique identifier for concept | NULL | 8 | 8.00 | 8 | MRXW_BAQ.RRF | char(8) |
CUI | Unique identifier for concept | NULL | 8 | 8.00 | 8 | MRXW_CHI.RRF | char(8) |
CUI | Unique identifier for concept | NULL | 8 | 8.00 | 8 | MRXW_CZE.RRF | char(8) |
CUI | Unique identifier for concept | NULL | 8 | 8.00 | 8 | MRXW_DAN.RRF | char(8) |
CUI | Unique identifier for concept | NULL | 8 | 8.00 | 8 | MRXW_DUT.RRF | char(8) |
CUI | Unique identifier for concept | NULL | 8 | 8.00 | 8 | MRXW_ENG.RRF | char(8) |
CUI | Unique identifier for concept | NULL | 8 | 8.00 | 8 | MRXW_EST.RRF | char(8) |
CUI | Unique identifier for concept | NULL | 8 | 8.00 | 8 | MRXW_FIN.RRF | char(8) |
CUI | Unique identifier for concept | NULL | 8 | 8.00 | 8 | MRXW_FRE.RRF | char(8) |
CUI | Unique identifier for concept | NULL | 8 | 8.00 | 8 | MRXW_GER.RRF | char(8) |
CUI | Unique identifier for concept | NULL | 8 | 8.00 | 8 | MRXW_GRE.RRF | char(8) |
CUI | Unique identifier for concept | NULL | 8 | 8.00 | 8 | MRXW_HEB.RRF | char(8) |
CUI | Unique identifier for concept | NULL | 8 | 8.00 | 8 | MRXW_HUN.RRF | char(8) |
CUI | Unique identifier for concept | NULL | 8 | 8.00 | 8 | MRXW_ITA.RRF | char(8) |
CUI | Unique identifier for concept | NULL | 8 | 8.00 | 8 | MRXW_JPN.RRF | char(8) |
CUI | Unique identifier for concept | NULL | 8 | 8.00 | 8 | MRXW_KOR.RRF | char(8) |
CUI | Unique identifier for concept | NULL | 8 | 8.00 | 8 | MRXW_LAV.RRF | char(8) |
CUI | Unique identifier for concept | NULL | 8 | 8.00 | 8 | MRXW_NOR.RRF | char(8) |
CUI | Unique identifier for concept | NULL | 8 | 8.00 | 8 | MRXW_POL.RRF | char(8) |
CUI | Unique identifier for concept | NULL | 8 | 8.00 | 8 | MRXW_POR.RRF | char(8) |
CUI | Unique identifier for concept | NULL | 8 | 8.00 | 8 | MRXW_RUS.RRF | char(8) |
CUI | Unique identifier for concept | NULL | 8 | 8.00 | 8 | MRXW_SCR.RRF | char(8) |
CUI | Unique identifier for concept | NULL | 8 | 8.00 | 8 | MRXW_SPA.RRF | char(8) |
CUI | Unique identifier for concept | NULL | 8 | 8.00 | 8 | MRXW_SWE.RRF | char(8) |
CUI | Unique identifier for concept | NULL | 8 | 8.00 | 8 | MRXW_TUR.RRF | char(8) |
CUI | Unique identifier for concept | NULL | 8 | 8.00 | 8 | MRXW_UKR.RRF | char(8) |
CURVER | Current Version flag | NULL | 1 | 1.00 | 1 | MRSAB.RRF | char(1) |
CVF | Content view flag | NULL | 0 | 0.00 | 0 | MRDEF.RRF | varchar(50) |
CVF | Content view flag | NULL | 0 | 0.00 | 0 | MRHIER.RRF | varchar(50) |
CVF | Content view flag | NULL | 0 | 0.00 | 0 | MRHIST.RRF | varchar(50) |
CVF | Content view flag | NULL | 0 | 0.00 | 0 | MRMAP.RRF | varchar(50) |
CVF | Content view flag | NULL | 0 | 0.00 | 0 | MRREL.RRF | varchar(50) |
CVF | Content view flag | NULL | 0 | 0.00 | 0 | MRSAT.RRF | varchar(50) |
CVF | Content view flag | NULL | 0 | 0.00 | 0 | MRSMAP.RRF | varchar(50) |
CVF | Content view flag | NULL | 0 | 1.22 | 5 | MRCONSO.RRF | varchar(50) |
CVF | Content view flag | NULL | 0 | 2.13 | 5 | MRSTY.RRF | varchar(50) |
CXN | The context number if the atom has multiple contexts | NULL | 1 | 2.17 | 5 | MRHIER.RRF | integer |
CXTY | Context type for a source | NULL | 0 | 5.14 | 13 | MRSAB.RRF | varchar(50) |
DEF | Definition | NULL | 1 | 232.23 | 10939 | MRDEF.RRF | varchar(16000) |
DES | Descriptive Name | NULL | 5 | 28.81 | 136 | MRCOLS.RRF | varchar(200) |
DES | Descriptive Name | NULL | 8 | 18.25 | 42 | MRFILES.RRF | varchar(200) |
DIR | Source asserted directionality flag | NULL | 0 | 0.13 | 1 | MRREL.RRF | varchar(1) |
DOCKEY | Key to be documented | NULL | 2 | 3.65 | 8 | MRDOC.RRF | varchar(50) |
DTY | SQL-92 data type for this column | NULL | 7 | 10.02 | 14 | MRCOLS.RRF | varchar(20) |
EXPL | Detailed explanation | NULL | 0 | 26.57 | 941 | MRDOC.RRF | varchar(1000) |
FIL | Physical FILENAME | NULL | 9 | 10.99 | 21 | MRCOLS.RRF | varchar(50) |
FIL | Physical FILENAME | NULL | 9 | 12.12 | 21 | MRFILES.RRF | varchar(50) |
FMT | Comma separated list of COL | NULL | 7 | 29.69 | 190 | MRFILES.RRF | varchar(300) |
FROMEXPR | The expression that a mapping is mapped from | NULL | 1 | 6.93 | 9 | MRSMAP.RRF | varchar(4000) |
FROMEXPR | The expression that a mapping is mapped from | NULL | 1 | 8.29 | 18 | MRMAP.RRF | varchar(4000) |
FROMID | Metathesaurus identifier for the entity being mapped from | NULL | 1 | 7.31 | 18 | MRMAP.RRF | varchar(50) |
FROMRES | Restriction applicable to the entity being mapped from | NULL | 0 | 0.00 | 0 | MRMAP.RRF | varchar(4000) |
FROMRULE | Machine processible rule applicable to the entity being mapped from | NULL | 0 | 0.00 | 0 | MRMAP.RRF | varchar(4000) |
FROMSID | Source asserted identifier for the entity being mapped from | NULL | 0 | 0.00 | 0 | MRMAP.RRF | varchar(50) |
FROMTYPE | The type of expression that a mapping is mapped from | NULL | 3 | 3.98 | 4 | MRSMAP.RRF | varchar(50) |
FROMTYPE | The type of expression that a mapping is mapped from | NULL | 3 | 3.99 | 4 | MRMAP.RRF | varchar(50) |
HCD | Source asserted hierarchical number or code of context member (if it exists) | NULL | 0 | 0.48 | 51 | MRHIER.RRF | varchar(100) |
IMETA | Version of the Metathesaurus that a source was added | NULL | 6 | 6.00 | 6 | MRSAB.RRF | varchar(10) |
ISPREF | Indicates whether AUI is preferred | NULL | 1 | 1.00 | 1 | MRCONSO.RRF | char(1) |
LAT | Language of Term(s) | NULL | 0 | 0.00 | 0 | CHANGE/DELETEDSUI.RRF | char(3) |
LAT | Language of Term(s) | NULL | 0 | 2.97 | 3 | MRSAB.RRF | char(3) |
LAT | Language of Term(s) | NULL | 3 | 3.00 | 3 | MRCONSO.RRF | char(3) |
LAT | Language of Term(s) | NULL | 3 | 3.00 | 3 | MRXNS_ENG.RRF | char(3) |
LAT | Language of Term(s) | NULL | 3 | 3.00 | 3 | MRXNW_ENG.RRF | char(3) |
LAT | Language of Term(s) | NULL | 3 | 3.00 | 3 | MRXW_ARA.RRF | char(3) |
LAT | Language of Term(s) | NULL | 3 | 3.00 | 3 | MRXW_BAQ.RRF | char(3) |
LAT | Language of Term(s) | NULL | 3 | 3.00 | 3 | MRXW_CHI.RRF | char(3) |
LAT | Language of Term(s) | NULL | 3 | 3.00 | 3 | MRXW_CZE.RRF | char(3) |
LAT | Language of Term(s) | NULL | 3 | 3.00 | 3 | MRXW_DAN.RRF | char(3) |
LAT | Language of Term(s) | NULL | 3 | 3.00 | 3 | MRXW_DUT.RRF | char(3) |
LAT | Language of Term(s) | NULL | 3 | 3.00 | 3 | MRXW_ENG.RRF | char(3) |
LAT | Language of Term(s) | NULL | 3 | 3.00 | 3 | MRXW_EST.RRF | char(3) |
LAT | Language of Term(s) | NULL | 3 | 3.00 | 3 | MRXW_FIN.RRF | char(3) |
LAT | Language of Term(s) | NULL | 3 | 3.00 | 3 | MRXW_FRE.RRF | char(3) |
LAT | Language of Term(s) | NULL | 3 | 3.00 | 3 | MRXW_GER.RRF | char(3) |
LAT | Language of Term(s) | NULL | 3 | 3.00 | 3 | MRXW_GRE.RRF | char(3) |
LAT | Language of Term(s) | NULL | 3 | 3.00 | 3 | MRXW_HEB.RRF | char(3) |
LAT | Language of Term(s) | NULL | 3 | 3.00 | 3 | MRXW_HUN.RRF | char(3) |
LAT | Language of Term(s) | NULL | 3 | 3.00 | 3 | MRXW_ITA.RRF | char(3) |
LAT | Language of Term(s) | NULL | 3 | 3.00 | 3 | MRXW_JPN.RRF | char(3) |
LAT | Language of Term(s) | NULL | 3 | 3.00 | 3 | MRXW_KOR.RRF | char(3) |
LAT | Language of Term(s) | NULL | 3 | 3.00 | 3 | MRXW_LAV.RRF | char(3) |
LAT | Language of Term(s) | NULL | 3 | 3.00 | 3 | MRXW_NOR.RRF | char(3) |
LAT | Language of Term(s) | NULL | 3 | 3.00 | 3 | MRXW_POL.RRF | char(3) |
LAT | Language of Term(s) | NULL | 3 | 3.00 | 3 | MRXW_POR.RRF | char(3) |
LAT | Language of Term(s) | NULL | 3 | 3.00 | 3 | MRXW_RUS.RRF | char(3) |
LAT | Language of Term(s) | NULL | 3 | 3.00 | 3 | MRXW_SCR.RRF | char(3) |
LAT | Language of Term(s) | NULL | 3 | 3.00 | 3 | MRXW_SPA.RRF | char(3) |
LAT | Language of Term(s) | NULL | 3 | 3.00 | 3 | MRXW_SWE.RRF | char(3) |
LAT | Language of Term(s) | NULL | 3 | 3.00 | 3 | MRXW_TUR.RRF | char(3) |
LAT | Language of Term(s) | NULL | 3 | 3.00 | 3 | MRXW_UKR.RRF | char(3) |
LUI | Unique identifier for term | NULL | 0 | 0.00 | 0 | CHANGE/MERGEDLUI.RRF | varchar(10) |
LUI | Unique identifier for term | NULL | 0 | 4.50 | 9 | MRSAT.RRF | varchar(10) |
LUI | Unique identifier for term | NULL | 8 | 8.00 | 8 | MRXW_BAQ.RRF | varchar(10) |
LUI | Unique identifier for term | NULL | 8 | 8.00 | 8 | MRXW_DAN.RRF | varchar(10) |
LUI | Unique identifier for term | NULL | 8 | 8.00 | 8 | MRXW_FIN.RRF | varchar(10) |
LUI | Unique identifier for term | NULL | 8 | 8.00 | 8 | MRXW_HEB.RRF | varchar(10) |
LUI | Unique identifier for term | NULL | 8 | 8.17 | 9 | MRXW_SCR.RRF | varchar(10) |
LUI | Unique identifier for term | NULL | 8 | 8.20 | 9 | MRXW_JPN.RRF | varchar(10) |
LUI | Unique identifier for term | NULL | 8 | 8.22 | 9 | AMBIGLUI.RRF | varchar(10) |
LUI | Unique identifier for term | NULL | 8 | 8.43 | 9 | MRXW_ENG.RRF | varchar(10) |
LUI | Unique identifier for term | NULL | 8 | 8.44 | 9 | MRCONSO.RRF | varchar(10) |
LUI | Unique identifier for term | NULL | 8 | 8.44 | 9 | MRXNS_ENG.RRF | varchar(10) |
LUI | Unique identifier for term | NULL | 8 | 8.44 | 9 | MRXNW_ENG.RRF | varchar(10) |
LUI | Unique identifier for term | NULL | 8 | 8.48 | 9 | MRXW_CZE.RRF | varchar(10) |
LUI | Unique identifier for term | NULL | 8 | 8.52 | 9 | MRXW_DUT.RRF | varchar(10) |
LUI | Unique identifier for term | NULL | 8 | 8.58 | 9 | MRXW_GER.RRF | varchar(10) |
LUI | Unique identifier for term | NULL | 8 | 8.67 | 9 | MRXW_SPA.RRF | varchar(10) |
LUI | Unique identifier for term | NULL | 8 | 8.77 | 9 | MRXW_POR.RRF | varchar(10) |
LUI | Unique identifier for term | NULL | 8 | 8.77 | 9 | MRXW_RUS.RRF | varchar(10) |
LUI | Unique identifier for term | NULL | 8 | 8.78 | 9 | MRXW_ITA.RRF | varchar(10) |
LUI | Unique identifier for term | NULL | 8 | 8.78 | 9 | MRXW_POL.RRF | varchar(10) |
LUI | Unique identifier for term | NULL | 8 | 8.80 | 9 | MRXW_FRE.RRF | varchar(10) |
LUI | Unique identifier for term | NULL | 8 | 8.82 | 9 | MRXW_SWE.RRF | varchar(10) |
LUI | Unique identifier for term | NULL | 8 | 8.90 | 9 | MRXW_KOR.RRF | varchar(10) |
LUI | Unique identifier for term | NULL | 8 | 8.98 | 9 | MRXW_NOR.RRF | varchar(10) |
LUI | Unique identifier for term | NULL | 8 | 8.99 | 9 | MRXW_HUN.RRF | varchar(10) |
LUI | Unique identifier for term | NULL | 8 | 8.99 | 9 | MRXW_LAV.RRF | varchar(10) |
LUI | Unique identifier for term | NULL | 9 | 9.00 | 9 | MRXW_ARA.RRF | varchar(10) |
LUI | Unique identifier for term | NULL | 9 | 9.00 | 9 | MRXW_CHI.RRF | varchar(10) |
LUI | Unique identifier for term | NULL | 9 | 9.00 | 9 | MRXW_EST.RRF | varchar(10) |
LUI | Unique identifier for term | NULL | 9 | 9.00 | 9 | MRXW_GRE.RRF | varchar(10) |
LUI | Unique identifier for term | NULL | 9 | 9.00 | 9 | MRXW_TUR.RRF | varchar(10) |
LUI | Unique identifier for term | NULL | 9 | 9.00 | 9 | MRXW_UKR.RRF | varchar(10) |
MAPATN | Mapping attribute name (for future use) | NULL | 0 | 2.82 | 6 | MRMAP.RRF | varchar(20) |
MAPATV | Mapping attribute value (for future use) | NULL | 0 | 0.00 | 1 | MRMAP.RRF | varchar(4000) |
MAPID | Metathesaurus asserted identifier for mapping | NULL | 10 | 10.98 | 11 | MRSMAP.RRF | varchar(50) |
MAPID | Metathesaurus asserted identifier for mapping | NULL | 10 | 10.99 | 11 | MRMAP.RRF | varchar(50) |
MAPIN | Mapping in current subset | NULL | 0 | 0.42 | 1 | MRCUI.RRF | char(1) |
MAPIN | Mapping in current subset | NULL | 1 | 1.00 | 1 | MRAUI.RRF | char(1) |
MAPRANK | Order in which mappings in a subset should be applied | NULL | 0 | 0.49 | 2 | MRMAP.RRF | integer |
MAPREASON | Reason for mapping | NULL | 0 | 0.00 | 4 | MRCUI.RRF | varchar(4000) |
MAPREASON | Reason for mapping | NULL | 4 | 4.00 | 4 | MRAUI.RRF | varchar(4000) |
MAPRES | Restriction applicable to this mapping | NULL | 0 | 34.78 | 429 | MRMAP.RRF | varchar(4000) |
MAPRULE | Machine processible rule applicable to this mapping | NULL | 0 | 9.57 | 336 | MRMAP.RRF | varchar(4000) |
MAPSETCUI | CUI of the map set | NULL | 8 | 8.00 | 8 | MRMAP.RRF | char(8) |
MAPSETCUI | CUI of the map set | NULL | 8 | 8.00 | 8 | MRSMAP.RRF | char(8) |
MAPSETSAB | SAB of the map set | NULL | 3 | 10.60 | 13 | MRSMAP.RRF | varchar(40) |
MAPSETSAB | SAB of the map set | NULL | 3 | 10.71 | 13 | MRMAP.RRF | varchar(40) |
MAPSID | Source asserted identifier for mapping | NULL | 0 | 0.00 | 0 | MRSMAP.RRF | varchar(50) |
MAPSID | Source asserted identifier for mapping | NULL | 0 | 0.01 | 36 | MRMAP.RRF | varchar(50) |
MAPSUBSETID | Map subset identifier used to identify a subset of related mappings within a map set | NULL | 0 | 0.49 | 1 | MRMAP.RRF | varchar(10) |
MAPTYPE | Type of mapping | NULL | 0 | 4.26 | 9 | MRMAP.RRF | varchar(50) |
MAX | Maximum Length | NULL | 1 | 1.37 | 5 | MRCOLS.RRF | integer |
METAUI | Metathesaurus asserted unique identifier | NULL | 0 | 7.85 | 10 | MRSAT.RRF | varchar(50) |
MIN | Minimum Length | NULL | 1 | 1.02 | 2 | MRCOLS.RRF | integer |
NSTR | Normalized string | NULL | 1 | 38.86 | 2460 | MRXNS_ENG.RRF | varchar(3000) |
NWD | Normalized word | NULL | 1 | 6.55 | 80 | MRXNW_ENG.RRF | varchar(100) |
PAUI | Unique identifier for parent atom | NULL | 0 | 8.46 | 9 | MRHIER.RRF | varchar(9) |
PCUI | Concept unique identifier in the previous Metathesaurus | NULL | 8 | 8.00 | 8 | CHANGE/DELETEDCUI.RRF | char(8) |
PCUI | Concept unique identifier in the previous Metathesaurus | NULL | 8 | 8.00 | 8 | CHANGE/MERGEDCUI.RRF | char(8) |
PLUI | Lexical unique identifier in the previous Metathesaurus | NULL | 0 | 0.00 | 0 | CHANGE/DELETEDLUI.RRF | varchar(10) |
PLUI | Lexical unique identifier in the previous Metathesaurus | NULL | 0 | 0.00 | 0 | CHANGE/MERGEDLUI.RRF | varchar(10) |
PSTR | Preferred name in the previous Metathesaurus | NULL | 0 | 0.00 | 0 | CHANGE/DELETEDLUI.RRF | varchar(3000) |
PSTR | Preferred name in the previous Metathesaurus | NULL | 0 | 0.00 | 0 | CHANGE/DELETEDSUI.RRF | varchar(3000) |
PSTR | Preferred name in the previous Metathesaurus | NULL | 4 | 4.00 | 4 | CHANGE/DELETEDCUI.RRF | varchar(3000) |
PSUI | String unique identifier in the previous Metathesaurus | NULL | 0 | 0.00 | 0 | CHANGE/DELETEDSUI.RRF | varchar(10) |
PTR | Path to root | NULL | 0 | 103.81 | 345 | MRHIER.RRF | varchar(1000) |
RANK | Termgroup ranking | NULL | 4 | 4.00 | 4 | MRRANK.RRF | integer |
RCUI | Unique identifier for root SRC concept | NULL | 8 | 8.00 | 8 | MRSAB.RRF | char(8) |
REASON | Explanation of change, if present | NULL | 0 | 0.00 | 0 | MRHIST.RRF | varchar(1000) |
REF | Documentation Section Number | NULL | 0 | 0.00 | 0 | MRCOLS.RRF | varchar(20) |
RELA | Additional relationship label | NULL | 0 | 0.00 | 0 | MRAUI.RRF | varchar(100) |
RELA | Additional relationship label | NULL | 0 | 0.00 | 0 | MRCUI.RRF | varchar(100) |
RELA | Additional relationship label | NULL | 0 | 10.69 | 54 | MRREL.RRF | varchar(100) |
RELA | Additional relationship label | NULL | 0 | 14.07 | 37 | MRMAP.RRF | varchar(100) |
RELA | Additional relationship label | NULL | 0 | 19.91 | 37 | MRSMAP.RRF | varchar(100) |
RELA | Additional relationship label | NULL | 0 | 2.71 | 12 | MRHIER.RRF | varchar(100) |
REL | Relationship label | NULL | 0 | 0.00 | 0 | MRAUI.RRF | varchar(4) |
REL | Relationship label | NULL | 2 | 2.00 | 2 | MRMAP.RRF | varchar(4) |
REL | Relationship label | NULL | 2 | 2.00 | 2 | MRSMAP.RRF | varchar(4) |
REL | Relationship label | NULL | 2 | 2.24 | 3 | MRREL.RRF | varchar(4) |
REL | Relationship label | NULL | 2 | 2.65 | 4 | MRCUI.RRF | varchar(4) |
RG | Relationship group | NULL | 0 | 0.06 | 2 | MRREL.RRF | varchar(10) |
RMETA | Version of the Metathesaurus where a version is removed | NULL | 0 | 0.09 | 6 | MRSAB.RRF | varchar(10) |
RSAB | Root source abbreviation | NULL | 2 | 5.94 | 15 | MRSAB.RRF | varchar(40) |
RUI | Unique identifier for relationship | NULL | 9 | 9.82 | 10 | MRREL.RRF | varchar(10) |
RWS | Number of rows | NULL | 1 | 5.56 | 8 | MRFILES.RRF | integer |
SABIN | Source in current subset | NULL | 1 | 1.00 | 1 | MRSAB.RRF | char(1) |
SAB | Source abbreviation | NULL | 0 | 0.00 | 0 | MRHIST.RRF | varchar(40) |
SAB | Source abbreviation | NULL | 2 | 4.12 | 11 | MRDEF.RRF | varchar(40) |
SAB | Source abbreviation | NULL | 2 | 5.31 | 15 | MRRANK.RRF | varchar(40) |
SAB | Source abbreviation | NULL | 2 | 5.48 | 15 | MRREL.RRF | varchar(40) |
SAB | Source abbreviation | NULL | 2 | 5.70 | 15 | MRCONSO.RRF | varchar(40) |
SAB | Source abbreviation | NULL | 2 | 5.75 | 13 | MRSAT.RRF | varchar(40) |
SAB | Source abbreviation | NULL | 2 | 7.90 | 13 | MRHIER.RRF | varchar(40) |
SATUI | Source asserted attribute identifier | NULL | 0 | 0.47 | 16 | MRDEF.RRF | varchar(50) |
SATUI | Source asserted attribute identifier | NULL | 0 | 3.24 | 36 | MRSAT.RRF | varchar(50) |
SAUI | Source asserted atom identifier | NULL | 0 | 1.73 | 18 | MRCONSO.RRF | varchar(100) |
SCC | Content contact info for a source | NULL | 0 | 152.05 | 332 | MRSAB.RRF | varchar(1000) |
SCIT | Source citation | NULL | 54 | 164.09 | 674 | MRSAB.RRF | varchar(4000) |
SCUI | Source asserted concept identifier | NULL | 0 | 5.28 | 95 | MRCONSO.RRF | varchar(100) |
SDUI | Source asserted descriptor identifier | NULL | 0 | 2.73 | 13 | MRCONSO.RRF | varchar(100) |
SF | Source Family | NULL | 2 | 4.20 | 13 | MRSAB.RRF | varchar(40) |
SLC | License contact info for a source | NULL | 12 | 167.35 | 346 | MRSAB.RRF | varchar(1000) |
SL | Source of relationship labels | NULL | 2 | 5.48 | 15 | MRREL.RRF | varchar(40) |
SON | Source Official Name | NULL | 10 | 48.65 | 145 | MRSAB.RRF | varchar(3000) |
SOURCEUI | Source asserted unique identifier | NULL | 0 | 0.00 | 0 | MRHIST.RRF | varchar(50) |
SRL | Source Restriction Level | NULL | 1 | 1.00 | 1 | MRCONSO.RRF | integer |
SRL | Source Restriction Level | NULL | 1 | 1.00 | 1 | MRSAB.RRF | integer |
SRUI | Source attributed relationship identifier | NULL | 0 | 1.20 | 36 | MRREL.RRF | varchar(50) |
SSN | Source short name | NULL | 3 | 26.96 | 89 | MRSAB.RRF | varchar(3000) |
STN | Semantic type tree number | NULL | 1 | 7.85 | 14 | MRSTY.RRF | varchar(100) |
STR | String | NULL | 1 | 38.20 | 2930 | MRCONSO.RRF | varchar(3000) |
STT | String type | NULL | 2 | 2.01 | 3 | MRCONSO.RRF | varchar(3) |
STYPE1 | The name of the column in MRCONSO.RRF that contains the first identifier to which the relationship is attached | NULL | 3 | 3.62 | 4 | MRREL.RRF | varchar(50) |
STYPE2 | The name of the column in MRCONSO.RRF that contains the second identifier to which the relationship is attached | NULL | 3 | 3.62 | 4 | MRREL.RRF | varchar(50) |
STYPE | The name of the column in MRCONSO.RRF or MRREL.RRF that contains the identifier to which the attribute is attached | NULL | 3 | 3.25 | 4 | MRSAT.RRF | varchar(50) |
STY | Semantic type | NULL | 4 | 17.65 | 39 | MRSTY.RRF | varchar(50) |
SUI | Unique identifier for string | NULL | 0 | 4.57 | 9 | MRSAT.RRF | varchar(10) |
SUI | Unique identifier for string | NULL | 8 | 8.00 | 8 | MRXW_BAQ.RRF | varchar(10) |
SUI | Unique identifier for string | NULL | 8 | 8.00 | 8 | MRXW_DAN.RRF | varchar(10) |
SUI | Unique identifier for string | NULL | 8 | 8.00 | 8 | MRXW_FIN.RRF | varchar(10) |
SUI | Unique identifier for string | NULL | 8 | 8.00 | 8 | MRXW_HEB.RRF | varchar(10) |
SUI | Unique identifier for string | NULL | 8 | 8.35 | 9 | AMBIGSUI.RRF | varchar(10) |
SUI | Unique identifier for string | NULL | 8 | 8.35 | 9 | MRXW_JPN.RRF | varchar(10) |
SUI | Unique identifier for string | NULL | 8 | 8.53 | 9 | MRXW_DUT.RRF | varchar(10) |
SUI | Unique identifier for string | NULL | 8 | 8.58 | 9 | MRCONSO.RRF | varchar(10) |
SUI | Unique identifier for string | NULL | 8 | 8.61 | 9 | MRXW_GER.RRF | varchar(10) |
SUI | Unique identifier for string | NULL | 8 | 8.64 | 9 | MRXNS_ENG.RRF | varchar(10) |
SUI | Unique identifier for string | NULL | 8 | 8.67 | 9 | MRXNW_ENG.RRF | varchar(10) |
SUI | Unique identifier for string | NULL | 8 | 8.67 | 9 | MRXW_ENG.RRF | varchar(10) |
SUI | Unique identifier for string | NULL | 8 | 8.71 | 9 | MRXW_SPA.RRF | varchar(10) |
SUI | Unique identifier for string | NULL | 8 | 8.79 | 9 | MRXW_POR.RRF | varchar(10) |
SUI | Unique identifier for string | NULL | 8 | 8.79 | 9 | MRXW_RUS.RRF | varchar(10) |
SUI | Unique identifier for string | NULL | 8 | 8.82 | 9 | MRXW_ITA.RRF | varchar(10) |
SUI | Unique identifier for string | NULL | 8 | 8.84 | 9 | MRXW_SWE.RRF | varchar(10) |
SUI | Unique identifier for string | NULL | 8 | 8.85 | 9 | MRXW_CZE.RRF | varchar(10) |
SUI | Unique identifier for string | NULL | 8 | 8.85 | 9 | MRXW_FRE.RRF | varchar(10) |
SUI | Unique identifier for string | NULL | 8 | 8.98 | 9 | MRXW_NOR.RRF | varchar(10) |
SUI | Unique identifier for string | NULL | 8 | 8.99 | 9 | MRXW_HUN.RRF | varchar(10) |
SUI | Unique identifier for string | NULL | 9 | 9.00 | 9 | MRXW_ARA.RRF | varchar(10) |
SUI | Unique identifier for string | NULL | 9 | 9.00 | 9 | MRXW_CHI.RRF | varchar(10) |
SUI | Unique identifier for string | NULL | 9 | 9.00 | 9 | MRXW_EST.RRF | varchar(10) |
SUI | Unique identifier for string | NULL | 9 | 9.00 | 9 | MRXW_GRE.RRF | varchar(10) |
SUI | Unique identifier for string | NULL | 9 | 9.00 | 9 | MRXW_KOR.RRF | varchar(10) |
SUI | Unique identifier for string | NULL | 9 | 9.00 | 9 | MRXW_LAV.RRF | varchar(10) |
SUI | Unique identifier for string | NULL | 9 | 9.00 | 9 | MRXW_POL.RRF | varchar(10) |
SUI | Unique identifier for string | NULL | 9 | 9.00 | 9 | MRXW_SCR.RRF | varchar(10) |
SUI | Unique identifier for string | NULL | 9 | 9.00 | 9 | MRXW_TUR.RRF | varchar(10) |
SUI | Unique identifier for string | NULL | 9 | 9.00 | 9 | MRXW_UKR.RRF | varchar(10) |
SUPPRESS | Suppressible flag | NULL | 1 | 1.00 | 1 | MRCONSO.RRF | char(1) |
SUPPRESS | Suppressible flag | NULL | 1 | 1.00 | 1 | MRDEF.RRF | char(1) |
SUPPRESS | Suppressible flag | NULL | 1 | 1.00 | 1 | MRRANK.RRF | char(1) |
SUPPRESS | Suppressible flag | NULL | 1 | 1.00 | 1 | MRREL.RRF | char(1) |
SUPPRESS | Suppressible flag | NULL | 1 | 1.00 | 1 | MRSAT.RRF | char(1) |
SVER | Release date or version number of a source | NULL | 0 | 0.00 | 0 | MRHIST.RRF | varchar(20) |
SVER | Release date or version number of a source | NULL | 0 | 5.08 | 15 | MRSAB.RRF | varchar(20) |
TFR | Term frequency for a source | NULL | 1 | 4.41 | 7 | MRSAB.RRF | integer |
TOEXPR | The expression that a mapping is mapped to | NULL | 0 | 6.03 | 242 | MRMAP.RRF | varchar(4000) |
TOEXPR | The expression that a mapping is mapped to | NULL | 1 | 6.92 | 242 | MRSMAP.RRF | varchar(4000) |
TOID | Metathesaurus identifier for the entity being mapped to | NULL | 0 | 5.18 | 18 | MRMAP.RRF | varchar(50) |
TORES | Restriction applicable to the entity being mapped to | NULL | 0 | 0.00 | 0 | MRMAP.RRF | varchar(4000) |
TORULE | Machine processible rule applicable to the entity being mapped to | NULL | 0 | 0.00 | 0 | MRMAP.RRF | varchar(4000) |
TOSID | Source asserted identifier for the entity being mapped to | NULL | 0 | 0.00 | 0 | MRMAP.RRF | varchar(50) |
TOTYPE | The type of expression that a mapping is mapped to | NULL | 0 | 3.98 | 23 | MRMAP.RRF | varchar(50) |
TOTYPE | The type of expression that a mapping is mapped to | NULL | 4 | 4.36 | 22 | MRSMAP.RRF | varchar(50) |
TS | Term status | NULL | 1 | 1.00 | 1 | MRCONSO.RRF | char(1) |
TTYL | Term type list for a source | NULL | 0 | 11.76 | 86 | MRSAB.RRF | varchar(400) |
TTY | Term type in source | NULL | 2 | 2.35 | 11 | MRCONSO.RRF | varchar(20) |
TTY | Term type in source | NULL | 2 | 2.58 | 11 | MRRANK.RRF | varchar(20) |
TUI | Unique identifier of Semantic type | NULL | 4 | 4.00 | 4 | MRSTY.RRF | char(4) |
TYPE | Type of information | NULL | 3 | 13.14 | 21 | MRDOC.RRF | varchar(50) |
VALUE | Value | NULL | 0 | 15.98 | 62 | MRDOC.RRF | varchar(200) |
VCUI | Unique identifier for versioned SRC concept | NULL | 0 | 7.71 | 8 | MRSAB.RRF | char(8) |
VEND | Valid end date for a source | NULL | 0 | 0.00 | 0 | MRSAB.RRF | char(8) |
VER | Last release version in which CUI1 was valid | NULL | 6 | 6.00 | 6 | MRAUI.RRF | varchar(10) |
VER | Last release version in which CUI1 was valid | NULL | 6 | 6.00 | 6 | MRCUI.RRF | varchar(10) |
VSAB | Versioned source abbreviation | NULL | 3 | 11.35 | 24 | MRSAB.RRF | varchar(40) |
VSTART | Valid start date for a source | NULL | 0 | 0.00 | 0 | MRSAB.RRF | char(8) |
WD | Word in lower-case | NULL | 1 | 10.53 | 54 | MRXW_FIN.RRF | varchar(500) |
WD | Word in lower-case | NULL | 1 | 2.90 | 38 | MRXW_KOR.RRF | varchar(500) |
WD | Word in lower-case | NULL | 1 | 3.65 | 68 | MRXW_CHI.RRF | varchar(500) |
WD | Word in lower-case | NULL | 1 | 4.58 | 35 | MRXW_EST.RRF | varchar(500) |
WD | Word in lower-case | NULL | 1 | 5.23 | 37 | MRXW_TUR.RRF | varchar(500) |
WD | Word in lower-case | NULL | 1 | 5.47 | 22 | MRXW_ARA.RRF | varchar(500) |
WD | Word in lower-case | NULL | 1 | 5.71 | 38 | MRXW_POR.RRF | varchar(500) |
WD | Word in lower-case | NULL | 1 | 5.91 | 38 | MRXW_ITA.RRF | varchar(500) |
WD | Word in lower-case | NULL | 1 | 6.12 | 19 | MRXW_HEB.RRF | varchar(500) |
WD | Word in lower-case | NULL | 1 | 6.13 | 24 | MRXW_UKR.RRF | varchar(500) |
WD | Word in lower-case | NULL | 1 | 6.23 | 80 | MRXW_ENG.RRF | varchar(500) |
WD | Word in lower-case | NULL | 1 | 6.38 | 25 | MRXW_DAN.RRF | varchar(500) |
WD | Word in lower-case | NULL | 1 | 6.67 | 46 | MRXW_SPA.RRF | varchar(500) |
WD | Word in lower-case | NULL | 1 | 6.83 | 39 | MRXW_FRE.RRF | varchar(500) |
WD | Word in lower-case | NULL | 1 | 7.14 | 40 | MRXW_RUS.RRF | varchar(500) |
WD | Word in lower-case | NULL | 1 | 7.17 | 18 | MRXW_BAQ.RRF | varchar(500) |
WD | Word in lower-case | NULL | 1 | 7.50 | 34 | MRXW_GRE.RRF | varchar(500) |
WD | Word in lower-case | NULL | 1 | 7.55 | 48 | MRXW_POL.RRF | varchar(500) |
WD | Word in lower-case | NULL | 1 | 7.57 | 52 | MRXW_CZE.RRF | varchar(500) |
WD | Word in lower-case | NULL | 1 | 7.89 | 51 | MRXW_DUT.RRF | varchar(500) |
WD | Word in lower-case | NULL | 1 | 7.97 | 27 | MRXW_HUN.RRF | varchar(500) |
WD | Word in lower-case | NULL | 1 | 7.98 | 29 | MRXW_LAV.RRF | varchar(500) |
WD | Word in lower-case | NULL | 1 | 8.02 | 37 | MRXW_SCR.RRF | varchar(500) |
WD | Word in lower-case | NULL | 1 | 8.37 | 41 | MRXW_GER.RRF | varchar(500) |
WD | Word in lower-case | NULL | 1 | 8.61 | 39 | MRXW_SWE.RRF | varchar(500) |
WD | Word in lower-case | NULL | 1 | 8.91 | 85 | MRXW_JPN.RRF | varchar(500) |
WD | Word in lower-case | NULL | 1 | 9.11 | 44 | MRXW_NOR.RRF | varchar(500) |

```
mysql> select * from MRREL limit 10;
```
CUI1 | AUI1 | STYPE1 | REL | CUI2 | AUI2 | STYPE2 | RELA | RUI | SRUI | SAB | SL | RG | DIR | SUPPRESS | CVF |
--|--|--|--|--|--|--|--|--|--|--|--|--|--|--|--
C0236642 | A0001895 | AUI | RB | C0270715 | A1389616 | AUI | NULL | R00689636 | NULL | AOD | AOD | NULL | NULL | N | NULL |
C0003787 | A0002112 | AUI | RB | C0037728 | A1397168 | AUI | NULL | R00689637 | NULL | AOD | AOD | NULL | NULL | N | NULL |
C0018090 | A0002644 | AUI | RB | C0032636 | A0103514 | AUI | NULL | R00689638 | NULL | AOD | AOD | NULL | NULL | N | NULL |
C0039194 | A0003844 | AUI | RB | C0024264 | A0483067 | AUI | NULL | R00689639 | NULL | AOD | AOD | NULL | NULL | N | NULL |
C0004561 | A0003849 | AUI | RB | C0024264 | A0483067 | AUI | NULL | R00689640 | NULL | AOD | AOD | NULL | NULL | N | NULL |
C0022801 | A0006210 | AUI | RB | C0035287 | A0488404 | AUI | NULL | R00689641 | NULL | AOD | AOD | NULL | NULL | N | NULL |
C0022801 | A0006210 | AUI | RB | C0227525 | A1182577 | AUI | NULL | R00689642 | NULL | AOD | AOD | NULL | NULL | N | NULL |
C0022801 | A0006210 | AUI | RB | C0449475 | A1182637 | AUI | NULL | R00689643 | NULL | AOD | AOD | NULL | NULL | N | NULL |
C0034143 | A0006342 | AUI | RB | C0682702 | A1389183 | AUI | NULL | R00689644 | NULL | AOD | AOD | NULL | NULL | N | NULL |
C0221406 | A0009638 | AUI | RB | C0020635 | A1393940 | AUI | NULL | R00689645 | NULL | AOD | AOD | NULL | NULL | N | NULL |

```
mysql> select * from MRDOC limit 10;
```
DOCKEY | VALUE | TYPE | EXPL |
--|--|--|--
ATN | AAL_TERM | expanded_form | AAL term |
ATN | ACCEPTABILITYID | expanded_form | Acceptability Id |
ATN | ACCEPTED_THERAPEUTIC_USE_FOR | expanded_form | Accepted therapeutic use for |
ATN | ACTIVE | expanded_form | Active |
ATN | ADDED_MEANING | expanded_form | Additional descriptive information |
ATN | ADDITIONAL_GUIDELINE | expanded_form | Additional explanatory text that is applicable to a concept (code/heading/subheading). |
ATN | ADDON_CODE | expanded_form | A "T" in this field indicates that it is an "Add-on" code, i.e. it is commonly carried out in addition to the primary procedure performed |
ATN | AGR | expanded_form | Alliance of Genome Resources |
ATN | AMBIGUITY_FLAG | expanded_form | Source atom ambiguity flag |
ATN | AMT | expanded_form | AOT uses MeSH term |


```
mysql> select * from MRSMAP limit 10;
```
MAPSETCUI | MAPSETSAB | MAPID | MAPSID | FROMEXPR | FROMTYPE | REL | RELA | TOEXPR | TOTYPE | CVF |
--|--|--|--|--|--|--|--|--|--|--
C1306694 | MTH | AT102971857 | NULL | C0264643 | CUI | SY | NULL | Hypertension, Renovascular AND Hypertension, Malignant | BOOLEAN_EXPRESSION_STR | NULL |
C1306694 | MTH | AT102971858 | NULL | C0276253 | CUI | SY | NULL | Pneumonia AND Cytomegalovirus Infections | BOOLEAN_EXPRESSION_STR | NULL |
C1306694 | MTH | AT102971859 | NULL | C0409780 | CUI | SY | NULL | Synovitis AND Hand | BOOLEAN_EXPRESSION_STR | NULL |
C1306694 | MTH | AT102971861 | NULL | C1706094 | CUI | SY | NULL | Adhesives AND Denture Retention | BOOLEAN_EXPRESSION_STR | NULL |
C1306694 | MTH | AT102971862 | NULL | C1706094 | CUI | SY | NULL | Dental Cements AND Orthodontics | BOOLEAN_EXPRESSION_STR | NULL |
C1306694 | MTH | AT102971863 | NULL | C0180739 | CUI | RN | NULL | Enteral Nutrition/instrumentation | BOOLEAN_EXPRESSION_STR | NULL |
C1306694 | MTH | AT102971864 | NULL | C1533661 | CUI | SY | NULL | Arthroscopy AND Wrist Joint | BOOLEAN_EXPRESSION_STR | NULL |
C1306694 | MTH | AT110677869 | NULL | C1962918 | CUI | RN | NULL | Wheelchairs AND Equipment and Supplies | BOOLEAN_EXPRESSION_STR | NULL |
C1306694 | MTH | AT110677871 | NULL | C1855348 | CUI | RU | NULL | Glomerulonephritis | BOOLEAN_EXPRESSION_STR | NULL |
C1306694 | MTH | AT110677872 | NULL | C1855348 | CUI | RU | NULL | Marfan Syndrome | BOOLEAN_EXPRESSION_STR | NULL |

```
mysql> select * from MRSTY limit 10;
```
CUI | TUI | STN | STY | ATUI | CVF |
--|--|--|--|--|--
C0541479 | T104 | A1.4.1.2 | Chemical Viewed Structurally | AT07863944 | NULL |
C0541480 | T104 | A1.4.1.2 | Chemical Viewed Structurally | AT07863945 | NULL |
C0541481 | T104 | A1.4.1.2 | Chemical Viewed Structurally | AT07863946 | NULL |
C0070474 | T104 | A1.4.1.2 | Chemical Viewed Structurally | AT07863947 | 256 |
C0541516 | T104 | A1.4.1.2 | Chemical Viewed Structurally | AT07863948 | NULL |
C0678461 | T104 | A1.4.1.2 | Chemical Viewed Structurally | AT07863949 | NULL |
C0678462 | T104 | A1.4.1.2 | Chemical Viewed Structurally | AT07863950 | 256 |
C0678518 | T104 | A1.4.1.2 | Chemical Viewed Structurally | AT07863951 | 256 |
C0678519 | T104 | A1.4.1.2 | Chemical Viewed Structurally | AT07863952 | 256 |
C0678520 | T104 | A1.4.1.2 | Chemical Viewed Structurally | AT07863953 | 256 |

```
mysql> select * from MRAUI limit 10;
```
AUI1 | CUI1 | VER | REL | RELA | MAPREASON | AUI2 | CUI2 | MAPIN |
--|--|--|--|--|--|--|--|--
A0000039 | C1411876 | 2022AA | NULL | NULL | move | A0000039 | C0869474 | Y |
A0000049 | C0003910 | 2005AB | NULL | NULL | move | A0000049 | C0236828 | Y |
A0000080 | C0003477 | 2011AA | NULL | NULL | move | A0000080 | C1527281 | Y |
A0000087 | C0596170 | 2008AB | NULL | NULL | move | A0000087 | C2267227 | Y |
A0000088 | C0596170 | 2008AB | NULL | NULL | move | A0000088 | C2267227 | Y |
A0000090 | C0596170 | 2008AB | NULL | NULL | move | A0000090 | C2267227 | Y |
A0000091 | C0596170 | 2008AB | NULL | NULL | move | A0000091 | C2267227 | Y |
A0000092 | C0596170 | 2008AB | NULL | NULL | move | A0000092 | C2267227 | Y |
A0000230 | C0029220 | 2007AA | NULL | NULL | move | A0000230 | C0236748 | Y |
A0000231 | C0029220 | 2007AA | NULL | NULL | move | A0000231 | C0236748 | Y |

```
mysql> select * from MRCONSO limit 10;
```
CUI | LAT | TS | LUI | STT | SUI | ISPREF | AUI | SAUI | SCUI | SDUI | SAB | TTY | CODE | STR | SRL | SUPPRESS | CVF |
--|--|--|--|--|--|--|--|--|--|--|--|--|--|--|--|--|--
C0026106 | ENG | S | L0026106 | PF | S0000001 | N | A0000002 | NULL | NULL | NULL | ICD10 | HT | F70 | Mild mental retardation | 3 | N | 256 |
C0026106 | ENG | S | L0026106 | PF | S0000001 | N | A0000003 | NULL | NULL | NULL | ICD10AM | HT | F70 | Mild mental retardation | 3 | N | 256 |
C0026351 | ENG | S | L0026351 | PF | S0000002 | N | A0000008 | NULL | NULL | NULL | ICD10 | HT | F71 | Moderate mental retardation | 3 | N | NULL |
C0026351 | ENG | S | L0026351 | PF | S0000002 | N | A0000009 | NULL | NULL | NULL | ICD10AM | HT | F71 | Moderate mental retardation | 3 | N | NULL |
C0036857 | ENG | S | L0036857 | PF | S0000003 | N | A0000014 | NULL | NULL | NULL | ICD10 | HT | F72 | Severe mental retardation | 3 | N | 256 |
C0036857 | ENG | S | L0036857 | PF | S0000003 | N | A0000015 | NULL | NULL | NULL | ICD10AM | HT | F72 | Severe mental retardation | 3 | N | 256 |
C0020796 | ENG | S | L0033296 | PF | S0000004 | N | A0000020 | NULL | NULL | NULL | ICD10 | HT | F73 | Profound mental retardation | 3 | N | 256 |
C0020796 | ENG | S | L0033296 | PF | S0000004 | N | A0000021 | NULL | NULL | NULL | ICD10AM | HT | F73 | Profound mental retardation | 3 | N | 256 |
C0025362 | ENG | S | L0080273 | PF | S0000005 | N | A0000026 | NULL | NULL | NULL | ICD10 | HT | F79 | Unspecified mental retardation | 3 | N | 256 |
C0025362 | ENG | S | L0080273 | PF | S0000005 | N | A0000027 | NULL | NULL | NULL | ICD10AM | HT | F79 | Unspecified mental retardation | 3 | N | 256 |

```
mysql> select * from MRFILES;
```
FIL | DES | FMT | CLS | RWS | BTS |
--|--|--|--|--|--
AMBIGLUI.RRF | Ambiguous term identifiers | LUI,CUI | 2 | 301093 | 5788399 |
AMBIGSUI.RRF | Ambiguous string identifiers | SUI,CUI | 2 | 207867 | 4022457 |
CHANGE/DELETEDCUI.RRF | Deleted concepts | PCUI,PSTR | 2 | 1426698 | 21400470 |
CHANGE/DELETEDLUI.RRF | Deleted terms | PLUI,PSTR | 2 | 0 | 0 |
CHANGE/DELETEDSUI.RRF | Deleted strings | PSUI,LAT,PSTR | 3 | 0 | 0 |
CHANGE/MERGEDCUI.RRF | Merged concepts | PCUI,CUI | 2 | 1536 | 29184 |
CHANGE/MERGEDLUI.RRF | Merged terms | PLUI,LUI | 2 | 0 | 0 |
MRAUI.RRF | AUI History | AUI1,CUI1,VER,REL,RELA,MAPREASON,AUI2,CUI2,MAPIN | 9 | 293552 | 15877630 |
MRCOLS.RRF | Attribute Relation | COL,DES,REF,MIN,AV,MAX,FIL,DTY | 8 | 339 | 23403 |
MRCONSO.RRF | Concept names and sources | CUI,LAT,TS,LUI,STT,SUI,ISPREF,AUI,SAUI,SCUI,SDUI,SAB,TTY,CODE,STR,SRL,SUPPRESS,CVF | 18 | 13501908 | 1737065435 |
MRCUI.RRF | CUI History | CUI1,VER,REL,RELA,MAPREASON,CUI2,MAPIN | 7 | 2716556 | 77130698 |
MRDEF.RRF | Definitions | CUI,AUI,ATUI,SATUI,SAB,DEF,SUPPRESS,CVF | 8 | 425261 | 118551841 |
MRDOC.RRF | Typed key value metadata map | DOCKEY,VALUE,TYPE,EXPL | 4 | 3396 | 218481 |
MRFILES.RRF | Relation Relation | FIL,DES,FMT,CLS,RWS,BTS | 6 | 52 | 4208 |
MRHIER.RRF | Computable hierarchies | CUI,AUI,CXN,PAUI,SAB,RELA,PTR,HCD,CVF | 9 | 31893483 | 4851178506 |
MRHIST.RRF | Source-asserted history | CUI,SOURCEUI,SAB,SVER,CHANGETYPE,CHANGEKEY,CHANGEVAL,REASON,CVF | 9 | 0 | 0 |
MRMAP.RRF | Mappings | MAPSETCUI,MAPSETSAB,MAPSUBSETID,MAPRANK,MAPID,MAPSID,FROMID,FROMSID,FROMEXPR,FROMTYPE,FROMRULE,FROMRES,REL,RELA,TOID,TOSID,TOEXPR,TOTYPE,TORULE,TORES,MAPRULE,MAPRES,MAPTYPE,MAPATN,MAPATV,CVF | 26 | 810346 | 129610753 |
MRRANK.RRF | Concept Name Ranking | RANK,SAB,TTY,SUPPRESS | 4 | 683 | 12217 |
MRREL.RRF | Related Concepts | CUI1,AUI1,STYPE1,REL,CUI2,AUI2,STYPE2,RELA,RUI,SRUI,SAB,SL,RG,DIR,SUPPRESS,CVF | 16 | 43842950 | 4093351915 |
MRSAB.RRF | Source Metadata | VCUI,RCUI,VSAB,RSAB,SON,SF,SVER,VSTART,VEND,IMETA,RMETA,SLC,SCC,SRL,TFR,CFR,CXTY,TTYL,ATNL,LAT,CENC,CURVER,SABIN,SSN,SCIT | 25 | 192 | 142036 |
MRSAT.RRF | Simple Concept, Term and String Attributes | CUI,LUI,SUI,METAUI,STYPE,CODE,ATUI,SATUI,ATN,SAB,ATV,SUPPRESS,CVF | 13 | 65915853 | 5967696352 |
MRSMAP.RRF | Simple Mappings | MAPSETCUI,MAPSETSAB,MAPID,MAPSID,FROMEXPR,FROMTYPE,REL,RELA,TOEXPR,TOTYPE,CVF | 11 | 416075 | 35648007 |
MRSTY.RRF | Semantic Types | CUI,TUI,STN,STY,ATUI,CVF | 6 | 3476668 | 199142173 |
MRXNS_ENG.RRF | Normalized String Index | LAT,NSTR,CUI,LUI,SUI | 5 | 12150129 | 886221009 |
MRXNW_ENG.RRF | Normalized Word Index | LAT,NWD,CUI,LUI,SUI | 5 | 39785958 | 1617668497 |
MRXW_ARA.RRF | Arabic Word Index | LAT,WD,CUI,LUI,SUI | 5 | 290245 | 13322541 |
MRXW_BAQ.RRF | Basque Word Index | LAT,WD,CUI,LUI,SUI | 5 | 2669 | 107206 |
MRXW_CHI.RRF | Chinese Word Index | LAT,WD,CUI,LUI,SUI | 5 | 601700 | 27220291 |
MRXW_CZE.RRF | Czech Word Index | LAT,WD,CUI,LUI,SUI | 5 | 477599 | 20363847 |
MRXW_DAN.RRF | Danish Word Index | LAT,WD,CUI,LUI,SUI | 5 | 2466 | 97114 |
MRXW_DUT.RRF | Dutch Word Index | LAT,WD,CUI,LUI,SUI | 5 | 1101850 | 46227836 |
MRXW_ENG.RRF | English Word Index | LAT,WD,CUI,LUI,SUI | 5 | 39223696 | 1581848830 |
MRXW_EST.RRF | Estonian Word Index | LAT,WD,CUI,LUI,SUI | 5 | 226586 | 8986331 |
MRXW_FIN.RRF | Finnish Word Index | LAT,WD,CUI,LUI,SUI | 5 | 42922 | 1875628 |
MRXW_FRE.RRF | French Word Index | LAT,WD,CUI,LUI,SUI | 5 | 2426179 | 101219317 |
MRXW_GER.RRF | German Word Index | LAT,WD,CUI,LUI,SUI | 5 | 799432 | 34054417 |
MRXW_GRE.RRF | Greek Word Index | LAT,WD,CUI,LUI,SUI | 5 | 274018 | 13634628 |
MRXW_HEB.RRF | Hebrew Word Index | LAT,WD,CUI,LUI,SUI | 5 | 1617 | 63262 |
MRXW_HUN.RRF | Hungarian Word Index | LAT,WD,CUI,LUI,SUI | 5 | 241751 | 10526508 |
MRXW_ITA.RRF | Italian Word Index | LAT,WD,CUI,LUI,SUI | 5 | 1199574 | 48609396 |
MRXW_JPN.RRF | Japanese Word Index | LAT,WD,CUI,LUI,SUI | 5 | 282000 | 16758359 |
MRXW_KOR.RRF | Korean Word Index | LAT,WD,CUI,LUI,SUI | 5 | 460600 | 19847488 |
MRXW_LAV.RRF | Latvian Word Index | LAT,WD,CUI,LUI,SUI | 5 | 230914 | 10092516 |
MRXW_NOR.RRF | Norwegian Word Index | LAT,WD,CUI,LUI,SUI | 5 | 125266 | 5530491 |
MRXW_POL.RRF | Polish Word Index | LAT,WD,CUI,LUI,SUI | 5 | 425767 | 18182640 |
MRXW_POR.RRF | Portuguese Word Index | LAT,WD,CUI,LUI,SUI | 5 | 1498232 | 60641784 |
MRXW_RUS.RRF | Russian Word Index | LAT,WD,CUI,LUI,SUI | 5 | 1111315 | 52355773 |
MRXW_SCR.RRF | Croatian Word Index | LAT,WD,CUI,LUI,SUI | 5 | 24050 | 1017136 |
MRXW_SPA.RRF | Spanish Word Index | LAT,WD,CUI,LUI,SUI | 5 | 9117253 | 375647723 |
MRXW_SWE.RRF | Swedish Word Index | LAT,WD,CUI,LUI,SUI | 5 | 288913 | 12571621 |
MRXW_TUR.RRF | Turkish Word Index | LAT,WD,CUI,LUI,SUI | 5 | 419840 | 17046315 |
MRXW_UKR.RRF | Ukrainian Word Index | LAT,WD,CUI,LUI,SUI | 5 | 25840 | 1210231 |

```
mysql> select * from MRSAB limit 10;
```
VCUI | RCUI | VSAB | RSAB | SON | SF | SVER | VSTART | VEND | IMETA | RMETA | SLC | SCC | SRL | TFR | CFR | CXTY | TTYL | ATNL | LAT | CENC | CURVER | SABIN | SSN | SCIT |
--|--|--|--|--|--|--|--|--|--|--|--|--|--|--|--|--|--|--|--|--|--|--|--|--
C1140092 | C1140091 | AIR93 | AIR | AI/RHEUM, 1993 | AIR | 1993 | NULL | NULL | 1995AA | NULL | May Cheh;;Lister Hill National Center for Biomedical Communications, National Library of Medicine;Building 38A, Room 9E902;8600 Rockville Pike;Bethesda;MD;;20894;;;cheh@nlm.nih.gov; | May Cheh;;Lister Hill National Center for Biomedical Communications, National Library of Medicine;Building 38A, Room 9E902;8600 Rockville Pike;Bethesda;MD;;20894;;;cheh@nlm.nih.gov; | 0 | 685 | 630 | FULL-MULTIPLE | DI,FI,HT,SY | NULL | ENG | UTF-8 | Y | Y | AI/RHEUM | ;;;;AI/RHEUM;;;;;National Library of Medicine, Lister Hill Center;1993;;Bethesda, MD;;;;;; |
C2366569 | C1140170 | ALT2009 | ALT | Alternative Billing Concepts, 2009 | ALT | 2009 | NULL | NULL | 2009AA | NULL | ;;ABC Coding Solutions - Alternative Link;6121 Indian School Road NE;Suite 131;Albuquerque;NM;United States;87110;1-877-621-5465;1-505-875-0002;Legal@ABCcodes.com; | Bernd G. Lucks;Chief Operating Officer;ABC Coding Solutions - Alternative Link;6121 Indian School Road NE;Suite 131;Albuquerque;NM;United States;87110;1-505-875-0001 ext. 202;;bernd.lucks@ABCcodes.com; | 3 | 4669 | 4613 | FULL | HT,PT | DATE_CREATED,DATE_LAST_MODIFIED,SOURCE_UI | ENG | UTF-8 | Y | Y | Alternative Billing Concepts | ;;;;ABC Codes and Terminology;;;9th;Albuquerque, NM;ABC Coding Solutions - Alternative Link;2009;;;;;;ENG;; |
C1140163 | C1140162 | AOD2000 | AOD | Alcohol and Other Drug Thesaurus, 2000 | AOD | 2000 | NULL | NULL | 2002AC | NULL | Nancy Winstanley;;NIAAA Library c/o CSR Incorporated;2107 Wilson Blvd., Suite 1000;;Arlington;VA;;22201;703-741-7147;; e-mail: nwinstanley@csrincorporated.com;; | Dagobert Soergel;;;;;;;;;301-405-2037;;ds52@umail.umd.edu; | 0 | 20685 | 15915 | FULL | DE,DS,ES,ET,EX,FN,NP,NS,NX,XD | HN,SOS | ENG | UTF-8 | Y | Y | Alcohol and Other Drug Thesaurus | ;;;;Alcohol and Other Drug Thesaurus: A Guide to Concepts and Terminology in Substance Abuse and Addiction;;;3rd. ed. [4 Volumes.];Bethesda, MD;National Institute on Alcohol Abuse and Alcoholism (NIAAA) and Center for Substance Abuse Prevention (CSAP);2000;;;;;;ENG;; |
C1704486 | C1704485 | AOT2003 | AOT | Authorized Osteopathic Thesaurus, 2003 | AOT | 2003 | NULL | NULL | 2006AD | NULL | ;;;;;Chevy Chase;MD;;;;;;http://www.aacom.org/InfoFor/educators/Pages/thesaurus.aspx | ;;American Association of Colleges of Osteopathic Medicine ;5550 Friendship Boulevard ;Suite 310;Chevy Chase;MD;United States;20815-7231;301-968-4100;301-968-4101;;http://www.aacom.org/InfoFor/educators/Pages/thesaurus.aspx | 0 | 471 | 276 | FULL-MULTIPLE | ET,PT | AMT | ENG | UTF-8 | Y | Y | Authorized Osteopathic Thesaurus | ;;;;Authorized Osteopathic Thesaurus;;;;Chevy Chase, MD;Educational Council of Osteopathic Principles of the American Association of Colleges of Osteopathic Medicine;2004;;;;;http://www.aacom.org/InfoFor/educators/Pages/thesaurus.aspx;ENG;; |
C5777091 | C4722517 | ATC_2022_23_03_06 | ATC | Anatomical Therapeutic Chemical Classification System, ATC_2022 | ATC | ATC_2022 | NULL | NULL | 2023AA | NULL | ;;WHO Collaborating Centre for Drug Statistics Methodology;Norwegian Institute of Public Health;P.O.Box 4404 Nydalen;Oslo;;Norway;0403;+47 21 07 81 60;+47 21 07 81 46;whocc@fhi.no;http://www.whocc.no/copyright_disclaimer/ | ;;WHO Collaborating Centre for Drug Statistics Methodology;Norwegian Institute of Public Health;P.O.Box 4404 Nydalen;Oslo;;Norway;0403;+47 21 07 81 60;+47 21 07 81 46;whocc@fhi.no;http://www.whocc.no/ | 0 | 7210 | 5794 | FULL | IN,PT,RXN_IN,RXN_PT | ATC_LEVEL,IS_DRUG_CLASS | ENG | UTF-8 | Y | Y | Anatomical Therapeutic Chemical Classification System | ;;WHO Collaborating Centre for Drug Statistics Methodology;;Anatomical Therapeutic Chemical (ATC) classification system;;;2022;Oslo, Norway;WHO Collaborating Centre for Drug Statistics Methodology;;;;;;http://www.whocc.no/copyright_disclaimer/;;; |
C1140164 | C1140165 | BI98 | BI | Beth Israel Vocabulary, 1.0 | BI | 1.0 | NULL | NULL | 1999AA | NULL | Daniel Z. Sands, M.D., M.P.H.;Clinical Systems Integration Architect;Center for Clinical Computing,Beth Israel Deaconess Medical Center,Harvard University;330 Brookline Avenue;;Boston;MA;United States;02215;617-667-1510;810-592-0716; e-mail: dsands@bidmc.Harvard.edu; | Howard Goldberg, MD.;;;;;;;;;;;hgoldber@bidmc.harvard.edu; | 2 | 1250 | 937 | NULL | AB,PT,RT,SY | NULL | ENG | UTF-8 | Y | Y | Beth Israel Problem List | Howard Goldberg, MD;;;;Beth Israel OMR Clinical Problem List Vocabulary;;;Version 1.0;Boston, MA;Beth Israel Deaconess Medical Center;1999;;;;;;ENG;; |
C4550264 | C3251798 | CCC2_5_2018 | CCC | Clinical Care Classification, 2_5_2018 | CCC | 2_5_2018 | NULL | NULL | 2018AA | NULL | Dr. Virginia K. Saba;CEO & President;SabaCare,Inc;;;Arlington;VA;United States;;703-521-6132;703-521-3866;vsaba@att.net;http://www.sabacare.com/; | Dr. Virginia K. Saba;CEO & President;SabaCare,Inc;;;Arlington;VA;United States;;703-521-6132;703-521-3866;vsaba@att.net;http://www.sabacare.com/; | 1 | 410 | 405 | FULL-MULTIPLE | HT,MP,MTH_HT,PT | NULL | ENG | UTF-8 | Y | Y | Clinical Care Classification | ;;SabaCare,Inc.;;Clinical Care Classification (CCC) System;;;2.5;;;;January 10, 2018;;;;;ENG;; |
C1140221 | C1140220 | CCPSS99 | CCPSS | Canonical Clinical Problem Statement System, 1999 | CCPSS | 1999 | NULL | NULL | 2000AA | NULL | Steven Brown, M.D.;Associate Professor, Biomedical Informatics;Eskind Biomedical Library, Vanderbilt University Medical Center;2209 Garland Ave;Room 442;Nashville;TN;United States;37232-8340;(615) 321-6335;;sbrown@vumclib.mc.vanderbilt.edu; | Steven Brown, MD;;Department of Biomedical Informatics Vanderbilt University;;;;;;;;;; | 3 | 15777 | 15245 | NULL | MP,PT,TX | CCF | ENG | UTF-8 | Y | Y | Clinical Problem Statements | ;;;;Canonical Clincial Problem Statement System;;;Version 1.0;;;June 23, 1999;;;;;;ENG;Contact: sbrown@vumclib.mc.vanderbilt.edu; |
C1541964 | C1140228 | CCS2005 | CCS | Clinical Classifications Software, 2005 | CCS | 2005 | NULL | NULL | 2005AC | NULL | Anne Elixhauser, Ph.D.;Senior Research Scientist;Agency for Healthcare Research and Quality;540 Gaither Road;;Rockville;MD;United States;20850;(301) 427-1411, 1-800-358-9295;(301) 594-1430;AElixhau@AHRQ.gov; | Anne Elixhauser, Ph.D.;Senior Research Scientist;Agency for Healthcare Research and Quality;540 Gaither Road;;Rockville;MD;United States;20850;1-800-358-9295;(301)-594-1430;AElixhau@AHRQ.gov; | 0 | 1617 | 1109 | FULL | HT,MD,MV,SD,SP,XM | CCI,FROMRSAB,FROMVSAB,MAPSETRSAB,MAPSETVERSION,MAPSETVSAB,MTH_MAPFROMCOMPLEXITY,MTH_MAPFROMEXHAUSTIVE,MTH_MAPSETCOMPLEXITY,MTH_MAPTOCOMPLEXITY,MTH_MAPTOEXHAUSTIVE,SOS,TORSAB,TOVSAB | ENG | UTF-8 | Y | Y | Clinical Classifications Software | ;;Agency for Healthcare Research and Quality (AHRQ);;Clinical Classifications Software (CCS);;;;;;April 2005;;Rockville,MD;;; http://www.hcup-us.ahrq.gov/toolssoftware/ccs/ccs.jsp;ENG;Phone: 301-594-1364.; |
C5770268 | C5400755 | CCSR_ICD10CM_2023 | CCSR_ICD10CM | Clinical Classifications Software Refined for ICD-10-CM, 2023 | CCS | 2023 | NULL | NULL | 2023AA | NULL | ;;Agency for Healthcare Research and Quality;5600 Fishers Lane;Mail Stop 07N94A;Rockville;MD;United States;20857;1-866-290-HCUP;(301) 594-1430;hcup@ahrq.gov;https://www.hcup-us.ahrq.gov/toolssoftware/ccsr/ccs_refined.jsp; | ;;Agency for Healthcare Research and Quality;5600 Fishers Lane;Mail Stop 07N94A;Rockville;MD;United States;20857;1-866-290-HCUP;(301)-594-1430;hcup@ahrq.gov;https://www.hcup-us.ahrq.gov/toolssoftware/ccsr/ccs_refined.jsp; | 0 | 546 | 545 | NULL | SD,XM | FROMRSAB,FROMVSAB,MAPSETRSAB,MAPSETVERSION,MAPSETVSAB,MTH_MAPFROMCOMPLEXITY,MTH_MAPFROMEXHAUSTIVE,MTH_MAPSETCOMPLEXITY,MTH_MAPTOCOMPLEXITY,MTH_MAPTOEXHAUSTIVE,TORSAB,TOVSAB | ENG | UTF-8 | Y | Y | Clinical Classifications Software Refined for ICD-10-CM | ;;Healthcare Cost and Utilization Project (HCUP);;Clinical Classifications Software Refined for ICD-10-CM;;;;;Agency for Healthcare Research and Quality (AHRQ);;November 2022;Rockville, MD;;;;ENG;; |
