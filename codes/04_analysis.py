import csv
import sqlite3
import numpy as np
import matplotlib.pyplot as plt


def main():
    db_con = sqlite3.connect('../enade.db')

    first_question(db_con)
    second_question(db_con)
    third_question(db_con)
    fourth_question(db_con)
    fifth_question(db_con)

    db_con.close()


def first_question(db_con):
    cur = db_con.cursor()

    execute_query(cur, '''select TIPO_SEXO, NOTA_GERAL from EXAME join ALUNO on EXAME.ID_ALUNO = ALUNO.ID_INSCRICAO join NOTAS on EXAME.ID_NOTA = NOTAS.ID_NOTA where NOTA_GERAL is not NULL''')

    query_result = cur.fetchall()

    header = ['gender', 'grade']
    rows = get_rows_from_query_result(query_result, header)

    write_rows_to_csv('genero-nota', header, rows)
    
    female_grades = []
    male_grades = []
    
    for row in rows:
        if row['gender'] == 'F':
            female_grades.append(row['grade'])
        elif row['gender'] == 'M':
            male_grades.append(row['grade'])
        else:
            print(f"Unhandled gender: '{row['gender']}'")
        
    plot_data = [female_grades, male_grades]

    generate_box_plot('genero-nota', 'Distribuição de notas por gênero', 'Gênero', ['F', 'M'], plot_data)

def second_question(db_con):
    cur = db_con.cursor()

    execute_query(cur, '''select Q_SOCIOEC_02, NOTA_GERAL from EXAME join SOCIOECONOMICO on EXAME.ID_SOCIOECON = SOCIOECONOMICO.ID_SOC join NOTAS on EXAME.ID_NOTA = NOTAS.ID_NOTA 
            where Q_SOCIOEC_02 is not NULL and Q_SOCIOEC_02 != ' ' and NOTA_GERAL is not NULL''')

    query_result = cur.fetchall()

    header = ['race', 'grade']
    rows = get_rows_from_query_result(query_result, header)
    
    write_rows_to_csv('raca-notas', header, rows)

    A_grades = []
    B_grades = []
    C_grades = []
    D_grades = []
    E_grades = []
    F_grades = []
    
    for row in rows:
        if row['race'] == 'A':
            A_grades.append(row['grade'])
        elif row['race'] == 'B':
            B_grades.append(row['grade'])
        elif row['race'] == 'C':
            C_grades.append(row['grade'])
        elif row['race'] == 'D':
            D_grades.append(row['grade'])
        elif row['race'] == 'E':
            E_grades.append(row['grade'])
        elif row['race'] == 'F':
            F_grades.append(row['grade'])
        else:
            print(f"Unhandled race: '{row['race']}'")
        
    plot_labels = ['Branca', 'Preta', 'Amarela', 'Parda', 'Indígena', 'NQD']
    plot_data = [A_grades, B_grades, C_grades, D_grades, E_grades, F_grades]

    generate_box_plot('raca-notas', 'Distribuição de notas por raça', 'Raça', plot_labels, plot_data)

def third_question(db_con):
    cur = db_con.cursor()

    execute_query(cur, '''select CO_REGIAO_CURSO, NOTA_GERAL from EXAME join CURSO on EXAME.ID_CURSO = CURSO.ID_CURSO join NOTAS on EXAME.ID_NOTA = NOTAS.ID_NOTA
            where CO_REGIAO_CURSO is not NULL and NOTA_GERAL is not NULL''')

    query_result = cur.fetchall()

    header = ['region', 'grade']
    rows = get_rows_from_query_result(query_result, header)
    
    write_rows_to_csv('regiao-notas', header, rows)

    N_grades = []
    NE_grades = []
    SE_grades = []
    S_grades = []
    C_O_grades = []

    for row in rows:
        if row['region'] == 1:
            N_grades.append(row['grade'])
        elif row['region'] == 2:
            NE_grades.append(row['grade'])
        elif row['region'] == 3:
            SE_grades.append(row['grade'])
        elif row['region'] == 4:
            S_grades.append(row['grade'])
        elif row['region'] == 5:
            C_O_grades.append(row['grade'])
        else:
            print(f"Unhandled region: '{row['region']}'")
    
    plot_labels = ['Norte', 'Nordeste', 'Sudeste', 'Sul', 'Centro-Oeste']
    plot_data = [N_grades, NE_grades, SE_grades, S_grades, C_O_grades]

    generate_box_plot('regiao-notas', 'Distribuição de notas por região', 'Região', plot_labels, plot_data)

