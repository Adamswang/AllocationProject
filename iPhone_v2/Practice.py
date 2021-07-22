import pandas as pd
import numpy as np


def dtprocess(xlsx_d, xlsx_s, xlsx_o, ratio_ini):

    df_d = pd.read_excel(xlsx_d, index_col=0)
    df_s = pd.read_excel(xlsx_s, index_col=0)

    df_p = pd.pivot_table(df_d, values='Demand', index=['Sold to Name', 'Model'], aggfunc=np.sum)
    for i in range(0, len(df_p)):
        print(str(df_p.to_records()[i]).replace(',', ' '))

    df_consol = pd.merge(df_d, df_s, on='MPN')
    df_consol = df_consol.fillna(0)
    df_consol2 = df_consol.groupby(['Model'], as_index=False)
    #df_consol2.groups.keys()
    for df_consol2_split in df_consol2:

        df_consol_split_main = pd.DataFrame(df_consol2_split[1]).reset_index(drop=True)
        df_consol_split_main = df_consol_split_main.groupby(['MPN', 'Supply CW+1', 'ODQ'], as_index=False)
        # print(list(df_consol_split_main))
        d_output = pd.DataFrame()
        m = df_consol2_split[0]
        print(m)
        for d_c_main_split in df_consol_split_main:
            od = d_c_main_split[0][2]
            s = d_c_main_split[0][1]
            d = d_c_main_split[1]['Demand'].values.tolist()
            d_c_split_main = pd.DataFrame(d_c_main_split[1]).reset_index(drop=True)

            if s > sum(d):
                F_allo = suffisupply(s, d, ratio_ini, od)

            elif s == 0:
                F_allo = [0 for i in range(len(ratio_ini))]
            else:
                F_allo = tightsupply(s, d, ratio_ini, od)

            F_allo = pd.DataFrame(F_allo, columns={'allo'})
            d_combine = pd.concat([d_c_split_main, F_allo], axis=1)
            d_combine = pd.DataFrame(d_combine)
            d_output = d_output.append(d_combine, ignore_index=True)



        print(d_output)


def tightsupply(supply, demand, ratio_ini, ODQ):
    supply_ini = supply
    ratio = ratio_ini[:]
    ind = [0 for i in range(len(ratio))]
    allo = [0 for i in range(len(ratio))]
    F_allo = [0 for i in range(len(ratio))]
    adj_s = [0 for i in range(len(ratio))]

    j = 0
    while sum(F_allo) < supply_ini:
        supply = supply - sum(allo)
        demand = list(map(lambda x, y: x-y, demand, allo))
        for l in range(len(ratio_ini)):
            if demand[l] == 0:
                ratio[l] = 0
        for i in range(len(ratio)):
            ind[i] = ratio[i]/sum(ratio)

        ind_position = [i for i, e in enumerate(ind) if e > 0]
        ind_count = sum(list(map(lambda x: x > 0, ind)))

        for i in range(len(ratio)):
            adj_s[i] = int((supply * ind[i])/ODQ)*ODQ
        if supply > ind_count * ODQ:
            for i in range(len(ratio)):
                allo[i] = min(adj_s[i], demand[i])
        else:
            allo = (np.random.randint(0, 1, len(ratio))).tolist()
            for k in ind_position:
                allo[k] = ODQ
                if sum(allo) == supply:
                    break
        for i in range(len(ratio)):
            F_allo[i] = F_allo[i] + allo[i]
    return F_allo


def suffisupply(supply, demand, ratio, ODQ):
    # define list
    ind = []
    for i in range(len(ratio)):
        ind.append(0)

    allo = []
    for i in range(len(ratio)):
        allo.append(0)

    F_allo = []
    for i in range(len(ratio)):
        F_allo.append(0)

    adj_s = []
    for i in range(len(ratio)):
        adj_s.append(0)

    allo = demand
    F_allo = allo

    return F_allo


xlsx_demand = '/Users/wangheng1223/Desktop/Weekly Reports/Allocation automation/demand_test.xlsx'
xlsx_supply = '/Users/wangheng1223/Desktop/Weekly Reports/Allocation automation/Supply Test.xlsx'
xlsx_out = '/Users/wangheng1223/Desktop/Weekly Reports/Allocation automation/Output_text.xlsx'
ratio_r = [0.18, 0.41, 0.41]
dtprocess(xlsx_demand, xlsx_supply, xlsx_out, ratio_r)


testlist = [0 for i in range(len(ratio_r))]
print(testlist)




