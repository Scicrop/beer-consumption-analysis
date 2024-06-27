import pandas as pd

def gen_holidays():
    feriados = {
        "data": ["2015-01-01", "2015-02-16", "2015-02-17", "2015-04-03", "2015-04-05", "2015-04-21",
                 "2015-05-01", "2015-06-04", "2015-09-07", "2015-10-12", "2015-11-02", "2015-11-15",
                 "2015-12-25"],
        "nome do feriado": ["Confraternização Universal", "Segunda-feira de Carnaval", "Carnaval",
                            "Sexta-feira Santa", "Páscoa", "Tiradentes", "Dia do Trabalho",
                            "Corpus Christi", "Independência do Brasil", "Nossa Senhora Aparecida",
                            "Finados", "Proclamação da República", "Natal"]
    }

    df_feriados = pd.DataFrame(feriados)
    df_feriados.to_csv('data/feriados-2015.csv', index=False)

    print("Arquivo feriados-2015.csv criado com sucesso!")

def clean_column_names(df):
    df.columns = (
        df.columns.str.strip()
        .str.lower()
        .str.replace(" ", "_")
        .str.replace("ã", "a")
        .str.replace("ç", "c")
        .str.replace("é", "e")
        .str.replace("á", "a")
        .str.replace("í", "i")
        .str.replace("ó", "o")
        .str.replace("ú", "u")
    )
    return df

def translate_column_names(df):
    translation_dict = {
        'data': 'date',
        'temperatura_media_(c)': 'avg_temperature_c',
        'temperatura_minima_(c)': 'min_temperature_c',
        'temperatura_maxima_(c)': 'max_temperature_c',
        'precipitacao_(mm)': 'precipitation_mm',
        'final_de_semana': 'weekend',
        'consumo_de_cerveja_(litros)': 'beer_consumption_liters',
        'nome_do_feriado': 'holiday_name'
    }
    df = df.rename(columns=translation_dict)
    return df