def fourth_question(db_con):
    cur = db_con.cursor()

    execute_query(cur, '''select Q_SOCIOEC_08, count(*) as TOTAL from EXAME
            join SOCIOECONOMICO on EXAME.ID_SOCIOECON = SOCIOECONOMICO.ID_SOC
            join CURSO on EXAME.ID_CURSO = CURSO.ID_CURSO
            where CO_REGIAO_CURSO = 1 and Q_SOCIOEC_08 is not NULL and Q_SOCIOEC_08 != ' '
            group by Q_SOCIOEC_08
            order by Q_SOCIOEC_08 ASC''')

    norte = cur.fetchall()

    execute_query(cur, '''select Q_SOCIOEC_08, count(*) as TOTAL from EXAME
            join SOCIOECONOMICO on EXAME.ID_SOCIOECON = SOCIOECONOMICO.ID_SOC
            join CURSO on EXAME.ID_CURSO = CURSO.ID_CURSO
            where CO_REGIAO_CURSO = 2 and Q_SOCIOEC_08 is not NULL and Q_SOCIOEC_08 != ' '
            group by Q_SOCIOEC_08
            order by Q_SOCIOEC_08 ASC''')

    nordeste = cur.fetchall()

    execute_query(cur, '''select Q_SOCIOEC_08, count(*) as TOTAL from EXAME
            join SOCIOECONOMICO on EXAME.ID_SOCIOECON = SOCIOECONOMICO.ID_SOC
            join CURSO on EXAME.ID_CURSO = CURSO.ID_CURSO
            where CO_REGIAO_CURSO = 3 and Q_SOCIOEC_08 is not NULL and Q_SOCIOEC_08 != ' '
            group by Q_SOCIOEC_08
            order by Q_SOCIOEC_08 ASC''')

    sudeste = cur.fetchall()

    execute_query(cur, '''select Q_SOCIOEC_08, count(*) as TOTAL from EXAME
            join SOCIOECONOMICO on EXAME.ID_SOCIOECON = SOCIOECONOMICO.ID_SOC
            join CURSO on EXAME.ID_CURSO = CURSO.ID_CURSO
            where CO_REGIAO_CURSO = 4 and Q_SOCIOEC_08 is not NULL and Q_SOCIOEC_08 != ' '
            group by Q_SOCIOEC_08
            order by Q_SOCIOEC_08 ASC''')

    sul = cur.fetchall()

    execute_query(cur, '''select Q_SOCIOEC_08, count(*) as TOTAL from EXAME
            join SOCIOECONOMICO on EXAME.ID_SOCIOECON = SOCIOECONOMICO.ID_SOC
            join CURSO on EXAME.ID_CURSO = CURSO.ID_CURSO
            where CO_REGIAO_CURSO = 5 and Q_SOCIOEC_08 is not NULL and Q_SOCIOEC_08 != ' '
            group by Q_SOCIOEC_08
            order by Q_SOCIOEC_08 ASC''')

    centro_oeste = cur.fetchall()


    header = ['wage', 'total']
    norte_rows = get_rows_from_query_result(norte, header)
    nordeste_rows = get_rows_from_query_result(nordeste, header)
    sudeste_rows = get_rows_from_query_result(sudeste, header)
    sul_rows = get_rows_from_query_result(sul, header)
    centro_oeste_rows = get_rows_from_query_result(centro_oeste, header)
    
    write_rows_to_csv('renda-regiao-norte', header, norte_rows)
    write_rows_to_csv('renda-regiao-nordeste', header, nordeste_rows)
    write_rows_to_csv('renda-regiao-sudeste', header, sudeste_rows)
    write_rows_to_csv('renda-regiao-sul', header, sul_rows)
    write_rows_to_csv('renda-regiao-centro-oeste', header, centro_oeste_rows)

    
    category_names = ['Até 1,5 s.m.', 'De 1,5 a 3 s.m.', 'De 3 a 4,5 s.m.', 'De 4,5 a 6 s.m.', 'De 6 a 10 s.m.', 'De 10 a 30 s.m.', 'Acima de 30 s.m.']
    
    total_norte = sum([r['total'] for r in norte_rows]) 
    total_nodeste = sum([r['total'] for r in nordeste_rows])
    total_sudeste = sum([r['total'] for r in sudeste_rows])
    total_sul = sum([r['total'] for r in sul_rows])
    total_centro_oeste = sum([r['total'] for r in centro_oeste_rows])

    results = {
        'Norte': [100 * row['total'] / total_norte for row in norte_rows],
        'Nordeste': [100 * row['total'] / total_nodeste for row in nordeste_rows],
        'Sudeste': [100 * row['total'] / total_sudeste for row in sudeste_rows],
        'Sul': [100 * row['total'] / total_sul for row in sul_rows],
        'Centro-Oeste': [100 * row['total'] / total_centro_oeste for row in centro_oeste_rows]
    }

    horizontal_bars_chart('renda-regiao', 'cool', results, category_names)


