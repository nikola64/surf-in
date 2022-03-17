import numpy as np
import plotly.graph_objects as go
import datetime
from plotly.subplots import make_subplots
import locale

from .dir_to_arrow import dir_to_arrow
from .dir_to_text import dir_to_text

'''
def plot_html(wa_t, wa_hst, wa_tp1, wa_dir1,
         wi_t, wi_speed, wi_gust, wi_dir,
         df_gfswave, df_gfswind):

    
    # Create figure
    #--------------
    fig = make_subplots(
        rows=5,
        cols=1,
        vertical_spacing=0.07,
        specs=[
            [{"type": "xy", "secondary_y": True}],
            [{"type": "xy", "secondary_y": True}],
            [{"type": "xy", "secondary_y": False}],
            [{"type": "xy", "secondary_y": False}],
            [{"type": "xy", "secondary_y": False}],
        ],
        subplot_titles=("<b>SURF</b>",
                        "<b>VENTS</b>",
                        "<b>MAREE</b>",
                        "<b>SWELL</b>",
                        "<b>METEO</b>"
                        ))
    
    # Create traces
    # --------------
    # subplot 1
    fig.add_trace(go.Scatter(x=wa_t,
                             y=wa_hst,
                             line=dict(color='dodgerblue',
                                       width=2),
                             fill='tozeroy',
                             name="Hs",
                             hovertemplate='%{y:.1f}m',
                             ),
                  secondary_y=False,
                  row=1,
                  col=1)
    
    fig.add_trace(go.Scatter(x=wa_t,
                             y=np.round(wa_tp1),
                             line=dict(color='navy',
                                       width=1),
                             name="Tp",
                             text=np.round(wa_tp1),
                             hovertemplate='%{text}s',
                             ),
                  secondary_y=True,
                  row=1,
                  col=1)
    
    fig.add_trace(go.Scatter(x=wa_t,
                             y=wa_dir1,
                             line=dict(color='white',
                                       width=0),
                             name="Dir",
                            text= 
                            [dir_to_arrow(wdir) + " " + \
                             dir_to_text(wdir) + " " + \
                                 str(int(wdir)) + "&#176;" for wdir in wa_dir1],
                            #wa_dir1 + "&#176;",
                             hovertemplate='%{text}',
                             ),
                  secondary_y=True,
                  row=1,
                  col=1)
    
    # subplot 2
    fig.add_trace(go.Scatter(x=wi_t,
                             y=(wi_speed + 5)/5,
                             line=dict(color='blueviolet',
                                       width=2),
                             fill='tozeroy',
                             name="Vitesse",
                             hovertemplate='%{y:.1f}Bft',
                             ),
                  secondary_y=False,
                  row=2,
                  col=1)
    
    fig.add_trace(go.Scatter(x=wi_t,
                             y=(wi_gust + 5)/5,
                             line=dict(color='white',
                                       width=0),
                             name="Raffales",
                             hovertemplate='%{y:.1f}Bft',
                             ),
                  secondary_y=True,
                  row=2,
                  col=1)
    
    fig.add_trace(go.Scatter(x=wi_t,
                             y=wi_dir,
                             line=dict(color='navy',
                                       width=1),
                             name="Dir",
                             text= 
                             [dir_to_arrow(wdir) + " " + \
                              dir_to_text(wdir) + " " + \
                                  str(int(wdir)) + "&#176;" for wdir in wi_dir],
                             hovertemplate='%{text}',
                             ),
                  secondary_y=True,
                  row=2,
                  col=1)
    
    # subplot 3
    fig.add_trace(go.Scatter(x=df_gfswave.time,
                             y=df_gfswave.hst,
                             line=dict(color='navy',
                                       width=1),
                             name="Niv",
                             hovertemplate='%{y:.1f}m XXCoef',
                             ),
                  secondary_y=False,
                  row=3,
                  col=1)
    
    
    # subplot 4
    fig.add_trace(go.Scatter(x=df_gfswave.time,
                             y=df_gfswave.hs1,
                             text=
                             df_gfswave.hs1.astype(str) + "m, " +
                             df_gfswave.tp1.astype(str) + "s, " +
                             df_gfswave.dir1.astype(int).astype(str) + "&#176;",
                             line=dict(color='dodgerblue',
                                       width=1),
                             name="Swell1",
                             hovertemplate='%{text}',
                             ),
                  row=4,
                  col=1)
    
    fig.add_trace(go.Scatter(x=df_gfswave.time,
                             y=df_gfswave.hs2,
                             text=
                             df_gfswave.hs2.astype(str) + "m, " +
                             df_gfswave.tp2.astype(str) + "s, " +
                             df_gfswave.dir2.astype(int).astype(str) + "&#176;",
                             line=dict(color='dodgerblue',
                                       width=1),
                             name="Swell2",
                             hovertemplate='%{text}',
                             ),
                  row=4,
                  col=1)
    
    fig.add_trace(go.Scatter(x=df_gfswave.time,
                             y=df_gfswave.hs3,
                             text=
                             df_gfswave.hs3.astype(str) + "m, " +
                             df_gfswave.tp3.astype(str) + "s, " +
                             df_gfswave.dir3.astype(int).astype(str) + "&#176;",
                             line=dict(color='dodgerblue',
                                       width=1),
                             name="Swell3",
                             hovertemplate='%{text}',
                             ),
                  row=4,
                  col=1)
    
    fig.add_trace(go.Scatter(x=df_gfswave.time,
                             y=df_gfswave.hs4,
                             text=
                             df_gfswave.hs4.astype(str) + "m, " +
                             df_gfswave.tp4.astype(str) + "s, " +
                             df_gfswave.dir4.astype(int).astype(str) + "&#176;",
                             line=dict(color='dodgerblue',
                                       width=1),
                             name="Swell4",
                             hovertemplate='%{text}',
                             ),
                  row=4,
                  col=1)
    
    fig.add_trace(go.Scatter(x=df_gfswave.time,
                             y=df_gfswave.hs5,
                             text=
                             df_gfswave.hs5.astype(str) + "m, " +
                             df_gfswave.tp5.astype(str) + "s, " +
                             df_gfswave.dir5.astype(int).astype(str) + "&#176;",
                             line=dict(color='dodgerblue',
                                       width=1),
                             name="Swell5",
                             hovertemplate='%{text}',
                             ),
                  row=4,
                  col=1)
    
    fig.add_trace(go.Scatter(x=df_gfswave.time,
                             y=df_gfswave.hs6,
                             text=
                             df_gfswave.hs6.astype(str) + "m, " +
                             df_gfswave.tp6.astype(str) + "s, " +
                             df_gfswave.dir6.astype(int).astype(str) + "&#176;",
                             line=dict(color='dodgerblue',
                                       width=1),
                             name="Swell6",
                             hovertemplate='%{text}',
                             ),
                  row=4,
                  col=1)
    
    # Create axis labels
    # -------------------
    # subplot 1
    fig.update_xaxes(matches='x2', row=1, col=1)
    fig.update_yaxes(title_text="Hs (m)",
                     range=[0, 7],
                     dtick=7 / 7,
                     secondary_y=False,
                     row=1,
                     col=1)
    fig.update_yaxes(title_text="Tp (s)",
                     range=[0, 21],
                     dtick=21 / 7,
                     secondary_y=True,
                     row=1,
                     col=1)
    
    # subplot 2
    fig.update_xaxes(matches='x1', row=3, col=1)
    fig.update_yaxes(title_text="Vitesse (Bft)",
                     range=[0, 5],
                     dtick=5 / 5,
                     secondary_y=False,
                     row=2,
                     col=1)
    fig.update_yaxes(title_text="Direction (&#176;)",
                     range=[0, 360],
                     dtick=360 / 5,
                     secondary_y=True,
                     row=2,
                     col=1)
    
    # subplot 3
    fig.update_xaxes(matches='x1', row=3, col=1)
    fig.update_yaxes(title_text="Niveau (m)",
                     range=[0, 5],
                     dtick=5 / 5,
                     row=3,
                     col=1)
    
    # subplot 4
    fig.update_xaxes(matches='x1', row=2, col=1)
    fig.update_yaxes(title_text="Hs (m)",
                     row=4,
                     col=1)
    
    # Create layout
    # -------------
    fig.update_layout(hovermode='x unified',
                      showlegend=False,
                      height=2000,
                      # template='plotly_dark',
                      )
    
    # Create buttons and range slider
    #--------------------------------
    
    fig.update_xaxes(fixedrange=True)
    fig.update_yaxes(fixedrange=True)
    fig.update_layout(font=dict(
        family="Verdana",
        size=18,
        color="Black"))

    #fig.update_xaxes(rangeslider_thickness = 0.01)
    # Add dropdown
    button1 = dict(method = "relayout",
               args = [{'xaxis.range': [wa_t[1], wa_t[10]]}],
               label = '1d')
    button2 = dict(method = "relayout",
               args = [{'xaxis.range': [wa_t[10], wa_t[20]]}],
               label = '2d')
    
    fig.update_layout(#width=800,
                      height=2000,
                     updatemenus=[dict(active=0,
                                       x= -0.25, y=1, 
                                       xanchor='left', 
                                       yanchor='top',
                                       buttons=[button1,
                                                button2])
                                  ])     

    # Save
    # -----
    fig.write_html("test.html")
    '''
    