def merge():
    # Carregar os dados do arquivo Consumo_Cerveja.csv
    consumo_cerveja = pd.read_csv('data/Consumo_cerveja.csv', delimiter=',')
    consumo_cerveja = clean_column_names(consumo_cerveja)
    consumo_cerveja['data'] = pd.to_datetime(consumo_cerveja['data'], format='%Y-%m-%d')
    consumo_cerveja = consumo_cerveja[consumo_cerveja['data'].dt.year == 2015]

    # Carregar os dados do arquivo paulista-2015.csv
    paulista = pd.read_csv('data/paulista-2015.csv', delimiter=';')
    paulista = clean_column_names(paulista)
    paulista['dia'] = pd.to_datetime(paulista['dia'], format='%d.%m.%Y')
    paulista = paulista[paulista['dia'].dt.year == 2015]

    # Renomear a coluna 'dia' para 'data' para facilitar a junção
    paulista = paulista.rename(columns={'dia': 'data'})

    # Realizar a junção dos dois DataFrames com base na coluna 'data'
    merged_data = pd.merge(consumo_cerveja, paulista, on='data', how='outer')

    # Carregar os dados do arquivo brasileirao_serie_a.csv
    brasileirao = pd.read_csv('data/brasileirao_serie_a.csv', delimiter=',')
    brasileirao = clean_column_names(brasileirao)
    brasileirao['data'] = pd.to_datetime(brasileirao['data'], format='%Y-%m-%d')
    brasileirao = brasileirao[brasileirao['data'].dt.year == 2015]

    # Realizar a junção do DataFrame resultante com o brasileirao_serie_a.csv
    merged_data = pd.merge(merged_data, brasileirao, on='data', how='outer')

    # Carregar os dados do arquivo feriados-2015.csv
    feriados = pd.read_csv('data/feriados-2015.csv')
    feriados = clean_column_names(feriados)
    feriados['data'] = pd.to_datetime(feriados['data'], format='%Y-%m-%d')

    # Realizar a junção do DataFrame resultante com o feriados-2015.csv
    final_data = pd.merge(merged_data, feriados, on='data', how='outer')

    # Filtrar os dados para incluir apenas o ano de 2015
    final_data = final_data[final_data['data'].dt.year == 2015]

    # Adicionar a coluna is_holiday
    final_data['is_holiday'] = final_data['nome_do_feriado'].apply(lambda x: 1 if pd.notna(x) else 0)

    # Adicionar a coluna has_match
    final_data['has_match'] = final_data.apply(lambda row: 1 if pd.notna(row['home']) or pd.notna(row['time_mandante']) or pd.notna(row['away']) or pd.notna(row['time_visitante']) else 0, axis=1)

    # Adicionar a coluna match_type
    def match_type(row):
        if pd.notna(row['home']) and pd.isna(row['time_mandante']) and pd.isna(row['away']) and pd.isna(row['time_visitante']):
            return 1
        elif pd.isna(row['home']) and pd.notna(row['time_mandante']) and pd.isna(row['away']) and pd.isna(row['time_visitante']):
            return 2
        elif pd.notna(row['home']) and pd.notna(row['time_mandante']) and pd.notna(row['away']) and pd.notna(row['time_visitante']):
            return 3
        else:
            return 0

    final_data['match_type'] = final_data.apply(match_type, axis=1)

    # Lista dos 10 times mais populares
    top_teams = ["flamengo", "corinthians", "sao paulo", "palmeiras", "vasco",
                 "cruzeiro", "gremio", "atletico mineiro", "bahia", "internacional"]

    # Adicionar colunas is_<time>
    for team in top_teams:
        column_name = f'is_{team.replace(" ", "_")}'
        final_data[column_name] = final_data.apply(lambda row: 1 if (pd.notna(row['home']) and team in row['home'].lower()) or
                                                           (pd.notna(row['time_mandante']) and team in row['time_mandante'].lower()) or
                                                           (pd.notna(row['away']) and team in row['away'].lower()) or
                                                           (pd.notna(row['time_visitante']) and team in row['time_visitante'].lower()) else 0, axis=1)

    # Lista de times da cidade de São Paulo
    sao_paulo_teams = ["sao paulo", "corinthians", "palmeiras", "santos", "portuguesa"]

    # Adicionar coluna is_city_match
    final_data['is_city_match'] = final_data.apply(lambda row: 1 if (pd.notna(row['home']) and any(team in row['home'].lower() for team in sao_paulo_teams)) or
                                                            (pd.notna(row['time_mandante']) and any(team in row['time_mandante'].lower() for team in sao_paulo_teams)) or
                                                            (pd.notna(row['away']) and any(team in row['away'].lower() for team in sao_paulo_teams)) or
                                                            (pd.notna(row['time_visitante']) and any(team in row['time_visitante'].lower() for team in sao_paulo_teams)) else 0, axis=1)

    # Remover as colunas indesejadas
    columns_to_drop = ['nacao', 'campeonato', 'rodada_x', 'ano', 'home', 'away', 'hght', 'aght',
                       'hgft', 'agft', 'odd_home', 'odd_draw', 'odd_away', 'over25', 'endereco',
                       'ano_campeonato', 'rodada_y', 'estadio', 'arbitro', 'publico', 'publico_max',
                       'time_mandante', 'time_visitante', 'tecnico_mandante', 'tecnico_visitante',
                       'colocacao_mandante', 'colocacao_visitante', 'valor_equipe_titular_mandante',
                       'valor_equipe_titular_visitante', 'idade_media_titular_mandante',
                       'idade_media_titular_visitante', 'gols_mandante', 'gols_visitante',
                       'gols_1_tempo_mandante', 'gols_1_tempo_visitante', 'escanteios_mandante',
                       'escanteios_visitante', 'faltas_mandante', 'faltas_visitante',
                       'chutes_bola_parada_mandante', 'chutes_bola_parada_visitante',
                       'defesas_mandante', 'defesas_visitante', 'impedimentos_mandante',
                       'impedimentos_visitante', 'chutes_mandante', 'chutes_visitante',
                       'chutes_fora_mandante', 'chutes_fora_visitante']
    final_data.drop(columns=columns_to_drop, inplace=True)

    final_data = translate_column_names(final_data)

    # Garantir que as colunas estejam no formato string
    final_data['avg_temperature_c'] = final_data['avg_temperature_c'].astype(str)
    final_data['min_temperature_c'] = final_data['min_temperature_c'].astype(str)
    final_data['max_temperature_c'] = final_data['max_temperature_c'].astype(str)
    final_data['precipitation_mm'] = final_data['precipitation_mm'].astype(str)
    final_data['beer_consumption_liters'] = final_data['beer_consumption_liters'].astype(str)

    # Converter as colunas para o formato numérico americano
    final_data['avg_temperature_c'] = final_data['avg_temperature_c'].str.replace(',', '.').astype(float)
    final_data['min_temperature_c'] = final_data['min_temperature_c'].str.replace(',', '.').astype(float)
    final_data['max_temperature_c'] = final_data['max_temperature_c'].str.replace(',', '.').astype(float)
    final_data['precipitation_mm'] = final_data['precipitation_mm'].str.replace(',', '.').astype(float)
    final_data['beer_consumption_liters'] = final_data['beer_consumption_liters'].str.replace('.', '').str.replace(',',
                                                                                                                   '.').astype(
        float)

    final_data['month'] = final_data['date'].dt.month
    # Adicionar a coluna week_day extraindo o dia da semana da coluna date
    final_data['week_day'] = final_data['date'].dt.dayofweek

    # Adicionar a coluna is_rain com valor 1 se precipitation_mm > 0 e 0 caso contrário
    final_data['is_rain'] = final_data['precipitation_mm'].apply(lambda x: 1 if x > 0 else 0)

    # Adicionar a coluna consumption_categ com base nos valores de beer_consumption_liters
    bins = [0, 5000, 10000, 15000, 20000, 25000, 30000, float('inf')]
    labels = ["0-5000", "5001-10000", "10001-15000", "15001-20000", "20001-25000", "25001-30000", ">30000"]
    final_data['consumption_categ'] = pd.cut(final_data['beer_consumption_liters'], bins=bins, labels=labels,
                                             right=False)
    # Adicionar a coluna max_temp_categ com base nos valores de max_temperature_c
    bins_temp = list(range(0, 45, 5)) + [float('inf')]
    labels_temp = ["0-5", "5-10", "10-15", "15-20", "20-25", "25-30", "30-35", "35-40", ">40"]
    final_data['max_temp_categ'] = pd.cut(final_data['max_temperature_c'], bins=bins_temp, labels=labels_temp,
                                          right=False)

    # Exportar o resultado em um novo arquivo CSV com separador ;
    final_data.to_csv('data/data.csv', sep=';', index=False)



    print("Arquivo data.csv criado com sucesso!")


# gen_holidays()
merge()