def fifth_question(db_con):
    cur = db_con.cursor()

    execute_query(cur, '''select Q_SOCIOEC_15, count(*) as TOTAL from EXAME
            join SOCIOECONOMICO on EXAME.ID_SOCIOECON = SOCIOECONOMICO.ID_SOC
            join CURSO on EXAME.ID_CURSO = CURSO.ID_CURSO
            where CO_REGIAO_CURSO = 1 and Q_SOCIOEC_15 is not NULL and Q_SOCIOEC_15 != ' '
            group by Q_SOCIOEC_15
            order by Q_SOCIOEC_15 ASC''')

    norte = cur.fetchall()

    execute_query(cur, '''select Q_SOCIOEC_15, count(*) as TOTAL from EXAME
            join SOCIOECONOMICO on EXAME.ID_SOCIOECON = SOCIOECONOMICO.ID_SOC
            join CURSO on EXAME.ID_CURSO = CURSO.ID_CURSO
            where CO_REGIAO_CURSO = 2 and Q_SOCIOEC_15 is not NULL and Q_SOCIOEC_15 != ' '
            group by Q_SOCIOEC_15
            order by Q_SOCIOEC_15 ASC''')

    nordeste = cur.fetchall()

    execute_query(cur, '''select Q_SOCIOEC_15, count(*) as TOTAL from EXAME
            join SOCIOECONOMICO on EXAME.ID_SOCIOECON = SOCIOECONOMICO.ID_SOC
            join CURSO on EXAME.ID_CURSO = CURSO.ID_CURSO
            where CO_REGIAO_CURSO = 3 and Q_SOCIOEC_15 is not NULL and Q_SOCIOEC_15 != ' '
            group by Q_SOCIOEC_15
            order by Q_SOCIOEC_15 ASC''')

    sudeste = cur.fetchall()

    execute_query(cur, '''select Q_SOCIOEC_15, count(*) as TOTAL from EXAME
            join SOCIOECONOMICO on EXAME.ID_SOCIOECON = SOCIOECONOMICO.ID_SOC
            join CURSO on EXAME.ID_CURSO = CURSO.ID_CURSO
            where CO_REGIAO_CURSO = 4 and Q_SOCIOEC_15 is not NULL and Q_SOCIOEC_15 != ' '
            group by Q_SOCIOEC_15
            order by Q_SOCIOEC_15 ASC''')

    sul = cur.fetchall()

    execute_query(cur, '''select Q_SOCIOEC_15, count(*) as TOTAL from EXAME
            join SOCIOECONOMICO on EXAME.ID_SOCIOECON = SOCIOECONOMICO.ID_SOC
            join CURSO on EXAME.ID_CURSO = CURSO.ID_CURSO
            where CO_REGIAO_CURSO = 5 and Q_SOCIOEC_15 is not NULL and Q_SOCIOEC_15 != ' '
            group by Q_SOCIOEC_15
            order by Q_SOCIOEC_15 ASC''')

    centro_oeste = cur.fetchall()


    header = ['class', 'total']
    norte_rows = get_rows_from_query_result(norte, header)
    nordeste_rows = get_rows_from_query_result(nordeste, header)
    sudeste_rows = get_rows_from_query_result(sudeste, header)
    sul_rows = get_rows_from_query_result(sul, header)
    centro_oeste_rows = get_rows_from_query_result(centro_oeste, header)
    
    write_rows_to_csv('cota-regiao-norte', header, norte_rows)
    write_rows_to_csv('cota-regiao-nordeste', header, nordeste_rows)
    write_rows_to_csv('cota-regiao-sudeste', header, sudeste_rows)
    write_rows_to_csv('cota-regiao-sul', header, sul_rows)
    write_rows_to_csv('cota-regiao-centro-oeste', header, centro_oeste_rows)

    
    category_names = ['Nâo', 'Étnico-racial', 'Renda', 'Escola pública ou particular c/ bolsa', 'Dois ou mais critérios anteriores', 'Sistema diferente dos anteriores']
    
    total_norte = sum([r['total'] for r in norte_rows]) 
    total_nodeste = sum([r['total'] for r in nordeste_rows])
    total_sudeste = sum([r['total'] for r in sudeste_rows])
    total_sul = sum([r['total'] for r in sul_rows])
    total_centro_oeste = sum([r['total'] for r in centro_oeste_rows])

    results = {
        'Norte': [100 * row['total'] / total_norte for row in norte_rows],
        'Nordeste': [100 * row['total'] / total_nodeste for row in nordeste_rows],
        'Sudeste': [100 * row['total'] / total_sudeste for row in sudeste_rows],
        'Sul': [100 * row['total'] / total_sul for row in sul_rows],
        'Centro-Oeste': [100 * row['total'] / total_centro_oeste for row in centro_oeste_rows]
    }

    horizontal_bars_chart('cota-regiao', 'plasma', results, category_names)

