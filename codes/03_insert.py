import csv
import sqlite3

enade_2017_csv_path = '../microdados/2017/3.DADOS/MICRODADOS_ENADE_2017.txt'
enade_2018_csv_path = '../microdados/2018/3.DADOS/microdados_enade_2018.txt'
enade_2019_csv_path = '../microdados/2019/3.DADOS/microdados_enade_2019.txt'



def main():
    enade = get_enade_rows()

    db_con = sqlite3.connect('../enade.db')

    insert_rows_into_db(db_con, enade)

    db_con.close()

def insert_rows_into_db(db_con, rows):
    cur = db_con.cursor()

    for row in rows:
        execute_query(cur, f'''INSERT OR IGNORE INTO INSTITUICAO (ID_IES, CO_CATEG_ADM, CO_ORG_ACAD) VALUES
            ({get_int_value(row.get('CO_IES'))}, {get_int_value(row.get('CO_CATEGAD'))}, {get_int_value(row.get('CO_ORGACAD'))})''')

        execute_query(cur, f'''INSERT INTO RESPOSTAS (RESP_ESC_ALUNO_OBJ_FORMGERAL, RESP_ACERTO_OBJ_FORMGERAL, RESP_ESC_ALUNO_OBJ_COMP_ESPEC, RESP_ACERTO_OBJ_COMP_ESPEC) VALUES
            ({get_text_value(row.get('DS_VT_ESC_OFG'))}, {get_text_value(row.get('DS_VT_ACE_OFG'))}, {get_text_value(row.get('DS_VT_ESC_OCE'))}, {get_text_value(row.get('DS_VT_ACE_OCE'))})''')

        id_resp = cur.lastrowid

        execute_query(cur, f'''INSERT OR IGNORE INTO CURSO (ID_CURSO, CO_GRUPO, CO_MUNIC_CURSO, CO_UF_CURSO, CO_REGIAO_CURSO) VALUES
            ({get_int_value(row.get('CO_CURSO'))}, {get_int_value(row.get('CO_GRUPO'))}, {get_int_value(row.get('CO_MUNIC_CURSO'))}, {get_int_value(row.get('CO_UF_CURSO'))}, {get_int_value(row.get('CO_REGIAO_CURSO'))})''')

        execute_query(cur, f'''INSERT INTO GABARITO (GAB_OBJ_FORMGERAL_ORIG, GAB_OBJ_FORMGERAL_FINAL, GAB_OBJ_COMP_ESPEC_ORIG, GAB_OBJ_COMP_ESPEC_FINAL) VALUES
            ({get_text_value(row.get('DS_VT_GAB_OFG_ORIG'))}, {get_text_value(row.get('DS_VT_GAB_OFG_FIN'))}, {get_text_value(row.get('DS_VT_GAB_OCE_ORIG'))}, {get_text_value(row.get('DS_VT_GAB_OCE_FIN'))})''')

        id_gab = cur.lastrowid

        execute_query(cur, f'''INSERT INTO DISCURSIVA (TIPO_SITU_FORMGERAL_D1, TIPO_SITU_FORMGERAL_D2, TIPO_SITU_COMP_ESPEC_D1, TIPO_SITU_COMP_ESPEC_D2, TIPO_SITU_COMP_ESPEC_D3) VALUES
            ({get_int_value(row.get('TP_SFG_D1'))}, {get_int_value(row.get('TP_SFG_D2'))}, {get_int_value(row.get('TP_SCE_D1'))}, {get_int_value(row.get('TP_SCE_D2'))}, {get_int_value(row.get('TP_SCE_D3'))})''')

        id_dis = cur.lastrowid

        execute_query(cur, f'''INSERT INTO OBJETIVA (NUM_ITENS_OBJ_FORMGERAL, NUM_ITENS_OBJ_FORMGERAL_ANULADOS, NUM_ITENS_OBJ_FORMGERAL_COEFBAIXO, NUM_ITENS_OBJ_FORMGERAL_N_APLICA, NUM_ITENS_OBJ_COMP_ESPEC, 
        NUM_ITENS_OBJ_COMP_ESPEC_ANULADOS, NUM_ITENS_OBJ_COMP_ESPEC_COEFBAIXO, NUM_ITENS_OBJ_COMP_ESPEC_N_APLICA) VALUES
            ({get_int_value(row.get('NU_ITEM_OFG'))}, {get_int_value(row.get('NU_ITEM_OFG_Z'))}, {get_int_value(row.get('NU_ITEM_OFG_X'))}, {get_int_value(row.get('NU_ITEM_OFG_N'))}, 
            {get_int_value(row.get('NU_ITEM_OCE'))}, {get_int_value(row.get('NU_ITEM_OCE_Z'))}, {get_int_value(row.get('NU_ITEM_OCE_X'))}, {get_int_value(row.get('NU_ITEM_OCE_N'))})''')

        id_obj = cur.lastrowid

        execute_query(cur, f'''INSERT INTO PERCEPCAO_PROVA (Q_PERCEP_PROVA_1, Q_PERCEP_PROVA_2, Q_PERCEP_PROVA_3, Q_PERCEP_PROVA_4, Q_PERCEP_PROVA_5, Q_PERCEP_PROVA_6, Q_PERCEP_PROVA_7, Q_PERCEP_PROVA_8, Q_PERCEP_PROVA_9) VALUES
            ({get_text_value(row.get('CO_RS_I1'))}, {get_text_value(row.get('CO_RS_I2'))}, {get_text_value(row.get('CO_RS_I3'))}, {get_text_value(row.get('CO_RS_I4'))}, {get_text_value(row.get('CO_RS_I5'))}, 
            {get_text_value(row.get('CO_RS_I6'))}, {get_text_value(row.get('CO_RS_I7'))}, {get_text_value(row.get('CO_RS_I8'))}, {get_text_value(row.get('CO_RS_I9'))})''')

        id_prv = cur.lastrowid

        execute_query(cur, f'''INSERT INTO ALUNO (NUM_IDADE, TIPO_SEXO, ANO_FIM_EM, ANO_INIC_GRAD, CO_TURNO_GRADUACAO, TIPO_INSCRICAO_ADM, TIPO_INSCRICAO, CODIGO_MODALIDADE_ENSINO) VALUES
            ({get_int_value(row.get('NU_IDADE'))}, {get_text_value(row.get('TP_SEXO'))}, {get_int_value(row.get('ANO_FIM_EM'))}, {get_int_value(row.get('ANO_IN_GRAD'))}, {get_int_value(row.get('CO_TURNO_GRADUACAO'))}, 
            {get_int_value(row.get('TP_INSCRICAO_ADM'))}, {get_int_value(row.get('TP_INSCRICAO'))}, {get_int_value(row.get('CO_MODALIDADE'))})''')
        
        id_inscricao = cur.lastrowid

        execute_query(cur, f'''INSERT INTO LICENCIATURA (Q_LICEN_69, Q_LICEN_70, Q_LICEN_71, Q_LICEN_72, Q_LICEN_73, Q_LICEN_74, Q_LICEN_75, Q_LICEN_76, Q_LICEN_77, Q_LICEN_78, Q_LICEN_79, Q_LICEN_80, Q_LICEN_81) VALUES
            ({get_text_value(row.get('QE_I69'))}, {get_text_value(row.get('QE_I70'))}, {get_text_value(row.get('QE_I71'))}, {get_text_value(row.get('QE_I72'))}, {get_text_value(row.get('QE_I73'))}, 
            {get_text_value(row.get('QE_I74'))}, {get_text_value(row.get('QE_I75'))}, {get_text_value(row.get('QE_I76'))}, {get_text_value(row.get('QE_I77'))}, {get_text_value(row.get('QE_I78'))},  
            {get_text_value(row.get('QE_I79'))},  {get_text_value(row.get('QE_I80'))},  {get_text_value(row.get('QE_I81'))})''')
        
        id_lic = cur.lastrowid    
        
        execute_query(cur, f'''INSERT INTO PRESENCA (TIPO_PRESENCA_GERAL, TIPO_PRESENCA_OBJ_FORMGERAL, TIPO_PRESENCA_DISC_FORMGERAL, TIPO_PRESENCA_OBJ_COMP_ESPEC, TIPO_PRESENCA_DISC_COMP_ESPEC) VALUES
            ({get_int_value(row.get('TP_PR_GER'))}, {get_int_value(row.get('TP_PR_OB_FG'))}, {get_int_value(row.get('TP_PR_DI_FG'))}, {get_int_value(row.get('TP_PR_OB_CE'))}, {get_int_value(row.get('TP_PR_DI_CE'))})''')
        
        id_pres = cur.lastrowid   

        execute_query(cur, f'''INSERT INTO NOTAS (NOTA_GERAL, NOTA_FORMGERAL, NOTA_OBJ_FORMGERAL, NOTA_DISC_FORMGERAL, NOTA_FORMGERAL_D1, NOTA_FORMGERAL_D1_PT, NOTA_FORMGERAL_D1_CT, NOTA_FORMGERAL_D2, 
            NOTA_FORMGERAL_D2_PT, NOTA_FORMGERAL_D2_CT, NOTA_COMP_ESPEC, NOTA_OBJ_COMP_ESPEC, NOTA_DIS_COMP_ESPEC, NOTA_COMP_ESPEC_D1, NOTA_COMP_ESPEC_D2, NOTA_COMP_ESPEC_D3) VALUES
            ({get_real_value(row.get('NT_GER'))}, {get_real_value(row.get('NT_FG'))}, {get_real_value(row.get('NT_OBJ_FG'))}, {get_real_value(row.get('NT_DIS_FG'))}, {get_real_value(row.get('NT_FG_D1'))}, 
            {get_real_value(row.get('NT_FG_D1_PT'))}, {get_real_value(row.get('NT_FG_D1_CT'))}, {get_real_value(row.get('NT_FG_D2'))}, {get_real_value(row.get('NT_FG_D2_PT'))}, 
            {get_real_value(row.get('NT_FG_D2_CT'))},  {get_real_value(row.get('NT_CE'))},  {get_real_value(row.get('NT_OBJ_CE'))}, {get_real_value(row.get('NT_DIS_CE'))}, 
            {get_real_value(row.get('NT_CE_D1'))}, {get_real_value(row.get('NT_CE_D2'))}, {get_real_value(row.get('NT_CE_D3'))})''')
        
        id_nt = cur.lastrowid

        execute_query(cur, f'''INSERT INTO SOCIOECONOMICO (Q_SOCIOEC_01, Q_SOCIOEC_02, Q_SOCIOEC_03, Q_SOCIOEC_04, Q_SOCIOEC_05, Q_SOCIOEC_06, Q_SOCIOEC_07, Q_SOCIOEC_08, Q_SOCIOEC_09, Q_SOCIOEC_10, Q_SOCIOEC_11, Q_SOCIOEC_12, Q_SOCIOEC_13, Q_SOCIOEC_14, Q_SOCIOEC_15, Q_SOCIOEC_16, 
            Q_SOCIOEC_17, Q_SOCIOEC_18, Q_SOCIOEC_19, Q_SOCIOEC_20, Q_SOCIOEC_21, Q_SOCIOEC_22, Q_SOCIOEC_23, Q_SOCIOEC_24, Q_SOCIOEC_25, Q_SOCIOEC_26, Q_SOCIOEC_27, Q_SOCIOEC_28, Q_SOCIOEC_29, Q_SOCIOEC_30, Q_SOCIOEC_31, Q_SOCIOEC_32, Q_SOCIOEC_33, Q_SOCIOEC_34, Q_SOCIOEC_35, Q_SOCIOEC_36, 
            Q_SOCIOEC_37, Q_SOCIOEC_38, Q_SOCIOEC_39, Q_SOCIOEC_40, Q_SOCIOEC_41, Q_SOCIOEC_42, Q_SOCIOEC_43, Q_SOCIOEC_44, Q_SOCIOEC_45, Q_SOCIOEC_46, Q_SOCIOEC_47, Q_SOCIOEC_48, Q_SOCIOEC_49, Q_SOCIOEC_50, Q_SOCIOEC_51, Q_SOCIOEC_52, Q_SOCIOEC_53, Q_SOCIOEC_54, Q_SOCIOEC_55,
            Q_SOCIOEC_56, Q_SOCIOEC_57, Q_SOCIOEC_58, Q_SOCIOEC_59, Q_SOCIOEC_60, Q_SOCIOEC_61, Q_SOCIOEC_62, Q_SOCIOEC_63, Q_SOCIOEC_64, Q_SOCIOEC_65, Q_SOCIOEC_66, Q_SOCIOEC_67, Q_SOCIOEC_68) VALUES
            ({get_text_value(row.get('QE_I01'))}, {get_text_value(row.get('QE_I02'))}, {get_text_value(row.get('QE_I03'))}, {get_text_value(row.get('QE_I04'))}, {get_text_value(row.get('QE_I05'))}, 
            {get_text_value(row.get('QE_I06'))}, {get_text_value(row.get('QE_I07'))}, {get_text_value(row.get('QE_I08'))}, {get_text_value(row.get('QE_I09'))}, {get_text_value(row.get('QE_I10'))}, 
            {get_text_value(row.get('QE_I11'))}, {get_text_value(row.get('QE_I12'))}, {get_text_value(row.get('QE_I13'))}, {get_text_value(row.get('QE_I14'))}, {get_text_value(row.get('QE_I15'))}, 
            {get_int_value(row.get('QE_I16'))}, {get_text_value(row.get('QE_I17'))}, {get_text_value(row.get('QE_I18'))}, {get_text_value(row.get('QE_I19'))}, {get_text_value(row.get('QE_I20'))}, 
            {get_text_value(row.get('QE_I21'))}, {get_text_value(row.get('QE_I22'))}, {get_text_value(row.get('QE_I23'))}, {get_text_value(row.get('QE_I24'))}, {get_text_value(row.get('QE_I25'))}, 
            {get_text_value(row.get('QE_I26'))}, {get_int_value(row.get('QE_I27'))}, {get_int_value(row.get('QE_I28'))}, {get_int_value(row.get('QE_I29'))}, {get_int_value(row.get('QE_I30'))}, 
            {get_int_value(row.get('QE_I31'))}, {get_int_value(row.get('QE_I32'))}, {get_int_value(row.get('QE_I33'))}, {get_int_value(row.get('QE_I34'))}, {get_int_value(row.get('QE_I35'))}, 
            {get_int_value(row.get('QE_I36'))}, {get_int_value(row.get('QE_I37'))}, {get_int_value(row.get('QE_I38'))}, {get_int_value(row.get('QE_I39'))}, {get_int_value(row.get('QE_I40'))}, 
            {get_int_value(row.get('QE_I41'))}, {get_int_value(row.get('QE_I42'))}, {get_int_value(row.get('QE_I43'))}, {get_int_value(row.get('QE_I44'))}, {get_int_value(row.get('QE_I45'))}, 
            {get_int_value(row.get('QE_I46'))}, {get_int_value(row.get('QE_I47'))}, {get_int_value(row.get('QE_I48'))}, {get_int_value(row.get('QE_I49'))}, {get_int_value(row.get('QE_I50'))}, 
            {get_int_value(row.get('QE_I51'))}, {get_int_value(row.get('QE_I52'))}, {get_int_value(row.get('QE_I53'))}, {get_int_value(row.get('QE_I54'))}, {get_int_value(row.get('QE_I55'))}, 
            {get_int_value(row.get('QE_I56'))}, {get_int_value(row.get('QE_I57'))}, {get_int_value(row.get('QE_I58'))}, {get_int_value(row.get('QE_I59'))}, {get_int_value(row.get('QE_I60'))}, 
            {get_int_value(row.get('QE_I61'))}, {get_int_value(row.get('QE_I62'))}, {get_int_value(row.get('QE_I63'))}, {get_int_value(row.get('QE_I64'))}, {get_int_value(row.get('QE_I65'))}, 
            {get_int_value(row.get('QE_I66'))}, {get_int_value(row.get('QE_I67'))}, {get_int_value(row.get('QE_I68'))})''')
        
        id_soc = cur.lastrowid

        execute_query(cur, f'''INSERT INTO EXAME (ID_IES, ID_CURSO, ID_ALUNO, ID_NOTA, ID_GABARITO, ID_OBJETIVAS, ID_DISCURSIVAS, ID_LICENCIATURA, ID_SOCIOECON, ID_RESPOSTAS, ID_PRESENCA, ID_PROVA, NUM_ANO, TIPO_PRESENCA) VALUES
            ({row.get('CO_IES')}, {row.get('CO_CURSO')}, {id_inscricao}, {id_nt}, {id_gab}, {id_obj}, {id_dis}, {id_lic},
             {id_soc}, {id_resp}, {id_pres}, {id_prv}, {get_int_value(row.get('NU_ANO'))}, {get_int_value(row.get('TP_PRES'))})''')
        
        print(cur.lastrowid)

    db_con.commit()

