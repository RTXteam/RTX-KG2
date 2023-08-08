## UMLS MySQL Walk Through

# RegEx MySQL Table -> Markdown Table
1. Replace: `\+(-)+` With: `\|--`
2. Replace: `^\|( )*` With: Nothing
3. Replace: `--\+$` With: `--`
4. Replace: `( )+` With: ` `

Script used:
```
sed -i -E "s/\+(-)+/\|--/g" umls_table.txt
sed -i -E "s/^\|( )*//g" umls_table.txt
sed -i -E "s/--\+$/--/g" umls_table.txt
sed -i -E "s/( )+/ /g" umls_table.txt
sed -i -E "s/<|>//g" umls_table.txt
```

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

Tables that `umls2rdf.py` uses:
- MRSTY
- MRCONSO
- MRSAB
- MRREL
- MRDEF
- MRSAT
- MRRANK
- MRDOC

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



```
mysql> select * from MRDEF limit 10;
```
CUI | AUI | ATUI | SATUI | SAB | DEF | SUPPRESS | CVF |
--|--|--|--|--|--|--|--
C0007662 | A15587413 | AT100258389 | NULL | MSH | Areas set apart as burial grounds. | N | NULL |
C0031705 | A0101053 | AT100258390 | NULL | MSH | A non-metal element that has the atomic symbol P, atomic number 15, and atomic weight 31. It is an essential element that takes part in a broad variety of biochemical reactions. | N | NULL |
C0319858 | A15585286 | AT100258391 | NULL | MSH | A genus of ectomycorrhizae basidiomycetous fungi in the family Cortinariaceae. Some species are poisonous. | N | NULL |
C0026655 | A0088287 | AT100258392 | NULL | MSH | A republic in southern Africa, south of TANZANIA, east of ZAMBIA and ZIMBABWE, bordered on the west by the Indian Ocean. Its capital is Maputo. It was formerly called Portuguese East Africa. | N | NULL |
C2350764 | A26632051 | AT100258393 | NULL | MSH | The flow of ions into or out of cells that cause EXCITATORY POSTSYNAPTIC POTENTIALS. | N | NULL |
C2350395 | A15587282 | AT100258394 | NULL | MSH | Timing the acquisition of imaging data to specific points in the cardiac cycle to minimize image blurring and other motion artifacts. | N | NULL |
C2350340 | A26678303 | AT100258395 | NULL | MSH | The ion flow that effects the POSTSYNAPTIC POTENTIAL. | N | NULL |
C0073209 | A12983302 | AT100258396 | NULL | MSH | A PROTEIN-SERINE-THREONINE KINASE that is found in PHOTORECEPTOR CELLS. It mediates light-dependent PHOSPHORYLATION of RHODOPSIN and plays an important role in PHOTOTRANSDUCTION. | N | NULL |
C0872279 | A15585197 | AT100258397 | NULL | MSH | A type of strength-building exercise program that requires the body muscle to exert a force against some form of resistance, such as weight, stretch bands, water, or immovable objects. Resistance exercise is a combination of static and dynamic contractions involving shortening and lengthening of skeletal muscles. | N | NULL |
C2350288 | A26632695 | AT100258398 | NULL | MSH | The duration of time from initiation to discontinuation of drug therapy. | N | NULL |

```
mysql> select * from MRDEF where SAB != "MSH" limit 10;
```
CUI | AUI | ATUI | SATUI | SAB | DEF | SUPPRESS | CVF |
--|--|--|--|--|--|--|--
C1965760 | A15884584 | AT104406511 | NULL | ALT | Mapping the practitioner type or specialty to a non-specified emergency or non-emergency transportation, travel, or delivery expense or service code. Use associated HCPCS II codes to bill for expense(s) or service(s). This code is used for scope-of-practice mapping, not for billing. | N | NULL |
C2366573 | A15884545 | AT104406512 | NULL | ALT | Mapping the practitioner type or specialty to a non-specified physician service or procedure code. Use associated HCPCS II codes to bill for physician service(s). This code is used for scope-of-practice mapping, not for billing. | N | NULL |
C2366625 | A15884463 | AT104406513 | NULL | ALT | Mapping the practitioner type or specialty to a nutritional therapy service code. Use associated HCPCS II codes to bill for nutrition service(s). This code is used for scope-of-practice mapping, not for billing. | N | NULL |
C2366594 | A15884632 | AT104406514 | NULL | ALT | Mapping the practitioner type or specialty to a wound care an/or therapy service code. Use associated HCPCS II codes to bill for wound care service(s). This code is used for scope-of-practice mapping, not for billing. | N | NULL |
C2366609 | A15884637 | AT104406515 | NULL | ALT | Mapping the practitioner type or specialty to a stabilizing, traction and/or restraining device or equipment code. Use associated HCPCS II codes to bill for stabilizing, traction or restraining device(s) or equipment. This code is used for scope-of-practice mapping, not for billing. | N | NULL |
C1535681 | A15884507 | AT104406516 | NULL | ALT | Mapping the practitioner type or specialty to a non-specified gastroenterology procedure. Use CPT® and/or HCPCS II codes to bill for all gastroenterology service(s). This code is used for scope-of-practice mapping, not for billing. | N | NULL |
C2366582 | A15884518 | AT104406517 | NULL | ALT | Mapping the practitioner type or specialty to a dental service adjunctive general code. Use associated HCPCS II codes to bill for dental service(s). This code is used for scope-of-practice mapping, not for billing. | N | NULL |
C2366655 | A15884685 | AT104406518 | NULL | ALT | Mapping the practitioner type or specialty to a prescription documentation service code. Use associated HCPCS II codes to bill for documentation service(s). This code is used for scope-of-practice mapping, not for billing. | N | NULL |
C2366632 | A15884500 | AT104406519 | NULL | ALT | Mapping the practitioner type or specialty to a vision rehab service code. Use associated HCPCS II codes to bill for vision service(s). This code is used for scope-of-practice mapping, not for billing. | N | NULL |
C1535683 | A15884654 | AT104406520 | NULL | ALT | Mapping the practitioner type or specialty to a non-specified diagnostic infusion procedure. Use CPT® and/or HCPCS II codes to bill for all infusion service(s). This code is used for scope-of-practice mapping, not for billing. | N | NULL |