def get_rows_from_query_result(query_result, header):
    result = []
    for row in query_result:
        row_dict = dict([(header[i], row[i]) for i in range(len(header))])
        result.append(row_dict)

    return result

def generate_box_plot(filename, title, xlabel, tick_labels, data):
    fig1, ax = plt.subplots()
    
    ax.set_title(title)
    ax.set_xlabel(xlabel, fontsize=8)
    ax.set_xticklabels(tick_labels)

    ax.boxplot(data)

    plt.savefig(f'../data-analysis/{filename}.png')

# Reference: https://matplotlib.org/stable/gallery/lines_bars_and_markers/horizontal_barchart_distribution.html
def horizontal_bars_chart(filename, colormap, results, category_names):
    labels = list(results.keys())
    data = np.array(list(results.values()))

    data_cum = data.cumsum(axis=1)
    
    category_colors = plt.colormaps[colormap](
        np.linspace(0.15, 0.85, data.shape[1]))

    fig, ax = plt.subplots(figsize=(19, 5))
    ax.invert_yaxis()
    ax.xaxis.set_visible(False)
    ax.set_xlim(0, np.sum(data, axis=1).max())

    for i, (colname, color) in enumerate(zip(category_names, category_colors)):
        widths = data[:, i]
        starts = data_cum[:, i] - widths
        rects = ax.barh(labels, widths, left=starts, height=0.5,
                        label=colname, color=color)

        r, g, b, _ = color
        text_color = 'white' if r * g * b < 0.5 else 'darkgrey'
        ax.bar_label(rects, fmt='%.2f', label_type='center', color=text_color)
    ax.legend(ncol=len(category_names), bbox_to_anchor=(0, 1),
              loc='lower left', fontsize='small')

    
    plt.savefig(f'../data-analysis/{filename}.png')


def write_rows_to_csv(filename, header, rows):
    with open(f'../data-analysis/{filename}.csv', 'w', newline='') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=header)

        writer.writeheader()
        writer.writerows(rows)

def execute_query(cur, query):
    try:
        return cur.execute(query)   
    except:
        print('Query:', query)
        raise
  

if __name__ == '__main__':
    main()