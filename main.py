"""
from turtle import filling
import surf
import numpy as np
import pandas as pd
import datetime
import plotly.graph_objects as go

from plotly.subplots import make_subplots

import surf.wind_calcs as wc

from surf.dir_to_arrow import dir_to_arrow
from surf.dir_to_text import dir_to_text

download=0
if download == 1:
  # fetch gfswave data
  #-------------------
  p_noaa = "https://polar.ncep.noaa.gov/waves/WEB/gfswave.latest_run/plots/gfswave.62001.bull"
  df_gfswave = surf.noaa.gfswave(p_noaa)

  # fetch gfswind data
  #-------------------
  p_windguru = r"https://old.windguru.cz/fr/index.php?sc=48572"
  df_gfswind = surf.windguru.gfswind(p_windguru)
  df_aromewind = surf.windguru.aromewind(p_windguru)

  # create df_start_end
  #--------------------
  t_start = datetime.date.today()
  t_end = t_start + datetime.timedelta(days=17)
  dictt = {"time": [t_start, t_end],
          "value": [np.nan, np.nan]}
  df_start_end = pd.DataFrame(dictt)
  df_start_end.time = pd.to_datetime(df_start_end.time)
  df_start_end = df_start_end.set_index(["time"])

  # treat wave
  #-----------
  # concat with df_start_end
  df_wave = pd.concat([df_gfswave, df_start_end])
  # sort index
  df_wave = df_wave.sort_index()
  # elimnate date before tstart and after tend
  df_wave = df_wave[~(df_wave.index < df_start_end.index[0])]
  df_wave = df_wave[~(df_wave.index > df_start_end.index[1])]
  # resample hourly with mean value
  df_wave = df_wave.resample('H').mean()

  # treat wind1
  #------------
  df_aromewind = df_aromewind[["WINDSPD", "GUST", "WINDDIR"]]
  # concat with df_start_end
  df_wind1 = pd.concat([df_aromewind, df_start_end])
  # sort index
  df_wind1 = df_wind1.sort_index()
  # elimnate date before tstart and after tend
  df_wind1 = df_wind1[~(df_wind1.index < df_start_end.index[0])]
  df_wind1 = df_wind1[~(df_wind1.index > df_start_end.index[1])]
  # resample hourly with mean value
  df_wind1 = df_wind1.resample('H').mean()

  # treat wind2
  #------------
  df_gfswind = df_gfswind[["WINDSPD", "GUST", "WINDDIR"]]
  # concat with df_start_end
  df_wind2 = pd.concat([df_gfswind, df_start_end])
  # sort index
  df_wind2 = df_wind2.sort_index()
  # elimnate date before tstart and after tend
  df_wind2 = df_wind2[~(df_wind2.index < df_start_end.index[0])]
  df_wind2 = df_wind2[~(df_wind2.index > df_start_end.index[1])]
  # resample hourly with mean value
  df_wind2 = df_wind2.resample('H').mean()

  # treat df_wind
  #--------------
  # combine
  df_wind = df_wind1.copy()
  df_wind = df_wind.combine_first(df_wind2)
  # knots to m/s
  df_wind["WINDSPD"] = df_wind["WINDSPD"]*0.514444
  df_wind["GUST"] = df_wind["GUST"]*0.514444
  # create u, v
  df_wind["U"], df_wind["V"] = wc.wind_spddir_to_uv(df_wind["WINDSPD"], df_wind["WINDDIR"])
  df_wind["Ug"], df_wind["Vg"] = wc.wind_spddir_to_uv(df_wind["GUST"], df_wind["WINDDIR"])

  # treat df_surf
  #---------------
  # concat df_wave and df_wind
  #frames = [df_wave[["hst", "tp1", "dir1"]], df_wind[["U", "V", "Ug", "Vg"]], ]
  frames = [df_wave[["hst", "tp1", "dir1"]], df_wind[["WINDSPD", "GUST", "WINDDIR"]], ]
  df_surf = pd.concat(frames, axis=1)
  # rename columns
  df_surf.rename(columns = {'hst':'wave_hs',
                          'tp1': "wave_tp",
                          "dir1": "wave_dir",
                          'WINDSPD':'wind_spd',
                          'GUST': "wind_max",
                          "WINDDIR": "wind_dir",},
                          inplace = True)

  # treat day
  #----------
  df_surf["day"] = df_surf.index.values
  df_surf["day_text"] = df_surf["day"].dt.strftime("%A %d")

  # treat wave
  #-----------
  df_surf["wave_dir_ar"] = df_surf["wave_dir"]
  df_surf["wave_dir_txt"] = df_surf["wave_dir"]
  mask = ~np.isnan(df_surf["wave_dir_ar"])
  df_surf["wave_dir_ar"].iloc[mask] = dir_to_arrow(df_surf["wave_dir_ar"][mask])
  df_surf["wave_dir_txt"].iloc[mask] = dir_to_text(df_surf["wave_dir_txt"][mask])
  df_surf["wave_tp_text"] = df_surf["wave_tp"].round(0)
  df_surf["wave_tp_text"] = df_surf["wave_tp_text"].apply(lambda x: "%0.0f" % x)
  #df_surf["wave_text"] = df_surf["wave_dir_txt"] + "<br>" +\
  #  df_surf["wave_tp_text"] + "<br>" +\
  #  "<b>" +  df_surf["wave_hs"].round(1).astype(str) + "</b>"

  # treat wind
  #-----------
  df_surf["wind_dir_ar"] = df_surf["wind_dir"]
  df_surf["wind_dir_txt"] = df_surf["wind_dir"]
  mask = ~np.isnan(df_surf["wind_dir_ar"])
  df_surf["wind_dir_ar"].iloc[mask] = dir_to_arrow(df_surf["wind_dir_ar"][mask])
  df_surf["wind_dir_txt"][mask] = dir_to_text(df_surf["wind_dir_txt"][mask])
  df_surf["wind_spd_bft"] = df_surf["wind_spd"].apply(lambda x: np.ceil(np.cbrt(np.power(x/0.836, 2))))
  df_surf["wind_spd_bft_txt"] = df_surf["wind_spd_bft"].apply(lambda x: "%0.0f" % x)
  df_surf["wind_text"] = df_surf["wind_spd_bft_txt"] + " " + df_surf["wind_dir_txt"]

  # treat grade
  #------------
  df_surf["grade"] = df_surf["wind_spd"]
  df_surf["grade_marker_color"] = df_surf["wind_dir_txt"]
  # colors
  c_red="#fb4b45"
  c_yellow="#e3ee52"
  c_green="#c1ea56"
  # based on directions
  df_surf["grade_marker_color"].replace("N", c_red, inplace=True)
  df_surf["grade_marker_color"].replace("NE", c_green, inplace=True) 
  df_surf["grade_marker_color"].replace("E", c_green, inplace=True) 
  df_surf["grade_marker_color"].replace("SE", c_green, inplace=True)
  df_surf["grade_marker_color"].replace("S", c_yellow, inplace=True) 
  df_surf["grade_marker_color"].replace("SW", c_red, inplace=True) 
  df_surf["grade_marker_color"].replace("W", c_red, inplace=True) 
  df_surf["grade_marker_color"].replace("NW", c_red, inplace=True)
  # based on wind speed <= 1Bft
  mask = df_surf["wind_spd_bft"]<=1
  df_surf["grade_marker_color"][mask] = c_green
  # based on wind speed = 2Bft
  mask = df_surf["wind_spd_bft"]==2
  maskk = df_surf["grade_marker_color"]!=c_green
  df_surf["grade_marker_color"][mask*maskk] = c_yellow
  
  df_surf.to_pickle("df_surf.pkl")

else:
  df_surf = pd.read_pickle("df_surf.pkl")
"""
# Flask
#------
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from flask import Flask, render_template
import pandas as pd
import json
import plotly