```
mysql> select * from MRDEF where SAB != "MSH" and SAB != "ALT" limit 10;
```
CUI | AUI | ATUI | SATUI | SAB | DEF | SUPPRESS | CVF |
--|--|--|--|--|--|--|--
C0032226 | A18556325 | AT130670828 | NULL | CHV | disease causing increase of the fluid amount in the chest wall cavity | N | NULL |
C0032226 | A18593399 | AT130670829 | NULL | CHV | disease causing increase of the fluid amount in the chest wall cavity | N | NULL |
C0032226 | A18649215 | AT130670830 | NULL | CHV | disease causing increase of the fluid amount in the chest wall cavity | N | NULL |
C0078049 | A18558170 | AT130670831 | NULL | CHV | a substance used to prevent chickenpox | N | NULL |
C0078049 | A18576590 | AT130670832 | NULL | CHV | a substance used to prevent chickenpox | N | NULL |
C0078049 | A18632385 | AT130670833 | NULL | CHV | a substance used to prevent chickenpox | N | NULL |
C0078049 | A18688022 | AT130670834 | NULL | CHV | a substance used to prevent chickenpox | N | NULL |
C0543431 | A18565798 | AT130670835 | NULL | CHV | a unit of radiation dose | N | NULL |
C0556645 | A18566010 | AT130670836 | NULL | CHV | a unit of radiation dose | N | NULL |
C0560132 | A18566104 | AT130670837 | NULL | CHV | a unit of radiation dose | N | NULL |

```
mysql> select SAB, count(*) from MRDEF group by SAB;
```
SAB | count(*) |
--|--
AIR | 160 |
ALT | 4281 |
AOT | 240 |
CCC | 408 |
CHV | 2657 |
CSP | 8265 |
FMA | 2147 |
GO | 43648 |
HL7V3.0 | 8270 |
HPO | 14040 |
ICF | 767 |
ICF-CY | 906 |
JABL | 724 |
LNC | 511 |
MCM | 18 |
MDR | 230 |
MDRARA | 230 |
MDRBPO | 230 |
MDRCZE | 230 |
MDRDUT | 230 |
MDRFRE | 230 |
MDRGER | 230 |
MDRGRE | 230 |
MDRHUN | 230 |
MDRITA | 230 |
MDRJPN | 230 |
MDRKOR | 230 |
MDRLAV | 230 |
MDRPOL | 230 |
MDRPOR | 230 |
MDRRUS | 230 |
MDRSPA | 230 |
MDRSWE | 230 |
MEDLINEPLUS | 1023 |
MSH | 32702 |
MSHCZE | 22345 |
MSHFRE | 138 |
MSHNOR | 7460 |
MSHPOR | 30811 |
MSHSCR | 1 |
MSHSPA | 30647 |
MSHSWE | 17142 |
NANDA-I | 304 |
NCI | 137609 |
NEU | 2660 |
NIC | 602 |
NOC | 581 |
NUCCHCPT | 589 |
OMS | 134 |
ORPHANET | 6669 |
PDQ | 6356 |
PNDS | 265 |
PSY | 2212 |
SCTSPA | 7511 |
SNOMEDCT_US | 9413 |
SPN | 4204 |
UMD | 12259 |
UWDA | 442 |

```
mysql> select * from MRSAT limit 10;
```
CUI | LUI | SUI | METAUI | STYPE | CODE | ATUI | SATUI | ATN | SAB | ATV | SUPPRESS | CVF |
--|--|--|--|--|--|--|--|--|--|--|--|--
C0002797 | NULL | NULL | NULL | CUI | NULL | AT00000003 | NULL | DA | MTH | 19900930 | N | NULL |
C0002804 | NULL | NULL | NULL | CUI | NULL | AT00000004 | NULL | DA | MTH | 19900930 | N | NULL |
C0197800 | NULL | NULL | NULL | CUI | NULL | AT00000007 | NULL | DA | MTH | 19940412 | N | NULL |
C0002808 | NULL | NULL | NULL | CUI | NULL | AT00000008 | NULL | DA | MTH | 19900930 | N | NULL |
C0002810 | NULL | NULL | NULL | CUI | NULL | AT00000009 | NULL | DA | MTH | 19900930 | N | NULL |
C0002811 | NULL | NULL | NULL | CUI | NULL | AT00000010 | NULL | DA | MTH | 19900930 | N | NULL |
C0197801 | NULL | NULL | NULL | CUI | NULL | AT00000011 | NULL | DA | MTH | 19940412 | N | NULL |
C0002812 | NULL | NULL | NULL | CUI | NULL | AT00000012 | NULL | DA | MTH | 19900930 | N | NULL |
C0002813 | NULL | NULL | NULL | CUI | NULL | AT00000013 | NULL | DA | MTH | 19900930 | N | NULL |
C0197803 | NULL | NULL | NULL | CUI | NULL | AT00000014 | NULL | DA | MTH | 19940412 | N | NULL |