def execute_query(cur, query):
    try:
        cur.execute(query)   
    except:
        print('Query:', query)
        raise

def get_enade_rows():
    enade = []

    enade_2017 = None
    enade_2018 = None
    enade_2019 = None

    
    enade_2017_csv = open(enade_2017_csv_path, newline='')
    enade_2018_csv = open(enade_2018_csv_path, newline='')
    enade_2019_csv = open(enade_2019_csv_path, newline='')

    dialect = csv.Sniffer().sniff(enade_2017_csv.read(10240))
    enade_2017_csv.seek(0)

    enade_2017 = csv.DictReader(enade_2017_csv, dialect=dialect)
    enade_2018 = csv.DictReader(enade_2018_csv, dialect=dialect)
    enade_2019 = csv.DictReader(enade_2019_csv, dialect=dialect)

    enade.extend(enade_2017)
    enade.extend(enade_2018)
    enade.extend(enade_2019)

    return enade

def get_text_value(val):
    if val == None or val == '':
        return 'null'
    
    return f"'{val}'"

def get_int_value(val):
    if val == None:
        return 'null'
    
    val = val.strip()
    if val == '' or val == 'NA':
        return 'null'

    return val

def get_real_value(val):
    if val == None:
        return 'null'

    val = val.strip()
    if val == '' or val == 'NA':
        return 'null'

    return val.replace(',', '.')    

if __name__ == '__main__':
    main()