df_surf = pd.read_pickle("df_surf.pkl")

def create_fig(df_surf, ind1, ind2, all=0):

  # create figure
  fig = make_subplots(
    rows=3,
    cols=1,
    vertical_spacing=0.1,
    shared_xaxes=True,
    #row_heights=[0.4, 0.4, 0.2],
    specs=[[{"secondary_y": True}],
      [{"secondary_y": False}],
      [{"secondary_y": False}]] ,
  )

  # hs trace
  if all==0:
    fig.add_trace(
      go.Bar(
          name="Hs",
          x=df_surf.index[ind1:ind2],
          y=df_surf["wave_hs"][ind1:ind2],
          text=df_surf["wave_hs"][ind1:ind2].round(1),
          textposition='auto',
          marker_color="#1D8DEE",
          hovertemplate ='%{y:.1f}m' + ', (Dir:%{customdata:.0f}&#176;)',
          customdata = df_surf["wave_dir"][ind1:ind2].round(0),
          ),
      secondary_y=False,
      row=1,
      col=1
      )
  else:
    fig.add_trace(
      go.Scatter(
          name="Hs",
          x=df_surf.index[ind1:ind2],
          y=df_surf["wave_hs"][ind1:ind2],
          mode="lines",
          line=dict(width=2, color='#1D8DEE'),
          fill="tozeroy",
          hovertemplate ='%{y:.1f}m' + ', (Dir:%{customdata:.0f}&#176;)',
          customdata = df_surf["wave_dir"][ind1:ind2].round(0),
          ),
      secondary_y=False,
      row=1,
      col=1
      )

  # tp trace
  fig.add_trace(
    go.Scatter(
        name="Tp",
        x=df_surf.index[ind1:ind2],
        y=df_surf["wave_tp"][ind1:ind2],
        mode="lines",
        line=dict(width=1, color='red'),
        hovertemplate ='%{text:.0f}s',
        text = df_surf["wave_tp"][ind1:ind2].round(0),
        ),
    secondary_y=True,
    row=1,
    col=1
    )

  # wind trace
  wind_mask = ~np.isnan(df_surf["wind_spd_bft"][ind1:ind2])
  fig.add_trace(
    go.Bar(
        name="",
        x=df_surf.index[ind1:ind2][wind_mask],
        y=df_surf["wind_spd"][ind1:ind2][wind_mask],
        marker_color=df_surf["grade_marker_color"][ind1:ind2][wind_mask],
        #line=dict(width=2, color='#657786'),
        text=df_surf["wind_dir_ar"][ind1:ind2][wind_mask],
        textposition='auto',
        hovertemplate ='Dir: %{text}, Mean: %{y:.1f}m/s,' + \
          ' Max: %{customdata:.1f}m/s',
        customdata = df_surf["wind_max"][ind1:ind2].round(1),
        ),
    row=2,
    col=1
    )
  
  # tide trace
  fig.add_trace(
    go.Scatter(
        name="Niveau",
        x=df_surf.index[ind1:ind2][wind_mask],
        y=df_surf["wind_spd"][ind1:ind2][wind_mask]*0,
        #line=dict(width=2, color='#657786'),
        #hovertext=df_surf["wind_text"][ind1:ind2],
        ),
    row=3,
    col=1
    )
    
  # set general layout parameters
  fig.update_layout(
    paper_bgcolor="#151E29",
    plot_bgcolor="#151E29",
        font=dict(
        family="Verdana",
        size=15,
        color="white",
        ),
    hovermode='x unified',
    hoverlabel=dict(
      bgcolor="#1B2737",
      font_size=15,
      font_family="Verdana"
    ),
    legend=dict(
      orientation="h",
      yanchor="bottom",
      y=1.02,
      xanchor="right",
      x=1
      ),
    showlegend=False,
    margin=go.layout.Margin(
        l=0, #left margin
        r=0, #right margin
        b=0.05, #bottom margin
        t=0.05, #top margin
    )
  )

  # set date tick format
  if all==0:
    fig.update_layout(
      xaxis_tickformat = '%a %d'
    )
  else:
    fig.update_layout(
      xaxis_tickformat = '%H'
    )


  # set grid parameters
  fig.update_xaxes(showgrid=True, gridwidth=1, gridcolor='#1B2737')
  fig.update_yaxes(showgrid=True, gridwidth=1, gridcolor='#1B2737')

  # set y-axes titles
  fig.update_yaxes(title_text="Vagues", secondary_y=False, row=1, col=1)
  fig['layout']['yaxis2']['showgrid'] = False
  fig.update_yaxes(title_text="Vents", row=2, col=1)
  fig.update_yaxes(title_text="Marée", row=3, col=1)

  # remove plotly modebar
  #fig["config"]["displayModeBar"]=False

  return fig


