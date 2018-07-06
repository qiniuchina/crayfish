#!/usr/bin/env python
# coding=utf-8

from sqlalchemy import create_engine
import matplotlib.pyplot as plt
from matplotlib import colors
import pandas as pd
from matplotlib.font_manager import FontProperties
if __name__ == '__main__':
    zhfont=FontProperties(fname='/usr/share/fonts/adobe-source-han-serif/SourceHanSerifCN-Regular.otf')
    DAYS = 8 #取最近的天数来显示
    engine = create_engine("mysql+pymysql://happy:qiniuno.1@115.28.165.184:3306/darklight?charset=utf8", max_overflow=5)
    sql = "select real_date_str,pred_result,real_result from stock_index_pred where pred_result!=-2 order by real_date_str DESC limit "+  str(DAYS)
    cur = engine.execute(sql)
    data = cur.fetchall()
    if(len(data) > 0):
        data.reverse()
        df = pd.DataFrame(data)
        pdata = df[[1,2]].values
        df = df.replace(1,'涨').replace(-1,'跌').replace(0,'平').replace(-2,'--')
        ndata = df[[1,2]].values
        fig = plt.figure(figsize=(12,4))
        ax = fig.add_subplot(111, frameon=True, xticks=[], yticks=[])
        cmap = colors.ListedColormap(['#808080', '#008000', '#F5FFFA', '#FF0000'])
        bounds=[-2.1,-1.1,-0.9,0.9,1.1]
        norm = colors.BoundaryNorm(bounds, cmap.N)
        the_table=plt.table(cellText=ndata.T, rowLabels=['预测结果','实际结果'],colLabels=df[[0]].values.reshape(-1), loc='center',cellLoc='center',cellColours= cmap(norm(pdata.T)))
        the_table.set_fontsize(20)
        the_table.scale(1,6.2)
        table_props = the_table.properties()
        table_cells = table_props['child_artists']
        for cell in table_cells: 
            cell.set_text_props(fontproperties=zhfont)
        #plt.show()
        plt.savefig("linear.png")