```
mysql> select * from MRSAT where SAB != "MTH" limit 10;
```
CUI | LUI | SUI | METAUI | STYPE | CODE | ATUI | SATUI | ATN | SAB | ATV | SUPPRESS | CVF |
--|--|--|--|--|--|--|--|--|--|--|--|--
C0226631 | L7947353 | S9261161 | A15487314 | AUI | 77500 | AT100000001 | NULL | LANGUAGE | FMA | Latin | N | NULL |
C0226476 | L1658590 | S1869222 | A15487357 | AUI | 43921 | AT100000002 | NULL | LANGUAGE | FMA | Latin | N | NULL |
C0226476 | L1658578 | S1869210 | A15487358 | AUI | 43921 | AT100000003 | NULL | LANGUAGE | FMA | Latin | N | NULL |
C1184758 | L7921465 | S9257177 | A15487423 | AUI | 75484 | AT100000004 | NULL | LANGUAGE | FMA | Latin | N | NULL |
C0224224 | L7917062 | S9255685 | A15487425 | AUI | 46777 | AT100000005 | NULL | LANGUAGE | FMA | Latin | N | NULL |
C1306642 | L7941514 | S9244381 | A15487435 | AUI | 71875 | AT100000006 | NULL | LANGUAGE | FMA | Latin | N | NULL |
C0227302 | L7921706 | S9259748 | A15487449 | AUI | 14929 | AT100000007 | NULL | LANGUAGE | FMA | Latin | N | NULL |
C0694589 | L1456954 | S1742895 | A15487461 | AUI | 67962 | AT100000008 | NULL | LANGUAGE | FMA | Latin | N | NULL |
C0152374 | L1457021 | S1742970 | A15487464 | AUI | 72455 | AT100000009 | NULL | LANGUAGE | FMA | Latin | N | NULL |
C0224086 | L7915107 | S9234531 | A15487481 | AUI | 9719 | AT100000010 | NULL | LANGUAGE | FMA | Latin | N | NULL |

