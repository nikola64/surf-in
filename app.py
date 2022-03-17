import plotly.graph_objects as go
from plotly.subplots import make_subplots
from flask import Flask, render_template
import pandas as pd
import numpy as np
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
        text=df_surf["wind_dir_txt"][ind1:ind2][wind_mask],
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
        l=0.05, #left margin
        r=0.05, #right margin
        b=0.05, #bottom margin
        t=0.15, #top margin
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