def plot_html(wa_t, wa_hst, wa_tp1, wa_dir1,
         wi_t, wi_speed, wi_gust, wi_dir,
         df_gfswave, df_gfswind):
    
        locale.setlocale(locale.LC_TIME, 'fr_FR')

        # Create datelist
        #----------------
        base = datetime.date.today()
        numdays=17
        date_list = [base + datetime.timedelta(days=x) for x in range(numdays)]

        # Create text subplots
        #---------------------
        text_s2 = [str(np.around(hs, 1)) + "<br>" + \
              str(int(tp1)) for hs, tp1 in zip(wa_hst, wa_tp1)]       
        text_s3 = ['<b>' + dir_to_arrow(dir) + '</b>'  for dir in wi_dir]
            
        # Create figure
        #--------------
        fig = make_subplots(
            rows=3,
            cols=1,
            vertical_spacing=0.1,
            specs=[
                [{"type": "xy"}],
                [{"type": "xy"}],
                [{"type": "xy"}]
                ],
            subplot_titles=("16-jours",
                            "Surf",
                            "Vents",
                            ),
            )
    
        # Create traces
        # --------------
        # subplot 1
        fig.add_trace(go.Scatter(x=wa_t,
                                 y=wa_hst,
                                 line=dict(color='dodgerblue',
                                           width=2),
                                 fill='tozeroy',
                                 name="Hs",
                                 hovertemplate='%{y:.1f}m',
                                 ),
                      row=1,
                      col=1)
        
        fig.update_xaxes(
            dtick="D1",
            tickformat="%d/%m",
            range=[date_list[0], date_list[-1]],
            showgrid=False,
            fixedrange=True,
            row=1, col=1)
        
        fig.update_yaxes(showgrid=False,
                         fixedrange=True,
                         row=1, col=1)
        
        # subplot 2
        fig.add_trace(go.Scatter(x=wa_t,
                                 y=wa_hst,
                                 line=dict(color='dodgerblue',
                                           width=2),
                                 fill='tozeroy',
                                 name="Hs",
                                 hovertemplate='%{y:.1f}m',
                                 mode="lines+markers+text",
                                 text=text_s2,
                                 textposition="top center",                           
                                 ),
                      row=2,
                      col=1)
        
        fig.update_xaxes(
            dtick=3600000,
            tickformat="%H",
            range=[date_list[0], date_list[1]],
            showgrid=False,
            fixedrange=True,
            row=2, col=1)

        fig.update_yaxes(showgrid=False,
                         fixedrange=True,
                         row=2, col=1)

        # subplot 3
        fig.add_trace(go.Scatter(x=wi_t,
                                 y=(wi_speed+5)/5,
                                 line=dict(color='darkorange',
                                           width=2),
                                 fill='tozeroy',
                                 name="Vitesse",
                                 hovertemplate='%{y:.1f}Bft',
                                 mode="lines+markers+text",
                                 text=text_s3,
                                 textposition="top center",                           
                                 ),
                      row=3,
                      col=1)
        
        fig.update_xaxes(
            dtick=3600000,
            tickformat="%H",
            range=[date_list[0], date_list[1]],
            showgrid=False,
            fixedrange=True,
            row=3, col=1)

        fig.update_yaxes(showgrid=False,
                         fixedrange=True,
                         row=3, col=1)

        # Create shapes
        fig.add_vrect(x0=date_list[0],
                      x1=date_list[1],
                      fillcolor="LightSalmon",
                      opacity=0.5,
                      layer="below",
                      line_width=0,
                      row=1,
                      col=1
            )
            
        fig.update_layout(showlegend=False,
                          annotations={'xanchor': 'left'},
                          )
        
        # create frames
        #--------------
        nt = len(date_list)-1
        frames = [
            dict(
                name=k,
                data=[go.Scatter(x=wa_t,
                                y=wa_hst,
                                line=dict(color='dodgerblue',
                                          width=2),
                                fill='tozeroy',
                                name="Hs",
                                hovertemplate='%{y:.1f}m',
                                         ),
                      ],
                layout=dict(
                    #title={'text': r"<b>" + date_list[k].strftime("%A %d/%m") + "</b>", },
                    shapes=[go.layout.Shape(type="rect",
                                  x0=date_list[k],
                                  x1=date_list[k+1],
                                  fillcolor="LightSalmon",
                                  opacity=0.5,
                                  layer="below",
                                  line_width=0,),
                          ],
                    xaxis2={'range': [date_list[k], date_list[k+1]],
                            'dtick': 3600000,
                            'tickformat': "%H",
                            },
                    xaxis3={'range': [date_list[k], date_list[k+1]],
                            'dtick': 3600000,
                            'tickformat': "%H",
                            }
                ),
                traces=[1],
            ) for k in range(nt)]

        # create buttons
        #---------------
        '''
        updatemenus = [dict(type='buttons',
                            buttons=[
                                dict(label='&#9658;',
                                     method='animate',
                                     args=[[f'{k}' for k in range(nt)],
                                           dict(mode='relayout',
                                                frame=dict(duration=0,
                                                           redraw=False),
                                                transition=dict(duration=100)
                                                )]
                                     ),
                                dict(label='&#9209;',
                                     method='animate',
                                     args=[[None], dict(mode='relayout',
                                                        frame=dict(
                                                            duration=0,
                                                            redraw=False),
                                                        transition=dict(
                                                            duration=100)
                                                        )],
                                     ),
                                dict(label='&#9198;',
                                     method='animate',
                                     args=[[0], dict(mode='relayout',
                                                     frame=dict(
                                                         duration=0,
                                                         redraw=False),
                                                     transition=dict(
                                                         duration=100)
                                                     )],
                                     ),
                            ],
                            showactive=False,
                            ),
                       ]
        '''
        
        # create sliders
        #---------------
        sliders = [
            {'currentvalue': {'prefix': '<b>',
                              'visible': True,
                              'xanchor': 'left',
                              'offset': 30,
                              'font': {'size': 25}},
             'borderwidth': 30,
             'pad': {'t': 50},
             'bordercolor': "white",
             'steps': [
                 {'args': [[k],
                           dict(mode='relayout',
                                frame=dict(duration=0, redraw=False),
                                transition=dict(duration=0)
                                )],
                'label': date_list[k].strftime("%d/%m"),
                'method': 'animate',
                  } for k in range(nt)]}]

        # create magic
        #-------------
        fig.update(frames=frames),
        fig.update_layout(#updatemenus=updatemenus,
                          sliders=sliders,
                          title="ANGLET",
                          template="plotly_dark",
                          font=dict(
                              family="Arial",
                              size=15,
                              #color="Black",
                              ),
                          hovermode='x unified',
                          )

        # Save
        # -----
        config={"displayModeBar": False, "showTips": False}
        fig.write_html("test.html", config=config)