As you can see from the image below (from `KG2.8.3pre`), the `CODE` column of the table corresponds to the FMA ID for that node.
![image](https://github.com/RTXteam/RTX-KG2/assets/36611732/c3a043fc-6e29-47c9-9598-f5b67dbec917)

```
mysql> select SAB, count(*) from MRSAT group by SAB;
```
SAB | count(*) |
--|--
ALT | 13272 |
AOD | 6054 |
AOT | 27 |
ATC | 7860 |
CCPSS | 15716 |
CCS | 23453 |
CCSR_ICD10CM | 12 |
CCSR_ICD10PCS | 12 |
CDT | 1275 |
CHV | 877774 |
CPT | 249691 |
CSP | 23251 |
CVX | 2755 |
DRUGBANK | 10459 |
FMA | 284369 |
GO | 168004 |
GS | 76415 |
HCDT | 7983 |
HCPCS | 66036 |
HCPT | 105273 |
HGNC | 810883 |
HL7V2.5 | 16770 |
HL7V3.0 | 38386 |
HPO | 29796 |
ICD10AM | 61299 |
ICD10CM | 101898 |
ICD10PCS | 79341 |
ICD9CM | 10190 |
ICF | 13822 |
ICF-CY | 386 |
ICNP | 1955 |
ICPC | 1318 |
ICPC2EENG | 1175 |
ICPC2ICD10ENG | 81849 |
ICPC2P | 29636 |
JABL | 490 |
KCD5 | 76 |
LCH_NW | 13 |
LNC | 2417573 |
MDR | 1045184 |
MDRARA | 1045184 |
MDRBPO | 1045184 |
MDRCZE | 1045184 |
MDRDUT | 1045184 |
MDRFRE | 1045184 |
MDRGER | 1045184 |
MDRGRE | 1045184 |
MDRHUN | 1045184 |
MDRITA | 1045184 |
MDRJPN | 780993 |
MDRKOR | 1045184 |
MDRLAV | 1045184 |
MDRPOL | 1045184 |
MDRPOR | 1045184 |
MDRRUS | 1045184 |
MDRSPA | 1045184 |
MDRSWE | 1045184 |
MED-RT | 95999 |
MEDCIN | 1355208 |
MEDLINEPLUS | 8173 |
MMSL | 242812 |
MMX | 412325 |
MSH | 4841113 |
MSHCZE | 81443 |
MSHFRE | 17 |
MSHITA | 59531 |
MSHLAV | 1191 |
MSHNOR | 62205 |
MSHPOR | 107509 |
MSHSCR | 8069 |
MSHSPA | 95836 |
MTH | 9493363 |
MTHMST | 1908 |
MTHSPL | 3345744 |
MVX | 411 |
NANDA-I | 1879 |
NCBI | 2034978 |
NCI | 158863 |
NDDF | 71219 |
NEU | 8194 |
NIC | 3023 |
NOC | 15731 |
NUCCHCPT | 522 |
OMIM | 204484 |
OMS | 21 |
PDQ | 55017 |
PNDS | 59 |
PPAC | 813 |
PSY | 8563 |
RCD | 175408 |
RXNORM | 2126399 |
SCTSPA | 5843064 |
SNMI | 85848 |
SNOMEDCT_US | 9779615 |
SNOMEDCT_VET | 457028 |
SPN | 19052 |
UMD | 46357 |
USP | 8802 |
USPMG | 1609 |
UWDA | 61526 |
VANDF | 349254 |

```
mysql> select * from MRRANK limit 10;
```
MRRANK_RANK | SAB | TTY | SUPPRESS |
--|--|--|--
266 | AIR | DI | N |
267 | AIR | FI | N |
264 | AIR | HT | N |
265 | AIR | SY | N |
364 | ALT | HT | N |
365 | ALT | PT | N |
282 | AOD | DE | N |
281 | AOD | DS | N |
277 | AOD | ES | N |
278 | AOD | ET | N |

# Studying `umls2rdf.py`

Tables Used:
- `MRSTY`
- `MRCONSO`
- `MRSAB`
- `MRREL`
- `MRDEF`
- `MRSAT`
- `MRRANK`
- `MRDOC`

## `MRSTY`

**What is taken?**

This table is accessed twice, once on line 143 and once on line 573. At the line 143 accession, the distinct columns `TUI`, `STN`, and `STY` are taken. At the line 573 accession, all of the columns from `MRSTY` are taken, which consists of `CUI`, `TUI`, `STN`, `STY`, `ATUI`, `CVF`.

**What do these columns mean?**

See [here](https://www.ncbi.nlm.nih.gov/books/NBK9685/table/ch03.Tf/).

**What does this table contain?**

**How does `umls2rdf.py` use this table?**

## `MRCONSO`

**What is taken?**

This table is accessed once, on line 491. All of the columns are taken, which consists of `CUI`, `LAT`, `TS`, `LUI`, `STT`, `SUI`, `ISPREF`, `AUI`, `SAUI`, `SCUI`, `SDUI`, `SAB`, `TTY`, `CODE`, `STR`, `SRL`, `SUPPRESS`, and `CVF`.

**What do these columns mean?**

See [here](https://www.ncbi.nlm.nih.gov/books/NBK9685/table/ch03.T.concept_names_and_sources_file_mr/).

**What does this table contain?**

**How does `umls2rdf.py` use this table?**

## `MRSAB`

**What is taken?**

This table is accessed once, on line 496. All of the columns are taken, which consists of `VCUI`, `RCUI`, `VSAB`, `RSAB`, `SON`, `SF`, `SVER`, `VSTART`, `VEND`, `IMETA`, `RMETA`, `SLC`, `SCC`, `SRL`, `TFR`, `CFR`, `CXTY`, `TTYL`, `ATNL`, `LAT`, `CENC`, `CURVER`, `SABIN`, `SSN`, and `SCIT`.

**What do these columns mean?**

See [here](https://www.ncbi.nlm.nih.gov/books/NBK9685/table/ch03.T.source_information_file_mrsab_rrf/).

**What does this table contain?**

**How does `umls2rdf.py` use this table?**

A limit of 1 is placed on this `scan` (per ontology code).

## `MRREL`

**What is taken?**

This table is accessed once, on line 527. All of the columns are taken, which consists of `CUI1`, `AUI1`, `STYPE1`, `REL`, `CUI2`, `AUI2`, `STYPE2`, `RELA`, `RUI`, `SRUI`, `SAB`, `SL`, `RG`, `DIR`, `SUPPRESS`, and `CVF`.

**What do these columns mean?**

See [here](https://www.ncbi.nlm.nih.gov/books/NBK9685/table/ch03.T.related_concepts_file_mrrel_rrf/).

**What does this table contain?**

**How does `umls2rdf.py` use this table?**

## `MRDEF`

**What is taken?**

This table is accessed once, on line 538. All of the columns are taken, which consists of `CUI`, `AUI`, `ATUI`, `SATUI`, `SAB`, `DEF`, `SUPPRESS`, and `CVF`.

**What do these columns mean?**

See [here](https://www.ncbi.nlm.nih.gov/books/NBK9685/table/ch03.T.definitions_file_mrdef_rrf/).

**What does this table contain?**

**How does `umls2rdf.py` use this table?**

## `MRSAT`

**What is taken?**

This table is accessed once, on line 549. All of the columns are taken, which consists of `CUI`, `LUI`, `SUI`, `METAUI`, `STYPE`, `CODE`, `ATUI`, `SATUI`, `ATN`, `SAB`, `ATV`, `SUPPRESS`, and `CVF`.

**What do these columns mean?**

See [here](https://www.ncbi.nlm.nih.gov/books/NBK9685/table/ch03.T.simple_concept_and_atom_attribute/).

**What does this table contain?**

**How does `umls2rdf.py` use this table?**

## `MRRANK`

**What is taken?**

This table is accessed once, on line 560. All of the columns are taken, which consists of `MRRANK_RANK`, `SAB`, `TTY`, and `SUPPRESS`.

**What do these columns mean?**

See [here](https://www.ncbi.nlm.nih.gov/books/NBK9685/table/ch03.T.concept_name_ranking_file_mrrank/).

**What does this table contain?**

**How does `umls2rdf.py` use this table?**

## `MRDOC`

**What is taken?**

This table is accessed once, on line 742. All of the columns are taken, which consists of `DOCKEY`, `VALUE`, `TYPE`, `EXPL`

**What do these columns mean?**

See [here](https://www.ncbi.nlm.nih.gov/books/NBK9685/table/ch03.Te/).

**What does this table contain?**

**How does `umls2rdf.py` use this table?**

## Assorted Notes

- The table is filtered based on which ontology's ttl file is being generated at the time. This is done through the scan function, which is the actual function that sends the query to MySQL. Thus, this does not create redundancy but instead in fact ensures that only the ontologies we care about are ever queries. This is done on lines 222 through 227, where the `filt` parameter is passed into the `WHERE` clause on the MySQL statement.

## To Do

1. Determine which columns are actually making their ways into the `TTL` files by examining the `TTL` files.

2. Decide on join points/concatentation between this tables. Ideally, we will be able to implement a streaming solution like with SemMedDB, where each row has everything we need to know about that CUI. With extra information (such as `MRDOC` content), we may have to create a supplementary file, but it should be pretty small.

3. Implement MySQL querying as decided on in step 2.

4. Run time tests on the solution decided on in step 3. We need to determine whether this will save the time currently used in roughly 14 hours (though a good chunk of that is load in) of ETL currently present. We probably want under 2-3 hours of MySQL time to make this a worthwhile change.

5. Repeat steps 3 and 4 until timing is desirable.

6. Evaluate whether the content is sufficiently comparable to what is currently in KG2.

### Step 1

Example: `umls-atc.ttl`

```
<http://purl.bioontology.org/ontology/ATC/C03AH01> a owl:Class ;
        skos:prefLabel """chlorothiazide, combinations"""@en ;
        skos:notation """C03AH01"""^^xsd:string ;
        rdfs:subClassOf <http://purl.bioontology.org/ontology/ATC/C03AH> ;
        <http://purl.bioontology.org/ontology/ATC/ATC_LEVEL> """5"""^^xsd:string ;
        UMLS:has_cui """C3652440"""^^xsd:string ;
        UMLS:has_tui """T109"""^^xsd:string ;
        UMLS:has_tui """T121"""^^xsd:string ;
        UMLS:has_sty <http://purl.bioontology.org/ontology/STY/T109> ;
        UMLS:has_sty <http://purl.bioontology.org/ontology/STY/T121> ;
```

Example: `umls-chv.ttl`
```
<http://purl.bioontology.org/ontology/CHV/0000050974> a owl:Class ;
        skos:prefLabel """synthesis"""@en ;
        skos:notation """0000050974"""^^xsd:string ;
        skos:definition """the combining of separate elements or substances to form a coherent whole"""@en ;
        <http://purl.bioontology.org/ontology/CHV/COMBO_SCORE> """0.413096903"""^^xsd:string ;
        <http://purl.bioontology.org/ontology/CHV/COMBO_SCORE_NO_TOP_WORDS> """0.413096903"""^^xsd:string ;
        <http://purl.bioontology.org/ontology/CHV/CONTEXT_SCORE> """0.4381"""^^xsd:string ;
        <http://purl.bioontology.org/ontology/CHV/CUI_SCORE> """0.4034"""^^xsd:string ;
        <http://purl.bioontology.org/ontology/CHV/DISPARAGED> """no"""^^xsd:string ;
        <http://purl.bioontology.org/ontology/CHV/FREQUENCY> """0.397790709"""^^xsd:string ;
        UMLS:has_cui """C0220781"""^^xsd:string ;
        UMLS:has_tui """T038"""^^xsd:string ;
        UMLS:has_sty <http://purl.bioontology.org/ontology/STY/T038> ;
```

Example: `umls-drugbank.ttl`
```
<http://purl.bioontology.org/ontology/DRUGBANK/DB09085> a owl:Class ;
        skos:prefLabel """Tetracaine"""@en ;
        skos:notation """DB09085"""^^xsd:string ;
        skos:altLabel """2-(Dimethylamino)ethyl p-(butylamino)benzoate"""@en , """2-(dimethylamino)ethyl 4-(butylamino)benzoate"""@en , """Amethocaine"""@en , """Amethocaine HCl"""@en , """Dicaine"""@en , """Diäthylaminoäthanol ester der p-butylaminobenzösäure"""@en , """Medihaler-Tetracaine"""@en , """Metraspray"""@en , """Tetracaine HCl"""@en , """Tetracaína"""@en , """Tétracaïne"""@en , """p-(butylamino)benzoic acid β-(dimethylamino)ethyl ester"""@en , """p-Butylaminobenzoyl-2-dimethylaminoethanol"""@en ;
        <http://purl.bioontology.org/ontology/DRUGBANK/FDA_UNII_CODE> """0619F35CGV"""^^xsd:string ;
        UMLS:has_cui """C0039629"""^^xsd:string ;
        UMLS:has_cui """C0304456"""^^xsd:string ;
        UMLS:has_cui """C0702211"""^^xsd:string ;
        UMLS:has_cui """C4292382"""^^xsd:string ;
        UMLS:has_cui """C4292391"""^^xsd:string ;
        UMLS:has_tui """T109"""^^xsd:string ;
        UMLS:has_tui """T121"""^^xsd:string ;
        UMLS:has_sty <http://purl.bioontology.org/ontology/STY/T109> ;
        UMLS:has_sty <http://purl.bioontology.org/ontology/STY/T121> ;
```

I am currently trying to find where `FDA_UNII_CODE` is in the data. I know that it is an attribute per https://www.nlm.nih.gov/research/umls/knowledge_sources/metathesaurus/release/attribute_names.html. 

It looks like, per running `select * from MRSAT where SAB="DRUGBANK" limit 20;`, the name of the attribute is in the `ATN` column and the value is in the `ATV` column.

This link discusses each of the `MRREL` types: https://www.nlm.nih.gov/research/umls/knowledge_sources/metathesaurus/release/abbreviations.html.

```
select * from MRCONSO con left join MRSAT sat on con.CODE=sat.CODE where con.SAB="DRUGBANK" limit 10;
```

CUI | LAT | TS | LUI | STT | SUI | ISPREF | AUI | SAUI | SCUI | SDUI | SAB | TTY | CODE | STR | SRL | SUPPRESS | CVF | CUI | LUI | SUI | METAUI | STYPE | CODE | ATUI | SATUI | ATN | SAB | ATV | SUPPRESS | CVF |
--|--|--|--|--|--|--|--|--|--|--|--|--|--|--|--|--|--|--|--|--|--|--|--|--|--|--|--|--|--|--
C0039601 | ENG | S | L13409149 | VO | S16395464 | Y | A27406646 | NULL | DB00624 | NULL | DRUGBANK | FSY | DB00624 | Testosteronum | 0 | N | 256 | C0039601 | L0039601 | S0092451 | A27059293 | SCUI | DB00624 | AT215745781 | NULL | SID | DRUGBANK | DB05275 | N | NULL |
C0039925 | ENG | S | L13409165 | PF | S16395565 | Y | A27406649 | NULL | DB00599 | NULL | DRUGBANK | FSY | DB00599 | Tiopentale | 0 | N | 256 | C0039925 | L0039925 | S0093293 | A27062921 | SCUI | DB00599 | AT215745786 | NULL | FDA_UNII_CODE | DRUGBANK | JI8Z5M7NA3 | N | NULL |
C0004057 | ENG | S | L13415345 | PF | S16396444 | Y | A27406659 | NULL | DB00945 | NULL | DRUGBANK | FSY | DB00945 | ácido acetilsalicílico | 0 | N | 256 | C0004057 | L0001063 | S0584084 | A27066872 | SCUI | DB00945 | AT215746200 | NULL | SID | DRUGBANK | EXPT00475 | N | NULL |
C0004057 | ENG | S | L13415345 | PF | S16396444 | Y | A27406659 | NULL | DB00945 | NULL | DRUGBANK | FSY | DB00945 | ácido acetilsalicílico | 0 | N | 256 | C0004057 | L0001063 | S0584084 | A27066872 | SCUI | DB00945 | AT215745697 | NULL | FDA_UNII_CODE | DRUGBANK | R16CO5Y76E | N | NULL |
C0006491 | ENG | S | L13413033 | PF | S16390917 | Y | A27406692 | NULL | DB00611 | NULL | DRUGBANK | FSY | DB00611 | Butorphanolum | 0 | N | 256 | C0006491 | L0006491 | S0021116 | A27064721 | SCUI | DB00611 | AT215745783 | NULL | FDA_UNII_CODE | DRUGBANK | QV897JC36D | N | NULL |
C0007735 | ENG | S | L13409541 | PF | S16391091 | Y | A27406763 | NULL | DB00456 | NULL | DRUGBANK | FSY | DB00456 | Cefalotina | 0 | N | 256 | C0007735 | L0007540 | S0023182 | A27055419 | SCUI | DB00456 | AT215745827 | NULL | SID | DRUGBANK | EXPT00946 | N | NULL |
C0061323 | ENG | P | L0061323 | VO | S16392549 | Y | A27406770 | NULL | DB00222 | NULL | DRUGBANK | FSY | DB00222 | Glimépiride | 0 | N | 256 | C0061323 | L0061323 | S1325002 | A27055170 | SCUI | DB00222 | AT215745888 | NULL | SID | DRUGBANK | APRD00381 | N | NULL |
C0064113 | ENG | S | L13414126 | PF | S16392995 | Y | A27406772 | NULL | DB01167 | NULL | DRUGBANK | FSY | DB01167 | Itraconazol | 0 | N | 256 | C0064113 | L0064113 | S0170262 | A27068928 | SCUI | DB01167 | AT215746145 | NULL | SID | DRUGBANK | APRD00040 | N | NULL |
C0064113 | ENG | S | L13414126 | PF | S16392995 | Y | A27406772 | NULL | DB01167 | NULL | DRUGBANK | FSY | DB01167 | Itraconazol | 0 | N | 256 | C0064113 | L0064113 | S0170262 | A27068928 | SCUI | DB01167 | AT215746144 | NULL | FDA_UNII_CODE | DRUGBANK | 304NUG5GF4 | N | NULL |
C0010927 | ENG | S | L13413100 | PF | S16391572 | Y | A27406779 | NULL | DB00851 | NULL | DRUGBANK | FSY | DB00851 | Dacarbazin | 0 | N | 256 | C0010927 | L0010927 | S0030020 | A27063198 | SCUI | DB00851 | AT215746222 | NULL | SID | DRUGBANK | APRD00331 | N | NULL |


For some reason, some (all?) of the names are in latin.

```
select con.CUI, con.CODE, con.ISPREF, con.STR, sat.ATN, sat.ATV from MRCONSO con left join MRSAT sat on con.CODE=sat.CODE where con.SAB="DRUGBANK" limit 10;
```
CUI | CODE | ISPREF | STR | ATN | ATV |
--|--|--|--|--|--
C1948374 | DB08906 | Y | Fluticasonum furoas | FDA_UNII_CODE | JS86977WNV |
C2930696 | DB08895 | Y | Tofacitinibum | FDA_UNII_CODE | 87LA6FU830 |
C1948374 | DB08906 | Y | Furoato de fluticasona | FDA_UNII_CODE | JS86977WNV |
C1948374 | DB08906 | Y | Furoate de fluticasone | FDA_UNII_CODE | JS86977WNV |
C0042665 | DB09185 | Y | Viloxazina | FDA_UNII_CODE | 5I5Y2789ZF |
C0123163 | DB09081 | Y | idébénone | FDA_UNII_CODE | HB6PN45W4J |
C0042665 | DB09185 | Y | Viloxazinum | FDA_UNII_CODE | 5I5Y2789ZF |
C0068700 | DB09220 | Y | Nicorandilum | FDA_UNII_CODE | 260456HAM0 |
C0037659 | DB09099 | Y | Somatostatine | FDA_UNII_CODE | 6E20216Q0L |
C0037659 | DB09099 | Y | Somatostatinum | FDA_UNII_CODE | 6E20216Q0L |

```
select con.CODE, GROUP_CONCAT(DISTINCT con.CUI), GROUP_CONCAT(DISTINCT CONCAT(con.ISPREF, '|', con.STR) SEPARATOR '\t'), GROUP_CONCAT(DISTINCT CONCAT(sat.ATN, '|', sat.ATV) SEPARATOR '\t') from MRCONSO con left join MRSAT sat on con.CODE=sat.CODE where con.SAB="DRUGBANK" GROUP BY con.CODE limit 10;
```

**NEED TO INCREASE MAX GROUP_CONCAT LENGTH FIRST**

**Had to use `\|` to display as a table**


CODE | GROUP_CONCAT(DISTINCT con.CUI) | GROUP_CONCAT(DISTINCT CONCAT(con.ISPREF, '\|', con.STR) SEPARATOR '\t') | GROUP_CONCAT(DISTINCT CONCAT(sat.ATN, '\|', sat.ATV) SEPARATOR '\t') |
--|--|--|--
DB00001 | C0378366,C0772394 | N\|Desulfatohirudin	N\|Lepirudin	Y\|Hirudin variant-1	Y\|Lepirudin recombinant	Y\|R-hirudin	Y\|[Leu1, Thr2]-63-desulfohirudin | FDA_UNII_CODE\|Y43GF64R34	RXAUI\|12740240	RXAUI\|12740241	RXAUI\|12740242	RXAUI\|8321260	RXAUI\|8471541	RXAUI\|8599806	RXCUI\|114934	RXCUI\|237057	SID\|BIOD00024	SID\|BTD00024 |
DB00002 | C0995188 | N\|Cetuximab	Y\|Cétuximab	Y\|Cetuximabum | FDA_UNII_CODE\|PQX0D8J21J	RXAUI\|8473993	RXAUI\|8692140	RXAUI\|8692141	RXCUI\|318341	SID\|BIOD00071	SID\|BTD00071 |
DB00003 | C1135662 | N\|Dornase alfa	Y\|Deoxyribonuclease (human clone 18-1 protein moiety)	Y\|Dornasa alfa	Y\|Dornase alfa, recombinant	Y\|Dornase alpha	Y\|Recombinant deoxyribonuclease (DNAse) | FDA_UNII_CODE\|953A26OA1Y	RXAUI\|10778765	RXAUI\|8278645	RXAUI\|8326085	RXAUI\|8339777	RXAUI\|8376403	RXAUI\|8686775	RXCUI\|337623	SID\|BIOD00001	SID\|BTD00001 |
DB00004 | C0717670,C1383469 | N\|Denileukin diftitox	Y\|Denileukin	Y\|Interleukin-2/diptheria toxin fusion protein | FDA_UNII_CODE\|25E79B5CTM	RXAUI\|10333971	RXAUI\|10333972	RXAUI\|8331268	RXCUI\|214470	RXCUI\|451876	SID\|BIOD00084	SID\|BTD00084 |
DB00005 | C0717758,C4291381,C4542001,C5135562 | N\|Etanercept	N\|etanercept-szzs	N\|etanercept-ykro	Y\|Recombinant human TNF	Y\|rhu TNFR:Fc	Y\|rhu-TNFR:Fc	Y\|TNFR-Immunoadhesin | FDA_UNII_CODE\|OP401G7OJC	RXAUI\|11350310	RXAUI\|11350311	RXAUI\|11350312	RXAUI\|11350313	RXAUI\|11350314	RXAUI\|8622888	RXAUI\|9712732	RXCUI\|1995554	RXCUI\|2103480	RXCUI\|214555	RXCUI\|2462511	SID\|BIOD00052	SID\|BTD00052 |
DB00006 | C0168273 | N\|Bivalirudin	Y\|Bivalirudina	Y\|Bivalirudinum | FDA_UNII_CODE\|TN9BEX005G	RXAUI\|8657293	RXAUI\|8715166	RXAUI\|8715167	RXCUI\|60819	SID\|BIOD00076	SID\|BTD00076	SID\|DB02351	SID\|EXPT03302 |
DB00007 | C0085272 | N\|Leuprolide	N\|Leuprorelin	Y\|Leuprorelina	Y\|Leuproreline	Y\|Leuprorelinum | FDA_UNII_CODE\|EFY6W0M8TG	RXAUI\|10785183	RXAUI\|10785184	RXAUI\|10785185	RXAUI\|8540224	RXAUI\|8646100	RXCUI\|42375	SID\|BIOD00009	SID\|BTD00009 |
DB00008 | C0391001 | N\|Peginterferon alfa-2a	Y\|PEG-IFN alfa-2A	Y\|PEG-Interferon alfa-2A	Y\|Pegylated Interfeaon alfa-2A	Y\|Pegylated interferon alfa-2a	Y\|Pegylated interferon alpha-2a	Y\|Pegylated-interferon alfa 2a | FDA_UNII_CODE\|Q46947FE7K	RXAUI\|11350315	RXAUI\|11350316	RXAUI\|11350317	RXAUI\|11350318	RXAUI\|11350319	RXAUI\|8672645	RXAUI\|8731057	RXCUI\|120608	SID\|BIOD00043	SID\|BTD00043 |
DB00009 | C0032143 | N\|Alteplase	N\|Tissue plasminogen activator	Y\|Alteplasa	Y\|Alteplase (genetical recombination)	Y\|Alteplase, recombinant	Y\|Alteplase,recombinant	Y\|Plasminogen activator (human tissue-type protein moiety)	Y\|rt-PA	Y\|t-PA	Y\|t-plasminogen activator	Y\|Tissue plasminogen activator alteplase	Y\|Tissue plasminogen activator, recombinant	Y\|tPA | FDA_UNII_CODE\|1RXS4UE564	RXAUI\|10778766	RXAUI\|8368173	RXAUI\|8383242	RXAUI\|8543112	RXAUI\|8578376	RXAUI\|9193634	RXAUI\|9193635	RXAUI\|9193636	RXAUI\|9193637	RXAUI\|9193638	RXAUI\|9193639	RXAUI\|9193640	RXAUI\|9193641	RXCUI\|8410	SID\|BIOD00050	SID\|BTD00050 |
DB00010 | C0142046 | N\|Sermorelin | FDA_UNII_CODE\|89243S03TE	RXAUI\|8619290	RXCUI\|56188	SID\|BIOD00033	SID\|BTD00033 |

Here is that first element in the `TTL` file:
```
<http://purl.bioontology.org/ontology/DRUGBANK/DB00001> a owl:Class ;
        skos:prefLabel """Lepirudin"""@en ;
        skos:notation """DB00001"""^^xsd:string ;
        skos:altLabel """Desulfatohirudin"""@en , """Hirudin variant-1"""@en , """Lepirudin recombinant"""@en , """R-hirudin"""@en , """[Leu1, Thr2]-63-desulfohirudin"""@en ;
        <http://purl.bioontology.org/ontology/DRUGBANK/SID> """BIOD00024"""^^xsd:string ;
        <http://purl.bioontology.org/ontology/DRUGBANK/FDA_UNII_CODE> """Y43GF64R34"""^^xsd:string ;
        <http://purl.bioontology.org/ontology/DRUGBANK/SID> """BTD00024"""^^xsd:string ;
        UMLS:has_cui """C0378366"""^^xsd:string ;
        UMLS:has_cui """C0772394"""^^xsd:string ;
        UMLS:has_tui """T116"""^^xsd:string ;
        UMLS:has_tui """T121"""^^xsd:string ;
        UMLS:has_sty <http://purl.bioontology.org/ontology/STY/T116> ;
        UMLS:has_sty <http://purl.bioontology.org/ontology/STY/T121> ;
```

Here is `DB00009` in the `TTL` file:
```
<http://purl.bioontology.org/ontology/DRUGBANK/DB00009> a owl:Class ;
        skos:prefLabel """Alteplase"""@en ;
        skos:notation """DB00009"""^^xsd:string ;
        skos:altLabel """Alteplasa"""@en , """Alteplase (genetical recombination)"""@en , """Alteplase, recombinant"""@en , """Alteplase,recombinant"""@en , """Plasminogen activator (human tissue-type protein moiety)"""@en , """Tissue plasminogen activator"""@en , """Tissue plasminogen activator alteplase"""@en , """Tissue plasminogen activator, recombinant"""@en , """rt-PA"""@en , """t-PA"""@en , """t-plasminogen activator"""@en , """tPA"""@en ;
        <http://purl.bioontology.org/ontology/DRUGBANK/FDA_UNII_CODE> """1RXS4UE564"""^^xsd:string ;
        <http://purl.bioontology.org/ontology/DRUGBANK/SID> """BIOD00050"""^^xsd:string ;
        <http://purl.bioontology.org/ontology/DRUGBANK/SID> """BTD00050"""^^xsd:string ;
        UMLS:has_cui """C0032143"""^^xsd:string ;
        UMLS:has_tui """T116"""^^xsd:string ;
        UMLS:has_tui """T121"""^^xsd:string ;
        UMLS:has_tui """T126"""^^xsd:string ;
        UMLS:has_sty <http://purl.bioontology.org/ontology/STY/T116> ;
        UMLS:has_sty <http://purl.bioontology.org/ontology/STY/T121> ;
        UMLS:has_sty <http://purl.bioontology.org/ontology/STY/T126> ;
```

I need to look more into how to tell which name is the correct name.

UMLS Source Predicates:
```
﻿[
  {
    "e.source_predicate": "UMLS:RB",
    "e.primary_knowledge_source": "infores:umls-metathesaurus",
    "count(e)": 235110
  },
  {
    "e.source_predicate": "UMLS:RO",
    "e.primary_knowledge_source": "infores:umls-metathesaurus",
    "count(e)": 722308
  },
  {
    "e.source_predicate": "UMLS:related_to",
    "e.primary_knowledge_source": "infores:medlineplus",
    "count(e)": 5658
  },
  {
    "e.source_predicate": "UMLS:RQ",
    "e.primary_knowledge_source": "infores:medlineplus",
    "count(e)": 3224
  },
  {
    "e.source_predicate": "UMLS:SY",
    "e.primary_knowledge_source": "infores:medlineplus",
    "count(e)": 932
  },
  {
    "e.source_predicate": "UMLS:mapped_to",
    "e.primary_knowledge_source": "infores:medlineplus",
    "count(e)": 1008
  },
  {
    "e.source_predicate": "UMLS:exhibited_by",
    "e.primary_knowledge_source": "infores:umls-metathesaurus",
    "count(e)": 2332
  },
  {
    "e.source_predicate": "UMLS:has_structural_class",
    "e.primary_knowledge_source": "infores:medrt-umls",
    "count(e)": 4
  },
  {
    "e.source_predicate": "UMLS:has_mapping_qualifier",
    "e.primary_knowledge_source": "infores:medlineplus",
    "count(e)": 42
  },
  {
    "e.source_predicate": "UMLS:measures",
    "e.primary_knowledge_source": "infores:umls-metathesaurus",
    "count(e)": 406
  },
  {
    "e.source_predicate": "UMLS:owning_subsection_of",
    "e.primary_knowledge_source": "infores:hl7-umls",
    "count(e)": 84
  },
  {
    "e.source_predicate": "UMLS:has_supported_concept_property",
    "e.primary_knowledge_source": "infores:hl7-umls",
    "count(e)": 738
  },
  {
    "e.source_predicate": "UMLS:has_supported_concept_relationship",
    "e.primary_knowledge_source": "infores:hl7-umls",
    "count(e)": 648
  },
  {
    "e.source_predicate": "UMLS:class_code_classified_by",
    "e.primary_knowledge_source": "infores:hl7-umls",
    "count(e)": 122
  },
  {
    "e.source_predicate": "UMLS:owning_section_of",
    "e.primary_knowledge_source": "infores:hl7-umls",
    "count(e)": 18
  },
  {
    "e.source_predicate": "UMLS:has_context_binding",
    "e.primary_knowledge_source": "infores:hl7-umls",
    "count(e)": 134
  },
  {
    "e.source_predicate": "UMLS:may_be_qualified_by",
    "e.primary_knowledge_source": "infores:hl7-umls",
    "count(e)": 40
  },
  {
    "e.source_predicate": "UMLS:larger_than",
    "e.primary_knowledge_source": "infores:hl7-umls",
    "count(e)": 2
  },
  {
    "e.source_predicate": "UMLS:component_of",
    "e.primary_knowledge_source": "infores:hl7-umls",
    "count(e)": 28
  },
  {
    "e.source_predicate": "UMLS:has_component",
    "e.primary_knowledge_source": "infores:hl7-umls",
    "count(e)": 18
  },
  {
    "e.source_predicate": "UMLS:has_owning_affiliate",
    "e.primary_knowledge_source": "infores:hl7-umls",
    "count(e)": 2
  },
  {
    "e.source_predicate": "UMLS:has_physiologic_effect",
    "e.primary_knowledge_source": "infores:medrt-umls",
    "count(e)": 2
  },
  {
    "e.source_predicate": "UMLS:has_form",
    "e.primary_knowledge_source": "infores:umls-metathesaurus",
    "count(e)": 2
  }
]
```