app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/all')
def all():
  
  # load data
  df_surf = pd.read_pickle("df_surf.pkl")

  # plot data
  fig = create_fig(df_surf, 0, 24*16, all=1)
 
  # create json
  graphJSON = json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)

  # template
  header="16 jours"
  next="day1_am"
  back="day1_pm"  
  temp = render_template('day.html', graphJSON=graphJSON, header=header,
   next=next, back=back)
  
  return temp

@app.route('/day1_am')
def day1_am():
  
  # load data
  df_surf = pd.read_pickle("df_surf.pkl")

  # plot data
  fig = create_fig(df_surf, 0, 12)
 
  # create json
  graphJSON = json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)

  # template
  header="Aujourd'hui" + ", matin"
  next="day1_pm"
  back="all"  
  temp = render_template('day.html', graphJSON=graphJSON, header=header,
   next=next, back=back)
  
  return temp

@app.route('/day1_pm')
def day1_pm():
  
  # load data
  df_surf = pd.read_pickle("df_surf.pkl")

  # plot data
  fig = create_fig(df_surf, 12, 24)
 
  # create json
  graphJSON = json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)

  # template
  header="Aujourd'hui" + ", aprem"
  next="day2_am"
  back="day1_am"  
  temp = render_template('day.html', graphJSON=graphJSON, header=header,
   next=next, back=back)
  
  return temp

@app.route('/day2_am')
def day2_am():
  
  # load data
  df_surf = pd.read_pickle("df_surf.pkl")

  # plot data
  fig = create_fig(df_surf, 24, 36)
 
  # create json
  graphJSON = json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)

  # template
  header="Demain" + ", matin"
  next="day2_pm"
  back="day1_pm"  
  temp = render_template('day.html', graphJSON=graphJSON, header=header,
   next=next, back=back)
  
  return temp

@app.route('/day2_pm')
def day2_pm():
  
  # load data
  df_surf = pd.read_pickle("df_surf.pkl")

  # plot data
  fig = create_fig(df_surf, 36, 48)
 
  # create json
  graphJSON = json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)

  # template
  header="Demain" + ", aprem"
  next="all"
  back="day2_am"  
  temp = render_template('day.html', graphJSON=graphJSON, header=header,
   next=next, back=back)
  
  return temp

@app.route('/style.css')
def compressed_css():
    return '/* ... */', 200, {'Content-Type': 'text/css; charset=utf-8'}

if __name__ == "__main__":
    app.run()
